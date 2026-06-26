# SPDX-License-Identifier: Apache-2.0
"""Entry point for the InvestorClaw v4.0 bridge.

Two listeners, one Python process:
  :8090  — MCP-HTTP server (FastMCP) — agent-facing tool surface
  :8092  — Dashboard web UI + REST + /healthz — user-facing config UI

Both ports share ic-engine session, sqlite db, and MnemosClient instance.

For the v4.0 beta pilot (24h timeline as of 2026-05-01):
  - MCP-HTTP at :8090 is load-bearing — at least 4 tools registered
    (portfolio_ask, portfolio_holdings, portfolio_refresh, portfolio_setup)
  - Dashboard at :8092 is minimal — placeholder static page + /healthz
  - mnemos-rs sibling container is OPTIONAL (not blocking for beta)
"""
from __future__ import annotations

import logging
import os
import sys

import structlog


def _configure_logging() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


def _bind_addr_to_host_port(bind: str) -> tuple[str, int]:
    """Parse a bind string like '0.0.0.0:8090' into (host, port)."""
    if ":" not in bind:
        raise ValueError(f"Invalid bind address {bind!r} — expected HOST:PORT")
    host, port_str = bind.rsplit(":", 1)
    return host, int(port_str)


def main() -> int:
    """Start the bridge.

    Loads ic-engine bridge tooling + starts FastMCP at IC_MCP_BIND and
    a tiny FastAPI app at IC_DASHBOARD_BIND for /healthz + dashboard
    static files. Both run in the same uvicorn process via mounted
    sub-apps (one ASGI app at root, another mounted at /mcp).
    """
    _configure_logging()
    logger = structlog.get_logger("investorclaw_bridge.serve")

    # Defer heavy imports until after logging is configured (so import
    # errors get logged with structlog).
    try:
        from fastapi import FastAPI
        from fastapi.responses import HTMLResponse, JSONResponse
        from fastapi.staticfiles import StaticFiles
        import uvicorn
    except ImportError as e:
        logger.error("bridge.import_error", missing=str(e))
        sys.stderr.write(
            f"FATAL: missing required dependency: {e}. "
            f"Did you install via `pip install -e bridge/`?\n"
        )
        return 2

    try:
        # FastMCP — provides MCP-HTTP transport
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        # FastMCP isn't packaged yet on all systems; for beta we can
        # serve a minimal /mcp endpoint manually if FastMCP is missing.
        FastMCP = None  # type: ignore[assignment]
        logger.warning(
            "bridge.fastmcp_missing",
            note="MCP server will be a placeholder; install `mcp` package for full functionality",
        )

    from . import mcp_server

    # Load /data/keys.env into os.environ so ic-engine subprocesses inherit
    # the keys (FINNHUB_KEY, MASSIVE_API_KEY, ALPHA_VANTAGE_KEY, NEWSAPI_KEY,
    # TOGETHER/INVESTORCLAW_NARRATIVE_API_KEY, etc.). The key_resolver module
    # parses + validates mode 0600; we only set keys not already in env so
    # operator-set ENV (Dockerfile / compose) wins over file values.
    from pathlib import Path
    from . import key_resolver

    keys_path = Path(os.environ.get("IC_KEYS_FILE", "/data/keys.env"))
    try:
        loaded = key_resolver.load_keys_env(keys_path)
        added = 0
        for k, v in loaded.items():
            if k not in os.environ:
                os.environ[k] = v
                added += 1
        logger.info(
            "bridge.keys.loaded",
            path=str(keys_path),
            in_file=len(loaded),
            added_to_env=added,
            keys=sorted(loaded.keys()),
        )
    except Exception as e:
        logger.warning(
            "bridge.keys.load_failed",
            path=str(keys_path),
            error=f"{type(e).__name__}: {e}",
        )

    mcp_bind = os.environ.get("IC_MCP_BIND", "0.0.0.0:8090")
    dashboard_bind = os.environ.get("IC_DASHBOARD_BIND", "0.0.0.0:8092")
    mnemos_base = os.environ.get("MNEMOS_BASE", "http://mnemos:5002")

    logger.info(
        "bridge.start",
        mcp_bind=mcp_bind,
        dashboard_bind=dashboard_bind,
        mnemos_base=mnemos_base,
        portfolio_dir=os.environ.get("IC_PORTFOLIO_DIR", "/data/portfolios"),
        engine_portfolio_dir=os.environ.get("INVESTOR_CLAW_PORTFOLIO_DIR", "(unset)"),
    )

    # ── Build the dashboard FastAPI app ────────────────────────────────
    dashboard_app = FastAPI(title="InvestorClaw v4.0", version="4.0.0a1")

    @dashboard_app.get("/healthz")
    async def healthz() -> JSONResponse:
        # Health includes init state so agents polling /healthz can also
        # gate on `init_state == "ready"` without an extra round-trip.
        from .mcp.tools import get_init_state as _get_init_state
        h = mcp_server.health_check()
        snap = _get_init_state()
        h["init_state"] = snap["state"]
        h["init_ready"] = snap["ready"]
        h["init_current_stage"] = snap["current_stage"]
        h["init_elapsed_ms"] = snap["elapsed_ms"]
        return JSONResponse(h)

    @dashboard_app.get("/api/version")
    async def version() -> JSONResponse:
        return JSONResponse({"version": "4.0.0a1", "service": "investorclaw-bridge"})

    # Wire the first-run setup API + bare-metal HTML form
    # (per GRAEAE 2026-05-01 — keep pilots in browser, out of nano)
    from . import setup_api
    setup_api.attach_to(dashboard_app)

    # Mount static dashboard files at /static (root is taken by setup redirect)
    dashboard_dir = "/opt/ic-engine/dashboard"
    if os.path.isdir(dashboard_dir):
        dashboard_app.mount(
            "/static", StaticFiles(directory=dashboard_dir, html=True), name="dashboard"
        )

    # Mount /reports → /data/reports so users can browse generated EOD HTML
    # files, JSON snapshots, etc. directly via http://localhost:18092/reports/
    # The reports dir is the bind-mounted ./reports/ on the host.
    reports_dir = os.environ.get("IC_REPORTS_DIR", "/data/reports")
    if os.path.isdir(reports_dir):
        dashboard_app.mount(
            "/reports",
            StaticFiles(directory=reports_dir, html=True),
            name="reports",
        )

    # Tabbed dashboard at / + per-section views at /dashboard/<tab>
    # — mounted last so it doesn't get preempted by other root-route registrations.
    from . import dashboard
    from .mcp.tools.portfolio import get_init_state as _get_init_state
    from .mcp.tools.keys import portfolio_keys_status, portfolio_keys_set
    from .mcp._runtime import _run_ic_engine

    async def _regenerate_sweep() -> dict:
        """Run the full data-refresh + analyzer sweep that backs every tab.
        Sequenced so a failing section doesn't abort the rest. Engine sections
        that don't write JSON (or aren't installed) just no-op.
        """
        results: dict = {}
        # Setup is fast and idempotent — re-discovers any newly uploaded files.
        results["setup"] = await _run_ic_engine(["setup"], timeout_sec=300.0)
        # The big refresh — pulls fresh prices for every position.
        results["refresh"] = await _run_ic_engine(["refresh"], timeout_sec=1800.0)
        # Per-section analyzers. Each writes its own JSON under /data/reports/.
        sections = [
            "performance", "bonds", "analyst", "news", "whatchanged",
            "scenario", "optimize", "rebalance", "cashflow", "peer",
            "markets", "synthesize",
        ]
        for sec in sections:
            try:
                results[sec] = await _run_ic_engine([sec], timeout_sec=900.0)
            except Exception as e:  # noqa: BLE001
                results[sec] = {"error": f"{type(e).__name__}: {e}"}
        return results

    dashboard.attach_to(
        dashboard_app,
        get_init_state=_get_init_state,
        get_keys_status=portfolio_keys_status,
        set_key=lambda name, value: portfolio_keys_set({name: value}),
        regenerate=_regenerate_sweep,
    )

    # ── Build the MCP-HTTP app ────────────────────────────────────────
    # FastMCP exposes its own ASGI app via streamable_http_app(), but the
    # session manager inside it must be started via an async context
    # manager (`session_manager.run()`) — wired through FastAPI's lifespan
    # parameter. Mounting without the lifespan gives:
    #   RuntimeError: Task group is not initialized. Make sure to use run().
    # See FastMCP docs for the canonical lifespan-mount pattern.
    from contextlib import asynccontextmanager

    if FastMCP is not None:
        # MCP server's StreamableHTTP transport ships DNS-rebinding protection
        # (mcp.server.transport_security.TransportSecuritySettings, on by
        # default). With allowed_hosts=[] and protection on, every Host header
        # except 127.0.0.1/localhost is rejected. That breaks the v4.0
        # container-to-container path: an agent in a sibling container hits the
        # bridge over the docker bridge IP (172.17.0.1:18090 in default bridge
        # mode, or `<service-name>:8090` in compose's user-defined bridge) and
        # gets `Streamable HTTP error: Invalid Host header`.
        #
        # The convention (RFC §8) is localhost-only by default, but localhost
        # is the *host*, not the *container*'s view of the host. For the
        # in-cluster MCP path to work at all, we need to allow the container
        # bridge IPs and compose service names.
        #
        # Default: disable rebinding protection (this service is meant to be
        # reached by sibling containers + localhost; not exposed publicly).
        # Override via env: MCP_ALLOWED_HOSTS=host1,host2,... to keep
        # protection on with an explicit allowlist.
        from mcp.server.transport_security import TransportSecuritySettings
        _allowed_hosts = os.environ.get("MCP_ALLOWED_HOSTS", "").strip()
        if _allowed_hosts:
            _sec = TransportSecuritySettings(
                enable_dns_rebinding_protection=True,
                allowed_hosts=[h.strip() for h in _allowed_hosts.split(",") if h.strip()],
            )
        else:
            _sec = TransportSecuritySettings(enable_dns_rebinding_protection=False)
        mcp_app = FastMCP("investorclaw", transport_security=_sec)
        mcp_server.register_tools(mcp_app)
        try:
            mcp_asgi = mcp_app.streamable_http_app()
        except AttributeError:
            try:
                mcp_asgi = mcp_app.sse_app()
            except AttributeError:
                logger.error(
                    "bridge.mcp_transport_unavailable",
                    note="FastMCP installed but no HTTP/SSE transport found; check mcp package version",
                )
                mcp_app = None
                mcp_asgi = None
    else:
        mcp_app = None
        mcp_asgi = None

    @asynccontextmanager
    async def mcp_lifespan(app):
        if mcp_app is not None and hasattr(mcp_app, "session_manager"):
            async with mcp_app.session_manager.run():
                yield
        else:
            yield

    # MCP-bound FastAPI app — mounts FastMCP at root so the inner /mcp path
    # becomes /mcp on the agent's URL. /healthz lives at root alongside.
    mcp_app_root = FastAPI(
        title="InvestorClaw MCP",
        version="4.0.0a1",
        lifespan=mcp_lifespan,
    )

    @mcp_app_root.get("/healthz")
    async def mcp_healthz() -> JSONResponse:
        from .mcp.tools import get_init_state as _get_init_state
        h = mcp_server.health_check()
        snap = _get_init_state()
        h["init_state"] = snap["state"]
        h["init_ready"] = snap["ready"]
        h["init_current_stage"] = snap["current_stage"]
        h["init_elapsed_ms"] = snap["elapsed_ms"]
        return JSONResponse(h)

    # Register REST wrappers BEFORE the FastMCP mount; FastAPI route
    # resolution prefers explicitly-registered routes over mounted apps,
    # so /api/portfolio/* takes precedence over the FastMCP catch-all.
    mcp_server.register_rest_routes(mcp_app_root)

    if mcp_asgi is not None:
        # Mount at root: FastMCP's internal /mcp path becomes the public /mcp.
        # This is the canonical path agents expect (see RFC §6.2 transport=http).
        mcp_app_root.mount("/", mcp_asgi)
    else:
        @mcp_app_root.get("/mcp")
        async def mcp_placeholder() -> JSONResponse:
            return JSONResponse(
                {
                    "error": "mcp_transport_unavailable",
                    "note": (
                        "FastMCP HTTP transport not initialized. "
                        "Install mcp>=1.4 or check ASGI integration."
                    ),
                },
                status_code=503,
            )

    # ── Run both listeners ─────────────────────────────────────────────
    # uvicorn can serve multiple ASGI apps via Config + Server multiplexing.
    # For simplicity in beta, we launch two uvicorn instances in asyncio.gather.
    import asyncio

    mcp_host, mcp_port = _bind_addr_to_host_port(mcp_bind)
    dash_host, dash_port = _bind_addr_to_host_port(dashboard_bind)

    mcp_config = uvicorn.Config(
        mcp_app_root, host=mcp_host, port=mcp_port, log_level="info"
    )
    dash_config = uvicorn.Config(
        dashboard_app, host=dash_host, port=dash_port, log_level="info"
    )
    mcp_uvicorn = uvicorn.Server(mcp_config)
    dash_uvicorn = uvicorn.Server(dash_config)

    # Boot-time auto-initialize so by the time any agent connects, the
    # envelope cache is already warm. The agent gets sub-second responses
    # on its very first portfolio_ask instead of the 5–15min cold-cache
    # path. Disable with IC_INITIALIZE_ON_BOOT=0.
    initialize_on_boot = os.environ.get("IC_INITIALIZE_ON_BOOT", "1").strip() not in ("0", "false", "no", "")

    async def _auto_initialize() -> None:
        # Brief delay so the listeners are up before we spawn engine subprocesses.
        await asyncio.sleep(2.0)
        try:
            from .mcp.tools.portfolio import portfolio_initialize
            logger.info("bridge.auto_initialize.start")
            result = await portfolio_initialize(seed_question="What is in my portfolio?")
            logger.info(
                "bridge.auto_initialize.done",
                ready=result.get("ready"),
                total_duration_ms=result.get("total_duration_ms"),
                stages=[s.get("stage") + ":" + str(s.get("exit_code")) for s in result.get("stages", [])],
            )
        except Exception as e:
            logger.warning("bridge.auto_initialize.failed", error=f"{type(e).__name__}: {e}")

    async def _run_both() -> None:
        tasks = [mcp_uvicorn.serve(), dash_uvicorn.serve()]
        if initialize_on_boot:
            tasks.append(_auto_initialize())
        await asyncio.gather(*tasks)

    try:
        asyncio.run(_run_both())
    except KeyboardInterrupt:
        logger.info("bridge.shutdown", reason="keyboard_interrupt")
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
