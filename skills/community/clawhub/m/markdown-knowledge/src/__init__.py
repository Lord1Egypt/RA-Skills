# Markdown Knowledge Base for OpenClaw
# 将您的 Markdown 知识库与 OpenClaw 无缝集成

__version__ = '1.1.1'
__author__ = 'aaronjager92'
__license__ = 'MIT'

# 核心类
from .knowledge_core import DocumentParser, IndexBuilder, KnowledgeSearcher

# OpenClaw 动作
from .actions import action_search, action_build, action_stats, action_check

# 配置
from .config import load_config, resolve_index_path, get_default_config

__all__ = [
    # 版本信息
    '__version__',
    '__author__',
    '__license__',
    # 核心类
    'DocumentParser',
    'IndexBuilder',
    'KnowledgeSearcher',
    # 动作函数
    'action_search',
    'action_build',
    'action_stats',
    'action_check',
    # 配置工具
    'load_config',
    'resolve_index_path',
    'get_default_config',
]
