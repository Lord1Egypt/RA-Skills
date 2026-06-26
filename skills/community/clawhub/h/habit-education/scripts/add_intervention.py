#!/usr/bin/env python3
"""追加干预记录"""
import sqlite3
from datetime import datetime

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

def add_intervention(habit_id, event_time, status_desc, action_taken, result, handled_by, notes=None):
    """追加一条干预记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    cursor.execute('''
    INSERT INTO intervention_records
    (habit_id, event_time, status_description, action_taken, result, handled_by, notes, recorded_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (habit_id, event_time, status_desc, action_taken, result, handled_by, notes, now))

    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_active_habits():
    """获取所有进行中习惯"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type FROM habits WHERE status = 'active' ORDER BY id")
    habits = cursor.fetchall()
    conn.close()
    return habits

if __name__ == '__main__':
    print("Usage: import from other scripts, not run directly")
