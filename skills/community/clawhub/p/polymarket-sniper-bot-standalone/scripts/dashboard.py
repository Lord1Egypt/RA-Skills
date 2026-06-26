from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "sniper.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    if not os.path.exists(DB_NAME):
        return "Database not initialized. Please run scripts/bootstrap.sh first."
    
    conn = get_db_connection()
    
    # Recent 50 positions, 100 logs
    positions = conn.execute('SELECT * FROM positions ORDER BY timestamp DESC LIMIT 50').fetchall()
    logs = conn.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100').fetchall()
    heartbeats = conn.execute('SELECT * FROM heartbeats ORDER BY timestamp DESC LIMIT 5').fetchall()
    
    conn.close()
    
    return render_template('index.html', positions=positions, logs=logs, heartbeats=heartbeats)

if __name__ == '__main__':
    print("Dashboard starting at http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)
