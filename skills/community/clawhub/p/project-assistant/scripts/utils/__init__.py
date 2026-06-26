#!/usr/bin/env python3
"""
工具模块
提供缓存管理、调用链分析、Git信息获取等功能
"""

from .cache_manager import (
    CacheManager,
    CacheConfig,
    CacheEntry,
    cleanup_old_caches,
)
from .call_chain_analyzer import (
    CallChainAnalyzer,
    FunctionInfo,
    CallInfo,
)
from .git_info import (
    is_git_repo,
    get_branch,
    get_status,
    get_last_commit,
    get_recent_commits,
    get_contributors,
    get_file_history,
    get_remote_url,
    get_tags,
    get_full_info,
)
from .file_utils import (
    get_directory_tree,
    count_files_by_extension,
    format_size,
    generate_project_md,
    write_project_md,
    read_project_md,
)
from .qa_cache import (
    QACacheManager,
    QACacheEntry,
)
from .doc_generator import (
    DocGenerator,
)
from .logger import (
    get_logger,
    configure_logging,
    LoggerAdapter,
    create_logger,
)

__all__ = [
    # Cache manager
    'CacheManager',
    'CacheConfig',
    'CacheEntry',
    'cleanup_old_caches',
    # Call chain analyzer
    'CallChainAnalyzer',
    'FunctionInfo',
    'CallInfo',
    # Git info
    'is_git_repo',
    'get_branch',
    'get_status',
    'get_last_commit',
    'get_recent_commits',
    'get_contributors',
    'get_file_history',
    'get_remote_url',
    'get_tags',
    'get_full_info',
    # File utils
    'get_directory_tree',
    'count_files_by_extension',
    'format_size',
    'generate_project_md',
    'write_project_md',
    'read_project_md',
    # QA Cache
    'QACacheManager',
    'QACacheEntry',
    # Doc Generator
    'DocGenerator',
    # Logger
    'get_logger',
    'configure_logging',
    'LoggerAdapter',
    'create_logger',
]