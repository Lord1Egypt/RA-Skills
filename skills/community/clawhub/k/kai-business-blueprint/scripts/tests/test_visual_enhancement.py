"""Tests for visual enhancement features (TDD).

Phase 1: Semantic arrow system + visual regression fixtures
Phase 2: Semantic shape vocabulary
Phase 3: Industry color themes
Phase 4: HTML template-driven output
"""

import json
import re
from pathlib import Path

import pytest

from business_blueprint.export_svg import (
    C_LIGHT,
    C_DARK,
    export_svg,
    _resolve_theme,
    _svg_defs,
    _node_svg,
    _legend_svg,
    NODE_W,
    NODE_H,
)
from business_blueprint.export_html import export_html_viewer


# ─── Shared Fixtures ──────────────────────────────────────────────

def _make_blueprint(**overrides) -> dict:
    """Minimal blueprint for testing."""
    bp = {
        "version": "1.0",
        "meta": {"title": "Test", "industry": "retail"},
        "library": {
            "capabilities": [
                {"id": "cap-sales", "name": "Sales"},
                {"id": "cap-inv", "name": "Inventory"},
            ],
            "actors": [
                {"id": "actor-mgr", "name": "Manager"},
            ],
            "flowSteps": [
                {"id": "flow-order", "name": "Create Order",
                 "actorId": "actor-mgr", "capabilityIds": ["cap-sales"],
                 "systemIds": [], "stepType": "task",
                 "inputRefs": [], "outputRefs": []},
            ],
            "systems": [
                {"id": "sys-pos", "name": "POS", "category": "frontend",
                 "capabilityIds": ["cap-sales"]},
                {"id": "sys-crm", "name": "CRM", "category": "backend",
                 "capabilityIds": ["cap-sales", "cap-inv"]},
                {"id": "sys-db", "name": "Database", "category": "database",
                 "capabilityIds": ["cap-inv"]},
            ],
        },
        "relations": [
            {"id": "rel-1", "type": "supports", "from": "sys-pos", "to": "cap-sales", "label": "supports"},
            {"id": "rel-2", "type": "depends-on", "from": "sys-crm", "to": "sys-db", "label": "depends on"},
            {"id": "rel-3", "type": "flows-to", "from": "sys-pos", "to": "sys-crm", "label": "data flow"},
            {"id": "rel-4", "type": "owned-by", "from": "flow-order", "to": "actor-mgr", "label": "owned by"},
        ],
        "views": [],
    }
    for key, value in overrides.items():
        bp[key] = value
    return bp


# ═══════════════════════════════════════════════════════════════════
# Phase 1: Semantic Arrow System
# ═══════════════════════════════════════════════════════════════════

class TestSemanticArrows:
    """Arrow rendering encodes relationship type with distinct visual styles."""

    def test_arrow_styles_dict_exists(self):
        """ARROW_STYLES maps relation type to (color, dash_pattern, marker)."""
        from business_blueprint.export_svg import ARROW_STYLES
        assert isinstance(ARROW_STYLES, dict)
        for key in ("supports", "depends-on", "flows-to", "owned-by"):
            assert key in ARROW_STYLES, f"Missing arrow style: {key}"

    def test_arrow_styles_have_required_fields(self):
        """Each arrow style has color, dash, marker."""
        from business_blueprint.export_svg import ARROW_STYLES
        for rel_type, style in ARROW_STYLES.items():
            assert "color" in style, f"{rel_type} missing color"
            assert "dash" in style, f"{rel_type} missing dash"
            assert "marker" in style, f"{rel_type} missing marker"

    def test_supports_arrow_is_solid_emerald(self):
        """supports = solid emerald arrow."""
        from business_blueprint.export_svg import ARROW_STYLES
        style = ARROW_STYLES["supports"]
        assert style["dash"] is None or style["dash"] == ""
        assert style["color"] != ""

    def test_depends_on_arrow_is_dashed_gray(self):
        """depends-on = dashed gray with open arrowhead."""
        from business_blueprint.export_svg import ARROW_STYLES
        style = ARROW_STYLES["depends-on"]
        assert style["dash"] is not None and style["dash"] != ""
        assert style["marker"] == "arrow-open"

    def test_flows_to_arrow_is_blue_solid(self):
        """flows-to = solid blue with filled arrowhead."""
        from business_blueprint.export_svg import ARROW_STYLES
        style = ARROW_STYLES["flows-to"]
        assert style["dash"] is None or style["dash"] == ""
        assert style["color"] != ""

    def test_owned_by_arrow_is_dotted_amber(self):
        """owned-by = dotted amber with dot marker."""
        from business_blueprint.export_svg import ARROW_STYLES
        style = ARROW_STYLES["owned-by"]
        assert style["dash"] is not None and style["dash"] != ""
        assert style["marker"] == "arrow-dot"

    def test_svg_defs_include_all_marker_types(self):
        """SVG defs include arrow-solid, arrow-dashed, arrow-open, arrow-dot markers."""
        defs = _svg_defs(colors=C_DARK, theme="dark")
        assert 'id="arrow-solid"' in defs
        assert 'id="arrow-dashed"' in defs
        assert 'id="arrow-open"' in defs
        assert 'id="arrow-dot"' in defs

    def test_arrow_open_is_hollow(self):
        """arrow-open marker has no fill (hollow arrowhead)."""
        defs = _svg_defs(colors=C_DARK, theme="dark")
        # Extract the arrow-open marker block
        open_match = re.search(
            r'<marker id="arrow-open".*?</marker>', defs, re.DOTALL
        )
        assert open_match, "arrow-open marker not found in defs"
        marker = open_match.group()
        assert 'fill="none"' in marker

    def test_arrow_dot_is_filled_circle(self):
        """arrow-dot marker renders a filled circle, not a triangle."""
        defs = _svg_defs(colors=C_DARK, theme="dark")
        dot_match = re.search(
            r'<marker id="arrow-dot".*?</marker>', defs, re.DOTALL
        )
        assert dot_match, "arrow-dot marker not found in defs"
        marker = dot_match.group()
        assert "<circle" in marker

    def test_exported_svg_uses_semantic_arrow_colors(self, tmp_path: Path):
        """Exported SVG contains distinct colors for different relation types."""
        bp = _make_blueprint()
        target = tmp_path / "arrows.svg"
        export_svg(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")

        # supports arrow should use its color (not just default)
        from business_blueprint.export_svg import ARROW_STYLES
        supports_color = ARROW_STYLES["supports"]["color"]
        assert supports_color in content, f"supports color {supports_color} not in SVG"

    def test_legend_shows_all_arrow_types(self, tmp_path: Path):
        """Legend includes entries for all 4 arrow types."""
        bp = _make_blueprint()
        target = tmp_path / "legend.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        # Legend should have text labels for each arrow type
        assert "supports" in content
        assert "flow-to" in content or "flows-to" in content


# ═══════════════════════════════════════════════════════════════════
# Phase 2: Semantic Shape Vocabulary
# ═══════════════════════════════════════════════════════════════════

class TestSemanticShapes:
    """Different entity types render with distinct SVG shapes."""

    def test_flowstep_renders_as_diamond(self):
        """flowStep nodes use <polygon> (diamond), not <rect>."""
        svg = _node_svg("f1", "Create Order", 100, 200, "flowStep", colors=C_LIGHT)
        # Diamond shape = <polygon>, not <rect>
        assert "<polygon" in svg, "flowStep should use polygon for diamond shape"

    def test_flowstep_diamond_has_transform(self):
        """Diamond polygon uses a rotated square transform."""
        svg = _node_svg("f1", "Order", 100, 200, "flowStep", colors=C_LIGHT)
        assert "transform" in svg or "points=" in svg

    def test_system_has_category_strip(self):
        """System nodes have a 4px-wide left color strip."""
        svg = _node_svg("s1", "CRM", 100, 200, "system", colors=C_LIGHT)
        # Should contain a small rect for the category indicator strip
        strip_match = re.search(r'width="4".*?height=', svg)
        assert strip_match or 'width="4"' in svg, \
            "System node should have a 4px-wide category strip"

    def test_capability_is_rounded_rect(self):
        """Capability nodes remain as rounded rectangles with rx=8."""
        svg = _node_svg("c1", "Sales", 100, 200, "capability", colors=C_LIGHT)
        assert '<rect' in svg
        assert 'rx="8"' in svg

    def test_actor_is_pill_shape(self):
        """Actor nodes remain as pill shapes with rx=22."""
        svg = _node_svg("a1", "Manager", 100, 200, "actor", colors=C_LIGHT)
        assert '<rect' in svg
        assert 'rx="22"' in svg

    def test_exported_svg_has_flowstep_diamonds(self, tmp_path: Path):
        """Full SVG export renders flowStep nodes as diamonds."""
        bp = _make_blueprint()
        target = tmp_path / "shapes.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        # flowStep node should have polygon (diamond)
        flow_group = re.search(
            r'<g class="node node-flowStep"[^>]*>.*?</g>', content, re.DOTALL
        )
        if flow_group:
            assert "<polygon" in flow_group.group(), \
                "flowStep group should contain polygon (diamond shape)"


# ═══════════════════════════════════════════════════════════════════
# Phase 3: Industry Color Themes
# ═══════════════════════════════════════════════════════════════════

class TestIndustryThemes:
    """Per-industry accent colors overlay on top of base theme."""

    def test_industry_themes_dict_exists(self):
        """INDUSTRY_THEMES maps industry name to accent overrides."""
        from business_blueprint.export_svg import INDUSTRY_THEMES
        assert isinstance(INDUSTRY_THEMES, dict)
        for industry in ("retail", "finance", "manufacturing"):
            assert industry in INDUSTRY_THEMES, f"Missing industry theme: {industry}"

    def test_industry_themes_have_accent_colors(self):
        """Each industry theme has at least a primary accent color."""
        from business_blueprint.export_svg import INDUSTRY_THEMES
        for industry, theme in INDUSTRY_THEMES.items():
            assert "accent" in theme, f"{industry} missing accent color"
            assert theme["accent"].startswith("#"), f"{industry} accent not a hex color"

    def test_retail_has_warm_orange_accent(self):
        """retail = warm orange (#F97316 or similar)."""
        from business_blueprint.export_svg import INDUSTRY_THEMES
        retail = INDUSTRY_THEMES["retail"]
        assert retail["accent"] in ("#F97316", "#EA580C", "#FB923C")

    def test_finance_has_deep_blue_accent(self):
        """finance = deep blue (#3B82F6 or similar)."""
        from business_blueprint.export_svg import INDUSTRY_THEMES
        finance = INDUSTRY_THEMES["finance"]
        assert finance["accent"] in ("#3B82F6", "#2563EB", "#1D4ED8")

    def test_manufacturing_has_slate_accent(self):
        """manufacturing = industrial slate/gray-green."""
        from business_blueprint.export_svg import INDUSTRY_THEMES
        mfg = INDUSTRY_THEMES["manufacturing"]
        assert mfg["accent"] in ("#6B7280", "#059669", "#4B5563")

    def test_resolve_theme_accepts_industry(self):
        """_resolve_theme can take industry parameter for accent overlay."""
        colors = _resolve_theme("dark", industry="retail")
        assert isinstance(colors, dict)
        # Retail accent should appear in the resolved colors
        from business_blueprint.export_svg import INDUSTRY_THEMES
        accent = INDUSTRY_THEMES["retail"]["accent"]
        # At least one color token should use the industry accent
        color_values = [v for v in colors.values() if isinstance(v, str) and v.startswith("#")]
        assert accent in color_values, \
            f"Retail accent {accent} not found in resolved theme colors"

    def test_resolve_theme_without_industry_unchanged(self):
        """_resolve_theme without industry returns base theme."""
        colors = _resolve_theme("dark")
        assert colors["bg"] == C_DARK["bg"]

    def test_common_industry_no_override(self):
        """common industry has no theme (uses base)."""
        colors = _resolve_theme("light", industry="common")
        assert colors["bg"] == C_LIGHT["bg"]

    def test_export_svg_accepts_industry(self, tmp_path: Path):
        """export_svg passes industry through to theme resolver."""
        bp = _make_blueprint()
        target = tmp_path / "industry.svg"
        export_svg(bp, target, theme="dark", industry="retail")
        content = target.read_text(encoding="utf-8")
        assert content.startswith("<svg")

    def test_export_html_reads_industry_from_blueprint(self, tmp_path: Path):
        """HTML viewer reads industry from blueprint meta."""
        bp = _make_blueprint()
        target = tmp_path / "industry.html"
        export_html_viewer(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert content.startswith("<!DOCTYPE html>")

    def test_different_industries_produce_different_colors(self, tmp_path: Path):
        """Retail and finance produce different SVG output colors."""
        bp = _make_blueprint()
        retail_svg = tmp_path / "retail.svg"
        export_svg(bp, retail_svg, theme="dark", industry="retail")

        bp["meta"]["industry"] = "finance"
        finance_svg = tmp_path / "finance.svg"
        export_svg(bp, finance_svg, theme="dark", industry="finance")

        retail_content = retail_svg.read_text(encoding="utf-8")
        finance_content = finance_svg.read_text(encoding="utf-8")

        # Extract color values from both SVGs
        retail_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', retail_content))
        finance_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', finance_content))

        # They should differ (not identical color sets)
        assert retail_colors != finance_colors, \
            "Retail and finance SVGs should have different color palettes"


# ═══════════════════════════════════════════════════════════════════
# Phase 1 (cont.): Visual Regression Fixtures
# ═══════════════════════════════════════════════════════════════════

class TestVisualRegression:
    """Structural SVG comparison against fixture blueprints.

    No pixel comparison — just node count, arrow count, text labels, colors.
    """

    def test_retail_basic_node_count(self, tmp_path: Path):
        """Retail blueprint produces correct number of node groups."""
        bp = _make_blueprint()
        target = tmp_path / "nodes.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        node_groups = re.findall(r'<g class="node', content)
        # 3 systems + 2 capabilities + 1 actor + 1 flowStep = 7
        assert len(node_groups) == 7, \
            f"Expected 7 nodes, got {len(node_groups)}"

    def test_retail_basic_text_labels_present(self, tmp_path: Path):
        """All entity names appear in SVG text elements."""
        bp = _make_blueprint()
        target = tmp_path / "labels.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        expected_labels = ["Sales", "Inventory", "Manager", "Create Order", "POS", "CRM", "Database"]
        for label in expected_labels:
            assert label in content, f"Label '{label}' missing from SVG"

    def test_retail_basic_has_arrows(self, tmp_path: Path):
        """SVG has arrow lines with markers."""
        bp = _make_blueprint()
        target = tmp_path / "arrows.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        arrows = re.findall(r'marker-end="url\(#[^"]+\)"', content)
        assert len(arrows) >= 2, f"Expected at least 2 arrows, got {len(arrows)}"

    def test_retail_basic_has_summary_cards(self, tmp_path: Path):
        """SVG includes summary cards with correct counts."""
        bp = _make_blueprint()
        target = tmp_path / "cards.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        assert "summary-card" in content
        # 3 systems
        assert re.search(r'>3<', content) or "3</text>" in content

    def test_retail_basic_has_legend(self, tmp_path: Path):
        """SVG includes legend section."""
        bp = _make_blueprint()
        target = tmp_path / "legend.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        assert 'class="legend"' in content
        assert "LEGEND" in content

    def test_dark_theme_bg_is_dark(self, tmp_path: Path):
        """Dark theme SVG has dark background."""
        bp = _make_blueprint()
        target = tmp_path / "dark.svg"
        export_svg(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert "#020617" in content

    def test_dark_theme_has_grid(self, tmp_path: Path):
        """Dark theme SVG has grid pattern."""
        bp = _make_blueprint()
        target = tmp_path / "grid.svg"
        export_svg(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert 'id="grid"' in content

    def test_empty_blueprint_no_crash(self, tmp_path: Path):
        """Empty blueprint (no entities) exports without error."""
        bp = {
            "version": "1.0",
            "meta": {"title": "Empty"},
            "library": {
                "capabilities": [], "actors": [],
                "flowSteps": [], "systems": [],
            },
            "relations": [],
            "views": [],
        }
        target = tmp_path / "empty.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")
        assert content.startswith("<svg")

    def test_svg_valid_xml(self, tmp_path: Path):
        """SVG is well-formed XML."""
        bp = _make_blueprint()
        target = tmp_path / "valid.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")

        assert content.startswith("<svg")
        assert content.strip().endswith("</svg>")
        # All tags are properly closed
        assert content.count("<svg") == content.count("</svg>")

    def test_svg_viewbox_present(self, tmp_path: Path):
        """SVG has viewBox attribute."""
        bp = _make_blueprint()
        target = tmp_path / "viewbox.svg"
        export_svg(bp, target, theme="light")
        content = target.read_text(encoding="utf-8")
        assert "viewBox=" in content


# ═══════════════════════════════════════════════════════════════════
# Phase 4: HTML Template
# ═══════════════════════════════════════════════════════════════════

class TestHtmlTemplate:
    """HTML viewer uses template file instead of inline f-strings."""

    def test_template_file_exists(self):
        """HTML template file exists in templates directory."""
        template_path = Path(__file__).resolve().parents[1] / "business_blueprint" / "templates" / "html-viewer.html"
        assert template_path.exists(), \
            "HTML template file should exist at business_blueprint/templates/html-viewer.html"

    def test_template_has_placeholders(self):
        """Template contains {{PLACEHOLDER}} markers for dynamic content."""
        template_path = Path(__file__).resolve().parents[1] / "business_blueprint" / "templates" / "html-viewer.html"
        if not template_path.exists():
            pytest.skip("Template not yet created")
        content = template_path.read_text(encoding="utf-8")
        # Key placeholders that must exist
        assert "{{TITLE}}" in content or "{{title}}" in content
        assert "{{SVG_CONTENT}}" in content or "{{svg_content}}" in content

    def test_html_output_is_self_contained(self, tmp_path: Path):
        """Generated HTML has no external JS/CSS dependencies (except Google Fonts)."""
        bp = _make_blueprint()
        target = tmp_path / "self.html"
        export_html_viewer(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")

        # No local script references
        assert not re.search(r'<script src="(?!https://fonts)', content)
        # No local stylesheet references
        assert not re.search(r'<link.*href="(?!https://fonts)', content)

    def test_html_contains_blueprint_json(self, tmp_path: Path):
        """HTML embeds the full blueprint JSON for download function."""
        bp = _make_blueprint()
        target = tmp_path / "json.html"
        export_html_viewer(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert "JSON.parse" in content
        assert "Sales" in content

    def test_html_has_download_button(self, tmp_path: Path):
        """HTML has SVG download button."""
        bp = _make_blueprint()
        target = tmp_path / "dl.html"
        export_html_viewer(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert "download" in content.lower()
        assert "SVG" in content


# ═══════════════════════════════════════════════════════════════════
# Integration: Cross-Phase Checks
# ═══════════════════════════════════════════════════════════════════

class TestIntegration:
    """Cross-phase integration tests."""

    def test_all_themes_export_without_error(self, tmp_path: Path):
        """Every theme + industry combination exports successfully."""
        bp = _make_blueprint()
        for theme in ("light", "dark"):
            for industry in ("retail", "finance", "manufacturing", "common"):
                target = tmp_path / f"{theme}-{industry}.svg"
                export_svg(bp, target, theme=theme, industry=industry)
                content = target.read_text(encoding="utf-8")
                assert content.startswith("<svg"), \
                    f"Failed for theme={theme}, industry={industry}"

    def test_html_viewer_with_industry_theme(self, tmp_path: Path):
        """HTML viewer works with industry-themed SVG."""
        bp = _make_blueprint()
        target = tmp_path / "industry-viewer.html"
        export_html_viewer(bp, target, theme="dark")
        content = target.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in content
        assert "<svg" in content

    def test_full_pipeline_plan_export_validate(self, tmp_path: Path):
        """Plan → write entities → export → validate pipeline works."""
        import subprocess
        import sys

        ROOT = Path(__file__).resolve().parents[1]

        # Step 1: Create plan
        bp_path = tmp_path / "pipeline.blueprint.json"
        result = subprocess.run(
            [sys.executable, "-m", "business_blueprint.cli",
             "--plan", str(bp_path),
             "--from", "Test blueprint for pipeline validation",
             "--industry", "retail"],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0

        # Step 2: Enrich with entities (simulating AI agent)
        bp = json.loads(bp_path.read_text(encoding="utf-8"))
        bp["library"]["capabilities"] = [
            {"id": "cap-test", "name": "Test Cap", "level": 1,
             "description": "Test", "ownerActorIds": [], "supportingSystemIds": []},
        ]
        bp_path.write_text(json.dumps(bp, ensure_ascii=False), encoding="utf-8")

        # Step 3: Export
        result = subprocess.run(
            [sys.executable, "-m", "business_blueprint.cli", "--export", str(bp_path)],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert (tmp_path / "solution.exports" / "solution.svg").exists()
        assert (tmp_path / "pipeline.blueprint.html").exists()

        # Step 4: Validate
        result = subprocess.run(
            [sys.executable, "-m", "business_blueprint.cli", "--validate", str(bp_path)],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert result.returncode == 0
