"""Structured spec builders for export formats.

Each builder reads a canonical blueprint and produces an intermediate
representation that the concrete exporter renders into the target format.
"""

from __future__ import annotations

from typing import Any
from xml.sax.saxutils import escape


# ─── Style matrix ────────────────────────────────────────────────
NODE_STYLES: dict[str, dict[str, Any]] = {
    "capability": {
        "svg": {"tag": "rect", "rx": 8, "ry": 8, "fill": "#E8F5F5", "stroke": "#0B6E6E", "stroke_width": 2},
        "drawio_shape": "roundedRectangle",
        "excalidraw": {"type": "rectangle", "strokeColor": "#0B6E6E", "backgroundColor": "#E8F5F5", "strokeStyle": "solid"},
    },
    "system": {
        "svg": {"tag": "rect", "rx": 0, "ry": 0, "fill": "#E8EEF5", "stroke": "#1C5BD9", "stroke_width": 2},
        "drawio_shape": "rectangle",
        "excalidraw": {"type": "rectangle", "strokeColor": "#1C5BD9", "backgroundColor": "#E8EEF5", "strokeStyle": "solid"},
    },
    "actor": {
        "svg": {"tag": "ellipse", "fill": "#FFF3E0", "stroke": "#D97706", "stroke_width": 2},
        "drawio_shape": "ellipse",
        "excalidraw": {"type": "ellipse", "strokeColor": "#D97706", "backgroundColor": "#FFF3E0", "strokeStyle": "solid"},
    },
    "flowStep": {
        "svg": {"tag": "polygon", "fill": "#F5F0E8", "stroke": "#8B6914", "stroke_width": 1.5},
        "drawio_shape": "process",
        "excalidraw": {"type": "diamond", "strokeColor": "#8B6914", "backgroundColor": "#F5F0E8", "strokeStyle": "solid"},
    },
}

RELATION_STYLES: dict[str, dict[str, Any]] = {
    "supports": {"stroke": "#0B6E6E", "dash": None, "marker": "solid-triangle"},
    "precedes": {"stroke": "#6B7280", "dash": None, "marker": "open-arrow"},
    "triggers": {"stroke": "#1C5BD9", "dash": None, "marker": "solid-arrow"},
    "handoff_to": {"stroke": "#D97706", "dash": "6,4", "marker": "open-arrow"},
    "integrates": {"stroke": "#8B5CF6", "dash": None, "marker": "double-arrow"},
}


# ─── Semantic colors by system category ──────────────────────────
SYSTEM_CATEGORY_COLORS: dict[str, dict[str, Any]] = {
    "frontend": {"svg_fill": "#ECFEFF", "svg_stroke": "#0891B2"},
    "backend": {"svg_fill": "#ECFDF5", "svg_stroke": "#10B981"},
    "database": {"svg_fill": "#F5F3FF", "svg_stroke": "#8B5CF6"},
    "cloud": {"svg_fill": "#FFFBEB", "svg_stroke": "#F59E0B"},
    "security": {"svg_fill": "#FFF1F2", "svg_stroke": "#F43F5E"},
    "external": {"svg_fill": "#F8FAFC", "svg_stroke": "#64748B"},
}

CATEGORY_ALIASES: dict[str, str] = {
    "web": "frontend", "mobile": "frontend", "ui": "frontend",
    "api": "backend", "service": "backend", "microservice": "backend",
    "storage": "database",
    "infra": "cloud", "infrastructure": "cloud", "devops": "cloud",
    "auth": "security",
    "third-party": "external", "third_party": "external", "saas": "external",
}


def _resolve_system_style(category: str | None) -> dict[str, Any] | None:
    """Get semantic colors for a system node by its category."""
    if not category:
        return None
    canonical = CATEGORY_ALIASES.get(category, category)
    colors = SYSTEM_CATEGORY_COLORS.get(canonical)
    if not colors:
        return None
    return {"svg_fill": colors["svg_fill"], "svg_stroke": colors["svg_stroke"]}


# ─── Layout helpers ──────────────────────────────────────────────
def _grid_positions(count: int, cols: int = 3, x_start: int = 40, y_start: int = 40,
                    cell_w: int = 200, cell_h: int = 80, gap: int = 20) -> list[tuple[int, int]]:
    positions: list[tuple[int, int]] = []
    for i in range(count):
        col = i % cols
        row = i // cols
        positions.append((x_start + col * (cell_w + gap), y_start + row * (cell_h + gap)))
    return positions


def _kind_for_entity(entity: dict[str, Any]) -> str:
    kind = entity.get("kind", "")
    if kind:
        return kind
    # Infer from which collection it came from
    if "capabilityIds" in entity and "actorId" not in entity:
        return "system"
    if "actorId" in entity:
        return "flowStep"
    return "capability"


# ─── Node spec builder ───────────────────────────────────────────
def build_node_specs(
    entities: list[dict[str, Any]],
    kind_map: dict[str, str] | None = None,
    cols: int = 3,
    system_categories: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Return a list of node specs with positions and styles.

    Args:
        entities: List of entity dicts with 'id' and 'name'.
        kind_map: Optional mapping from entity id to kind.
        cols: Number of grid columns.
        system_categories: Optional mapping from system id to category string.
    """
    positions = _grid_positions(len(entities), cols=cols)
    specs: list[dict[str, Any]] = []
    for idx, entity in enumerate(entities):
        kind = kind_map.get(entity["id"], _kind_for_entity(entity)) if kind_map else _kind_for_entity(entity)
        style = NODE_STYLES.get(kind, NODE_STYLES["capability"])

        # Apply semantic colors for system nodes with a category
        if kind == "system" and system_categories and entity["id"] in system_categories:
            semantic = _resolve_system_style(system_categories[entity["id"]])
            if semantic:
                svg_style = style["svg"].copy()
                svg_style["fill"] = semantic["svg_fill"]
                svg_style["stroke"] = semantic["svg_stroke"]
                style = dict(style)
                style["svg"] = svg_style

        x, y = positions[idx]
        specs.append({
            "id": entity["id"],
            "label": entity.get("name", entity.get("id", "")),
            "kind": kind,
            "x": x,
            "y": y,
            "width": 200,
            "height": 64,
            "style": style,
        })
    return specs


# ─── Relation spec builder ───────────────────────────────────────
def build_relation_specs(
    relations: list[dict[str, Any]],
    node_ids: set[str],
) -> list[dict[str, Any]]:
    """Build relation specs from canonical relations array."""
    specs: list[dict[str, Any]] = []
    for rel in relations:
        rel_type = rel.get("type", "supports")
        style = RELATION_STYLES.get(rel_type, RELATION_STYLES["supports"])
        source = rel.get("sourceId", rel.get("source", ""))
        target = rel.get("targetId", rel.get("target", ""))
        if source in node_ids and target in node_ids:
            specs.append({
                "id": rel.get("id", f"rel-{source}-{target}"),
                "type": rel_type,
                "sourceId": source,
                "targetId": target,
                "label": rel.get("label", ""),
                "style": style,
            })
    return specs


# ─── Implicit relation builder (from capabilityIds backlinks) ────
def build_implicit_relations(
    systems: list[dict[str, Any]],
    flow_steps: list[dict[str, Any]],
    node_ids: set[str],
) -> list[dict[str, Any]]:
    """Create implicit 'supports' relations from capabilityIds backlinks."""
    rels: list[dict[str, Any]] = []
    for system in systems:
        for cap_id in system.get("capabilityIds", []):
            if system["id"] in node_ids and cap_id in node_ids:
                rels.append({
                    "id": f"rel-{system['id']}-{cap_id}",
                    "type": "supports",
                    "sourceId": system["id"],
                    "targetId": cap_id,
                    "label": "",
                    "style": RELATION_STYLES["supports"],
                })
    for step in flow_steps:
        actor_id = step.get("actorId", "")
        if actor_id and actor_id in node_ids and step["id"] in node_ids:
            rels.append({
                "id": f"rel-{actor_id}-{step['id']}",
                "type": "precedes",
                "sourceId": actor_id,
                "targetId": step["id"],
                "label": "",
                "style": RELATION_STYLES["precedes"],
            })
    for step in flow_steps:
        for cap_id in step.get("capabilityIds", []):
            if step["id"] in node_ids and cap_id in node_ids:
                rels.append({
                    "id": f"rel-{step['id']}-{cap_id}",
                    "type": "triggers",
                    "sourceId": step["id"],
                    "targetId": cap_id,
                    "label": "",
                    "style": RELATION_STYLES["triggers"],
                })
    return rels


# ─── SVG spec builder ────────────────────────────────────────────
def build_svg_spec(blueprint: dict[str, Any]) -> dict[str, Any]:
    library = blueprint.get("library", {})
    capabilities = library.get("capabilities", [])
    systems = library.get("systems", [])
    actors = library.get("actors", [])
    flow_steps = library.get("flowSteps", [])

    all_nodes = []
    kind_map: dict[str, str] = {}
    for c in capabilities:
        all_nodes.append(c)
        kind_map[c["id"]] = "capability"
    for s in systems:
        all_nodes.append(s)
        kind_map[s["id"]] = "system"
    for a in actors:
        all_nodes.append(a)
        kind_map[a["id"]] = "actor"
    for f in flow_steps:
        all_nodes.append(f)
        kind_map[f["id"]] = "flowStep"

    node_specs = build_node_specs(all_nodes, kind_map=kind_map, cols=3)
    node_ids = {n["id"] for n in node_specs}

    explicit_rels = build_relation_specs(blueprint.get("relations", []), node_ids)
    implicit_rels = build_implicit_relations(systems, flow_steps, node_ids)
    all_rels = explicit_rels + implicit_rels

    max_y = max((n["y"] + n["height"] for n in node_specs), default=200)
    width = max(900, max((n["x"] + n["width"] for n in node_specs), default=900) + 40)
    height = max_y + 60

    return {
        "nodes": node_specs,
        "relations": all_rels,
        "width": width,
        "height": height,
    }


def render_svg(svg_spec: dict[str, Any]) -> str:
    rows = ""
    for node in svg_spec["nodes"]:
        style = node["style"]["svg"]
        tag = style["tag"]
        label = escape(node["label"])
        if tag == "rect":
            rx = style.get("rx", 0)
            ry = style.get("ry", 0)
            fill = style.get("fill", "#fff")
            stroke = style.get("stroke", "#333")
            sw = style.get("stroke_width", 1)
            rows += (
                f'<rect x="{node["x"]}" y="{node["y"]}" width="{node["width"]}" height="{node["height"]}" '
                f'rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            )
            rows += (
                f'<text x="{node["x"] + 12}" y="{node["y"] + node["height"] // 2 + 5}" '
                f'font-size="13" fill="#18212F" font-family="system-ui">{label}</text>'
            )
        elif tag == "ellipse":
            fill = style.get("fill", "#fff")
            stroke = style.get("stroke", "#333")
            sw = style.get("stroke_width", 1)
            cx = node["x"] + node["width"] // 2
            cy = node["y"] + node["height"] // 2
            rows += (
                f'<ellipse cx="{cx}" cy="{cy}" rx="{node["width"] // 2}" ry="{node["height"] // 2}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            )
            rows += (
                f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" '
                f'font-size="13" fill="#18212F" font-family="system-ui">{label}</text>'
            )
        elif tag == "polygon":
            fill = style.get("fill", "#fff")
            stroke = style.get("stroke", "#333")
            sw = style.get("stroke_width", 1)
            pts = _diamond_points(node)
            rows += f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            rows += (
                f'<text x="{node["x"] + node["width"] // 2}" y="{node["y"] + node["height"] // 2 + 5}" '
                f'text-anchor="middle" font-size="12" fill="#18212F" font-family="system-ui">{label}</text>'
            )

    for rel in svg_spec["relations"]:
        rows += _render_svg_relation(rel, svg_spec["nodes"])

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_spec["width"]}" '
        f'height="{svg_spec["height"]}">{rows}</svg>'
    )


def _diamond_points(node: dict[str, Any]) -> str:
    cx = node["x"] + node["width"] // 2
    cy = node["y"] + node["height"] // 2
    w2 = node["width"] // 2
    h2 = node["height"] // 2
    return f"{cx},{cy - h2} {cx + w2},{cy} {cx},{cy + h2} {cx - w2},{cy}"


def _render_svg_relation(rel: dict[str, Any], nodes: list[dict[str, Any]]) -> str:
    source = next((n for n in nodes if n["id"] == rel["sourceId"]), None)
    target = next((n for n in nodes if n["id"] == rel["targetId"]), None)
    if not source or not target:
        return ""
    x1 = source["x"] + source["width"] // 2
    y1 = source["y"] + source["height"]
    x2 = target["x"] + target["width"] // 2
    y2 = target["y"]
    stroke = rel["style"]["stroke"]
    dash = rel["style"].get("dash")
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{stroke}" stroke-width="1.5"{dash_attr}/>'
    )


# ─── draw.io spec builder ────────────────────────────────────────
def build_drawio_spec(blueprint: dict[str, Any]) -> dict[str, Any]:
    library = blueprint.get("library", {})
    capabilities = library.get("capabilities", [])
    systems = library.get("systems", [])
    actors = library.get("actors", [])
    flow_steps = library.get("flowSteps", [])

    all_nodes = []
    kind_map: dict[str, str] = {}
    for c in capabilities:
        all_nodes.append(c)
        kind_map[c["id"]] = "capability"
    for s in systems:
        all_nodes.append(s)
        kind_map[s["id"]] = "system"
    for a in actors:
        all_nodes.append(a)
        kind_map[a["id"]] = "actor"
    for f in flow_steps:
        all_nodes.append(f)
        kind_map[f["id"]] = "flowStep"

    node_specs = build_node_specs(all_nodes, kind_map=kind_map, cols=3)
    node_ids = {n["id"] for n in node_specs}

    explicit_rels = build_relation_specs(blueprint.get("relations", []), node_ids)
    implicit_rels = build_implicit_relations(systems, flow_steps, node_ids)

    return {
        "nodes": node_specs,
        "relations": explicit_rels + implicit_rels,
    }


def render_drawio(drawio_spec: dict[str, Any]) -> str:
    cells = ""
    for idx, node in enumerate(drawio_spec["nodes"], start=1):
        style = node["style"]
        shape = style["drawio_shape"]
        label = escape(node["label"])
        cells += (
            f'<mxCell id="node-{node["id"]}" value="{label}" style="shape={shape};" vertex="1" parent="1">'
            f'<mxGeometry x="{node["x"]}" y="{node["y"]}" width="{node["width"]}" height="{node["height"]}" as="geometry"/>'
            f'</mxCell>'
        )

    for rel in drawio_spec["relations"]:
        source = f'node-{rel["sourceId"]}'
        target = f'node-{rel["targetId"]}'
        label = escape(rel.get("label", ""))
        cells += (
            f'<mxCell id="rel-{rel["id"]}" value="{label}" edge="1" source="{source}" target="{target}" parent="1">'
            f'<mxGeometry relative="1" as="geometry"/>'
            f'</mxCell>'
        )

    return (
        '<mxfile host="app.diagrams.net"><diagram name="Blueprint"><mxGraphModel>'
        f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>{cells}</root>'
        '</mxGraphModel></diagram></mxfile>'
    )


# ─── Excalidraw spec builder ─────────────────────────────────────
def build_excalidraw_spec(blueprint: dict[str, Any]) -> dict[str, Any]:
    library = blueprint.get("library", {})
    capabilities = library.get("capabilities", [])
    systems = library.get("systems", [])
    actors = library.get("actors", [])
    flow_steps = library.get("flowSteps", [])

    all_nodes = []
    kind_map: dict[str, str] = {}
    for c in capabilities:
        all_nodes.append(c)
        kind_map[c["id"]] = "capability"
    for s in systems:
        all_nodes.append(s)
        kind_map[s["id"]] = "system"
    for a in actors:
        all_nodes.append(a)
        kind_map[a["id"]] = "actor"
    for f in flow_steps:
        all_nodes.append(f)
        kind_map[f["id"]] = "flowStep"

    node_specs = build_node_specs(all_nodes, kind_map=kind_map, cols=3)

    return {"nodes": node_specs}


def render_excalidraw(exc_spec: dict[str, Any]) -> str:
    import json
    elements = []
    for idx, node in enumerate(exc_spec["nodes"]):
        style = node["style"]["excalidraw"]
        elem = {
            "id": node["id"],
            "type": style["type"],
            "x": node["x"],
            "y": node["y"],
            "width": node["width"],
            "height": node["height"],
            "strokeColor": style["strokeColor"],
            "backgroundColor": style["backgroundColor"],
            "fillStyle": style.get("strokeStyle", "solid"),
            "seed": idx + 1,
            "version": 1,
            "versionNonce": idx + 10,
            "isDeleted": False,
            "boundElements": None,
        }
        elements.append(elem)
        # Text label
        elements.append({
            "id": f"text-{node['id']}",
            "type": "text",
            "x": node["x"] + 12,
            "y": node["y"] + node["height"] // 2 + 4,
            "width": node["width"] - 24,
            "height": 20,
            "fontSize": 14,
            "fontFamily": 1,
            "text": node["label"],
            "textAlign": "left",
            "verticalAlign": "top",
            "strokeColor": "#18212F",
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "seed": idx + 100,
            "version": 1,
            "versionNonce": idx + 110,
            "isDeleted": False,
        })

    payload = {
        "type": "excalidraw",
        "version": 2,
        "source": "business-blueprint-skill",
        "elements": elements,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
