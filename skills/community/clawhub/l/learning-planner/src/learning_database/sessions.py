"""
学习时长记录数据操作
"""
from datetime import datetime, timedelta
from .connection import get_connection


def _days_modifier(days: int, max_days: int = 3650) -> str:
    try:
        value = int(days)
    except (TypeError, ValueError) as exc:
        raise ValueError("days must be an integer") from exc
    if value < 0 or value > max_days:
        raise ValueError(f"days must be between 0 and {max_days}")
    return f"-{value} days"


def start_session(goal_id: int, notes: str = None) -> int:
    """开始学习会话"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO sessions (goal_id, notes)
        VALUES (?, ?)
    """, (goal_id, notes))
    
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id


def end_session(session_id: int):
    """结束学习会话"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取开始时间
    cursor.execute("SELECT start_time FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    
    if row:
        start_time = datetime.fromisoformat(row[0])
        end_time = datetime.now()
        duration = int((end_time - start_time).total_seconds() / 60)
        
        cursor.execute("""
            UPDATE sessions 
            SET end_time = ?, duration = ?
            WHERE id = ?
        """, (end_time.strftime("%Y-%m-%d %H:%M:%S"), duration, session_id))
        
        # 更新目标已完成时长
        cursor.execute("SELECT goal_id FROM sessions WHERE id = ?", (session_id,))
        goal_row = cursor.fetchone()
        if goal_row:
            cursor.execute("""
                UPDATE goals 
                SET completed_hours = completed_hours + ?
                WHERE id = ?
            """, (duration / 60, goal_row[0]))
        
        conn.commit()
    
    conn.close()


def get_session(session_id: int) -> dict:
    """获取会话详情"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def list_sessions(goal_id: int = None, days: int = 7) -> list:
    """列出学习记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if goal_id:
        cursor.execute("""
            SELECT * FROM sessions 
            WHERE goal_id = ? AND start_time >= date('now', ?)
            ORDER BY start_time DESC
        """, (goal_id, _days_modifier(days)))
    else:
        cursor.execute("""
            SELECT * FROM sessions 
            WHERE start_time >= date('now', ?)
            ORDER BY start_time DESC
        """, (_days_modifier(days),))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_total_time(goal_id: int = None, days: int = 7) -> int:
    """获取总学习时长（分钟）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if goal_id:
        cursor.execute("""
            SELECT SUM(duration) FROM sessions 
            WHERE goal_id = ? AND start_time >= date('now', ?)
        """, (goal_id, _days_modifier(days)))
    else:
        cursor.execute("""
            SELECT SUM(duration) FROM sessions 
            WHERE start_time >= date('now', ?)
        """, (_days_modifier(days),))
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] or 0


def get_daily_stats(days: int = 7) -> list:
    """获取每日学习统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            date(start_time) as day,
            SUM(duration) as total_minutes,
            COUNT(*) as session_count
        FROM sessions 
        WHERE start_time >= date('now', ?)
        GROUP BY day
        ORDER BY day
    """, (_days_modifier(days),))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_active_goals_today() -> list:
    """获取今日活跃的学习目标"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT DISTINCT g.* FROM goals g
        JOIN sessions s ON g.id = s.goal_id
        WHERE date(s.start_time) = ?
        ORDER BY g.priority
    """, (today,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]
