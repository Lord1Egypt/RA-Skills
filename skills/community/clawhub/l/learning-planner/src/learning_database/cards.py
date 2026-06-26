"""
复习卡片数据操作
"""
import json
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


def create_card(front: str, back: str, goal_id: int = None, tags: list = None) -> int:
    """创建复习卡片"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO cards (goal_id, front, back, tags)
        VALUES (?, ?, ?, ?)
    """, (goal_id, front, back, json.dumps(tags or [], ensure_ascii=False)))
    
    card_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return card_id


def get_card(card_id: int) -> dict:
    """获取卡片详情"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return _row_to_dict(row)
    return None


def list_cards(goal_id: int = None, limit: int = 50) -> list:
    """列出卡片"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if goal_id:
        cursor.execute("SELECT * FROM cards WHERE goal_id = ? LIMIT ?", (goal_id, limit))
    else:
        cursor.execute("SELECT * FROM cards LIMIT ?", (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def get_due_cards(limit: int = 20) -> list:
    """获取到期的复习卡片"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM cards 
        WHERE next_review IS NULL OR next_review <= ?
        ORDER BY next_review NULLS FIRST, repetitions
        LIMIT ?
    """, (today, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def get_new_cards(limit: int = 10) -> list:
    """获取新卡片（从未复习过）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM cards 
        WHERE repetitions = 0
        ORDER BY created_at
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def review_card(card_id: int, quality: int, time_spent: int = None):
    """
    复习卡片 - 使用 SM-2 算法
    quality: 0-5 的评分
    """
    card = get_card(card_id)
    if not card:
        return
    
    # SM-2 算法
    ease_factor = card.get("ease_factor", 2.5)
    repetitions = card.get("repetitions", 0)
    interval = card.get("interval", 0)
    
    # 更新难度系数
    ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    ease_factor = max(1.3, ease_factor)  # 最小 1.3
    
    if quality < 3:
        # 回答错误，重新开始
        repetitions = 0
        interval = 1
    else:
        # 回答正确
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = int(interval * ease_factor)
        repetitions += 1
    
    # 计算下次复习时间
    next_review = (datetime.now() + timedelta(days=interval)).strftime("%Y-%m-%d")
    
    # 更新卡片
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE cards 
        SET ease_factor = ?, interval = ?, repetitions = ?, 
            next_review = ?, last_review = date('now')
        WHERE id = ?
    """, (ease_factor, interval, repetitions, next_review, card_id))
    
    # 记录复习
    cursor.execute("""
        INSERT INTO reviews (card_id, quality, time_spent)
        VALUES (?, ?, ?)
    """, (card_id, quality, time_spent))
    
    conn.commit()
    conn.close()


def delete_card(card_id: int):
    """删除卡片"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()


def get_review_stats(days: int = 7) -> dict:
    """获取复习统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 总卡片数
    cursor.execute("SELECT COUNT(*) FROM cards")
    total_cards = cursor.fetchone()[0]
    
    # 今日到期
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
        SELECT COUNT(*) FROM cards 
        WHERE next_review IS NULL OR next_review <= ?
    """, (today,))
    due_today = cursor.fetchone()[0]
    
    # 最近复习次数
    cursor.execute("""
        SELECT COUNT(*) FROM reviews 
        WHERE reviewed_at >= date('now', ?)
    """, (_days_modifier(days),))
    recent_reviews = cursor.fetchone()[0]
    
    # 平均质量
    cursor.execute("""
        SELECT AVG(quality) FROM reviews 
        WHERE reviewed_at >= date('now', ?)
    """, (_days_modifier(days),))
    avg_quality = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return {
        "total_cards": total_cards,
        "due_today": due_today,
        "recent_reviews": recent_reviews,
        "avg_quality": round(avg_quality, 2),
    }


def get_all_tags() -> list:
    """获取所有标签"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT tags FROM cards WHERE tags IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    
    tags = set()
    for row in rows:
        try:
            card_tags = json.loads(row[0])
            tags.update(card_tags)
        except:
            pass
    
    return sorted(list(tags))


def _row_to_dict(row) -> dict:
    """将行转换为字典"""
    result = dict(row)
    if result.get("tags"):
        try:
            result["tags"] = json.loads(result["tags"])
        except:
            result["tags"] = []
    else:
        result["tags"] = []
    return result
