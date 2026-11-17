#!/usr/bin/env python3
"""
ecosystem/adapters/agentkey.py — AgentKey 统一 MCP 网关适配器（v1.0.0 · P1b）

AgentKey（Chainbase）：一个主密钥 → ~1800 工具（搜索/社交/金融/加密/电商），
MCP 协议交付：find_tools → describe_tool → execute_tool。

本适配器：
  1. 生态适配器（EcosystemAdapter）：向 infoseek 声明触发/采集/凭据/状态/输出契约
  2. MCP 客户端骨架：find_tools / describe_tool / execute_tool 封装
     - mcp 库可用 → stdio/HTTP 直连（生产路径）
     - mcp 库缺失 → 优雅降级 CapabilityUnavailable（不中断 pipeline）
  3. 金融子集白名单：Finance（Tushare/Yahoo/Finnhub）优先接入，社交默认 OFF

注册：ecosystem/registry.py 的 adapter_names 追加 'agentkey'
合规：requires_consent=true（registry.yaml），涉社交/个人数据必须显式授权
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..base import EcosystemAdapter

# ── 能力常量 ──
CAP_NAME = "AgentKey"
AUTH_ENV = "AGENTKEY_API_KEY"

# 金融子集白名单（默认接入；社交类别需 consent 授权后手动扩）
TOOL_CATEGORIES = {
    "finance": ["Finance", "Market Data", "Stock", "Forex", "Crypto Market"],
    "search": ["Search", "Web Search"],
    "social": ["Social", "Twitter", "Reddit", "YouTube"],   # 默认 OFF
}


class AgentKeyError(Exception):
    """AgentKey 调用错误基类。code 与 engine_lifecycle.classify 兼容（429→quota/401→forbidden）。"""
    def __init__(self, message: str = "", code: Optional[int] = None):
        super().__init__(message or self.__class__.__name__)
        self.code = code


class AgentKeyQuotaError(AgentKeyError):
    def __init__(self, message: str = "AgentKey credits exhausted", code: int = 429):
        super().__init__(message, code)


class AgentKeyAuthError(AgentKeyError):
    def __init__(self, message: str = "AgentKey unauthorized", code: int = 401):
        super().__init__(message, code)


class AgentKeyUnavailable(AgentKeyError):
    """mcp 库缺失 / 网关不可达（非致命，由 pipeline 降级）。"""
    def __init__(self, message: str = "AgentKey unavailable", code: Optional[int] = None):
        super().__init__(message, code)


class AgentKeyAdapter(EcosystemAdapter):
    name = 'agentkey'
    display_name = 'AgentKey'

    # ── 生态契约（base.EcosystemAdapter 五件套）──
    def trigger_spec(self) -> dict:
        return {
            'mode': 'tool_declaration',
            'detail': 'infoseek 三级路由 L1 网关层；registry.yaml 声明 gateway_api',
            'entry': 'scripts/tiered_router.py（L1 分支）',
        }

    def collection_spec(self) -> dict:
        return {
            'mode': 'external',
            'inject_sources': False,
            'builtin_fallback': True,
            'detail': 'MCP find_tools→describe_tool→execute_tool；金融子集白名单优先',
        }

    def credential_spec(self) -> dict:
        return {
            'required_env': [AUTH_ENV],
            'optional_env': ['INFOSEEK_AGENTKEY_TIMEOUT'],
            'detail': '主 API key（console.agentkey.app 获取）；MCP 网关统一认证',
        }

    def state_spec(self) -> dict:
        return {
            'data_dir': '~/.infoseek（env 可覆盖）',
            'archives_dir': '~/infoseek-archives',
            'local_persistence': False,
            'remote_capable': True,
        }

    def output_spec(self) -> dict:
        return {
            'format': 'json',
            'delivery': '结构化工具输出（对齐 infoseek 锚点 schema）',
            'archive': False,
        }


# ═══════════════════════════════════════════════════════════════
# MCP 客户端骨架
# ═══════════════════════════════════════════════════════════════

def _mcp_available() -> bool:
    try:
        import mcp  # noqa: F401
        return True
    except Exception:
        return False


def _require_key() -> None:
    if not os.environ.get(AUTH_ENV):
        raise AgentKeyUnavailable(f"{AUTH_ENV} 未配置")


def _gate(subset: str = "finance") -> None:
    """合规闸口：社交子集必须显式授权（consent）。"""
    if subset in ("social",):
        from core.capability_registry import is_effective_enabled, requires_consent, consent_granted  # noqa: F401
        if requires_consent(CAP_NAME) and not consent_granted(CAP_NAME):
            raise AgentKeyAuthError("AgentKey-Social 需显式 consent 授权（涉个人数据）")


def find_tools(query: str, subset: str = "finance", limit: int = 10) -> List[Dict]:
    """发现可用工具（find_tools）。mcp 库缺失 → 优雅降级。"""
    _require_key()
    _gate(subset)
    if not _mcp_available():
        raise AgentKeyUnavailable("mcp 库未安装（pip install mcp）；骨架降级")
    # ── 生产路径：mcp stdio/HTTP 直连（接入时补）──
    raise AgentKeyUnavailable("find_tools 生产实现待接入（骨架）")


def describe_tool(tool_id: str) -> Dict:
    """查看工具详情（describe_tool）。"""
    _require_key()
    if not _mcp_available():
        raise AgentKeyUnavailable("mcp 库未安装")
    raise AgentKeyUnavailable("describe_tool 生产实现待接入（骨架）")


def execute_tool(tool_id: str, parameters: Optional[dict] = None) -> Dict:
    """执行工具（execute_tool）。429→quota / 401→forbidden 与 engine_lifecycle 兼容。"""
    _require_key()
    if not _mcp_available():
        raise AgentKeyUnavailable("mcp 库未安装")
    raise AgentKeyUnavailable("execute_tool 生产实现待接入（骨架）")


def search(query: str, subset: str = "finance", max_results: int = 5) -> List[Dict]:
    """高层入口：find_tools → (预算内) execute_tool，输出对齐 infoseek 锚点。

    返回 [{url, title, snippet, score, source, tool_id, provider, cost}]
    失败/未接入 → 上抛 AgentKeyUnavailable（由 tiered_router 降级链兜底）
    """
    _require_key()
    _gate(subset)
    tools = find_tools(query, subset=subset, limit=max_results)
    out: List[Dict] = []
    for t in tools[:max_results]:
        tid = t.get("tool_id") or t.get("id") or ""
        desc = describe_tool(tid)
        if not desc.get("enabled", True):
            continue
        res = execute_tool(tid, {})  # 参数按工具 schema 由调用方填充
        out.append({
            "url": f"agentkey://exec/{tid}",
            "title": t.get("name", tid),
            "snippet": str(res)[:200],
            "score": 80,
            "source": "AgentKey",
            "tool_id": tid,
            "provider": t.get("provider", ""),
            "cost": t.get("cost", 0),
        })
    return out


# 供 registry.py 自动发现
def _register():
    return AgentKeyAdapter
