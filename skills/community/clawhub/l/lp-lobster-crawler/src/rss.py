"""RSS/Atom 订阅源生成。"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from feedgen.feed import FeedGenerator

from src.models import Chapter, Novel, get_session


def generate_feed(
    site: str | None = None,
    grade: str | None = None,
    limit: int = 50,
    db_path: str | None = None,
) -> FeedGenerator:
    """生成 RSS feed。

    Args:
        site: 按站点过滤。
        grade: 按分级过滤。
        limit: 最大条目数。
        db_path: 数据库路径。

    Returns:
        FeedGenerator 实例。
    """
    session = get_session(db_path)

    fg = FeedGenerator()
    fg.title("龙虾爬虫更新订阅")
    fg.link(href="https://lobster-crawler.local/rss", rel="self")
    fg.description("龙虾平台内容更新 RSS 订阅源")
    fg.language("zh-CN")
    fg.lastBuildDate(datetime.now(timezone.utc))

    query = session.query(Novel)
    if site:
        query = query.filter_by(site=site)
    if grade:
        query = query.filter_by(grade=grade)

    novels = query.order_by(Novel.last_updated.desc()).limit(limit).all()

    for novel in novels:
        # 获取最新章节
        latest_chapters = (
            session.query(Chapter)
            .filter_by(novel_id=novel.id)
            .order_by(Chapter.created_at.desc())
            .limit(3)
            .all()
        )

        fe = fg.add_entry()
        fe.id(f"lobster-{novel.site}-{novel.external_id}")
        fe.title(f"[{novel.site}] {novel.title}")

        summary_parts = []
        if novel.author:
            summary_parts.append(f"作者: {novel.author}")
        if novel.category:
            summary_parts.append(f"分类: {novel.category}")
        summary_parts.append(f"状态: {novel.status}")
        summary_parts.append(f"分级: {novel.grade}")
        if latest_chapters:
            summary_parts.append(f"最新: {latest_chapters[0].title}")
        fe.summary("\n".join(summary_parts))

        if novel.url:
            fe.link(href=novel.url)
        if novel.last_updated:
            fe.updated(novel.last_updated.replace(tzinfo=timezone.utc))

    session.close()
    return fg


def write_rss(output_path: str | Path, **kwargs: Any) -> str:
    """生成 RSS XML 并写入文件。

    Args:
        output_path: 输出文件路径。
        **kwargs: 传递给 generate_feed 的参数。

    Returns:
        输出文件路径。
    """
    fg = generate_feed(**kwargs)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fg.rss_file(str(path))
    return str(path)


def write_atom(output_path: str | Path, **kwargs: Any) -> str:
    """生成 Atom XML 并写入文件。

    Args:
        output_path: 输出文件路径。
        **kwargs: 传递给 generate_feed 的参数。

    Returns:
        输出文件路径。
    """
    fg = generate_feed(**kwargs)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fg.atom_file(str(path))
    return str(path)
