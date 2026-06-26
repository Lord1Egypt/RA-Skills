"""爬虫框架测试。"""

import os
import tempfile

import pytest

from src.spiders.items import ChapterItem, EpisodeItem, NovelItem
from src.spiders.pipelines import SQLitePipeline
from src.models import Novel, Chapter, Episode, init_db


class TestItems:
    def test_novel_item_fields(self):
        item = NovelItem(
            site="webnovel",
            external_id="123",
            title="Test",
            author="Author",
        )
        assert item["site"] == "webnovel"
        assert item["title"] == "Test"

    def test_chapter_item_fields(self):
        item = ChapterItem(
            site="webnovel",
            novel_external_id="123",
            external_id="ch1",
            index=1,
            title="Ch 1",
            content="Hello",
            word_count=5,
        )
        assert item["index"] == 1

    def test_episode_item_fields(self):
        item = EpisodeItem(
            site="reelshorts",
            novel_external_id="rs1",
            external_id="ep1",
            index=1,
            media_url="https://example.com/v.mp4",
            duration=120,
        )
        assert item["duration"] == 120


class TestSQLitePipeline:
    @pytest.fixture
    def pipeline_and_db(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        os.environ["DB_PATH"] = db_path

        from src.config import clear_cache
        clear_cache()

        pipeline = SQLitePipeline()

        class FakeSpider:
            name = "test"

        pipeline.open_spider(FakeSpider())
        yield pipeline, db_path

        pipeline.close_spider(FakeSpider())
        del os.environ["DB_PATH"]
        clear_cache()
        os.unlink(db_path)

    def test_process_novel_item(self, pipeline_and_db):
        pipeline, db_path = pipeline_and_db
        item = NovelItem(
            site="webnovel",
            external_id="n100",
            title="Pipeline Novel",
            author="Bot",
        )

        class FakeSpider:
            name = "test"

        result = pipeline.process_item(item, FakeSpider())
        assert result["title"] == "Pipeline Novel"

        # 验证入库
        session = init_db(db_path)
        novel = session.query(Novel).filter_by(external_id="n100").first()
        assert novel is not None
        assert novel.title == "Pipeline Novel"
        session.close()

    def test_process_chapter_item(self, pipeline_and_db):
        pipeline, db_path = pipeline_and_db

        class FakeSpider:
            name = "test"

        # 先插入小说
        novel_item = NovelItem(site="webnovel", external_id="n200", title="Parent Novel")
        pipeline.process_item(novel_item, FakeSpider())

        # 再插入章节
        ch_item = ChapterItem(
            site="webnovel",
            novel_external_id="n200",
            external_id="ch_200_1",
            index=1,
            title="Chapter One",
            content="Some text",
            word_count=9,
        )
        pipeline.process_item(ch_item, FakeSpider())

        session = init_db(db_path)
        chapter = session.query(Chapter).filter_by(external_id="ch_200_1").first()
        assert chapter is not None
        assert chapter.title == "Chapter One"
        session.close()
