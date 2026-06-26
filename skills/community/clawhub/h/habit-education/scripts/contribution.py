#!/usr/bin/env python3
"""记录教育付出"""
import sqlite3
from datetime import datetime

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

CATEGORIES = [
    '习惯干预', '思想教育', '习惯养成引导', '教育基础设施',
    '生涯规划', '内容管控', '金融教育', '兴趣引导', '其他'
]

EFFORT_LEVELS = ['low', 'medium', 'high']

def add_contribution(contributor, category, description, effort_level, happened_at, notes=None):
    """记录一条教育付出"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    cursor.execute('''
    INSERT INTO education_contributions
    (contributor, category, description, effort_level, happened_at, notes, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (contributor, category, description, effort_level, happened_at, notes, now))

    conn.commit()
    conn.close()
    return cursor.lastrowid

def get_all_contributions():
    """获取所有付出记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, contributor, category, description FROM education_contributions ORDER BY id")
    records = cursor.fetchall()
    conn.close()
    return records

if __name__ == '__main__':
    print("Usage: import from other scripts, not run directly")
