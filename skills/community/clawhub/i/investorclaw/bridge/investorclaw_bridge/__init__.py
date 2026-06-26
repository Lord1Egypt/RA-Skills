# SPDX-License-Identifier: Apache-2.0
"""InvestorClaw v4.0 bridge package.

Exposes ic-engine analytical commands as MCP-HTTP tools. Talks to the
mnemos-rs sibling container over HTTP. Serves the dashboard web UI.

Module layout:
    serve         entry point (uvicorn + FastAPI app)
    mcp_server    FastMCP server registering ic-engine tool wrappers
    mnemos_client HTTP client to mnemos-rs (matching the Rust trait)
    bundle        bundle.json import/export with atomic cross-DB rename
    dashboard     dashboard static-file routes + REST API
    auth          token-auth for remote deploys
"""

__version__ = "4.0.0a1"
