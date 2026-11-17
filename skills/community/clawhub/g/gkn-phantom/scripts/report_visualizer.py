#!/usr/bin/env python3
"""Professional HTML/PDF Report Visualizer for GKN-Phantom v3.0.

Generates beautiful, self-contained HTML reports suitable for delivering to
clients. Produces a single-file report with embedded CSS/JS — no external CDN
dependencies, works fully offline.

Features:
  - Executive dashboard with risk gauge, finding counts, scan metadata
  - Finding cards: color-coded severity, collapsible evidence, remediation
  - Attack path graph: pure CSS/SVG nodes with hover tooltips
  - Asset inventory: sortable HTML table
  - WAF/Fingerprint summary: technology stack cards
  - Remediation priority matrix: 2x2 effort/impact plot
  - Interactive: severity filters, keyword search, collapse/expand, dark mode
  - Export: standalone HTML, print-friendly CSS, optional PDF via weasyprint

Usage:
  python report_visualizer.py --findings findings.json --assets assets.json \\
      --paths paths.json --log execution_log.json \\
      [--format html|pdf|both] [--output report]

Dependencies: Python 3.10+ stdlib; weasyprint is optional for PDF output.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html as _html
import json
import os
import sys
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import load_json, dump_json  # noqa: E402

# =============================================================================
# Constants
# =============================================================================

SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEVERITY_COLORS = {
    "critical": "#dc3545",
    "high":     "#fd7e14",
    "medium":   "#ffc107",
    "low":      "#17a2b8",
}
SEVERITY_BG = {
    "critical": "#fff5f5",
    "high":     "#fff8f0",
    "medium":   "#fffef5",
    "low":      "#f5fbfc",
}
SEVERITY_BORDER = {
    "critical": "#f5c6cb",
    "high":     "#ffe0c0",
    "medium":   "#fff3cd",
    "low":      "#bee5eb",
}

RISK_COLORS = [
    (0, 30,   "#28a745"),   # green
    (31, 60,  "#ffc107"),   # yellow
    (61, 80,  "#fd7e14"),   # orange
    (81, 100, "#dc3545"),   # red
]

CVSS_VECTORS = {
    "critical": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H",
    "high":     "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
    "medium":   "CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:L",
    "low":      "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:U/C:L/I:N/A:N",
}

FINDING_ICONS = {
    "sqli":             "&#9889;",
    "xss":              "&#10060;",
    "idor":             "&#128274;",
    "ssrf":             "&#127760;",
    "rce":              "&#128187;",
    "file_upload":      "&#128206;",
    "misconfig":        "&#9881;",
    "weak_credential":  "&#128273;",
    "component_exposure":"&#128269;",
    "logic_flaw":       "&#9888;",
    "lfi":              "&#128196;",
    "csrf":             "&#128220;",
    "open_redirect":    "&#10145;",
    "info_disclosure":  "&#128065;",
    "default":          "&#128030;",
}

# =============================================================================
# Data processing
# =============================================================================

def _risk_score(findings: list[dict]) -> int:
    points = {"critical": 25, "high": 15, "medium": 8, "low": 3}
    score = sum(points.get(f.get("severity", "low"), 3) for f in findings if f.get("status") == "validated")
    return min(100, score)


def _risk_color(score: int) -> str:
    for lo, hi, color in RISK_COLORS:
        if lo <= score <= hi:
            return color
    return "#dc3545"


def _risk_label(score: int) -> str:
    if score <= 30:
        return "Low Risk"
    elif score <= 60:
        return "Medium Risk"
    elif score <= 80:
        return "High Risk"
    return "Critical Risk"


def _count_by_severity(findings: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        if f.get("status") == "validated":
            sev = f.get("severity", "low")
            if sev in counts:
                counts[sev] += 1
    return counts


def _finding_type_label(ftype: str) -> str:
    mapping = {
        "sqli": "SQL Injection",
        "xss": "Cross-Site Scripting",
        "idor": "IDOR",
        "ssrf": "SSRF",
        "rce": "Remote Code Execution",
        "file_upload": "File Upload",
        "misconfig": "Misconfiguration",
        "weak_credential": "Weak Credential",
        "component_exposure": "Component Exposure",
        "logic_flaw": "Logic Flaw",
        "lfi": "Local File Inclusion",
        "csrf": "CSRF",
        "open_redirect": "Open Redirect",
        "info_disclosure": "Information Disclosure",
    }
    return mapping.get(ftype, ftype.replace("_", " ").title())


def _severity_sort(findings: list[dict]) -> list[dict]:
    return sorted(findings, key=lambda f: (SEVERITY_ORDER.get(f.get("severity", "low"), 99), f.get("type", "")))


def _esc(text: Any) -> str:
    """HTML-escape a value, returning '' for None."""
    if text is None:
        return ""
    return _html.escape(str(text))


def _truncate(text: str, length: int = 500) -> str:
    if not text:
        return ""
    if len(text) <= length:
        return _esc(text)
    return _esc(text[:length]) + "&hellip;"


def _format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "N/A"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        return f"{h}h {m}m"


def _extract_scan_metadata(log: list[dict]) -> dict:
    """Extract scan metadata from execution log."""
    start_ts = None
    end_ts = None
    mode = "standard"
    target = ""

    for entry in log or []:
        ts = entry.get("ts", "")
        state = entry.get("state", "")
        msg = entry.get("msg", "")
        if state == "INIT" and not start_ts:
            start_ts = ts
        if state in ("COMPLETE", "DONE", "ERROR") and not end_ts:
            end_ts = ts
        if "target" in entry and not target:
            target = entry.get("target", "")
        if "mode" in entry or "safe_mode" in str(msg).lower():
            mode = "safe_mode" if "blocked" in str(msg).lower() else "standard"

    duration = None
    if start_ts and end_ts:
        try:
            fmt = "%Y-%m-%dT%H:%M:%SZ"
            s = _dt.datetime.strptime(start_ts, fmt)
            e = _dt.datetime.strptime(end_ts, fmt)
            duration = (e - s).total_seconds()
        except (ValueError, TypeError):
            pass

    return {
        "target": target or "N/A",
        "date": (start_ts or "N/A")[:10],
        "duration": _format_duration(duration),
        "mode": mode,
    }


# =============================================================================
# HTML/CSS/JS Templates
# =============================================================================

CSS = r"""/* ============================================================
   GKN-Phantom v3.0 — Professional Report Stylesheet
   Self-contained, no external dependencies
   ============================================================ */

:root {
    --bg: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-card: #ffffff;
    --text: #212529;
    --text-secondary: #6c757d;
    --text-muted: #adb5bd;
    --border: #dee2e6;
    --border-light: #e9ecef;
    --shadow: 0 1px 3px rgba(0,0,0,0.08);
    --shadow-hover: 0 4px 12px rgba(0,0,0,0.12);
    --radius: 8px;
    --radius-sm: 4px;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "PingFang SC", "Microsoft YaHei", sans-serif;
    --font-mono: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, "Courier New", monospace;
    --accent: #0d6efd;
    --accent-hover: #0b5ed7;
}

[data-theme="dark"] {
    --bg: #1a1d23;
    --bg-secondary: #21252b;
    --bg-card: #282c34;
    --text: #e1e4e8;
    --text-secondary: #959da5;
    --text-muted: #586069;
    --border: #444d56;
    --border-light: #373e47;
    --shadow: 0 1px 3px rgba(0,0,0,0.3);
    --shadow-hover: 0 4px 12px rgba(0,0,0,0.5);
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: var(--font);
    font-size: 14px;
    line-height: 1.6;
    color: var(--text);
    background: var(--bg-secondary);
    -webkit-font-smoothing: antialiased;
}

/* ---- Header / Branding ---- */
.header {
    background: linear-gradient(135deg, #1a1d23 0%, #2c3e50 100%);
    color: #ffffff;
    padding: 28px 40px;
    border-bottom: 3px solid var(--accent);
    position: sticky;
    top: 0;
    z-index: 100;
}
.header-inner {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}
.header-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}
.header-logo {
    width: 42px;
    height: 42px;
    background: var(--accent);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 20px;
    color: #fff;
}
.header h1 {
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
}
.header-sub {
    font-size: 11px;
    color: #8896a4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 1px;
}
.header-actions {
    display: flex;
    gap: 10px;
    align-items: center;
}
.btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 16px;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    background: var(--bg-card);
    color: var(--text);
    transition: all 0.15s ease;
    text-decoration: none;
    white-space: nowrap;
}
.btn:hover { background: var(--bg-secondary); border-color: var(--text-muted); }
.btn-primary { background: var(--accent); color: #fff; border-color: var(--accent); }
.btn-primary:hover { background: var(--accent-hover); }
.btn-sm { padding: 5px 10px; font-size: 12px; }

/* ---- Container ---- */
.container { max-width: 1400px; margin: 0 auto; padding: 28px 32px; }

/* ---- Navigation ---- */
.nav-bar {
    background: var(--bg-card);
    border-bottom: 1px solid var(--border);
    padding: 0 32px;
    position: sticky;
    top: 98px;
    z-index: 99;
    display: flex;
    gap: 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
}
.nav-bar a {
    display: block;
    padding: 12px 18px;
    font-size: 13px;
    font-weight: 500;
    color: var(--text-secondary);
    text-decoration: none;
    border-bottom: 2px solid transparent;
    transition: all 0.15s;
    white-space: nowrap;
}
.nav-bar a:hover, .nav-bar a.active { color: var(--accent); border-bottom-color: var(--accent); }

/* ---- Toolbar ---- */
.toolbar {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    align-items: center;
    padding: 16px 0;
}
.filter-group {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.filter-btn {
    padding: 6px 14px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    cursor: pointer;
    background: var(--bg-card);
    color: var(--text-secondary);
    transition: all 0.15s;
}
.filter-btn:hover { border-color: var(--text-muted); }
.filter-btn.active-sev { color: #fff; border-color: transparent; }
.filter-btn.critical.active-sev { background: #dc3545; }
.filter-btn.high.active-sev { background: #fd7e14; }
.filter-btn.medium.active-sev { background: #ffc107; color: #212529; }
.filter-btn.low.active-sev { background: #17a2b8; }
.search-box {
    flex: 1;
    min-width: 220px;
    padding: 7px 14px;
    border: 1px solid var(--border);
    border-radius: 20px;
    font-size: 13px;
    background: var(--bg-card);
    color: var(--text);
    outline: none;
    transition: border-color 0.15s;
}
.search-box:focus { border-color: var(--accent); }
.toolbar-actions { display: flex; gap: 8px; margin-left: auto; }

/* ---- Section ---- */
.section { margin-bottom: 40px; }
.section-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 20px;
    padding-bottom: 10px;
    border-bottom: 2px solid var(--border-light);
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title .icon { font-size: 22px; }

/* ---- Dashboard ---- */
.dashboard {
    display: grid;
    grid-template-columns: 280px 1fr;
    gap: 24px;
    margin-bottom: 0;
}
@media (max-width: 900px) { .dashboard { grid-template-columns: 1fr; } }

/* Risk Gauge */
.risk-gauge-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
.risk-gauge { position: relative; width: 180px; height: 180px; }
.risk-gauge svg { transform: rotate(-90deg); }
.risk-gauge-bg { fill: none; stroke: var(--border-light); stroke-width: 14; }
.risk-gauge-fg { fill: none; stroke-width: 14; stroke-linecap: round; transition: stroke-dashoffset 0.8s ease; }
.risk-gauge-value {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
    font-size: 42px; font-weight: 800; line-height: 1;
}
.risk-gauge-label {
    position: absolute; top: 62%; left: 50%; transform: translateX(-50%);
    font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 1px;
}
.risk-gauge-card h3 { margin-top: 16px; font-size: 15px; font-weight: 600; }

/* Finding count cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
}
.metric-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 20px 22px;
    display: flex;
    align-items: center;
    gap: 16px;
    cursor: default;
    transition: box-shadow 0.15s;
}
.metric-card:hover { box-shadow: var(--shadow-hover); }
.metric-badge {
    width: 48px; height: 48px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; font-weight: 800; color: #fff; flex-shrink: 0;
}
.metric-info .metric-value { font-size: 28px; font-weight: 700; line-height: 1.2; }
.metric-info .metric-label { font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; }

/* Scan metadata */
.meta-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 20px 22px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin-top: 16px;
}
.meta-item { }
.meta-item .meta-label { font-size: 11px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.meta-item .meta-value { font-size: 14px; font-weight: 600; color: var(--text); word-break: break-all; }

/* ---- Finding Cards ---- */
.finding-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    margin-bottom: 16px;
    overflow: hidden;
    border-left: 4px solid #ccc;
    transition: box-shadow 0.15s, opacity 0.3s;
}
.finding-card:hover { box-shadow: var(--shadow-hover); }
.finding-card.hidden { display: none; }
.finding-card.sev-critical { border-left-color: #dc3545; }
.finding-card.sev-high     { border-left-color: #fd7e14; }
.finding-card.sev-medium   { border-left-color: #ffc107; }
.finding-card.sev-low      { border-left-color: #17a2b8; }

.finding-header {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 20px;
    cursor: pointer;
    user-select: none;
    transition: background 0.1s;
}
.finding-header:hover { background: var(--bg-secondary); }
.finding-severity-badge {
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #fff;
    white-space: nowrap;
}
.finding-type { font-weight: 600; font-size: 15px; flex: 1; }
.finding-target { font-size: 12px; color: var(--text-secondary); font-family: var(--font-mono); word-break: break-all; }
.finding-confidence {
    font-size: 12px; font-weight: 500; color: var(--text-secondary);
    background: var(--bg-secondary); padding: 4px 10px; border-radius: 12px;
    white-space: nowrap;
}
.finding-chevron {
    font-size: 12px; color: var(--text-muted);
    transition: transform 0.2s; width: 20px; text-align: center;
}
.finding-card.expanded .finding-chevron { transform: rotate(180deg); }

.finding-body { display: none; padding: 0 20px 20px; }
.finding-card.expanded .finding-body { display: block; }

.finding-section { margin-top: 16px; }
.finding-section h4 {
    font-size: 13px; font-weight: 600; color: var(--text);
    margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;
}

/* Evidence blocks */
.evidence-block {
    background: #1e1e1e;
    color: #d4d4d4;
    border-radius: var(--radius-sm);
    padding: 14px 16px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.5;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    max-height: 300px;
    overflow-y: auto;
    margin-bottom: 8px;
}
.evidence-label {
    font-size: 11px; font-weight: 600; color: #858585; text-transform: uppercase;
    letter-spacing: 0.5px; margin-bottom: 4px;
}
/* Syntax highlighting for HTTP */
.http-method { color: #569cd6; font-weight: 600; }
.http-path { color: #dcdcaa; }
.http-header { color: #9cdcfe; }
.http-header-val { color: #ce9178; }
.http-body { color: #d4d4d4; }

/* Remediation */
.remediation-text {
    background: #f0f9eb;
    border: 1px solid #c3e6cb;
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    font-size: 13px;
    color: #155724;
    line-height: 1.6;
}
[data-theme="dark"] .remediation-text { background: #1e3525; border-color: #2d5a3f; color: #8fd19e; }

/* Steps */
.steps-list { padding-left: 20px; }
.steps-list li { margin-bottom: 6px; font-size: 13px; color: var(--text); }

/* CVSS */
.cvss-block {
    background: var(--bg-secondary);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    font-size: 12px;
}
.cvss-vector { font-family: var(--font-mono); color: var(--accent); word-break: break-all; }
.cvss-metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 8px; margin-top: 8px; }
.cvss-metric { text-align: center; }
.cvss-metric .cvss-label { font-size: 10px; color: var(--text-secondary); text-transform: uppercase; }
.cvss-metric .cvss-val { font-size: 16px; font-weight: 700; color: var(--text); }

/* ---- Attack Path ---- */
.path-graph {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 28px;
    overflow-x: auto;
}
.path-svg { display: block; margin: 0 auto; }
.path-node { cursor: pointer; transition: transform 0.15s, filter 0.15s; }
.path-node:hover { transform: scale(1.15); filter: brightness(1.15); }
.path-edge { stroke: var(--text-muted); stroke-width: 2; fill: none; marker-end: url(#arrowhead); }
.path-edge.confirmed { stroke: var(--accent); stroke-width: 2.5; }
.path-tooltip {
    position: absolute; background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-sm); padding: 10px 14px; font-size: 12px;
    box-shadow: var(--shadow-hover); pointer-events: none; z-index: 200; max-width: 280px;
    display: none; line-height: 1.5;
}
.path-legend { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 16px; justify-content: center; }
.path-legend-item { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text-secondary); }
.path-legend-dot { width: 10px; height: 10px; border-radius: 50%; }

/* ---- Asset Table ---- */
.asset-table-wrap { overflow-x: auto; background: var(--bg-card); border-radius: var(--radius); box-shadow: var(--shadow); }
.asset-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.asset-table th {
    background: var(--bg-secondary); padding: 12px 16px; text-align: left;
    font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
    color: var(--text-secondary); border-bottom: 2px solid var(--border);
    cursor: pointer; user-select: none; white-space: nowrap;
}
.asset-table th:hover { color: var(--accent); }
.asset-table th .sort-arrow { margin-left: 4px; font-size: 10px; }
.asset-table td {
    padding: 10px 16px; border-bottom: 1px solid var(--border-light);
    color: var(--text); word-break: break-all;
}
.asset-table tr:hover td { background: var(--bg-secondary); }
.asset-table .mono { font-family: var(--font-mono); font-size: 12px; }
.ssl-A { color: #28a745; font-weight: 700; }
.ssl-B { color: #ffc107; font-weight: 700; }
.ssl-C { color: #fd7e14; font-weight: 700; }
.ssl-D,.ssl-F,.ssl-T { color: #dc3545; font-weight: 700; }

/* ---- WAF / Fingerprint ---- */
.tech-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 14px;
}
.tech-card {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 16px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: box-shadow 0.15s;
}
.tech-card:hover { box-shadow: var(--shadow-hover); }
.tech-icon {
    width: 40px; height: 40px; border-radius: 8px;
    background: var(--bg-secondary);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.tech-info { min-width: 0; }
.tech-name { font-weight: 600; font-size: 14px; color: var(--text); }
.tech-version { font-size: 11px; color: var(--text-secondary); }
.tech-category { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.waf-detected {
    background: #fff3cd; border: 1px solid #ffc107; border-radius: var(--radius);
    padding: 14px 18px; margin-bottom: 16px; font-weight: 600; font-size: 14px;
    display: flex; align-items: center; gap: 10px;
}
[data-theme="dark"] .waf-detected { background: #3d3200; border-color: #665500; color: #ffda6a; }
.waf-badge { background: #ffc107; color: #212529; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; }

/* ---- Remediation Matrix ---- */
.matrix-wrap {
    background: var(--bg-card);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    padding: 24px;
    overflow-x: auto;
}
.matrix-grid {
    display: grid;
    grid-template-columns: 80px 1fr 1fr;
    grid-template-rows: auto 1fr 1fr;
    gap: 1px;
    background: var(--border-light);
    border-radius: var(--radius-sm);
    overflow: hidden;
    min-width: 500px;
}
.matrix-cell {
    background: var(--bg-card);
    padding: 16px;
    min-height: 100px;
}
.matrix-label {
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px; color: var(--text-secondary);
    writing-mode: vertical-lr; text-orientation: mixed;
}
.matrix-axis {
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 12px; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.5px;
}
.matrix-quad { display: flex; flex-direction: column; gap: 4px; }
.matrix-quad h5 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }
.matrix-quad.quick-wins { border-left: 3px solid #28a745; }
.matrix-quad.quick-wins h5 { color: #28a745; }
.matrix-quad.major-projects { border-left: 3px solid var(--accent); }
.matrix-quad.major-projects h5 { color: var(--accent); }
.matrix-quad.low-hanging { border-left: 3px solid #ffc107; }
.matrix-quad.low-hanging h5 { color: #b8860b; }
.matrix-quad.defer { border-left: 3px solid var(--text-muted); }
.matrix-quad.defer h5 { color: var(--text-muted); }
.matrix-item {
    font-size: 11px; padding: 3px 8px; border-radius: 3px;
    background: var(--bg-secondary); cursor: default;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* ---- Footer ---- */
.footer {
    text-align: center; padding: 24px 32px; font-size: 11px;
    color: var(--text-muted); border-top: 1px solid var(--border-light); margin-top: 40px;
}

/* ---- Print ---- */
@media print {
    .header, .nav-bar, .toolbar, .header-actions, .footer { display: none !important; }
    body { background: #fff; font-size: 12px; color: #000; }
    .container { max-width: 100%; padding: 0; }
    .finding-body { display: block !important; }
    .finding-card { break-inside: avoid; box-shadow: none; border: 1px solid #ccc; margin-bottom: 8px; }
    .section { margin-bottom: 20px; }
    .dashboard { grid-template-columns: 1fr; }
    @page { margin: 1.5cm; }
}

/* ---- Misc ---- */
.empty-state { text-align: center; padding: 40px; color: var(--text-muted); font-size: 14px; }
.badge-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 4px; }
.scroll-top {
    position: fixed; bottom: 24px; right: 24px;
    width: 40px; height: 40px; border-radius: 50%;
    background: var(--accent); color: #fff; border: none; cursor: pointer;
    font-size: 18px; box-shadow: var(--shadow-hover); display: none;
    align-items: center; justify-content: center; z-index: 150;
}
"""

JS = r"""// GKN-Phantom Report Interactivity — pure vanilla JS

document.addEventListener('DOMContentLoaded', function() {
    // ---- Severity Filters ----
    var activeFilters = { critical: true, high: true, medium: true, low: true };
    var filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(function(btn) {
        btn.addEventListener('click', function() {
            var sev = this.dataset.severity;
            activeFilters[sev] = !activeFilters[sev];
            this.classList.toggle('active-sev', activeFilters[sev]);
            applyFilters();
        });
    });

    // ---- Search ----
    var searchBox = document.getElementById('findingSearch');
    if (searchBox) {
        searchBox.addEventListener('input', function() {
            applyFilters();
        });
    }

    function applyFilters() {
        var query = (searchBox ? searchBox.value.toLowerCase() : '');
        var cards = document.querySelectorAll('.finding-card');
        var anyVisible = false;
        cards.forEach(function(card) {
            var sev = card.dataset.severity;
            var text = card.textContent.toLowerCase();
            var matchSev = activeFilters[sev];
            var matchSearch = !query || text.indexOf(query) !== -1;
            if (matchSev && matchSearch) {
                card.classList.remove('hidden');
                anyVisible = true;
            } else {
                card.classList.add('hidden');
            }
        });
        var empty = document.getElementById('emptyState');
        if (empty) empty.style.display = anyVisible ? 'none' : 'block';
    }

    // ---- Collapse/Expand All ----
    var expandAllBtn = document.getElementById('expandAllBtn');
    var collapseAllBtn = document.getElementById('collapseAllBtn');
    if (expandAllBtn) {
        expandAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.finding-card').forEach(function(c) { c.classList.add('expanded'); });
        });
    }
    if (collapseAllBtn) {
        collapseAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.finding-card').forEach(function(c) { c.classList.remove('expanded'); });
        });
    }

    // ---- Individual Finding Card Toggle ----
    document.querySelectorAll('.finding-header').forEach(function(header) {
        header.addEventListener('click', function() {
            this.parentElement.classList.toggle('expanded');
        });
    });

    // ---- Smooth Scroll Nav ----
    document.querySelectorAll('.nav-bar a[href^="#"]').forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            document.querySelectorAll('.nav-bar a').forEach(function(a) { a.classList.remove('active'); });
            this.classList.add('active');
        });
    });

    // Highlight active nav on scroll
    window.addEventListener('scroll', function() {
        var sections = document.querySelectorAll('.section[id]');
        var navLinks = document.querySelectorAll('.nav-bar a');
        var scrollPos = window.scrollY + 120;
        sections.forEach(function(sec) {
            if (sec.offsetTop <= scrollPos && sec.offsetTop + sec.offsetHeight > scrollPos) {
                navLinks.forEach(function(a) {
                    a.classList.toggle('active', a.getAttribute('href') === '#' + sec.id);
                });
            }
        });
    });

    // ---- Dark / Light Mode Toggle ----
    var themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        var saved = localStorage.getItem('gkn-theme');
        if (saved === 'dark') { document.documentElement.setAttribute('data-theme', 'dark'); themeToggle.textContent = '\u2600 Light'; }
        themeToggle.addEventListener('click', function() {
            var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            if (isDark) {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('gkn-theme', 'light');
                themeToggle.textContent = '\u263E Dark';
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('gkn-theme', 'dark');
                themeToggle.textContent = '\u2600 Light';
            }
        });
    }

    // ---- Asset Table Sorting ----
    document.querySelectorAll('.asset-table th[data-sort]').forEach(function(th) {
        th.addEventListener('click', function() {
            var col = this.dataset.sort;
            var asc = this.dataset.dir !== 'asc';
            this.dataset.dir = asc ? 'asc' : 'desc';
            var tbody = this.closest('table').querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            rows.sort(function(a, b) {
                var va = (a.querySelector('td[data-col="' + col + '"]') || {}).textContent || '';
                var vb = (b.querySelector('td[data-col="' + col + '"]') || {}).textContent || '';
                var na = parseFloat(va), nb = parseFloat(vb);
                if (!isNaN(na) && !isNaN(nb)) { return asc ? na - nb : nb - na; }
                return asc ? va.localeCompare(vb) : vb.localeCompare(va);
            });
            // Update arrow indicators
            this.querySelector('.sort-arrow').textContent = asc ? '\u25B2' : '\u25BC';
            this.closest('table').querySelectorAll('th .sort-arrow').forEach(function(a, i) {
                if (a.parentElement !== th) a.textContent = '\u25B3';
            });
            rows.forEach(function(r) { tbody.appendChild(r); });
        });
    });

    // ---- Scroll to Top Button ----
    var scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
        window.addEventListener('scroll', function() {
            scrollBtn.style.display = window.scrollY > 400 ? 'flex' : 'none';
        });
        scrollBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ---- Path Graph Tooltips ----
    var tooltip = document.getElementById('pathTooltip');
    document.querySelectorAll('.path-node').forEach(function(node) {
        node.addEventListener('mouseenter', function(e) {
            var detail = this.dataset.detail || '';
            tooltip.innerHTML = detail;
            tooltip.style.display = 'block';
        });
        node.addEventListener('mousemove', function(e) {
            tooltip.style.left = (e.pageX + 14) + 'px';
            tooltip.style.top = (e.pageY - 10) + 'px';
        });
        node.addEventListener('mouseleave', function() {
            tooltip.style.display = 'none';
        });
    });
});
"""


# =============================================================================
# HTML template
# =============================================================================

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GKN-Phantom v3.0 — Penetration Test Report — {report_target}</title>
<style>
{css}
</style>
</head>
<body>

<!-- Header -->
<header class="header">
  <div class="header-inner">
    <div class="header-brand">
      <div class="header-logo">GKN</div>
      <div>
        <h1>GKN-Phantom v3.0</h1>
        <div class="header-sub">Penetration Test Report</div>
      </div>
    </div>
    <div class="header-actions">
      <button class="btn btn-sm" id="themeToggle" title="Toggle dark/light mode">&#x263E; Dark</button>
      <button class="btn btn-sm" onclick="window.print()" title="Print report">&#x2399; Print</button>
      <button class="btn btn-sm" id="exportHtmlBtn" title="Download standalone HTML">&#x2B07; HTML</button>
    </div>
  </div>
</header>

<!-- Navigation -->
<nav class="nav-bar">
  <a href="#dashboard" class="active">Dashboard</a>
  <a href="#findings">Findings</a>
  <a href="#attack-paths">Attack Paths</a>
  <a href="#assets">Asset Inventory</a>
  <a href="#fingerprint">WAF / Fingerprint</a>
  <a href="#matrix">Remediation Matrix</a>
</nav>

<div class="container">

<!-- ================================================================
     SECTION: Dashboard
     ================================================================ -->
<section class="section" id="dashboard">
  <h2 class="section-title"><span class="icon">&#x1F4CA;</span> Executive Dashboard</h2>

  <div class="dashboard">
    <!-- Risk Gauge -->
    <div class="risk-gauge-card">
      <div class="risk-gauge">
        <svg viewBox="0 0 160 160" width="180" height="180">
          <circle class="risk-gauge-bg" cx="80" cy="80" r="70"/>
          <circle class="risk-gauge-fg" cx="80" cy="80" r="70"
            stroke="{risk_color}"
            stroke-dasharray="439.82"
            stroke-dashoffset="{risk_dashoffset}"
            id="riskGaugeArc"/>
        </svg>
        <div class="risk-gauge-value" style="color:{risk_color}">{risk_score}</div>
        <div class="risk-gauge-label">Risk Score</div>
      </div>
      <h3 style="color:{risk_color}">{risk_label}</h3>
    </div>

    <!-- Metrics -->
    <div>
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-badge" style="background:#dc3545">{count_critical}</div>
          <div class="metric-info"><div class="metric-value">{count_critical}</div><div class="metric-label">Critical</div></div>
        </div>
        <div class="metric-card">
          <div class="metric-badge" style="background:#fd7e14">{count_high}</div>
          <div class="metric-info"><div class="metric-value">{count_high}</div><div class="metric-label">High</div></div>
        </div>
        <div class="metric-card">
          <div class="metric-badge" style="background:#ffc107;color:#212529">{count_medium}</div>
          <div class="metric-info"><div class="metric-value">{count_medium}</div><div class="metric-label">Medium</div></div>
        </div>
        <div class="metric-card">
          <div class="metric-badge" style="background:#17a2b8">{count_low}</div>
          <div class="metric-info"><div class="metric-value">{count_low}</div><div class="metric-label">Low</div></div>
        </div>
      </div>
      <div class="meta-card">
        <div class="meta-item"><div class="meta-label">Target</div><div class="meta-value">{meta_target}</div></div>
        <div class="meta-item"><div class="meta-label">Scan Date</div><div class="meta-value">{meta_date}</div></div>
        <div class="meta-item"><div class="meta-label">Duration</div><div class="meta-value">{meta_duration}</div></div>
        <div class="meta-item"><div class="meta-label">Mode</div><div class="meta-value">{meta_mode}</div></div>
      </div>
    </div>
  </div>
</section>

<!-- ================================================================
     SECTION: Findings
     ================================================================ -->
<section class="section" id="findings">
  <h2 class="section-title"><span class="icon">&#x1F50D;</span> Validated Findings ({total_findings})</h2>

  <div class="toolbar">
    <div class="filter-group">
      <button class="filter-btn critical active-sev" data-severity="critical">Critical ({count_critical})</button>
      <button class="filter-btn high active-sev" data-severity="high">High ({count_high})</button>
      <button class="filter-btn medium active-sev" data-severity="medium">Medium ({count_medium})</button>
      <button class="filter-btn low active-sev" data-severity="low">Low ({count_low})</button>
    </div>
    <input type="text" class="search-box" id="findingSearch" placeholder="Search findings...">
    <div class="toolbar-actions">
      <button class="btn btn-sm" id="expandAllBtn">&#x2B07; Expand All</button>
      <button class="btn btn-sm" id="collapseAllBtn">&#x2B06; Collapse All</button>
    </div>
  </div>

  <div id="emptyState" class="empty-state" style="display:none">No findings match your filter criteria.</div>

  {finding_cards}
</section>

<!-- ================================================================
     SECTION: Attack Paths
     ================================================================ -->
<section class="section" id="attack-paths">
  <h2 class="section-title"><span class="icon">&#x1F578;</span> Attack Path Visualization</h2>
  {attack_path_section}
</section>

<!-- ================================================================
     SECTION: Asset Inventory
     ================================================================ -->
<section class="section" id="assets">
  <h2 class="section-title"><span class="icon">&#x1F4E6;</span> Asset Inventory</h2>
  {asset_table}
</section>

<!-- ================================================================
     SECTION: WAF / Fingerprint
     ================================================================ -->
<section class="section" id="fingerprint">
  <h2 class="section-title"><span class="icon">&#x1F3F7;</span> Technology Stack &amp; WAF Fingerprint</h2>
  {waf_section}
  {tech_section}
</section>

<!-- ================================================================
     SECTION: Remediation Priority Matrix
     ================================================================ -->
<section class="section" id="matrix">
  <h2 class="section-title"><span class="icon">&#x1F4C8;</span> Remediation Priority Matrix</h2>
  {matrix_section}
</section>

</div><!-- /container -->

<!-- Path tooltip -->
<div class="path-tooltip" id="pathTooltip"></div>

<!-- Scroll to top -->
<button class="scroll-top" id="scrollTopBtn" title="Back to top">&#x2191;</button>

<!-- Footer -->
<div class="footer">
  Generated by GKN-Phantom v3.0 &mdash; {report_date} &mdash; Confidential
</div>

<script>
{js}
// Export HTML button
document.getElementById('exportHtmlBtn').addEventListener('click', function() {{
    var html = document.documentElement.outerHTML;
    var blob = new Blob(['<!DOCTYPE html>\\n' + html], {{type: 'text/html'}});
    var a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = '{report_filename}.html';
    a.click();
    URL.revokeObjectURL(a.href);
}});
</script>

</body>
</html>"""


# =============================================================================
# HTML builders
# =============================================================================

def _build_finding_card(f: dict) -> str:
    """Build a single collapsible finding card HTML."""
    sev = f.get("severity", "low")
    ftype = f.get("type", "unknown")
    target = f.get("target", "")
    confidence = f.get("confidence", 0.0)
    evidence = f.get("evidence", {}) or {}
    request = evidence.get("request", "")
    response = evidence.get("response", "")
    remediation = f.get("remediation", "Apply vendor/security best practices for this vulnerability class.")
    repro_steps = f.get("reproduction_steps", [])
    if not repro_steps and evidence:
        repro_steps = [
            "Identify the vulnerable endpoint: " + target,
            "Send the crafted request as shown below",
            "Observe the response confirming the vulnerability",
        ]

    # CVSS-style breakdown
    cvss = CVSS_VECTORS.get(sev, CVSS_VECTORS["low"])
    cvss_parts = {}
    for part in cvss.split("/"):
        if ":" in part:
            k, v = part.split(":", 1)
            cvss_parts[k] = v

    icon = FINDING_ICONS.get(ftype, FINDING_ICONS["default"])
    sev_color = SEVERITY_COLORS.get(sev, "#17a2b8")

    # Syntax-highlighted request snippet
    req_html = _syntax_highlight_http(_esc(request)) if request else "<em>No request captured</em>"
    resp_html = _syntax_highlight_http(_esc(response)) if response else "<em>No response captured</em>"

    steps_html = "".join(f"<li>{_esc(s)}</li>" for s in repro_steps) if repro_steps else "<li>No reproduction steps provided.</li>"

    card = f"""
<div class="finding-card sev-{_esc(sev)}" data-severity="{_esc(sev)}">
  <div class="finding-header">
    <span class="finding-severity-badge" style="background:{sev_color}">{_esc(sev)}</span>
    <span class="finding-type">{icon} {_esc(_finding_type_label(ftype))}</span>
    <span class="finding-target">{_esc(target)}</span>
    <span class="finding-confidence">Conf: {confidence:.0%}</span>
    <span class="finding-chevron">&#x25BC;</span>
  </div>
  <div class="finding-body">
    <div class="finding-section">
      <h4>Evidence &mdash; Request</h4>
      <div class="evidence-label">HTTP Request</div>
      <div class="evidence-block">{req_html}</div>
    </div>
    <div class="finding-section">
      <h4>Evidence &mdash; Response</h4>
      <div class="evidence-label">HTTP Response</div>
      <div class="evidence-block">{resp_html}</div>
    </div>
    <div class="finding-section">
      <h4>Remediation</h4>
      <div class="remediation-text">{_esc(remediation)}</div>
    </div>
    <div class="finding-section">
      <h4>Reproduction Steps</h4>
      <ol class="steps-list">{steps_html}</ol>
    </div>
    <div class="finding-section">
      <h4>CVSS Severity Breakdown</h4>
      <div class="cvss-block">
        <div class="cvss-vector">{_esc(cvss)}</div>
        <div class="cvss-metrics">
          <div class="cvss-metric"><div class="cvss-label">Attack Vector</div><div class="cvss-val">{_esc(cvss_parts.get('AV','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Complexity</div><div class="cvss-val">{_esc(cvss_parts.get('AC','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Privileges</div><div class="cvss-val">{_esc(cvss_parts.get('PR','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">User Interaction</div><div class="cvss-val">{_esc(cvss_parts.get('UI','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Scope</div><div class="cvss-val">{_esc(cvss_parts.get('S','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Confidentiality</div><div class="cvss-val">{_esc(cvss_parts.get('C','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Integrity</div><div class="cvss-val">{_esc(cvss_parts.get('I','N/A'))}</div></div>
          <div class="cvss-metric"><div class="cvss-label">Availability</div><div class="cvss-val">{_esc(cvss_parts.get('A','N/A'))}</div></div>
        </div>
      </div>
    </div>
  </div>
</div>"""
    return card


def _syntax_highlight_http(text: str) -> str:
    """Apply basic CSS-class-based syntax highlighting to HTTP text."""
    if not text:
        return text
    lines = text.split("\n")
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            out.append("")
            continue
        # HTTP method line
        if stripped.startswith(("GET ", "POST ", "PUT ", "DELETE ", "PATCH ", "HEAD ", "OPTIONS ", "HTTP/")):
            parts = stripped.split(" ")
            if len(parts) >= 1 and parts[0] in ("GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"):
                parts[0] = f'<span class="http-method">{_esc(parts[0])}</span>'
            if len(parts) >= 2:
                parts[1] = f'<span class="http-path">{_esc(parts[1])}</span>'
            out.append(" ".join(parts))
        # Header line
        elif ":" in stripped and not stripped.startswith("{"):
            key, _, val = stripped.partition(":")
            out.append(f'<span class="http-header">{_esc(key)}</span>:<span class="http-header-val">{_esc(val)}</span>')
        else:
            out.append(f'<span class="http-body">{_esc(stripped)}</span>')
    return "\n".join(out)


def _build_attack_path_svg(paths: list[dict]) -> str:
    """Build an SVG attack path graph with CSS-styled nodes and edges."""
    if not paths:
        return '<div class="empty-state">No attack paths discovered.</div>'

    nodes: list[dict] = []
    edges: list[dict] = []
    for path in paths:
        for n in (path.get("nodes") or []):
            if n not in nodes:
                nodes.append(n)
        for e in (path.get("edges") or []):
            if e not in edges:
                edges.append(e)

    if not nodes:
        return '<div class="empty-state">No attack path nodes to display.</div>'

    # Layout: arrange nodes in a layered left-to-right layout
    severity_rank = {"critical": 3, "high": 2, "medium": 1, "low": 0}
    node_rows: dict[str, list[dict]] = {}
    for n in nodes:
        sev = n.get("severity", "low")
        node_rows.setdefault(sev, []).append(n)

    ordered_sevs = ["critical", "high", "medium", "low"]
    width_per_node = 160
    height_per_row = 90
    margin_x = 100
    margin_y = 50

    positions: dict[str, tuple[float, float]] = {}
    row_idx = 0
    for sev in ordered_sevs:
        row_nodes = node_rows.get(sev, [])
        for col_idx, node in enumerate(row_nodes):
            x = margin_x + col_idx * width_per_node
            y = margin_y + row_idx * height_per_row
            node_id = node.get("id", node.get("ref", ""))
            positions[node_id] = (x, y)
        row_idx += 1

    total_width = max(margin_x + max(len(row_nodes) for row_nodes in node_rows.values()) * width_per_node + margin_x, 600)
    total_height = margin_y + row_idx * height_per_row + margin_y

    # Build SVG elements
    svg_nodes: list[str] = []
    svg_edges: list[str] = []
    sev_colors = {"critical": "#dc3545", "high": "#fd7e14", "medium": "#ffc107", "low": "#17a2b8"}

    # Defs
    svg_defs = """<defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#959da5"/>
    </marker>
    <marker id="arrowhead-confirmed" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#0d6efd"/>
    </marker>
    <filter id="nodeShadow"><feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.15"/></filter>
  </defs>"""

    # Edges
    for edge in edges:
        src = edge.get("source", edge.get("src", ""))
        dst = edge.get("target", edge.get("dst", edge.get("dest", "")))
        confirmed = edge.get("confirmed", False)
        if src in positions and dst in positions:
            x1, y1 = positions[src]
            x2, y2 = positions[dst]
            marker = "arrowhead-confirmed" if confirmed else "arrowhead"
            cls = "confirmed" if confirmed else ""
            svg_edges.append(f'<line x1="{x1}" y1="{y1 + 16}" x2="{x2}" y2="{y2 - 16}" class="path-edge {cls}" marker-end="url(#{marker})"/>')

    # Nodes
    for node in nodes:
        node_id = node.get("id", node.get("ref", ""))
        if node_id not in positions:
            continue
        x, y = positions[node_id]
        sev = node.get("severity", "low")
        color = sev_colors.get(sev, "#17a2b8")
        label = node.get("type", node.get("label", node_id))
        target = node.get("target", node.get("ref", ""))
        # Truncate label
        short_label = str(label)[:20]
        if len(str(label)) > 20:
            short_label += "…"

        detail_html = _esc(f"<b>{_finding_type_label(str(label))}</b><br>{target}<br>Severity: {sev}")

        svg_nodes.append(f"""<g class="path-node" data-detail="{detail_html}" transform="translate({x},{y})" filter="url(#nodeShadow)">
      <circle cx="0" cy="0" r="16" fill="{color}" stroke="#fff" stroke-width="2"/>
      <text x="0" y="30" text-anchor="middle" font-family="sans-serif" font-size="10" fill="var(--text)">{_esc(short_label)}</text>
    </g>""")

    svg = f"""<div class="path-graph">
    <svg class="path-svg" viewBox="0 0 {total_width} {total_height}" style="max-width:100%;height:auto">
      {svg_defs}
      {"".join(svg_edges)}
      {"".join(svg_nodes)}
    </svg>
    <div class="path-legend">
      <div class="path-legend-item"><span class="path-legend-dot" style="background:#0d6efd"></span> Confirmed Edge</div>
      <div class="path-legend-item"><span class="path-legend-dot" style="background:#959da5"></span> Candidate Edge</div>
    </div>
  </div>"""
    return svg


def _build_asset_table(assets: dict) -> str:
    """Build a sortable HTML table of discovered assets."""
    if not assets:
        return '<div class="empty-state">No asset data available.</div>'

    endpoints = assets.get("endpoints", [])
    subdomains = assets.get("subdomains", [])
    domains_list = assets.get("domains", [])
    # Build rows from available data
    rows: list[dict] = []

    # Combine subdomains and domains
    all_domains: list[str] = list(subdomains or [])
    if domains_list:
        all_domains.extend(domains_list)
    if not all_domains:
        all_domains = [assets.get("target", "N/A")]

    info = assets.get("info", assets)

    for domain in all_domains:
        domain_str = domain if isinstance(domain, str) else domain.get("domain", str(domain))
        ports = info.get("ports", info.get("open_ports", []))
        if isinstance(ports, str):
            ports = ports.split(",")
        ports_str = ", ".join(str(p) for p in (ports or [])) or "N/A"
        ip_str = info.get("ip", info.get("ips", ""))
        if isinstance(ip_str, list):
            ip_str = ", ".join(ip_str)
        ssl_grade = info.get("ssl_grade", info.get("ssl", {}).get("grade", "N/A")) if isinstance(info.get("ssl"), dict) else "N/A"

        rows.append({
            "domain": domain_str,
            "ip": ip_str or "N/A",
            "ports": ports_str,
            "technologies": _esc(", ".join(str(t.get("name", t)) for t in (info.get("technologies", []) or [])) or "N/A"),
            "ssl_grade": ssl_grade,
        })

    if not rows:
        rows.append({"domain": assets.get("target", "N/A"), "ip": "N/A", "ports": "N/A", "technologies": "N/A", "ssl_grade": "N/A"})

    tbody = ""
    for r in rows:
        ssl_class = f"ssl-{r['ssl_grade'][:1]}" if r['ssl_grade'] and r['ssl_grade'] != "N/A" else ""
        tbody += f"""<tr>
      <td data-col="domain">{_esc(r['domain'])}</td>
      <td data-col="ip" class="mono">{_esc(r['ip'])}</td>
      <td data-col="ports">{_esc(r['ports'])}</td>
      <td data-col="technologies">{r['technologies']}</td>
      <td data-col="ssl_grade" class="{_esc(ssl_class)}">{_esc(r['ssl_grade'])}</td>
    </tr>"""

    return f"""<div class="asset-table-wrap">
    <table class="asset-table">
      <thead>
        <tr>
          <th data-sort="domain">Domain <span class="sort-arrow">&#x25B3;</span></th>
          <th data-sort="ip">IP <span class="sort-arrow">&#x25B3;</span></th>
          <th data-sort="ports">Open Ports <span class="sort-arrow">&#x25B3;</span></th>
          <th data-sort="technologies">Technologies <span class="sort-arrow">&#x25B3;</span></th>
          <th data-sort="ssl_grade">SSL Grade <span class="sort-arrow">&#x25B3;</span></th>
        </tr>
      </thead>
      <tbody>{tbody}</tbody>
    </table>
  </div>"""


def _build_waf_section(assets: dict) -> str:
    """Build the WAF detection section."""
    waf_info = assets.get("waf", assets.get("WAF", None))
    if not waf_info:
        waf_name = assets.get("info", {}).get("waf", "")
        if not waf_name:
            return ""
        waf_info = {"name": waf_name, "detected": True}

    if isinstance(waf_info, str):
        waf_info = {"name": waf_info, "detected": True}

    if not waf_info.get("detected"):
        return """<div style="padding:12px 18px;background:var(--bg-card);border-radius:8px;box-shadow:var(--shadow);margin-bottom:16px;font-size:13px;color:var(--text-secondary)">
      &#9989; No WAF detected on target.
    </div>"""

    name = waf_info.get("name", "Unknown WAF")
    vendor = waf_info.get("vendor", "")
    return f"""<div class="waf-detected">
      &#9888; WAF Detected: <span class="waf-badge">{_esc(name)}</span>
      {_esc(vendor)}
    </div>"""


def _build_tech_section(assets: dict) -> str:
    """Build technology stack cards."""
    technologies = assets.get("technologies", assets.get("info", {}).get("technologies", []))
    if not technologies:
        return '<div class="empty-state">No technology fingerprint data available.</div>'

    cards: list[str] = []
    tech_icons: dict[str, str] = {
        "nginx": "&#127760;", "apache": "&#127760;", "iis": "&#127760;",
        "php": "&#128420;", "python": "&#128013;", "node.js": "&#128296;",
        "react": "&#9889;", "vue": "&#128065;", "angular": "&#127918;",
        "jquery": "&#128190;", "bootstrap": "&#128444;",
        "mysql": "&#128451;", "postgresql": "&#128451;", "mongodb": "&#128450;",
        "wordpress": "&#128214;", "drupal": "&#128214;", "joomla": "&#128214;",
        "cloudflare": "&#9729;", "aws": "&#9729;", "azure": "&#9729;",
        "docker": "&#128230;", "kubernetes": "&#9881;",
    }

    for t in technologies:
        if isinstance(t, str):
            name = t
            version = ""
            category = ""
        else:
            name = t.get("name", t.get("technology", str(t)))
            version = t.get("version", "")
            category = t.get("category", "")
        icon = tech_icons.get(name.lower(), "&#128736;")
        cards.append(f"""<div class="tech-card">
      <div class="tech-icon">{icon}</div>
      <div class="tech-info">
        <div class="tech-name">{_esc(name)}</div>
        <div class="tech-version">{_esc(version) if version else "&nbsp;"}</div>
        <div class="tech-category">{_esc(category) if category else "&nbsp;"}</div>
      </div>
    </div>""")

    return f'<div class="tech-grid">{"".join(cards)}</div>'


def _classify_remediation(sev: str) -> tuple[str, str]:
    """Classify a finding into the remediation matrix quadrants."""
    critical_high = {"critical": "major_projects", "high": "major_projects"}
    medium_low = {"medium": "low_hanging", "low": "defer"}
    # Critical/High findings are high impact, mapped by type
    impact = "high" if sev in ("critical", "high") else "low"
    # Simple ones (like misconfig, info_disclosure) are low effort
    return (impact, "varies")


def _build_matrix(findings: list[dict]) -> str:
    """Build the remediation priority matrix HTML."""
    validated = [f for f in findings if f.get("status") == "validated"]
    if not validated:
        return '<div class="empty-state">No findings to prioritize.</div>'

    # Classify each finding
    quadrants: dict[str, list[dict]] = {
        "quick_wins": [],      # High Impact, Low Effort
        "major_projects": [],  # High Impact, High Effort
        "low_hanging": [],     # Low Impact, Low Effort
        "defer": [],           # Low Impact, High Effort
    }

    # Heuristic: complex vulns (sqli, rce, ssrf) are high effort; simple ones low effort
    high_effort_types = {"sqli", "rce", "ssrf", "lfi", "file_upload", "idor", "logic_flaw", "csrf"}
    high_impact_sevs = {"critical", "high"}

    for f in validated:
        sev = f.get("severity", "low")
        ftype = f.get("type", "unknown")
        impact = "high" if sev in high_impact_sevs else "low"
        effort = "high" if ftype in high_effort_types else "low"

        if impact == "high" and effort == "low":
            quadrants["quick_wins"].append(f)
        elif impact == "high" and effort == "high":
            quadrants["major_projects"].append(f)
        elif impact == "low" and effort == "low":
            quadrants["low_hanging"].append(f)
        else:
            quadrants["defer"].append(f)

    def _quad_items(flist: list[dict]) -> str:
        if not flist:
            return '<span style="font-size:11px;color:var(--text-muted)">None</span>'
        items = ""
        for f in flist:
            sev = f.get("severity", "low")
            color = SEVERITY_COLORS.get(sev, "#17a2b8")
            label = _finding_type_label(f.get("type", "unknown"))
            items += f'<span class="matrix-item" style="border-left:3px solid {color}" title="{_esc(label)} @ {_esc(f.get("target",""))}">{_esc(label)}</span>'
        return items

    # Layout: top row = Low Effort / High Effort; left column = High Impact / Low Impact
    return f"""<div class="matrix-wrap">
    <div class="matrix-grid">
      <div class="matrix-cell matrix-axis"></div>
      <div class="matrix-cell matrix-axis">Low Effort</div>
      <div class="matrix-cell matrix-axis">High Effort</div>

      <div class="matrix-cell matrix-label">High Impact</div>
      <div class="matrix-cell matrix-quad quick-wins">
        <h5>Quick Wins ({len(quadrants['quick_wins'])})</h5>
        {_quad_items(quadrants['quick_wins'])}
      </div>
      <div class="matrix-cell matrix-quad major-projects">
        <h5>Major Projects ({len(quadrants['major_projects'])})</h5>
        {_quad_items(quadrants['major_projects'])}
      </div>

      <div class="matrix-cell matrix-label">Low Impact</div>
      <div class="matrix-cell matrix-quad low-hanging">
        <h5>Low-Hanging Fruit ({len(quadrants['low_hanging'])})</h5>
        {_quad_items(quadrants['low_hanging'])}
      </div>
      <div class="matrix-cell matrix-quad defer">
        <h5>Defer / Accept ({len(quadrants['defer'])})</h5>
        {_quad_items(quadrants['defer'])}
      </div>
    </div>
  </div>"""


# =============================================================================
# Report assembly
# =============================================================================

def build_html(findings: list[dict], assets: dict, paths: list[dict],
               log: list[dict]) -> str:
    """Assemble the complete HTML report and return it as a string."""
    validated = [f for f in findings if f.get("status") == "validated"]
    sorted_findings = _severity_sort(validated)
    counts = _count_by_severity(findings)
    risk = _risk_score(findings)
    metadata = _extract_scan_metadata(log)

    # Risk gauge calculation
    circumference = 439.82  # 2*PI*70
    risk_offset = circumference - (risk / 100.0) * circumference

    # Build finding cards
    card_htmls = [_build_finding_card(f) for f in sorted_findings]
    finding_cards = "\n".join(card_htmls) if card_htmls else '<div class="empty-state">No validated findings to report.</div>'

    # Build other sections
    attack_path_html = _build_attack_path_svg(paths)
    asset_table = _build_asset_table(assets)
    waf_html = _build_waf_section(assets)
    tech_html = _build_tech_section(assets)
    matrix_html = _build_matrix(findings)

    report_date = _dt.datetime.now().strftime("%Y-%m-%d %H:%M UTC")

    report_target = _esc(metadata.get("target", "N/A"))

    html = HTML_TEMPLATE.format(
        css=CSS,
        js=JS,
        report_target=report_target or "N/A",
        report_filename=f"GKN-Phantom_Report_{_esc(metadata.get('target','report')).replace('://','_').replace('/','_').replace(':','_')}",
        report_date=report_date,
        risk_score=risk,
        risk_color=_risk_color(risk),
        risk_label=_risk_label(risk),
        risk_dashoffset=f"{risk_offset:.2f}",
        count_critical=counts["critical"],
        count_high=counts["high"],
        count_medium=counts["medium"],
        count_low=counts["low"],
        total_findings=len(validated),
        meta_target=_esc(metadata["target"]),
        meta_date=_esc(metadata.get("date", "N/A")),
        meta_duration=_esc(metadata.get("duration", "N/A")),
        meta_mode=_esc(metadata.get("mode", "standard")),
        finding_cards=finding_cards,
        attack_path_section=attack_path_html,
        asset_table=asset_table,
        waf_section=waf_html,
        tech_section=tech_html,
        matrix_section=matrix_html,
    )

    return html


# =============================================================================
# PDF generation
# =============================================================================

def _generate_pdf_weasyprint(html_content: str, output_path: str) -> bool:
    """Generate PDF using weasyprint. Returns True on success."""
    try:
        from weasyprint import HTML  # type: ignore[import-untyped]
        HTML(string=html_content).write_pdf(output_path)
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Warning: weasyprint PDF generation failed: {e}", file=sys.stderr)
        return False


def _generate_pdf_print_css(html_content: str, output_path: str) -> str:
    """Save HTML with print-CSS instructions. Returns the path."""
    # The HTML already has @media print rules embedded.
    # Just save the HTML and instruct the user.
    html_path = output_path.rsplit(".", 1)[0] + "_printable.html"
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html_content)

    instructions = f"""
    PDF generation via weasyprint is not available (pip install weasyprint).
    A printable HTML file has been saved to: {html_path}

    To get a PDF:
      1. Open {html_path} in Chrome/Edge
      2. Press Ctrl+P (or Cmd+P)
      3. Select "Save as PDF" as the destination
      4. Set margins to "None" and enable "Background graphics"
      5. Click Save
    """
    return instructions


# =============================================================================
# CLI
# =============================================================================

def main() -> int:
    ap = argparse.ArgumentParser(
        description="GKN-Phantom v3.0 — Professional HTML/PDF Report Visualizer"
    )
    ap.add_argument("--findings", required=True,
                    help="Path to validated findings JSON")
    ap.add_argument("--assets", required=True,
                    help="Path to asset inventory JSON")
    ap.add_argument("--paths", required=True,
                    help="Path to attack paths JSON")
    ap.add_argument("--log", required=True,
                    help="Path to execution log JSON")
    ap.add_argument("--format", choices=["html", "pdf", "both"], default="html",
                    help="Output format (default: html)")
    ap.add_argument("--output", default="report",
                    help="Output file base name without extension (default: report)")
    args = ap.parse_args()

    # Load data
    findings = load_json(args.findings)
    assets = load_json(args.assets)
    paths = load_json(args.paths)
    log = load_json(args.log)

    # Ensure lists
    if isinstance(findings, dict):
        findings = findings.get("findings", [])
    if isinstance(paths, dict):
        paths = paths.get("paths", paths.get("attack_paths", []))
    if isinstance(assets, dict):
        pass  # assets stays as dict
    else:
        assets = {}

    # Build HTML
    html_content = build_html(findings, assets, paths, log)

    fmt = args.format
    output_base = args.output

    results: list[str] = []

    if fmt in ("html", "both"):
        html_path = output_base + ".html"
        with open(html_path, "w", encoding="utf-8") as fh:
            fh.write(html_content)
        results.append(f"HTML report saved to: {os.path.abspath(html_path)}")

    if fmt in ("pdf", "both"):
        pdf_path = output_base + ".pdf"
        if _generate_pdf_weasyprint(html_content, pdf_path):
            results.append(f"PDF report saved to: {os.path.abspath(pdf_path)}")
        else:
            msg = _generate_pdf_print_css(html_content, pdf_path)
            results.append(msg)

    for r in results:
        print(r)

    return 0


if __name__ == "__main__":
    sys.exit(main())
