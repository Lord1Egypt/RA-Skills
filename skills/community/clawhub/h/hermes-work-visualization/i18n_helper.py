#!/usr/bin/env python3
"""
Internationalization helper for work-visualization skill
Supports automatic language detection and bilingual output
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

# Language codes
LANG_ZH = "zh"
LANG_EN = "en"

# Default language
DEFAULT_LANG = LANG_EN


class I18NHelper:
    """Internationalization helper class"""

    def __init__(self, skill_path: Path):
        """
        Initialize I18N helper

        Args:
            skill_path: Path to the skill directory
        """
        self.skill_path = skill_path
        self.lang = self._detect_language()
        self.translations = self._load_translations()

    def _detect_language(self) -> str:
        """
        Detect user language based on environment variables

        Priority:
        1. HERMES_LANG environment variable (highest)
        2. LANG system variable
        3. Default (English)

        Returns:
            Language code ('zh' or 'en')
        """
        # Check HERMES_LANG first (highest priority)
        hermes_lang = os.environ.get('HERMES_LANG', '').lower()
        if hermes_lang:
            if hermes_lang.startswith(LANG_ZH):
                return LANG_ZH
            elif hermes_lang.startswith(LANG_EN):
                return LANG_EN

        # Check LANG system variable
        sys_lang = os.environ.get('LANG', '').lower()
        if sys_lang:
            if 'zh' in sys_lang or 'cn' in sys_lang:
                return LANG_ZH
            elif 'en' in sys_lang:
                return LANG_EN

        # Check LC_ALL
        lc_all = os.environ.get('LC_ALL', '').lower()
        if lc_all:
            if 'zh' in lc_all or 'cn' in lc_all:
                return LANG_ZH
            elif 'en' in lc_all:
                return LANG_EN

        # Default to English
        return DEFAULT_LANG

    def _load_translations(self) -> Dict[str, Any]:
        """
        Load translations from i18n.json file

        Returns:
            Dictionary containing all translations
        """
        i18n_file = self.skill_path / 'i18n.json'

        try:
            with open(i18n_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load translations: {e}")
            return {}

    def get(self, key: str, lang: str = None, default: str = None) -> str:
        """
        Get translated string by key

        Args:
            key: Translation key (e.g., 'output.title')
            lang: Language code (optional, defaults to detected language)
            default: Default value if key not found

        Returns:
            Translated string
        """
        if lang is None:
            lang = self.lang

        # Split key by dots
        keys = key.split('.')

        # Navigate through translation dictionary
        value = self.translations.get(lang, {})
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                break

        # Return value if found, otherwise try default language
        if value and isinstance(value, str):
            return value

        # Try default language as fallback
        if lang != DEFAULT_LANG:
            value = self.translations.get(DEFAULT_LANG, {})
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    break
            if value and isinstance(value, str):
                return value

        # Return default if provided, otherwise return the key itself
        return default if default is not None else key

    def t(self, key: str, default: str = None) -> str:
        """
        Shorthand for get()

        Args:
            key: Translation key
            default: Default value if key not found

        Returns:
            Translated string
        """
        return self.get(key, default=default)

    def get_language(self) -> str:
        """
        Get current language

        Returns:
            Language code ('zh' or 'en')
        """
        return self.lang

    def is_chinese(self) -> bool:
        """
        Check if current language is Chinese

        Returns:
            True if Chinese, False otherwise
        """
        return self.lang == LANG_ZH

    def is_english(self) -> bool:
        """
        Check if current language is English

        Returns:
            True if English, False otherwise
        """
        return self.lang == LANG_EN


# Global instance
_i18n_instance = None


def get_i18n(skill_path: Path = None) -> I18NHelper:
    """
    Get or create I18N helper instance

    Args:
        skill_path: Path to the skill directory (required for first call)

    Returns:
        I18NHelper instance
    """
    global _i18n_instance

    if _i18n_instance is None:
        if skill_path is None:
            # Try to auto-detect skill path
            skill_path = Path(__file__).parent.parent
        _i18n_instance = I18NHelper(skill_path)

    return _i18n_instance


def translate(key: str, default: str = None, skill_path: Path = None) -> str:
    """
    Translate a key (convenience function)

    Args:
        key: Translation key
        default: Default value if key not found
        skill_path: Path to the skill directory

    Returns:
        Translated string
    """
    i18n = get_i18n(skill_path)
    return i18n.get(key, default=default)


def get_language(skill_path: Path = None) -> str:
    """
    Get current language (convenience function)

    Args:
        skill_path: Path to the skill directory

    Returns:
        Language code ('zh' or 'en')
    """
    i18n = get_i18n(skill_path)
    return i18n.get_language()


if __name__ == "__main__":
    # Test the i18n helper
    print("Testing I18N Helper...")

    # Create instance
    i18n = I18NHelper(Path(__file__).parent.parent)

    print(f"Detected language: {i18n.get_language()}")
    print(f"Is Chinese: {i18n.is_chinese()}")
    print(f"Is English: {i18n.is_english()}")

    # Test translations
    print(f"\nTitle: {i18n.get('output.title')}")
    print(f"Task progress: {i18n.get('output.task_progress')}")
    print(f"Skill usage: {i18n.get('output.skill_usage')}")

    # Test with explicit language
    print(f"\nEnglish title: {i18n.get('output.title', lang='en')}")
    print(f"Chinese title: {i18n.get('output.title', lang='zh')}")
