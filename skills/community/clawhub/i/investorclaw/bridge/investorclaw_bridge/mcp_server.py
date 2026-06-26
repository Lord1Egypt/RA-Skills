# SPDX-License-Identifier: Apache-2.0
"""Backward-compat shim — surfaces the new bridge.investorclaw_bridge.mcp
package via the original mcp_server module path.

Existing imports continue to work:

    from investorclaw_bridge import mcp_server
    mcp_server.register_tools(app)
    mcp_server.health_check()
    mcp_server._run_ic_engine([...])
    monkeypatch.setattr(mcp_server, "IC_ENGINE_BIN", ...)

The MCP layer was split into bridge/investorclaw_bridge/mcp/ on
2026-05-02 to mirror v5 mnemos's mnemos/mcp/ layout per GRAEAE
consultation (Option C+ contract-driven mirroring across mnemos +
ic-engine + mnemos-rs). See bridge/investorclaw_bridge/mcp/__init__.py
for the new layout.
"""
from .mcp import (  # noqa: F401
    AskBody,
    IC_ENGINE_BIN,
    IcEngineError,
    KEYS_FILE,
    PORTFOLIO_DIR,
    REPORTS_DIR,
    TOOL_REGISTRY,
    TOOLS,
    YF_CACHE_DIR,
    _PROVIDER_KEY_FALLBACKS,
    _clear_yfinance_cache,
    _resolve_narrative_api_key,
    _run_ic_engine,
    health_check,
    logger,
    register_rest_routes,
    register_tools,
    tool_input_schema,
)
