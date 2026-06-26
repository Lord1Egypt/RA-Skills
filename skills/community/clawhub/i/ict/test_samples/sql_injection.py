import sqlite3

def unsafe_query(user_input):
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    # 危险：直接拼接用户输入
    query = "SELECT * FROM users WHERE name = '" + user_input + "'"
    cursor.execute(query)
    return cursor.fetchall()
