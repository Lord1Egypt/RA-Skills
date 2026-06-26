#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iFlow Internationalization (i18n) Module"""

from typing import Dict, Any, Optional
from pathlib import Path
import json


class Translator:
    """Simple internationalization translator"""
    
    def __init__(self, translations: Dict[str, Dict[str, Any]], default_lang: str = 'en'):
        self.translations = translations
        self.default_lang = default_lang
        self._current_lang = default_lang
    
    @classmethod
    def from_dir(cls, dir_path: str, default_lang: str = 'en') -> 'Translator':
        dir_path = Path(dir_path)
        translations = {}
        for lang_file in dir_path.glob('*.json'):
            with open(lang_file, 'r', encoding='utf-8') as f:
                translations[lang_file.stem] = json.load(f)
        return cls(translations, default_lang)
    
    def set_language(self, lang: str) -> None:
        if lang not in self.translations:
            raise ValueError(f"Language '{lang}' not available")
        self._current_lang = lang
    
    def translate(self, key: str, lang: Optional[str] = None, **kwargs) -> str:
        lang = lang or self._current_lang
        translation = self.translations.get(lang, {}).get(key)
        if translation is None:
            translation = self.translations.get(self.default_lang, {}).get(key, key)
        if kwargs:
            try:
                return translation.format(**kwargs)
            except KeyError:
                pass
        return translation
    
    def get_available_languages(self) -> list:
        return list(self.translations.keys())


# Global translator
_translator: Optional[Translator] = None

def init_translator(translations: Dict[str, Dict[str, Any]], default_lang: str = 'en') -> Translator:
    global _translator
    _translator = Translator(translations, default_lang)
    return _translator

def t(key: str, lang: Optional[str] = None, **kwargs) -> str:
    if _translator is None:
        return key
    return _translator.translate(key, lang, **kwargs)


# Common translations
COMMON = {
    'en': {
        'success': 'Success', 'error': 'Error', 'warning': 'Warning',
        'loading': 'Loading...', 'saving': 'Saving...', 'creating': 'Creating...',
        'cancel': 'Cancel', 'confirm': 'Confirm', 'save': 'Save', 'delete': 'Delete',
        'edit': 'Edit', 'create': 'Create', 'close': 'Close', 'back': 'Back',
        'next': 'Next', 'previous': 'Previous', 'submit': 'Submit', 'done': 'Done',
        'yes': 'Yes', 'no': 'No', 'ok': 'OK', 'retry': 'Retry', 'skip': 'Skip',
        'enabled': 'Enabled', 'disabled': 'Disabled', 'active': 'Active',
        'online': 'Online', 'offline': 'Offline', 'not_found': 'Not found',
    },
    'zh': {
        'success': '成功', 'error': '错误', 'warning': '警告',
        'loading': '加载中...', 'saving': '保存中...', 'creating': '创建中...',
        'cancel': '取消', 'confirm': '确认', 'save': '保存', 'delete': '删除',
        'edit': '编辑', 'create': '创建', 'close': '关闭', 'back': '返回',
        'next': '下一步', 'previous': '上一步', 'submit': '提交', 'done': '完成',
        'yes': '是', 'no': '否', 'ok': '确定', 'retry': '重试', 'skip': '跳过',
        'enabled': '已启用', 'disabled': '已禁用', 'active': '活跃',
        'online': '在线', 'offline': '离线', 'not_found': '未找到',
    }
}
