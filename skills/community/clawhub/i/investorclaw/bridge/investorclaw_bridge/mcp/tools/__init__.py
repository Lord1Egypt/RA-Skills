# SPDX-License-Identifier: Apache-2.0
"""Canonical MCP tool registry for ic-engine bridge.

Mirrors v5 mnemos's mnemos/mcp/tools/__init__.py: a single TOOL_REGISTRY
dict that domain modules contribute to. Both transports (MCP via FastMCP
and REST via FastAPI) iterate this registry to wire their endpoints.

Naming: tools follow the `domain_action` convention
(`portfolio_ask`, `portfolio_holdings`, etc.) for cross-runtime
compatibility with the agentic-cobol harness and the v4.0
dockerized-skill RFC.
"""
from __future__ import annotations

from typing import Any

from .portfolio import (
    TOOLS as PORTFOLIO_TOOLS,
    portfolio_ask,
    portfolio_holdings,
    portfolio_refresh,
    portfolio_setup,
    portfolio_initialize,
    portfolio_initialize_status,
    get_init_state,
)
from .keys import (
    KEYS_TOOLS,
    portfolio_keys_status,
    portfolio_keys_set,
    portfolio_keys_delete,
)
from .responses import (
    RESPONSE_TOOLS,
    portfolio_response_get,
    portfolio_response_list,
    portfolio_response_delete,
    portfolio_response_flag_bad,
)

# Single canonical registry across all domains. Add new domain modules by
# importing their TOOLS dict and merging here.
TOOL_REGISTRY: dict[str, dict[str, Any]] = {}
for _domain in (PORTFOLIO_TOOLS, KEYS_TOOLS, RESPONSE_TOOLS):
    TOOL_REGISTRY.update(_domain)

# Alias for v5 mnemos parity
TOOLS = TOOL_REGISTRY


def tool_input_schema(tool_info: dict[str, Any]) -> dict[str, Any]:
    """Convert a tool descriptor (description/parameters/required/handler)
    into the JSON Schema shape the MCP transport sends as `inputSchema`.
    Mirrors v5 mnemos's tool_input_schema().
    """
    schema: dict[str, Any] = {
        "type": "object",
        "properties": tool_info["parameters"],
    }
    if tool_info.get("required"):
        schema["required"] = tool_info["required"]
    return schema


__all__ = [
    "TOOL_REGISTRY",
    "TOOLS",
    "tool_input_schema",
    "portfolio_ask",
    "portfolio_holdings",
    "portfolio_refresh",
    "portfolio_setup",
    "portfolio_initialize",
    "portfolio_initialize_status",
    "get_init_state",
    "portfolio_keys_status",
    "portfolio_keys_set",
    "portfolio_keys_delete",
    "portfolio_response_get",
    "portfolio_response_list",
    "portfolio_response_delete",
    "portfolio_response_flag_bad",
]
