import sqlite3
import datetime

DB_NAME = "sniper.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Positions: market_id, side, size_usd, entry_price, tx_hash, pnl, timestamps
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_id TEXT,
            side TEXT,
            size_usd REAL,
            entry_price REAL,
            tx_hash TEXT,
            pnl REAL,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Logs: timestamp, level, event, message
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            event TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Heartbeats: Tracks liveness
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heartbeats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def log_event(level, event, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (level, event, message) VALUES (?, ?, ?)', (level, event, message))
    conn.commit()
    conn.close()

def record_position(market_id, side, size_usd, entry_price, tx_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO positions (market_id, side, size_usd, entry_price, tx_hash, status) VALUES (?, ?, ?, ?, ?, ?)', 
                   (market_id, side, size_usd, entry_price, tx_hash, "OPEN"))
    conn.commit()
    conn.close()

def send_heartbeat():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO heartbeats (timestamp) VALUES (?)', (datetime.datetime.now(),))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
