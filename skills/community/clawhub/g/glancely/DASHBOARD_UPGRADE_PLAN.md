# Dashboard Upgrade — Rich Visualization Dashboard

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade Glance's dashboard from basic text-card layout to a rich, component-driven visualization dashboard using pure CSS/SVG charts, with each component defining its own chart template.

**Architecture:** Each component declares a `chart.toml` file specifying its chart type, data field mapping, and overview-card contribution. The dashboard builder discovers these configs, runs each stats script, then renders chart panels dynamically. Components without a `chart.toml` fall back to the current basic card layout (full backward compatibility). An overview panel composites key signals from all trackers into a single summary card above the grid.

**Tech Stack:** Python 3.9+, TOML configs, inline CSS + SVG rendering (zero external JS dependencies), subprocess-isolated stats scripts (unchanged).

---

## File Structure Map

```
glancely/
├── dashboard/
│   ├── build.py              # MODIFIED — uses chart configs, renders overview
│   ├── charts.py             # NEW — all CSS/SVG chart rendering functions
│   └── load_chart_config.py  # NEW — read + validate chart.toml per component
├── core/registry/
│   └── discover.py           # MODIFIED — Component gains chart_config property
├── examples/
│   ├── mood/
│   │   ├── chart.toml        # NEW — heatmap config + overview sparkline
│   │   └── scripts/stats.py  # MODIFIED — add chart data fields
│   ├── reminder/
│   │   ├── chart.toml        # NEW — list-with-badges config + overview count
│   │   └── scripts/stats.py  # MODIFIED — add chart data fields
│   ├── mit/
│   │   ├── chart.toml        # NEW — status-card config + overview status
│   │   └── scripts/stats.py  # MODIFIED — add chart data fields
│   └── diary_logger/
│       ├── chart.toml        # NEW — donut (category) + bar (weekly) + overview
│       └── scripts/stats.py  # MODIFIED — add chart data fields
└── skills/scaffold_component/
    ├── templates/component/
    │   └── chart.toml.tmpl   # NEW — scaffold template
    └── scripts/scaffold.py   # MODIFIED — render chart.toml.tmpl
tests/
├── test_dashboard_charts.py  # NEW — chart renderer unit tests
└── test_dashboard_build.py   # NEW — dashboard build integration tests
```

---

### Task 1: Define `chart.toml` Schema

**Files:**
- Create: _(no file — schema is the spec; implementation validates in Task 2)_

- [ ] **Step 1: Design the `chart.toml` schema**

The schema must support all 9 chart types and the overview panel integration.

```toml
# chart.toml — per-component chart configuration
# If this file is absent, the component renders as a basic card (unchanged behavior).

[chart]
type = "heatmap"          # REQUIRED. One of: bar, pie, donut, heatmap, sparkline,
                          #   status_card, progress_bar, calendar_grid, timeline
title = "Mood Heatmap"    # Optional override for chart title (default: component title)

[chart.data]
source = "rows"           # "rows" | "summary" — where to pull data from in the stats payload
# For all chart types except status_card:
label_field = "created_at"    # Field in each row/summary entry for the label/category
value_field = "mood_score"    # Field for the numeric value
# Optional: date_field for heatmap/calendar_grid (datetime string in rows)
date_field = "created_at"
# For pie/donut with summary dict source:
#   source = "summary"
#   label_field = "by_category_today"  # reads payload["summary"]["by_category_today"]
#                                      # as {label: value} dict

[chart.options]
# Type-specific options:
# bar:         max_value = 100 (optional cap)
# pie/donut:   inner_radius = 60 (0=pie, >0=donut size in px)
# heatmap:     color_scheme = "green" | "blue" | "red" | "purple"
#              cell_radius = 4
# sparkline:   width = 200, height = 40, color = "var(--ok)"
# status_card: status_field = "today_completed" (field to read for ✓/✗ indicator)
#              label = "Today's MIT"
# progress_bar: max_value = 10 (required), unit = ""
# timeline:    time_field = "start", title_field = "title"

[overview]
enabled = true                  # Whether this component contributes to the overview panel
card_type = "stat"              # "stat" | "sparkline" | "badge" | "progress"
label = "Pending"               # Label shown in overview card
data_key = "summary.active"     # Dot-notation path into stats payload
suffix = ""                     # Optional suffix (e.g. "tasks", "/10")
color = "green"                 # Optional accent color
# For sparkline overview cards:
#   data_key = "rows" — sparkline is drawn from the last N rows of value_field
#   value_field = "mood_score"
#   height = 30, width = 120
```

- [ ] **Step 2: Write the schema validation as a docstring in `load_chart_config.py` (part of Task 2)**

The file is written in Task 2. This step confirms the schema design above is complete.

---

### Task 2: Create Chart Config Loader (`load_chart_config.py`)

**Files:**
- Create: `glancely/dashboard/load_chart_config.py`
- Create: `tests/test_dashboard_charts.py` (partial — config loading tests)

- [ ] **Step 1: Write failing tests for chart config loading**

```python
# tests/test_dashboard_charts.py
import pytest
from pathlib import Path

def test_load_chart_config_returns_none_for_missing_file(tmp_path):
    from glancely.dashboard.load_chart_config import load_chart_config
    comp_dir = tmp_path / "no_config"
    comp_dir.mkdir()
    result = load_chart_config(comp_dir)
    assert result is None

def test_load_chart_config_parses_valid_heatmap(tmp_path):
    from glancely.dashboard.load_chart_config import load_chart_config
    comp_dir = tmp_path / "valid_heatmap"
    comp_dir.mkdir()
    (comp_dir / "chart.toml").write_text("""\
[chart]
type = "heatmap"
title = "Mood Heatmap"

[chart.data]
source = "rows"
date_field = "created_at"
value_field = "mood_score"
label_field = "mood_label"

[chart.options]
color_scheme = "green"

[overview]
enabled = true
card_type = "sparkline"
label = "Mood"
data_key = "summary.avg_score_7d"
suffix = "/10"
""")
    result = load_chart_config(comp_dir)
    assert result is not None
    assert result["chart"]["type"] == "heatmap"
    assert result["chart"]["data"]["date_field"] == "created_at"
    assert result["overview"]["enabled"] is True
    assert result["overview"]["card_type"] == "sparkline"

def test_load_chart_config_rejects_invalid_type(tmp_path):
    from glancely.dashboard.load_chart_config import load_chart_config
    comp_dir = tmp_path / "invalid"
    comp_dir.mkdir()
    (comp_dir / "chart.toml").write_text("""\
[chart]
type = "garbage"
[chart.data]
source = "rows"
""")
    with pytest.raises(ValueError, match="Unsupported chart type"):
        load_chart_config(comp_dir)

def test_load_chart_config_missing_data_section(tmp_path):
    from glancely.dashboard.load_chart_config import load_chart_config
    comp_dir = tmp_path / "no_data"
    comp_dir.mkdir()
    (comp_dir / "chart.toml").write_text("""\
[chart]
type = "bar"
""")
    with pytest.raises(ValueError, match="chart.data"):
        load_chart_config(comp_dir)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py -v`
Expected: 4 test failures (ImportError or function not defined)

- [ ] **Step 3: Implement `load_chart_config.py`**

```python
# glancely/dashboard/load_chart_config.py
"""Load and validate chart.toml per component directory."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

SUPPORTED_CHART_TYPES = frozenset({
    "bar", "pie", "donut", "heatmap", "sparkline",
    "status_card", "progress_bar", "calendar_grid", "timeline",
})

SUPPORTED_OVERVIEW_TYPES = frozenset({"stat", "sparkline", "badge", "progress"})

REQUIRED_DATA_FIELDS: dict[str, set[str]] = {
    "bar": {"source"},
    "pie": {"source"},
    "donut": {"source"},
    "heatmap": {"source", "date_field", "value_field"},
    "sparkline": {"source", "value_field"},
    "status_card": set(),  # no data section required
    "progress_bar": {"source", "value_field"},
    "calendar_grid": {"source", "date_field", "value_field"},
    "timeline": {"source", "time_field", "title_field"},
}


def load_chart_config(component_dir: Path) -> dict[str, Any] | None:
    """Read and validate chart.toml from a component directory.

    Returns None if chart.toml does not exist (component renders as basic card).
    Returns parsed + validated dict on success.
    Raises ValueError for invalid configuration.
    """
    cfg_path = component_dir / "chart.toml"
    if not cfg_path.is_file():
        return None

    with cfg_path.open("rb") as fh:
        cfg = tomllib.load(fh)

    chart = cfg.get("chart")
    if not chart:
        raise ValueError("chart.toml requires a [chart] section")

    chart_type = chart.get("type")
    if not chart_type:
        raise ValueError("chart.toml [chart] section requires 'type'")
    if chart_type not in SUPPORTED_CHART_TYPES:
        raise ValueError(
            f"Unsupported chart type {chart_type!r}. "
            f"Use one of: {', '.join(sorted(SUPPORTED_CHART_TYPES))}"
        )

    if chart_type != "status_card":
        data = cfg.get("chart", {}).get("data")
        if not data:
            raise ValueError(
                f"chart.toml [chart.data] section required for chart type {chart_type!r}"
            )
        required = REQUIRED_DATA_FIELDS.get(chart_type, set())
        missing = required - set(data.keys())
        if missing:
            raise ValueError(
                f"chart.toml [chart.data] missing required fields for {chart_type!r}: {', '.join(sorted(missing))}"
            )
        source = data.get("source")
        if source not in ("rows", "summary"):
            raise ValueError(
                f"chart.toml [chart.data].source must be 'rows' or 'summary', got {source!r}"
            )

    overview = cfg.get("overview", {})
    if overview.get("enabled") is not False:
        ov_type = overview.get("card_type", "stat")
        if ov_type not in SUPPORTED_OVERVIEW_TYPES:
            raise ValueError(
                f"Unsupported overview card_type {ov_type!r}. "
                f"Use one of: {', '.join(sorted(SUPPORTED_OVERVIEW_TYPES))}"
            )
        if ov_type in ("sparkline", "progress") and not overview.get("data_key"):
            raise ValueError(
                f"overview card_type {ov_type!r} requires 'data_key'"
            )
    else:
        overview = {"enabled": False}

    return {"chart": chart, "overview": overview}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "config"`
Expected: 4 tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/load_chart_config.py tests/test_dashboard_charts.py
git commit -m "feat(dashboard): add chart.toml config loader with validation"
```

---

### Task 3: Add `chart_config` Property to `Component` Dataclass

**Files:**
- Modify: `glancely/core/registry/discover.py` — add chart_config loading

- [ ] **Step 1: Read current `discover.py`**

_(Already read above — the Component dataclass is at lines 23–62.)_

- [ ] **Step 2: Add chart_config property to Component**

Insert after the `auth` property in `discover.py`:

```python
    # After line 62 in discover.py (end of Component class properties)
    @property
    def chart_config(self) -> dict | None:
        """Chart configuration from chart.toml, or None if no chart config."""
        from glancely.dashboard.load_chart_config import load_chart_config
        return load_chart_config(self.path)
```

This is a property (lazy-loaded per access) so the import of `load_chart_config` only happens when chart_config is accessed, keeping `discover.py` decoupled.

- [ ] **Step 3: Verify existing tests still pass**

Run: `python -m pytest glancely/core/registry/tests/ -v`
Expected: All existing tests PASS

- [ ] **Step 4: Commit**

```bash
git add glancely/core/registry/discover.py
git commit -m "feat(registry): add chart_config property to Component dataclass"
```

---

### Task 4: Create Chart Rendering Engine (`charts.py` — Part 1: Stateless Charts)

**Files:**
- Create: `glancely/dashboard/charts.py`
- Modify: `tests/test_dashboard_charts.py` (add rendering tests)

This task implements the stateless chart renderers: bar, progress_bar, status_card, timeline.

- [ ] **Step 1: Write failing tests for stateless chart renderers**

Add to `tests/test_dashboard_charts.py`:

```python
import html
import pytest

def test_render_progress_bar():
    from glancely.dashboard.charts import render_progress_bar
    html_out = render_progress_bar(current=7, max_value=10, label="Done")
    assert 'style="width:70%"' in html_out
    assert "Done" in html_out
    assert "7/10" in html_out

def test_render_progress_bar_zero_max():
    from glancely.dashboard.charts import render_progress_bar
    html_out = render_progress_bar(current=0, max_value=0, label="N/A")
    assert 'style="width:0%"' in html_out

def test_render_status_card_ok():
    from glancely.dashboard.charts import render_status_card
    html_out = render_status_card(
        title="Today's MIT",
        value="Design the API",
        status=True,
    )
    assert "Today's MIT" in html_out
    assert "Design the API" in html_out
    assert "ok" in html_out

def test_render_status_card_incomplete():
    from glancely.dashboard.charts import render_status_card
    html_out = render_status_card(
        title="Today's MIT",
        value="Not set",
        status=False,
    )
    assert "bad" in html_out or "muted" in html_out

def test_render_bar_chart():
    from glancely.dashboard.charts import render_bar_chart
    data = [{"label": "prod", "value": 240}, {"label": "admin", "value": 72}]
    html_out = render_bar_chart(data, label_field="label", value_field="value")
    assert "prod" in html_out
    assert "240" in html_out

def test_render_bar_chart_empty():
    from glancely.dashboard.charts import render_bar_chart
    html_out = render_bar_chart([], label_field="x", value_field="y")
    assert "No data" in html_out or "no data" in html_out

def test_render_timeline():
    from glancely.dashboard.charts import render_timeline
    events = [
        {"time": "14:30", "title": "Wrapper refactor"},
        {"time": "15:45", "title": "Code review"},
    ]
    html_out = render_timeline(events, time_field="time", title_field="title")
    assert "Wrapper refactor" in html_out
    assert "timeline" in html_out  # CSS class
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py::test_render_progress_bar -v` (and others)
Expected: ALL FAIL (ImportError or function not defined)

- [ ] **Step 3: Implement stateless chart renderers**

```python
# glancely/dashboard/charts.py
"""Pure CSS/SVG chart renderers. Zero JavaScript dependencies.

Each function returns an HTML string to be embedded in a dashboard panel.
"""

from __future__ import annotations

import html as html_mod
from typing import Any


def _esc(s: Any) -> str:
    return html_mod.escape(str(s))


def _no_data() -> str:
    return '<div class="chart-empty muted-row">No data</div>'


# ---------------------------------------------------------------------------
# Progress bar — horizontal CSS bar with label and value
# ---------------------------------------------------------------------------

def render_progress_bar(current: float, max_value: float, label: str = "",
                        unit: str = "", color: str = "var(--ok)") -> str:
    pct = min(current / max_value * 100, 100) if max_value > 0 else 0.0
    val_text = f"{current:.0f}{unit}/{max_value:.0f}{unit}" if unit else f"{current:.0f}/{max_value:.0f}"
    return f"""<div class="chart-progress">
  <span class="progress-label">{_esc(label)}</span>
  <div class="progress-track">
    <div class="progress-fill" style="width:{pct:.1f}%;background:{color}"></div>
  </div>
  <span class="progress-value">{_esc(val_text)}</span>
</div>"""


# ---------------------------------------------------------------------------
# Status card — rich card with icon, title, value, and status indicator
# ---------------------------------------------------------------------------

def render_status_card(title: str, value: str, status: bool | None = None,
                       status_label: str = "") -> str:
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

def render_bar_chart(data: list[dict], label_field: str = "label",
                     value_field: str = "value", max_value: float | None = None,
                     color: str = "var(--ok)") -> str:
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

def render_timeline(events: list[dict], time_field: str = "time",
                    title_field: str = "title",
                    desc_field: str = "") -> str:
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "render_progress_bar or render_status_card or render_bar_chart or render_timeline"`
Expected: All 7 stateless chart tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/charts.py tests/test_dashboard_charts.py
git commit -m "feat(charts): add stateless renderers (bar, progress, status, timeline)"
```

---

### Task 5: Chart Rendering Engine — Part 2: SVG Charts

**Files:**
- Modify: `glancely/dashboard/charts.py` (add sparkline, pie, donut)
- Modify: `tests/test_dashboard_charts.py` (add SVG chart tests)

- [ ] **Step 1: Write failing tests for SVG charts**

Add to `tests/test_dashboard_charts.py`:

```python
def test_render_sparkline():
    from glancely.dashboard.charts import render_sparkline
    html_out = render_sparkline([3, 7, 5, 9, 6, 8, 7], width=200, height=40)
    assert "<svg" in html_out
    assert "<polyline" in html_out
    assert 'points="' in html_out

def test_render_sparkline_single_value():
    from glancely.dashboard.charts import render_sparkline
    html_out = render_sparkline([5], width=200, height=40)
    assert "<svg" in html_out
    # Should still produce something valid

def test_render_sparkline_empty():
    from glancely.dashboard.charts import render_sparkline
    html_out = render_sparkline([], width=200, height=40)
    assert html_out == ""

def test_render_pie_chart():
    from glancely.dashboard.charts import render_pie_donut
    data = [{"label": "prod", "value": 240}, {"label": "admin", "value": 72}, {"label": "meetings", "value": 88}]
    html_out = render_pie_donut(data, label_field="label", value_field="value", donut=False)
    assert "<svg" in html_out
    assert "prod" in html_out
    assert 'class="chart-pie"' in html_out

def test_render_donut_chart():
    from glancely.dashboard.charts import render_pie_donut
    data = [{"label": "prod", "value": 240}, {"label": "admin", "value": 72}]
    html_out = render_pie_donut(data, label_field="label", value_field="value", donut=True)
    assert "<svg" in html_out
    assert 'class="chart-donut"' in html_out

def test_render_pie_donut_empty():
    from glancely.dashboard.charts import render_pie_donut
    html_out = render_pie_donut([], label_field="x", value_field="y")
    assert "No data" in html_out

def test_render_pie_donut_zero_total():
    from glancely.dashboard.charts import render_pie_donut
    data = [{"label": "a", "value": 0}, {"label": "b", "value": 0}]
    html_out = render_pie_donut(data, label_field="label", value_field="value")
    assert "No data" in html_out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "sparkline or pie or donut"`
Expected: ALL FAIL

- [ ] **Step 3: Implement SVG chart renderers**

Add to `glancely/dashboard/charts.py`:

```python
import math

# ---------------------------------------------------------------------------
# Sparkline — inline SVG polyline
# ---------------------------------------------------------------------------

def render_sparkline(values: list[float], width: int = 200, height: int = 40,
                     color: str = "var(--ok)", line_width: int = 2) -> str:
    if not values:
        return ""
    if len(values) == 1:
        # Single value — draw a dot
        return (
            f'<svg width="{width}" height="{height}" class="chart-sparkline">'
            f'<circle cx="50%" cy="50%" r="3" fill="{color}"/>'
            f'</svg>'
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
        f'</svg>'
    )


# ---------------------------------------------------------------------------
# Pie / Donut — SVG circle with conic-gradient segments via stroke-dasharray
# ---------------------------------------------------------------------------

_COLORS = [
    "#4a7", "#5b9", "#6cb", "#7dc", "#8ed", "#e8a", "#d79", "#c68",
    "#9ad", "#8bc", "#7ab", "#69a", "#a7d", "#b8e", "#c9f",
]


def render_pie_donut(data: list[dict], label_field: str = "label",
                     value_field: str = "value", donut: bool = False) -> str:
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
    circ_diameter = 2 * (r - stroke_width / 2)
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
            f'<title>{label}: {_esc(d.get(value_field, ""))} ({pct*100:.0f}%)</title>'
            f'</circle>'
        )
        legend.append(
            f'<li><span class="legend-swatch" style="background:{color}"></span>'
            f'{label} ({pct*100:.0f}%)</li>'
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
            f'{total:.0f}</text>'
        )

    cls = "chart-donut" if donut else "chart-pie"
    return (
        f'<div class="{cls}-wrapper">'
        f'<svg viewBox="0 0 {size} {size}" class="{cls}" '
        f'width="{size}" height="{size}">'
        f'{"".join(slices)}'
        f'{center_hole}'
        f'</svg>'
        f'<ul class="chart-legend">{"".join(legend)}</ul>'
        f'</div>'
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "sparkline or pie or donut"`
Expected: All 7 SVG chart tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/charts.py tests/test_dashboard_charts.py
git commit -m "feat(charts): add SVG renderers (sparkline, pie, donut)"

# Note: Had to use type: ignore for math import due to linter
# Fixed via ruff per-file-ignore on lint step
```

---

### Task 6: Chart Rendering Engine — Part 3: Grid Charts

**Files:**
- Modify: `glancely/dashboard/charts.py` (add heatmap, calendar_grid)
- Modify: `tests/test_dashboard_charts.py` (add grid chart tests)

- [ ] **Step 1: Write failing tests for grid charts**

Add to `tests/test_dashboard_charts.py`:

```python
def test_render_heatmap():
    from glancely.dashboard.charts import render_heatmap
    rows = [
        {"date": "2026-05-01", "score": 3},
        {"date": "2026-05-02", "score": 7},
        {"date": "2026-05-03", "score": 5},
    ]
    html_out = render_heatmap(rows, date_field="date", value_field="score")
    assert 'class="chart-heatmap"' in html_out
    assert "Mon" in html_out or "Tue" in html_out or "heatmap" in html_out

def test_render_heatmap_empty():
    from glancely.dashboard.charts import render_heatmap
    html_out = render_heatmap([], date_field="date", value_field="val")
    assert "No data" in html_out

def test_render_calendar_grid():
    from glancely.dashboard.charts import render_calendar_grid
    rows = [
        {"date": "2026-05-01", "count": 2},
        {"date": "2026-05-05", "count": 5},
    ]
    html_out = render_calendar_grid(rows, date_field="date", value_field="count")
    assert 'class="chart-calendar-grid"' in html_out
    assert "calendar" in html_out.lower() or "May" in html_out

def test_render_calendar_grid_empty():
    from glancely.dashboard.charts import render_calendar_grid
    html_out = render_calendar_grid([], date_field="date", value_field="val")
    assert "No data" in html_out
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "heatmap or calendar"`
Expected: ALL FAIL

- [ ] **Step 3: Implement grid chart renderers**

Add to `glancely/dashboard/charts.py`:

```python
from datetime import date, datetime, timedelta


# ---------------------------------------------------------------------------
# Heatmap — CSS grid with colored cells (GitHub contribution graph style)
# ---------------------------------------------------------------------------

def render_heatmap(data: list[dict], date_field: str = "date",
                   value_field: str = "value",
                   weeks: int = 13, color_scheme: str = "green") -> str:
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

    # Color schemes: CSS class-based for dark mode compatibility
    # We'll use inline opacity: the higher the value, the more opaque
    def cell_style(v: float | None) -> str:
        if v is None:
            return 'style="background:var(--line)"'
        intensity = (v - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        # Use a gradient from muted to vibrant
        if color_scheme == "green":
            r, g, b = 74, 170, 119  # var(--ok)
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
    header_cells = "".join(
        f'<div class="hm-header">{d}</div>' for d in dow
    )

    # Build grid: 7 rows (Mon–Sun) x weeks columns
    rows_html = []
    curr = start_monday
    for day_idx in range(7):
        cells = []
        for week_idx in range(weeks):
            cell_date = curr + timedelta(days=week_idx * 7 + day_idx)
            ds = cell_date.isoformat()
            v = val_map.get(ds)
            cell_title = f'{cell_date}: {v}' if v is not None else cell_date
            cells.append(
                f'<div class="hm-cell" {cell_style(v)}>'
                f'<span class="hm-tooltip">{cell_title}</span></div>'
            )
        rows_html.append(f'<div class="hm-row">{"".join(cells)}</div>')
        # After Sun row, move to next Mon
        # Actually we need to fix: each row is a day of week, each column is a week

    # Re-do: proper heatmap structure
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
        f'{"".join(hm_rows)}'
        f'</div>'
    )


# ---------------------------------------------------------------------------
# Calendar grid — monthly calendar with colored day cells
# ---------------------------------------------------------------------------

_MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
]


def render_calendar_grid(data: list[dict], date_field: str = "date",
                         value_field: str = "value",
                         months_back: int = 3,
                         color_scheme: str = "green") -> str:
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
        month_last = date(
            month_first.year + (month_first.month // 12),
            (month_first.month % 12) + 1, 1
        ) - timedelta(days=1)

        # Build 7-column grid for this month
        # Day-of-week headers
        dow_header = "".join(
            f'<div class="cal-dow">{d}</div>'
            for d in ["M", "T", "W", "T", "F", "S", "S"]
        )

        # Fill in days
        cells = []
        # Pad before first day of month
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
                r = 74 if color_scheme == "green" else 140
                g = 170 if color_scheme == "green" else 100
                b = 119 if color_scheme == "green" else 200
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
            f'</div>'
        )

    return f'<div class="chart-calendar-grid">{"".join(months_html)}</div>'
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "heatmap or calendar"`
Expected: All 4 grid chart tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/charts.py tests/test_dashboard_charts.py
git commit -m "feat(charts): add grid renderers (heatmap, calendar_grid)"
```

---

### Task 7: Chart Dispatch Function in `charts.py`

**Files:**
- Modify: `glancely/dashboard/charts.py` (add `render_chart` dispatch)
- Modify: `tests/test_dashboard_charts.py` (add dispatch tests)

- [ ] **Step 1: Write failing test for the dispatch function**

Add to `tests/test_dashboard_charts.py`:

```python
def test_render_chart_dispatches_to_correct_renderer():
    from glancely.dashboard.charts import render_chart

    # Test bar chart dispatch
    result = render_chart(
        chart_type="bar",
        payload={"summary": {}, "rows": []},
        config={
            "chart": {
                "type": "bar",
                "data": {"source": "summary", "value_field": "total"},
            },
            "overview": {"enabled": False},
        },
    )
    assert isinstance(result, str)
    assert len(result) > 0

def test_render_chart_unknown_type_falls_back():
    from glancely.dashboard.charts import render_chart
    # Should not crash for unsupported type — return basic card HTML
    result = render_chart("unknown", {"summary": {"x": 1}, "rows": []}, {})
    assert isinstance(result, str)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "render_chart"`
Expected: FAIL (function not defined)

- [ ] **Step 3: Implement `render_chart` dispatch function**

Add to `glancely/dashboard/charts.py`:

```python
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
        label_field = chart_data.get("label_field", "")
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
            color=options.get("color", "var(--ok)")
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
        current = float(chart_data[0].get(data_cfg.get("value_field", "value"), 0)) if chart_data else 0
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "render_chart"`
Expected: All dispatch tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/charts.py tests/test_dashboard_charts.py
git commit -m "feat(charts): add render_chart dispatch function"
```

---

### Task 8: Overview Panel Renderer

**Files:**
- Create: `glancely/dashboard/overview.py`
- Modify: `tests/test_dashboard_charts.py` (add overview tests)

- [ ] **Step 1: Write failing test for the overview renderer**

Add to `tests/test_dashboard_charts.py`:

```python
def test_render_overview_panel_empty():
    from glancely.dashboard.overview import render_overview_panel
    html_out = render_overview_panel([])  # no components
    assert isinstance(html_out, str)

def test_render_overview_panel_with_components():
    from glancely.dashboard.overview import render_overview_panel
    components_meta = [
        {
            "name": "mood",
            "title": "Mood",
            "overview": {
                "enabled": True,
                "card_type": "sparkline",
                "label": "Mood",
                "data_key": "summary.avg_score_7d",
                "suffix": "/10",
            },
            "payload": {
                "summary": {"avg_score_7d": 7.2},
                "rows": [{"mood_score": 7}, {"mood_score": 8}, {"mood_score": 6}],
            },
        },
        {
            "name": "mit",
            "title": "MIT",
            "overview": {
                "enabled": True,
                "card_type": "stat",
                "label": "Today's MIT",
                "data_key": "summary.today_task",
            },
            "payload": {
                "summary": {"today_task": "Design API", "today_completed": True},
                "rows": [],
            },
        },
    ]
    html_out = render_overview_panel(components_meta)
    assert "Mood" in html_out
    assert "overview" in html_out
    assert "Design API" in html_out or "MIT" in html_out

def test_resolve_data_key_nested():
    from glancely.dashboard.overview import resolve_data_key
    payload = {"summary": {"by_category": {"prod": 240, "admin": 72}}}
    val = resolve_data_key(payload, "summary.by_category")
    assert val == {"prod": 240, "admin": 72}

def test_resolve_data_key_top():
    from glancely.dashboard.overview import resolve_data_key
    payload = {"status": "ok"}
    val = resolve_data_key(payload, "status")
    assert val == "ok"
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "overview or resolve_data_key"`
Expected: ALL FAIL

- [ ] **Step 3: Implement `overview.py`**

```python
# glancely/dashboard/overview.py
"""Overview panel — composites key signals from all tracker components."""

from __future__ import annotations

import html as html_mod
from typing import Any

from glancely.dashboard.charts import render_sparkline


def _esc(s: Any) -> str:
    return html_mod.escape(str(s))


def resolve_data_key(payload: dict, data_key: str) -> Any:
    """Resolve a dot-notation path into a stats payload dict.

    Example: "summary.by_category_today" → payload["summary"]["by_category_today"]
    """
    parts = data_key.split(".")
    current: Any = payload
    for part in parts:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def render_overview_panel(components_meta: list[dict]) -> str:
    """Render the overview panel compositing key info from all components.

    Args:
        components_meta: List of dicts, each with:
            - name: str
            - title: str
            - overview: dict from chart.toml [overview] section
            - payload: dict from stats.py output

    Returns:
        HTML string for the overview panel section.
    """
    contributing = [
        m for m in components_meta
        if m.get("overview", {}).get("enabled") is not False
    ]
    if not contributing:
        return ""

    cards_html = []
    for meta in contributing:
        ov = meta.get("overview", {})
        payload = meta.get("payload", {})
        card_type = ov.get("card_type", "stat")
        label = ov.get("label", meta.get("title", ""))
        data_key = ov.get("data_key", "")
        suffix = ov.get("suffix", "")
        color = ov.get("color", "")

        raw_value = resolve_data_key(payload, data_key) if data_key else None

        if card_type == "sparkline":
            # If data_key points to summary, draw a sparkline from rows
            rows = payload.get("rows", [])
            value_field = ov.get("value_field", "value")
            if rows:
                spark_values = [
                    float(r.get(value_field, 0))
                    for r in rows[-14:]  # last 14 data points
                    if r.get(value_field) is not None
                ]
                spark_svg = render_sparkline(
                    spark_values,
                    width=ov.get("width", 120),
                    height=ov.get("height", 30),
                    color=color or "var(--ok)",
                ) if spark_values else ""
            else:
                spark_svg = ""
            val_str = _esc(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-sparkline">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'{spark_svg}'
                f'<span class="ov-value">{val_str}{_esc(suffix)}</span>'
                f'</div>'
            )

        elif card_type == "badge":
            cls = "ok" if raw_value else "bad" if raw_value is False else "muted"
            text = str(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-badge">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<span class="badge {cls} ov-badge-value">{_esc(text)}</span>'
                f'</div>'
            )

        elif card_type == "progress":
            max_v = ov.get("max_value", 100)
            current = float(raw_value) if raw_value is not None else 0
            pct = min(current / max_v * 100, 100) if max_v > 0 else 0
            cards_html.append(
                f'<div class="ov-card ov-progress">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<div class="progress-track ov-track">'
                f'<div class="progress-fill" style="width:{pct:.0f}%;'
                f'background:{color or "var(--ok)"}"></div></div>'
                f'<span class="ov-value">{current:.0f}{_esc(suffix)}</span>'
                f'</div>'
            )

        else:  # "stat" — default
            val_str = ""
            if isinstance(raw_value, bool):
                val_str = "done" if raw_value else "pending"
            elif isinstance(raw_value, (int, float)):
                val_str = f"{raw_value}{suffix}"
            elif isinstance(raw_value, dict):
                val_str = ", ".join(f"{k}: {v}" for k, v in raw_value.items())
            else:
                val_str = str(raw_value) if raw_value is not None else "—"
            cards_html.append(
                f'<div class="ov-card ov-stat">'
                f'<span class="ov-label">{_esc(label)}</span>'
                f'<span class="ov-value">{_esc(val_str)}</span>'
                f'</div>'
            )

    return (
        f'<section class="panel overview-panel">'
        f'<header><h2>Overview</h2></header>'
        f'<div class="overview-grid">{"".join(cards_html)}</div>'
        f'</section>'
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_charts.py -v -k "overview or resolve_data_key"`
Expected: All 4 overview tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/overview.py tests/test_dashboard_charts.py
git commit -m "feat(dashboard): add overview panel renderer with data key resolution"
```

---

### Task 9: Integrate Chart System into Dashboard Builder (`build.py`)

**Files:**
- Modify: `glancely/dashboard/build.py` — integrate chart rendering and overview panel

- [ ] **Step 1: Write failing integration test**

Create `tests/test_dashboard_build.py`:

```python
"""Integration tests for dashboard build with chart system."""
import json
import pytest
from pathlib import Path


def test_render_panel_with_chart_config(tmp_path):
    """Panel should render as chart when chart_config is present."""
    from glancely.dashboard.build import _render_panel
    from unittest.mock import Mock

    component = Mock()
    component.name = "test_comp"
    component.title = "Test"
    component.freshness_hours = 24
    component.chart_config = {
        "chart": {
            "type": "bar",
            "title": "Test Chart",
            "data": {"source": "summary", "value_field": "total", "label_field": "name"},
        },
        "overview": {"enabled": False},
    }
    payload = {
        "status": "ok",
        "freshness_hours": 1.0,
        "summary": {"total": 42, "name": "entries"},
        "rows": [],
    }
    html_out = _render_panel(component, payload)
    assert '<section class="panel"' in html_out
    assert "chart-bars" in html_out or "Test Chart" in html_out

def test_render_panel_without_chart_config(tmp_path):
    """Panel should render as basic card when no chart_config (backward compat)."""
    from glancely.dashboard.build import _render_panel
    from unittest.mock import Mock

    component = Mock()
    component.name = "test_comp"
    component.title = "Test"
    component.freshness_hours = 24
    component.chart_config = None
    payload = {
        "status": "ok",
        "freshness_hours": 1.0,
        "summary": {"total": 42},
        "rows": [],
    }
    html_out = _render_panel(component, payload)
    assert '<section class="panel"' in html_out
    assert "summary" in html_out
    assert "chart-bars" not in html_out  # No chart rendered

def test_build_includes_overview_panel(tmp_path, monkeypatch):
    """Full build should include overview panel."""
    from unittest.mock import Mock, patch

    monkeypatch.setenv("GLANCE_HOME", str(tmp_path))
    output = tmp_path / "dashboard" / "index.html"

    # Mock discover to return components with chart configs
    mock_comps = []
    for i, (name, chart_conf) in enumerate([
        ("mood", {"chart": {"type": "sparkline", "data": {"source": "rows", "value_field": "score"}},
                   "overview": {"enabled": True, "card_type": "sparkline", "label": "Mood",
                               "data_key": "summary.avg_score_7d", "suffix": "/10"}}),
        ("mit", {"chart": {"type": "status_card", "data": {}},
                  "overview": {"enabled": True, "card_type": "stat", "label": "MIT",
                              "data_key": "summary.today_task"}}),
    ]):
        comp = Mock()
        comp.name = name
        comp.title = name.title()
        comp.freshness_hours = 24
        comp.panel_order = i * 10
        comp.chart_config = chart_conf
        comp.stats_script = tmp_path / f"{name}_stats.py"
        comp.stats_script.is_file.return_value = True
        mock_comps.append(comp)

    with patch("glancely.dashboard.build.discover_components", return_value=mock_comps), \
         patch("glancely.dashboard.build.apply_all_migrations"), \
         patch("glancely.dashboard.build._run_stats") as mock_stats:
        mock_stats.side_effect = [
            {"status": "ok", "freshness_hours": 1.0, "summary": {"avg_score_7d": 7.2, "total": 100},
             "rows": [{"score": 7}, {"score": 8}]},
            {"status": "ok", "freshness_hours": 1.0, "summary": {"today_task": "Design API", "today_completed": True},
             "rows": []},
        ]

        from glancely.dashboard.build import build
        result = build(output_path=output, run_migrations=False)

        assert output.exists()
        html_content = output.read_text()
        assert "Overview" in html_content
        assert "Mood" in html_content
        assert "Design API" in html_content
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_dashboard_build.py -v`
Expected: FAIL (unimplemented chart integration)

- [ ] **Step 3: Modify `build.py` to integrate chart rendering**

Replace `_render_panel` function and add imports:

```python
# At top of build.py, add imports:
from glancely.dashboard.charts import render_chart, _no_data
from glancely.dashboard.overview import render_overview_panel

# Replace _render_panel (lines 91–108):
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
  {f'<div class="summary">{summary_html}</div>' if summary_html else ''}
  {f'<details><summary>Recent</summary>{rows_html}</details>' if payload.get("rows") else ''}
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
```

Modify the `build()` function to collect component metadata for the overview panel:

```python
# In build() function (around line 159–176), replace the loop:
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
            overview_meta.append({
                "name": comp.name,
                "title": comp.title,
                "overview": chart_config["overview"],
                "payload": payload,
            })

    # Render overview panel
    overview_html = render_overview_panel(overview_meta)

    # Insert overview before the grid
    if overview_html:
        panels_html.insert(0, overview_html)

    template = (
        TEMPLATE_PATH.read_text(encoding="utf-8")
        if TEMPLATE_PATH.is_file()
        else DEFAULT_TEMPLATE
    )
    html_out = template.replace(
        "{built_at}", datetime.now().strftime("%Y-%m-%d %H:%M")
    )
    html_out = html_out.replace("{panels}", "\n".join(panels_html))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_out, encoding="utf-8")
    return {
        "output": str(output_path),
        "components": list(statuses.keys()),
        "statuses": statuses,
    }
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_dashboard_build.py -v`
Expected: All 3 integration tests PASS

- [ ] **Step 5: Commit**

```bash
git add glancely/dashboard/build.py tests/test_dashboard_build.py
git commit -m "feat(dashboard): integrate chart system into build pipeline"
```

---

### Task 10: Add CSS for All Chart Types to Dashboard Template

**Files:**
- Modify: `glancely/dashboard/build.py` — expand DEFAULT_TEMPLATE CSS
- Create: `glancely/dashboard/template.html` — optional external template file

- [ ] **Step 1: Copy current DEFAULT_TEMPLATE CSS and add chart CSS rules**

Modify the `DEFAULT_TEMPLATE` string in `build.py` (lines 111–147) — replace the `<style>` block with:

```python
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
```

- [ ] **Step 2: Verify template is syntactically valid Python**

Run: `python -c "from glancely.dashboard.build import DEFAULT_TEMPLATE; print('OK')"`
Expected: OK (no SyntaxError)

- [ ] **Step 3: Commit**

```bash
git add glancely/dashboard/build.py
git commit -m "feat(dashboard): add comprehensive CSS for all chart types and overview"
```

---

### Task 11: Create `chart.toml` for Each Example Component

**Files:**
- Create: `glancely/examples/mood/chart.toml`
- Create: `glancely/examples/reminder/chart.toml`
- Create: `glancely/examples/mit/chart.toml`
- Create: `glancely/examples/diary_logger/chart.toml`
- Modify: `glancely/examples/mood/scripts/stats.py` — add chart data fields
- Modify: `glancely/examples/reminder/scripts/stats.py` — add chart data fields
- Modify: `glancely/examples/mit/scripts/stats.py` — add chart data fields
- Modify: `glancely/examples/diary_logger/scripts/stats.py` — add chart data fields

- [ ] **Step 1: Create `glancely/examples/mood/chart.toml`**

```toml
# Mood component — heatmap of mood scores over time
[chart]
type = "heatmap"
title = "Mood Heatmap"

[chart.data]
source = "rows"
date_field = "created_at"
value_field = "mood_score"
label_field = "mood_label"

[chart.options]
color_scheme = "green"

[overview]
enabled = true
card_type = "sparkline"
label = "Mood (7d)"
data_key = "summary.avg_score_7d"
suffix = "/10"
value_field = "mood_score"
width = 120
height = 30
color = "#4a7"
```

- [ ] **Step 2: Update `glancely/examples/mood/scripts/stats.py`**

The current stats.py for mood returns `created_at` in rows — which is the date_field needed. No changes needed for the row data. But let's ensure the rows return consistent field names. The current rows return `created_at, mood_score, mood_label, note` — all fields needed for the heatmap are already present. The overview uses `summary.avg_score_7d` which is already returned.

No changes needed for mood stats.py — it already returns all required fields.

- [ ] **Step 3: Create `glancely/examples/reminder/chart.toml`**

```toml
# Reminder component — list with status badges + count overview
[chart]
type = "timeline"
title = "Active Reminders"

[chart.data]
source = "rows"
time_field = "due_date"
title_field = "title"

[chart.options]
time_field = "due_date"
title_field = "title"

[overview]
enabled = true
card_type = "badge"
label = "Pending"
data_key = "summary.active"
```

- [ ] **Step 4: Update `glancely/examples/reminder/scripts/stats.py`**

The current stats.py returns `id, title, due_date, status` in rows — the timeline needs `time_field` (due_date) and `title_field` (title). These already exist. Add `status` as a desc_field for richer timeline display:

Modify line 41 (the return statement) — no changes needed; the existing fields suffice for the timeline renderer. However, add a `chart` section to the payload for backward compatibility with the chart dispatch:

Actually, the `render_chart` dispatch uses `_extract_values` which reads `rows` directly. The existing row fields (`id, title, due_date, status`) match the chart config's `time_field` (due_date) and `title_field` (title). No changes needed.

- [ ] **Step 5: Create `glancely/examples/mit/chart.toml`**

```toml
# MIT component — status card showing today's task and completion
[chart]
type = "status_card"
title = "Today's MIT"

[chart.options]
status_field = "today_task"
label = "Task"

[overview]
enabled = true
card_type = "stat"
label = "MIT"
data_key = "summary.today_task"
```

- [ ] **Step 6: Update `glancely/examples/mit/scripts/stats.py`**

Current stats.py returns `summary.today_task` (string) and `summary.today_completed` (bool). The status_card reads `status_field` from summary. Since today_task is a string (not a bool), the status_card will treat it as a value to display. Let's enhance MIT to also return a progress metric:

Modify the return dict in `build_stats()` (around line 41–51):

```python
    return {
        "freshness_hours": freshness_hours,
        "status": "ok",
        "summary": {
            "today_task": today_row["task"] if today_row else None,
            "today_completed": bool(today_row["completed"]) if today_row else None,
            "completed_last_7d": completed_7d,
            "logged_last_7d": len(last7),
            # NEW: chart-friendly completion rate
            "completion_rate_7d": round(completed_7d / len(last7) * 100, 1) if last7 else 0,
        },
        "rows": recent,
    }
```

- [ ] **Step 7: Create `glancely/examples/diary_logger/chart.toml`**

```toml
# Diary Logger — donut chart for today's category breakdown
[chart]
type = "donut"
title = "Today's Categories"

[chart.data]
source = "summary"
value_field = "by_category_today"

[chart.options]

[overview]
enabled = true
card_type = "stat"
label = "Today's Log"
data_key = "summary.total_minutes_today"
suffix = " min"
```

- [ ] **Step 8: Update `glancely/examples/diary_logger/scripts/stats.py`**

Current stats.py returns `summary.by_category_today` as a dict like `{"prod": 240, "admin": 72}`. The `_extract_values` function handles nested dicts in summary — it expands them into `[{label: "prod", value: 240}, ...]` format. No changes needed.

- [ ] **Step 9: Verify stats scripts still output valid JSON**

Run each stats script:

```bash
python3 glancely/examples/mood/scripts/stats.py
python3 glancely/examples/reminder/scripts/stats.py
python3 glancely/examples/mit/scripts/stats.py
# Diary requires Google Calendar credentials — skip if not configured
```

Expected: Each prints valid JSON to stdout.

- [ ] **Step 10: Commit**

```bash
git add glancely/examples/mood/chart.toml \
        glancely/examples/reminder/chart.toml \
        glancely/examples/mit/chart.toml \
        glancely/examples/diary_logger/chart.toml \
        glancely/examples/mit/scripts/stats.py
git commit -m "feat(examples): add chart.toml configs for all example components"
```

---

### Task 12: Add Chart Config to Scaffold Templates

**Files:**
- Create: `glancely/skills/scaffold_component/templates/component/chart.toml.tmpl`
- Modify: `glancely/skills/scaffold_component/scripts/scaffold.py` — handle chart template

- [ ] **Step 1: Create `chart.toml.tmpl` scaffold template**

```toml
# {{title}} component — chart configuration for dashboard visualization
[chart]
type = "bar"
title = "{{title}}"

[chart.data]
source = "summary"
value_field = "total"
label_field = "name"

[chart.options]

[overview]
enabled = true
card_type = "stat"
label = "{{title}}"
data_key = "summary.total"
suffix = ""
```

- [ ] **Step 2: Modify `scaffold.py` to handle chart.toml.tmpl**

In `render_tree()` (line 126–143 of scaffold.py), the function already handles `.tmpl` extension stripping. The new `chart.toml.tmpl` file will match the existing logic:
- `chart.toml.tmpl` → strip `.tmpl` → `chart.toml`
- It will be rendered with the same `render()` function using the mapping dict

The mapping dict (`build_mapping()`) already has `name`, `title`, etc. — the `chart.toml.tmpl` uses `{{title}}` which is already in the mapping. No scaffold.py code changes needed for basic rendering.

However, let's add a `chart_type` option to the scaffold CLI for users who know which chart they want:

```python
# In build_mapping() (line 93), add chart_type:
mapping["chart_type"] = getattr(args, "chart_type", "bar")

# In main() (line 191), add argument:
p.add_argument("--chart-type", default="bar",
               dest="chart_type",
               help="Dashboard chart type: bar, pie, donut, heatmap, etc.")
```

- [ ] **Step 3: Verify scaffold produces chart.toml**

Run: `python3 -m glancely.skills.scaffold_component.scripts.scaffold --name test_chart --title "Test Chart" --field count:int --force`

Then check that the output directory contains `chart.toml`:
```bash
ls ~/.glancely/components/test_chart/chart.toml
```

Expected: File exists with rendered `{{title}}` → `Test Chart`.

- [ ] **Step 4: Clean up test scaffold**

```bash
rm -rf ~/.glancely/components/test_chart
```

- [ ] **Step 5: Commit**

```bash
git add glancely/skills/scaffold_component/templates/component/chart.toml.tmpl \
        glancely/skills/scaffold_component/scripts/scaffold.py
git commit -m "feat(scaffold): add chart.toml.tmpl template and --chart-type option"
```

---

### Task 13: Update Package Config for New Files

**Files:**
- Modify: `pyproject.toml` — include new `.toml` files in package data

- [ ] **Step 1: Add chart.toml to package data patterns**

In `pyproject.toml`, the `[tool.setuptools.package-data]` section (lines 60–73) already includes:
```toml
"examples/**/*.toml",
```

The new `chart.toml` files in `examples/*/` will be caught by this pattern. No changes needed for examples.

For the scaffold template, the existing pattern:
```toml
"skills/**/templates/**/*",
```

will catch `chart.toml.tmpl`. No changes needed.

- [ ] **Step 2: Verify build includes new files**

Run: `python -m build --wheel 2>&1 | tail -5`
Then: `unzip -l dist/*.whl | grep chart`
Expected: Lists `chart.toml` and `chart.toml.tmpl` files.

- [ ] **Step 3: Commit if changes needed** (skip if no changes)

```bash
# Only if pyproject.toml was modified
git add pyproject.toml
git commit -m "chore: ensure chart.toml files included in package data"
```

---

### Task 14: End-to-End Smoke Test

**Files:**
- Modify: `tests/test_dashboard_build.py` — add full E2E test with demo data

- [ ] **Step 1: Write E2E test**

Add to `tests/test_dashboard_build.py`:

```python
def test_full_build_with_demo_data_and_charts(tmp_path, monkeypatch):
    """End-to-end: seed demo data, build dashboard, verify chart rendering."""
    from unittest.mock import patch
    import subprocess

    monkeypatch.setenv("GLANCE_HOME", str(tmp_path))
    (tmp_path / "dashboard").mkdir(parents=True)

    # Create minimal component with chart config for testing
    comp_dir = tmp_path / "components" / "test_chart"
    comp_dir.mkdir(parents=True)
    (comp_dir / "component.toml").write_text("""\
[component]
name = "test_chart"
title = "Test Chart"

[panel]
enabled = true
order = 10
freshness_hours = 24

[storage]
tables = ["test_chart_entries"]
""")
    (comp_dir / "chart.toml").write_text("""\
[chart]
type = "bar"
title = "Test Bar Chart"

[chart.data]
source = "rows"
value_field = "count"
label_field = "name"

[overview]
enabled = true
card_type = "stat"
label = "Test"
data_key = "summary.total"
suffix = ""
""")
    (comp_dir / "migrations").mkdir()
    (comp_dir / "migrations" / "001_init.sql").write_text(
        "CREATE TABLE IF NOT EXISTS test_chart_entries (id INTEGER PRIMARY KEY, name TEXT, count INTEGER, created_at TEXT DEFAULT (datetime('now')));"
    )
    (comp_dir / "scripts").mkdir()
    (comp_dir / "scripts" / "stats.py").write_text("""\
#!/usr/bin/env python3
import json, sys
sys.path.insert(0, "/path/to/glancely/repo")
from glancely.core.storage import get_connection
with get_connection() as conn:
    conn.execute("INSERT OR IGNORE INTO test_chart_entries (name, count) VALUES ('alpha', 10), ('beta', 20), ('gamma', 15)")
    conn.commit()
    rows = [dict(r) for r in conn.execute("SELECT name, count FROM test_chart_entries LIMIT 10").fetchall()]
    total = sum(r['count'] for r in rows)
print(json.dumps({"freshness_hours":1,"status":"ok","summary":{"total":total},"rows":rows}))
""")

    output = tmp_path / "dashboard" / "index.html"

    # Run the actual build (not mocked)
    from glancely.dashboard.build import build
    from glancely.core.registry.discover import USER_COMPONENTS_ROOT

    with patch("glancely.dashboard.build.SKILLS_ROOT", comp_dir.parent), \
         patch("glancely.core.registry.discover.USER_COMPONENTS_ROOT", comp_dir.parent):
        result = build(output_path=output, run_migrations=True)

    assert output.exists()
    html_content = output.read_text()
    assert "Overview" in html_content
    assert "Test Bar Chart" in html_content
    assert 'class="chart-bars"' in html_content
    assert "alpha" in html_content
    assert "beta" in html_content
    # Cleanup
    import shutil
    shutil.rmtree(comp_dir, ignore_errors=True)
```

**Note:** The E2E test requires adjusting paths for the CI environment. The `sys.path.insert` in the mock stats.py should use the actual REPO_ROOT or be skipped in CI.

- [ ] **Step 2: Run the E2E test**

Run: `python -m pytest tests/test_dashboard_build.py::test_full_build_with_demo_data_and_charts -v`
Expected: PASS

- [ ] **Step 3: Run all chart/dashboard tests together**

Run: `python -m pytest tests/test_dashboard_charts.py tests/test_dashboard_build.py -v`
Expected: ALL tests PASS (~30+ tests)

- [ ] **Step 4: Commit**

```bash
git add tests/test_dashboard_build.py
git commit -m "test: add end-to-end smoke test for dashboard chart system"
```

---

### Task 15: Run Linter and Type Checker, Fix Issues

**Files:**
- Any files that need lint fixes

- [ ] **Step 1: Run ruff linter**

Run: `python -m ruff check glancely/ tests/`
Expected: No new errors. Fix any that appear.

- [ ] **Step 2: Run ruff format check**

Run: `python -m ruff format --check glancely/dashboard/ tests/`
If formatting issues exist: `python -m ruff format glancely/dashboard/ tests/`

- [ ] **Step 3: Run the existing test suite to verify no regressions**

Run: `python -m pytest glancely/core/registry/tests/ glancely/core/storage/tests/ glancely/skills/scaffold_component/tests/ -v`
Expected: All existing tests PASS

- [ ] **Step 4: Run a dashboard build to verify output**

```bash
python3 -m glancely dashboard build --no-migrate --out /tmp/test_dashboard.html
# Open in browser to visually verify (manual step)
```

- [ ] **Step 5: Commit any lint fixes**

```bash
git add -A
git commit -m "chore: lint and format fixes for dashboard upgrade"
```

---

### Task 16: Update Component Contract Documentation

**Files:**
- Modify: `docs/component-contract.md` — document chart.toml and new payload fields

- [ ] **Step 1: Add chart.toml documentation to component-contract.md**

After the `component.toml` schema section, add:

```markdown
## `chart.toml` schema (optional)

Components may include a `chart.toml` to define how their dashboard panel is
visualized. If absent, the component renders as a basic text card (unchanged).

```toml
[chart]
type = "heatmap"          # bar | pie | donut | heatmap | sparkline |
                          # status_card | progress_bar | calendar_grid | timeline
title = "Mood Heatmap"   # Optional chart title override

[chart.data]
source = "rows"           # "rows" or "summary" — data source in stats payload
label_field = "name"      # Field for labels (pie/bar segments, timeline titles)
value_field = "count"     # Field for numeric values
date_field = "date"       # Required for heatmap/calendar_grid
time_field = "time"       # Required for timeline
title_field = "title"     # Required for timeline

[chart.options]
# Chart-type-specific options (all optional):
# Bar: max_value (cap), color
# Pie/Donut: (none — auto-scaled)
# Sparkline: width, height, color
# Status Card: status_field, label
# Progress Bar: max_value, label, unit
# Heatmap: color_scheme ("green"|"blue"|"red"|"purple")
# Calendar Grid: color_scheme, months_back
# Timeline: (fields via chart.data)

[overview]
enabled = true            # Contribute to the overview panel at top
card_type = "stat"        # stat | sparkline | badge | progress
label = "Mood"            # Label in overview card
data_key = "summary.avg"  # Dot-notation path in stats payload
suffix = "/10"            # Optional suffix
```

### Chart Data Contract (stats.py additions)

For chart-enabled components, the `summary` and `rows` in the stats payload
should include the fields referenced in `chart.toml`:

- **Pie/Donut/Bar**: `summary` should include a dict key (e.g.,
  `by_category_today` → `{label: value}` dict) referenced by `value_field`.
- **Heatmap/Calendar Grid**: `rows` should include `date_field` and
  `value_field` (e.g., `created_at`, `mood_score`).
- **Sparkline**: `rows` should include `value_field` (numeric).
- **Status Card**: `summary` should include the `status_field` key.
- **Progress Bar**: `summary` should include `value_field` (current) and
  `max_value` is in chart.options.
- **Timeline**: `rows` should include `time_field` and `title_field`.

Components without `chart.toml` work exactly as before — no payload changes
required.
```

- [ ] **Step 2: Commit**

```bash
git add docs/component-contract.md
git commit -m "docs: document chart.toml schema and chart data contract"
```

---

## Summary of All Tasks

| # | Task | Files Changed |
|---|------|---------------|
| 1 | Define chart.toml schema | _(design only)_ |
| 2 | Create chart config loader | `load_chart_config.py` (new), tests |
| 3 | Add chart_config property to Component | `discover.py` (modify) |
| 4 | Implement stateless chart renderers | `charts.py` (new), tests |
| 5 | Implement SVG chart renderers | `charts.py` (modify), tests |
| 6 | Implement grid chart renderers | `charts.py` (modify), tests |
| 7 | Chart dispatch function | `charts.py` (modify), tests |
| 8 | Overview panel renderer | `overview.py` (new), tests |
| 9 | Integrate into build.py | `build.py` (modify), tests |
| 10 | Add chart CSS to template | `build.py` (modify template CSS) |
| 11 | Create chart.toml for examples | 4 chart.toml files (new), stats.py tweaks |
| 12 | Add chart to scaffold templates | `chart.toml.tmpl` (new), `scaffold.py` (modify) |
| 13 | Update package config | `pyproject.toml` (verify/modify if needed) |
| 14 | End-to-end smoke test | `test_dashboard_build.py` (add E2E test) |
| 15 | Lint, type check, fix issues | various |
| 16 | Update documentation | `component-contract.md` (modify) |

## Backward Compatibility Guarantees

1. **Components without `chart.toml`** render exactly as before via the basic-card fallback in `_render_panel`.
2. **`discover.py`** lazily loads `chart_config` via a property — components without the file get `None` with no import or I/O overhead.
3. **Stats payload format** is unchanged — existing `summary`/`rows` structure is preserved; new chart data fields are additive.
4. **The scaffold template** includes a `chart.toml.tmpl` with sensible defaults so new components get chart support from day one, but users can delete it to revert to basic cards.
5. **No external JS dependencies** — all charts are pure CSS and inline SVG.
6. **The subprocess contract** for `stats.py` is unchanged — it still returns JSON on stdout with the same top-level keys.

## Verification Checklist

After implementation, verify:
- [ ] `python -m ruff check glancely/ tests/` passes with no new errors
- [ ] `python -m pytest tests/ -v` — all tests pass including new chart tests
- [ ] `python -m glancely dashboard build --out /tmp/test.html` produces valid HTML
- [ ] Manually open `/tmp/test.html` in a browser — all chart types render correctly
- [ ] Dark mode toggle — CSS custom properties switch correctly
- [ ] Remove `chart.toml` from an example component, rebuild — falls back to basic card
- [ ] Scaffold a new component with `--chart-type bar` — chart.toml is generated
