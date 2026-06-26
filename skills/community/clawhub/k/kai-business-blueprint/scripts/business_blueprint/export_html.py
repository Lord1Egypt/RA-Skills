"""Generate self-contained HTML viewer with inline architecture SVG.

Uses template file from business_blueprint/templates/html-viewer.html.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from export_svg import FONT, FONT_MONO, _resolve_theme


_TEMPLATE_PATH = Path(__file__).parent / "templates" / "html-viewer.html"


def _get_skill_version() -> str:
    """Read skill version from pyproject.toml (source of truth over installed package)."""
    try:
        toml_path = Path(__file__).parent.parent / "pyproject.toml"
        text = toml_path.read_text()
        for line in text.splitlines():
            if line.startswith("version "):
                return line.split('"')[1]
    except Exception:
        pass
    import importlib.metadata
    try:
        return importlib.metadata.version("business-blueprint-skill")
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


_SKILL_VERSION = _get_skill_version()


def _esc(s: str) -> str:
    return escape(str(s))


def _build_architecture_svg(blueprint: dict[str, Any], colors: dict, theme: str) -> str:
    """Build architecture SVG for the HTML viewer.

    Uses free-flow L→R data flow layout by default.
    When no standard export template applies, viewer output must stay on
    freeflow rather than silently switching to another generic view type.
    """
    import tempfile
    from export_svg import export_svg_auto

    industry = blueprint.get("meta", {}).get("industry", "") or None
    with tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as f:
        tmp_path = Path(f.name)
    export_svg_auto(blueprint, tmp_path, theme=theme, industry=industry)
    result = tmp_path.read_text(encoding="utf-8")
    tmp_path.unlink()
    return result


def _build_summary_cards(n_systems: int, n_capabilities: int,
                          n_actors: int, n_flow_steps: int,
                          sys_coverage: str) -> str:
    """Build summary cards HTML for architecture blueprints."""
    cards = [
        ("Systems", str(n_systems)),
        ("Capabilities", str(n_capabilities)),
        ("Actors", str(n_actors)),
        ("Flow Steps", str(n_flow_steps)),
        ("Sys Coverage", sys_coverage),
    ]
    cards_html = ""
    for label, value in cards:
        cards_html += f"""
        <div class="summary-card">
            <div class="card-value">{value}</div>
            <div class="card-label">{label}</div>
        </div>"""
    return f'<div class="summary-cards">{cards_html}\n    </div>'


def _build_knowledge_summary_cards(blueprint: dict[str, Any]) -> str:
    """Build summary cards HTML for domain-knowledge blueprints."""
    knowledge = (blueprint.get("library", {}) or {}).get("knowledge", {}) or {}
    relations = blueprint.get("relations", []) or []
    clarify_requests = (blueprint.get("context", {}) or {}).get("clarifyRequests", []) or []

    def _count(key: str) -> int:
        items = knowledge.get(key, [])
        return len(items) if isinstance(items, list) else 0

    # Count entities flagged with non-empty self-check questions
    flagged = 0
    for entities in knowledge.values():
        if not isinstance(entities, list):
            continue
        for ent in entities:
            if not isinstance(ent, dict):
                continue
            sc = ent.get("_selfCheck") or {}
            qs = sc.get("questions") if isinstance(sc, dict) else None
            if isinstance(qs, list) and qs:
                flagged += 1

    cards = [
        ("痛点", str(_count("painPoints"))),
        ("策略", str(_count("strategies"))),
        ("规则", str(_count("rules"))),
        ("指标", str(_count("metrics"))),
        ("实践", str(_count("practices"))),
        ("误区", str(_count("pitfalls"))),
        ("关系", str(len(relations))),
        ("待澄清", str(len(clarify_requests))),
        ("自检待确认", str(flagged)),
    ]
    cards_html = ""
    for label, value in cards:
        cards_html += f"""
        <div class="summary-card">
            <div class="card-value">{value}</div>
            <div class="card-label">{label}</div>
        </div>"""
    return f'<div class="summary-cards">{cards_html}\n    </div>'


def _build_clarify_section(blueprint: dict[str, Any]) -> str:
    """For knowledge blueprints, list clarifyRequests so the user knows what to verify."""
    requests = (blueprint.get("context", {}) or {}).get("clarifyRequests", []) or []
    if not requests:
        return ""
    items = ""
    for req in requests:
        if not isinstance(req, dict):
            continue
        question = _esc(req.get("question", ""))
        target = _esc(req.get("targetEntityId", ""))
        rationale = _esc(req.get("rationale", ""))
        items += f"""
        <li>
            <div style="font-weight:600;margin-bottom:4px;">→ {target}</div>
            <div style="margin-bottom:4px;">{question}</div>
            <div style="color:#6B7280;font-size:12px;">{rationale}</div>
        </li>"""
    return f"""
    <div class="description-section">
        <h2 class="description-title">待澄清的问题（pitch 前请回答）</h2>
        <ul style="list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:12px;">{items}
        </ul>
    </div>"""


def _build_description_section(blueprint: dict[str, Any]) -> str:
    """Build description cards section from blueprint context."""
    ctx = blueprint.get("context", {})
    goals = ctx.get("goals", [])
    scope = ctx.get("scope", [])
    assumptions = ctx.get("assumptions", [])
    constraints = ctx.get("constraints", [])

    key_decisions = []
    for ref in ctx.get("sourceRefs", []):
        excerpt = ref.get("excerpt", "")
        for line in excerpt.split("\n"):
            stripped = line.strip()
            if stripped.startswith("- ") and ("design" in stripped.lower() or "decision" in stripped.lower()):
                key_decisions.append(stripped[2:].strip())

    card_sections = []
    if goals:
        card_sections.append(("Design Goals", "#F59E0B", goals))
    if scope:
        card_sections.append(("Scope", "#34D399", scope))
    if key_decisions:
        card_sections.append(("Key Decisions", "#A78BFA", key_decisions))
    if assumptions:
        card_sections.append(("Assumptions", "#60A5FA", assumptions))
    if constraints:
        card_sections.append(("Constraints", "#FB923C", constraints))

    if not card_sections:
        return ""

    description_cards = ""
    for sec_title, sec_color, items in card_sections:
        items_html = "".join(f'<li>{_esc(item)}</li>' for item in items)
        description_cards += f"""
        <div class="desc-card">
            <div class="desc-card-title" style="color:{sec_color};">{_esc(sec_title)}</div>
            <ul class="desc-card-list">{items_html}</ul>
        </div>"""

    return f"""
    <div class="description-section">
        <h2 class="description-title">Architecture Description</h2>
        <div class="description-grid">{description_cards}
        </div>
    </div>"""


def export_html_viewer(blueprint: dict[str, Any], target: Path, theme: str = "light") -> None:
    """Generate a self-contained HTML viewer with inline SVG.

    Branches on ``meta.blueprintType``:
    - ``architecture`` (default): standard summary cards (Systems/Capabilities/...)
    - ``domain-knowledge``: knowledge summary cards (痛点/策略/...) + clarifyRequests
    """
    from export_knowledge import is_knowledge_blueprint

    colors = _resolve_theme(theme)
    title = blueprint.get("meta", {}).get("title", "Business Blueprint")
    lib = blueprint.get("library", {})

    svg_content = _build_architecture_svg(blueprint, colors, theme)

    if is_knowledge_blueprint(blueprint):
        summary_cards = _build_knowledge_summary_cards(blueprint)
        description_section = (
            _build_description_section(blueprint)
            + _build_clarify_section(blueprint)
        )
    else:
        n_systems = len(lib.get("systems", []))
        n_capabilities = len(lib.get("capabilities", []))
        n_actors = len(lib.get("actors", []))
        n_flow_steps = len(lib.get("flowSteps", []))
        systems_with_caps = sum(1 for s in lib.get("systems", []) if s.get("capabilityIds"))
        sys_coverage = f"{int(systems_with_caps / n_systems * 100)}%" if n_systems else "N/A"
        summary_cards = _build_summary_cards(
            n_systems, n_capabilities, n_actors, n_flow_steps, sys_coverage
        )
        description_section = _build_description_section(blueprint)

    safe_json = json.dumps(json.dumps(blueprint, ensure_ascii=False)).replace("</", "<\\/")

    header_bg = "#020617" if theme == "dark" else "#0F2742"
    header_text = "#E2E8F0" if theme == "dark" else "#fff"

    dark_extras = ""
    if theme == "dark":
        dark_extras = f"""
        .header {{ background: {header_bg}; color: {header_text}; }}
        .header .meta {{ font-size: 13px; color: #94A3B8; }}
        .summary-cards {{ background: linear-gradient(180deg, {colors["layer_header_bg"]}, {colors["bg"]}); }}
        .summary-card {{ background: {colors["canvas"]}; border-color: {colors["border"]}; }}
        .summary-card .card-value {{ color: {colors["text_main"]}; }}
        .summary-card .card-label {{ color: {colors["text_sub"]}; }}
        body {{ background: linear-gradient(180deg, {colors["bg"]} 0%, #0F172A 100%); }}
        .viewer svg {{ box-shadow: 0 2px 12px rgba(0,0,0,0.4); }}
"""
    else:
        dark_extras = f"""
        .summary-cards {{ background: linear-gradient(180deg, {colors["layer_header_bg"]}, {colors["bg"]}); }}
        .summary-card {{ background: {colors["canvas"]}; border-color: {colors["border"]}; }}
        .summary-card .card-value {{ color: {colors["text_main"]}; }}
        .summary-card .card-label {{ color: {colors["text_sub"]}; }}
"""

    grid_bg = ""
    if theme == "dark":
        grid_bg = '<div style="position:fixed;top:0;left:0;width:100%;height:100%;background-image:linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px);background-size:40px 40px;pointer-events:none;z-index:0;"></div>'

    # Load template and substitute placeholders
    template = _TEMPLATE_PATH.read_text(encoding="utf-8")
    html = template
    html = html.replace("{{TITLE}}", _esc(title))
    html = html.replace("{{FONT}}", FONT)
    html = html.replace("{{FONT_MONO}}", FONT_MONO)
    html = html.replace("{{BG_COLOR}}", colors["bg"])
    html = html.replace("{{TEXT_MAIN}}", colors["text_main"])
    html = html.replace("{{TEXT_SUB}}", colors["text_sub"])
    html = html.replace("{{BORDER}}", colors["border"])
    html = html.replace("{{CAP_STROKE}}", colors["cap_stroke"])
    html = html.replace("{{HEADER_BG}}", header_bg)
    html = html.replace("{{HEADER_TEXT}}", header_text)
    html = html.replace("{{CARD_BG}}", colors["canvas"])
    html = html.replace("{{CARD_BORDER}}", colors["border"])
    html = html.replace("{{DARK_EXTRAS}}", dark_extras)
    html = html.replace("{{GRID_BG}}", grid_bg)
    html = html.replace("{{VERSION}}", _SKILL_VERSION)
    html = html.replace("{{SVG_CONTENT}}", svg_content)
    html = html.replace("{{SUMMARY_CARDS}}", summary_cards)
    html = html.replace("{{DESCRIPTION_SECTION}}", description_section)
    html = html.replace("{{BLUEPRINT_JSON}}", safe_json)

    target.write_text(html, encoding="utf-8")
