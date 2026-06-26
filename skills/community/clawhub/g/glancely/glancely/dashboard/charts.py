"""Pure CSS/SVG chart renderers. Zero JavaScript dependencies.

Each function returns an HTML string to be embedded in a dashboard panel.
"""

from __future__ import annotations

import html as html_mod
import math
from datetime import date, timedelta
from typing import Any


def _esc(s: Any) -> str:
    return html_mod.escape(str(s))


def _no_data() -> str:
    return '<div class="chart-empty muted-row">No data</div>'


# ---------------------------------------------------------------------------
# Progress bar — horizontal CSS bar with label and value
# ---------------------------------------------------------------------------


def render_progress_bar(
    current: float, max_value: float, label: str = "", unit: str = "", color: str = "var(--ok)"
) -> str:
    pct = min(current / max_value * 100, 100) if max_value > 0 else 0.0
    val_text = (
        f"{current:.0f}{unit}/{max_value:.0f}{unit}" if unit else f"{current:.0f}/{max_value:.0f}"
    )
    return f"""<div class="chart-progress">
  <span class="progress-label">{_esc(label)}</span>
  <div class="progress-track">
    <div class="progress-fill" style="width:{pct:.0f}%;background:{color}"></div>
  </div>
  <span class="progress-value">{_esc(val_text)}</span>
</div>"""


# ---------------------------------------------------------------------------
# Status card — rich card with icon, title, value, and status indicator
# ---------------------------------------------------------------------------


def render_status_card(
    title: str, value: str, status: bool | None = None, status_label: str = ""
) -> str:
    if status is True:
        badge_class = "ok"
        badge_text = status_label or "done"
    elif status is False:
        badge_class = "bad"
        badge_text = status_label or "pending"
    else:
        badge_class = "muted"
        badge_text = status_label or "—"
    return f"""<div class="chart-status-card">
  <div class="status-title">{_esc(title)}</div>
  <div class="status-value">{_esc(value)}</div>
  <span class="badge {badge_class}">{_esc(badge_text)}</span>
</div>"""


# ---------------------------------------------------------------------------
# Bar chart — horizontal CSS bars
# ---------------------------------------------------------------------------


def render_bar_chart(
    data: list[dict],
    label_field: str = "label",
    value_field: str = "value",
    max_value: float | None = None,
    color: str = "var(--ok)",
) -> str:
    if not data:
        return _no_data()
    values = [d.get(value_field, 0) for d in data]
    max_v = max_value if max_value is not None else max(values)
    if max_v == 0:
        max_v = 1
    bars = []
    for d in data:
        v = d.get(value_field, 0)
        pct = (v / max_v * 100) if max_v > 0 else 0
        bars.append(f"""<div class="bar-item">
  <span class="bar-label">{_esc(d.get(label_field, ""))}</span>
  <div class="bar-track">
    <div class="bar-fill" style="width:{pct:.1f}%;background:{color}"></div>
  </div>
  <span class="bar-value">{_esc(v)}</span>
</div>""")
    return f'<div class="chart-bars">{"".join(bars)}</div>'


# ---------------------------------------------------------------------------
# Timeline — vertical CSS timeline with dots
# ---------------------------------------------------------------------------


def render_timeline(
    events: list[dict], time_field: str = "time", title_field: str = "title", desc_field: str = ""
) -> str:
    if not events:
        return _no_data()
    items = []
    for ev in events[:20]:  # limit to 20 items
        desc_html = ""
        if desc_field and ev.get(desc_field):
            desc_html = f'<div class="timeline-desc">{_esc(ev[desc_field])}</div>'
        items.append(f"""<div class="timeline-item">
  <div class="timeline-dot"></div>
  <div class="timeline-time">{_esc(ev.get(time_field, ""))}</div>
  <div class="timeline-content">
    <div class="timeline-title">{_esc(ev.get(title_field, ""))}</div>
    {desc_html}
  </div>
</div>""")
    return f'<div class="chart-timeline">{"".join(items)}</div>'


# ---------------------------------------------------------------------------
# Sparkline — inline SVG polyline
# ---------------------------------------------------------------------------


def render_sparkline(
    values: list[float],
    width: int = 200,
    height: int = 40,
    color: str = "var(--ok)",
    line_width: int = 2,
) -> str:
    if not values:
        return ""
    if len(values) == 1:
        # Single value — draw a dot
        return (
            f'<svg width="{width}" height="{height}" class="chart-sparkline">'
            f'<circle cx="50%" cy="50%" r="3" fill="{color}"/>'
            f"</svg>"
        )
    min_v = min(values)
    max_v = max(values)
    v_range = max_v - min_v or 1  # avoid div-by-zero
    pad_x = 2
    pad_y = 2
    draw_w = width - pad_x * 2
    draw_h = height - pad_y * 2
    points = []
    for i, v in enumerate(values):
        x = pad_x + i * draw_w / (len(values) - 1)
        y = pad_y + draw_h - (v - min_v) * draw_h / v_range
        points.append(f"{x:.1f},{y:.1f}")
    return (
        f'<svg width="{width}" height="{height}" class="chart-sparkline">'
        f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" '
        f'stroke-width="{line_width}" stroke-linecap="round" stroke-linejoin="round"/>'
        f"</svg>"
    )


# ---------------------------------------------------------------------------
# Pie / Donut — SVG circle with conic-gradient segments via stroke-dasharray
# ---------------------------------------------------------------------------

_COLORS = [
    "#4a7",
    "#5b9",
    "#6cb",
    "#7dc",
    "#8ed",
    "#e8a",
    "#d79",
    "#c68",
    "#9ad",
    "#8bc",
    "#7ab",
    "#69a",
    "#a7d",
    "#b8e",
    "#c9f",
]


def render_pie_donut(
    data: list[dict], label_field: str = "label", value_field: str = "value", donut: bool = False
) -> str:
    if not data:
        return _no_data()
    total = sum(d.get(value_field, 0) for d in data)
    if total <= 0:
        return _no_data()

    # Limit to 15 slices to avoid visual clutter
    data = data[:15]

    size = 200
    center = size / 2
    r = 70
    inner_r = 35 if donut else 0
    stroke_width = r - inner_r
    # The effective circle drawn by the stroke is at radius (inner_r + stroke_width/2)
    eff_r = inner_r + stroke_width / 2
    circumference = 2 * math.pi * eff_r

    slices = []
    legend = []
    cumulative = 0.0

    for i, d in enumerate(data):
        pct = d.get(value_field, 0) / total
        if pct <= 0:
            continue
        seg_len = pct * circumference
        color = _COLORS[i % len(_COLORS)]
        label = _esc(d.get(label_field, ""))
        # Rotational offset: start from top (-90deg)
        # Convert cumulative fraction to dashoffset
        offset = circumference - cumulative * circumference
        slices.append(
            f'<circle cx="{center}" cy="{center}" r="{eff_r:.1f}" '
            f'fill="none" stroke="{color}" stroke-width="{stroke_width}" '
            f'stroke-dasharray="{seg_len:.1f} {circumference - seg_len:.1f}" '
            f'stroke-dashoffset="-{offset:.1f}" '
            f'transform="rotate(-90 {center} {center})"/>'
        )
        # Use <title> for tooltip on hover
        slices.append(
            f'<circle cx="{center}" cy="{center}" r="{eff_r:.1f}" '
            f'fill="none" stroke="transparent" stroke-width="{stroke_width}" '
            f'stroke-dasharray="{seg_len:.1f} {circumference - seg_len:.1f}" '
            f'stroke-dashoffset="-{offset:.1f}" '
            f'transform="rotate(-90 {center} {center})" class="pie-slice-hit">'
            f"<title>{label}: {_esc(d.get(value_field, ''))} ({pct * 100:.0f}%)</title>"
            f"</circle>"
        )
        legend.append(
            f'<li><span class="legend-swatch" style="background:{color}"></span>'
            f"{label} ({pct * 100:.0f}%)</li>"
        )
        cumulative += pct

    # Center hole for donut
    center_hole = ""
    if donut and inner_r > 0:
        center_hole = (
            f'<circle cx="{center}" cy="{center}" r="{inner_r}" '
            f'fill="var(--card, #fff)"/>'
            f'<text x="{center}" y="{center}" text-anchor="middle" '
            f'dominant-baseline="central" class="donut-center-text">'
            f"{total:.0f}</text>"
        )

    cls = "chart-donut" if donut else "chart-pie"
    return (
        f'<div class="{cls}-wrapper">'
        f'<svg viewBox="0 0 {size} {size}" class="{cls}" '
        f'width="{size}" height="{size}">'
        f"{''.join(slices)}"
        f"{center_hole}"
        f"</svg>"
        f'<ul class="chart-legend">{"".join(legend)}</ul>'
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Heatmap — CSS grid with colored cells (GitHub contribution graph style)
# ---------------------------------------------------------------------------


def render_heatmap(
    data: list[dict],
    date_field: str = "date",
    value_field: str = "value",
    weeks: int = 13,
    color_scheme: str = "green",
) -> str:
    if not data:
        return _no_data()

    # Build a lookup from date string to value
    val_map: dict[str, float] = {}
    for d in data:
        ds = d.get(date_field)
        if ds:
            ds_str = str(ds)[:10]  # YYYY-MM-DD
            val_map[ds_str] = float(d.get(value_field, 0))

    # Build the grid: last N weeks, Mon–Sun columns
    today = date.today()
    # Start from the end of last week (Sunday) going back `weeks` weeks
    end_sunday = today + timedelta(days=(6 - today.weekday()))
    start_monday = end_sunday - timedelta(days=weeks * 7 - 1)

    all_values = list(val_map.values()) if val_map else [0]
    max_v = max(all_values) if all_values else 1
    min_v = min(all_values)

    # Color schemes
    def cell_style(v: float | None) -> str:
        if v is None:
            return 'style="background:var(--line)"'
        intensity = (v - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        if color_scheme == "green":
            r, g, b = 74, 170, 119
        elif color_scheme == "blue":
            r, g, b = 74, 140, 220
        elif color_scheme == "red":
            r, g, b = 204, 68, 68
        elif color_scheme == "purple":
            r, g, b = 140, 100, 200
        else:
            r, g, b = 74, 170, 119
        alpha = 0.15 + intensity * 0.85
        return f'style="background:rgba({r},{g},{b},{alpha:.2f})"'

    # Day-of-week headers
    dow = ["Mon", "", "Wed", "", "Fri", "", ""]
    header_cells = "".join(f'<div class="hm-header">{d}</div>' for d in dow)

    # Days of week as rows, weeks as columns
    hm_rows = []
    for dow_idx in range(7):
        cells = []
        for w in range(weeks):
            cell_date = start_monday + timedelta(days=w * 7 + dow_idx)
            if cell_date > today:
                cells.append('<div class="hm-cell hm-empty"></div>')
                continue
            ds = cell_date.isoformat()
            v = val_map.get(ds)
            cells.append(
                f'<div class="hm-cell" {cell_style(v)} title="{cell_date}: {v or 0}"></div>'
            )
        hm_rows.append(f'<div class="hm-row">{"".join(cells)}</div>')

    return (
        f'<div class="chart-heatmap">'
        f'<div class="hm-header-row">{header_cells}</div>'
        f"{''.join(hm_rows)}"
        f"</div>"
    )


# ---------------------------------------------------------------------------
# Calendar grid — monthly calendar with colored day cells
# ---------------------------------------------------------------------------

_MONTH_NAMES = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


def render_calendar_grid(
    data: list[dict],
    date_field: str = "date",
    value_field: str = "value",
    months_back: int = 3,
    color_scheme: str = "green",
) -> str:
    if not data:
        return _no_data()

    # Build lookup
    val_map: dict[str, float] = {}
    for d in data:
        ds = str(d.get(date_field, ""))[:10]
        if ds:
            val_map[ds] = float(d.get(value_field, 0))

    today = date.today()
    all_values = list(val_map.values()) if val_map else [0]
    max_v = max(all_values) if all_values else 1

    months_html = []
    for m_offset in range(months_back - 1, -1, -1):
        # Month to display
        month_first = date(today.year, today.month, 1)
        # Go back m_offset months
        for _ in range(m_offset):
            month_first = (month_first - timedelta(days=1)).replace(day=1)
        # Calculate last day of month
        if month_first.month == 12:
            month_last = date(month_first.year + 1, 1, 1) - timedelta(days=1)
        else:
            month_last = date(month_first.year, month_first.month + 1, 1) - timedelta(days=1)

        # Day-of-week headers
        dow_header = "".join(
            f'<div class="cal-dow">{d}</div>' for d in ["M", "T", "W", "T", "F", "S", "S"]
        )

        # Fill in days
        cells = []
        start_dow = month_first.weekday()  # 0=Mon
        for _ in range(start_dow):
            cells.append('<div class="cal-cell cal-empty"></div>')

        for day in range(1, month_last.day + 1):
            curr = date(month_first.year, month_first.month, day)
            ds = curr.isoformat()
            v = val_map.get(ds)
            if curr > today:
                cells.append('<div class="cal-cell cal-future"></div>')
            elif v is None:
                cells.append('<div class="cal-cell cal-no-data"></div>')
            else:
                intensity = min(v / max_v, 1.0) if max_v > 0 else 0.5
                if color_scheme == "green":
                    r, g, b = 74, 170, 119
                elif color_scheme == "blue":
                    r, g, b = 74, 140, 220
                elif color_scheme == "red":
                    r, g, b = 204, 68, 68
                elif color_scheme == "purple":
                    r, g, b = 140, 100, 200
                else:
                    r, g, b = 74, 170, 119
                alpha = 0.2 + intensity * 0.8
                cells.append(
                    f'<div class="cal-cell" '
                    f'style="background:rgba({r},{g},{b},{alpha:.2f})" '
                    f'title="{ds}: {v}">'
                    f'<span class="cal-day">{day}</span></div>'
                )

        months_html.append(
            f'<div class="cal-month">'
            f'<div class="cal-month-title">{_MONTH_NAMES[month_first.month - 1]} {month_first.year}</div>'
            f'<div class="cal-dow-row">{dow_header}</div>'
            f'<div class="cal-grid">{"".join(cells)}</div>'
            f"</div>"
        )

    return f'<div class="chart-calendar-grid">{"".join(months_html)}</div>'


# ---------------------------------------------------------------------------
# Chart dispatch — selects the right renderer based on chart.toml config
# ---------------------------------------------------------------------------


def _extract_values(payload: dict, config: dict) -> list[dict]:
    """Extract chart data from stats payload based on chart config."""
    chart_data = config.get("chart", {}).get("data", {})
    source = chart_data.get("source", "rows")

    if source == "summary":
        summary = payload.get("summary", {})
        value_field = chart_data.get("value_field", "")
        # If value_field names a key in summary that is itself a dict,
        # expand it into {label: value} pairs (e.g., by_category_today)
        if value_field and value_field in summary and isinstance(summary[value_field], dict):
            nested = summary[value_field]
            return [{"label": str(k), "value": v} for k, v in nested.items()]
        # Otherwise return a single-item list from summary values
        return [summary]

    # source == "rows"
    return payload.get("rows", [])


def render_chart(chart_type: str, payload: dict, config: dict) -> str:
    """Render a chart panel based on chart type, stats payload, and config.

    Args:
        chart_type: One of the SUPPORTED_CHART_TYPES
        payload: The stats.py JSON output dict
        config: The full parsed chart.toml dict (chart + overview sections)

    Returns:
        HTML string to embed in the panel.
    """
    chart_cfg = config.get("chart", {})
    chart_title = chart_cfg.get("title", "")
    data_cfg = chart_cfg.get("data", {})
    options = chart_cfg.get("options", {})

    if chart_type == "status_card":
        data_key = options.get("status_field", "")
        label = options.get("label", "")
        # Read from summary via dot notation
        summary = payload.get("summary", {})
        value = summary.get(data_key, "") if data_key else ""
        if isinstance(value, dict):
            value = ", ".join(f"{k}: {v}" for k, v in value.items())
        status = bool(value) if isinstance(value, (bool, int)) else None
        return render_status_card(
            title=chart_title or label,
            value=str(value),
            status=True if isinstance(value, bool) and value else status,
        )

    # Extract data from payload
    chart_data = _extract_values(payload, config)

    if not chart_data:
        return _no_data()

    if chart_type == "bar":
        return render_bar_chart(
            chart_data,
            label_field=data_cfg.get("label_field", "label"),
            value_field=data_cfg.get("value_field", "value"),
            max_value=options.get("max_value"),
            color=options.get("color", "var(--ok)"),
        )

    if chart_type in ("pie", "donut"):
        return render_pie_donut(
            chart_data,
            label_field=data_cfg.get("label_field", "label"),
            value_field=data_cfg.get("value_field", "value"),
            donut=(chart_type == "donut"),
        )

    if chart_type == "sparkline":
        values = [d.get(data_cfg.get("value_field", "value"), 0) for d in chart_data]
        return render_sparkline(
            values,
            width=options.get("width", 200),
            height=options.get("height", 40),
            color=options.get("color", "var(--ok)"),
        )

    if chart_type == "progress_bar":
        max_v = options.get("max_value", 100)
        current = (
            float(chart_data[0].get(data_cfg.get("value_field", "value"), 0)) if chart_data else 0
        )
        return render_progress_bar(
            current=current,
            max_value=max_v,
            label=options.get("label", ""),
            unit=options.get("unit", ""),
        )

    if chart_type == "heatmap":
        return render_heatmap(
            chart_data,
            date_field=data_cfg.get("date_field", "date"),
            value_field=data_cfg.get("value_field", "value"),
            color_scheme=options.get("color_scheme", "green"),
        )

    if chart_type == "calendar_grid":
        return render_calendar_grid(
            chart_data,
            date_field=data_cfg.get("date_field", "date"),
            value_field=data_cfg.get("value_field", "value"),
            color_scheme=options.get("color_scheme", "green"),
        )

    if chart_type == "timeline":
        return render_timeline(
            chart_data,
            time_field=data_cfg.get("time_field", "time"),
            title_field=data_cfg.get("title_field", "title"),
            desc_field=data_cfg.get("desc_field", ""),
        )

    # Fallback: basic card rendering (unchanged behavior)
    return ""
