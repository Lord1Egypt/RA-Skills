# SPDX-License-Identifier: Apache-2.0
"""
InvestorClaw v4.x dashboard — server-rendered tabbed UI on :18092.

Each tab is its own FastAPI route returning a complete HTML page.
Section content reuses the engine's render helpers from
``ic_engine.rendering.eod_email_template`` so the dashboard tabs and the
EOD email render with identical styling and data shapes.

Tabs:
    /                     Overview — status + quick actions
    /dashboard/holdings   Top holdings + asset / sector breakdown
    /dashboard/performance Sharpe + Sortino + drawdown + period
    /dashboard/whatchanged Day-over-day attribution + top movers
    /dashboard/scenarios  Stress tests + drawdown / VaR
    /dashboard/bonds      Yield-to-maturity + duration + bond ladder
    /dashboard/analyst    Analyst consensus + price-target spread
    /dashboard/news       Per-holding headlines (with clickable links)
    /dashboard/synthesis  Multi-factor advisor narrative
    /dashboard/reports    Archive of generated EOD HTML reports
    /dashboard/settings   API-key management + provider config
    /dashboard/about      Version + license + disclaimer
"""
from __future__ import annotations

import datetime as _dt
import glob as _glob
import json as _json
import os
import pathlib
from typing import Any, Dict

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse


REPORTS_DIR = os.environ.get("IC_REPORTS_DIR", "/data/reports")

# (slug, label, icon)
# Coverage map (cobol nlq-prompts.json v2.5.0 — 30 NLQs):
#   Overview p23/p24 | Holdings p01/p02/p11/p28 | Performance p03/p04
#   What Changed (delta) | Scenarios | Bonds p14/p15 | Analyst p05
#   News p06/p16/p19 | Markets p17/p18/p21/p22 | Lookup p27
#   Optimize p09/p10/p12/p13 | Cashflow p25 | Peer p26
#   Synthesis p07/p08 | Reports p23/p24 | Settings | About p20/p29/p30
TABS = [
    ("", "Overview", "📊"),
    ("holdings", "Holdings", "📁"),
    ("performance", "Performance", "📈"),
    ("whatchanged", "What Changed", "Δ"),
    ("scenarios", "Scenarios", "⚡"),
    ("bonds", "Bonds", "🏛"),
    ("optimize", "Optimize", "🎚"),
    ("cashflow", "Cashflow", "💵"),
    ("peer", "Peer", "⚖"),
    ("analyst", "Analyst", "🎯"),
    ("news", "News", "📰"),
    ("markets", "Markets", "🌐"),
    ("lookup", "Lookup", "🔎"),
    ("synthesis", "Synthesis", "✦"),
    ("reports", "Reports", "📄"),
    ("settings", "Settings", "⚙"),
    ("about", "About", "ℹ"),
]


def _try_engine_helpers():
    """Import the engine's render helpers; return a stub set if unavailable."""
    try:
        from ic_engine.rendering import eod_email_template as t
        return t
    except ImportError:
        return None


_T = _try_engine_helpers()


def _load_json(filename: str) -> Dict[str, Any]:
    path = pathlib.Path(REPORTS_DIR) / filename
    if not path.is_file():
        return {}
    try:
        return _json.loads(path.read_text())
    except Exception:
        return {}


def _coerce_position_count(value) -> int:
    """position_count can be a scalar (older engine) or a dict-by-asset-class
    (current engine writes ``{'equity': 215, 'bond': 38, 'cash': 16, ...}``).
    Sum the dict values; fall back to 0 if neither shape applies.
    """
    if isinstance(value, dict):
        try:
            return sum(int(v or 0) for v in value.values())
        except (TypeError, ValueError):
            return 0
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _shell(active_slug: str, body: str, title: str = "InvestorClaw") -> str:
    """Wrap content in the standard dashboard shell with tab navigation."""
    nav_items = []
    for slug, label, icon in TABS:
        href = "/" if slug == "" else f"/dashboard/{slug}"
        active_cls = " active" if slug == active_slug else ""
        nav_items.append(
            f'<a href="{href}" class="tab{active_cls}">'
            f'<span class="tab-icon">{icon}</span>{label}</a>'
        )
    nav = "".join(nav_items)
    today = _dt.date.today().isoformat()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — InvestorClaw</title>
<style>
:root {{ color-scheme: dark light; }}
* {{ box-sizing: border-box; }}
body {{
  font: 14px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  margin: 0; padding: 0;
  background: #0d1117; color: #c9d1d9;
}}
@media (prefers-color-scheme: light) {{
  body {{ background: #fafbfc; color: #24292f; }}
}}
header {{
  background: #161b22; border-bottom: 1px solid #30363d;
  padding: 16px 32px; display: flex; justify-content: space-between; align-items: center;
}}
header h1 {{ font-size: 18px; margin: 0; color: #f0f6fc; }}
header .meta {{ color: #8b949e; font-size: 12px; }}
nav {{
  background: #161b22; border-bottom: 1px solid #30363d;
  padding: 0 16px; overflow-x: auto; white-space: nowrap;
}}
.tab {{
  display: inline-block; padding: 12px 16px; color: #8b949e;
  text-decoration: none; border-bottom: 3px solid transparent;
  transition: color 0.1s, border-color 0.1s;
}}
.tab:hover {{ color: #c9d1d9; }}
.tab.active {{ color: #58a6ff; border-bottom-color: #58a6ff; }}
.tab-icon {{ margin-right: 6px; opacity: 0.85; }}
main {{ padding: 24px 32px; max-width: 1200px; margin: 0 auto; }}
h2 {{ margin: 0 0 16px; font-size: 18px; color: #f0f6fc; }}
.muted {{ color: #8b949e; font-size: 13px; }}
a {{ color: #58a6ff; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
a.primary {{
  display: inline-block; background: #238636; color: #fff;
  padding: 8px 14px; border-radius: 6px; font-weight: 600;
  margin: 4px 0;
}}
a.primary:hover {{ background: #2ea043; text-decoration: none; }}
code {{
  background: #161b22; padding: 2px 6px; border-radius: 3px;
  font-size: 12px; color: #c9d1d9;
}}
ul {{ list-style: none; padding: 0; margin: 0; }}
li {{ padding: 6px 0; border-bottom: 1px solid #21262d; }}
li:last-child {{ border-bottom: none; }}
.kpi-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 12px; margin: 12px 0;
}}
.kpi {{
  background: #161b22; border: 1px solid #30363d; border-radius: 6px;
  padding: 14px;
}}
.kpi-label {{ color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }}
.kpi-value {{ color: #c9d1d9; font-size: 18px; font-weight: 600; margin-top: 4px; }}
.kpi-positive {{ color: #3fb950; }}
.kpi-negative {{ color: #f85149; }}
.empty {{
  background: #161b22; border: 1px dashed #30363d; border-radius: 6px;
  padding: 24px; text-align: center; color: #8b949e;
}}
.section-card {{
  background: #161b22; border: 1px solid #30363d; border-radius: 8px;
  padding: 16px; margin-bottom: 16px;
}}
table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
th {{
  text-align: left; padding: 8px 12px; background: #21262d;
  color: #c9d1d9; font-size: 11px; text-transform: uppercase;
  letter-spacing: 0.04em; font-weight: 600;
}}
td {{ padding: 6px 12px; border-bottom: 1px solid #21262d; }}
form .row {{ margin-bottom: 12px; }}
form label {{ display: block; color: #8b949e; font-size: 12px; margin-bottom: 4px; }}
form input[type="text"], form input[type="password"] {{
  background: #0d1117; border: 1px solid #30363d; border-radius: 4px;
  padding: 8px 12px; color: #c9d1d9; width: 360px; font-size: 13px;
}}
form input[type="file"] {{
  background: #0d1117; border: 1px solid #30363d; border-radius: 4px;
  padding: 6px; color: #c9d1d9; font-size: 13px;
}}
form.inline {{ display: inline-block; margin: 0; }}
form.inline button.regen {{
  background: #1f6feb; color: #fff; border: 0; padding: 8px 14px;
  border-radius: 6px; font-weight: 600; cursor: pointer; margin-left: 8px;
}}
form.inline button.regen:hover {{ background: #388bfd; }}
form button {{
  background: #238636; color: #fff; border: 0; padding: 8px 14px;
  border-radius: 6px; font-weight: 600; cursor: pointer;
}}
form button:hover {{ background: #2ea043; }}
.footer {{ margin-top: 48px; color: #8b949e; font-size: 12px; padding: 16px 0; border-top: 1px solid #21262d; }}
</style>
</head>
<body>

<header>
  <h1>InvestorClaw</h1>
  <span class="meta">{today} · v4.1.x</span>
</header>

<nav>{nav}</nav>

<main>
{body}
</main>

<div class="footer" style="padding-left:32px;padding-right:32px;max-width:1200px;margin:0 auto;">
  Educational only — not investment advice ·
  <a href="https://github.com/argonautsystems/InvestorClaw">project home</a> ·
  <a href="https://github.com/mnemos-os/mnemos-ic-runtime">runtime</a>
</div>

</body>
</html>"""


def _section_or_empty(rendered: str, empty_msg: str) -> str:
    """Return rendered HTML or an empty-state placeholder."""
    if rendered and rendered.strip():
        return rendered
    return f'<div class="empty">{empty_msg}</div>'


def _list_recent_eod_reports(limit: int = 30) -> list:
    """Return list of (filename, size_kb, mtime_iso) for recent EOD HTML files."""
    if not os.path.isdir(REPORTS_DIR):
        return []
    out = []
    for path in sorted(
        _glob.glob(os.path.join(REPORTS_DIR, "eod_report_*.html")), reverse=True
    )[:limit]:
        fname = os.path.basename(path)
        size_kb = os.path.getsize(path) / 1024
        mtime = _dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime(
            "%Y-%m-%d %H:%M"
        )
        out.append((fname, size_kb, mtime))
    return out


# ----------------------------------------------------------------------------
# Per-tab handlers
# ----------------------------------------------------------------------------


def _overview(get_init_state, message: str = "") -> str:
    snap = get_init_state()
    today = _dt.date.today().isoformat()
    today_compact = today.replace("-", "")
    eod_today_path = os.path.join(REPORTS_DIR, f"eod_report_{today_compact}.html")
    has_today = os.path.isfile(eod_today_path)
    msg_html = (
        f'<div class="section-card" style="border-color:#3fb950;color:#3fb950;">{message}</div>'
        if message else ""
    )

    holdings = _load_json("holdings_summary.json")
    # holdings_summary.json shape: top-level keys include "summary" which holds
    # total_value / net_value / equity_value / bond_value / cash_value, plus
    # *_pct columns. Some legacy variants nest it under "data".
    summary = holdings.get("summary") or holdings.get("data", {}) or {}
    total_value = float(summary.get("total_value") or summary.get("net_value") or 0)
    equity_value = float(summary.get("equity_value", 0) or 0)
    bond_value = float(summary.get("bond_value", 0) or 0)
    cash_value = float(summary.get("cash_value", 0) or 0)
    position_count = _coerce_position_count(summary.get("position_count", 0))

    today_card = (
        f'<a href="/reports/eod_report_{today_compact}.html" class="primary">'
        f'Open today\'s EOD report ({today})</a>'
        if has_today
        else f'<p class="muted">No EOD report for {today} yet.</p>'
    )

    recent = _list_recent_eod_reports(7)
    recent_html = (
        "<ul>"
        + "\n".join(
            f'<li><a href="/reports/{fname}">{fname}</a> '
            f'<span class="muted">— {kb:.0f} KB · {mtime}</span></li>'
            for fname, kb, mtime in recent
        )
        + "</ul>"
        if recent
        else '<p class="muted">No reports generated yet. Run the pipeline.</p>'
    )

    body = f"""
{msg_html}
<h2>Status
  <form class="inline" action="/dashboard/regenerate" method="post">
    <button class="regen" type="submit" title="Refresh all sections + re-run analyzers (~3-5 min)">↻ Regenerate</button>
  </form>
</h2>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Engine</div><div class="kpi-value">{snap['state']}</div></div>
  <div class="kpi"><div class="kpi-label">Init ready</div><div class="kpi-value">{'yes' if snap['ready'] else 'no'}</div></div>
  <div class="kpi"><div class="kpi-label">Total Value</div><div class="kpi-value">${total_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Positions</div><div class="kpi-value">{position_count}</div></div>
</div>

<h2>Allocation</h2>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Equity</div><div class="kpi-value">${equity_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Bonds</div><div class="kpi-value">${bond_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Cash</div><div class="kpi-value">${cash_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">MCP endpoint</div><div class="kpi-value"><code>:18090/mcp</code></div></div>
</div>

<h2>Today's EOD report</h2>
{today_card}

<h2>Recent EOD reports</h2>
{recent_html}

<h2>Quick links</h2>
<ul>
  <li><a href="/reports/">Browse all reports</a></li>
  <li><a href="/healthz">/healthz</a> · liveness JSON</li>
  <li><a href="/api/version">/api/version</a> · bridge version</li>
</ul>
"""
    return _shell("", body, title="Overview")


def _holdings_tab() -> str:
    """Full holdings detail — KPIs, sector breakdown, accounts, every position."""
    summary_doc = _load_json("holdings_summary.json")
    raw_doc = _load_json(".raw/holdings.json")
    analyst = _load_json("analyst_recommendations_summary.json")

    if not summary_doc:
        body = ('<h2>Holdings</h2><div class="empty">No holdings data yet. '
                "Drop a portfolio file into <code>./portfolios/</code> and "
                "run <code>investorclaw setup</code> in the container.</div>")
        return _shell("holdings", body, title="Holdings")

    summary = summary_doc.get("summary", {}) or {}
    total_value = float(summary.get("total_value") or summary.get("net_value") or 0)
    equity_value = float(summary.get("equity_value", 0) or 0)
    bond_value = float(summary.get("bond_value", 0) or 0)
    cash_value = float(summary.get("cash_value", 0) or 0)
    crypto_value = float(summary.get("crypto_value", 0) or 0)
    position_count = _coerce_position_count(summary.get("position_count", 0))
    ugl = float(summary.get("unrealized_gl", 0) or 0)
    ugl_pct = float(summary.get("unrealized_gl_pct", 0) or 0)
    ugl_color = "kpi-positive" if ugl >= 0 else "kpi-negative"

    kpis = f"""
<h2>Portfolio summary</h2>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Total Value</div><div class="kpi-value">${total_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Positions</div><div class="kpi-value">{position_count}</div></div>
  <div class="kpi"><div class="kpi-label">Unrealized G/L</div><div class="kpi-value {ugl_color}">${ugl:,.0f} ({ugl_pct*100:+.2f}%)</div></div>
  <div class="kpi"><div class="kpi-label">Equity</div><div class="kpi-value">${equity_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Bonds</div><div class="kpi-value">${bond_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Cash</div><div class="kpi-value">${cash_value:,.0f}</div></div>
  <div class="kpi"><div class="kpi-label">Crypto</div><div class="kpi-value">${crypto_value:,.0f}</div></div>
</div>"""

    # Sector breakdown — engine ships either {sector: weight_float} (current)
    # or {sector: {weight_pct, value}} (legacy). Handle both.
    def _sector_weight(info):
        if isinstance(info, dict):
            return float(info.get("weight_pct", 0) or 0)
        try:
            return float(info or 0)
        except (TypeError, ValueError):
            return 0.0

    sectors = summary_doc.get("sector_weights", {}) or {}
    if sectors:
        sector_rows = []
        for sec, info in sorted(sectors.items(), key=lambda kv: -_sector_weight(kv[1])):
            if isinstance(info, dict):
                weight = float(info.get("weight_pct", 0) or 0)
                value = float(info.get("value", 0) or 0)
            else:
                weight = _sector_weight(info)
                value = total_value * weight / 100
            sector_rows.append(
                f"<tr><td>{_h(sec)}</td>"
                f'<td style="text-align:right;">{weight:.2f}%</td>'
                f'<td style="text-align:right;">${value:,.0f}</td></tr>'
            )
        sector_block = (
            "<h2>Sector allocation</h2><div class=\"section-card\"><table>"
            "<tr><th>Sector</th><th style=\"text-align:right;\">Weight</th>"
            "<th style=\"text-align:right;\">Value</th></tr>"
            + "".join(sector_rows) + "</table></div>"
        )
    else:
        sector_block = ""

    # Accounts breakdown — defensive against engine returning floats or dicts.
    def _acct_value(info):
        if isinstance(info, dict):
            try:
                return float(info.get("value", 0) or 0)
            except (TypeError, ValueError):
                return 0.0
        try:
            return float(info or 0)
        except (TypeError, ValueError):
            return 0.0

    accounts = summary_doc.get("accounts", {}) or {}
    if accounts:
        acct_rows = []
        for name, info in sorted(accounts.items(), key=lambda kv: -_acct_value(kv[1])):
            info_dict = info if isinstance(info, dict) else {}
            value = _acct_value(info)
            ftype = _h(str(info_dict.get("financial_type", "—")))
            classification = _h(str(info_dict.get("classification", "—")))
            acct_rows.append(
                f"<tr><td>{_h(name)}</td>"
                f'<td>{ftype}</td>'
                f'<td>{classification}</td>'
                f'<td style="text-align:right;">${value:,.0f}</td>'
                f'<td style="text-align:right;">{(value/total_value*100 if total_value else 0):.1f}%</td></tr>'
            )
        acct_block = (
            "<h2>Accounts</h2><div class=\"section-card\"><table>"
            "<tr><th>Account</th><th>Type</th><th>Class</th>"
            "<th style=\"text-align:right;\">Value</th>"
            "<th style=\"text-align:right;\">Weight</th></tr>"
            + "".join(acct_rows) + "</table></div>"
        )
    else:
        acct_block = ""

    # All positions — pull from .raw/holdings.json (CDM portfolioState.positions)
    positions = (
        raw_doc.get("portfolio", {})
        .get("portfolioState", {})
        .get("positions", [])
    )
    if positions:
        pos_rows = []
        # Sort by market value descending
        positions_sorted = sorted(
            positions,
            key=lambda p: -float(p.get("marketValue", 0) or 0),
        )
        for p in positions_sorted:
            sym = _h(((p.get("asset") or {}).get("securityName")
                      or (p.get("product") or {}).get("productIdentifier", {}).get("identifier", "")))
            sec_type = _h((p.get("asset") or {}).get("securityType", ""))
            sector = _h((p.get("asset") or {}).get("sector", "—"))
            qty = float((p.get("priceQuantity") or {}).get("quantity", {}).get("amount", 0) or 0)
            cur_price = float((p.get("priceQuantity") or {}).get("currentPrice", {}).get("amount", 0) or 0)
            cost_price = float((p.get("priceQuantity") or {}).get("costBasisPrice", {}).get("amount", 0) or 0)
            mv = float(p.get("marketValue", 0) or 0)
            cb = float(p.get("costBasis", 0) or 0)
            gl = float(p.get("unrealizedGainLoss", 0) or 0)
            gl_pct = float(p.get("unrealizedGainLossPct", 0) or 0)
            gl_color = "#3fb950" if gl >= 0 else "#f85149"
            weight = (mv / total_value * 100) if total_value else 0
            pos_rows.append(
                f"<tr>"
                f"<td><strong>{sym}</strong></td>"
                f"<td>{sec_type}</td>"
                f"<td>{sector}</td>"
                f'<td style="text-align:right;">{qty:,.2f}</td>'
                f'<td style="text-align:right;">${cur_price:,.2f}</td>'
                f'<td style="text-align:right;">${cost_price:,.2f}</td>'
                f'<td style="text-align:right;">${mv:,.0f}</td>'
                f'<td style="text-align:right;">{weight:.2f}%</td>'
                f'<td style="text-align:right;color:{gl_color};">${gl:,.0f}</td>'
                f'<td style="text-align:right;color:{gl_color};">{gl_pct*100:+.2f}%</td>'
                f"</tr>"
            )
        pos_table = (
            f"<h2>All positions ({len(positions)})</h2>"
            "<div class=\"section-card\" style=\"overflow-x:auto;\"><table>"
            "<tr><th>Symbol</th><th>Type</th><th>Sector</th>"
            "<th style=\"text-align:right;\">Qty</th>"
            "<th style=\"text-align:right;\">Price</th>"
            "<th style=\"text-align:right;\">Cost</th>"
            "<th style=\"text-align:right;\">Market Value</th>"
            "<th style=\"text-align:right;\">Weight</th>"
            "<th style=\"text-align:right;\">G/L $</th>"
            "<th style=\"text-align:right;\">G/L %</th></tr>"
            + "".join(pos_rows) + "</table></div>"
        )
    else:
        # Fall back to top_equity from summary
        top = summary_doc.get("top_equity", []) or []
        if top:
            rows = []
            for h in top:
                sym = _h(h.get("symbol", ""))
                sec = _h(h.get("sector", "—"))
                value = float(h.get("value", 0) or 0)
                weight = float(h.get("weight_pct", 0) or 0)
                gl = float(h.get("gl_pct", 0) or 0)
                gl_color = "#3fb950" if gl >= 0 else "#f85149"
                rows.append(
                    f"<tr><td><strong>{sym}</strong></td><td>{sec}</td>"
                    f'<td style="text-align:right;">${value:,.0f}</td>'
                    f'<td style="text-align:right;">{weight:.2f}%</td>'
                    f'<td style="text-align:right;color:{gl_color};">{gl:+.2f}%</td></tr>'
                )
            pos_table = (
                f"<h2>Top equity holdings (top {len(top)})</h2>"
                "<div class=\"section-card\"><p class=\"muted\">"
                "Full position-level detail unavailable; install or refresh "
                "the portfolio for the complete table.</p>"
                "<table><tr><th>Symbol</th><th>Sector</th>"
                "<th style=\"text-align:right;\">Value</th>"
                "<th style=\"text-align:right;\">Weight</th>"
                "<th style=\"text-align:right;\">G/L</th></tr>"
                + "".join(rows) + "</table></div>"
            )
        else:
            pos_table = '<div class="empty">No position-level detail.</div>'

    body = kpis + sector_block + acct_block + pos_table
    return _shell("holdings", body, title="Holdings")


def _h(s) -> str:
    """HTML-escape helper."""
    if s is None:
        return ""
    import html
    return html.escape(str(s))


def _performance_tab() -> str:
    perf = _load_json("performance.json")
    if not perf:
        body = '<h2>Performance</h2><div class="empty">No performance data. Run <code>investorclaw performance</code> in the container.</div>'
    elif _T:
        body = "<h2>Performance</h2>\n" + _T._render_performance_summary(perf)
    else:
        body = "<h2>Performance</h2>\n" + _section_or_empty("", "Engine helpers unavailable.")
    return _shell("performance", body, title="Performance")


def _whatchanged_tab() -> str:
    wc = _load_json("whatchanged.json")
    if _T:
        body = "<h2>What Changed</h2>\n" + _section_or_empty(
            _T._render_whatchanged(wc),
            "No attribution data. Run <code>investorclaw whatchanged</code> in the container.",
        )
    else:
        body = "<h2>What Changed</h2>\n" + _section_or_empty("", "Engine helpers unavailable.")
    return _shell("whatchanged", body, title="What Changed")


def _scenarios_tab() -> str:
    scen = _load_json("scenario.json")
    if _T:
        body = "<h2>Scenarios &amp; Stress Tests</h2>\n" + _section_or_empty(
            _T._render_scenario(scen),
            "No scenario data. Run <code>investorclaw scenario</code> in the container.",
        )
    else:
        body = "<h2>Scenarios</h2>\n" + _section_or_empty("", "Engine helpers unavailable.")
    return _shell("scenarios", body, title="Scenarios")


def _bonds_tab() -> str:
    bonds = _load_json("bond_analysis.json")
    if _T:
        body = "<h2>Fixed Income</h2>\n" + _section_or_empty(
            _T._render_bond_summary(bonds),
            "No bond data (your portfolio may have no bond holdings, or run <code>investorclaw bonds</code>).",
        )
    else:
        body = "<h2>Fixed Income</h2>\n" + _section_or_empty("", "Engine helpers unavailable.")
    return _shell("bonds", body, title="Bonds")


def _analyst_tab() -> str:
    a = _load_json("analyst_recommendations_summary.json")
    if _T:
        body = "<h2>Analyst Coverage</h2>\n" + _section_or_empty(
            _T._render_analyst_summary(a),
            "No analyst data. Run <code>investorclaw analyst</code>.",
        )
    else:
        body = "<h2>Analyst</h2>\n" + _section_or_empty("", "Engine helpers unavailable.")
    return _shell("analyst", body, title="Analyst")


def _news_tab() -> str:
    """Full per-holding news coverage — every headline, sortable, with sentiment + impact."""
    cache = _load_json("portfolio_news_cache.json")
    summary = _load_json("portfolio_news.json")

    if not cache and not summary:
        body = ('<h2>News</h2><div class="empty">No news data yet. '
                "Run <code>investorclaw news</code> in the container.</div>")
        return _shell("news", body, title="News")

    per_symbol = cache.get("per_symbol", {}) if cache else {}
    all_news = cache.get("all_news", []) if cache else []
    timestamp = cache.get("timestamp", "") if cache else ""
    symbols_covered = cache.get("symbols", []) if cache else []
    skipped = cache.get("skipped_symbols", []) if cache else []

    # Top-of-page summary KPIs
    total_items = sum(len(items) for items in per_symbol.values()) if per_symbol else len(all_news)
    sym_with_news = len([s for s, items in per_symbol.items() if items]) if per_symbol else 0
    kpis = f"""
<h2>News coverage</h2>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Symbols covered</div><div class="kpi-value">{len(symbols_covered)}</div></div>
  <div class="kpi"><div class="kpi-label">With news</div><div class="kpi-value">{sym_with_news}</div></div>
  <div class="kpi"><div class="kpi-label">Total items</div><div class="kpi-value">{total_items}</div></div>
  <div class="kpi"><div class="kpi-label">Last fetch</div><div class="kpi-value" style="font-size:13px;">{_h(timestamp[:19].replace('T',' '))}</div></div>
</div>
"""

    # Editorial summary (posture / tailwinds / risks) from portfolio_news.json
    if summary:
        posture = _h(summary.get("posture", "—"))
        narrative = _h(summary.get("narrative", "")).replace("\n", "<br>")
        tailwinds = summary.get("key_tailwinds", []) or []
        risks = summary.get("key_risks", []) or []
        tailwinds_html = ("<ul>" + "".join(f"<li>{_h(t)}</li>" for t in tailwinds) + "</ul>") if tailwinds else ""
        risks_html = ("<ul>" + "".join(f"<li>{_h(r)}</li>" for r in risks) + "</ul>") if risks else ""

        editorial = f"""
<h2>Editorial summary</h2>
<div class="section-card">
  <p><strong>Posture:</strong> {posture}</p>
  {f'<p>{narrative}</p>' if narrative else ''}
  {f'<p><strong>Key tailwinds</strong></p>{tailwinds_html}' if tailwinds else ''}
  {f'<p><strong>Key risks</strong></p>{risks_html}' if risks else ''}
</div>
"""
    else:
        editorial = ""

    # Per-symbol news listing
    def _sentiment_color(s) -> str:
        s = (str(s) or "").lower()
        if "positive" in s or "bull" in s:
            return "#3fb950"
        if "negative" in s or "bear" in s:
            return "#f85149"
        return "#8b949e"

    def _item_html(item: Dict[str, Any]) -> str:
        title = _h(item.get("title", ""))
        link = item.get("link") or item.get("url") or ""
        source = _h(item.get("source", ""))
        date = _h(str(item.get("publish_date", ""))[:19].replace("T", " "))
        sentiment = item.get("sentiment", "neutral")
        sentiment_color = _sentiment_color(sentiment)
        confidence = item.get("confidence")
        impact_pct = item.get("impact_pct")
        summary_text = _h(item.get("summary", ""))[:300]

        meta_bits = [f'<span style="color:{sentiment_color};font-weight:600;">{_h(sentiment)}</span>']
        if confidence is not None:
            try:
                meta_bits.append(f'conf {float(confidence):.0%}')
            except Exception:
                pass
        if impact_pct is not None:
            try:
                meta_bits.append(f'impact {float(impact_pct):+.2f}%')
            except Exception:
                pass
        if source:
            meta_bits.append(_h(source))
        if date:
            meta_bits.append(date)
        meta = ' · '.join(meta_bits)

        title_html = (
            f'<a href="{_h(link)}" target="_blank" rel="noopener noreferrer">{title}</a>'
            if link else title
        )
        return (
            f'<div style="padding:10px 0;border-bottom:1px solid #21262d;">'
            f'<div style="font-weight:600;margin-bottom:4px;">{title_html}</div>'
            f'<div style="font-size:12px;color:#8b949e;margin-bottom:4px;">{meta}</div>'
            + (f'<div style="font-size:13px;color:#c9d1d9;">{summary_text}…</div>' if summary_text else '')
            + '</div>'
        )

    if per_symbol:
        # Sort symbols by item count (most news first), then alphabetically
        symbols_sorted = sorted(
            per_symbol.items(),
            key=lambda kv: (-len(kv[1] or []), kv[0]),
        )
        per_symbol_blocks = []
        for sym, items in symbols_sorted:
            if not items:
                continue
            items_html = "".join(_item_html(it) for it in items)
            per_symbol_blocks.append(
                f'<details open style="margin-bottom:16px;">'
                f'<summary style="cursor:pointer;padding:8px 12px;background:#161b22;'
                f'border:1px solid #30363d;border-radius:6px;font-weight:600;">'
                f'<span style="color:#58a6ff;">{_h(sym)}</span> '
                f'<span style="color:#8b949e;font-weight:normal;font-size:12px;">— {len(items)} item{"s" if len(items)!=1 else ""}</span>'
                f'</summary>'
                f'<div style="padding:8px 12px;background:#0d1117;border:1px solid #30363d;border-top:none;border-radius:0 0 6px 6px;">'
                f'{items_html}'
                f'</div></details>'
            )
        per_sym_block = (
            f'<h2>News by holding ({sym_with_news} symbols)</h2>'
            + "".join(per_symbol_blocks)
        )
    else:
        per_sym_block = ""

    skipped_block = ""
    if skipped:
        skipped_block = (
            f'<h2 style="margin-top:32px;">Skipped symbols ({len(skipped)})</h2>'
            f'<div class="section-card"><p class="muted">No news fetched for these holdings '
            "(provider didn't return data, or rate-limit hit):</p>"
            f'<p style="font-family:monospace;font-size:12px;">{_h(", ".join(skipped))}</p></div>'
        )

    body = kpis + editorial + per_sym_block + skipped_block
    return _shell("news", body, title="News")


def _synthesis_tab() -> str:
    syn = _load_json("portfolio_analysis.json")
    if not syn:
        body = '<h2>Synthesis</h2><div class="empty">No synthesis data. Run <code>investorclaw synthesize</code>.</div>'
        return _shell("synthesis", body, title="Synthesis")

    # synthesis is a dict; render the narrative and any FA topics
    narr = (syn.get("data") or syn).get("narrative") or syn.get("narrative") or ""
    parts = ["<h2>Synthesis</h2>"]
    if narr:
        narr_html = "<br>".join(line.strip() for line in narr.splitlines() if line.strip())
        parts.append(f'<div class="section-card">{narr_html}</div>')
    # FA topics
    if _T:
        try:
            from ic_engine.commands.fa_discussion import extract_fa_topics
            topics = extract_fa_topics(pathlib.Path(REPORTS_DIR), preloaded={"synthesize": syn})
            parts.append(_section_or_empty(_T._render_fa_topics(topics), ""))
        except Exception:
            pass
    body = "\n".join(parts)
    return _shell("synthesis", body, title="Synthesis")


def _optimize_tab() -> str:
    """Optimization + rebalance — covers cobol p09/p10/p11/p12/p13."""
    opt = _load_json("optimize.json")
    rebal = _load_json("rebalance.json")
    rebal_tax = _load_json("rebalance_tax.json")
    parts = ["<h2>Portfolio Optimization &amp; Rebalance</h2>"]
    parts.append(
        '<p class="muted">Sharpe-maximizing and minimum-volatility allocations from PyPortfolioOpt, '
        'plus rebalance trades against the target allocation (with optional tax-impact view).</p>'
    )

    def _alloc_block(title: str, alloc: dict, expected_sharpe=None, expected_vol=None) -> str:
        if not alloc:
            return ""
        rows = []
        for sym, w in sorted(alloc.items(), key=lambda kv: -float(kv[1] or 0)):
            try:
                pct = float(w) * 100
            except Exception:
                pct = 0
            if pct < 0.05:
                continue
            rows.append(f'<tr><td><code>{_h(sym)}</code></td><td style="text-align:right;">{pct:.2f}%</td></tr>')
        meta_bits = []
        if expected_sharpe is not None:
            try:
                meta_bits.append(f"Sharpe {float(expected_sharpe):.3f}")
            except Exception:
                pass
        if expected_vol is not None:
            try:
                meta_bits.append(f"Vol {float(expected_vol)*100:.2f}%")
            except Exception:
                pass
        meta = (' <span class="muted">— ' + ' · '.join(meta_bits) + '</span>') if meta_bits else ''
        return (
            f'<h3>{title}{meta}</h3>'
            f'<div class="section-card"><table>'
            f'<tr><th>Symbol</th><th style="text-align:right;">Weight</th></tr>'
            + "".join(rows) + '</table></div>'
        )

    if opt:
        # Two common shapes: {max_sharpe: {...}, min_vol: {...}} or top-level allocation
        ms = opt.get("max_sharpe") or opt.get("data", {}).get("max_sharpe") or {}
        mv = opt.get("min_volatility") or opt.get("data", {}).get("min_volatility") or {}
        parts.append(_alloc_block(
            "Maximum Sharpe allocation",
            ms.get("weights") or ms.get("allocation") or {},
            ms.get("expected_sharpe"),
            ms.get("expected_volatility"),
        ))
        parts.append(_alloc_block(
            "Minimum-volatility allocation",
            mv.get("weights") or mv.get("allocation") or {},
            mv.get("expected_sharpe"),
            mv.get("expected_volatility"),
        ))
        if not ms and not mv:
            # fallback — just dump weights if present
            top = opt.get("weights") or opt.get("data", {}).get("weights") or {}
            parts.append(_alloc_block("Optimal allocation", top))
    else:
        parts.append(
            '<div class="empty">No optimization run yet. '
            'Run <code>investorclaw optimize</code> in the container, or click '
            '<strong>Regenerate</strong> on the Overview tab.</div>'
        )

    # Rebalance trades — current vs target
    def _trades_block(title: str, doc: dict) -> str:
        if not doc:
            return ""
        trades = (
            doc.get("trades")
            or doc.get("data", {}).get("trades")
            or doc.get("rebalance_trades", [])
            or []
        )
        if not trades:
            return ""
        rows = []
        for t in trades[:200]:
            sym = _h(str(t.get("symbol", "")))
            action = _h(str(t.get("action") or t.get("side") or ""))
            current_pct = t.get("current_pct") or t.get("current_weight")
            target_pct = t.get("target_pct") or t.get("target_weight")
            delta = t.get("delta_pct") or t.get("trade_pct")
            dollar = t.get("dollar_amount") or t.get("notional") or t.get("amount")
            tax = t.get("tax_impact") or t.get("tax_cost")

            def _pct(v):
                try:
                    return f"{float(v)*100:+.2f}%" if abs(float(v)) <= 1 else f"{float(v):+.2f}%"
                except Exception:
                    return "—"

            def _money(v):
                try:
                    return f"${float(v):,.0f}"
                except Exception:
                    return "—"

            rows.append(
                f'<tr><td><code>{sym}</code></td><td>{action}</td>'
                f'<td>{_pct(current_pct)}</td><td>{_pct(target_pct)}</td>'
                f'<td>{_pct(delta)}</td><td>{_money(dollar)}</td>'
                f'<td>{_money(tax) if tax is not None else "—"}</td></tr>'
            )
        return (
            f'<h3>{title}</h3>'
            f'<div class="section-card"><table>'
            f'<tr><th>Symbol</th><th>Action</th><th>Current</th><th>Target</th>'
            f'<th>Δ</th><th>Notional</th><th>Tax impact</th></tr>'
            + "".join(rows) + '</table></div>'
        )

    parts.append(_trades_block("Rebalance trades", rebal))
    parts.append(_trades_block("Tax-aware rebalance trades", rebal_tax))
    if not rebal and not rebal_tax:
        parts.append(
            '<h3>Rebalance</h3>'
            '<div class="empty">No rebalance run yet. '
            'Run <code>investorclaw rebalance</code> or <code>investorclaw rebalance-tax</code>.</div>'
        )

    return _shell("optimize", "\n".join(parts), title="Optimize")


def _cashflow_tab() -> str:
    """Projected cash flow — dividends + bond coupons. Covers cobol p25."""
    cf = _load_json("cashflow.json")
    parts = ["<h2>Projected cash flow</h2>"]
    parts.append('<p class="muted">Forward-looking dividends and bond coupons over the next quarter / year.</p>')
    if not cf:
        parts.append(
            '<div class="empty">No cashflow data. '
            'Run <code>investorclaw cashflow</code> in the container.</div>'
        )
        return _shell("cashflow", "\n".join(parts), title="Cashflow")

    data = cf.get("data") or cf
    total_q = data.get("total_quarter") or data.get("quarter_total") or data.get("next_quarter_income")
    total_y = data.get("total_year") or data.get("year_total") or data.get("annual_income")
    div = data.get("dividends_total") or data.get("dividend_income")
    coup = data.get("coupons_total") or data.get("coupon_income")

    def _money(v):
        try:
            return f"${float(v):,.0f}"
        except Exception:
            return "—"

    parts.append(f"""<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Next quarter</div><div class="kpi-value">{_money(total_q)}</div></div>
  <div class="kpi"><div class="kpi-label">Next 12 months</div><div class="kpi-value">{_money(total_y)}</div></div>
  <div class="kpi"><div class="kpi-label">Dividends (annual)</div><div class="kpi-value">{_money(div)}</div></div>
  <div class="kpi"><div class="kpi-label">Coupons (annual)</div><div class="kpi-value">{_money(coup)}</div></div>
</div>""")

    rows_in = data.get("by_symbol") or data.get("schedule") or data.get("payments") or []
    if rows_in:
        rows = []
        for item in rows_in[:300]:
            sym = _h(str(item.get("symbol", "")))
            kind = _h(str(item.get("type") or item.get("kind") or ""))
            pay_date = _h(str(item.get("date") or item.get("ex_date") or item.get("pay_date") or "")[:10])
            amt = item.get("amount") or item.get("payment")
            yld = item.get("yield") or item.get("dividend_yield")
            rows.append(
                f'<tr><td><code>{sym}</code></td><td>{kind}</td>'
                f'<td>{pay_date}</td><td style="text-align:right;">{_money(amt)}</td>'
                f'<td style="text-align:right;">{(f"{float(yld)*100:.2f}%" if yld is not None else "—")}</td></tr>'
            )
        parts.append(
            '<h3>Schedule</h3>'
            '<div class="section-card"><table>'
            '<tr><th>Symbol</th><th>Type</th><th>Date</th>'
            '<th style="text-align:right;">Amount</th>'
            '<th style="text-align:right;">Yield</th></tr>'
            + "".join(rows) + '</table></div>'
        )
    return _shell("cashflow", "\n".join(parts), title="Cashflow")


def _peer_tab() -> str:
    """Peer / benchmark comparison — covers cobol p26."""
    peer = _load_json("peer.json")
    parts = ["<h2>Benchmark comparison</h2>"]
    parts.append('<p class="muted">Your portfolio vs broad-market benchmarks (VTI, SPY, AGG, etc.). Returns, Sharpe, drawdown side-by-side.</p>')
    if not peer:
        parts.append(
            '<div class="empty">No peer comparison yet. '
            'Run <code>investorclaw peer</code> in the container.</div>'
        )
        return _shell("peer", "\n".join(parts), title="Peer")

    data = peer.get("data") or peer
    benchmarks = data.get("benchmarks") or data.get("comparison") or []
    portfolio_metrics = data.get("portfolio_metrics") or data.get("portfolio") or {}

    if portfolio_metrics:
        def _fmt(v, kind="pct"):
            if v is None:
                return "—"
            try:
                if kind == "pct":
                    f = float(v)
                    return f"{f*100:+.2f}%" if abs(f) <= 1 else f"{f:+.2f}%"
                return f"{float(v):.3f}"
            except Exception:
                return "—"

        parts.append(f"""<h3>Your portfolio</h3>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Total return</div><div class="kpi-value">{_fmt(portfolio_metrics.get('total_return'))}</div></div>
  <div class="kpi"><div class="kpi-label">Annualized</div><div class="kpi-value">{_fmt(portfolio_metrics.get('annualized_return'))}</div></div>
  <div class="kpi"><div class="kpi-label">Sharpe</div><div class="kpi-value">{_fmt(portfolio_metrics.get('sharpe'),'num')}</div></div>
  <div class="kpi"><div class="kpi-label">Max drawdown</div><div class="kpi-value">{_fmt(portfolio_metrics.get('max_drawdown'))}</div></div>
</div>""")

    if benchmarks:
        rows = []
        for b in benchmarks:
            sym = _h(str(b.get("symbol") or b.get("benchmark") or ""))
            tot = b.get("total_return") or b.get("return")
            ann = b.get("annualized_return")
            sh = b.get("sharpe")
            dd = b.get("max_drawdown")
            corr = b.get("correlation")
            beta = b.get("beta")

            def _p(v):
                if v is None:
                    return "—"
                try:
                    f = float(v)
                    return f"{f*100:+.2f}%" if abs(f) <= 1 else f"{f:+.2f}%"
                except Exception:
                    return "—"

            def _n(v):
                if v is None:
                    return "—"
                try:
                    return f"{float(v):.3f}"
                except Exception:
                    return "—"

            rows.append(
                f'<tr><td><code>{sym}</code></td><td>{_p(tot)}</td><td>{_p(ann)}</td>'
                f'<td>{_n(sh)}</td><td>{_p(dd)}</td><td>{_n(corr)}</td><td>{_n(beta)}</td></tr>'
            )
        parts.append(
            '<h3>Benchmarks</h3>'
            '<div class="section-card"><table>'
            '<tr><th>Symbol</th><th>Total return</th><th>Annualized</th>'
            '<th>Sharpe</th><th>Max DD</th><th>Corr</th><th>Beta</th></tr>'
            + "".join(rows) + '</table></div>'
        )
    return _shell("peer", "\n".join(parts), title="Peer")


def _markets_tab() -> str:
    """Broad-market / crypto / FX context — covers cobol p17/p18/p21/p22."""
    mk = _load_json("markets.json")
    parts = ["<h2>Markets snapshot</h2>"]
    parts.append('<p class="muted">Indices, crypto, FX. Updated by <code>investorclaw markets</code> (or auto-refreshed by Regenerate).</p>')
    if not mk:
        parts.append(
            '<div class="empty">No markets snapshot yet. '
            'Run <code>investorclaw markets</code> or click <strong>Regenerate</strong>.</div>'
        )
        return _shell("markets", "\n".join(parts), title="Markets")

    data = mk.get("data") or mk

    def _block(title: str, items: list) -> str:
        if not items:
            return ""
        rows = []
        for it in items:
            sym = _h(str(it.get("symbol") or it.get("ticker") or it.get("name") or ""))
            name = _h(str(it.get("name") or ""))
            price = it.get("price") or it.get("last")
            chg = it.get("change_pct") or it.get("pct_change") or it.get("change_percent")

            def _money(v):
                if v is None:
                    return "—"
                try:
                    return f"${float(v):,.2f}"
                except Exception:
                    return "—"

            def _pct(v):
                if v is None:
                    return "—"
                try:
                    f = float(v)
                    return f"{f*100:+.2f}%" if abs(f) <= 1 else f"{f:+.2f}%"
                except Exception:
                    return "—"

            color = ""
            try:
                f = float(chg or 0)
                color = "color:#3fb950;" if f > 0 else ("color:#f85149;" if f < 0 else "")
            except Exception:
                pass
            rows.append(
                f'<tr><td><code>{sym}</code></td><td>{name}</td>'
                f'<td style="text-align:right;">{_money(price)}</td>'
                f'<td style="text-align:right;{color}">{_pct(chg)}</td></tr>'
            )
        return (
            f'<h3>{title}</h3>'
            f'<div class="section-card"><table>'
            f'<tr><th>Symbol</th><th>Name</th>'
            f'<th style="text-align:right;">Price</th><th style="text-align:right;">Change</th></tr>'
            + "".join(rows) + '</table></div>'
        )

    parts.append(_block("Indices", data.get("indices") or []))
    parts.append(_block("Crypto", data.get("crypto") or []))
    parts.append(_block("Foreign exchange", data.get("forex") or data.get("fx") or []))
    parts.append(_block("Fixed income / yields", data.get("rates") or data.get("yields") or []))

    summary = data.get("summary") or data.get("narrative")
    if summary:
        parts.append(
            '<h3>Summary</h3>'
            f'<div class="section-card">{_h(str(summary)).replace(chr(10),"<br>")}</div>'
        )
    return _shell("markets", "\n".join(parts), title="Markets")


def _lookup_tab(symbol: str = "", message: str = "") -> str:
    """Per-ticker lookup — covers cobol p27."""
    msg_html = (
        f'<div class="section-card" style="border-color:#3fb950;color:#3fb950;">{_h(message)}</div>'
        if message else ""
    )
    sym_clean = "".join(c for c in (symbol or "").upper() if c.isalnum() or c in "-.")[:12]

    form = f"""<h2>Symbol lookup</h2>
<p class="muted">Quick quote + fundamentals for any ticker. Uses the same providers as the engine (yfinance / Massive / Finnhub fallback).</p>
<div class="section-card">
  <form action="/dashboard/lookup" method="get">
    <div class="row">
      <label>Symbol (e.g. AAPL, MSFT, BTC-USD)</label>
      <input type="text" name="symbol" value="{_h(sym_clean)}" placeholder="AAPL" required>
    </div>
    <button type="submit">Look up</button>
  </form>
</div>
"""

    detail = ""
    if sym_clean:
        # Look for a cached lookup; fall back to a hint if missing.
        lk = _load_json(f"lookup_{sym_clean.lower()}.json") or _load_json(f"lookup/{sym_clean}.json")
        if lk:
            d = lk.get("data") or lk
            name = _h(str(d.get("name") or d.get("longName") or sym_clean))
            price = d.get("price") or d.get("last") or d.get("regularMarketPrice")
            chg = d.get("change_pct") or d.get("regularMarketChangePercent")
            sector = _h(str(d.get("sector") or ""))
            industry = _h(str(d.get("industry") or ""))
            mcap = d.get("market_cap") or d.get("marketCap")
            pe = d.get("pe_ratio") or d.get("trailingPE")
            div_y = d.get("dividend_yield") or d.get("dividendYield")
            summary = _h(str(d.get("summary") or d.get("longBusinessSummary") or ""))[:1200]

            def _money(v):
                if v is None:
                    return "—"
                try:
                    return f"${float(v):,.2f}"
                except Exception:
                    return "—"

            def _big(v):
                if v is None:
                    return "—"
                try:
                    f = float(v)
                    if f >= 1e12: return f"${f/1e12:.2f}T"
                    if f >= 1e9: return f"${f/1e9:.2f}B"
                    if f >= 1e6: return f"${f/1e6:.2f}M"
                    return f"${f:,.0f}"
                except Exception:
                    return "—"

            def _pct(v):
                if v is None:
                    return "—"
                try:
                    f = float(v)
                    return f"{f*100:+.2f}%" if abs(f) <= 1 else f"{f:+.2f}%"
                except Exception:
                    return "—"

            detail = f"""<h3>{_h(sym_clean)} — {name}</h3>
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Last price</div><div class="kpi-value">{_money(price)}</div></div>
  <div class="kpi"><div class="kpi-label">Change</div><div class="kpi-value">{_pct(chg)}</div></div>
  <div class="kpi"><div class="kpi-label">Market cap</div><div class="kpi-value">{_big(mcap)}</div></div>
  <div class="kpi"><div class="kpi-label">P/E (trailing)</div><div class="kpi-value">{(f'{float(pe):.2f}' if pe is not None else '—')}</div></div>
  <div class="kpi"><div class="kpi-label">Dividend yield</div><div class="kpi-value">{_pct(div_y)}</div></div>
  <div class="kpi"><div class="kpi-label">Sector</div><div class="kpi-value" style="font-size:14px;">{sector or '—'}</div></div>
</div>
{f'<div class="section-card"><p>{summary}</p></div>' if summary else ''}
"""
        else:
            detail = (
                f'<div class="empty">No cached lookup for <code>{_h(sym_clean)}</code>. '
                f'Run <code>investorclaw lookup {_h(sym_clean)}</code> in the container '
                f'to populate (or wait for the next Regenerate sweep).</div>'
            )

    body = msg_html + form + detail
    return _shell("lookup", body, title="Lookup")


def _reports_tab() -> str:
    reports = _list_recent_eod_reports(50)
    if not reports:
        body = '<h2>Reports</h2><div class="empty">No EOD reports generated yet.</div>'
    else:
        rows = []
        for fname, kb, mtime in reports:
            rows.append(
                f'<tr><td><a href="/reports/{fname}">{fname}</a></td>'
                f'<td>{kb:.0f} KB</td><td class="muted">{mtime}</td></tr>'
            )
        table = (
            "<table><tr><th>Report</th><th>Size</th><th>Generated</th></tr>"
            + "".join(rows)
            + "</table>"
        )
        body = f"""<h2>Reports archive</h2>
<p class="muted">{len(reports)} EOD reports on disk. Click a row to view in this browser, or download the HTML.</p>
<div class="section-card">{table}</div>
<h2>JSON snapshots</h2>
<p class="muted">Raw section data behind the dashboard tabs.</p>
<ul>"""
        json_files = sorted(_glob.glob(os.path.join(REPORTS_DIR, "*.json")))
        for jp in json_files:
            jname = os.path.basename(jp)
            jsize = os.path.getsize(jp) / 1024
            body += f'<li><a href="/reports/{jname}">{jname}</a> <span class="muted">— {jsize:.1f} KB</span></li>'
        body += "</ul>"
    return _shell("reports", body, title="Reports")


def _settings_tab(get_keys_status, message: str = "") -> str:
    status = get_keys_status()
    configured = status.get("configured", []) or []
    settable = status.get("settable", []) or []
    msg_html = (
        f'<div class="section-card" style="border-color:#3fb950;color:#3fb950;">{message}</div>'
        if message
        else ""
    )

    config_rows = []
    for key in configured:
        config_rows.append(
            f"<tr><td><code>{key}</code></td>"
            "<td><span class=\"kpi-positive\">configured</span></td></tr>"
        )
    for key in settable:
        if key not in configured:
            config_rows.append(
                f"<tr><td><code>{key}</code></td>"
                "<td class=\"muted\">not set</td></tr>"
            )

    set_form = """<form action="/dashboard/settings/keys" method="post">
  <div class="row">
    <label>Key name</label>
    <input type="text" name="key_name" placeholder="TOGETHER_API_KEY" required>
  </div>
  <div class="row">
    <label>Value (saved to /data/keys.env mode 0600 inside the container)</label>
    <input type="password" name="key_value" placeholder="tgp_v1_..." required>
  </div>
  <button type="submit">Save key</button>
</form>"""

    # Portfolio upload — list current files + form to add a new one.
    portfolio_files = []
    pdir = pathlib.Path(os.environ.get("IC_PORTFOLIO_DIR", "/data/portfolios"))
    if pdir.is_dir():
        try:
            for p in sorted(pdir.iterdir()):
                if p.is_file() and not p.name.startswith("."):
                    portfolio_files.append((p.name, p.stat().st_size))
        except OSError:
            pass

    files_rows = "".join(
        f'<tr><td><code>{_h(name)}</code></td>'
        f'<td style="text-align:right;">{size/1024:.1f} KB</td></tr>'
        for name, size in portfolio_files
    ) or '<tr><td colspan="2" class="muted">No portfolio files uploaded yet.</td></tr>'

    upload_form = """<form action="/dashboard/upload" method="post" enctype="multipart/form-data">
  <div class="row">
    <label>Portfolio file (CSV, XLSX, PDF — saved to <code>/data/portfolios/</code>)</label>
    <input type="file" name="portfolio_file" required accept=".csv,.tsv,.xls,.xlsx,.pdf,.json,.ofx,.qfx">
  </div>
  <button type="submit">Upload &amp; refresh</button>
</form>"""

    body = f"""<h2>Settings — provider keys</h2>
{msg_html}
<p class="muted">Keys persist to <code>/data/keys.env</code> inside the named Docker volume,
mode 0600. Allowlisted names only — arbitrary key names are rejected.</p>

<div class="section-card">
  <table>
    <tr><th>Key</th><th>Status</th></tr>
    {"".join(config_rows)}
  </table>
</div>

<h2>Add or update a key</h2>
<div class="section-card">
{set_form}
</div>

<h2>Portfolio files</h2>
<p class="muted">Files are auto-detected by <code>investorclaw setup</code>. Drop a CSV / XLSX / PDF
broker statement here; the upload triggers a refresh and the new positions appear in the Holdings tab.</p>
<div class="section-card">
  <table>
    <tr><th>File</th><th style="text-align:right;">Size</th></tr>
    {files_rows}
  </table>
</div>

<h2>Upload a portfolio file</h2>
<div class="section-card">
{upload_form}
</div>
"""
    return _shell("settings", body, title="Settings")


def _about_tab() -> str:
    body = """<h2>About InvestorClaw</h2>
<div class="section-card">
  <p><strong>InvestorClaw v4.1.x</strong> — deterministic-first portfolio analyzer.</p>
  <p>Real money math, no LLM math. Holdings, performance (Sharpe + Sortino, max drawdown,
  beta, value-at-risk), bond duration, FRED yield curves, sector breakdowns, scenario
  rebalancing. The engine is pure Python; the narrator is an LLM with strict
  no-fabrication validation against an HMAC-signed envelope.</p>
</div>

<h2>License</h2>
<div class="section-card">
  <p>Substantive code (bridge, dashboard, Dockerfile, tests): <strong>Apache 2.0</strong>.</p>
  <p>Distribution-edge artifacts (SKILL.md, compose.yml, install.yaml, agent-skills/**):
  <strong>MIT-0</strong> (MIT No Attribution).</p>
</div>

<h2>Repos</h2>
<ul>
  <li><a href="https://github.com/argonautsystems/InvestorClaw">argonautsystems/InvestorClaw</a> — umbrella project (this repo)</li>
  <li><a href="https://github.com/mnemos-os/mnemos-ic-runtime">mnemos-os/mnemos-ic-runtime</a> — v4.x dockerized-skill runtime</li>
  <li><a href="https://github.com/argonautsystems/ic-engine">argonautsystems/ic-engine</a> — Python engine source</li>
</ul>

<h2>Glossary</h2>
<p class="muted">Concept definitions for portfolio metrics shown in the dashboard tabs.</p>
<div class="section-card">
  <dl style="margin:0;">
    <dt><strong>Sharpe ratio</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Excess return per unit of total volatility. Higher is better; 1.0 is solid, 2.0+ is excellent.</dd>
    <dt><strong>Sortino ratio</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Like Sharpe, but only penalizes downside volatility. More representative for asymmetric portfolios.</dd>
    <dt><strong>Maximum drawdown</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Largest peak-to-trough decline over the analyzed window. Smaller (closer to 0) is better.</dd>
    <dt><strong>Beta</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Sensitivity to a benchmark (typically S&amp;P 500). β=1.0 moves with the market, &gt;1 amplifies, &lt;1 dampens.</dd>
    <dt><strong>Value-at-Risk (VaR 95%)</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Estimated maximum loss over one period at 95% confidence. The 5% tail beyond this is your "bad day".</dd>
    <dt><strong>Yield-to-maturity (YTM)</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Total annualized return on a bond if held to maturity, factoring in coupons and price.</dd>
    <dt><strong>Duration</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Bond's sensitivity to interest-rate moves. Higher duration = more rate risk.</dd>
    <dt><strong>Sharpe-maximizing allocation</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Weights chosen to maximize risk-adjusted return; computed via PyPortfolioOpt against historical returns + covariance.</dd>
    <dt><strong>Minimum-volatility allocation</strong></dt>
    <dd class="muted" style="margin-bottom:8px;">Weights chosen to minimize portfolio variance — the safest mix of your symbols, not necessarily the highest-return.</dd>
  </dl>
</div>

<h2>First-time setup</h2>
<div class="section-card">
  <ol style="margin:0;padding-left:20px;color:#c9d1d9;">
    <li style="margin-bottom:6px;">Drop your broker statement (CSV / XLSX / PDF) into <code>/data/portfolios/</code> via the <a href="/dashboard/settings">Settings</a> upload form.</li>
    <li style="margin-bottom:6px;">Add at least one provider key on <a href="/dashboard/settings">Settings</a> — TOGETHER for narrative, FINNHUB for analyst, NEWSAPI/MARKETAUX for news.</li>
    <li style="margin-bottom:6px;">Click <strong>↻ Regenerate</strong> on the <a href="/">Overview</a> tab — the engine refreshes every section (~3-5 min for a 200-position portfolio).</li>
    <li>Browse the tabs: Holdings → Performance → Bonds → Analyst → News.</li>
  </ol>
</div>

<h2>Disclaimer</h2>
<div class="section-card" style="border-color:#d29922;color:#e3b341;">
  <p><strong>Educational analysis only — NOT investment advice.</strong></p>
  <p>InvestorClaw is not a fiduciary advisor and does not execute trades, move money,
  or authenticate to brokerage accounts. Always consult a qualified financial advisor
  before acting on any analysis output.</p>
</div>
"""
    return _shell("about", body, title="About")


# ----------------------------------------------------------------------------
# FastAPI wiring
# ----------------------------------------------------------------------------


async def _safe_call(fn):
    """Invoke a sync-or-async zero-arg callable; swallow exceptions silently
    so a background-fired task never crashes the event loop.
    """
    try:
        result = fn()
        import inspect as _inspect
        if _inspect.iscoroutine(result):
            await result
    except Exception:
        # Background task — log via structlog if available, else swallow.
        try:
            import structlog
            structlog.get_logger("dashboard").warning(
                "background_task_failed", task=getattr(fn, "__name__", str(fn))
            )
        except Exception:
            pass


def attach_to(
    app: FastAPI,
    get_init_state,
    get_keys_status,
    set_key,
    regenerate=None,
) -> None:
    """Mount all dashboard tab routes on the given FastAPI app.

    Parameters
    ----------
    get_init_state : callable -> dict
        Returns the engine init snapshot (state, ready, current_stage, elapsed_ms).
    get_keys_status : callable -> dict
        Returns ``{"configured": [...], "settable": [...]}``.
    set_key : callable(name, value) -> dict
        Persists a single key, returns ``{"configured": [...], "rejected": [...]}``.
    regenerate : optional async callable() -> dict
        Triggers a full refresh + analyzer sweep. Called from the Regenerate
        button on the Overview tab. Should return quickly (background-fired).
    """

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    async def overview(message: str = "") -> HTMLResponse:
        return HTMLResponse(_overview(get_init_state, message=message))

    @app.get("/dashboard/", include_in_schema=False)
    async def dashboard_root() -> RedirectResponse:
        return RedirectResponse(url="/", status_code=303)

    @app.get("/dashboard/holdings", response_class=HTMLResponse, include_in_schema=False)
    async def holdings() -> HTMLResponse:
        return HTMLResponse(_holdings_tab())

    @app.get("/dashboard/performance", response_class=HTMLResponse, include_in_schema=False)
    async def performance() -> HTMLResponse:
        return HTMLResponse(_performance_tab())

    @app.get("/dashboard/whatchanged", response_class=HTMLResponse, include_in_schema=False)
    async def whatchanged() -> HTMLResponse:
        return HTMLResponse(_whatchanged_tab())

    @app.get("/dashboard/scenarios", response_class=HTMLResponse, include_in_schema=False)
    async def scenarios() -> HTMLResponse:
        return HTMLResponse(_scenarios_tab())

    @app.get("/dashboard/bonds", response_class=HTMLResponse, include_in_schema=False)
    async def bonds() -> HTMLResponse:
        return HTMLResponse(_bonds_tab())

    @app.get("/dashboard/analyst", response_class=HTMLResponse, include_in_schema=False)
    async def analyst() -> HTMLResponse:
        return HTMLResponse(_analyst_tab())

    @app.get("/dashboard/news", response_class=HTMLResponse, include_in_schema=False)
    async def news() -> HTMLResponse:
        return HTMLResponse(_news_tab())

    @app.get("/dashboard/optimize", response_class=HTMLResponse, include_in_schema=False)
    async def optimize() -> HTMLResponse:
        return HTMLResponse(_optimize_tab())

    @app.get("/dashboard/cashflow", response_class=HTMLResponse, include_in_schema=False)
    async def cashflow() -> HTMLResponse:
        return HTMLResponse(_cashflow_tab())

    @app.get("/dashboard/peer", response_class=HTMLResponse, include_in_schema=False)
    async def peer() -> HTMLResponse:
        return HTMLResponse(_peer_tab())

    @app.get("/dashboard/markets", response_class=HTMLResponse, include_in_schema=False)
    async def markets() -> HTMLResponse:
        return HTMLResponse(_markets_tab())

    @app.get("/dashboard/lookup", response_class=HTMLResponse, include_in_schema=False)
    async def lookup(symbol: str = "", message: str = "") -> HTMLResponse:
        return HTMLResponse(_lookup_tab(symbol=symbol, message=message))

    @app.get("/dashboard/synthesis", response_class=HTMLResponse, include_in_schema=False)
    async def synthesis() -> HTMLResponse:
        return HTMLResponse(_synthesis_tab())

    @app.get("/dashboard/reports", response_class=HTMLResponse, include_in_schema=False)
    async def reports() -> HTMLResponse:
        return HTMLResponse(_reports_tab())

    @app.get("/dashboard/settings", response_class=HTMLResponse, include_in_schema=False)
    async def settings(message: str = "") -> HTMLResponse:
        # get_keys_status may be sync or async (e.g. portfolio_keys_status is async)
        import inspect as _inspect
        result = get_keys_status()
        if _inspect.iscoroutine(result):
            result = await result
        return HTMLResponse(_settings_tab(lambda: result, message=message))

    @app.post("/dashboard/settings/keys", include_in_schema=False)
    async def settings_save_key(request: Request) -> RedirectResponse:
        form = await request.form()
        name = (form.get("key_name") or "").strip()
        value = (form.get("key_value") or "").strip()
        if not name or not value:
            return RedirectResponse(
                url="/dashboard/settings?message=Missing+name+or+value",
                status_code=303,
            )
        import inspect as _inspect
        result = set_key(name, value)
        if _inspect.iscoroutine(result):
            result = await result
        rejected = result.get("rejected") or []
        if rejected:
            msg = f"Key {name} rejected (not in allowlist)"
        else:
            msg = f"Saved {name}"
        from urllib.parse import quote
        return RedirectResponse(
            url=f"/dashboard/settings?message={quote(msg)}",
            status_code=303,
        )

    @app.get("/dashboard/about", response_class=HTMLResponse, include_in_schema=False)
    async def about() -> HTMLResponse:
        return HTMLResponse(_about_tab())

    @app.post("/dashboard/upload", include_in_schema=False)
    async def upload_portfolio(request: Request) -> RedirectResponse:
        """Multipart upload — write to /data/portfolios/, then trigger setup."""
        from urllib.parse import quote
        try:
            form = await request.form()
        except Exception as e:
            return RedirectResponse(
                url=f"/dashboard/settings?message={quote('Upload parse failed: ' + str(e))}",
                status_code=303,
            )
        upload = form.get("portfolio_file")
        if upload is None or not getattr(upload, "filename", ""):
            return RedirectResponse(
                url="/dashboard/settings?message=No+file+selected",
                status_code=303,
            )
        # Sanitize filename — strip path components, allow alphanumeric + . _ -
        raw_name = os.path.basename(upload.filename)
        safe_name = "".join(c for c in raw_name if c.isalnum() or c in "._-") or "portfolio.upload"
        if len(safe_name) > 200:
            safe_name = safe_name[-200:]

        pdir = pathlib.Path(os.environ.get("IC_PORTFOLIO_DIR", "/data/portfolios"))
        try:
            pdir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return RedirectResponse(
                url=f"/dashboard/settings?message={quote('Cannot create dir: ' + str(e))}",
                status_code=303,
            )

        dest = pdir / safe_name
        try:
            content = await upload.read()
            dest.write_bytes(content)
            try:
                dest.chmod(0o644)
            except OSError:
                pass
        except Exception as e:
            return RedirectResponse(
                url=f"/dashboard/settings?message={quote('Write failed: ' + str(e))}",
                status_code=303,
            )

        # Fire setup in the background — don't block the redirect.
        if regenerate is not None:
            try:
                import asyncio as _asyncio
                _asyncio.create_task(_safe_call(regenerate))
            except Exception:
                pass

        return RedirectResponse(
            url=f"/dashboard/settings?message={quote(f'Saved {safe_name} ({len(content)//1024} KB) — refresh queued')}",
            status_code=303,
        )

    @app.post("/dashboard/regenerate", include_in_schema=False)
    async def regenerate_now() -> RedirectResponse:
        """Fire the regenerate callable in the background; redirect immediately."""
        from urllib.parse import quote
        if regenerate is None:
            return RedirectResponse(
                url=f"/?message={quote('Regenerate not wired (no callable provided)')}",
                status_code=303,
            )
        try:
            import asyncio as _asyncio
            _asyncio.create_task(_safe_call(regenerate))
            msg = "Regeneration started — refresh + analyzer sweep takes ~3-5 min for a 200-position portfolio."
        except Exception as e:
            msg = f"Failed to start regenerate: {e}"
        return RedirectResponse(
            url=f"/?message={quote(msg)}",
            status_code=303,
        )
