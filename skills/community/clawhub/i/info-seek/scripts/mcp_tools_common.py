#!/usr/bin/env python3
"""mcp_tools_common.py — Infoseek MCP 工具公共层（G11 拆分 v1.0.1）

集中管理工具模块共享的：路径常量 / 状态目录 / 认证配置 / 审计状态 / 公共辅助。
被 mcp_tools_search / mcp_tools_archive / mcp_tools_analysis / mcp_tools_keys /
mcp_tools_async 与门面 infoseek_mcp_server.py 共同引用（单一事实源）。
"""
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

# ── 路径常量（v1.0.0 状态层中立：运行态数据统一位于 ~/.infoseek 或 env 指定目录，
#    不再绑定 skill 安装目录 / WORKSPACE，适配只读与临时安装平台）──
CORE_DIR = Path(__file__).parent.parent / 'core'
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from state_dir import (
    get_data_dir, get_db_path, get_log_path,
    audit_log_path, get_archives_dir,
)

WORKSPACE = Path(os.environ.get('OPENCLAW_WORKSPACE', str(Path.home())))
INFOSEEK_ROOT = Path(os.environ.get('INFOSEEK_ROOT', str(Path(__file__).parent.parent)))
INFOSEEK_DIR = get_data_dir()
DB_PATH = get_db_path()
LOG_PATH = get_log_path()
ARCHIVES_DIR = get_archives_dir()

# ── 认证配置（v1.5.1+）──
AUTH_TOKEN = os.environ.get('INFOSEEK_AUTH_TOKEN')
PROTOCOL_VERSION = "2024-11-05"  # MCP 协议版本
SERVER_NAME = "infoseek-search"
# ══ 版本单源（v1.8.1 治理）═══════════════════════════════════════════
# SKILL_VERSION = 全仓唯一对外版本真源（single source of truth）。
# 消费点：SERVER_VERSION（本文件）→ infoseek_mcp_server / infoseek_archive_server
#         → core/__init__.__version__ → SKILL.md / manifest.yaml / CHANGELOG.md
#         → RELEASE_NOTES.md
# 另有三个不同维度的版本，禁止与 SKILL_VERSION 比较大小或混用：
#   · mod-v   模块内部版本（domain_router mod-v1.8.1 / anchor_score_v2 mod-v2.0.2）
#   · algo-v  算法与结果体版本（infoseek_core_v2 返回体 'version': '1.2.0'）
#   · proto-v 协议版本（PROTOCOL_VERSION = MCP 协议；v3.0.0 = 流式 yield 协议）
# 一致性由 tests/test_version_single_source.py 守护。
SKILL_VERSION = "2.6.1"

SERVER_VERSION = SKILL_VERSION  # MCP serverInfo.version（对外协议应答，随真源）

# ── v1.6.2 新增：审计日志 + 工具调用统计 ──
SERVER_START_TIME = time.time()  # 启动时间
TOOL_CALL_COUNTER = {}  # 工具调用计数（按工具名）
AUDIT_LOG_PATH = audit_log_path()


def ensure_dirs():
    INFOSEEK_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVES_DIR.mkdir(parents=True, exist_ok=True)


def mask_token(token: str) -> str:
    """Token 脱敏：只保留前 4 与后 4 位（v1.6.1 PATCH，防日志泄漏）"""
    if not token:
        return '(none)'
    if len(token) <= 8:
        return token[:2] + '***'
    return f"{token[:4]}...{token[-4:]}"
