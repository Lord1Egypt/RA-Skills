"""Integration tests for dashboard build with chart system."""

from __future__ import annotations


def test_render_panel_with_chart_config(tmp_path):
    """Panel should render as chart when chart_config is present."""
    from unittest.mock import Mock

    from glancely.dashboard.build import _render_panel

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
    from unittest.mock import Mock

    from glancely.dashboard.build import _render_panel

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
    for i, (name, chart_conf) in enumerate(
        [
            (
                "mood",
                {
                    "chart": {
                        "type": "sparkline",
                        "data": {"source": "rows", "value_field": "score"},
                    },
                    "overview": {
                        "enabled": True,
                        "card_type": "sparkline",
                        "label": "Mood",
                        "data_key": "summary.avg_score_7d",
                        "suffix": "/10",
                    },
                },
            ),
            (
                "mit",
                {
                    "chart": {"type": "status_card", "data": {}},
                    "overview": {
                        "enabled": True,
                        "card_type": "stat",
                        "label": "MIT",
                        "data_key": "summary.today_task",
                    },
                },
            ),
        ]
    ):
        comp = Mock()
        comp.name = name
        comp.title = name.title()
        comp.freshness_hours = 24
        comp.panel_order = i * 10
        comp.chart_config = chart_conf
        # Mock stats_script as a regular attribute (not property)
        comp.stats_script = Mock()
        comp.stats_script.is_file.return_value = True
        mock_comps.append(comp)

    with (
        patch("glancely.dashboard.build.discover_components", return_value=mock_comps),
        patch("glancely.dashboard.build.apply_all_migrations"),
        patch("glancely.dashboard.build._run_stats") as mock_stats,
    ):
        mock_stats.side_effect = [
            {
                "status": "ok",
                "freshness_hours": 1.0,
                "summary": {"avg_score_7d": 7.2, "total": 100},
                "rows": [{"score": 7}, {"score": 8}],
            },
            {
                "status": "ok",
                "freshness_hours": 1.0,
                "summary": {"today_task": "Design API", "today_completed": True},
                "rows": [],
            },
        ]

        from glancely.dashboard.build import build

        build(output_path=output, run_migrations=False)

        assert output.exists()
        html_content = output.read_text()
        assert "Overview" in html_content
        assert "Mood" in html_content
        assert "Design API" in html_content
