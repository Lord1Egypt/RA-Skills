"""
Chart Rendering Contract Tests — BUG-002 regression suite.

Root cause (BUG-002, 2026-04-14):
  AI used Chart.js for bar/line/radar charts instead of the ECharts standard,
  causing: (1) rotated bar chart labels clipped by grid bottom, (2) line chart
  data artificially split into multiple series with null values, (3) complete
  HTML shell rewrite when switching chart libraries.

These tests verify that:
  1. All charts use ECharts (Chart.js is NOT in the standard template)
  2. Chart containers are <div> elements, not <canvas>
  3. ECharts bar charts with rotated labels have grid.bottom >= 60
  4. Line chart data is not artificially split with null values
"""
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
FIXTURES_DIR = Path(__file__).parent / "fixtures"


def load_html(name: str) -> str:
    """Load an HTML file from fixtures/ or project root."""
    p = FIXTURES_DIR / name
    if not p.exists():
        # Fall back to project root for generated reports
        p = REPO_ROOT.parent / name
    return p.read_text(encoding="utf-8")


def load_project_report(name: str) -> str:
    """Load a project report fixture, then fall back to the user's project directory."""
    path = FIXTURES_DIR / name
    if not path.exists():
        path = REPO_ROOT.parent / name
    if not path.exists():
        pytest.skip(f"project report fixture missing: {path}")
    return path.read_text(encoding="utf-8")


# ── L2: Chart Library Standard ───────────────────────────────────────────────

class TestChartLibraryStandard:
    """All charts must use ECharts. Chart.js is NOT in the standard template."""

    def test_no_chart_js_script_tag(self):
        """Must NOT load Chart.js via <script src>."""
        html = load_html("minimal_report.html")
        assert "chart.js" not in html.lower(), (
            "Chart.js must not be loaded. Use ECharts for ALL charts.\n"
            "See BUG-002: AI generated Chart.js charts causing rendering issues."
        )

    def test_echarts_script_present(self):
        """Must load ECharts via <script src> when charts exist."""
        html = load_project_report("anthropic-2026-report.html")
        assert "echarts" in html.lower(), (
            "ECharts script must be loaded when report contains charts."
        )

    def test_no_canvas_elements(self):
        """Chart containers must use <div>, not <canvas> (Chart.js artifact)."""
        html = load_project_report("anthropic-2026-report.html")
        assert "<canvas" not in html, (
            "<canvas> elements are Chart.js artifacts. Use <div> for ECharts."
        )

    def test_echarts_init_count(self):
        """Must have correct number of echarts.init calls for charts."""
        html = load_project_report("anthropic-2026-report.html")
        init_count = html.count("echarts.init")
        assert init_count >= 3, (
            f"Expected at least 3 echarts.init calls, found {init_count}."
        )

    def test_chart_container_divs(self):
        """Chart containers must be <div> with id starting with 'chart-'."""
        html = load_project_report("anthropic-2026-report.html")
        import re
        chart_divs = re.findall(r'<div\s+id="chart-[^"]+"', html)
        assert len(chart_divs) >= 3, (
            f"Expected at least 3 <div id='chart-...'> containers, found {len(chart_divs)}."
        )


# ── L2: Chart Configuration ─────────────────────────────────────────────────

class TestBarChartConfig:
    """Bar charts must have proper grid bottom when labels are rotated."""

    def test_rotated_labels_have_sufficient_grid_bottom(self):
        """If x-axis labels are rotated, grid.bottom must be >= 60."""
        html = load_project_report("anthropic-2026-report.html")
        # Find grid blocks that contain rotate > 0
        import re
        # Pattern: grid: { ... bottom: NN ... }
        grid_matches = re.findall(r'grid:\s*\{([^}]+)\}', html)
        for grid_config in grid_matches:
            has_rotate = 'rotate:' in grid_config or 'rotate :' in grid_config
            # Check if this grid has a bottom value
            bottom_match = re.search(r'bottom:\s*(\d+)', grid_config)
            if has_rotate and bottom_match:
                bottom = int(bottom_match.group(1))
                assert bottom >= 60, (
                    f"grid.bottom={bottom} is too small for rotated labels. "
                    f"Must be >= 60 when rotate > 0.\n"
                    f"Grid config: {grid_config}"
                )

    def test_bar_chart_has_label_data(self):
        """Bar chart must have x-axis labels for model names."""
        html = load_project_report("anthropic-2026-report.html")
        assert "Claude Opus 4.6" in html, "Bar chart missing 'Claude Opus 4.6' label"
        assert "Claude Sonnet 4.6" in html, "Bar chart missing 'Claude Sonnet 4.6' label"
        assert "Claude Mythos Preview" in html, "Bar chart missing 'Claude Mythos Preview' label"


class TestLineChartConfig:
    """Line charts must not have artificial gaps from null value injection."""

    def test_line_chart_data_completeness(self):
        """Line chart must contain the full data series from the IR."""
        html = load_project_report("anthropic-2026-report.html")
        # The IR data is: [50, 58, 65, 72, 80.8, 87, 91, 93]
        # At minimum, the primary series must contain 80.8 (2026 Q1 value)
        assert "80.8" in html, "Line chart missing 80.8% data point for 2026 Q1"

    def test_line_chart_has_xaxis_labels(self):
        """Line chart must have all expected quarter labels."""
        html = load_project_report("anthropic-2026-report.html")
        expected = ['2025 Q1', '2025 Q2', '2025 Q3', '2025 Q4', '2026 Q1']
        for label in expected:
            assert label in html, f"Line chart missing x-axis label: {label}"


# ── L2: Regression — No HTML Shell Mutation ─────────────────────────────────

class TestNoHtmlShellMutation:
    """Switching chart libraries must NOT change HTML shell structure."""

    def test_kpi_grids_unchanged(self):
        """KPI grid count must not change after chart library switch."""
        html = load_project_report("anthropic-2026-report.html")
        kpi_count = html.count('kpi-grid')
        assert kpi_count >= 5, (
            f"Expected at least 5 kpi-grid references, found {kpi_count}. "
            f"HTML shell may have been mutated during chart changes."
        )

    def test_fade_in_up_on_grids(self):
        """KPI grids must have fade-in-up class on the grid container."""
        html = load_project_report("anthropic-2026-report.html")
        assert 'kpi-grid' in html and 'fade-in-up' in html
        # fade-in-up should be on the grid container, not individual cards
        assert 'kpi-grid' in html and 'fade-in-up">' in html, (
            "fade-in-up class should be on grid containers."
        )

    def test_toc_structure_unchanged(self):
        """If report has TOC, it must still exist after chart changes."""
        html = load_project_report("anthropic-2026-report.html")
        # Only check if the report has TOC structure at all
        has_toc = 'id="toc-toggle-btn"' in html
        if has_toc:
            assert 'id="toc-sidebar"' in html

    def test_summary_card_unchanged(self):
        """If report has summary card, it must still exist after chart changes."""
        html = load_project_report("anthropic-2026-report.html")
        # Only check if the report has summary card structure
        has_card = 'id="card-mode-btn"' in html
        if has_card:
            assert 'id="sc-overlay"' in html

    def test_report_sections_intact(self):
        """All report sections must still exist after chart changes."""
        html = load_project_report("anthropic-2026-report.html")
        assert 'id="section-models"' in html, "Models section missing"
        assert 'id="section-risks"' in html, "Risks section missing"
        assert 'id="section-forecast"' in html, "Forecast section missing"
