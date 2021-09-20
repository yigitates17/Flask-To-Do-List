from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/itstajyer1/PycharmProjects/pythonProject/ToDo/todo_database.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)


@app.route('/')
def index():
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)


@app.route('/add', methods=["POST"])
def add():
    title = request.form.get("todo_title")
    newTodo = Todo(title=title, complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/complete/<string:todo_id>')
def complete(todo_id):
    completed = Todo.query.filter_by(id=todo_id).first()
    completed.complete = not completed.complete
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<string:todo_id>')
def delete(todo_id):
    deleted = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(deleted)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    db.create_all()
    app.config["SECRET_KEY"] = "QWERTY123"
    app.run(debug=True)
