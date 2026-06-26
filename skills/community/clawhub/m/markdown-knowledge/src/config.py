#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件加载模块
统一管理配置路径兼容，避免多处复制
"""

import json
from pathlib import Path
from typing import Dict, List

# 动态检测实际安装路径（兼容 clawhub 安装到 workspace/skills）
_SELF_DIR = Path(__file__).parent.parent
SKILL_DIR = _SELF_DIR
OLD_SKILL_DIR = Path.home() / '.openclaw' / 'knowledge-base'
WORKSPACE_SKILL_DIR = Path.home() / '.openclaw' / 'workspace' / 'skills' / 'markdown-knowledge'


def get_config_paths() -> List[Path]:
    """返回配置文件的搜索路径列表（按优先级）"""
    return [
        SKILL_DIR / 'config.json',
        WORKSPACE_SKILL_DIR / 'config.json',
        OLD_SKILL_DIR / 'config.json',
    ]


def get_index_paths() -> List[Path]:
    """返回索引文件的搜索路径列表（按优先级）"""
    return [
        SKILL_DIR / 'index.json',
        WORKSPACE_SKILL_DIR / 'index.json',
        OLD_SKILL_DIR / 'index.json',
    ]


def get_default_config() -> Dict:
    """返回默认配置"""
    return {
        'knowledge_path': str(Path.home() / 'Knowledge'),
        'index_path': str(SKILL_DIR / 'index.json'),
        'search_top_k': 3,
        'auto_refresh': True,
        'refresh_interval': 3600,
        'exclude_patterns': ['.markdown', '.trash', '@Recycle', 'node_modules']
    }


def load_config() -> Dict:
    """加载配置文件

    优先路径：~/.openclaw/skills/markdown-knowledge/config.json
    兼容旧路径：~/.openclaw/knowledge-base/config.json（v1.0.0 旧版）
    """
    for config_path in get_config_paths():
        if config_path.exists():
            if config_path == OLD_SKILL_DIR / 'config.json':
                print(f"⚠️ 检测到旧版配置路径: {config_path}")
                print(f"   建议迁移至: {SKILL_DIR / 'config.json'}")
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    return get_default_config()


def resolve_index_path(config: Dict = None) -> Path:
    """解析 index_path，兼容新旧路径"""
    if config and config.get('index_path'):
        return Path(config['index_path']).expanduser()

    for ip in get_index_paths():
        if ip.exists():
            return ip
    return SKILL_DIR / 'index.json'
