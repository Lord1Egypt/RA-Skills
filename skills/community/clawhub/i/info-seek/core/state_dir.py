#!/usr/bin/env python3
"""
core/state_dir.py — Infoseek 运行时数据目录集中解析（v3.1.1 新增）

把可变状态（claim / alias / entity 画像等 JSON）从技能源码目录（core/）剥离，
避免：① 技能更新时数据被覆盖；② 源码目录被运行时数据污染；③ 源码无法干净版本化。

目录解析优先级：
  1. INFOSEEK_DATA_DIR  显式数据目录
  2. INFOSEEK_DB        所在目录（.mcp.json 默认 ~/.infoseek/infoseek_db.json）
  3. ~/ .infoseek       兜底
"""

from __future__ import annotations

import os
from pathlib import Path


def get_data_dir() -> Path:
    """返回运行时数据目录（不存在则自动创建）。"""
    env = os.environ.get("INFOSEEK_DATA_DIR")
    if env:
        p = Path(env)
    else:
        db = os.environ.get("INFOSEEK_DB")
        p = Path(db).parent if db else (Path.home() / ".infoseek")
    p.mkdir(parents=True, exist_ok=True)
    return p


def state_path(filename: str) -> Path:
    """返回运行时状态文件的绝对路径（位于数据目录内）。"""
    return get_data_dir() / filename


def get_db_path() -> Path:
    """返回主数据库文件路径（INFOSEEK_DB 显式指定时原样使用）。"""
    env = os.environ.get("INFOSEEK_DB")
    return Path(env) if env else state_path("infoseek_db.json")


def get_log_path() -> Path:
    """返回主日志文件路径。"""
    return state_path("infoseek.log")


def audit_log_path() -> Path:
    """返回审计日志路径。"""
    return state_path("audit.log")


def get_archives_dir() -> Path:
    """返回归档目录（INFOSEEK_ARCHIVE 显式指定时使用；兜底 ~/infoseek-archives）。"""
    env = os.environ.get("INFOSEEK_ARCHIVE")
    p = Path(env) if env else (Path.home() / "infoseek-archives")
    p.mkdir(parents=True, exist_ok=True)
    return p
