"""SVG rendering for domain-knowledge blueprints — pitch-grade layout.

Layout structure
================

    ┌─────────────────────────────────────────────────────────────┐
    │ Title + intent                                              │ TITLE
    ├─────────────────────────────────────────────────────────────┤
    │ ⚖ 平台规则                                                   │
    │ [rule-001] [rule-002] [rule-003] [rule-004]                 │ RULES BAND
    ├─────────────────────────────────────────────────────────────┤
    │ ⚠ 痛点          💡 策略          📊 指标                      │
    │ [pain-001] ━━━ [str-001] ━━━ [met-001]                       │ MAIN
    │ [pain-002] ━━━ [str-002]                                    │ TRIPTYCH
    │ [pain-003] ━━━ [str-005]                                    │
    │ ...                                                         │
    ├─────────────────────────────────────────────────────────────┤
    │ ✅ 最佳实践           │  ❌ 常见误区                          │
    │ [bp-001] [bp-002] ... │  [pit-001] [pit-002] [pit-003] ...   │ BANDS
    └─────────────────────────────────────────────────────────────┘

Key design decisions
====================

1. **Row alignment minimises crossings**:
   strategies are placed in the row of the painPoint they primarily ``solve``;
   metrics are placed in the row of the strategy they primarily ``measure``.
   The dominant ``solves`` / ``measures`` lines become near-horizontal.

2. **Bezier curves, not straight lines**: cross-zone connections (rule→strategy,
   pitfall→painPoint, practice→pitfall, strategy→practice) use cubic Bezier
   so they don't slice across the canvas.

3. **Grouped band backgrounds**: rules / practices / pitfalls each sit in a
   tinted card, so the eye groups them as zones rather than as 19 random nodes.

4. **Self-check questions** still surface as a yellow border + ``?`` badge.

Out of scope (Phase 3): force-directed layout, > 50 entities pagination.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape


# ─── Visual tokens ──────────────────────────────────────────────────────────

KNOWLEDGE_STYLES: dict[str, dict[str, str]] = {
    "painPoint": {"fill": "#FEE2E2", "stroke": "#DC2626", "icon": "⚠", "header": "痛点"},
    "strategy": {"fill": "#D1FAE5", "stroke": "#0B6E6E", "icon": "💡", "header": "策略"},
    "rule":     {"fill": "#FEF3C7", "stroke": "#D97706", "icon": "📋", "header": "平台规则"},
    "metric":   {"fill": "#E0E7FF", "stroke": "#4F46E5", "icon": "📊", "header": "指标"},
    "practice": {"fill": "#DCFCE7", "stroke": "#10B981", "icon": "✅", "header": "最佳实践"},
    "pitfall":  {"fill": "#FEF3C7", "stroke": "#F59E0B", "icon": "❌", "header": "常见误区"},
}

DEFAULT_STYLE = {"fill": "#F3F4F6", "stroke": "#6B7280", "icon": "📦", "header": "其他"}

# Two-tier relation rendering:
#   - "primary" relations carry the main story (solves / measures). Slightly
#     stronger but still very light, no label by default — the row alignment
#     already encodes "this strategy solves that pain", so the line is just
#     visual confirmation.
#   - "secondary" relations are supporting context (requires, prevents,
#     enforces, causes, …). Drawn at very low opacity so they don't fight
#     the main story. Labels are tooltip-only.
RELATION_STYLES: dict[str, dict[str, str]] = {
    "solves":     {"color": "#0B6E6E", "dash": "",    "label": "解决",   "tier": "primary"},
    "measures":   {"color": "#4F46E5", "dash": "",    "label": "衡量",   "tier": "primary"},
    "prevents":   {"color": "#10B981", "dash": "4,4", "label": "规避",   "tier": "secondary"},
    "enforces":   {"color": "#D97706", "dash": "6,4", "label": "约束",   "tier": "secondary"},
    "requires":   {"color": "#94A3B8", "dash": "3,4", "label": "依赖",   "tier": "tertiary"},
    "causes":     {"color": "#DC2626", "dash": "",    "label": "导致",   "tier": "secondary"},
    "impacts":    {"color": "#F59E0B", "dash": "4,4", "label": "影响",   "tier": "secondary"},
    "supports":   {"color": "#10B981", "dash": "",    "label": "支撑",   "tier": "secondary"},
    "enforcedBy": {"color": "#D97706", "dash": "6,4", "label": "受约束", "tier": "secondary"},
    "measuredBy": {"color": "#4F46E5", "dash": "4,4", "label": "受监控", "tier": "secondary"},
}

# Per-tier render parameters
TIER_RENDER = {
    "primary":   {"width": 1.4, "opacity": 0.55, "show_label": False},
    "secondary": {"width": 1.0, "opacity": 0.32, "show_label": False},
    "tertiary":  {"width": 0.8, "opacity": 0.22, "show_label": False},
}


# ─── Layout constants ───────────────────────────────────────────────────────

PAGE_W = 1280
PAD = 56
TITLE_H = 90
RULES_BAND_H = 140
MAIN_HEADER_H = 36
ROW_H = 78
PRACT_BAND_H = 0      # computed dynamically based on wrap
PITF_BAND_H = 0
BAND_GAP_V = 28

NODE_W = 200
NODE_H = 60
COL_GAP = 90
NODE_RX = 10

BAND_NODE_W = 168
BAND_NODE_H = 54
BAND_NODE_GAP = 14
BAND_INNER_PAD = 18


SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}


# ─── Helpers ────────────────────────────────────────────────────────────────

def _esc(s: Any) -> str:
    return escape(str(s)) if s is not None else ""


def _has_self_check_questions(entity: dict[str, Any]) -> bool:
    sc = entity.get("_selfCheck")
    if not isinstance(sc, dict):
        return False
    qs = sc.get("questions", [])
    return isinstance(qs, list) and len(qs) > 0


def _self_check_tooltip(entity: dict[str, Any]) -> str:
    sc = entity.get("_selfCheck") or {}
    qs = sc.get("questions", []) if isinstance(sc, dict) else []
    if not qs:
        return ""
    body = "&#10;".join(f"• {_esc(q)}" for q in qs)
    return f"未确认的自检项：&#10;{body}"


def _wrap_text(text: str, max_chars: int = 14) -> list[str]:
    if not text:
        return [""]
    out: list[str] = []
    line = ""
    for ch in text:
        if len(line) >= max_chars:
            out.append(line)
            line = ""
        line += ch
    if line:
        out.append(line)
    return out[:2]


# ─── Node rendering ─────────────────────────────────────────────────────────

def _render_node(
    entity: dict[str, Any],
    x: float,
    y: float,
    *,
    width: float = NODE_W,
    height: float = NODE_H,
) -> str:
    """Render a knowledge entity card.

    Per-entity icons are intentionally NOT drawn — the entity's category is
    already signalled by:
      - colour (border + tinted fill)
      - position (column header / band card title carries the icon once)
    Repeating the same icon on every node within a category causes visual
    noise without adding information. Instead, the left edge gets a thin
    accent strip in the entity's brand colour to reinforce categorisation.
    """
    entity_type = entity.get("entityType", "")
    style = KNOWLEDGE_STYLES.get(entity_type, DEFAULT_STYLE)
    has_questions = _has_self_check_questions(entity)

    border_color = "#F59E0B" if has_questions else style["stroke"]
    border_width = 2.4 if has_questions else 1.2

    name = entity.get("name", "")
    # More text room now that the icon is gone — increase per-line capacity
    max_chars = 16 if width < 180 else 18
    lines = _wrap_text(name, max_chars=max_chars)

    eid = _esc(entity.get("id", ""))
    parts = [
        f'<g class="kg-node kg-{entity_type}" id="{eid}">',
        # Drop shadow for depth
        f'<rect x="{x + 1.5}" y="{y + 2.5}" width="{width}" height="{height}" '
        f'rx="{NODE_RX}" ry="{NODE_RX}" fill="rgba(15,23,42,0.06)"/>',
        # Card body
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'rx="{NODE_RX}" ry="{NODE_RX}" fill="{style["fill"]}" '
        f'stroke="{border_color}" stroke-width="{border_width}"/>',
        # Subtle left accent strip (3px) tinted with the category colour —
        # silent category cue without the icon repetition.
        f'<rect x="{x}" y="{y + 4}" width="3" height="{height - 8}" '
        f'rx="1.5" ry="1.5" fill="{style["stroke"]}" fill-opacity="0.55"/>',
    ]

    text_x = x + 14
    if len(lines) == 1:
        parts.append(
            f'<text x="{text_x}" y="{y + height / 2 + 5}" font-size="13" '
            f'font-family="system-ui, sans-serif" fill="#0F172A" '
            f'font-weight="600">{_esc(lines[0])}</text>'
        )
    else:
        parts.append(
            f'<text x="{text_x}" y="{y + height / 2 - 4}" font-size="13" '
            f'font-family="system-ui, sans-serif" fill="#0F172A" '
            f'font-weight="600">{_esc(lines[0])}</text>'
        )
        parts.append(
            f'<text x="{text_x}" y="{y + height / 2 + 14}" font-size="13" '
            f'font-family="system-ui, sans-serif" fill="#0F172A" '
            f'font-weight="600">{_esc(lines[1])}</text>'
        )

    severity = entity.get("severity")
    if isinstance(severity, str) and severity:
        sev_color = {
            "critical": "#DC2626", "high": "#EA580C",
            "medium": "#D97706", "low": "#65A30D",
        }.get(severity, "#6B7280")
        parts.append(
            f'<text x="{x + width - 8}" y="{y + 14}" font-size="9" '
            f'text-anchor="end" fill="{sev_color}" font-weight="700" '
            f'font-family="system-ui, sans-serif">{_esc(severity.upper())}</text>'
        )

    if has_questions:
        # Minimal badge: a soft amber "?" glyph, no white circle, no border.
        # The yellow border on the card already signals "needs review";
        # the glyph is just a redundancy cue at the corner.
        bx = x + width - 11
        by = y + height - 8
        tooltip = _self_check_tooltip(entity)
        parts.append(
            f'<g class="kg-selfcheck-badge">'
            f'<text x="{bx}" y="{by}" text-anchor="middle" '
            f'font-size="13" font-weight="700" fill="#F59E0B" '
            f'fill-opacity="0.85" font-family="system-ui, sans-serif">?</text>'
            f'<title>{_esc(tooltip)}</title>'
            f'</g>'
        )

    parts.append("</g>")
    return "".join(parts)


# ─── Relation rendering ─────────────────────────────────────────────────────

def _bezier_path(x1: float, y1: float, x2: float, y2: float) -> str:
    """Cubic Bezier between two points. Control points biased horizontally for
    horizontal flows and vertically for vertical flows.
    """
    dx = x2 - x1
    dy = y2 - y1
    # Mostly horizontal flow → bend horizontally
    if abs(dx) >= abs(dy):
        cx_offset = max(40.0, abs(dx) * 0.4)
        c1x = x1 + (cx_offset if dx >= 0 else -cx_offset)
        c1y = y1
        c2x = x2 - (cx_offset if dx >= 0 else -cx_offset)
        c2y = y2
    else:
        cy_offset = max(40.0, abs(dy) * 0.4)
        c1x = x1
        c1y = y1 + (cy_offset if dy >= 0 else -cy_offset)
        c2x = x2
        c2y = y2 - (cy_offset if dy >= 0 else -cy_offset)
    return f"M {x1} {y1} C {c1x} {c1y}, {c2x} {c2y}, {x2} {y2}"


def _connection_anchors(
    a: tuple[float, float, float, float],
    b: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    """Pick edges on each rect that minimise distance.

    Each rect is (x, y, w, h); returns (x1, y1, x2, y2).
    """
    ax, ay, aw, ah = a
    bx, by, bw, bh = b

    a_centers = {
        "right":  (ax + aw, ay + ah / 2),
        "left":   (ax,      ay + ah / 2),
        "top":    (ax + aw / 2, ay),
        "bottom": (ax + aw / 2, ay + ah),
    }
    b_centers = {
        "right":  (bx + bw, by + bh / 2),
        "left":   (bx,      by + bh / 2),
        "top":    (bx + bw / 2, by),
        "bottom": (bx + bw / 2, by + bh),
    }

    best = None
    best_d = float("inf")
    for ak, ap in a_centers.items():
        for bk, bp in b_centers.items():
            # Prefer "outgoing then incoming" pairings that look sensible
            d = (ap[0] - bp[0]) ** 2 + (ap[1] - bp[1]) ** 2
            # Penalise pairs that fold back
            if ak == "right" and bk == "right" and bp[0] > ap[0]:
                d *= 1.4
            if ak == "left" and bk == "left" and bp[0] < ap[0]:
                d *= 1.4
            if d < best_d:
                best_d = d
                best = (*ap, *bp)
    assert best is not None
    return best  # type: ignore[return-value]


def _render_relation(
    rel: dict[str, Any],
    rects: dict[str, tuple[float, float, float, float]],
) -> str:
    from_id = rel.get("from")
    to_id = rel.get("to")
    if not isinstance(from_id, str) or not isinstance(to_id, str):
        return ""
    if from_id not in rects or to_id not in rects:
        return ""

    rel_type = rel.get("type", "")
    style = RELATION_STYLES.get(
        rel_type,
        {"color": "#94A3B8", "dash": "3,4", "label": rel_type or "", "tier": "tertiary"},
    )
    tier = TIER_RENDER.get(style.get("tier", "secondary"), TIER_RENDER["secondary"])

    x1, y1, x2, y2 = _connection_anchors(rects[from_id], rects[to_id])
    path = _bezier_path(x1, y1, x2, y2)

    dash_attr = f' stroke-dasharray="{style["dash"]}"' if style["dash"] else ""
    # ``<title>`` provides hover tooltip for label-less primary lines.
    label = style["label"]
    title_text = f"{label}：{from_id} → {to_id}" if label else f"{from_id} → {to_id}"

    line = (
        f'<g class="kg-rel kg-rel-{style.get("tier", "secondary")}">'
        f'<path d="{path}" fill="none" stroke="{style["color"]}" '
        f'stroke-width="{tier["width"]}"{dash_attr} '
        f'stroke-opacity="{tier["opacity"]}" stroke-linecap="round" '
        f'marker-end="url(#kg-arrow-{rel_type or "default"})"/>'
        f'<title>{_esc(title_text)}</title>'
        f'</g>'
    )

    # Label suppressed by default — tier dictates visibility. Row alignment
    # (strategies aligned to their solved painPoint, metrics aligned to their
    # measured strategy) makes the meaning self-evident.
    if not tier.get("show_label"):
        return line

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2 - 4
    text_w = max(28, len(label) * 11)
    label_svg = (
        f'<g class="kg-rel-label">'
        f'<rect x="{mx - text_w / 2}" y="{my - 11}" width="{text_w}" '
        f'height="16" rx="3" fill="#FFFFFF" fill-opacity="0.92" '
        f'stroke="{style["color"]}" stroke-width="0.6" stroke-opacity="0.5"/>'
        f'<text x="{mx}" y="{my + 1}" font-size="10" '
        f'text-anchor="middle" fill="{style["color"]}" '
        f'font-family="system-ui, sans-serif" font-weight="600">'
        f'{_esc(label)}</text>'
        f'</g>'
    )
    return line + label_svg


def _arrow_markers() -> str:
    parts = ['<defs>']
    for rel_type, style in RELATION_STYLES.items():
        tier = TIER_RENDER.get(style.get("tier", "secondary"), TIER_RENDER["secondary"])
        parts.append(
            f'<marker id="kg-arrow-{rel_type}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{style["color"]}" '
            f'fill-opacity="{tier["opacity"] + 0.15:.2f}"/></marker>'
        )
    parts.append(
        '<marker id="kg-arrow-default" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#94A3B8" fill-opacity="0.45"/></marker>'
    )
    parts.append('</defs>')
    return "".join(parts)


# ─── Layout: row alignment for the main triptych ────────────────────────────

def _sort_painpoints(pp: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        pp,
        key=lambda p: (
            SEVERITY_ORDER.get(p.get("severity", "low"), 4),
            p.get("level", 9),
            p.get("id", ""),
        ),
    )


def _align_main(
    painpoints: list[dict[str, Any]],
    strategies: list[dict[str, Any]],
    metrics: list[dict[str, Any]],
    relations: list[dict[str, Any]],
) -> tuple[
    list[tuple[int, dict[str, Any]]],   # (row, painpoint)
    list[tuple[int, dict[str, Any]]],   # (row, strategy)
    list[tuple[int, dict[str, Any]]],   # (row, metric)
    int,                                # total rows
]:
    sorted_pp = _sort_painpoints(painpoints)
    pain_row = {p["id"]: i for i, p in enumerate(sorted_pp)}

    # solves: strategy → painPoint
    str_to_pain: dict[str, list[str]] = {}
    for r in relations:
        if isinstance(r, dict) and r.get("type") == "solves":
            f, t = r.get("from"), r.get("to")
            if isinstance(f, str) and isinstance(t, str):
                str_to_pain.setdefault(f, []).append(t)

    # measures: metric → strategy
    met_to_str: dict[str, list[str]] = {}
    for r in relations:
        if isinstance(r, dict) and r.get("type") == "measures":
            f, t = r.get("from"), r.get("to")
            if isinstance(f, str) and isinstance(t, str):
                met_to_str.setdefault(f, []).append(t)

    # Strategies: anchor each to its primary solved painPoint
    pp_layout = [(i, p) for i, p in enumerate(sorted_pp)]

    str_used: set[str] = set()
    str_row: dict[str, int] = {}
    rows_with_str: set[int] = set()
    # First pass: each painPoint row tries to claim its primary strategy
    for row, p in pp_layout:
        for s in strategies:
            sid = s.get("id")
            if not isinstance(sid, str) or sid in str_used:
                continue
            if p["id"] in str_to_pain.get(sid, []):
                str_row[sid] = row
                str_used.add(sid)
                rows_with_str.add(row)
                break

    # Remaining strategies: fill empty rows first (compress vertical whitespace)
    pp_rows = {row for row, _ in pp_layout}
    empty_pp_rows = sorted(pp_rows - rows_with_str)
    next_free = max(pp_rows, default=-1) + 1
    for s in strategies:
        sid = s.get("id")
        if not isinstance(sid, str) or sid in str_used:
            continue
        if empty_pp_rows:
            row = empty_pp_rows.pop(0)
        else:
            row = next_free
            next_free += 1
        str_row[sid] = row
        str_used.add(sid)

    str_layout = [(str_row[s["id"]], s) for s in strategies if s.get("id") in str_row]

    # Metrics: anchor each to its primary measured strategy's row
    met_used: set[str] = set()
    met_row: dict[str, int] = {}
    rows_with_met: set[int] = set()
    # Walk strategies in row order so claims are deterministic
    for sid, srow in sorted(str_row.items(), key=lambda kv: kv[1]):
        for m in metrics:
            mid = m.get("id")
            if not isinstance(mid, str) or mid in met_used:
                continue
            if sid in met_to_str.get(mid, []) and srow not in rows_with_met:
                met_row[mid] = srow
                met_used.add(mid)
                rows_with_met.add(srow)
                break

    # Remaining metrics: fill empty rows (any row in [0, max_row] without a metric)
    str_rows_set = set(str_row.values())
    all_rows_so_far = pp_rows | str_rows_set
    empty_met_rows = sorted(all_rows_so_far - rows_with_met)
    next_free_m = max(all_rows_so_far, default=-1) + 1
    for m in metrics:
        mid = m.get("id")
        if not isinstance(mid, str) or mid in met_used:
            continue
        if empty_met_rows:
            row = empty_met_rows.pop(0)
        else:
            row = next_free_m
            next_free_m += 1
        met_row[mid] = row
        met_used.add(mid)

    met_layout = [(met_row[m["id"]], m) for m in metrics if m.get("id") in met_row]

    total_rows = max(
        [row for row, _ in pp_layout]
        + [row for row, _ in str_layout]
        + [row for row, _ in met_layout]
        + [-1],
    ) + 1
    return pp_layout, str_layout, met_layout, total_rows


# ─── Layout: bands ──────────────────────────────────────────────────────────

def _wrap_band(
    entities: list[dict[str, Any]],
    x_start: float,
    y_start: float,
    band_width: float,
    inner_pad: float = BAND_INNER_PAD,
) -> tuple[dict[str, tuple[float, float, float, float]], float]:
    """Place band entities in a wrapped grid. Returns (rects, band_height)."""
    rects: dict[str, tuple[float, float, float, float]] = {}
    if not entities:
        return rects, BAND_NODE_H + 2 * inner_pad

    avail = band_width - 2 * inner_pad
    cols = max(1, int((avail + BAND_NODE_GAP) // (BAND_NODE_W + BAND_NODE_GAP)))
    cur_col = 0
    cur_row = 0
    for ent in entities:
        ent_id = ent.get("id")
        if not isinstance(ent_id, str):
            continue
        x = x_start + inner_pad + cur_col * (BAND_NODE_W + BAND_NODE_GAP)
        y = y_start + inner_pad + cur_row * (BAND_NODE_H + BAND_NODE_GAP)
        rects[ent_id] = (x, y, BAND_NODE_W, BAND_NODE_H)
        cur_col += 1
        if cur_col >= cols:
            cur_col = 0
            cur_row += 1
    band_h = (cur_row + (1 if cur_col == 0 else 1)) * BAND_NODE_H + \
             cur_row * BAND_NODE_GAP + 2 * inner_pad
    return rects, band_h


def _capsule_path(x: float, y: float, w: float, h: float, r: float = 12) -> str:
    """Capsule shape: flat left edge, rounded right corners.

    Mirrors the slide-creator / report-creator convention
    ``border-radius: 0 r r 0`` for cards with a left-edge accent bar.
    Returns an SVG path ``d`` attribute value.
    """
    return (
        f"M {x} {y} "
        f"L {x + w - r} {y} "
        f"Q {x + w} {y} {x + w} {y + r} "
        f"L {x + w} {y + h - r} "
        f"Q {x + w} {y + h} {x + w - r} {y + h} "
        f"L {x} {y + h} Z"
    )


def _band_card(
    x: float, y: float, w: float, h: float,
    title: str, accent: str, fill: str,
) -> str:
    """Capsule card with a flush left-edge accent bar.

    Layout: a left accent strip (flat rect, accent colour) sits seamlessly
    against a tinted body whose right corners are rounded. No visible seam
    because the body starts where the accent ends and they share the same
    flat top/bottom edges.
    """
    bar_w = 4.0
    body_x = x + bar_w
    body_w = w - bar_w
    body_path = _capsule_path(body_x, y, body_w, h, r=12)

    return (
        # Body (right corners rounded, left flat)
        f'<path d="{body_path}" fill="{fill}" fill-opacity="0.5" '
        f'stroke="{accent}" stroke-width="1" stroke-opacity="0.35"/>'
        # Accent bar (flush against the flat left edge of the body)
        f'<rect x="{x}" y="{y}" width="{bar_w}" height="{h}" fill="{accent}"/>'
        # Title sits inside the body
        f'<text x="{body_x + 12}" y="{y + 22}" font-size="13" font-weight="700" '
        f'fill="{accent}" font-family="system-ui, sans-serif">{_esc(title)}</text>'
    )


# ─── Top-level renderer ─────────────────────────────────────────────────────

def render_knowledge_svg(blueprint: dict[str, Any]) -> str:
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}
    relations = blueprint.get("relations", []) or []
    meta = blueprint.get("meta", {}) or {}

    pp = [e for e in (knowledge.get("painPoints") or []) if isinstance(e, dict)]
    st = [e for e in (knowledge.get("strategies") or []) if isinstance(e, dict)]
    rl = [e for e in (knowledge.get("rules") or []) if isinstance(e, dict)]
    mt = [e for e in (knowledge.get("metrics") or []) if isinstance(e, dict)]
    pr = [e for e in (knowledge.get("practices") or []) if isinstance(e, dict)]
    pf = [e for e in (knowledge.get("pitfalls") or []) if isinstance(e, dict)]
    # User-defined entity-type arrays (anything not in the 6 standard buckets)
    standard_keys = {"painPoints", "strategies", "rules", "metrics", "practices", "pitfalls"}
    extras: list[dict[str, Any]] = []
    for k, v in knowledge.items():
        if k in standard_keys or not isinstance(v, list):
            continue
        extras.extend(e for e in v if isinstance(e, dict))

    rects: dict[str, tuple[float, float, float, float]] = {}

    # ─── Geometry calculation ───
    # The page width is fixed (PAGE_W) so the layout looks consistent across
    # blueprints; the triptych is centred horizontally inside that width and
    # bands fill the entire content area.
    page_w = PAGE_W
    content_left = PAD
    content_w = page_w - 2 * PAD
    triptych_w = 3 * NODE_W + 2 * COL_GAP
    triptych_left = content_left + max(0, (content_w - triptych_w) / 2)
    col_pp_x = triptych_left
    col_st_x = triptych_left + NODE_W + COL_GAP
    col_mt_x = triptych_left + 2 * (NODE_W + COL_GAP)

    rules_band_x = content_left
    rules_band_w = content_w
    practices_band_x = content_left
    practices_band_w = (content_w - 28) / 2
    pitfalls_band_x = practices_band_x + practices_band_w + 28
    pitfalls_band_w = content_w - practices_band_w - 28

    # 1. Title
    cur_y = PAD
    title_top = cur_y
    cur_y += TITLE_H

    # 2. Rules band — single wrap
    rules_rects, rules_h = _wrap_band(rl, rules_band_x, cur_y + 32, rules_band_w)
    rules_card_h = rules_h + 32
    rules_card_y = cur_y
    rects.update(rules_rects)
    cur_y += rules_card_h + BAND_GAP_V

    # 3. Main triptych
    pp_layout, st_layout, mt_layout, n_rows = _align_main(pp, st, mt, relations)
    main_header_y = cur_y
    main_grid_y = cur_y + MAIN_HEADER_H
    for row, p in pp_layout:
        rects[p["id"]] = (col_pp_x, main_grid_y + row * ROW_H, NODE_W, NODE_H)
    for row, s in st_layout:
        rects[s["id"]] = (col_st_x, main_grid_y + row * ROW_H, NODE_W, NODE_H)
    for row, m in mt_layout:
        rects[m["id"]] = (col_mt_x, main_grid_y + row * ROW_H, NODE_W, NODE_H)
    main_h = MAIN_HEADER_H + n_rows * ROW_H + 16
    cur_y += main_h + BAND_GAP_V

    # 4. Practices + Pitfalls bands (side by side, wrapped)
    pract_rects, pract_h = _wrap_band(pr, practices_band_x, cur_y + 32, practices_band_w)
    pitf_rects, pitf_h = _wrap_band(pf, pitfalls_band_x, cur_y + 32, pitfalls_band_w)
    rects.update(pract_rects)
    rects.update(pitf_rects)
    bottom_band_h = max(pract_h, pitf_h) + 32
    bottom_band_y = cur_y
    cur_y += bottom_band_h

    # 5. Extras band — collects any user-defined entity types
    extras_card_y = None
    extras_card_h = 0
    if extras:
        cur_y += BAND_GAP_V
        extras_rects, extras_h = _wrap_band(
            extras, content_left, cur_y + 32, content_w
        )
        rects.update(extras_rects)
        extras_card_h = extras_h + 32
        extras_card_y = cur_y
        cur_y += extras_card_h

    canvas_h = cur_y + PAD

    # ─── SVG assembly ───
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {page_w} {canvas_h}" '
        f'width="{page_w}" height="{canvas_h}" '
        f'font-family="system-ui, -apple-system, sans-serif">',
        _arrow_markers(),
        f'<rect width="{page_w}" height="{canvas_h}" fill="#F7F5F1"/>',
    ]

    # Title
    title = meta.get("title", "Domain Knowledge Blueprint")
    intent = meta.get("detectedIntent", "")
    parts.append(
        f'<text x="{PAD}" y="{title_top + 36}" font-size="22" font-weight="700" '
        f'fill="#0F172A">{_esc(title)}</text>'
    )
    if intent:
        parts.append(
            f'<text x="{PAD}" y="{title_top + 62}" font-size="13" fill="#475569">'
            f'意图：{_esc(intent[:96])}</text>'
        )

    # Rules band card
    parts.append(_band_card(
        rules_band_x, rules_card_y, rules_band_w, rules_card_h,
        "⚖ 平台规则与政策（约束策略）",
        KNOWLEDGE_STYLES["rule"]["stroke"],
        KNOWLEDGE_STYLES["rule"]["fill"],
    ))

    # Main column headers — typography only, no underline (cleaner)
    for col_x, label, color in (
        (col_pp_x, "⚠ 痛点", KNOWLEDGE_STYLES["painPoint"]["stroke"]),
        (col_st_x, "💡 策略", KNOWLEDGE_STYLES["strategy"]["stroke"]),
        (col_mt_x, "📊 指标", KNOWLEDGE_STYLES["metric"]["stroke"]),
    ):
        parts.append(
            f'<text x="{col_x}" y="{main_header_y + 22}" font-size="14" '
            f'font-weight="700" fill="{color}">{_esc(label)}</text>'
        )

    # Practices + Pitfalls cards
    parts.append(_band_card(
        practices_band_x, bottom_band_y, practices_band_w, bottom_band_h,
        "✅ 最佳实践（支撑策略）",
        KNOWLEDGE_STYLES["practice"]["stroke"],
        KNOWLEDGE_STYLES["practice"]["fill"],
    ))
    parts.append(_band_card(
        pitfalls_band_x, bottom_band_y, pitfalls_band_w, bottom_band_h,
        "❌ 常见误区（导致痛点）",
        KNOWLEDGE_STYLES["pitfall"]["stroke"],
        KNOWLEDGE_STYLES["pitfall"]["fill"],
    ))

    # Extras card (user-defined entity types)
    if extras and extras_card_y is not None:
        parts.append(_band_card(
            content_left, extras_card_y, content_w, extras_card_h,
            "📦 其他（自定义实体）",
            DEFAULT_STYLE["stroke"], DEFAULT_STYLE["fill"],
        ))

    # Relations first (drawn under nodes)
    for rel in relations:
        if isinstance(rel, dict):
            parts.append(_render_relation(rel, rects))

    # Nodes (main triptych — full size)
    for _, p in pp_layout:
        x, y, w, h = rects[p["id"]]
        parts.append(_render_node(p, x, y, width=w, height=h))
    for _, s in st_layout:
        x, y, w, h = rects[s["id"]]
        parts.append(_render_node(s, x, y, width=w, height=h))
    for _, m in mt_layout:
        x, y, w, h = rects[m["id"]]
        parts.append(_render_node(m, x, y, width=w, height=h))

    # Nodes (band — smaller)
    for ent in rl + pr + pf + extras:
        eid = ent.get("id")
        if not isinstance(eid, str) or eid not in rects:
            continue
        x, y, w, h = rects[eid]
        parts.append(_render_node(ent, x, y, width=w, height=h))

    parts.append('</svg>')
    return "".join(parts)


def export_knowledge_svg(blueprint: dict[str, Any], target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_knowledge_svg(blueprint), encoding="utf-8")


def is_knowledge_blueprint(blueprint: dict[str, Any]) -> bool:
    meta = blueprint.get("meta", {}) or {}
    if meta.get("blueprintType") == "domain-knowledge":
        return True
    library = blueprint.get("library", {}) or {}
    knowledge = library.get("knowledge", {}) or {}
    if not isinstance(knowledge, dict):
        return False
    return any(isinstance(v, list) and v for v in knowledge.values())
