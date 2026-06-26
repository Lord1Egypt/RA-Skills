"""Novel / Chapter / Episode 数据模型。"""

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Novel(Base):
    """小说/作品模型。"""

    __tablename__ = "novels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    site: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    external_id: Mapped[str] = mapped_column(String(200), nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    author: Mapped[str] = mapped_column(String(200), default="")
    category: Mapped[str] = mapped_column(String(100), default="")
    status: Mapped[str] = mapped_column(String(50), default="ongoing")
    summary: Mapped[str] = mapped_column(Text, default="")
    cover_url: Mapped[str] = mapped_column(String(1000), default="")
    url: Mapped[str] = mapped_column(String(1000), default="")
    grade: Mapped[str] = mapped_column(String(20), default="low")
    last_updated: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    chapters: Mapped[list["Chapter"]] = relationship(
        back_populates="novel", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("site", "external_id", name="uq_novel_site_extid"),
    )

    def __repr__(self) -> str:
        return f"<Novel(id={self.id}, site={self.site!r}, title={self.title!r})>"


class Chapter(Base):
    """章节模型（用于小说类站点）。"""

    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    novel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("novels.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_id: Mapped[str] = mapped_column(String(200), nullable=False)
    index: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(500), default="")
    content: Mapped[str] = mapped_column(Text, default="")
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    novel: Mapped["Novel"] = relationship(back_populates="chapters")

    __table_args__ = (
        UniqueConstraint("novel_id", "external_id", name="uq_chapter_novel_extid"),
    )

    def __repr__(self) -> str:
        return f"<Chapter(id={self.id}, novel_id={self.novel_id}, title={self.title!r})>"


class Episode(Base):
    """剧集模型（用于短剧类站点，如 ReelShorts）。"""

    __tablename__ = "episodes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    novel_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("novels.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_id: Mapped[str] = mapped_column(String(200), nullable=False)
    index: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str] = mapped_column(String(500), default="")
    media_url: Mapped[str] = mapped_column(String(1000), default="")
    duration: Mapped[int] = mapped_column(Integer, default=0)
    thumbnail_url: Mapped[str] = mapped_column(String(1000), default="")
    publish_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    novel: Mapped["Novel"] = relationship()

    __table_args__ = (
        UniqueConstraint("novel_id", "external_id", name="uq_episode_novel_extid"),
    )

    def __repr__(self) -> str:
        return f"<Episode(id={self.id}, novel_id={self.novel_id}, title={self.title!r})>"
