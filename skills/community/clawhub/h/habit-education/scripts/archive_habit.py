#!/usr/bin/env python3
"""归档习惯"""
import sqlite3
from datetime import datetime

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

def archive_habit(habit_id, original_type, days_tracked, success_rate, summary, notes=None, subject=None, memory_level='长期习惯'):
    """归档一个习惯"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # 更新 habits 表状态
    cursor.execute('''
    UPDATE habits SET status = 'archived', archived_at = ?, memory_level = ?
    WHERE id = ?
    ''', (now, memory_level, habit_id))

    # 插入归档总结
    cursor.execute('''
    INSERT INTO archived_habits_summary
    (habit_id, original_type, archived_at, days_tracked, final_success_rate, summary, notes, subject, memory_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (habit_id, original_type, now, days_tracked, success_rate, summary, notes, subject, memory_level))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Usage: import from other scripts, not run directly")
