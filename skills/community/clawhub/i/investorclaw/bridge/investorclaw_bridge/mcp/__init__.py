# SPDX-License-Identifier: Apache-2.0
"""ic-engine bridge MCP layer.

Layout mirrors v5 mnemos (mnemos-production v5.0.0) per GRAEAE
2026-05-02 consultation (Option C+ contract-driven mirroring):

  _runtime.py     — subprocess executor, env config, health_check
  transport.py    — FastMCP @app.tool() + FastAPI REST decorators
  tools/
    __init__.py   — TOOL_REGISTRY canonical dict (mirrors v5)
    portfolio.py  — pure async handlers + tool descriptors

The single mcp_server.py module remains as a backward-compat shim
(re-exports below) so existing serve.py + tests work unchanged.
"""
from ._runtime import (
    IC_ENGINE_BIN,
    IcEngineError,
    KEYS_FILE,
    PORTFOLIO_DIR,
    REPORTS_DIR,
    YF_CACHE_DIR,
    _PROVIDER_KEY_FALLBACKS,
    _clear_yfinance_cache,
    _resolve_narrative_api_key,
    _run_ic_engine,
    health_check,
    logger,
)
from .transport import AskBody, register_rest_routes, register_tools
from .tools import TOOL_REGISTRY, TOOLS, tool_input_schema

__all__ = [
    # public transport surface
    "register_tools",
    "register_rest_routes",
    "health_check",
    "AskBody",
    # registry surface (mirrors v5 mnemos)
    "TOOL_REGISTRY",
    "TOOLS",
    "tool_input_schema",
    # runtime helpers (test-monkeypatchable + serve.py imports)
    "IcEngineError",
    "_run_ic_engine",
    "_clear_yfinance_cache",
    "_resolve_narrative_api_key",
    # env config (test-monkeypatchable)
    "IC_ENGINE_BIN",
    "PORTFOLIO_DIR",
    "REPORTS_DIR",
    "KEYS_FILE",
    "YF_CACHE_DIR",
    "_PROVIDER_KEY_FALLBACKS",
    "logger",
]
