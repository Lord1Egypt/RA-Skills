"""
hermes-memory-bridge / config.py
路径、常量与日志配置

支持环境变量覆盖：
  HERMES_HOME         - Hermes 根目录（默认 ~/.hermes）
  WORKBUDDY_HOME     - WorkBuddy 根目录（默认 ~/WorkBuddy）
  BRIDGE_LOG_LEVEL   - 日志级别 DEBUG|INFO|WARNING|ERROR（默认 INFO）
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Optional

# ─── 版本 ────────────────────────────────────────────────────────────
__version__ = "1.1.0"

# ─── 日志初始化（所有模块共享）───────────────────────────────────────
_log_level = os.getenv("BRIDGE_LOG_LEVEL", "INFO").upper()
_log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(
    level=getattr(logging, _log_level, logging.INFO),
    format=_log_format,
    stream=sys.stderr,
)
logger = logging.getLogger("hermes-memory-bridge")


def _get_logger(name: str) -> logging.Logger:
    """获取子模块 logger"""
    return logging.getLogger(f"hermes-memory-bridge.{name}")


# ─── Hermes 路径（支持 HERMES_HOME 环境变量）────────────────────────
def _resolve_hermes_home() -> Path:
    env = os.getenv("HERMES_HOME", "").strip()
    if env:
        p = Path(env)
        if not p.is_dir():
            logger.warning(f"HERMES_HOME={env} 不存在或不是目录，使用默认值 ~/.hermes")
            p = Path.home() / ".hermes"
    else:
        p = Path.home() / ".hermes"
    return p


HERMES_HOME: Path = _resolve_hermes_home()
HERMES_MEMORIES_DIR: Path = HERMES_HOME / "memories"
HERMES_DB: Path = HERMES_HOME / "state.db"

# ─── 共用互通目录 ────────────────────────────────────────────────────
SHARED_DIR: Path = HERMES_HOME / "shared"
WORKBUDDY_LOG: Path = SHARED_DIR / "workbuddy.log"
HERMES_LOG: Path = SHARED_DIR / "hermes.log"
BRIDGE_META: Path = SHARED_DIR / "meta.json"

# ─── WorkBuddy 路径（智能查找，支持 WORKBUDDY_HOME 环境变量）──────────

def get_workbuddy_memory_dir() -> Optional[Path]:
    """
    动态查找 WorkBuddy 记忆目录。

    优先级：
    1. WORKBUDDY_MEMORY_DIR 环境变量（完整路径）
    2. WORKBUDDY_HOME 环境变量 → 其下找最新时间戳子目录
    3. ~/WorkBuddy → 找最新时间戳子目录 → .workbuddy/memory

    Returns:
        Path 或 None（均找不到时返回 None，不抛异常）
    """
    # 优先级 1：直接指定
    env_mem = os.getenv("WORKBUDDY_MEMORY_DIR", "").strip()
    if env_mem:
        p = Path(env_mem)
        if p.is_dir():
            logger.debug(f"使用 WORKBUDDY_MEMORY_DIR={p}")
            return p
        logger.warning(f"WORKBUDDY_MEMORY_DIR={env_mem} 不存在或不是目录")

    # 优先级 2：WORKBUDDY_HOME
    wb_home = os.getenv("WORKBUDDY_HOME", "").strip()
    if not wb_home:
        wb_home = str(Path.home() / "WorkBuddy")
    wb_root = Path(wb_home)

    if not wb_root.is_dir():
        logger.warning(f"WorkBuddy 根目录不存在: {wb_root}，记忆搜索功能将受限")
        return None

    # 找最新子目录（格式为纯数字时间戳）
    try:
        subdirs = [
            d for d in wb_root.iterdir()
            if d.is_dir() and d.name.isdigit() and len(d.name) >= 10
        ]
    except PermissionError as e:
        logger.warning(f"读取 {wb_root} 权限不足: {e}")
        return None

    if not subdirs:
        logger.warning(f"{wb_root} 下未找到 WorkBuddy 项目子目录，记忆搜索功能将受限")
        return None

    latest = max(subdirs, key=lambda d: d.name)
    memory_dir = latest / ".workbuddy" / "memory"
    logger.debug(f"自动发现 WorkBuddy 目录: {latest.name}，记忆目录: {memory_dir}")
    return memory_dir


WORKBUDDY_MEMORY_DIR: Optional[Path] = get_workbuddy_memory_dir()

# ─── 常量 ────────────────────────────────────────────────────────────
ENTRY_DELIMITER = "\n§\n"
MAX_ENTRY_CHARS = 4000
MAX_EVENTS = 100  # meta.json 中保留的最大事件条数
