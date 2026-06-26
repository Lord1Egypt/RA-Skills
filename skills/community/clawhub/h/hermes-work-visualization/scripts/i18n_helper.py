#!/usr/bin/env python3
"""
语言检测和翻译模块
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

# 配置路径
I18N_FILE = Path(__file__).parent.parent / "i18n.json"

def load_i18n_config() -> Dict:
    """加载i18n配置"""
    with open(I18N_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def detect_language() -> str:
    """检测用户语言设置"""
    config = load_i18n_config()

    # 1. 检查环境变量
    env_var = config.get('language_detection', {}).get('env_var', 'HERMES_LANG')
    lang_from_env = os.environ.get(env_var)
    if lang_from_env:
        return lang_from_env

    # 2. 检查系统语言环境变量
    system_lang = os.environ.get('LANG', '').lower()
    if system_lang.startswith('zh'):
        return 'zh'
    elif system_lang.startswith('en'):
        return 'en'

    # 3. 使用默认语言或fallback
    default = config.get('default_language', 'auto')
    if default != 'auto':
        return default

    fallback = config.get('language_detection', {}).get('fallback', 'zh')
    return fallback

def get_text(key: str, lang: Optional[str] = None) -> str:
    """获取指定语言的文本"""
    if not lang:
        lang = detect_language()

    config = load_i18n_config()
    ui_config = config.get('ui', {}).get(lang, {})

    # 递归查找嵌套键
    keys = key.split('.')
    value = ui_config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, key)
        else:
            return key

    return value if value != key else key

def get_all_texts(lang: str) -> Dict:
    """获取指定语言的所有文本"""
    config = load_i18n_config()
    return config.get('ui', {}).get(lang, {})

def is_supported_language(lang: str) -> bool:
    """检查是否支持该语言"""
    config = load_i18n_config()
    return lang in config.get('available_languages', [])
