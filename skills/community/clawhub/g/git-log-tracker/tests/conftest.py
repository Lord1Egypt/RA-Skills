"""跨阶段通用 fixture（方案 B）。

本文件提供所有阶段共享的 mock 数据 fixture，以及 sys.path 注入兜底——
使测试无论从仓库根还是 src/ 下运行都能 import flat 布局的源码模块。
"""

import sys
from pathlib import Path

import pytest

# src/ 注入兜底：源码为 flat 布局（cli/db/config/hook/models 直接在 src/ 下），
# 用 `from db import ...` 等方式互相 import，必须保证 src/ 在 sys.path。
SRC = Path(__file__).resolve().parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


@pytest.fixture
def sample_commit() -> dict:
    """一条规范化的 commit 元数据（与 hook.get_commit_info 输出同形）。"""
    return {
        "commit_hash": "a" * 40,
        "short_hash": "aaaaaaa",
        "author_name": "Alice",
        "author_email": "alice@example.com",
        "author_ts": "2026-06-01T12:00:00+08:00",
        "committer_name": "Alice",
        "committer_email": "alice@example.com",
        "commit_subject": "feat: 初始提交",
        "commit_body": "正文内容",
        "branch": "master",
        "parent_hashes": None,
    }


@pytest.fixture
def git_log_output() -> str:
    """模拟 `git log -1 --format=...` 的标准输出。

    字段顺序与 hook.get_commit_info 一致：H h an ae aI cn ce s P D b
    （body 放最后以支持多行）。
    """
    return "\n".join([
        "a" * 40,                          # %H
        "aaaaaaa",                         # %h
        "Alice",                           # %an
        "alice@example.com",               # %ae
        "2026-06-01T12:00:00+08:00",       # %aI
        "Alice",                           # %cn
        "alice@example.com",               # %ce
        "feat: 初始提交",                   # %s
        "",                                # %P (无父，首次提交)
        "HEAD -> master, origin/master",   # %D
        "正文内容",                         # %b
    ])
