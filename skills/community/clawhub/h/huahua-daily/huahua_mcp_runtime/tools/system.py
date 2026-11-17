"""system MCP tool implementations."""

import asyncio  # noqa: F401
import json  # noqa: F401
import os  # noqa: F401
import re  # noqa: F401
import time  # noqa: F401
from typing import Optional  # noqa: F401

from .binding import bind_runtime
from ..update_check import get_mcp_update_status

_RUNTIME_DEPENDENCIES = ("_OFFICIAL_API", "_clear_session_caches", "_get", "_require_token", "_session", "build_tool_manifest")

_EXPECTED_QUANT_SCHEMA_VERSION = "quant-v2"
_EXPECTED_STRATEGY_CONTEXT_SCHEMA_VERSION = "quant_strategy_context.v3"
_EXPECTED_AGENT_SCHEMA_VERSION = "agent-v1"
_EXPECTED_AGENT_IMPORT_REVIEW_SCHEMA_VERSION = "agent_import_review.v1"
_BACKEND_COMPATIBILITY_SUCCESS_TTL = 6 * 60 * 60
_BACKEND_COMPATIBILITY_FAILURE_TTL = 15 * 60
_backend_compatibility_cache: dict = {"value": None, "expires_at": 0.0}
_backend_compatibility_lock: Optional[asyncio.Lock] = None
_backend_compatibility_lock_loop: Optional[asyncio.AbstractEventLoop] = None

if False:  # pragma: no cover - populated by bind() before tool registration
    _OFFICIAL_API = None
    _clear_session_caches = None
    _get = None
    _require_token = None
    _session = None
    build_tool_manifest = None


def bind(runtime_globals: dict) -> None:
    global _backend_compatibility_cache
    global _backend_compatibility_lock, _backend_compatibility_lock_loop
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)
    _backend_compatibility_cache = {"value": None, "expires_at": 0.0}
    _backend_compatibility_lock = None
    _backend_compatibility_lock_loop = None


def _get_backend_compatibility_lock() -> asyncio.Lock:
    global _backend_compatibility_lock, _backend_compatibility_lock_loop
    loop = asyncio.get_running_loop()
    if (
        _backend_compatibility_lock is None
        or _backend_compatibility_lock_loop is not loop
    ):
        _backend_compatibility_lock = asyncio.Lock()
        _backend_compatibility_lock_loop = loop
    return _backend_compatibility_lock


async def set_token(token: str) -> str:
    """
    手动设置 Agent Token（运行时配置）。
    推荐通过环境变量 HUAHUA_AGENT_TOKEN 配置，无需调用此工具。

    Args:
        token: 从 App 设置页「Agent 访问令牌」中生成的令牌（PRO 会员专属）
    """
    normalized_token = str(token or "").strip()
    if not normalized_token:
        raise ValueError("Agent Token 不能为空")
    if len(normalized_token) > 4096:
        raise ValueError("Agent Token 过长")
    if any(ord(character) < 32 or ord(character) == 127 for character in normalized_token):
        raise ValueError("Agent Token 不能包含控制字符")
    _session["token"] = normalized_token
    _clear_session_caches()
    return f"✅ Token 已设置，将连接官方后端：{_session['base_url']}"


async def get_tool_manifest() -> dict:
    """
    返回本 MCP 服务的能力边界、认证方式和建议调用顺序。
    MCP 启动时会后台检查公开仓库版本；首次调用最多等待该检查 2 秒。
    同时以最多 2 秒读取后端量化与 Agent 能力握手，分别报告契约是否兼容。
    成功结果在进程内缓存 6 小时，失败结果 15 分钟后重试。
    更新检查失败只会标记 unavailable，不影响能力发现和后续业务工具。
    """
    update_status, backend_compatibility = await asyncio.gather(
        get_mcp_update_status(),
        _get_backend_compatibility(),
    )
    return build_tool_manifest(_OFFICIAL_API, update_status, backend_compatibility)


async def _get_backend_compatibility() -> dict:
    now = time.monotonic()
    cached = _backend_compatibility_cache["value"]
    if cached is not None and now < _backend_compatibility_cache["expires_at"]:
        return cached

    async with _get_backend_compatibility_lock():
        now = time.monotonic()
        cached = _backend_compatibility_cache["value"]
        if cached is not None and now < _backend_compatibility_cache["expires_at"]:
            return cached

        expected = {
            "quant": {
                "schemaVersion": _EXPECTED_QUANT_SCHEMA_VERSION,
                "strategyContextSchemaVersion": _EXPECTED_STRATEGY_CONTEXT_SCHEMA_VERSION,
            },
            "agentImports": {
                "schemaVersion": _EXPECTED_AGENT_SCHEMA_VERSION,
                "importReviewSchemaVersion": _EXPECTED_AGENT_IMPORT_REVIEW_SCHEMA_VERSION,
            },
        }
        try:
            quant_result, agent_result = await asyncio.wait_for(
                asyncio.gather(
                    _get("/api/quant/capabilities"),
                    _get("/api/agent/capabilities"),
                    return_exceptions=True,
                ),
                timeout=2,
            )
        except Exception:
            quant_result = agent_result = RuntimeError("capability handshake timeout")

        quant_unavailable = isinstance(quant_result, BaseException)
        agent_unavailable = isinstance(agent_result, BaseException)
        quant_invalid = not quant_unavailable and not isinstance(quant_result, dict)
        agent_invalid = not agent_unavailable and not isinstance(agent_result, dict)
        quant_capabilities = quant_result if isinstance(quant_result, dict) else None
        agent_capabilities = agent_result if isinstance(agent_result, dict) else None
        quant_features = quant_capabilities.get("features") if quant_capabilities else None
        quant_compatible = (
            quant_capabilities.get("schemaVersion") == _EXPECTED_QUANT_SCHEMA_VERSION
            and quant_capabilities.get("strategyContextSchemaVersion") == _EXPECTED_STRATEGY_CONTEXT_SCHEMA_VERSION
            and isinstance(quant_features, dict)
            and all(quant_features.get(name) is True for name in (
                "portfolioPerformance", "backtests", "quantSnapshots",
            ))
        ) if quant_capabilities is not None else False if quant_invalid else None
        agent_compatible = (
            agent_capabilities.get("schemaVersion") == _EXPECTED_AGENT_SCHEMA_VERSION
            and agent_capabilities.get("importReviewSchemaVersion") == _EXPECTED_AGENT_IMPORT_REVIEW_SCHEMA_VERSION
        ) if agent_capabilities is not None else False if agent_invalid else None

        component_compatibilities = (quant_compatible, agent_compatible)
        compatible = (
            False if False in component_compatibilities
            else True if all(value is True for value in component_compatibilities)
            else None
        )
        result = {
            "status": (
                "compatible" if compatible is True
                else "incompatible" if compatible is False
                else "unavailable"
            ),
            "compatible": compatible,
            "expected": expected,
            "reported": {
                "quant": quant_capabilities,
                "agentImports": agent_capabilities,
            },
            "components": {
                "quant": {
                    "status": (
                        "unavailable" if quant_unavailable
                        else "invalid" if quant_invalid
                        else "compatible" if quant_compatible
                        else "incompatible"
                    ),
                    "compatible": quant_compatible,
                },
                "agentImports": {
                    "status": (
                        "unavailable" if agent_unavailable
                        else "invalid" if agent_invalid
                        else "compatible" if agent_compatible
                        else "incompatible"
                    ),
                    "compatible": agent_compatible,
                },
            },
        }
        _backend_compatibility_cache["value"] = result
        ttl = (
            _BACKEND_COMPATIBILITY_SUCCESS_TTL
            if compatible is True
            else _BACKEND_COMPATIBILITY_FAILURE_TTL
        )
        _backend_compatibility_cache["expires_at"] = time.monotonic() + ttl
        return result


async def get_current_user() -> dict:
    """
    获取当前登录用户的账号信息（昵称、UID、会员状态等）。
    需要有效的 Agent Token（PRO 会员专属）。
    """
    _require_token()
    return await _get("/api/auth/me")


async def get_app_version() -> dict:
    """
    获取最新 App 版本信息，包括版本号、更新日志、下载地址、是否强制更新。
    适合回答"最新版本是多少""有什么新功能"等问题。
    """
    _require_token()
    return await _get("/api/version")


async def get_app_versions(page: int = 1, page_size: int = 5) -> dict:
    """
    获取 App 版本历史列表（分页，从新到旧）。
    适合查看历史更新记录。

    Args:
        page: 页码，从 1 开始
        page_size: 每页条数，1-20，默认 5
    """
    _require_token()
    return await _get("/api/versions", params={
        "page": max(1, page),
        "page_size": min(20, max(1, page_size)),
    })
