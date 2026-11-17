"""Public MCP tool ordering and registration.

Framework v2 (2026-08): tools are annotated with a profile (``core`` / ``full``)
and cancelled tools are removed from the registry. ``HUAHUA_MCP_PROFILE`` selects
the active surface; the default remains ``full`` so existing deployments keep
every compatible tool. Cancelled tools are not registered at all.
"""

import os
from dataclasses import dataclass
from typing import Optional

from .tools import community, fund, import_tools, market, portfolio, portfolio_actions, quant, reports, system


CORE_PROFILE = "core"
FULL_PROFILE = "full"
DEFAULT_PROFILE = FULL_PROFILE
PROFILE_ENV = "HUAHUA_MCP_PROFILE"

# Tools cancelled in framework v2. Kept for one release window in the changelog
# so agents still running older SKILL instructions can reconcile; they are not
# registered and return unknown-tool errors from hosts.
REMOVED_TOOLS = frozenset({
    "get_app_versions",
    "get_indices",
    "get_danmaku",
    "send_danmaku",
    "get_notices",
    "get_community_notices",
})

# Stable daily workflows. Binary screenshot tools intentionally remain full-only:
# local agents should upload explicit files through the CLI instead of sending Base64
# through the model context.
_CORE_TOOL_NAMES = frozenset({
    # system
    "set_token",
    "get_tool_manifest",
    "get_current_user",
    "get_app_version",
    # portfolio
    "get_summary",
    "get_records",
    "get_transactions",
    "get_sync_meta",
    "get_portfolio_preferences",
    # fund (batch-first)
    "search_item",
    "get_item_estimate",
    "get_batch_fund_fees",
    "get_batch_fund_profiles",
    "get_batch_fund_quant_metrics",
    "get_batch_fund_period_ranks",
    # market
    "get_status",
    "get_overview",
    "get_index_metrics",
    "get_sector_metrics",
    "get_instrument_catalog",
    "get_instrument_quotes",
    "calculate_trading_dates",
    "get_next_trading_day",
    "get_night_estimate",
    "get_fund_flow",
    # trade
    "request_transaction",
    "get_agent_requests",
    "update_agent_request",
    # import
    "request_import_review",
    # reports
    "submit_personal_strategy_report",
    # quant
    "get_quant_strategy_context",
    "get_batch_fund_nav_history",
    "get_transaction_ledger",
})

TOOL_MODULES = (system, fund, market, portfolio, reports, portfolio_actions, import_tools, community, quant)
_TOOL_ORDER = (
    "set_token",
    "get_tool_manifest",
    "get_current_user",
    "search_item",
    "get_item_detail",
    "get_item_estimate",
    "get_fund_source_previews",
    "get_daily_rank",
    "get_item_history",
    "get_item_dividends",
    "get_fund_timeline",
    "get_fund_fees",
    "get_batch_fund_fees",
    "get_fund_period_rank",
    "get_fund_profile",
    "get_batch_fund_profiles",
    "get_fund_quant_metrics",
    "get_batch_fund_quant_metrics",
    "get_batch_fund_period_ranks",
    "get_status",
    "get_overview",
    "get_sector_wind",
    "get_yesterday_rank",
    "get_fund_flow",
    "get_index_metrics",
    "get_sector_metrics",
    "get_holder_ranking",
    "get_night_estimate",
    "get_night_watchlist",
    "get_purchase_limit_watchlist",
    "get_auto_invest_plans",
    "get_fund_disciplines",
    "get_portfolio_preferences",
    "get_benchmark_history",
    "get_instrument_catalog",
    "get_instrument_quotes",
    "get_instrument_timeline",
    "get_instrument_history",
    "calculate_trading_dates",
    "get_next_trading_day",
    "get_sync_meta",
    "get_raw_sync_data",
    "get_transactions",
    "get_groups",
    "get_tags",
    "get_records",
    "get_summary",
    "submit_personal_strategy_report",
    "request_transaction",
    "get_agent_requests",
    "update_agent_request",
    "import_holding_screenshots",
    "import_transaction_screenshots",
    "request_import_review",
    "get_community_ranking",
    "get_community_my_rank",
    "get_community_user",
    "get_community_stats",
    "get_community_following",
    "search_community_users",
    "get_community_authorization",
    "authorize_community",
    "revoke_community_authorization",
    "follow_community_user",
    "analyze_jcti",
    "get_transaction_ledger",
    "get_batch_fund_nav_history",
    "get_portfolio_nav_history",
    "get_portfolio_trade_review",
    "get_quant_strategy_context",
    "run_portfolio_backtest",
    "get_portfolio_backtest",
    "save_quant_snapshot",
    "get_quant_snapshots",
    "get_quant_snapshot_review",
    "get_app_version",
)


@dataclass(frozen=True)
class ToolSpec:
    name: str
    domain: str
    profile: str
    scope: str
    effects: frozenset[str] = frozenset()
    payload_class: str = "small_json"
    deprecated: bool = False


_DOMAIN_BY_MODULE = {
    system: "profile",
    fund: "market",
    market: "market",
    portfolio: "portfolio",
    reports: "personal_reports",
    portfolio_actions: "trade",
    import_tools: "imports",
    community: "community",
    quant: "quant",
}
_DOMAIN_OVERRIDES = {
    "set_token": "local",
    "get_tool_manifest": "local",
    "get_app_version": "misc",
    "analyze_jcti": "misc",
    "get_transaction_ledger": "portfolio",
    "get_portfolio_nav_history": "portfolio",
    "get_portfolio_trade_review": "portfolio",
    "get_batch_fund_nav_history": "quant",
}
_SCOPE_BY_DOMAIN = {
    "local": "local",
    "profile": "profile:read",
    "portfolio": "portfolio:read",
    "quant": "quant:read",
    "market": "market:read",
    "community": "community:read",
    "trade": "trade:request",
    "personal_reports": "messages:write",
    "imports": "import:request",
    "misc": "ai:analyze",
}
_SCOPE_OVERRIDES = {
    "get_app_version": "agent_token:any (backend endpoint public)",
    "authorize_community": "community:write",
    "revoke_community_authorization": "community:write",
    "follow_community_user": "community:write",
    "get_batch_fund_nav_history": "market:read",
    "run_portfolio_backtest": "quant:write",
    "save_quant_snapshot": "quant:write",
}
_CONFIRMATION_REQUIRED = frozenset({
    "authorize_community",
    "revoke_community_authorization",
    "follow_community_user",
    "request_transaction",
    "update_agent_request",
    "request_import_review",
    "submit_personal_strategy_report",
})
_STATE_CHANGE = _CONFIRMATION_REQUIRED | {
    "run_portfolio_backtest",
    "save_quant_snapshot",
}
_LARGE_JSON_TOOLS = frozenset({
    "get_raw_sync_data",
    "get_item_history",
    "get_instrument_history",
    "get_batch_fund_nav_history",
    "submit_personal_strategy_report",
})
_BINARY_TOOLS = frozenset({
    "import_holding_screenshots",
    "import_transaction_screenshots",
})


def _tool_module(name: str):
    return next(module for module in TOOL_MODULES if hasattr(module, name))


def _build_tool_spec(name: str) -> ToolSpec:
    domain = _DOMAIN_OVERRIDES.get(name, _DOMAIN_BY_MODULE[_tool_module(name)])
    effects = set()
    if name in _STATE_CHANGE:
        effects.add("state_change")
    if name in _CONFIRMATION_REQUIRED:
        effects.add("confirmation_required")
    if name == "follow_community_user":
        effects.add("non_idempotent_toggle")
    payload_class = (
        "binary" if name in _BINARY_TOOLS
        else "large_json" if name in _LARGE_JSON_TOOLS
        else "small_json"
    )
    return ToolSpec(
        name=name,
        domain=domain,
        profile=CORE_PROFILE if name in _CORE_TOOL_NAMES else FULL_PROFILE,
        scope=_SCOPE_OVERRIDES.get(name, _SCOPE_BY_DOMAIN[domain]),
        effects=frozenset(effects),
        payload_class=payload_class,
        deprecated=name in _BINARY_TOOLS,
    )


TOOL_SPECS = tuple(_build_tool_spec(name) for name in _TOOL_ORDER)
TOOL_NAMES = tuple(spec.name for spec in TOOL_SPECS)
CORE_TOOLS = frozenset(spec.name for spec in TOOL_SPECS if spec.profile == CORE_PROFILE)
TOOL_SPEC_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}

assert len(TOOL_NAMES) == len(set(TOOL_NAMES)), "tool registry names must be unique"
assert not (REMOVED_TOOLS & set(TOOL_NAMES)), "cancelled tools must not be registered"
assert CORE_TOOLS <= set(TOOL_NAMES), "core tools must exist in the registry"


def resolve_profile() -> str:
    """Return the active profile from ``HUAHUA_MCP_PROFILE`` (default ``full``)."""
    profile = os.environ.get(PROFILE_ENV, "").strip().lower()
    return profile if profile in {CORE_PROFILE, FULL_PROFILE} else DEFAULT_PROFILE


def active_tool_names(profile: Optional[str] = None) -> tuple[str, ...]:
    """Return the tool names registered for a profile (default: resolved env)."""
    selected = resolve_profile() if profile is None else profile
    if selected == CORE_PROFILE:
        return tuple(name for name in TOOL_NAMES if name in CORE_TOOLS)
    return TOOL_NAMES


def active_tool_specs(profile: Optional[str] = None) -> tuple[ToolSpec, ...]:
    names = set(active_tool_names(profile))
    return tuple(spec for spec in TOOL_SPECS if spec.name in names)


def capabilities_for_profile(profile: str) -> dict[str, list[str]]:
    capabilities: dict[str, list[str]] = {}
    for spec in active_tool_specs(profile):
        if spec.domain == "local":
            continue
        capabilities.setdefault(spec.domain, []).append(spec.name)
    return capabilities


def tool_scopes_for_profile(profile: str) -> dict[str, str]:
    return {spec.name: spec.scope for spec in active_tool_specs(profile)}


def tools_with_effect(profile: str, effect: str) -> list[str]:
    return [
        spec.name for spec in active_tool_specs(profile)
        if effect in spec.effects
    ]


def register_tools(mcp, runtime_globals: dict) -> None:
    names = active_tool_names()
    for name in names:
        runtime_globals[name] = getattr(_tool_module(name), name)
    for module in TOOL_MODULES:
        module.bind(runtime_globals)
    for name in names:
        mcp.tool()(runtime_globals[name])
