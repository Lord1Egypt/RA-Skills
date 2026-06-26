"""基于数据库的增量去重过滤器。

在 Scrapy 内置 RFPDupeFilter（URL 级去重）之上，增加内容级去重：
- 章节级别：检查 chapter.external_id 是否已存在
- 作品级别：检查 novel.last_updated 是否有新内容

可与 Scrapy DupeFilter 叠加使用。
"""

import logging
from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from src.models import Chapter, Episode, Novel, get_session

logger = logging.getLogger(__name__)


class IncrementalChecker:
    """增量检查器 — 判断内容是否需要抓取。"""

    def __init__(self, db_path: str | None = None) -> None:
        self._session: Session | None = None
        self._db_path = db_path

    def open(self) -> None:
        """初始化数据库连接。"""
        from src.models import init_db
        self._session = init_db(self._db_path)

    def close(self) -> None:
        """关闭数据库连接。"""
        if self._session:
            self._session.close()

    def is_chapter_new(self, site: str, novel_external_id: str, chapter_external_id: str) -> bool:
        """判断章节是否为新章节。

        Args:
            site: 站点名称。
            novel_external_id: 作品外部 ID。
            chapter_external_id: 章节外部 ID。

        Returns:
            True 表示是新章节，需要抓取。
        """
        if not self._session:
            return True

        novel = (
            self._session.query(Novel)
            .filter_by(site=site, external_id=novel_external_id)
            .first()
        )
        if not novel:
            return True

        existing = (
            self._session.query(Chapter)
            .filter_by(novel_id=novel.id, external_id=chapter_external_id)
            .first()
        )
        return existing is None

    def is_episode_new(self, site: str, novel_external_id: str, episode_external_id: str) -> bool:
        """判断剧集是否为新剧集。"""
        if not self._session:
            return True

        novel = (
            self._session.query(Novel)
            .filter_by(site=site, external_id=novel_external_id)
            .first()
        )
        if not novel:
            return True

        existing = (
            self._session.query(Episode)
            .filter_by(novel_id=novel.id, external_id=episode_external_id)
            .first()
        )
        return existing is None

    def get_last_chapter_index(self, site: str, novel_external_id: str) -> int:
        """获取作品最新章节序号。

        Returns:
            最大章节 index，无章节时返回 0。
        """
        if not self._session:
            return 0

        novel = (
            self._session.query(Novel)
            .filter_by(site=site, external_id=novel_external_id)
            .first()
        )
        if not novel:
            return 0

        from sqlalchemy import func
        result = (
            self._session.query(func.max(Chapter.index))
            .filter_by(novel_id=novel.id)
            .scalar()
        )
        return result or 0

    def get_novel_last_updated(self, site: str, novel_external_id: str) -> datetime | None:
        """获取作品最后更新时间。"""
        if not self._session:
            return None

        novel = (
            self._session.query(Novel)
            .filter_by(site=site, external_id=novel_external_id)
            .first()
        )
        return novel.last_updated if novel else None
