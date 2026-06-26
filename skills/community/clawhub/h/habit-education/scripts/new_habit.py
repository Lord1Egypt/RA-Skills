#!/usr/bin/env python3
"""插入新习惯并记录首次干预"""
import sqlite3
import sys
from datetime import datetime

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

def check_duplicate(name):
    """检查是否有语义重复的习惯"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, type, status FROM habits WHERE status = 'active'")
    active = cursor.fetchall()
    conn.close()
    return active

def insert_habit(name, htype, created_by, subject, event_time, status_desc, action_taken, result, handled_by, notes=None):
    """插入新习惯并记录首次干预"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d')

    cursor.execute('''
    INSERT INTO habits (name, type, created_by, status, created_at, subject)
    VALUES (?, ?, ?, 'active', ?, ?)
    ''', (name, htype, created_by, today, subject))
    habit_id = cursor.lastrowid

    cursor.execute('''
    INSERT INTO intervention_records
    (habit_id, event_time, status_description, action_taken, result, handled_by, notes, recorded_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (habit_id, event_time, status_desc, action_taken, result, handled_by, notes, now))

    conn.commit()
    conn.close()
    return habit_id

if __name__ == '__main__':
    # 用法示例
    print("Usage: import from other scripts, not run directly")
