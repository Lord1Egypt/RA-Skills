#!/usr/bin/env python3
"""习惯养成统计分析"""
import sqlite3
from collections import defaultdict

DB_PATH = '/home/istina/.openclaw/workspace/habit_education.db'

def get_overall_stats():
    """获取整体统计数据"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 习惯总数
    cursor.execute("SELECT COUNT(*) FROM habits")
    total = cursor.fetchone()[0]
    
    # 进行中/已归档
    cursor.execute("SELECT COUNT(*) FROM habits WHERE status = 'active'")
    active = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM habits WHERE status = 'archived'")
    archived = cursor.fetchone()[0]
    
    # 好/坏习惯
    cursor.execute("SELECT COUNT(*) FROM habits WHERE type = 'good'")
    good = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM habits WHERE type = 'bad'")
    bad = cursor.fetchone()[0]
    
    # 记忆等级分布
    cursor.execute("""
    SELECT memory_level, COUNT(*) 
    FROM (
        SELECT memory_level FROM habits WHERE memory_level IS NOT NULL
        UNION ALL
        SELECT memory_level FROM archived_habits_summary WHERE memory_level IS NOT NULL
    )
    GROUP BY memory_level
    """)
    memory_dist = dict(cursor.fetchall())
    
    conn.close()
    
    return {
        'total': total,
        'active': active,
        'archived': archived,
        'good': good,
        'bad': bad,
        'memory_distribution': memory_dist
    }

def get_habit_intervention_stats(habit_id):
    """获取某个习惯的干预统计"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT result, COUNT(*) 
    FROM intervention_records 
    WHERE habit_id = ?
    GROUP BY result
    """, (habit_id,))
    result_dist = dict(cursor.fetchall())
    
    cursor.execute("SELECT COUNT(*) FROM intervention_records WHERE habit_id = ?", (habit_id,))
    total_records = cursor.fetchone()[0]
    
    conn.close()
    return {'result_distribution': result_dist, 'total_records': total_records}

def get_contribution_stats():
    """获取付出记录统计"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT contributor, COUNT(*) FROM education_contributions GROUP BY contributor")
    by_contributor = dict(cursor.fetchall())
    
    cursor.execute("SELECT category, COUNT(*) FROM education_contributions GROUP BY category")
    by_category = dict(cursor.fetchall())
    
    cursor.execute("SELECT effort_level, COUNT(*) FROM education_contributions GROUP BY effort_level")
    by_effort = dict(cursor.fetchall())
    
    conn.close()
    return {
        'by_contributor': by_contributor,
        'by_category': by_category,
        'by_effort': by_effort
    }

if __name__ == '__main__':
    print("Usage: import from other scripts, not run directly")
