"""
学习目标数据操作
"""
import json
from datetime import datetime, timedelta
from .connection import get_connection


def create_goal(title: str, description: str = None, parent_id: int = None,
                priority: str = "medium", deadline: str = None, 
                estimated_hours: int = 0) -> int:
    """创建学习目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO goals (title, description, parent_id, priority, deadline, estimated_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (title, description, parent_id, priority, deadline, estimated_hours))
    
    goal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return goal_id


def get_goal(goal_id: int) -> dict:
    """获取目标详情"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM goals WHERE id = ?", (goal_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def list_goals(parent_id=None, status=None) -> list:
    """列出目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if parent_id is not None:
        cursor.execute("SELECT * FROM goals WHERE parent_id = ? ORDER BY priority, created_at", 
                       (parent_id,))
    elif status:
        cursor.execute("SELECT * FROM goals WHERE status = ? ORDER BY priority, created_at", 
                       (status,))
    else:
        cursor.execute("SELECT * FROM goals WHERE parent_id IS NULL ORDER BY priority, created_at")
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def update_goal(goal_id: int, data: dict):
    """更新目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed_fields = ["title", "description", "priority", "status", "progress", 
                      "deadline", "estimated_hours", "completed_hours"]
    
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            values.append(data[field])
    
    if not updates:
        conn.close()
        return
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    values.append(goal_id)
    
    query = f"UPDATE goals SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def delete_goal(goal_id: int):
    """删除目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
    conn.commit()
    conn.close()


def get_subgoals(goal_id: int) -> list:
    """获取子目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM goals WHERE parent_id = ? ORDER BY priority, created_at", 
                   (goal_id,))
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def update_progress(goal_id: int, progress: float):
    """更新目标进度"""
    progress = max(0, min(100, progress))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    status = "completed" if progress >= 100 else "active"
    
    cursor.execute("""
        UPDATE goals SET progress = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (progress, status, goal_id))
    
    conn.commit()
    conn.close()
    
    # 更新父目标进度
    goal = get_goal(goal_id)
    if goal and goal.get("parent_id"):
        _update_parent_progress(goal["parent_id"])


def _update_parent_progress(parent_id: int):
    """更新父目标进度"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT AVG(progress) FROM goals WHERE parent_id = ?", (parent_id,))
    avg_progress = cursor.fetchone()[0] or 0
    
    status = "completed" if avg_progress >= 100 else "active"
    
    cursor.execute("""
        UPDATE goals SET progress = ?, status = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (avg_progress, status, parent_id))
    
    conn.commit()
    conn.close()


def get_goal_tree(goal_id: int = None) -> list:
    """获取目标树"""
    goals = list_goals(parent_id=goal_id)
    
    for goal in goals:
        goal["children"] = get_goal_tree(goal["id"])
    
    return goals


def get_stats() -> dict:
    """获取目标统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 总目标数
    cursor.execute("SELECT COUNT(*) FROM goals")
    total = cursor.fetchone()[0]
    
    # 各状态数量
    cursor.execute("SELECT status, COUNT(*) FROM goals GROUP BY status")
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 平均进度
    cursor.execute("SELECT AVG(progress) FROM goals")
    avg_progress = cursor.fetchone()[0] or 0
    
    # 即将到期（7天内）
    cursor.execute("""
        SELECT COUNT(*) FROM goals 
        WHERE status = 'active' 
        AND deadline IS NOT NULL 
        AND deadline <= date('now', '+7 days')
    """)
    due_soon = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "active": status_counts.get("active", 0),
        "completed": status_counts.get("completed", 0),
        "paused": status_counts.get("paused", 0),
        "avg_progress": round(avg_progress, 2),
        "due_soon": due_soon,
    }
