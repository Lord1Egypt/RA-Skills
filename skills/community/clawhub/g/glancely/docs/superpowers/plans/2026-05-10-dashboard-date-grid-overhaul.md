# Dashboard Date-Grid Overhaul Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every tracker default to a read-only date-grid visualization (heatmap or calendar_grid) so users see patterns at a glance — no clicks, no compact stat cards.

**Architecture:** Scaffold auto-infers chart type from field types (numeric → heatmap, text/bool → calendar_grid). The chart.toml template renders the correct data config dynamically. Example chart.tomls are updated to match. No changes to chart renderers or dashboard build — just config and scaffold logic.

**Tech Stack:** Python 3.9+, TOML, SQLite, pytest

---

### Task 1: Add auto-inference of chart type in scaffold.py

**Files:**
- Modify: `glancely/skills/scaffold_component/scripts/scaffold.py:58-131, 215-216`
- Test: `tests/test_scaffold.py` (new file)

- [ ] **Step 1: Write the failing test for auto-inference**

Create `tests/test_scaffold.py`:

```python
"""Tests for scaffold chart-type auto-inference."""
from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "fields,expected",
    [
        ([("count", "int")], "heatmap"),
        ([("weight", "float")], "heatmap"),
        ([("count", "int"), ("notes", "text")], "heatmap"),
        ([("mood", "text")], "calendar_grid"),
        ([("done", "bool")], "calendar_grid"),
        ([], "calendar_grid"),
    ],
)
def test_infer_chart_type(fields, expected):
    from glancely.skills.scaffold_component.scripts.scaffold import _infer_chart_type

    assert _infer_chart_type(fields) == expected


def test_infer_chart_type_respects_explicit():
    """When user passes an explicit --chart-type, never override it."""
    # This is tested via scaffold integration below
    pass
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_scaffold.py -v`
Expected: FAIL with ImportError (function not defined)

- [ ] **Step 3: Add `_infer_chart_type` and change default**

In `glancely/skills/scaffold_component/scripts/scaffold.py`, add after `FIELD_TYPE_TO_SQL` (after line 49):

```python
NUMERIC_FIELD_TYPES = frozenset({"int", "integer", "float", "real"})


def _infer_chart_type(fields: list[tuple[str, str]]) -> str:
    """Pick heatmap for numeric trackers, calendar_grid for text/bool."""
    if not fields:
        return "calendar_grid"
    for _name, ftype in fields:
        if ftype.lower() in NUMERIC_FIELD_TYPES:
            return "heatmap"
    return "calendar_grid"
```

Change line 215 from:
```python
    p.add_argument("--chart-type", default="bar", dest="chart_type",
```
to:
```python
    p.add_argument("--chart-type", default="auto", dest="chart_type",
```

In `build_mapping`, after line 119 (`"freshness_hours": args.freshness_hours,`), add:
```python
        "chart_type": _infer_chart_type(fields) if args.chart_type == "auto" else args.chart_type,
```

And delete the existing `"chart_type": args.chart_type,` on line 123.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_scaffold.py::test_infer_chart_type -v`
Expected: 6 PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_scaffold.py glancely/skills/scaffold_component/scripts/scaffold.py
git commit -m "feat: auto-infer chart type (heatmap for numeric, calendar_grid for text)"
```

---

### Task 2: Update chart.toml.tmpl for dynamic chart configs

**Files:**
- Modify: `glancely/skills/scaffold_component/templates/component/chart.toml.tmpl`
- Modify: `glancely/skills/scaffold_component/templates/component/scripts/stats.py.tmpl`

- [ ] **Step 1: Update the chart.toml.tmpl**

Replace the entire content of `glancely/skills/scaffold_component/templates/component/chart.toml.tmpl`:

```toml
# {{title}} component — chart configuration for dashboard visualization
[chart]
type = "{{chart_type}}"
title = "{{title}}"

[chart.data]
source = "rows"
date_field = "created_at"
value_field = "{{first_numeric}}"

[chart.options]
color_scheme = "{{color_scheme}}"

[overview]
enabled = true
card_type = "stat"
label = "{{title}}"
data_key = "summary.total"
suffix = ""
```

- [ ] **Step 2: Update scaffold.py `build_mapping` to supply new template variables**

In `glancely/skills/scaffold_component/scripts/scaffold.py`, inside `build_mapping` (around line 116-131), replace the `chart_type` line and add `first_numeric` and `color_scheme`:

Replace:
```python
        "chart_type": _infer_chart_type(fields) if args.chart_type == "auto" else args.chart_type,
```

With:
```python
        inferred = _infer_chart_type(fields) if args.chart_type == "auto" else args.chart_type
        first_numeric = "_presence"
        for fn, ft in fields:
            if ft.lower() in NUMERIC_FIELD_TYPES:
                first_numeric = fn
                break
        color_scheme = "green" if inferred == "heatmap" else "blue"
```

And in the return dict, replace:
```python
        "chart_type": args.chart_type,
```
with:
```python
        "chart_type": inferred,
        "first_numeric": first_numeric,
        "color_scheme": color_scheme,
```

- [ ] **Step 3: Update stats.py.tmpl to include a presence marker for calendar_grid**

The calendar_grid needs a numeric value field. For text-only trackers, rows have no numeric field. Add a computed `_presence` column.

In `glancely/skills/scaffold_component/templates/component/scripts/stats.py.tmpl`, after line 31 (`"SELECT * FROM {{name}}_entries ORDER BY created_at DESC LIMIT 10"`), modify to:

Change:
```python
        rows = [
            dict(r) for r in conn.execute(
                "SELECT * FROM {{name}}_entries ORDER BY created_at DESC LIMIT 10"
            ).fetchall()
        ]
```

To:
```python
        raw_rows = conn.execute(
            "SELECT * FROM {{name}}_entries ORDER BY created_at DESC LIMIT 30"
        ).fetchall()
        rows = []
        for r in raw_rows:
            d = dict(r)
            # Calendar grid / heatmap need a numeric value — use 1 as presence marker
            d["_presence"] = 1
            rows.append(d)
```

And change the summary return to match:
```python
        "rows": rows,
```

- [ ] **Step 4: Run a scaffold integration test**

Run: `pytest tests/test_scaffold.py -v`
Expected: tests pass

- [ ] **Step 5: Commit**

```bash
git add glancely/skills/scaffold_component/templates/component/chart.toml.tmpl \
        glancely/skills/scaffold_component/templates/component/scripts/stats.py.tmpl \
        glancely/skills/scaffold_component/scripts/scaffold.py
git commit -m "feat: dynamic chart.toml template with date-field config for heatmap/calendar_grid"
```

---

### Task 3: Update mood example to calendar_grid

**Files:**
- Modify: `glancely/examples/mood/chart.toml`

- [ ] **Step 1: Change mood chart.toml from heatmap to calendar_grid**

Replace `glancely/examples/mood/chart.toml` content:

```toml
# Mood component — calendar grid showing daily mood scores
[chart]
type = "calendar_grid"
title = "Mood"

[chart.data]
source = "rows"
date_field = "created_at"
value_field = "mood_score"
label_field = "mood_label"

[chart.options]
color_scheme = "blue"

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

- [ ] **Step 2: Commit**

```bash
git add glancely/examples/mood/chart.toml
git commit -m "feat: change mood to calendar_grid for glance-friendly date view"
```

---

### Task 4: Update MIT example to calendar_grid

**Files:**
- Modify: `glancely/examples/mit/chart.toml`
- Modify: `glancely/examples/mit/scripts/stats.py`

- [ ] **Step 1: Change MIT chart.toml from status_card to calendar_grid**

Replace `glancely/examples/mit/chart.toml` content:

```toml
# MIT component — calendar grid showing completed/incomplete days
[chart]
type = "calendar_grid"
title = "MIT"

[chart.data]
source = "rows"
date_field = "date"
value_field = "completed"

[chart.options]
color_scheme = "green"

[overview]
enabled = true
card_type = "stat"
label = "Completion"
data_key = "summary.completion_rate_7d"
suffix = "%"
```

- [ ] **Step 2: Update MIT stats.py to return enough rows for calendar_grid**

Currently MIT stats returns only last 7 days. Calendar grid shows 3 months. Expand to 90 days.

In `glancely/examples/mit/scripts/stats.py`, change the query in `build_stats()` from:

```python
        last7 = list(conn.execute(
            "SELECT date, task, completed FROM mit_entries "
            "WHERE date >= date('now','-7 days') ORDER BY date DESC"
        ))
```

To:

```python
        last90 = list(conn.execute(
            "SELECT date, task, completed FROM mit_entries "
            "WHERE date >= date('now','-90 days') ORDER BY date DESC"
        ))
```

Then update all references from `last7` to `last90` (4 occurrences in lines 28-34).

- [ ] **Step 3: Run existing MIT tests to verify no regression**

Run: `pytest glancely/examples/mit/tests/test_mit.py -v`
Expected: existing tests pass

- [ ] **Step 4: Commit**

```bash
git add glancely/examples/mit/chart.toml glancely/examples/mit/scripts/stats.py
git commit -m "feat: change MIT to calendar_grid with 90-day date grid view"
```

---

### Task 5: End-to-end dashboard verification

**Files:**
- Modify: `tests/test_dashboard_build.py`

- [ ] **Step 1: Run existing tests**

Run: `pytest tests/ -v 2>&1 | tail -40`
Expected: all tests pass (or only known failures)

- [ ] **Step 2: Manual end-to-end smoke test**

```bash
rm -rf ~/.glancely
glancely setup
glancely scaffold --name water --title "Water" --field glasses:int --force
glancely scaffold --name gratitude --title "Gratitude" --field feel:text --force
python3 ~/.glancely/components/water/scripts/log.py --glasses 8
python3 ~/.glancely/components/gratitude/scripts/log.py --feel "thankful"
glancely dashboard build
cat ~/.glancely/dashboard/index.html | python3 -c "
import sys
html = sys.stdin.read()
assert 'class=\"chart-heatmap\"' in html, 'Missing heatmap for water'
assert 'class=\"chart-calendar-grid\"' in html, 'Missing calendar_grid for gratitude'
assert 'water' in html.lower()
assert 'gratitude' in html.lower()
print('OK: dashboard renders both chart types')
"
```

Expected: `OK: dashboard renders both chart types`

- [ ] **Step 3: Commit (if any fixes needed)**

---

### Task 6: Update ClawHub skill and PyPI package versions

**Files:**
- Modify: `SKILL.md` (root)
- Modify: `pyproject.toml`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Bump version in pyproject.toml**

Change `version = "0.2.0"` to `version = "0.3.0"`.

- [ ] **Step 2: Bump version in SKILL.md**

Change `version: 0.2.0` to `version: 0.3.0`.

- [ ] **Step 3: Add changelog entry**

Prepend to `CHANGELOG.md`:

```markdown
## 0.3.0 (2026-05-10)

- Dashboard overhaul: every tracker defaults to a date-grid visualization
- New trackers auto-infer chart type: numeric fields → heatmap, text/bool → calendar_grid
- Mood: changed to calendar_grid for glance-friendly daily view
- MIT: changed to calendar_grid showing 90-day completion history
- Scaffold template includes `_presence` marker for text-only trackers
```

- [ ] **Step 4: Commit**

```bash
git add SKILL.md pyproject.toml CHANGELOG.md
git commit -m "chore: bump to 0.3.0"
```

- [ ] **Step 5: Build and publish to PyPI**

```bash
python3 -m build
python3 -m twine upload dist/*
```

- [ ] **Step 6: Publish updated skill to ClawHub**

```bash
npx clawhub skill publish . --slug glancely --version 0.3.0 --changelog "Dashboard overhaul: date-grid defaults (heatmap for numeric, calendar_grid for text), MIT calendar view, mood calendar view"
```
