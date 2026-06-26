#!/usr/bin/env python3
"""Build the read-only dashboard HTML.

Walk skills/, call each component's scripts/stats.py as a subprocess (each
component owns its imports), aggregate into one static HTML page.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glancely.core.registry import discover_components  # noqa: E402
from glancely.core.storage import apply_all_migrations  # noqa: E402
from glancely.dashboard.charts import render_chart  # noqa: E402
from glancely.dashboard.overview import render_overview_panel  # noqa: E402

SKILLS_ROOT = REPO_ROOT / "glancely" / "skills"
TEMPLATE_PATH = Path(__file__).resolve().parent / "template.html"


def _run_stats(component) -> dict:
    if not component.stats_script.is_file():
        return {"status": "error", "summary": {"error": "missing scripts/stats.py"}, "rows": []}
    try:
        out = subprocess.check_output(
            [sys.executable, str(component.stats_script)],
            cwd=REPO_ROOT,
            env={**os.environ, "PYTHONPATH": str(REPO_ROOT)},
            timeout=30,
            stderr=subprocess.PIPE,
        )
        return json.loads(out)
    except subprocess.TimeoutExpired:
        return {"status": "error", "summary": {"error": "stats.py timed out"}, "rows": []}
    except subprocess.CalledProcessError as exc:
        return {
            "status": "error",
            "summary": {"error": exc.stderr.decode("utf-8", "replace")[:500]},
            "rows": [],
        }
    except json.JSONDecodeError as exc:
        return {
            "status": "error",
            "summary": {"error": f"stats.py emitted non-JSON: {exc}"},
            "rows": [],
        }


def _status_badge(status: str, freshness_hours: float | None, threshold: float | None) -> str:
    if status == "error":
        return '<span class="badge bad">error</span>'
    if status == "empty":
        return '<span class="badge muted">empty</span>'
    if threshold is not None and freshness_hours is not None and freshness_hours > threshold:
        return f'<span class="badge bad">stale {freshness_hours:.1f}h</span>'
    if freshness_hours is not None:
        return f'<span class="badge ok">fresh {freshness_hours:.1f}h</span>'
    return '<span class="badge ok">ok</span>'


def _render_summary(summary: dict) -> str:
    if not summary:
        return ""
    items = []
    for k, v in summary.items():
        if isinstance(v, dict):
            inner = ", ".join(
                f"{html.escape(str(ik))}: {html.escape(str(iv))}" for ik, iv in v.items()
            )
            items.append(f"<div><strong>{html.escape(str(k))}</strong>: {inner}</div>")
        else:
            items.append(
                f"<div><strong>{html.escape(str(k))}</strong>: {html.escape(str(v))}</div>"
            )
    return "\n".join(items)


def _render_rows(rows: list[dict]) -> str:
    if not rows:
        return '<div class="muted-row">no recent entries</div>'
    keys: list[str] = []
    for r in rows:
        for k in r.keys():
            if k not in keys:
                keys.append(k)
    head = "".join(f"<th>{html.escape(k)}</th>" for k in keys)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r.get(k, '')))}</td>" for k in keys) + "</tr>"
        for r in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def _render_panel(component, payload: dict) -> str:
    badge = _status_badge(
        payload.get("status", "ok"),
        payload.get("freshness_hours"),
        component.freshness_hours,
    )

    chart_config = component.chart_config
    if chart_config and chart_config.get("chart", {}).get("type"):
        # Render as chart panel
        chart_type = chart_config["chart"]["type"]
        chart_title = chart_config["chart"].get("title", component.title)
        chart_html = render_chart(chart_type, payload, chart_config)

        # Still show summary data below chart if rows exist
        rows_html = _render_rows(payload.get("rows") or [])
        summary_html = _render_summary(payload.get("summary") or {})

        return f"""
<section class="panel" data-component="{html.escape(component.name)}">
  <header>
    <h2>{html.escape(chart_title)}</h2>
    {badge}
  </header>
  <div class="chart-container">{chart_html}</div>
  {f'<div class="summary">{summary_html}</div>' if summary_html else ""}
  {f"<details><summary>Recent</summary>{rows_html}</details>" if payload.get("rows") else ""}
</section>
""".strip()
    else:
        # Backward-compatible basic card (unchanged)
        summary_html = _render_summary(payload.get("summary") or {})
        rows_html = _render_rows(payload.get("rows") or [])
        return f"""
<section class="panel" data-component="{html.escape(component.name)}">
  <header>
    <h2>{html.escape(component.title)}</h2>
    {badge}
  </header>
  <div class="summary">{summary_html}</div>
  <details><summary>Recent</summary>{rows_html}</details>
</section>
""".strip()


DEFAULT_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>glancely — Dashboard</title>
  <style>
    :root {
      color-scheme: light dark;
      --bg: #fafafa; --fg: #222; --muted: #888;
      --card: #fff; --line: #eee;
      --ok: #4a7; --bad: #c44;
      --chart-line: #ddd;
    }
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #111; --fg: #eee; --muted: #888;
        --card: #1a1a1a; --line: #2a2a2a;
        --chart-line: #333;
      }
    }
    body {
      background: var(--bg); color: var(--fg);
      font: 14px/1.5 -apple-system, system-ui, sans-serif;
      margin: 0; padding: 24px;
    }
    h1 { margin: 0 0 4px; font-size: 20px; }
    .built-at { color: var(--muted); font-size: 12px; margin-bottom: 24px; }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 16px;
    }
    .panel {
      background: var(--card); border: 1px solid var(--line);
      border-radius: 8px; padding: 16px;
    }
    .panel header {
      display: flex; justify-content: space-between;
      align-items: baseline; margin-bottom: 8px;
    }
    .panel h2 { margin: 0; font-size: 16px; }
    .summary div { margin: 2px 0; }
    .badge {
      font-size: 11px; padding: 2px 8px; border-radius: 4px;
      white-space: nowrap;
    }
    .badge.ok { background: rgba(74,170,119,0.18); color: var(--ok); }
    .badge.bad { background: rgba(204,68,68,0.18); color: var(--bad); }
    .badge.muted { background: rgba(136,136,136,0.18); color: var(--muted); }
    details { margin-top: 8px; }
    details summary { cursor: pointer; color: var(--muted); }
    table {
      width: 100%; border-collapse: collapse;
      font-size: 12px; margin-top: 8px;
    }
    th, td {
      text-align: left; padding: 4px 6px;
      border-bottom: 1px solid var(--line);
    }
    th { color: var(--muted); font-weight: 500; }
    .muted-row { color: var(--muted); font-size: 12px; padding: 4px 0; }
    .chart-empty {
      color: var(--muted); font-size: 13px;
      text-align: center; padding: 24px 0;
    }

    /* ── Overview Panel ── */
    .overview-panel {
      grid-column: 1 / -1;
      border-color: var(--ok);
    }
    .overview-grid {
      display: flex; flex-wrap: wrap;
      gap: 12px; margin-top: 8px;
    }
    .ov-card {
      flex: 1 1 140px; min-width: 120px;
      padding: 12px; border-radius: 6px;
      background: rgba(128,128,128,0.06);
      text-align: center;
    }
    .ov-label {
      display: block; font-size: 11px;
      color: var(--muted); margin-bottom: 4px;
      text-transform: uppercase; letter-spacing: 0.5px;
    }
    .ov-value {
      display: block; font-size: 18px;
      font-weight: 600; margin-top: 4px;
    }
    .ov-badge-value { font-size: 14px; }

    /* ── Progress Bar ── */
    .chart-progress { margin: 8px 0; }
    .progress-label { font-size: 12px; color: var(--muted); display: block; margin-bottom: 4px; }
    .progress-track {
      height: 10px; background: var(--line);
      border-radius: 5px; overflow: hidden; margin: 4px 0;
    }
    .progress-fill {
      height: 100%; border-radius: 5px;
      transition: width 0.5s ease;
    }
    .progress-value {
      font-size: 12px; color: var(--muted);
      display: block; text-align: right;
    }

    /* ── Status Card ── */
    .chart-status-card { text-align: center; padding: 16px 0; }
    .status-title { font-size: 12px; color: var(--muted); margin-bottom: 4px; }
    .status-value { font-size: 16px; font-weight: 600; margin-bottom: 8px; }

    /* ── Bar Chart ── */
    .chart-bars { margin: 8px 0; }
    .bar-item {
      display: flex; align-items: center;
      gap: 8px; margin: 4px 0;
    }
    .bar-label {
      font-size: 12px; min-width: 60px;
      text-align: right; color: var(--muted);
    }
    .bar-track {
      flex: 1; height: 16px;
      background: var(--line); border-radius: 4px;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%; border-radius: 4px;
      min-width: 2px; transition: width 0.3s ease;
    }
    .bar-value {
      font-size: 12px; min-width: 36px;
      color: var(--fg); text-align: left;
    }

    /* ── Pie / Donut ── */
    .chart-pie-wrapper, .chart-donut-wrapper {
      text-align: center; margin: 8px 0;
    }
    .chart-pie, .chart-donut { display: inline-block; }
    .pie-slice-hit { cursor: pointer; }
    .donut-center-text {
      font-size: 18px; font-weight: 600;
      fill: var(--fg);
    }
    .chart-legend {
      list-style: none; padding: 0; margin: 8px 0 0;
      display: flex; flex-wrap: wrap;
      gap: 6px 14px; justify-content: center;
      font-size: 12px;
    }
    .legend-swatch {
      display: inline-block; width: 10px; height: 10px;
      border-radius: 2px; margin-right: 4px;
      vertical-align: middle;
    }

    /* ── Sparkline ── */
    .chart-sparkline { display: inline-block; vertical-align: middle; }

    /* ── Heatmap ── */
    .chart-heatmap {
      display: inline-block; margin: 8px 0; overflow-x: auto;
      max-width: 100%;
    }
    .hm-header-row {
      display: flex; gap: 2px; margin-bottom: 2px;
      padding-left: 24px;
    }
    .hm-header {
      width: 14px; font-size: 9px; color: var(--muted);
      text-align: center;
    }
    .hm-row { display: flex; gap: 2px; margin: 1px 0; }
    .hm-cell {
      width: 14px; height: 14px; border-radius: 2px;
      position: relative;
    }
    .hm-cell:hover { outline: 2px solid var(--fg); z-index: 1; }
    .hm-empty { background: transparent; }

    /* ── Calendar Grid ── */
    .chart-calendar-grid { margin: 8px 0; }
    .cal-month { margin-bottom: 12px; }
    .cal-month-title {
      font-size: 13px; font-weight: 600;
      margin-bottom: 4px;
    }
    .cal-dow-row, .cal-grid {
      display: grid; grid-template-columns: repeat(7, 1fr);
      gap: 2px; max-width: 280px;
    }
    .cal-dow {
      font-size: 10px; color: var(--muted);
      text-align: center; padding: 2px 0;
    }
    .cal-cell {
      aspect-ratio: 1; border-radius: 4px;
      display: flex; align-items: center; justify-content: center;
      font-size: 11px; cursor: default;
    }
    .cal-empty, .cal-future { background: transparent; }
    .cal-no-data { background: var(--line); opacity: 0.3; }
    .cal-future { color: var(--muted); opacity: 0.3; }
    .cal-day { font-size: 10px; }

    /* ── Timeline ── */
    .chart-timeline {
      position: relative; margin: 8px 0;
      padding-left: 24px;
    }
    .chart-timeline::before {
      content: ""; position: absolute; left: 8px; top: 4px; bottom: 4px;
      width: 2px; background: var(--line);
    }
    .timeline-item {
      position: relative; margin-bottom: 12px;
    }
    .timeline-dot {
      position: absolute; left: -20px; top: 5px;
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--ok); border: 2px solid var(--card);
    }
    .timeline-time {
      font-size: 11px; color: var(--muted);
      margin-bottom: 2px;
    }
    .timeline-title { font-size: 13px; font-weight: 500; }
    .timeline-desc { font-size: 12px; color: var(--muted); }

    /* ── Chart Container ── */
    .chart-container { margin-top: 4px; }
  </style>
</head>
<body>
  <h1>glancely</h1>
  <div class="built-at">Built {built_at}</div>
  <div class="grid">{panels}</div>
</body>
</html>
"""


def build(output_path: Path | None = None, run_migrations: bool = True) -> dict:
    from glancely.core.storage.db import GLANCE_HOME

    if output_path is None:
        output_path = GLANCE_HOME / "dashboard" / "index.html"

    if run_migrations:
        apply_all_migrations(SKILLS_ROOT)

    components = discover_components(panel_only=True)

    panels_html: list[str] = []
    statuses: dict[str, str] = {}
    overview_meta: list[dict] = []  # NEW: collect for overview panel

    for comp in components:
        payload = _run_stats(comp)
        statuses[comp.name] = payload.get("status", "unknown")
        panels_html.append(_render_panel(comp, payload))

        # Collect overview metadata if chart_config exists with overview section
        chart_config = comp.chart_config
        if chart_config and chart_config.get("overview", {}).get("enabled") is not False:
            overview_meta.append(
                {
                    "name": comp.name,
                    "title": comp.title,
                    "overview": chart_config["overview"],
                    "payload": payload,
                }
            )

    # Render overview panel
    overview_html = render_overview_panel(overview_meta)

    # Insert overview before the grid
    if overview_html:
        panels_html.insert(0, overview_html)

    template = (
        TEMPLATE_PATH.read_text(encoding="utf-8") if TEMPLATE_PATH.is_file() else DEFAULT_TEMPLATE
    )
    html_out = template.replace("{built_at}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    html_out = html_out.replace("{panels}", "\n".join(panels_html))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_out, encoding="utf-8")
    return {
        "output": str(output_path),
        "components": list(statuses.keys()),
        "statuses": statuses,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=None)
    p.add_argument("--no-migrate", action="store_true")
    args = p.parse_args(argv)
    result = build(Path(args.out) if args.out else None, run_migrations=not args.no_migrate)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
