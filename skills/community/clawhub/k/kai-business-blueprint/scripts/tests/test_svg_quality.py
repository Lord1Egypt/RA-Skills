"""Tests for free-flow SVG layout and quality checks."""

import json
import pytest

from business_blueprint.export_svg import (
    _layout_free_flow,
    _layout_layered,
    _check_layout_quality,
    _render_free_flow_svg,
    _get_subtitle,
    _categorize_system,
)


# ── Fixtures ──────────────────────────────────────────────────────


def _make_blueprint(**overrides):
    """Create a minimal blueprint for testing."""
    bp = {
        "version": "1.0",
        "meta": {"title": "Test Blueprint", "industry": "common"},
        "library": {
            "capabilities": [],
            "actors": [
                {"id": "actor-client", "name": "API Client"},
            ],
            "flowSteps": [
                {
                    "id": "flow-auth",
                    "name": "Authenticate",
                    "systemIds": ["sys-cognito"],
                    "nextStepIds": ["flow-route"],
                    "seqIndex": 0,
                },
                {
                    "id": "flow-route",
                    "name": "Route Request",
                    "systemIds": ["sys-api-gateway"],
                    "nextStepIds": ["flow-execute"],
                    "seqIndex": 1,
                },
                {
                    "id": "flow-execute",
                    "name": "Execute Logic",
                    "systemIds": ["sys-lambda"],
                    "nextStepIds": [],
                    "seqIndex": 2,
                },
            ],
            "systems": [
                {
                    "id": "sys-api-gateway",
                    "name": "API Gateway",
                    "kind": "system",
                    "description": "REST API gateway",
                    "capabilityIds": [],
                    "properties": {"service": "apigateway"},
                },
                {
                    "id": "sys-lambda",
                    "name": "Lambda",
                    "kind": "system",
                    "description": "Serverless compute",
                    "capabilityIds": [],
                    "properties": {"service": "lambda", "features": ["Feature A", "Feature B"]},
                },
                {
                    "id": "sys-cognito",
                    "name": "Cognito",
                    "kind": "system",
                    "description": "User authentication",
                    "capabilityIds": [],
                    "properties": {"service": "cognito-idp"},
                },
            ],
        },
    }
    for key, value in overrides.items():
        if key == "library":
            bp["library"].update(value)
        else:
            bp[key] = value
    return bp


def _make_layered_label_overlap_blueprint():
    """Create a layered blueprint that forces elbow-arrow labels to compete for space."""
    return {
        "version": "1.0",
        "meta": {"title": "Layered Blueprint", "industry": "common"},
        "library": {
            "capabilities": [],
            "actors": [
                {"id": "actor-client", "name": "API Client"},
            ],
            "flowSteps": [],
            "systems": [
                {
                    "id": "sys-entry-a",
                    "name": "Entry A",
                    "kind": "system",
                    "description": "Entry system A",
                    "capabilityIds": [],
                    "layer": "Layer 1",
                    "features": ["Feature A"],
                },
                {
                    "id": "sys-entry-b",
                    "name": "Entry B",
                    "kind": "system",
                    "description": "Entry system B",
                    "capabilityIds": [],
                    "layer": "Layer 1",
                    "features": ["Feature B"],
                },
                {
                    "id": "sys-core-a",
                    "name": "Core A",
                    "kind": "system",
                    "description": "Core system A",
                    "capabilityIds": [],
                    "layer": "Layer 2",
                    "features": ["Feature C"],
                },
                {
                    "id": "sys-core-b",
                    "name": "Core B",
                    "kind": "system",
                    "description": "Core system B",
                    "capabilityIds": [],
                    "layer": "Layer 2",
                    "features": ["Feature D"],
                },
            ],
        },
        "relations": [
            {
                "id": "rel-entry-a-core-b",
                "type": "flows-to",
                "from": "sys-entry-a",
                "to": "sys-core-b",
                "label": "Tool Attach",
            },
            {
                "id": "rel-entry-b-core-a",
                "type": "depends-on",
                "from": "sys-entry-b",
                "to": "sys-core-a",
                "label": "Runtime Host",
            },
        ],
    }


# ── Layout tests ──────────────────────────────────────────────────


class TestLayoutFreeFlow:
    def test_all_systems_get_nodes(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        system_ids = {s["id"] for s in bp["library"]["systems"]}
        node_ids = set(layout["nodes"].keys())
        # All systems should have nodes
        assert system_ids <= node_ids

    def test_clients_node_when_actors_exist(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        assert "clients" in layout["nodes"]

    def test_no_clients_node_without_actors(self):
        bp = _make_blueprint()
        bp["library"]["actors"] = []
        layout = _layout_free_flow(bp)
        assert "clients" not in layout["nodes"]

    def test_main_flow_left_to_right(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        gw = layout["nodes"]["sys-api-gateway"]
        lam = layout["nodes"]["sys-lambda"]
        # API Gateway should be to the left of Lambda
        assert gw["x"] < lam["x"]

    def test_main_flow_center_alignment(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        # All main flow systems should be center-aligned (same center Y ±5px)
        cognito = layout["nodes"]["sys-cognito"]
        gateway = layout["nodes"]["sys-api-gateway"]
        # Cognito is on main flow now (part of chain), same row as API Gateway
        assert abs(cognito["y"] - gateway["y"]) <= 5

    def test_no_overlapping_nodes(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        nodes = list(layout["nodes"].items())
        for i, (a_id, a) in enumerate(nodes):
            for b_id, b in nodes[i + 1:]:
                a_right = a["x"] + a["w"]
                a_bottom = a["y"] + a["h"]
                b_right = b["x"] + b["w"]
                b_bottom = b["y"] + b["h"]
                # No overlap: separated on at least one axis
                separated = (
                    a_right + 5 < b["x"]
                    or b_right + 5 < a["x"]
                    or a_bottom + 5 < b["y"]
                    or b_bottom + 5 < a["y"]
                )
                assert separated, f"{a_id} and {b_id} overlap"


# ── Quality check tests ───────────────────────────────────────────


class TestCheckLayoutQuality:
    def test_clean_blueprint(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        issues = _check_layout_quality(layout, bp)
        # Filter out canvas size for minimal blueprints
        issues = [i for i in issues if "canvas" not in i.lower()]
        assert issues == [], f"Unexpected issues: {issues}"

    def test_missing_system_node(self):
        bp = _make_blueprint()
        bp["library"]["systems"].append(
            {"id": "sys-missing", "name": "Missing", "kind": "system", "capabilityIds": [], "properties": {}}
        )
        layout = _layout_free_flow(bp)
        # The missing system should get a node via fallback placement
        assert "sys-missing" in layout["nodes"]

    def test_title_coverage(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        # Title bottom is y=62, all nodes should be >= 72
        for nid, n in layout["nodes"].items():
            assert n["y"] >= 72, f"{nid} at y={n['y']} overlaps title"

    def test_canvas_minimum_size(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        # Minimal blueprints have fewer systems, canvas adapts
        assert layout["width"] >= 900
        assert layout["height"] >= 200


# ── Rendering tests ───────────────────────────────────────────────


class TestRenderFreeFlowSvg:
    def test_no_empty_fill_or_stroke(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark")
        for line in svg.splitlines():
            assert 'fill=""' not in line, f"Empty fill: {line.strip()[:80]}"
            # Check for empty stroke (but not in defs)
            if 'stroke=""' in line and "<defs>" not in line:
                assert False, f"Empty stroke: {line.strip()[:80]}"

    def test_title_not_covered(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark")
        # Title block: y=10, h=52, bottom=62
        # All element rects with w>100 should be at y>=72
        import re
        for line in svg.splitlines():
            if 'class="title-block"' in line:
                continue
            m = re.search(r'x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', line)
            if m:
                x, y, w, h = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
                if x > 10 and w > 100 and 5 < y < 72:
                    assert False, f"Element at y={y} covers title: {line.strip()[:80]}"

    def test_arrows_exist(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark")
        arrow_lines = [l for l in svg.splitlines() if 'marker-end' in l and ('<line' in l or '<path' in l)]
        # At least the content arrows (not legend)
        content_arrows = [l for l in arrow_lines if 'x1="12"' not in l]
        assert len(content_arrows) >= 2

    def test_dark_theme_colors(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark")
        assert "#34D399" in svg  # dark theme arrow color

    def test_light_theme_colors(self):
        bp = _make_blueprint()
        layout = _layout_free_flow(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="light")
        assert "#0B6E6E" in svg  # light theme arrow color

    def test_dark_background_grows_with_extended_canvas(self):
        bp = _make_layered_label_overlap_blueprint()
        layout = _layout_layered(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark", blueprint=bp)

        import re

        svg_tag = re.search(r'<svg[^>]*height="(\d+)"', svg)
        bg_rect = re.search(r'<rect width="(\d+)" height="(\d+)" fill="#020617"/>', svg)
        grid_rect = re.search(r'<rect width="(\d+)" height="(\d+)" fill="url\(#grid\)"/>', svg)

        assert svg_tag is not None
        assert bg_rect is not None
        assert grid_rect is not None

        svg_h = int(svg_tag.group(1))
        assert int(bg_rect.group(2)) == svg_h
        assert int(grid_rect.group(2)) == svg_h

    def test_elbow_arrow_labels_do_not_overlap(self):
        bp = _make_layered_label_overlap_blueprint()
        layout = _layout_layered(bp)
        svg = _render_free_flow_svg(layout, "Test", "Test", theme="dark", blueprint=bp)

        import re

        def _rect_for(label: str) -> tuple[int, int, int, int]:
            pattern = (
                rf'<rect x="([0-9.]+)" y="([0-9.]+)" width="([0-9.]+)" height="18" '
                rf'rx="3" fill="#1E293B" fill-opacity="0.9"/>'
                rf'<text x="([0-9.]+)" y="([0-9.]+)"[^>]*>{label}</text>'
            )
            match = re.search(pattern, svg)
            assert match is not None, f"Label '{label}' not found"
            x, y, w = int(float(match.group(1))), int(float(match.group(2))), int(float(match.group(3)))
            return x, y, x + w, y + 18

        a = _rect_for("Tool Attach")
        b = _rect_for("Runtime Host")

        overlap = not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
        assert not overlap, f"Arrow labels overlap: {a} vs {b}"


# ── Subtitle truncation tests ─────────────────────────────────────


class TestGetSubtitle:
    def test_truncates_long_english(self):
        sys_obj = {
            "name": "Test",
            "description": "A very long description that should be truncated properly",
            "properties": {"features": ["Provisioned Concurrency Is Very Long", "Another Long Feature Name Here Too"]},
        }
        subs = _get_subtitle(sys_obj)
        for sub in subs:
            px = sum(8 if ord(c) > 127 else 6 for c in sub)
            # Allow ~130px (node width ~140px with some margin)
            assert px <= 135, f"Subtitle too wide: '{sub}' ({px}px)"

    def test_truncates_long_chinese(self):
        sys_obj = {
            "name": "测试",
            "description": "这是一个非常长的中文描述，需要被正确截断以防止溢出节点宽度",
            "properties": {"features": ["非常长的功能名称", "另一个很长的功能特性"]},
        }
        subs = _get_subtitle(sys_obj)
        for sub in subs:
            px = sum(8 if ord(c) > 127 else 6 for c in sub)
            assert px <= 125, f"Subtitle too wide: '{sub}' ({px}px)"

    def test_returns_max_3_lines(self):
        sys_obj = {
            "name": "Test",
            "description": "desc1,desc2,desc3",
            "properties": {"features": ["F1", "F2", "F3", "F4", "F5"]},
        }
        subs = _get_subtitle(sys_obj)
        assert len(subs) <= 3


# ── Categorization tests ──────────────────────────────────────────


class TestCategorizeSystem:
    def test_message_bus_has_colors(self):
        """EventBridge should get proper colors, not empty strings."""
        from business_blueprint.export_svg import _resolve_system_colors
        fill, stroke = _resolve_system_colors("message_bus", "dark")
        assert fill != "", "message_bus should have fill for dark theme"
        assert stroke != "", "message_bus should have stroke for dark theme"

    def test_cloudwatch_cloud_category(self):
        sys_obj = {"name": "CloudWatch", "properties": {"service": "cloudwatch"}}
        assert _categorize_system(sys_obj) == "cloud"

    def test_lambda_backend_category(self):
        sys_obj = {"name": "Lambda", "properties": {"service": "lambda"}}
        assert _categorize_system(sys_obj) == "backend"

    def test_dynamodb_database_category(self):
        sys_obj = {"name": "DynamoDB", "properties": {"service": "dynamodb"}}
        assert _categorize_system(sys_obj) == "database"


# ── Integration test with full blueprint ──────────────────────────


class TestIntegration:
    def test_aws_serverless_blueprint(self):
        """Full quality check on the aws-serverless blueprint."""
        bp_path = pytest.importorskip("pathlib").Path("aws-serverless.blueprint.json")
        if not bp_path.exists():
            pytest.skip("aws-serverless.blueprint.json not found")

        import json as json_mod
        bp = json_mod.loads(bp_path.read_text(encoding="utf-8"))
        layout = _layout_free_flow(bp)

        # Quality check
        issues = _check_layout_quality(layout, bp)
        assert issues == [], f"Layout issues: {issues}"

        # Render and check SVG
        svg = _render_free_flow_svg(
            layout, bp["meta"]["title"], f"Industry: {bp['meta']['industry']}", theme="dark"
        )

        # No empty colors
        assert 'fill=""' not in svg
        assert 'stroke=""' not in svg

        # Title not covered
        import re
        for line in svg.splitlines():
            if 'class="title-block"' in line:
                continue
            m = re.search(r'x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)"', line)
            if m:
                x, y, w = int(m.group(1)), int(m.group(2)), int(m.group(3))
                if x > 10 and w > 100 and 5 < y < 72:
                    assert False, f"Element at y={y} covers title"
