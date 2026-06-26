#!/usr/bin/env python3
"""查询习惯状态"""
import sqlite3

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

def get_active_habits():
    """获取所有进行中习惯"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT h.id, h.name, h.type, h.memory_level, 
           (SELECT COUNT(*) FROM intervention_records WHERE habit_id = h.id) as record_count
    FROM habits h
    WHERE h.status = 'active'
    ORDER BY h.id
    """)
    habits = cursor.fetchall()
    conn.close()
    return habits

def get_archived_habits():
    """获取所有已归档习惯"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT ah.habit_id, h.name, ah.original_type, ah.memory_level, ah.final_success_rate, ah.archived_at
    FROM archived_habits_summary ah
    JOIN habits h ON h.id = ah.habit_id
    ORDER BY ah.habit_id
    """)
    habits = cursor.fetchall()
    conn.close()
    return habits

def get_intervention_records(habit_id):
    """获取某个习惯的所有干预记录"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT event_time, status_description, action_taken, result, handled_by, notes
    FROM intervention_records
    WHERE habit_id = ?
    ORDER BY event_time DESC
    """, (habit_id,))
    records = cursor.fetchall()
    conn.close()
    return records

def get_all_habits_summary():
    """获取全部习惯汇总（进行中+已归档）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 进行中
    cursor.execute("""
    SELECT h.id, h.name, h.type, h.status, h.memory_level
    FROM habits h
    WHERE h.status = 'active'
    ORDER BY h.id
    """)
    active = [{'id': r[0], 'name': r[1], 'type': r[2], 'status': r[3], 'memory_level': r[4]} for r in cursor.fetchall()]
    
    # 已归档
    cursor.execute("""
    SELECT h.id, h.name, h.type, h.status, ah.memory_level
    FROM habits h
    JOIN archived_habits_summary ah ON ah.habit_id = h.id
    WHERE h.status = 'archived'
    ORDER BY h.id
    """)
    archived = [{'id': r[0], 'name': r[1], 'type': r[2], 'status': r[3], 'memory_level': r[4]} for r in cursor.fetchall()]
    
    conn.close()
    return {'active': active, 'archived': archived}

if __name__ == '__main__':
    print("Usage: import from other scripts, not run directly")
