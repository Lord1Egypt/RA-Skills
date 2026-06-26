"""Lightweight i18n module for kiwi-voice.

Loads YAML locale files from kiwi/locales/ and provides
a simple t(key) translation function with dot-notation keys.
"""

import os
from typing import Any

import yaml

from kiwi import PROJECT_ROOT

_translations: dict = {}
_locale: str = "ru"
_fallback: str = "en"


def setup(locale: str = "ru", fallback: str = "en") -> None:
    """Initialize i18n with the given locale and fallback."""
    global _locale, _fallback, _translations
    _locale = locale
    _fallback = fallback
    _translations = {}

    locales_dir = os.path.join(PROJECT_ROOT, "kiwi", "locales")
    for lang in {fallback, locale}:
        path = os.path.join(locales_dir, f"{lang}.yaml")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                _translations[lang] = yaml.safe_load(f) or {}


def _resolve(key: str, data: dict) -> Any:
    """Resolve a dot-separated key in a nested dict."""
    parts = key.split(".")
    current = data
    for part in parts:
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def t(key: str, **kwargs) -> Any:
    """Get translated value by dot-notation key.

    Returns the value for the current locale, falling back
    to the fallback locale, then to the raw key string.
    Supports {placeholder} formatting via kwargs for str values.
    Returns lists/dicts as-is for non-string values.
    """
    result = _resolve(key, _translations.get(_locale, {}))
    if result is None:
        result = _resolve(key, _translations.get(_fallback, {}))
    if result is None:
        return key
    if isinstance(result, str) and kwargs:
        result = result.format(**kwargs)
    return result


def get_locale() -> str:
    """Return the current active locale code."""
    return _locale


def get_fallback() -> str:
    """Return the current fallback locale code."""
    return _fallback
