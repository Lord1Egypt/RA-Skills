"""Capability manifest for the public MCP surface."""

import os
from typing import Any

from .tool_registry import (
    CORE_PROFILE,
    FULL_PROFILE,
    TOOL_SPEC_BY_NAME,
    active_tool_specs,
    capabilities_for_profile,
    resolve_profile,
    tool_scopes_for_profile,
    tools_with_effect,
)
from .version import __version__


def _filter_safety_for_profile(safety: dict[str, Any], profile: str) -> dict[str, Any]:
    """Keep tool lists in the safety section aligned with the active profile."""
    if profile == FULL_PROFILE:
        return safety
    from .tool_registry import CORE_TOOLS

    filtered = dict(safety)
    for key in (
        "direct_state_change_tools",
        "confirmation_required_tools",
        "non_idempotent_toggle_tools",
        "destructive_tools",
    ):
        values = filtered.get(key)
        if isinstance(values, list):
            filtered[key] = [name for name in values if name in CORE_TOOLS]
    return filtered


def build_tool_manifest(
    official_api: str,
    update_status: dict[str, Any] | None = None,
    backend_compatibility: dict[str, Any] | None = None,
    profile: str | None = None,
) -> dict:
    """
    返回本 MCP 服务的能力边界、认证方式和建议调用顺序。
    可用于 Agent 在会话开始时自检。

    ``profile`` 显式传入时使用该值；否则从 ``HUAHUA_MCP_PROFILE`` 解析，
    默认 ``full``。非法显式值回退到环境解析（与 tool_registry 一致）。
    """
    if profile not in {CORE_PROFILE, FULL_PROFILE}:
        profile = None
    active_profile = resolve_profile() if profile is None else profile
    remote = os.environ.get("HUAHUA_MCP_REMOTE", "").strip().lower() in {
        "1", "true", "yes", "on",
    }
    return {
        "name": "huahua-daily",
        "transport": "streamable-http" if remote else "stdio",
        "profile": active_profile,
        "runtime": {
            "version": __version__,
            "updateCheck": update_status or {
                "status": "not_checked",
                "currentVersion": __version__,
                "latestVersion": None,
                "updateAvailable": None,
            },
        },
        "auth": (
            {
                "requestHeader": "Authorization: Bearer <Agent Token>",
                "tokenStorage": "request_context_only",
            }
            if remote
            else {
                "primary_env": "HUAHUA_AGENT_TOKEN",
                "header": "Authorization: AgentToken <token>",
            }
        ),
        "api_base": official_api,
        "backendCompatibility": backend_compatibility or {
            "status": "not_checked",
            "compatible": None,
        },
        "toolScopes": tool_scopes_for_profile(active_profile),
        "toolMetadata": {
            spec.name: {
                "domain": spec.domain,
                "profile": spec.profile,
                "payloadClass": spec.payload_class,
                "deprecated": spec.deprecated,
            }
            for spec in active_tool_specs(active_profile)
        },
        "capabilities": capabilities_for_profile(active_profile),
        "safety": _filter_safety_for_profile({
            "direct_trading": False,
            "trade_flow": "request_transaction 支持买入金额、卖出金额/份额和精确分组，只创建待确认信号，必须由用户在 App 内确认。",
            "trade_request_idempotency": "同一交易或导入请求重试时复用 client_request_id；服务端按当前用户在 7 天窗口内去重。",
            "agent_request_update_boundary": "MCP 只能把待确认请求标记为 DISMISSED；PROCESSED 必须由 App 在用户确认后设置。",
            "direct_state_change_tools": tools_with_effect(active_profile, "state_change"),
            "confirmation_required_tools": tools_with_effect(active_profile, "confirmation_required"),
            "non_idempotent_toggle_tools": tools_with_effect(active_profile, "non_idempotent_toggle"),
            "personal_report_write": True,
            "personal_report_flow": "submit_personal_strategy_report 只写入当前 Agent Token 所属用户的报告中心；不能指定 user_id 或广播。",
            "personal_report_required_scope": TOOL_SPEC_BY_NAME["submit_personal_strategy_report"].scope,
            "quant_snapshot_write": True,
            "quant_snapshot_write_boundary": "仅归档 token 所属用户的策略观察；真实持仓、组合版本和内容哈希由服务端捕获，不保存建议金额。",
            "quant_data_basis": "单基金指标使用官方净值 D 日；组合回放使用 linked_daily_return_v1 的 G 日归属；QDII 夜盘仅作执行参考；回测零费率；不宣称严格 point-in-time。",
            "public_report_write": False,
            "cloud_sync_read": "get_records/get_summary/get_raw_sync_data 读取云端实时同步主数据；固定使用结构化组合接口，不读取云端历史备份快照。",
            "portfolio_freshness": "组合新鲜度只看 portfolioUpdatedAt（原始接口为 meta.portfolio_updated_at）；data.timestamp 是客户端谱系/迁移元数据，不得作为同步时间。",
            "valuation_basis": "marketValue 使用不晚于北京时间今日的最新官方净值锚点：优先比较行情帧 dwjz/last_nav_date 与组合快照 lastNav/lastNavDate；estimatedNav 只进入 estimatedMarketValue，不进入官方市值。",
            "estimate_timeout_handling": "timeout、stale last-good 或 estimateDecision=unavailable 的帧不参与当日收益；检查 summary.estimateCompleteness，不能把不可用帧的 0 元当成真实零涨跌。",
            "cloud_sync_write": False,
            "cloud_history_snapshot_write": False,
            "empty_portfolio_restore": "已确认的空组合主数据会被识别为合法可恢复状态，但 MCP 不提供恢复或覆盖写入工具。",
            "destructive_tools": [],
        }, active_profile),
    }
