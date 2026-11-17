"""Tests for i18n module."""
import sys; sys.path.insert(0, "src")

from perplexity_toolkit.utils.i18n import (
    get_ui_string, get_skip_prefixes, get_skip_keywords,
    UI_STRINGS, SKIP_PREFIXES, SKIP_ANSWER_KEYWORDS,
)


class TestGetUiString:
    def test_zh_deep_research(self):
        assert get_ui_string("deep_research", "zh") == "深度研究"

    def test_en_deep_research(self):
        assert get_ui_string("deep_research", "en") == "Deep Research"

    def test_zh_completed(self):
        assert get_ui_string("completed", "zh") == "已完成"

    def test_en_completed(self):
        assert get_ui_string("completed", "en") == "Completed"

    def test_unknown_locale_falls_back_to_zh(self):
        assert get_ui_string("deep_research", "fr") == "深度研究"

    def test_unknown_key_returns_key(self):
        assert get_ui_string("nonexistent_key", "zh") == "nonexistent_key"


class TestSkipPrefixes:
    def test_zh_prefixes(self):
        prefs = get_skip_prefixes("zh")
        assert "答案" in prefs
        assert "已完成" in prefs

    def test_en_prefixes(self):
        prefs = get_skip_prefixes("en")
        assert "Answer" in prefs
        assert "Completed" in prefs

    def test_unknown_locale(self):
        prefs = get_skip_prefixes("fr")
        assert prefs == SKIP_PREFIXES["zh"]


class TestSkipKeywords:
    def test_zh_keywords(self):
        kw = get_skip_keywords("zh")
        assert "分享" in kw

    def test_en_keywords(self):
        kw = get_skip_keywords("en")
        assert "Share" in kw


class TestUiStrings:
    def test_zh_and_en_have_same_keys(self):
        zh_keys = set(UI_STRINGS["zh"].keys())
        en_keys = set(UI_STRINGS["en"].keys())
        assert zh_keys == en_keys


class TestConsoleProbeLabels:
    """The three labels console.py matches on (studied pill / expand / chip prefix)."""

    def test_key_exists_in_both_locales(self):
        for key in ("studied", "expand", "remove_prefix"):
            assert key in UI_STRINGS["zh"]
            assert key in UI_STRINGS["en"]

    def test_studied_zh_en(self):
        assert get_ui_string("studied", "zh") == "已研究"
        # en value is a completion-form label matching 「已研究」; not live-verified
        assert get_ui_string("studied", "en") == "Researched"

    def test_expand_zh_en(self):
        assert get_ui_string("expand", "zh") == "展开"
        assert get_ui_string("expand", "en") == "Expand"

    def test_remove_prefix_zh_en(self):
        assert get_ui_string("remove_prefix", "zh") == "移除 "
        assert get_ui_string("remove_prefix", "en") == "Remove "

    def test_legacy_expand_label_is_the_existing_show_more(self):
        assert get_ui_string("show_more", "zh") == "查看更多"
        assert get_ui_string("show_more", "en") == "Show more"
