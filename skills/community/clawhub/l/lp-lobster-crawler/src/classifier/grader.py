"""内容分级引擎。

根据更新频率和热度对作品进行三级分类：
- high: 高优先级 — 频繁更新的热门作品，触发即时播报
- medium: 中优先级 — 常规更新作品，日汇总播报
- low: 低优先级 — 更新缓慢或完结作品，周汇总播报
"""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from src.config import get_setting
from src.models import Chapter, Episode, Novel


# 分级常量
GRADE_HIGH = "high"
GRADE_MEDIUM = "medium"
GRADE_LOW = "low"


def grade_novel(novel: Novel, session: Session) -> str:
    """对单部作品进行分级。

    Args:
        novel: Novel 模型实例。
        session: 数据库 session。

    Returns:
        分级结果："high" / "medium" / "low"。
    """
    now = datetime.utcnow()

    # 从配置读取阈值
    high_days = get_setting("classifier", "high", "min_update_frequency_days", default=2)
    medium_days = get_setting("classifier", "medium", "min_update_frequency_days", default=7)

    # 1. 基于最后更新时间
    if novel.last_updated:
        days_since_update = (now - novel.last_updated).days
        if days_since_update <= high_days:
            return GRADE_HIGH
        if days_since_update <= medium_days:
            return GRADE_MEDIUM

    # 2. 基于近期章节/剧集数量（作为补充指标）
    recent_count = _count_recent_content(novel, session, days=high_days)
    if recent_count >= 3:
        return GRADE_HIGH

    recent_count_week = _count_recent_content(novel, session, days=medium_days)
    if recent_count_week >= 1:
        return GRADE_MEDIUM

    # 3. 已完结作品降为低优先
    if novel.status in ("completed", "finished", "ended"):
        return GRADE_LOW

    return GRADE_LOW


def grade_all(session: Session) -> dict[str, list[Novel]]:
    """对数据库中所有作品进行分级。

    Args:
        session: 数据库 session。

    Returns:
        {grade: [Novel, ...]} 字典。
    """
    novels = session.query(Novel).all()
    result: dict[str, list[Novel]] = {
        GRADE_HIGH: [],
        GRADE_MEDIUM: [],
        GRADE_LOW: [],
    }

    for novel in novels:
        grade = grade_novel(novel, session)
        # 更新数据库中的分级
        if novel.grade != grade:
            novel.grade = grade
        result[grade].append(novel)

    session.commit()
    return result


def get_update_frequency(novel: Novel, session: Session, days: int = 30) -> float:
    """计算作品在过去 N 天的平均更新频率（每天更新次数）。

    Args:
        novel: Novel 实例。
        session: 数据库 session。
        days: 统计的天数范围。

    Returns:
        每日平均更新次数。
    """
    since = datetime.utcnow() - timedelta(days=days)
    count = _count_recent_content(novel, session, days=days)
    return count / max(days, 1)


def _count_recent_content(novel: Novel, session: Session, days: int = 7) -> int:
    """统计作品近期新增内容数量。"""
    since = datetime.utcnow() - timedelta(days=days)

    chapter_count = (
        session.query(Chapter)
        .filter(
            Chapter.novel_id == novel.id,
            Chapter.created_at >= since,
        )
        .count()
    )

    episode_count = (
        session.query(Episode)
        .filter(
            Episode.novel_id == novel.id,
            Episode.created_at >= since,
        )
        .count()
    )

    return chapter_count + episode_count
