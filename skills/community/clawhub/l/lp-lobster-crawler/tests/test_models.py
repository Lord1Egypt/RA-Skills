"""数据模型测试。"""

import os
import tempfile

import pytest

from src.models import Base, Chapter, Episode, Novel, get_engine, init_db


@pytest.fixture
def db_session():
    """创建临时数据库并返回 session。"""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    try:
        session = init_db(db_path)
        yield session
        session.close()
    finally:
        os.unlink(db_path)


class TestNovel:
    def test_create_novel(self, db_session):
        novel = Novel(
            site="webnovel",
            external_id="12345",
            title="Test Novel",
            author="Test Author",
            category="Fantasy",
            status="ongoing",
        )
        db_session.add(novel)
        db_session.commit()

        result = db_session.query(Novel).first()
        assert result.title == "Test Novel"
        assert result.site == "webnovel"
        assert result.external_id == "12345"

    def test_unique_constraint(self, db_session):
        novel1 = Novel(site="webnovel", external_id="111", title="Novel A")
        novel2 = Novel(site="webnovel", external_id="111", title="Novel B")
        db_session.add(novel1)
        db_session.commit()
        db_session.add(novel2)
        with pytest.raises(Exception):
            db_session.commit()


class TestChapter:
    def test_create_chapter_with_novel(self, db_session):
        novel = Novel(site="webnovel", external_id="100", title="My Novel")
        db_session.add(novel)
        db_session.commit()

        chapter = Chapter(
            novel_id=novel.id,
            external_id="ch_1",
            index=1,
            title="Chapter 1",
            content="Hello world",
            word_count=11,
        )
        db_session.add(chapter)
        db_session.commit()

        result = db_session.query(Chapter).first()
        assert result.novel_id == novel.id
        assert result.title == "Chapter 1"
        assert result.novel.title == "My Novel"

    def test_cascade_delete(self, db_session):
        novel = Novel(site="webnovel", external_id="200", title="Del Novel")
        db_session.add(novel)
        db_session.commit()

        chapter = Chapter(novel_id=novel.id, external_id="ch_del", index=1)
        db_session.add(chapter)
        db_session.commit()

        db_session.delete(novel)
        db_session.commit()
        assert db_session.query(Chapter).count() == 0


class TestEpisode:
    def test_create_episode(self, db_session):
        novel = Novel(site="reelshorts", external_id="rs_1", title="Short Drama")
        db_session.add(novel)
        db_session.commit()

        episode = Episode(
            novel_id=novel.id,
            external_id="ep_1",
            index=1,
            title="Episode 1",
            media_url="https://example.com/video.mp4",
            duration=120,
        )
        db_session.add(episode)
        db_session.commit()

        result = db_session.query(Episode).first()
        assert result.title == "Episode 1"
        assert result.duration == 120
