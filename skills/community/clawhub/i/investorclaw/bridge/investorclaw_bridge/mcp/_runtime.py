# SPDX-License-Identifier: Apache-2.0
"""ic-engine subprocess runtime + env-driven config.

Mirrors v5 mnemos's mnemos/mcp/tools/_runtime.py separation of concerns:
the runtime helpers (subprocess executor, env config, REST proxy primitives)
are decoupled from transport (transport.py) and from tool handlers
(tools/portfolio.py). Tools call into _run_ic_engine() and shape results;
transport adapters wire the tool handlers to MCP @app.tool() decorators
or FastAPI POST routes.
"""
from __future__ import annotations

import asyncio
import json
import os
import shutil
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger("investorclaw_bridge.mcp")


# ──────────────────────────────────────────────────────────────────────
# Configuration — env-driven so the container can rewire without rebuild
# ──────────────────────────────────────────────────────────────────────


IC_ENGINE_BIN = os.environ.get(
    "IC_ENGINE_BIN", "/opt/ic-engine/.venv/bin/investorclaw"
)
PORTFOLIO_DIR = Path(os.environ.get("IC_PORTFOLIO_DIR", "/data/portfolios"))
REPORTS_DIR = Path(os.environ.get("IC_REPORTS_DIR", "/data/reports"))
KEYS_FILE = Path(os.environ.get("IC_KEYS_FILE", "/data/keys.env"))

# yfinance writes session cookies + ticker-tz cache to ~/.cache/py-yfinance/
# inside the container. Once Yahoo's anti-bot rate-limits a session, the
# cookie carries the backoff state and every subsequent ic-engine subprocess
# inherits the lockout. Clearing this dir on subprocess timeout breaks the
# cascade — see commit 50387b1 on mnemos-os/mnemos-ic-runtime.
YF_CACHE_DIR = Path(os.environ.get("YF_CACHE_DIR", "/home/ic/.cache/py-yfinance"))


# Provider key map — operator sets ONE of these in /data/keys.env.
# Cost policy: Together MiniMax is the fleet default (Anthropic-free).
_PROVIDER_KEY_FALLBACKS = (
    "INVESTORCLAW_NARRATIVE_API_KEY",  # explicit override wins
    "TOGETHER_API_KEY",                # fleet default
    "GOOGLE_API_KEY",                  # only with -flash variant
    "GEMINI_API_KEY",                  # alias
    "OPENAI_API_KEY",                  # last resort
)


def _resolve_narrative_api_key() -> str | None:
    """Return the first non-empty narrative API key from the fallback chain."""
    for var in _PROVIDER_KEY_FALLBACKS:
        v = os.environ.get(var, "").strip()
        if v:
            return v
    return None


class IcEngineError(Exception):
    """Raised when the ic-engine subprocess exits non-zero or times out."""


def _clear_yfinance_cache() -> None:
    """Delete the yfinance per-user cache directory. Called from the
    subprocess-reap path on TimeoutError to break the rate-limit-cookie
    cascade. Safe on missing/partial dir — rmtree(ignore_errors=True)
    swallows ENOENT and EACCES.
    """
    try:
        shutil.rmtree(YF_CACHE_DIR, ignore_errors=True)
        logger.info("mcp.yf_cache.cleared", path=str(YF_CACHE_DIR))
    except Exception as exc:
        logger.warning("mcp.yf_cache.clear_failed", path=str(YF_CACHE_DIR), error=str(exc))


async def _run_ic_engine(
    args: list[str],
    *,
    timeout_sec: float = 1800.0,
) -> dict[str, Any]:
    """Run `investorclaw <args>` in a subprocess; return the parsed envelope.

    Returns a dict with keys: stdout, stderr, exit_code, ic_result, narrative.
    ic_result is the parsed `{"ic_result": {...}}` envelope from stdout's
    last line, or None if the engine returned only narrative text.

    Raises IcEngineError on non-zero exit *unless* the result includes a
    structured envelope (in which case the caller decides semantics).

    The reap path SIGTERMs orphans on timeout/cancellation and clears the
    yfinance cache to break the cascade documented in YF_CACHE_DIR above.
    """
    bin_path = IC_ENGINE_BIN if Path(IC_ENGINE_BIN).exists() else "investorclaw"
    if not shutil.which(bin_path) and not Path(bin_path).exists():
        raise IcEngineError(
            f"ic-engine binary not found at {IC_ENGINE_BIN!r} or on PATH. "
            f"Container build must install it at /opt/ic-engine/.venv/bin/investorclaw."
        )

    full_cmd = [bin_path, *args]
    logger.info("mcp.ic_engine.invoke", cmd=full_cmd)

    sub_env = dict(os.environ)
    api_key = _resolve_narrative_api_key()
    if api_key:
        sub_env.setdefault("INVESTORCLAW_NARRATIVE_API_KEY", api_key)
        sub_env.setdefault("INVESTORCLAW_STONKMODE_API_KEY", api_key)
        sub_env.setdefault("INVESTORCLAW_CONSULTATION_API_KEY", api_key)

    proc = await asyncio.create_subprocess_exec(
        *full_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=str(PORTFOLIO_DIR.parent),
        env=sub_env,
    )
    timed_out = False
    try:
        try:
            stdout_b, stderr_b = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_sec
            )
        except asyncio.TimeoutError:
            timed_out = True
            raise IcEngineError(
                f"ic-engine command timed out after {timeout_sec}s: {full_cmd}"
            )
    except (asyncio.CancelledError, asyncio.TimeoutError, IcEngineError):
        if proc.returncode is None:
            try:
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=2.0)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
            except ProcessLookupError:
                pass
        if timed_out:
            _clear_yfinance_cache()
        raise
    finally:
        if proc.returncode is None:
            try:
                proc.kill()
                await proc.wait()
            except ProcessLookupError:
                pass

    stdout = stdout_b.decode("utf-8", errors="replace")
    stderr = stderr_b.decode("utf-8", errors="replace")
    exit_code = proc.returncode or 0

    # Parse the structured ic_result envelope if present (last JSON line).
    ic_result = None
    narrative = stdout
    for line in reversed(stdout.splitlines()):
        line = line.strip()
        if line.startswith('{"ic_result"'):
            try:
                ic_result = json.loads(line)
                narrative = stdout.rsplit(line, 1)[0].rstrip()
                break
            except json.JSONDecodeError:
                pass

    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_code": exit_code,
        "ic_result": ic_result,
        "narrative": narrative,
    }


def health_check() -> dict[str, Any]:
    """Basic liveness — surfaced at /healthz on both :8090 (MCP) and :8092 (dashboard)."""
    bin_present = Path(IC_ENGINE_BIN).exists() or bool(shutil.which("investorclaw"))
    return {
        "status": "ok" if bin_present else "degraded",
        "ic_engine_bin_found": bin_present,
        "portfolio_dir": str(PORTFOLIO_DIR),
        "portfolio_dir_exists": PORTFOLIO_DIR.exists(),
        "reports_dir": str(REPORTS_DIR),
    }
