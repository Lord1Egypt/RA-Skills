"""Tests for the i18n module."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwi.i18n import setup, t, get_locale, get_fallback


def test_setup_sets_locale():
    setup("en", fallback="ru")
    assert get_locale() == "en"
    assert get_fallback() == "ru"


def test_setup_loads_translations():
    setup("en", fallback="ru")
    result = t("wake_word.keyword")
    assert result is not None
    assert isinstance(result, str)


def test_t_returns_key_on_missing():
    setup("en", fallback="ru")
    result = t("nonexistent.key.path")
    assert result == "nonexistent.key.path"


def test_t_supports_placeholder_formatting():
    setup("en", fallback="ru")
    result = t("responses.heard", command="test command")
    assert "test command" in result


def test_t_returns_list_for_list_values():
    setup("en", fallback="ru")
    result = t("hallucinations.phrases")
    assert isinstance(result, list)
    assert len(result) > 0


def test_t_returns_dict_for_dict_values():
    setup("en", fallback="ru")
    result = t("wake_word.typos")
    assert isinstance(result, dict)


def test_fallback_locale():
    setup("en", fallback="ru")
    # Both locales should have wake_word.keyword
    result = t("wake_word.keyword")
    assert result != "wake_word.keyword"


def test_all_locales_load():
    """Verify all 15 locale YAML files load without errors."""
    locales = ["en", "ru", "es", "pt", "fr", "it", "de", "tr", "pl", "zh", "ja", "ko", "hi", "ar", "id"]
    for locale in locales:
        setup(locale, fallback="en")
        result = t("wake_word.keyword")
        assert result != "wake_word.keyword", f"Locale {locale} failed to load wake_word.keyword"


def test_all_locales_have_required_sections():
    """Verify all locales have the core sections."""
    required_keys = [
        "wake_word.keyword",
        "responses.greeting",
        "responses.heard",
        "commands.stop",
    ]
    locales = ["en", "ru", "es", "pt", "fr", "it", "de", "tr", "pl", "zh", "ja", "ko", "hi", "ar", "id"]
    for locale in locales:
        setup(locale, fallback="en")
        for key in required_keys:
            result = t(key)
            assert result != key, f"Locale {locale} missing key: {key}"
