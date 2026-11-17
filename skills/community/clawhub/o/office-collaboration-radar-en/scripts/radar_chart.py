#!/usr/bin/env python3
r"""Generate a seven-dimension SVG collaboration-health radar.

Uses only the Python standard library. CLI:
  python radar_chart.py generate --card card.json --out radar.svg
  python radar_chart.py scores   --card card.json
  python radar_chart.py selftest
"""

from __future__ import annotations

import argparse
import html
import json
import math
import sys
from pathlib import Path
from typing import Any

from process import RadarInputError, _load_json, write_output_text

# SVG layout constants.
SVG_WIDTH = 600
SVG_HEIGHT = 520
CENTER_X = SVG_WIDTH // 2
CENTER_Y = 230
RADIUS = 180
LEVELS = 5
LABEL_OFFSET = 22
TABLE_Y = 440

# Light background with a deep-green accent.
GRID_COLOR = "#d4d4d8"
AXIS_COLOR = "#a1a1aa"
POLYGON_FILL = "rgba(22,163,74,0.18)"
POLYGON_STROKE = "#16a34a"
DOT_COLOR = "#16a34a"
LABEL_COLOR = "#27272a"
TABLE_BORDER = "#e4e4e7"
TABLE_HEADER_BG = "#f0fdf4"

# Seven dimensions in clockwise display order.
DIMENSIONS = [
    ("progress_clarity", "Progress clarity", "Evidence coverage for progress"),
    ("decision_certainty", "Decision certainty", "Decisions with a confirmation source"),
    ("task_health", "Action health", "Actions with supported owner and deadline"),
    ("risk_control", "Risk control", "Risks with a stated mitigation"),
    ("collab_flow", "Collaboration flow", "Evidence-backed cross-functional handoffs"),
    ("evidence_coverage", "Evidence coverage", "Evidence coverage across card items"),
    ("confirmation_debt", "Review debt", "Fewer unresolved review items is healthier"),
]


def compute_scores(card: dict) -> dict[str, float]:
    """Compute seven collaboration-health dimensions from zero to 100."""
    scores: dict[str, float] = {}

    # Progress clarity.
    items = card.get("progress")
    if isinstance(items, list) and items:
        ok = sum(1 for p in items if isinstance(p, dict)
                 and p.get("evidence") and p["evidence"] != "Not provided")
        scores["progress_clarity"] = round(ok / len(items) * 100, 1)
    else:
        scores["progress_clarity"] = 100.0

    # Decision certainty.
    items = card.get("confirmed_decisions")
    if isinstance(items, list) and items:
        ok = sum(1 for d in items if isinstance(d, dict)
                 and d.get("confirmed_by") and d["confirmed_by"] not in ("Not provided", ""))
        scores["decision_certainty"] = round(ok / len(items) * 100, 1)
    else:
        scores["decision_certainty"] = 100.0

    # Action health.
    items = card.get("action_items")
    if isinstance(items, list) and items:
        healthy = 0
        for a in items:
            if not isinstance(a, dict):
                continue
            has_owner = a.get("owner") and a["owner"] not in ("Not provided", "")
            has_ddl = a.get("ddl") and a["ddl"] not in ("Not provided", "")
            no_conflict = not a.get("conflict")
            if has_owner and has_ddl and no_conflict:
                healthy += 1
        scores["task_health"] = round(healthy / len(items) * 100, 1)
    else:
        scores["task_health"] = 100.0

    # Risk control.
    items = card.get("risks_dependencies")
    if isinstance(items, list) and items:
        ok = sum(1 for r in items if isinstance(r, dict)
                 and r.get("mitigation") and r["mitigation"] not in ("Not provided", ""))
        scores["risk_control"] = round(ok / len(items) * 100, 1)
    else:
        scores["risk_control"] = 100.0

    # Collaboration flow.
    items = card.get("cross_department_relationships")
    if isinstance(items, list) and items:
        ok = sum(1 for c in items if isinstance(c, dict)
                 and c.get("evidence") and c["evidence"] != "Not provided")
        scores["collab_flow"] = round(ok / len(items) * 100, 1)
    else:
        scores["collab_flow"] = 100.0

    # Evidence coverage.
    ev_keys = [
        "progress", "confirmed_decisions", "action_items",
        "risks_dependencies", "cross_department_relationships",
        "needs_human_confirmation",
    ]
    all_items: list[dict] = []
    for k in ev_keys:
        section = card.get(k, [])
        if isinstance(section, list):
            all_items.extend([i for i in section if isinstance(i, dict)])
    if all_items:
        ev_ok = sum(1 for i in all_items
                    if i.get("evidence") and i["evidence"] != "Not provided")
        scores["evidence_coverage"] = round(ev_ok / len(all_items) * 100, 1)
    else:
        scores["evidence_coverage"] = 50.0

    # Review debt is inverse: more unresolved items reduce the score.
    nhc = card.get("needs_human_confirmation")
    count = len(nhc) if isinstance(nhc, list) else 0
    scores["confirmation_debt"] = round(max(0, 100 - count * 25), 1)

    return scores


def _axis_point(angle: float, level: float, radius: float = RADIUS) -> tuple[float, float]:
    """Convert angle and normalized level into canvas coordinates."""
    x = CENTER_X + radius * level * math.cos(angle)
    y = CENTER_Y + radius * level * math.sin(angle)
    return x, y


def _path_points(scores: dict[str, float]) -> str:
    """Return the data-polygon path in dimension order."""
    n = len(DIMENSIONS)
    pts = []
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        level = min(scores.get(key, 0), 100) / 100
        x, y = _axis_point(angle, level)
        pts.append(f"{x:.1f},{y:.1f}")
    return " ".join(pts)


def generate_svg(scores: dict[str, float], title: str = "Collaboration Health Radar") -> str:
    """Generate a complete SVG radar chart."""
    n = len(DIMENSIONS)

    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}"'
        f' width="{SVG_WIDTH}" height="{SVG_HEIGHT}"'
        f' font-family="system-ui, -apple-system, sans-serif">'
    )
    lines.append(f'<rect width="{SVG_WIDTH}" height="{SVG_HEIGHT}" fill="#ffffff"/>')

    # Title.
    lines.append(
        f'<text x="{CENTER_X}" y="28" text-anchor="middle"'
        f' font-size="18" font-weight="700" fill="{LABEL_COLOR}">{html.escape(title, quote=True)}</text>'
    )

    # Concentric grid and axes.
    for level in range(1, LEVELS + 1):
        lv = level / LEVELS
        pts = []
        for i in range(n):
            angle = -math.pi / 2 + i * 2 * math.pi / n
            x, y = _axis_point(angle, lv)
            pts.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(pts)
        lines.append(
            f'<polygon points="{poly}" fill="none" stroke="{GRID_COLOR}"'
            f' stroke-width="1"/>'
        )
        # Level label.
        lines.append(
            f'<text x="{CENTER_X}" y="{CENTER_Y - RADIUS * lv + 4}"'
            f' text-anchor="middle" font-size="9" fill="#a1a1aa">{level * 20}</text>'
        )

    # Axes.
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        x1, y1 = _axis_point(angle, 0)
        x2, y2 = _axis_point(angle, 1)
        lines.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"'
            f' stroke="{AXIS_COLOR}" stroke-width="1"/>'
        )

    # Data polygon.
    data_pts = _path_points(scores)
    lines.append(
        f'<polygon points="{data_pts}" fill="{POLYGON_FILL}"'
        f' stroke="{POLYGON_STROKE}" stroke-width="2.2"/>'
    )

    # Data points.
    for i, (key, _, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        level = min(scores.get(key, 0), 100) / 100
        x, y = _axis_point(angle, level)
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="{DOT_COLOR}"/>')
        # Score label.
        score_label_y = y - 10 if y < CENTER_Y else y + 14
        lines.append(
            f'<text x="{x:.1f}" y="{score_label_y:.1f}" text-anchor="middle"'
            f' font-size="10" font-weight="600" fill="{DOT_COLOR}">{scores.get(key, 0):.0f}</text>'
        )

    # Axis labels.
    for i, (key, dim_label, _) in enumerate(DIMENSIONS):
        angle = -math.pi / 2 + i * 2 * math.pi / n
        lx, ly = _axis_point(angle, 1 + LABEL_OFFSET / RADIUS)
        lines.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle"'
            f' font-size="12" fill="{LABEL_COLOR}">{dim_label}</text>'
        )

    # Score table.
    col_w = 180
    row_h = 22
    table_start_x = CENTER_X - col_w * 1.5
    # Header row.
    lines.append(
        f'<rect x="{table_start_x}" y="{TABLE_Y}" width="{col_w * 3}"'
        f' height="{row_h}" fill="{TABLE_HEADER_BG}" stroke="{TABLE_BORDER}" stroke-width="1"/>'
    )
    lines.append(
        f'<text x="{table_start_x + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">Dimension</text>'
    )
    lines.append(
        f'<text x="{table_start_x + col_w + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">Description</text>'
    )
    lines.append(
        f'<text x="{table_start_x + col_w * 2 + 8}" y="{TABLE_Y + 15}" font-size="11"'
        f' font-weight="600" fill="{LABEL_COLOR}">Score</text>'
    )

    for j, (key, dim_label, dim_desc) in enumerate(DIMENSIONS):
        y = TABLE_Y + row_h + j * row_h
        bg = "#fafafa" if j % 2 == 0 else "#ffffff"
        lines.append(
            f'<rect x="{table_start_x}" y="{y}" width="{col_w * 3}" height="{row_h}"'
            f' fill="{bg}" stroke="{TABLE_BORDER}" stroke-width="0.5"/>'
        )
        lines.append(
            f'<text x="{table_start_x + 8}" y="{y + 15}" font-size="11"'
            f' fill="{LABEL_COLOR}">{dim_label}</text>'
        )
        lines.append(
            f'<text x="{table_start_x + col_w + 8}" y="{y + 15}" font-size="10"'
            f' fill="#71717a">{dim_desc}</text>'
        )
        val = scores.get(key, 0)
        color = "#16a34a" if val >= 70 else ("#eab308" if val >= 40 else "#ef4444")
        lines.append(
            f'<text x="{table_start_x + col_w * 2 + 8}" y="{y + 15}" font-size="12"'
            f' font-weight="600" fill="{color}">{val:.0f}</text>'
        )

    lines.append("</svg>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def _load_card_json(path: str) -> dict:
    return _load_json(Path(path))


def _selftest() -> int:
    print("== Office Collaboration Radar v0.1.2 radar self-test ==")
    fails = 0

    sample = {
        "project_overview": {"project_name": "X", "summary": "On track"},
        "progress": [
            {"item": "Design complete", "evidence": "Review approved"},
            {"item": "Development in progress", "evidence": "Not provided"},
        ],
        "confirmed_decisions": [
            {"decision": "Use option A", "result": "Approved", "confirmed_by": "Alex", "evidence": "Meeting notes"},
        ],
        "action_items": [
            {"task": "Integration", "owner": "Blair", "ddl": "Wednesday", "evidence": "Chat"},
            {"task": "Write docs", "owner": "Not provided", "ddl": "Not provided", "evidence": "Not provided", "conflict": "Conflict detected; human review required"},
        ],
        "risks_dependencies": [
            {"type": "Risk", "description": "External dependency", "mitigation": "Fallback", "evidence": "Review"},
        ],
        "cross_department_relationships": [
            {"from": "Product", "to": "Engineering", "collaboration_item": "Requirement review", "evidence": "Meeting"},
        ],
        "needs_human_confirmation": [{"item": "Budget", "reason": "Over plan"}],
    }

    # T1: score calculation.
    scores = compute_scores(sample)
    ok = (0 <= scores["task_health"] <= 100
          and scores["decision_certainty"] == 100.0
          and scores["risk_control"] == 100.0
          and scores["confirmation_debt"] == 75.0)
    print(("PASS" if ok else "FAIL"), "T1 score calculation:", {k: v for k, v in sorted(scores.items())})
    fails += 0 if ok else 1

    # T2: SVG structure.
    svg = generate_svg(scores, "Test Radar")
    ok = ("<svg" in svg and "</svg>" in svg
          and "Progress clarity" in svg and "Action health" in svg
          and "Test Radar" in svg)
    print(("PASS" if ok else "FAIL"), "T2 SVG structure:", len(svg), "bytes")
    fails += 0 if ok else 1

    # T3: empty card.
    empty = {}
    scores_e = compute_scores(empty)
    ok = all(0 <= v <= 100 for v in scores_e.values())
    print(("PASS" if ok else "FAIL"), "T3 empty card:", {k: v for k, v in sorted(scores_e.items())})
    fails += 0 if ok else 1

    # T4: SVG write.
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        out = Path(td) / "test.svg"
        out.write_text(svg, encoding="utf-8")
        ok = out.exists() and out.stat().st_size > 500
        print(("PASS" if ok else "FAIL"), "T4 SVG write:", out.stat().st_size, "bytes")
        fails += 0 if ok else 1

    # T5: title escaping prevents raw script markup.
    xss_title = '<script>alert(1)</script>&"x"'
    svg_xss = generate_svg(scores, xss_title)
    ok = (
        "&lt;script&gt;" in svg_xss
        and "&amp;" in svg_xss
        and "&quot;" in svg_xss
        and "<script>" not in svg_xss
    )
    print(("PASS" if ok else "FAIL"), "T5 title escaping:", "&lt;script&gt;" in svg_xss)
    fails += 0 if ok else 1

    print("=" * 40)
    if fails == 0:
        print("ALL PASS -- v0.1.2 radar")
        return 0
    print(f"{fails} checks failed")
    return 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(prog="radar_chart", description="Collaboration health SVG radar generator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("generate", help="Generate an SVG radar")
    p_gen.add_argument("--card", required=True, help="Card JSON path")
    p_gen.add_argument("--out", required=True, help="New output SVG path")
    p_gen.add_argument("--force", action="store_true", help="Replace the named output if it already exists")
    p_gen.add_argument("--title", default="Collaboration Health Radar", help="Chart title")

    sub.add_parser("scores", help="Print dimension scores as JSON").add_argument("--card", required=True)

    sub.add_parser("selftest", help="Run radar self-tests")

    args = parser.parse_args(argv)

    if args.cmd == "selftest":
        return _selftest()

    if args.cmd == "scores":
        card = _load_card_json(args.card)
        print(json.dumps(compute_scores(card), ensure_ascii=False, indent=2))
        return 0

    if args.cmd == "generate":
        card = _load_card_json(args.card)
        scores = compute_scores(card)
        svg = generate_svg(scores, args.title)
        write_output_text(
            Path(args.out),
            svg,
            protected_paths=[Path(args.card)],
            force=args.force,
        )
        print(f"Radar generated -> {args.out} ({len(svg)} bytes)")
        return 0

    return 1


def _cli_entry(argv: list[str]) -> int:
    try:
        return main(argv)
    except RadarInputError as e:
        print(f"[input error] {e}", file=sys.stderr)
        return 2
    except SystemExit as e:
        return int(e.code) if e.code is not None else 1
    except Exception as e:
        print(f"[unexpected error] {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(_cli_entry(sys.argv[1:]))
