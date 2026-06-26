"""播报模块测试。"""

from unittest.mock import MagicMock

from src.broadcast.templates import (
    get_broadcast_strategy,
    render_daily_digest,
    render_immediate,
    render_weekly_digest,
)


class TestTemplates:
    def _make_novel(self, **kwargs):
        novel = MagicMock()
        novel.title = kwargs.get("title", "Test Novel")
        novel.site = kwargs.get("site", "webnovel")
        novel.author = kwargs.get("author", "Author")
        novel.grade = kwargs.get("grade", "high")
        novel.status = kwargs.get("status", "ongoing")
        novel.url = kwargs.get("url", "https://example.com/book/1")
        return novel

    def test_render_immediate(self):
        novel = self._make_novel(title="My Novel")
        chapters = [MagicMock(title=f"Ch {i}") for i in range(1, 4)]
        result = render_immediate(novel, chapters=chapters, new_count=3)

        assert "My Novel" in result
        assert "3 章/集" in result
        assert "Ch 1" in result

    def test_render_daily_digest(self):
        items = [
            {"novel": self._make_novel(title="Novel A"), "new_count": 5},
            {"novel": self._make_novel(title="Novel B"), "new_count": 2},
        ]
        result = render_daily_digest(items)

        assert "今日更新汇总" in result
        assert "Novel A" in result
        assert "Novel B" in result

    def test_render_weekly_digest(self):
        items = [
            {"novel": self._make_novel(title="Weekly Novel"), "new_count": 10},
        ]
        result = render_weekly_digest(items)

        assert "本周更新汇总" in result
        assert "Weekly Novel" in result


class TestStrategy:
    def test_high_is_immediate(self):
        assert get_broadcast_strategy("high") == "immediate"

    def test_medium_is_daily(self):
        assert get_broadcast_strategy("medium") == "daily_digest"

    def test_low_is_weekly(self):
        assert get_broadcast_strategy("low") == "weekly_digest"

    def test_unknown_defaults_weekly(self):
        assert get_broadcast_strategy("unknown") == "weekly_digest"
