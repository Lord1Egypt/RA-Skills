"""Scrapy Pipeline — 数据入库。"""

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from src.models import Chapter, Episode, Novel, init_db
from src.config import get_setting


class SQLitePipeline:
    """将爬取的 Item 存入 SQLite 数据库。"""

    def __init__(self) -> None:
        self.session: Session | None = None

    def open_spider(self, spider: Any) -> None:
        db_path = get_setting("database", "path", default="data/lobster.db")
        self.session = init_db(db_path)

    def close_spider(self, spider: Any) -> None:
        if self.session:
            self.session.close()

    def process_item(self, item: dict[str, Any], spider: Any) -> dict[str, Any]:
        if self.session is None:
            return item

        item_type = type(item).__name__

        if item_type == "NovelItem":
            self._upsert_novel(item)
        elif item_type == "ChapterItem":
            self._upsert_chapter(item)
        elif item_type == "EpisodeItem":
            self._upsert_episode(item)

        return item

    def _upsert_novel(self, item: dict[str, Any]) -> None:
        """插入或更新小说。"""
        assert self.session is not None
        existing = (
            self.session.query(Novel)
            .filter_by(site=item["site"], external_id=item["external_id"])
            .first()
        )
        if existing:
            for field in ("title", "author", "category", "status", "summary", "cover_url", "url"):
                if item.get(field):
                    setattr(existing, field, item[field])
            existing.last_updated = datetime.utcnow()
        else:
            novel = Novel(
                site=item["site"],
                external_id=item["external_id"],
                title=item.get("title", ""),
                author=item.get("author", ""),
                category=item.get("category", ""),
                status=item.get("status", "ongoing"),
                summary=item.get("summary", ""),
                cover_url=item.get("cover_url", ""),
                url=item.get("url", ""),
                last_updated=datetime.utcnow(),
            )
            self.session.add(novel)
        self.session.commit()

    def _upsert_chapter(self, item: dict[str, Any]) -> None:
        """插入或更新章节。"""
        assert self.session is not None
        novel = (
            self.session.query(Novel)
            .filter_by(site=item["site"], external_id=item["novel_external_id"])
            .first()
        )
        if not novel:
            return

        existing = (
            self.session.query(Chapter)
            .filter_by(novel_id=novel.id, external_id=item["external_id"])
            .first()
        )
        if existing:
            for field in ("title", "content", "word_count"):
                if item.get(field):
                    setattr(existing, field, item[field])
        else:
            chapter = Chapter(
                novel_id=novel.id,
                external_id=item["external_id"],
                index=item.get("index", 0),
                title=item.get("title", ""),
                content=item.get("content", ""),
                word_count=item.get("word_count", 0),
                publish_date=item.get("publish_date"),
            )
            self.session.add(chapter)
        novel.last_updated = datetime.utcnow()
        self.session.commit()

    def _upsert_episode(self, item: dict[str, Any]) -> None:
        """插入或更新剧集。"""
        assert self.session is not None
        novel = (
            self.session.query(Novel)
            .filter_by(site=item["site"], external_id=item["novel_external_id"])
            .first()
        )
        if not novel:
            return

        existing = (
            self.session.query(Episode)
            .filter_by(novel_id=novel.id, external_id=item["external_id"])
            .first()
        )
        if existing:
            for field in ("title", "media_url", "duration", "thumbnail_url"):
                if item.get(field):
                    setattr(existing, field, item[field])
        else:
            episode = Episode(
                novel_id=novel.id,
                external_id=item["external_id"],
                index=item.get("index", 0),
                title=item.get("title", ""),
                media_url=item.get("media_url", ""),
                duration=item.get("duration", 0),
                thumbnail_url=item.get("thumbnail_url", ""),
                publish_date=item.get("publish_date"),
            )
            self.session.add(episode)
        novel.last_updated = datetime.utcnow()
        self.session.commit()
