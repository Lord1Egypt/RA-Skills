# tests/test_dashboard_charts.py
"""Unit tests for chart config loading, rendering, and dispatch."""

from __future__ import annotations

import pytest

# ============================================================================
# Overview panel tests (Task 8)
# ============================================================================


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


# ============================================================================
# Chart dispatch tests (Task 7)
# ============================================================================


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


# ============================================================================
# Grid chart renderer tests (Task 6)
# ============================================================================


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


# ============================================================================
# SVG chart renderer tests (Task 5)
# ============================================================================


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


def test_render_sparkline_empty():
    from glancely.dashboard.charts import render_sparkline

    html_out = render_sparkline([], width=200, height=40)
    assert html_out == ""


def test_render_pie_chart():
    from glancely.dashboard.charts import render_pie_donut

    data = [
        {"label": "prod", "value": 240},
        {"label": "admin", "value": 72},
        {"label": "meetings", "value": 88},
    ]
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


# ============================================================================
# Stateless chart renderer tests (Task 4)
# ============================================================================


def test_render_progress_bar():
    from glancely.dashboard.charts import render_progress_bar

    html_out = render_progress_bar(current=7, max_value=10, label="Done")
    assert "width:70%" in html_out
    assert "Done" in html_out
    assert "7/10" in html_out


def test_render_progress_bar_zero_max():
    from glancely.dashboard.charts import render_progress_bar

    html_out = render_progress_bar(current=0, max_value=0, label="N/A")
    assert "width:0%" in html_out


def test_render_status_card_ok():
    from glancely.dashboard.charts import render_status_card

    html_out = render_status_card(
        title="Today's MIT",
        value="Design the API",
        status=True,
    )
    assert "Today" in html_out and "MIT" in html_out
    assert "Design the API" in html_out
    assert "ok" in html_out


def test_render_status_card_incomplete():
    from glancely.dashboard.charts import render_status_card

    html_out = render_status_card(
        title="Today's MIT",
        value="Not set",
        status=False,
    )
    assert "Not set" in html_out
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


# ============================================================================
# Config loading tests (Task 2)
# ============================================================================


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
