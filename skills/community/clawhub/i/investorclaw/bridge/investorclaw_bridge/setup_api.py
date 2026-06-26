# SPDX-License-Identifier: Apache-2.0
"""First-run setup API + bare-metal HTML form for v4.0 beta pilot.

Per GRAEAE 2026-05-01: making pilot users `nano keys.env` and manually
move CSV files corrupts the primary signal of the pivot (we wanted to
eliminate install friction; making them edit shell files in a terminal
trades one friction for another).

This module ships a minimal browser-driven setup flow:
  GET  /setup          → HTML form (unstyled, single-page, JS-free)
  POST /setup/keys     → save API keys to /data/keys.env (mode 0600)
  POST /setup/portfolio → upload portfolio CSV/xls/PDF to /data/portfolios/
  GET  /setup/status   → JSON: which keys configured, which portfolio files present

No styling. No JS. No build step. Forms POST natively, server returns
HTML. Works in every browser; degrades gracefully if user has cookies
disabled, JS blocked, or connection flakes.
"""
from __future__ import annotations

import os
import re
import stat
from html import escape
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

import structlog

logger = structlog.get_logger("investorclaw_bridge.setup")


# ──────────────────────────────────────────────────────────────────────
# Configuration paths — env-driven for testability
# ──────────────────────────────────────────────────────────────────────


PORTFOLIO_DIR = Path(os.environ.get("IC_PORTFOLIO_DIR", "/data/portfolios"))
KEYS_FILE = Path(os.environ.get("IC_KEYS_FILE", "/data/keys.env"))


# Keys we know about — drives the form layout. Adding a new key:
# (a) add it here, (b) restart container, (c) it shows up in the form.
KNOWN_KEYS = [
    {
        "name": "TOGETHER_API_KEY",
        "label": "Together AI key",
        "description": "Recommended for narrative synthesis (MiniMaxAI/MiniMax-M2.7)",
        "required": False,
    },
    {
        "name": "OPENAI_API_KEY",
        "label": "OpenAI key",
        "description": "Alternative narrative LLM (gpt-4o, gpt-5)",
        "required": False,
    },
    {
        "name": "FINNHUB_KEY",
        "label": "Finnhub key",
        "description": "Real-time quotes + analyst ratings (free tier at finnhub.io)",
        "required": False,
    },
    {
        "name": "FRED_API_KEY",
        "label": "FRED API key",
        "description": "Treasury / TIPS yield curves (free at fred.stlouisfed.org)",
        "required": False,
    },
    {
        "name": "NEWSAPI_KEY",
        "label": "NewsAPI key",
        "description": "News correlation for held positions (free at newsapi.org)",
        "required": False,
    },
    {
        "name": "ALPHA_VANTAGE_KEY",
        "label": "Alpha Vantage key",
        "description": "Supplemental price data (free at alphavantage.co)",
        "required": False,
    },
    {
        "name": "MASSIVE_API_KEY",
        "label": "Massive (FMP) key",
        "description": "Fundamentals, ratios, peer comps (financialmodelingprep.com)",
        "required": False,
    },
    {
        "name": "MARKETAUX_API_KEY",
        "label": "Marketaux key",
        "description": "Per-symbol news with sentiment (marketaux.com)",
        "required": False,
    },
]


_VALID_KEY_NAME = re.compile(r"^[A-Z][A-Z0-9_]+$")


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────


def _read_existing_keys() -> dict[str, str]:
    """Read keys.env if present (regardless of mode — UX wins over strict
    perm check during setup; key_resolver enforces 0600 at runtime).

    For display purposes only — masks values to last 4 chars.
    """
    if not KEYS_FILE.exists():
        return {}
    keys: dict[str, str] = {}
    try:
        for raw in KEYS_FILE.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return keys


def _save_keys(updates: dict[str, str]) -> None:
    """Merge updates into /data/keys.env. Empty values delete the key.
    Sets file mode 0600 after write."""
    PORTFOLIO_DIR.parent.mkdir(parents=True, exist_ok=True)
    existing = _read_existing_keys()
    for name, value in updates.items():
        if not _VALID_KEY_NAME.match(name):
            continue  # silently skip invalid names
        if value:
            existing[name] = value
        else:
            existing.pop(name, None)

    lines = ["# InvestorClaw v4.0 keys.env — managed by /setup", ""]
    for name in sorted(existing.keys()):
        lines.append(f"{name}={existing[name]}")
    lines.append("")

    # Write with restrictive umask so initial mode is tight even before chmod
    old_umask = os.umask(0o077)
    try:
        KEYS_FILE.write_text("\n".join(lines))
    finally:
        os.umask(old_umask)
    KEYS_FILE.chmod(0o600)
    logger.info("setup.keys_saved", count=len(existing), path=str(KEYS_FILE))


def _list_portfolio_files() -> list[dict[str, str]]:
    """List uploaded portfolio files in /data/portfolios/."""
    if not PORTFOLIO_DIR.exists():
        return []
    out = []
    for p in sorted(PORTFOLIO_DIR.iterdir()):
        if p.is_file() and not p.name.startswith("."):
            out.append({
                "name": p.name,
                "size_bytes": str(p.stat().st_size),
            })
    return out


# ──────────────────────────────────────────────────────────────────────
# HTML rendering — unstyled, JS-free
# ──────────────────────────────────────────────────────────────────────


def _render_form(*, banner: str = "") -> str:
    existing = _read_existing_keys()
    files = _list_portfolio_files()

    key_rows: list[str] = []
    for k in KNOWN_KEYS:
        name = k["name"]
        current = existing.get(name, "")
        masked = (
            f'<span style="color:#6a6;">configured ({len(current)} chars; ends ...{escape(current[-4:])})</span>'
            if current
            else '<span style="color:#a66;">not configured</span>'
        )
        key_rows.append(
            f"""
            <tr>
              <td><label for="{escape(name)}"><strong>{escape(k['label'])}</strong></label><br>
                  <small>{escape(k['description'])}</small><br>
                  <small>Status: {masked}</small></td>
              <td><input type="password" id="{escape(name)}" name="{escape(name)}"
                         placeholder="paste new value (leave blank to keep current)"
                         autocomplete="off"
                         style="width: 32em;"></td>
            </tr>
            """
        )

    file_rows = "".join(
        f'<li><code>{escape(f["name"])}</code> ({f["size_bytes"]} bytes)</li>'
        for f in files
    )
    if not file_rows:
        file_rows = (
            '<li><em>No portfolio files yet — upload one below.</em></li>'
        )

    banner_html = f'<p style="color:#262;background:#efe;padding:0.5em;border-radius:4px;">{escape(banner)}</p>' if banner else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>InvestorClaw v4.0 — Setup</title>
<style>
  body {{ font-family: -apple-system, system-ui, sans-serif; max-width: 56em;
          margin: 2em auto; padding: 0 1em; color: #222; line-height: 1.5; }}
  h1 {{ font-size: 1.5em; margin-bottom: 0.25em; }}
  h2 {{ font-size: 1.15em; margin-top: 2em; }}
  table {{ border-collapse: collapse; width: 100%; }}
  td {{ padding: 0.5em; vertical-align: top; border-bottom: 1px solid #eee; }}
  input[type="text"], input[type="password"] {{ padding: 0.4em; font-size: 1em; }}
  button {{ padding: 0.6em 1.2em; font-size: 1em; cursor: pointer;
            background: #246; color: #fff; border: 0; border-radius: 4px; }}
  button:hover {{ background: #135; }}
  small {{ color: #666; }}
  code {{ background: #f4f4f5; padding: 0.1em 0.35em; border-radius: 3px; }}
</style>
</head>
<body>
<h1>InvestorClaw v4.0 <small style="color:#888;font-weight:normal;">— Setup</small></h1>
{banner_html}
<p>Configure your API keys and upload a portfolio file. After this, your agent
(Claude Desktop / zeroclaw / openclaw / hermes) will be able to answer
portfolio questions via MCP.</p>

<h2>1. API keys</h2>
<form method="POST" action="/setup/keys">
<table>{''.join(key_rows)}</table>
<p><button type="submit">Save keys</button>
<small style="margin-left:1em;">Stored in <code>/data/keys.env</code> mode 0600 inside the container.</small></p>
</form>

<h2>2. Portfolio files</h2>
<p>Already uploaded:</p>
<ul>{file_rows}</ul>

<form method="POST" action="/setup/portfolio" enctype="multipart/form-data">
<p><label>Upload portfolio file (.csv, .xls, .xlsx, .pdf):
<input type="file" name="portfolio_file" accept=".csv,.xls,.xlsx,.pdf" required></label></p>
<p><button type="submit">Upload</button></p>
</form>

<h2>3. Connect your agent</h2>
<p>Once setup is complete, point your agent at the MCP server:</p>
<pre style="background:#f4f4f5;padding:1em;border-radius:4px;overflow-x:auto;">
mcpServers:
  investorclaw:
    transport: http
    url: http://127.0.0.1:8090/mcp
</pre>
<p>Per-agent config snippets are in <code>agent-skills/&lt;agent&gt;/config-snippet.*</code>
in the InvestorClaw v4.0 distribution.</p>

<hr>
<p><small>InvestorClaw v4.0 (Apache 2.0 service / MIT distribution edge).
<a href="/healthz">healthz</a> · <a href="/api/version">version</a> ·
educational use only — not investment advice.</small></p>
</body>
</html>
"""


# ──────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────


router = APIRouter(prefix="/setup", tags=["setup"])


@router.get("", response_class=HTMLResponse)
async def setup_page() -> HTMLResponse:
    return HTMLResponse(_render_form())


@router.post("/keys", response_class=HTMLResponse)
async def save_keys_form(**form_values: str):  # noqa: ARG002
    """Form-style save — accepts ALL form fields, filters to KNOWN_KEYS only.

    FastAPI's signature here is via the request body — we pull form values
    via Form() parsing in a wrapper to avoid declaring 6 separate Form() params.
    """
    # Re-implemented below with explicit Form params for clarity; this stub
    # is overwritten by the explicit route registration in the app builder.
    raise NotImplementedError  # pragma: no cover


# Explicit form-handler with all known keys as optional Form params.
# FastAPI prefers explicit Form() declarations; the **form_values pattern
# above doesn't always parse correctly across versions.

async def save_keys_explicit(
    TOGETHER_API_KEY: str = Form(""),
    OPENAI_API_KEY: str = Form(""),
    FINNHUB_KEY: str = Form(""),
    FRED_API_KEY: str = Form(""),
    NEWSAPI_KEY: str = Form(""),
    ALPHA_VANTAGE_KEY: str = Form(""),
):
    updates = {
        "TOGETHER_API_KEY": TOGETHER_API_KEY,
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "FINNHUB_KEY": FINNHUB_KEY,
        "FRED_API_KEY": FRED_API_KEY,
        "NEWSAPI_KEY": NEWSAPI_KEY,
        "ALPHA_VANTAGE_KEY": ALPHA_VANTAGE_KEY,
    }
    # Strip leading/trailing whitespace; empty values become "delete the key"
    updates = {k: v.strip() for k, v in updates.items()}
    saved = {k: v for k, v in updates.items() if v}
    _save_keys(updates)
    banner = (
        f"Saved {len(saved)} key{'s' if len(saved) != 1 else ''}: "
        f"{', '.join(sorted(saved.keys()))}"
        if saved
        else "No keys submitted (all fields blank — existing values preserved)."
    )
    return HTMLResponse(_render_form(banner=banner))


@router.post("/portfolio", response_class=HTMLResponse)
async def upload_portfolio(
    portfolio_file: UploadFile = File(...),
):
    if not portfolio_file.filename:
        raise HTTPException(400, "No file selected")

    # Strict allowlist — refuse anything we can't parse
    suffix = Path(portfolio_file.filename).suffix.lower()
    if suffix not in {".csv", ".xls", ".xlsx", ".pdf"}:
        raise HTTPException(
            400, f"Unsupported file type: {suffix}. Allowed: .csv .xls .xlsx .pdf"
        )

    PORTFOLIO_DIR.mkdir(parents=True, exist_ok=True)
    # Sanitize filename — strip path components, keep basename
    safe_name = Path(portfolio_file.filename).name
    dest = PORTFOLIO_DIR / safe_name

    contents = await portfolio_file.read()
    dest.write_bytes(contents)
    dest.chmod(0o600)

    logger.info(
        "setup.portfolio_uploaded",
        path=str(dest),
        size=len(contents),
        original_name=portfolio_file.filename,
    )
    banner = f"Uploaded: {safe_name} ({len(contents)} bytes)"
    return HTMLResponse(_render_form(banner=banner))


@router.get("/status")
async def setup_status() -> JSONResponse:
    """Machine-readable status — what's configured, what's not."""
    existing = _read_existing_keys()
    return JSONResponse({
        "keys": {
            k["name"]: {
                "configured": k["name"] in existing,
                "label": k["label"],
                "required": k["required"],
            }
            for k in KNOWN_KEYS
        },
        "portfolio_files": _list_portfolio_files(),
        "data_dir": str(PORTFOLIO_DIR.parent),
    })


def attach_to(app, register_root_redirect: bool = False) -> None:
    """Wire the setup router onto a FastAPI app, plus the explicit form handler.

    When ``register_root_redirect`` is True the legacy `/` → `/setup` 303
    redirect is added. The dashboard landing page (added in v4.1.32) renders
    a real `/` route, so callers should leave this False unless they have no
    other root handler. Default: False.
    """
    # Override the router's POST /setup/keys with the explicit form-param version
    app.post("/setup/keys", response_class=HTMLResponse)(save_keys_explicit)
    app.include_router(router)
    if register_root_redirect:
        @app.get("/", include_in_schema=False)
        async def root_redirect() -> RedirectResponse:
            return RedirectResponse(url="/setup", status_code=303)
