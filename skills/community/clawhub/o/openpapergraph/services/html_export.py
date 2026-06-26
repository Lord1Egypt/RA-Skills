"""Export a GraphData object as a self-contained interactive HTML file.

Uses vis-network for graph visualization with semantic left-right layout:
- LEFT column: papers referenced BY seed papers (references)
- CENTER column: seed papers themselves
- RIGHT column: papers that CITE the seed papers (citations)

Features:
- Bidirectional hover linking between graph nodes and paper list
- Material Design inspired UI with clean, professional aesthetics
- Legend, source management, delete-source functionality
- Optional LLM-powered summary panel (floating action button)
- Search, filter, and export controls

Security: API keys are NEVER embedded in the HTML output.
"""

import html
import json
import math
import os
import sys
from collections import Counter
from typing import List, Optional

from schemas import GraphData, Paper

VIS_NETWORK_CDN = "https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"

# Logo image path (relative to this file's directory)
_LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "figures", "logo-part-light-full.png")


def _get_logo_b64() -> str:
    """Load logo PNG and return as base64 data URI, or empty string if not found."""
    import base64
    try:
        with open(_LOGO_PATH, "rb") as f:
            data = f.read()
        return "data:image/png;base64," + base64.b64encode(data).decode()
    except FileNotFoundError:
        return ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _safe(text: Optional[str], max_len: int = 0) -> str:
    if not text:
        return ""
    escaped = html.escape(text)
    if max_len and len(escaped) > max_len:
        return escaped[:max_len] + "\u2026"
    return escaped


def _authors_short(authors: List[str], max_authors: int = 3) -> str:
    if not authors:
        return "Unknown"
    names = [html.escape(a) for a in authors[:max_authors]]
    suffix = " et al." if len(authors) > max_authors else ""
    return ", ".join(names) + suffix


def _paper_sort_key(p: dict) -> tuple:
    year = p.get("year")
    return (0 if year is not None else 1, -(year or 0), (p.get("title") or "").lower())


def _year_color(year: Optional[int], min_year: int, max_year: int) -> str:
    if year is None or min_year == max_year:
        return "#888888"
    t = (year - min_year) / (max_year - min_year)
    colors = [
        (66, 133, 244),
        (52, 168, 83),
        (251, 188, 4),
        (234, 67, 53),
    ]
    idx = t * (len(colors) - 1)
    i = min(int(idx), len(colors) - 2)
    frac = idx - i
    r = int(colors[i][0] + frac * (colors[i + 1][0] - colors[i][0]))
    g = int(colors[i][1] + frac * (colors[i + 1][1] - colors[i][1]))
    b = int(colors[i][2] + frac * (colors[i + 1][2] - colors[i][2]))
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Node classification
# ---------------------------------------------------------------------------

def _classify_nodes(papers, edges, seed_set):
    """Classify each paper as 'seed', 'reference', 'citation', or 'indirect'.

    Edge convention: {"source": A, "target": B, "type": "cites"} means A cites B.
    - If A is seed and B is non-seed → B is a reference (seed cites it) → LEFT
    - If A is non-seed and B is seed → A is a citation (it cites seed) → RIGHT
    """
    classification = {}
    for p in papers:
        pid = p["id"]
        if pid in seed_set:
            classification[pid] = "seed"
        else:
            classification[pid] = "indirect"

    for e in edges:
        src, tgt = e["source"], e["target"]
        if src in seed_set and tgt not in seed_set:
            if classification.get(tgt) != "citation":
                classification[tgt] = "reference"
        elif tgt in seed_set and src not in seed_set:
            if classification.get(src) != "reference":
                classification[src] = "citation"

    return classification


# ---------------------------------------------------------------------------
# HTML Generation
# ---------------------------------------------------------------------------

def _fetch_vis_network_js() -> Optional[str]:
    try:
        import httpx
        print("[html-export] Downloading vis-network for inline embedding...", file=sys.stderr)
        resp = httpx.get(VIS_NETWORK_CDN, timeout=30.0, follow_redirects=True)
        resp.raise_for_status()
        print(f"[html-export] Downloaded vis-network ({len(resp.text) // 1024} KB)", file=sys.stderr)
        return resp.text
    except Exception as e:
        print(f"[html-export] Failed to download vis-network: {e}", file=sys.stderr)
        return None


# Node type → visual config
NODE_STYLES = {
    "seed":      {"shape": "star",    "color": "#6C5CE7", "border": "#4A3DB5", "size_min": 20},
    "reference": {"shape": "dot",     "color": "#0984E3", "border": "#0769B5", "size_min": 7},
    "citation":  {"shape": "diamond", "color": "#00B894", "border": "#009975", "size_min": 7},
    "indirect":  {"shape": "dot",     "color": "#B2BEC3", "border": "#95A5A6", "size_min": 6},
}

# Hierarchical level: reference=0, seed=1, citation=2, indirect=1
NODE_LEVELS = {"reference": 0, "seed": 1, "citation": 2, "indirect": 1}


def _generate_year_colors(min_year: int, max_year: int) -> dict:
    """Generate a stable color for each year with maximum contrast between neighbors.

    Uses the full HSL color wheel (0-360°) spread evenly across years,
    then applies golden-angle permutation so adjacent years in the timeline
    get maximally different hues.
    """
    import colorsys

    unique_years = list(range(min_year, max_year + 1))
    n = len(unique_years)
    if n == 0:
        return {}

    colors = {}
    # Golden angle (~137.5°) gives maximum separation between consecutive assignments
    GOLDEN_ANGLE = 137.508 / 360.0

    for i, year in enumerate(unique_years):
        # Golden-angle hue: each consecutive year jumps ~137.5° around the wheel
        hue = (i * GOLDEN_ANGLE) % 1.0

        # Moderate saturation and lightness for readability on white background
        sat = 0.60 + 0.10 * math.sin(i * 0.7)   # 0.50-0.70
        light = 0.45 + 0.08 * math.cos(i * 0.5)  # 0.37-0.53

        r, g, b = colorsys.hls_to_rgb(hue, light, sat)
        colors[year] = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    return colors


def _darken_hex(hex_color: str, factor: float = 0.2) -> str:
    """Darken a hex color by a factor (0-1)."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = int(r * (1 - factor))
    g = int(g * (1 - factor))
    b = int(b * (1 - factor))
    return f"#{r:02x}{g:02x}{b:02x}"


def _compute_positions(papers, edges, classification, seed_set, min_year, max_year):
    """Compute 2D positions using a horizontal timeline layout.

    Papers are arranged left-to-right by year (earliest on the left,
    latest on the right). Years are spaced evenly regardless of gaps.
    Within each year column, papers scatter vertically using golden-angle
    spirals to avoid overlaps.
    """
    GOLDEN_ANGLE = 2.39996323
    n_total = len(papers)
    from collections import defaultdict

    # --- Group papers by year ---
    all_years_list = sorted([p.get("year") for p in papers if p.get("year")])
    median_year = all_years_list[len(all_years_list) // 2] if all_years_list else (min_year + max_year) // 2

    by_year = defaultdict(list)
    for p in papers:
        yr = p.get("year") or median_year
        by_year[yr].append(p)

    sorted_years = sorted(by_year.keys())
    n_years = len(sorted_years)
    if n_years == 0:
        return {}

    # --- Horizontal layout: evenly spaced year columns ---
    # Spacing adapts to number of years — more years = tighter
    col_spacing = max(100, min(250, 3000 // max(n_years, 1)))

    # Year → x position (evenly spaced, not proportional to year gap)
    year_x = {}
    for i, yr in enumerate(sorted_years):
        year_x[yr] = i * col_spacing

    # Center around origin
    all_xs = list(year_x.values())
    cx = (min(all_xs) + max(all_xs)) / 2

    # --- Place papers within each year column ---
    all_pos = {}
    for yr, yr_papers in by_year.items():
        base_x = year_x[yr] - cx

        yr_papers.sort(key=lambda p: (
            0 if p["id"] in seed_set else 1,
            -(p.get("citation_count") or 0),
            p.get("title") or "",
        ))

        n_in_year = len(yr_papers)
        # Vertical scatter radius grows with cluster size
        max_scatter = min(300, 40 + n_in_year * 15)

        for idx, p in enumerate(yr_papers):
            pid = p["id"]
            is_seed = pid in seed_set

            # Golden-angle spiral — primarily vertical spread
            angle = idx * GOLDEN_ANGLE
            layer = idx // 6
            radius = 15 + layer * 25
            radius = min(radius, max_scatter)

            if is_seed:
                dx = math.cos(angle) * radius * 0.15  # minimal x jitter
                dy = math.sin(angle) * radius * 0.25
            else:
                dx = math.cos(angle) * radius * 0.3   # small x jitter
                dy = math.sin(angle) * radius          # full y spread

            all_pos[pid] = {"x": base_x + dx, "y": dy}

    # --- Collision avoidance ---
    ids = list(all_pos.keys())
    min_gap = max(35, 180 / max(math.sqrt(n_total), 1))
    for _ in range(15):
        for i in range(len(ids)):
            for j in range(i + 1, min(i + 40, len(ids))):
                a, b = all_pos[ids[i]], all_pos[ids[j]]
                ddx = b["x"] - a["x"]
                ddy = b["y"] - a["y"]
                d = math.sqrt(ddx * ddx + ddy * ddy) or 0.1
                if d < min_gap:
                    push = (min_gap - d) * 0.3
                    nx, ny = ddx / d, ddy / d
                    a["x"] -= push * nx
                    a["y"] -= push * ny
                    b["x"] += push * nx
                    b["y"] += push * ny

    return all_pos


def generate_html(
    graph: GraphData,
    title: str = "Paper Graph",
    pre_summary: Optional[dict] = None,
    inline_js: bool = False,
) -> str:
    papers = sorted([n.to_dict() for n in graph.nodes], key=_paper_sort_key)
    edges = graph.edges
    seed_set = set(graph.seed_papers)

    years = [p["year"] for p in papers if p.get("year")]
    min_year = min(years) if years else 2000
    max_year = max(years) if years else 2025

    classification = _classify_nodes(papers, edges, seed_set)

    # Count by type
    type_counts = Counter(classification.values())

    # --- Year-based color palette (stable, academic-friendly) ---
    year_colors = _generate_year_colors(min_year, max_year)

    # --- Compute time-based 2D positions ---
    positions = _compute_positions(papers, edges, classification, seed_set, min_year, max_year)

    vis_nodes = []
    for p in papers:
        pid = p["id"]
        ntype = classification.get(pid, "indirect")
        style = NODE_STYLES[ntype]
        cite_count = p.get("citation_count", 0)
        size = style["size_min"] + min(12, int(math.log1p(cite_count) * 2))

        pos = positions.get(pid, {"x": 0, "y": 0})

        # Use year-based color; fallback to type color for papers without year
        p_year = p.get("year")
        bg_color = year_colors.get(p_year, style["color"]) if p_year else style["color"]
        # Darken for border
        border_color = _darken_hex(bg_color, 0.2)

        vis_nodes.append({
            "id": pid,
            "label": (p.get("title") or "Untitled")[:35] + ("\u2026" if len(p.get("title") or "") > 35 else ""),
            "title": "",
            "size": size,
            "color": {
                "background": bg_color,
                "border": border_color,
                "highlight": {"background": "#FF6B35", "border": "#CC4400"},
                "hover": {"background": "#FF9966", "border": "#CC4400"},
            },
            "borderWidth": 3 if ntype == "seed" else 1,
            "font": {"size": 10 if ntype == "seed" else 8, "color": "#2D3436"},
            "shape": style["shape"],
            "group": ntype,
            "x": pos["x"],
            "y": pos["y"],
        })

    vis_edges = []
    for e in edges:
        vis_edges.append({
            "from": e["source"],
            "to": e["target"],
            "arrows": "to",
            "color": {"color": "#DFE6E9", "hover": "#FF9966", "highlight": "#FF6B35"},
            "width": 1,
        })

    papers_json = json.dumps(papers, ensure_ascii=False)
    vis_nodes_json = json.dumps(vis_nodes, ensure_ascii=False)
    vis_edges_json = json.dumps(vis_edges, ensure_ascii=False)
    seed_set_json = json.dumps(list(seed_set), ensure_ascii=False)
    classification_json = json.dumps(classification, ensure_ascii=False)
    pre_summary_json = json.dumps(pre_summary, ensure_ascii=False) if pre_summary else "null"
    type_counts_json = json.dumps(dict(type_counts), ensure_ascii=False)
    year_colors_json = json.dumps(year_colors, ensure_ascii=False)

    year_counts = Counter(p.get("year") for p in papers if p.get("year"))
    year_dist = sorted(year_counts.items())
    year_dist_json = json.dumps(year_dist, ensure_ascii=False)

    source_counts = Counter(p.get("source", "unknown") for p in papers)
    source_dist_json = json.dumps(sorted(source_counts.items(), key=lambda x: -x[1]), ensure_ascii=False)

    if inline_js:
        js_content = _fetch_vis_network_js()
        if js_content:
            vis_script_tag = f"<script>{js_content}</script>"
        else:
            vis_script_tag = f'<script src="{VIS_NETWORK_CDN}"></script>'
    else:
        vis_script_tag = f'<script src="{VIS_NETWORK_CDN}"></script>'

    logo_b64 = _get_logo_b64()

    return _HTML_TEMPLATE.format(
        title=_safe(title),
        total_papers=len(papers),
        total_edges=len(edges),
        min_year=min_year,
        max_year=max_year,
        papers_json=papers_json,
        vis_nodes_json=vis_nodes_json,
        vis_edges_json=vis_edges_json,
        seed_set_json=seed_set_json,
        classification_json=classification_json,
        pre_summary_json=pre_summary_json,
        year_dist_json=year_dist_json,
        source_dist_json=source_dist_json,
        type_counts_json=type_counts_json,
        year_colors_json=year_colors_json,
        vis_script_tag=vis_script_tag,
        n_seed=type_counts.get("seed", 0),
        n_ref=type_counts.get("reference", 0),
        n_cite=type_counts.get("citation", 0),
        n_indirect=type_counts.get("indirect", 0),
        logo_b64=logo_b64,
    )


def export_html(
    graph: GraphData,
    output_path: str,
    title: str = "Paper Graph",
    pre_summary: Optional[dict] = None,
    inline_js: bool = False,
) -> str:
    content = generate_html(graph, title=title, pre_summary=pre_summary, inline_js=inline_js)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[html-export] Saved interactive graph to: {output_path}", file=sys.stderr)
    return output_path


# ---------------------------------------------------------------------------
# HTML Template
# ---------------------------------------------------------------------------

_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{vis_script_tag}
<style>
/* ====== Reset & Base ====== */
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background: #FAFBFC; color: #1A1A2E;
  height: 100vh; overflow: hidden;
  -webkit-font-smoothing: antialiased;
}}

/* ====== Layout ====== */
.app {{ display: flex; flex-direction: column; height: 100vh; }}
.toolbar {{
  height: 52px; display: flex; align-items: center; padding: 0 20px; gap: 16px;
  background: #fff; border-bottom: 1px solid #E8ECF0;
  flex-shrink: 0; z-index: 50;
}}
.toolbar-title {{
  font-size: 15px; font-weight: 700; color: #1A1A2E;
  display: flex; align-items: center; gap: 8px;
}}
.toolbar-title svg {{ width: 20px; height: 20px; }}
.toolbar-stats {{
  display: flex; gap: 12px; margin-left: auto; font-size: 12px; color: #64748B;
}}
.toolbar-stats .chip {{
  display: inline-flex; align-items: center; gap: 4px;
  padding: 3px 10px; border-radius: 12px; background: #F1F5F9;
  font-weight: 500;
}}
.toolbar-stats .chip .dot {{
  width: 8px; height: 8px; border-radius: 50%; display: inline-block;
}}

.main-area {{ display: flex; flex: 1; overflow: hidden; }}
.graph-panel {{ flex: 1; position: relative; background: #FFFFFF; }}
.side-panel {{
  width: 380px; min-width: 320px; max-width: 450px;
  display: flex; flex-direction: column;
  border-left: 1px solid #E8ECF0;
  background: #FAFBFC;
}}

/* ====== Graph Controls ====== */
.graph-controls {{
  position: absolute; top: 12px; left: 12px; z-index: 10;
  display: flex; gap: 6px;
}}
.graph-controls button {{
  padding: 6px 14px; border: 1px solid #E8ECF0; border-radius: 8px;
  background: rgba(255,255,255,0.96); cursor: pointer; font-size: 12px;
  color: #475569; font-weight: 500;
  transition: all 0.15s; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}}
.graph-controls button:hover {{ background: #4361EE; color: #fff; border-color: #4361EE; }}

/* ====== Legend ====== */
.graph-legend {{
  position: absolute; bottom: 12px; left: 12px; z-index: 10;
  background: rgba(255,255,255,0.96); border-radius: 10px; padding: 10px 14px;
  font-size: 11px; display: flex; flex-direction: column; gap: 6px;
  border: 1px solid #E8ECF0; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  color: #475569;
}}
.graph-legend .legend-title {{
  font-weight: 600; font-size: 11px; color: #1A1A2E; margin-bottom: 2px;
}}
.legend-row {{ display: flex; align-items: center; gap: 8px; }}
.legend-icon {{
  width: 14px; height: 14px; display: inline-flex; align-items: center; justify-content: center;
  font-size: 14px; line-height: 1;
}}
.legend-label {{ font-size: 11px; }}
.legend-count {{ font-size: 10px; color: #94A3B8; margin-left: auto; }}

/* ====== Year Legend ====== */
.year-legend {{
  position: absolute; bottom: 12px; right: 12px; z-index: 10;
  background: rgba(255,255,255,0.96); border-radius: 10px; padding: 8px 14px;
  font-size: 11px; display: flex; align-items: center; gap: 8px;
  border: 1px solid #E8ECF0; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  color: #475569;
}}
.year-legend .gradient {{
  width: 120px; height: 10px; border-radius: 5px;
  /* Actual gradient set dynamically in JS from YEAR_COLORS */
}}

/* ====== Graph Canvas ====== */
#graph-canvas {{ width: 100%; height: 100%; }}

/* ====== Side Panel ====== */
.side-header {{
  padding: 14px 16px; background: #fff;
  border-bottom: 1px solid #E8ECF0; flex-shrink: 0;
}}
.side-tabs {{
  display: flex; gap: 0; border-bottom: 2px solid #E8ECF0; margin-bottom: 10px;
}}
.side-tab {{
  flex: 1; padding: 8px 12px; text-align: center; cursor: pointer;
  font-size: 12px; font-weight: 500; color: #94A3B8;
  border: none; background: none; border-bottom: 2px solid transparent;
  margin-bottom: -2px; transition: all 0.15s;
}}
.side-tab:hover {{ color: #4361EE; }}
.side-tab.active {{ color: #4361EE; border-bottom-color: #4361EE; font-weight: 600; }}

.search-box {{
  width: 100%; padding: 8px 12px; border: 1px solid #E8ECF0; border-radius: 8px;
  font-size: 13px; outline: none; transition: border 0.15s;
  background: #FAFBFC;
}}
.search-box:focus {{ border-color: #4361EE; background: #fff; }}
.filter-row {{
  display: flex; gap: 8px; margin-top: 8px; flex-wrap: wrap;
}}
.filter-row select, .filter-row button {{
  padding: 5px 10px; border: 1px solid #E8ECF0; border-radius: 6px;
  font-size: 12px; background: #fff; cursor: pointer; color: #475569;
}}
.filter-row select:focus {{ border-color: #4361EE; outline: none; }}
.filter-row button:hover {{ border-color: #4361EE; color: #4361EE; }}

/* ====== Paper List ====== */
.paper-list {{
  flex: 1; overflow-y: auto; padding: 8px 10px;
  scroll-behavior: smooth;
}}
.paper-item {{
  padding: 10px 12px; margin-bottom: 6px;
  background: #fff; border-radius: 8px;
  border: 1px solid #E8ECF0;
  cursor: pointer; transition: all 0.15s;
  font-size: 13px;
}}
.paper-item:hover {{ border-color: #4361EE; box-shadow: 0 1px 4px rgba(67,97,238,0.1); }}
.paper-item.highlighted {{ border-color: #FF6B35; background: #FFF8F5; }}
.paper-item.selected {{ border-color: #4361EE; background: #F0F4FF; box-shadow: 0 1px 4px rgba(67,97,238,0.15); }}
.paper-item .paper-title {{
  font-weight: 600; color: #1A1A2E; margin-bottom: 4px;
  line-height: 1.4; font-size: 13px;
}}
.paper-item .paper-meta {{
  font-size: 11px; color: #64748B; line-height: 1.5;
  display: flex; flex-wrap: wrap; align-items: center; gap: 4px;
}}
.badge {{
  display: inline-block; padding: 1px 7px; border-radius: 4px;
  font-weight: 600; font-size: 10px; color: #fff;
}}
.badge-seed {{ background: #6C5CE7; }}
.badge-ref {{ background: #0984E3; }}
.badge-cite {{ background: #00B894; }}
.badge-year {{
  font-weight: 500; font-size: 10px;
}}
.paper-item .paper-details {{
  max-height: 0; overflow: hidden; transition: max-height 0.35s ease;
  margin-top: 0;
}}
.paper-item.selected .paper-details {{ max-height: 500px; margin-top: 8px; }}
.paper-detail-section {{
  font-size: 11px; color: #475569; line-height: 1.5; margin-bottom: 6px;
}}
.paper-detail-section .detail-label {{
  font-weight: 600; color: #1A1A2E; font-size: 10px; text-transform: uppercase;
  letter-spacing: 0.5px; margin-bottom: 2px;
}}
.paper-detail-section .detail-value {{
  color: #64748B;
}}
.paper-detail-section .author-list {{
  display: flex; flex-wrap: wrap; gap: 3px;
}}
.paper-detail-section .author-tag {{
  background: #F1F5F9; border-radius: 4px; padding: 1px 6px;
  font-size: 10px; color: #475569; white-space: nowrap;
}}
.paper-abstract {{
  font-size: 11px; color: #64748B; line-height: 1.5;
  background: #F8FAFC; border-radius: 6px; padding: 8px 10px;
  border-left: 3px solid #E2E8F0;
}}
.paper-actions {{
  margin-top: 6px; max-height: 0; overflow: hidden; transition: max-height 0.2s;
}}
.paper-item.selected .paper-actions {{ max-height: 50px; }}
.convert-seed-btn-list {{
  padding: 4px 12px; border: 1px solid #6C5CE7; border-radius: 6px;
  background: #fff; color: #6C5CE7; font-size: 11px; cursor: pointer;
  font-weight: 500; transition: all 0.15s;
}}
.convert-seed-btn-list:hover {{ background: #6C5CE7; color: #fff; }}

/* ====== Source List Tab ====== */
.source-list {{
  flex: 1; overflow-y: auto; padding: 8px 10px;
}}
.source-item {{
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 12px; margin-bottom: 6px;
  background: #fff; border-radius: 8px;
  border: 1px solid #E8ECF0; font-size: 13px;
  transition: all 0.15s;
}}
.source-item:hover {{ border-color: #E74C3C; }}
.source-item .source-info {{
  flex: 1; min-width: 0;
}}
.source-item .source-title {{
  font-weight: 600; color: #1A1A2E; margin-bottom: 3px;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.source-item .source-meta {{
  font-size: 11px; color: #64748B;
}}
.source-delete {{
  padding: 4px 10px; border: 1px solid #E8ECF0; border-radius: 6px;
  background: #fff; color: #E74C3C; font-size: 11px; cursor: pointer;
  font-weight: 500; transition: all 0.15s; flex-shrink: 0; margin-left: 8px;
}}
.source-delete:hover {{ background: #E74C3C; color: #fff; border-color: #E74C3C; }}

/* ====== Export Buttons ====== */
.export-bar {{
  padding: 8px 12px; background: #fff;
  border-top: 1px solid #E8ECF0; flex-shrink: 0;
  display: flex; gap: 6px;
}}
.export-bar button {{
  flex: 1; padding: 6px; border: 1px solid #E8ECF0; border-radius: 6px;
  background: #fff; cursor: pointer; font-size: 11px; color: #475569;
  font-weight: 500; transition: all 0.15s;
}}
.export-bar button:hover {{ background: #4361EE; color: #fff; border-color: #4361EE; }}

/* ====== Empty State ====== */
.empty-state {{
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 40px 20px; color: #94A3B8; text-align: center;
}}
.empty-state svg {{ width: 48px; height: 48px; margin-bottom: 12px; opacity: 0.5; }}
.empty-state p {{ font-size: 13px; }}

/* ====== Tooltip ====== */
.node-tooltip {{
  position: absolute; z-index: 100; pointer-events: none;
  background: #fff; border: 1px solid #E8ECF0;
  border-radius: 10px; padding: 14px 16px; max-width: 380px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  font-size: 13px; line-height: 1.5;
  opacity: 0; transition: opacity 0.12s;
}}
.node-tooltip.visible {{ opacity: 1; }}
.node-tooltip.pinned {{ pointer-events: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border-color: #4361EE; }}
.node-tooltip .tt-title {{ font-weight: 700; margin-bottom: 6px; color: #1A1A2E; }}
.node-tooltip .tt-type {{
  display: inline-block; padding: 1px 7px; border-radius: 4px;
  font-size: 10px; font-weight: 600; color: #fff; margin-bottom: 6px;
}}
.node-tooltip .tt-row {{ color: #64748B; font-size: 12px; margin-bottom: 2px; }}
.node-tooltip .tt-abstract {{
  font-size: 11px; color: #64748B; margin-top: 6px;
  border-top: 1px solid #E8ECF0; padding-top: 6px;
}}

/* ====== Summary FAB ====== */
.summary-fab {{
  position: fixed; bottom: 24px; right: 404px; z-index: 200;
  width: 48px; height: 48px; border-radius: 50%;
  background: #4361EE; color: #fff; border: none; cursor: pointer;
  box-shadow: 0 4px 12px rgba(67,97,238,0.35);
  font-size: 20px; display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
}}
.summary-fab:hover {{ transform: scale(1.08); box-shadow: 0 6px 18px rgba(67,97,238,0.45); }}

/* ====== Summary Panel (Modal) ====== */
.summary-overlay {{
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3); z-index: 300;
  opacity: 0; pointer-events: none; transition: opacity 0.2s;
}}
.summary-overlay.visible {{ opacity: 1; pointer-events: auto; }}
.summary-panel {{
  position: fixed; top: 50%; left: 50%;
  transform: translate(-50%, -50%) scale(0.95);
  width: 660px; max-width: 90vw; max-height: 80vh;
  background: #fff; border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
  z-index: 301; overflow: hidden;
  opacity: 0; pointer-events: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}}
.summary-panel.visible {{ opacity: 1; pointer-events: auto; transform: translate(-50%, -50%) scale(1); }}
.summary-panel-header {{
  padding: 14px 20px; background: #4361EE;
  color: #fff; display: flex; justify-content: space-between; align-items: center;
}}
.summary-panel-header h3 {{ font-size: 15px; font-weight: 600; }}
.summary-panel-close {{
  background: none; border: none; color: rgba(255,255,255,0.8); font-size: 18px;
  cursor: pointer; padding: 4px 8px; border-radius: 4px;
}}
.summary-panel-close:hover {{ color: #fff; background: rgba(255,255,255,0.15); }}
.summary-panel-body {{ padding: 20px; overflow-y: auto; max-height: calc(80vh - 54px); }}
.summary-section {{ margin-bottom: 18px; }}
.summary-section h4 {{
  font-size: 13px; font-weight: 600; color: #4361EE; margin-bottom: 8px;
  padding-bottom: 4px; border-bottom: 2px solid #EBF0FF;
}}
.summary-section p, .summary-section li {{
  font-size: 13px; color: #1A1A2E; line-height: 1.6;
}}
.summary-section ul {{ padding-left: 18px; }}
.summary-section li {{ margin-bottom: 4px; }}
.summary-loading {{ text-align: center; padding: 40px; }}
.summary-loading .spinner {{
  width: 36px; height: 36px; border: 3px solid #EBF0FF;
  border-top-color: #4361EE; border-radius: 50%;
  animation: spin 0.7s linear infinite; margin: 0 auto 16px;
}}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}
.summary-error {{ text-align: center; padding: 30px; color: #E74C3C; }}
.summary-error button {{
  margin-top: 12px; padding: 8px 16px; border: 1px solid #E74C3C;
  border-radius: 6px; background: #fff; color: #E74C3C;
  cursor: pointer; transition: all 0.15s; font-size: 12px;
}}
.summary-error button:hover {{ background: #E74C3C; color: #fff; }}

/* ====== API Key Form ====== */
.api-key-form {{ padding: 16px; text-align: center; }}
.api-key-form p {{ font-size: 12px; color: #64748B; margin-bottom: 12px; line-height: 1.5; }}
.api-key-form input {{
  width: 100%; padding: 9px 12px; border: 1px solid #E8ECF0; border-radius: 8px;
  font-size: 12px; font-family: monospace; outline: none; transition: border 0.15s;
  margin-bottom: 8px; background: #FAFBFC;
}}
.api-key-form input:focus {{ border-color: #4361EE; background: #fff; }}
.api-key-form .form-row {{ display: flex; gap: 8px; margin-bottom: 8px; }}
.api-key-form .form-row input, .api-key-form .form-row select {{
  flex: 1; padding: 8px 10px; border: 1px solid #E8ECF0; border-radius: 6px;
  font-size: 12px; outline: none; background: #FAFBFC;
}}
.api-key-form .form-row select:focus, .api-key-form .form-row input:focus {{ border-color: #4361EE; background: #fff; }}
.api-key-form button.submit-btn {{
  padding: 9px 24px; border: none; border-radius: 8px;
  background: #4361EE; color: #fff;
  font-size: 13px; font-weight: 500; cursor: pointer; transition: all 0.15s; margin-top: 4px;
}}
.api-key-form button.submit-btn:hover {{ background: #3651D4; }}
.api-key-form .hint {{ font-size: 11px; color: #94A3B8; margin-top: 10px; }}

/* ====== Mode Tabs ====== */
.mode-tabs {{ display: flex; border-bottom: 2px solid #E8ECF0; margin-bottom: 14px; }}
.mode-tab {{
  flex: 1; padding: 9px 14px; text-align: center; cursor: pointer;
  font-size: 12px; font-weight: 500; color: #94A3B8;
  border-bottom: 2px solid transparent;
  margin-bottom: -2px; transition: all 0.15s; background: none;
  border-top: none; border-left: none; border-right: none;
}}
.mode-tab:hover {{ color: #4361EE; }}
.mode-tab.active {{ color: #4361EE; border-bottom-color: #4361EE; font-weight: 600; }}

/* ====== Manual Mode ====== */
.manual-mode {{ padding: 0 4px; }}
.manual-mode .step {{ margin-bottom: 14px; }}
.manual-mode .step-label {{
  font-size: 12px; font-weight: 600; color: #4361EE; margin-bottom: 6px;
  display: flex; align-items: center; gap: 6px;
}}
.manual-mode .step-num {{
  display: inline-flex; width: 20px; height: 20px; border-radius: 50%;
  background: #4361EE; color: #fff; font-size: 10px;
  align-items: center; justify-content: center; font-weight: 700;
}}
.manual-mode textarea {{
  width: 100%; border: 1px solid #E8ECF0; border-radius: 8px;
  padding: 10px 12px; font-size: 12px; font-family: "SF Mono", "Fira Code", monospace;
  outline: none; resize: vertical; transition: border 0.15s; background: #FAFBFC;
}}
.manual-mode textarea:focus {{ border-color: #4361EE; background: #fff; }}
.manual-mode .btn-row {{ display: flex; gap: 8px; margin-top: 6px; }}
.manual-mode .btn-row button {{
  padding: 7px 16px; border-radius: 6px; font-size: 12px;
  cursor: pointer; transition: all 0.15s; font-weight: 500;
}}
.manual-mode .btn-primary {{ border: none; background: #4361EE; color: #fff; }}
.manual-mode .btn-primary:hover {{ background: #3651D4; }}
.manual-mode .btn-secondary {{ border: 1px solid #E8ECF0; background: #fff; color: #64748B; }}
.manual-mode .btn-secondary:hover {{ border-color: #4361EE; color: #4361EE; }}
.manual-mode .copied-toast {{
  display: inline-block; color: #00B894; font-size: 12px; margin-left: 8px;
  opacity: 0; transition: opacity 0.2s;
}}
.manual-mode .copied-toast.show {{ opacity: 1; }}

/* ====== Confirm Dialog ====== */
.confirm-overlay {{
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.35); z-index: 400;
  display: flex; align-items: center; justify-content: center;
}}
.confirm-dialog {{
  background: #fff; border-radius: 12px; padding: 24px; min-width: 320px;
  box-shadow: 0 12px 40px rgba(0,0,0,0.15); text-align: center;
}}
.confirm-dialog h4 {{ font-size: 15px; margin-bottom: 8px; color: #1A1A2E; }}
.confirm-dialog p {{ font-size: 13px; color: #64748B; margin-bottom: 16px; }}
.confirm-dialog .btn-group {{ display: flex; gap: 8px; justify-content: center; }}
.confirm-dialog button {{
  padding: 8px 20px; border-radius: 6px; font-size: 13px;
  cursor: pointer; font-weight: 500; transition: all 0.15s;
}}
.confirm-dialog .btn-cancel {{ border: 1px solid #E8ECF0; background: #fff; color: #64748B; }}
.confirm-dialog .btn-cancel:hover {{ border-color: #4361EE; color: #4361EE; }}
.confirm-dialog .btn-danger {{ border: none; background: #E74C3C; color: #fff; }}
.confirm-dialog .btn-danger:hover {{ background: #C0392B; }}

/* ====== Toast ====== */
.toast {{
  position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
  background: #1A1A2E; color: #fff; padding: 10px 20px; border-radius: 8px;
  font-size: 13px; z-index: 500; opacity: 0; transition: opacity 0.2s;
  pointer-events: none; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}
.toast.visible {{ opacity: 1; }}

/* ====== Scrollbar ====== */
.paper-list::-webkit-scrollbar, .source-list::-webkit-scrollbar {{ width: 5px; }}
.paper-list::-webkit-scrollbar-track, .source-list::-webkit-scrollbar-track {{ background: transparent; }}
.paper-list::-webkit-scrollbar-thumb, .source-list::-webkit-scrollbar-thumb {{ background: #DFE6E9; border-radius: 3px; }}
.paper-list::-webkit-scrollbar-thumb:hover, .source-list::-webkit-scrollbar-thumb:hover {{ background: #B2BEC3; }}
.summary-panel-body::-webkit-scrollbar {{ width: 5px; }}
.summary-panel-body::-webkit-scrollbar-track {{ background: transparent; }}
.summary-panel-body::-webkit-scrollbar-thumb {{ background: #DFE6E9; border-radius: 3px; }}
</style>
</head>
<body>

<div class="app">
  <!-- Top Toolbar -->
  <div class="toolbar">
    <div class="toolbar-title">
      <img src="{logo_b64}" alt="OpenPaperGraph" style="height:28px;" onerror="this.style.display='none'">
    </div>
    <div class="toolbar-stats">
      <span class="chip"><span class="dot" style="background:#6C5CE7"></span> Seeds: {n_seed}</span>
      <span class="chip"><span class="dot" style="background:#0984E3"></span> References: {n_ref}</span>
      <span class="chip"><span class="dot" style="background:#00B894"></span> Citations: {n_cite}</span>
      <span class="chip">{total_papers} papers</span>
      <span class="chip">{total_edges} edges</span>
    </div>
  </div>

  <div class="main-area">
    <!-- Graph Panel -->
    <div class="graph-panel">
      <div class="graph-controls">
        <button onclick="resetView()" title="Reset to timeline layout">Reset</button>
        <button onclick="togglePhysics()" id="btn-physics" title="Toggle physics">Physics</button>
        <button onclick="fitAll()" title="Fit all nodes">Fit All</button>
      </div>
      <div id="graph-canvas"></div>
      <!-- Legend -->
      <div class="graph-legend">
        <div class="legend-title">Layout Semantics</div>
        <div class="legend-row">
          <span class="legend-icon" style="color:#0984E3">&#9679;</span>
          <span class="legend-label">References (LEFT)</span>
          <span class="legend-count">{n_ref}</span>
        </div>
        <div class="legend-row">
          <span class="legend-icon" style="color:#6C5CE7">&#9733;</span>
          <span class="legend-label">Seeds (CENTER)</span>
          <span class="legend-count">{n_seed}</span>
        </div>
        <div class="legend-row">
          <span class="legend-icon" style="color:#00B894">&#9670;</span>
          <span class="legend-label">Citations (RIGHT)</span>
          <span class="legend-count">{n_cite}</span>
        </div>
      </div>
      <div class="year-legend">
        <span>{min_year}</span>
        <div class="gradient"></div>
        <span>{max_year}</span>
      </div>
    </div>

    <!-- Side Panel -->
    <div class="side-panel">
      <div class="side-header">
        <div class="side-tabs">
          <button class="side-tab active" onclick="switchSideTab('papers')" id="tab-papers">Papers</button>
          <button class="side-tab" onclick="switchSideTab('sources')" id="tab-sources">Seeds / Sources</button>
        </div>
        <div id="papers-controls">
          <input type="text" class="search-box" id="search-box" placeholder="Search title, author, year..." oninput="filterPapers()">
          <div class="filter-row">
            <select id="type-filter" onchange="filterPapers()">
              <option value="">All Types</option>
              <option value="seed">Seeds</option>
              <option value="reference">References</option>
              <option value="citation">Citations</option>
            </select>
            <select id="year-filter" onchange="filterPapers()"><option value="">All Years</option></select>
            <select id="sort-select" onchange="sortPapers()">
              <option value="year-desc">Year &darr;</option>
              <option value="year-asc">Year &uarr;</option>
              <option value="cite-desc">Cites &darr;</option>
              <option value="title-asc">Title A-Z</option>
            </select>
            <button onclick="clearFilters()">Clear</button>
          </div>
        </div>
      </div>
      <div class="paper-list" id="paper-list"></div>
      <div class="source-list" id="source-list" style="display:none"></div>
      <div class="export-bar">
        <button onclick="exportAs('json')">JSON</button>
        <button onclick="exportAs('csv')">CSV</button>
        <button onclick="exportAs('markdown')">Markdown</button>
        <button onclick="copyForLLM()" title="Copy a structured summary of all papers to clipboard, ready to paste into any LLM">Copy for LLM</button>
      </div>
    </div>
  </div>
</div>

<!-- Tooltip -->
<div class="node-tooltip" id="node-tooltip"></div>

<!-- Toast -->
<div class="toast" id="toast-msg"></div>

<!-- Summary FAB + Panel -->
<button class="summary-fab" id="summary-fab" onclick="toggleSummary()" title="AI Summary">&#10022;</button>
<div class="summary-overlay" id="summary-overlay" onclick="closeSummary()"></div>
<div class="summary-panel" id="summary-panel">
  <div class="summary-panel-header">
    <h3>AI Summary &amp; Classification</h3>
    <button class="summary-panel-close" onclick="closeSummary()">&times;</button>
  </div>
  <div class="summary-panel-body" id="summary-body"></div>
</div>

<script>
// ====== Data ======
var SERVER_MODE = false;  // overridden by graph_server.py in serve mode
const ALL_PAPERS_ORIG = {papers_json};
let ALL_PAPERS = [...ALL_PAPERS_ORIG];
const VIS_NODES_DATA = {vis_nodes_json};
const VIS_EDGES_DATA = {vis_edges_json};
const SEED_SET = new Set({seed_set_json});
const CLASSIFICATION = {classification_json};
const PRE_SUMMARY = {pre_summary_json};
const YEAR_DIST = {year_dist_json};
const SOURCE_DIST = {source_dist_json};
const TYPE_COUNTS = {type_counts_json};
const YEAR_COLORS = {year_colors_json};

// State
let papers = [...ALL_PAPERS];
let selectedId = null;
let hoverLock = false;
let physicsEnabled = true;
let summaryCache = null;
let summaryState = "idle";
let currentSideTab = "papers";

const paperById = {{}};
ALL_PAPERS.forEach(p => {{ paperById[p.id] = p; }});

// ====== Helpers ======
function escapeHtml(text) {{
  if (!text) return "";
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}}

function showToast(msg) {{
  const t = document.getElementById("toast-msg");
  t.textContent = msg;
  t.classList.add("visible");
  setTimeout(() => t.classList.remove("visible"), 2500);
}}

function getTypeBadge(pid) {{
  const t = CLASSIFICATION[pid];
  if (t === "seed") return '<span class="badge badge-seed">SEED</span>';
  if (t === "reference") return '<span class="badge badge-ref">REF</span>';
  if (t === "citation") return '<span class="badge badge-cite">CITE</span>';
  return '';
}}

function getTypeColor(pid) {{
  // Return year-based color if available
  const p = ALL_PAPERS.find(x => x.id === pid);
  if (p && p.year && YEAR_COLORS[p.year]) return YEAR_COLORS[p.year];
  // No year → neutral gray
  return "#A0AEC0";
}}

// Paper-by-ID lookup cache for performance
const _paperById = {{}};
ALL_PAPERS.forEach(p => {{ _paperById[p.id] = p; }});

// ====== Initialize vis-network ======
const container = document.getElementById("graph-canvas");
const nodes = new vis.DataSet(VIS_NODES_DATA);
const edges = new vis.DataSet(VIS_EDGES_DATA);

const network = new vis.Network(container, {{ nodes, edges }}, {{
  layout: {{
    randomSeed: 42,
  }},
  physics: {{
    enabled: false,
  }},
  interaction: {{
    hover: true,
    tooltipDelay: 0,
    hideEdgesOnDrag: false,
    hideEdgesOnZoom: false,
    zoomView: true,
    dragView: true,
    dragNodes: true,
  }},
  edges: {{
    smooth: {{ type: "cubicBezier", forceDirection: "horizontal", roundness: 0.35 }},
  }},
}});

// Save original timeline positions before any physics runs
const ORIGINAL_POSITIONS = {{}};
VIS_NODES_DATA.forEach(n => {{
  ORIGINAL_POSITIONS[n.id] = {{ x: n.x, y: n.y }};
}});

// Positions are pre-computed in Python — fit to view after render
physicsEnabled = false;
document.getElementById("btn-physics").textContent = "Physics Off";
setTimeout(function() {{
  network.fit({{ animation: {{ duration: 300, easingFunction: "easeInOutCubic" }} }});
}}, 100);

// ====== Set year-color gradient ======
(function() {{
  const years = Object.keys(YEAR_COLORS).map(Number).sort((a,b) => a - b);
  if (years.length > 0) {{
    const stops = years.map((y, i) => YEAR_COLORS[y] + " " + (i / Math.max(years.length - 1, 1) * 100).toFixed(1) + "%");
    const gradEl = document.querySelector(".year-legend .gradient");
    if (gradEl) gradEl.style.background = "linear-gradient(to right, " + stops.join(", ") + ")";
  }}
}})();

// ====== Populate year filter ======
const yearSet = new Set(ALL_PAPERS.map(p => p.year).filter(Boolean));
const yearSelect = document.getElementById("year-filter");
[...yearSet].sort((a,b) => b - a).forEach(y => {{
  const opt = document.createElement("option");
  opt.value = y; opt.textContent = y;
  yearSelect.appendChild(opt);
}});

// ====== Side Tab Switch ======
function switchSideTab(tab) {{
  currentSideTab = tab;
  document.getElementById("tab-papers").classList.toggle("active", tab === "papers");
  document.getElementById("tab-sources").classList.toggle("active", tab === "sources");
  document.getElementById("paper-list").style.display = tab === "papers" ? "" : "none";
  document.getElementById("source-list").style.display = tab === "sources" ? "" : "none";
  document.getElementById("papers-controls").style.display = tab === "papers" ? "" : "none";
  if (tab === "sources") renderSourceList();
}}

// ====== Render Paper List ======
function renderPaperList() {{
  const list = document.getElementById("paper-list");
  list.innerHTML = "";
  if (papers.length === 0) {{
    list.innerHTML = '<div class="empty-state"><p>No papers match your filters.</p></div>';
    return;
  }}
  papers.forEach(p => {{
    const div = document.createElement("div");
    div.className = "paper-item";
    div.id = "paper-" + CSS.escape(p.id);
    div.dataset.paperId = p.id;
    if (p.id === selectedId) div.classList.add("selected");

    const typeBadge = getTypeBadge(p.id);
    const yearColor = getTypeColor(p.id);
    const yearBadge = p.year ? '<span class="badge badge-year" style="background:' + yearColor + '">' + p.year + '</span>' : '';
    const hasAuthors = p.authors && p.authors.length > 0;
    const authorsShort = hasAuthors
      ? p.authors.slice(0, 2).join(", ") + (p.authors.length > 2 ? " et al." : "")
      : "";
    const citeText = p.citation_count ? p.citation_count + " cites" : "";

    // Full author list for expanded view
    const authorTags = hasAuthors
      ? (p.authors || []).map(a => '<span class="author-tag">' + escapeHtml(a) + '</span>').join('')
      : '<span class="detail-value" style="color:#94A3B8;font-style:italic">Not available</span>';

    // Abstract or summary for expanded view
    const abstractText = p.abstract || "";
    const abstractHtml = abstractText
      ? '<div class="paper-abstract">' + escapeHtml(abstractText.substring(0, 400)) + (abstractText.length > 400 ? '...' : '') + '</div>'
      : '<div class="paper-abstract" style="color:#94A3B8;font-style:italic">No abstract available</div>';

    // DOI / URL link
    const linkHtml = p.doi
      ? '<a href="https://doi.org/' + escapeHtml(p.doi) + '" target="_blank" style="color:#4361EE;font-size:10px;text-decoration:none">DOI: ' + escapeHtml(p.doi) + '</a>'
      : (p.url ? '<a href="' + escapeHtml(p.url) + '" target="_blank" style="color:#4361EE;font-size:10px;text-decoration:none">Open &rarr;</a>' : '');

    // Convert to Seed button (server mode only, non-seed only)
    var convertBtn = '';
    if (typeof SERVER_MODE !== "undefined" && SERVER_MODE && !SEED_SET.has(p.id)) {{
      convertBtn = '<div class="paper-actions"><button class="convert-seed-btn-list" data-pid="' + escapeHtml(p.id) + '">\u2B06 Convert to Seed</button></div>';
    }}

    div.innerHTML =
      '<div class="paper-title">' + escapeHtml(p.title || "Untitled") + '</div>' +
      '<div class="paper-meta">' +
        typeBadge + yearBadge +
        (authorsShort ? ' <span>' + escapeHtml(authorsShort) + '</span>' : '') +
        (citeText ? ' &middot; <span>' + citeText + '</span>' : '') +
      '</div>' +
      '<div class="paper-details">' +
        (p.year || citeText ? '<div class="paper-detail-section">' +
          '<div class="detail-label">Info</div>' +
          '<div class="detail-value">' + (p.year ? 'Year: ' + p.year : '') + (p.year && citeText ? ' &middot; ' : '') + citeText + '</div>' +
        '</div>' : '') +
        '<div class="paper-detail-section">' +
          '<div class="detail-label">Authors</div>' +
          '<div class="author-list">' + (authorTags || '<span class="detail-value">Unknown</span>') + '</div>' +
        '</div>' +
        '<div class="paper-detail-section">' +
          '<div class="detail-label">Abstract</div>' +
          abstractHtml +
        '</div>' +
        (linkHtml ? '<div class="paper-detail-section">' + linkHtml + '</div>' : '') +
        convertBtn +
      '</div>';

    // Attach convert button event (if present)
    var cBtn = div.querySelector(".convert-seed-btn-list");
    if (cBtn) {{
      cBtn.addEventListener("click", function(e) {{
        e.stopPropagation();
        if (typeof confirmConvertToSeed === "function") {{
          confirmConvertToSeed(p.id);
        }} else {{
          showToast("Convert to seed is only available in serve mode");
        }}
      }});
    }}

    div.addEventListener("mouseenter", () => {{
      if (hoverLock) return;
      hoverLock = true;
      highlightNode(p.id, true);
      smoothFocusNode(p.id);
      setTimeout(() => {{ hoverLock = false; }}, 50);
    }});
    div.addEventListener("mouseleave", () => {{
      if (selectedId !== p.id) highlightNode(p.id, false);
    }});
    div.addEventListener("click", () => {{
      if (selectedId === p.id) {{
        selectedId = null;
        div.classList.remove("selected");
        highlightNode(p.id, false);
      }} else {{
        if (selectedId) {{
          const prev = document.getElementById("paper-" + CSS.escape(selectedId));
          if (prev) prev.classList.remove("selected");
          highlightNode(selectedId, false);
        }}
        selectedId = p.id;
        div.classList.add("selected");
        highlightNode(p.id, true);
        smoothFocusNode(p.id);
      }}
    }});
    list.appendChild(div);
  }});
}}

// ====== Render Source List ======
function renderSourceList() {{
  const list = document.getElementById("source-list");
  const seedPapers = ALL_PAPERS.filter(p => SEED_SET.has(p.id));
  if (seedPapers.length === 0) {{
    list.innerHTML = '<div class="empty-state"><p>No seed papers. The graph is empty.</p></div>';
    return;
  }}
  list.innerHTML = "";
  seedPapers.forEach(p => {{
    const div = document.createElement("div");
    div.className = "source-item";
    // Count connected nodes
    const refCount = VIS_EDGES_DATA.filter(e => e.from === p.id).length;
    const citeCount = VIS_EDGES_DATA.filter(e => e.to === p.id).length;
    div.innerHTML =
      '<div class="source-info">' +
        '<div class="source-title">' + escapeHtml(p.title || "Untitled") + '</div>' +
        '<div class="source-meta">' + (p.year || "N/A") + ' &middot; ' + refCount + ' refs &middot; ' + citeCount + ' cites</div>' +
      '</div>' +
      '<button class="source-delete" data-seed-id="' + escapeHtml(p.id) + '">Remove</button>';
    div.querySelector(".source-delete").addEventListener("click", function() {{
      confirmDeleteSource(p.id);
    }});
    list.appendChild(div);
  }});
}}

// ====== Delete Source ======
function confirmDeleteSource(seedId) {{
  const p = paperById[seedId];
  const name = p ? (p.title || "Untitled").substring(0, 50) : seedId.substring(0, 20);

  const overlay = document.createElement("div");
  overlay.className = "confirm-overlay";
  const dialog = document.createElement("div");
  dialog.className = "confirm-dialog";
  dialog.innerHTML =
    '<h4>Remove Seed Paper?</h4>' +
    '<p>This will remove <strong>' + escapeHtml(name) + '</strong> and its exclusive references/citations from the graph.</p>' +
    '<div class="btn-group">' +
      '<button class="btn-cancel">Cancel</button>' +
      '<button class="btn-danger">Remove</button>' +
    '</div>';
  overlay.appendChild(dialog);
  document.body.appendChild(overlay);
  dialog.querySelector(".btn-cancel").addEventListener("click", function() {{
    overlay.remove();
  }});
  dialog.querySelector(".btn-danger").addEventListener("click", function() {{
    overlay.remove();
    executeDeleteSource(seedId);
  }});
}}

function executeDeleteSource(seedId) {{
  // Server mode: persist deletion via API, then reload
  if (typeof SERVER_MODE !== "undefined" && SERVER_MODE) {{
    showToast("Removing seed...");
    fetch("/api/delete-source", {{
      method: "POST",
      headers: {{"Content-Type": "application/json"}},
      body: JSON.stringify({{seed_id: seedId}}),
    }}).then(function(resp) {{ return resp.json(); }}).then(function(result) {{
      if (result.status === "ok") {{
        showToast(result.message || "Seed removed and saved to JSON");
        setTimeout(function() {{ window.location.reload(); }}, 1000);
      }} else {{
        showToast("Error: " + (result.message || "Failed to delete"));
      }}
    }}).catch(function(err) {{
      showToast("Error: " + err.message);
    }});
    return;
  }}

  // Static mode: client-side only (not persisted)
  const allEdges = edges.get();
  const connectedThroughSeed = new Set();
  allEdges.forEach(e => {{
    if (e.from === seedId) connectedThroughSeed.add(e.to);
    if (e.to === seedId) connectedThroughSeed.add(e.from);
  }});

  const otherSeeds = [...SEED_SET].filter(s => s !== seedId);
  const exclusiveNodes = new Set();
  connectedThroughSeed.forEach(nid => {{
    if (SEED_SET.has(nid)) return;
    let connectedToOther = false;
    allEdges.forEach(e => {{
      if ((e.from === nid && otherSeeds.includes(e.to)) ||
          (e.to === nid && otherSeeds.includes(e.from))) {{
        connectedToOther = true;
      }}
    }});
    if (!connectedToOther) exclusiveNodes.add(nid);
  }});

  const edgesToRemove = allEdges.filter(e =>
    e.from === seedId || e.to === seedId ||
    exclusiveNodes.has(e.from) || exclusiveNodes.has(e.to)
  ).map(e => e.id);
  edges.remove(edgesToRemove);

  const nodesToRemove = [seedId, ...exclusiveNodes];
  nodes.remove(nodesToRemove);

  SEED_SET.delete(seedId);
  nodesToRemove.forEach(nid => {{
    delete paperById[nid];
    delete CLASSIFICATION[nid];
  }});
  ALL_PAPERS = ALL_PAPERS.filter(p => !nodesToRemove.includes(p.id));
  papers = papers.filter(p => !nodesToRemove.includes(p.id));

  renderPaperList();
  renderSourceList();
  showToast("Removed seed and " + exclusiveNodes.size + " exclusive papers");

  if (SEED_SET.size === 0) {{
    document.getElementById("paper-list").innerHTML = '<div class="empty-state"><p>All seeds removed. No papers to display.</p></div>';
  }}

  summaryCache = null;
  summaryState = "idle";
}}

// ====== Graph year color (JS) ======
function getYearColor(year) {{
  if (!year) return "#888888";
  const minY = {min_year}, maxY = {max_year};
  if (minY === maxY) return "#888888";
  const t = (year - minY) / (maxY - minY);
  const colors = [[66,133,244],[52,168,83],[251,188,4],[234,67,53]];
  const idx = t * (colors.length - 1);
  const i = Math.min(Math.floor(idx), colors.length - 2);
  const frac = idx - i;
  const r = Math.round(colors[i][0] + frac * (colors[i+1][0] - colors[i][0]));
  const g = Math.round(colors[i][1] + frac * (colors[i+1][1] - colors[i][1]));
  const b = Math.round(colors[i][2] + frac * (colors[i+1][2] - colors[i][2]));
  return "rgb(" + r + "," + g + "," + b + ")";
}}

// ====== Graph <-> List Interaction ======
let hoverTimeout = null;
network.on("hoverNode", function(params) {{
  if (hoverLock) return;
  clearTimeout(hoverTimeout);
  hoverTimeout = setTimeout(() => {{
    hoverLock = true;
    const pid = params.node;
    showTooltip(pid, params.event);
    highlightListItem(pid, true);
    scrollToListItem(pid);
    setTimeout(() => {{ hoverLock = false; }}, 50);
  }}, 30);
}});

network.on("blurNode", function(params) {{
  clearTimeout(hoverTimeout);
  // Don't hide tooltip if it's pinned (clicked)
  const tt = document.getElementById("node-tooltip");
  if (!tt.classList.contains("pinned")) hideTooltip();
  if (params.node !== selectedId) highlightListItem(params.node, false);
}});

network.on("click", function(params) {{
  if (params.nodes.length > 0) {{
    const pid = params.nodes[0];
    if (selectedId === pid) {{
      selectedId = null;
      highlightListItem(pid, false);
      highlightNode(pid, false);
      hideTooltip();
    }} else {{
      if (selectedId) {{
        highlightListItem(selectedId, false);
        highlightNode(selectedId, false);
      }}
      selectedId = pid;
      highlightListItem(pid, true, true);
      scrollToListItem(pid);
      // Show tooltip pinned on click (stays until next click)
      showTooltip(pid, params.event);
      document.getElementById("node-tooltip").classList.add("pinned");
    }}
  }} else {{
    // Clicked on empty space — clear selection and tooltip
    if (selectedId) {{
      highlightListItem(selectedId, false);
      highlightNode(selectedId, false);
      selectedId = null;
    }}
    hideTooltip();
  }}
}});

function showTooltip(pid, event) {{
  const p = paperById[pid];
  if (!p) return;
  const tooltip = document.getElementById("node-tooltip");
  const ntype = CLASSIFICATION[pid] || "indirect";
  const typeColors = {{ seed: "#6C5CE7", reference: "#0984E3", citation: "#00B894", indirect: "#B2BEC3" }};
  const typeLabels = {{ seed: "Seed Paper", reference: "Reference (cited by seed)", citation: "Citation (cites seed)", indirect: "Indirect" }};
  const authorsText = p.authors && p.authors.length > 0
    ? p.authors.slice(0, 5).join(", ") + (p.authors.length > 5 ? " et al." : "")
    : "Unknown";
  tooltip.innerHTML =
    '<span class="tt-type" style="background:' + typeColors[ntype] + '">' + typeLabels[ntype] + '</span>' +
    '<div class="tt-title">' + escapeHtml(p.title || "Untitled") + '</div>' +
    '<div class="tt-row"><strong>Authors:</strong> ' + escapeHtml(authorsText) + '</div>' +
    '<div class="tt-row"><strong>Year:</strong> ' + (p.year || "N/A") + ' &middot; <strong>Citations:</strong> ' + (p.citation_count || 0) + '</div>' +
    (p.doi ? '<div class="tt-row"><strong>DOI:</strong> ' + escapeHtml(p.doi) + '</div>' : '') +
    (p.abstract ? '<div class="tt-abstract">' + escapeHtml(p.abstract.substring(0, 250)) + (p.abstract.length > 250 ? '...' : '') + '</div>' : '');
  const rect = container.getBoundingClientRect();
  let x = (event.center ? event.center.x : event.clientX || 0) + 15;
  let y = (event.center ? event.center.y : event.clientY || 0) + 15;
  if (x + 400 > window.innerWidth) x = x - 420;
  if (y + 300 > window.innerHeight) y = y - 320;
  tooltip.style.left = x + "px";
  tooltip.style.top = y + "px";
  tooltip.classList.add("visible");
}}

function hideTooltip() {{
  const tt = document.getElementById("node-tooltip");
  tt.classList.remove("visible");
  tt.classList.remove("pinned");
}}

function highlightListItem(pid, on, isSelected) {{
  const el = document.getElementById("paper-" + CSS.escape(pid));
  if (!el) return;
  if (on) {{
    el.classList.add(isSelected ? "selected" : "highlighted");
  }} else {{
    el.classList.remove("highlighted");
    if (!isSelected && pid !== selectedId) el.classList.remove("selected");
  }}
}}

function scrollToListItem(pid) {{
  const el = document.getElementById("paper-" + CSS.escape(pid));
  if (!el) return;
  el.scrollIntoView({{ behavior: "smooth", block: "center" }});
}}

function highlightNode(pid, on) {{
  try {{
    if (on) {{
      const current = nodes.get(pid);
      if (!current) return;
      nodes.update({{
        id: pid,
        borderWidth: 4,
        color: {{
          ...current.color,
          border: "#FF6B35",
          background: "#FF9966",
        }},
        size: (current._origSize || current.size) + 6,
        _origSize: current._origSize || current.size,
        _origColor: current._origColor || current.color,
      }});
    }} else {{
      const current = nodes.get(pid);
      if (!current || !current._origColor) return;
      nodes.update({{
        id: pid,
        borderWidth: SEED_SET.has(pid) ? 3 : 1,
        color: current._origColor,
        size: current._origSize || current.size,
      }});
    }}
  }} catch(e) {{}}
}}

function smoothFocusNode(pid) {{
  const pos = network.getPositions([pid]);
  if (!pos[pid]) return;
  const scale = network.getScale();
  network.moveTo({{
    position: pos[pid],
    scale: Math.max(scale, 0.7),
    animation: {{ duration: 400, easingFunction: "easeInOutCubic" }},
  }});
}}

// ====== Controls ======
function resetView() {{
  // Turn off physics
  physicsEnabled = false;
  network.setOptions({{ physics: {{ enabled: false }} }});
  document.getElementById("btn-physics").textContent = "Physics Off";
  // Restore all nodes to original timeline positions (moveNode preserves styling)
  for (const [id, pos] of Object.entries(ORIGINAL_POSITIONS)) {{
    try {{ network.moveNode(id, pos.x, pos.y); }} catch(e) {{}}
  }}
  // Fit to view
  setTimeout(() => {{
    network.fit({{ animation: {{ duration: 500, easingFunction: "easeInOutCubic" }} }});
  }}, 50);
}}
function fitAll() {{
  network.fit({{ animation: {{ duration: 500, easingFunction: "easeInOutCubic" }} }});
}}
function togglePhysics() {{
  physicsEnabled = !physicsEnabled;
  network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
  document.getElementById("btn-physics").textContent = physicsEnabled ? "Physics On" : "Physics Off";
}}

// ====== Filter & Sort ======
function filterPapers() {{
  const query = document.getElementById("search-box").value.toLowerCase();
  const yearVal = document.getElementById("year-filter").value;
  const typeVal = document.getElementById("type-filter").value;
  papers = ALL_PAPERS.filter(p => {{
    if (yearVal && String(p.year) !== yearVal) return false;
    if (typeVal && CLASSIFICATION[p.id] !== typeVal) return false;
    if (query) {{
      const text = [p.title, ...(p.authors||[]), String(p.year||""), p.source||"", p.abstract||""].join(" ").toLowerCase();
      if (!text.includes(query)) return false;
    }}
    return true;
  }});
  applySortAndRender();
  highlightFilteredNodes();
}}

function highlightFilteredNodes() {{
  const filtered = new Set(papers.map(p => p.id));
  VIS_NODES_DATA.forEach(n => {{
    try {{
      if (filtered.has(n.id)) {{
        nodes.update({{ id: n.id, opacity: 1.0 }});
      }} else {{
        nodes.update({{ id: n.id, opacity: 0.15 }});
      }}
    }} catch(e) {{}}
  }});
}}

function sortPapers() {{ applySortAndRender(); }}

function applySortAndRender() {{
  const sortVal = document.getElementById("sort-select").value;
  papers.sort((a, b) => {{
    switch(sortVal) {{
      case "year-desc": return (b.year||0) - (a.year||0) || (a.title||"").localeCompare(b.title||"");
      case "year-asc": return (a.year||0) - (b.year||0) || (a.title||"").localeCompare(b.title||"");
      case "cite-desc": return (b.citation_count||0) - (a.citation_count||0);
      case "title-asc": return (a.title||"").localeCompare(b.title||"");
      default: return 0;
    }}
  }});
  renderPaperList();
}}

function clearFilters() {{
  document.getElementById("search-box").value = "";
  document.getElementById("year-filter").value = "";
  document.getElementById("type-filter").value = "";
  papers = [...ALL_PAPERS];
  VIS_NODES_DATA.forEach(n => {{
    try {{ nodes.update({{ id: n.id, opacity: 1.0 }}); }} catch(e) {{}}
  }});
  applySortAndRender();
}}

// ====== Export ======
function exportAs(format) {{
  let content, filename, mime;
  const exportPapers = papers;
  if (format === "json") {{
    content = JSON.stringify(exportPapers, null, 2);
    filename = "papers.json"; mime = "application/json";
  }} else if (format === "csv") {{
    const header = "id,title,authors,year,citation_count,type,source,url,doi,abstract";
    const rows = exportPapers.map(p => {{
      return [p.id, csvEscape(p.title), csvEscape((p.authors||[]).join("; ")),
              p.year||"", p.citation_count||0, CLASSIFICATION[p.id]||"", p.source||"", p.url||"", p.doi||"",
              csvEscape((p.abstract||"").substring(0, 300))].join(",");
    }});
    content = header + "\\n" + rows.join("\\n");
    filename = "papers.csv"; mime = "text/csv";
  }} else if (format === "markdown") {{
    const lines = ["# Paper List\\n"];
    exportPapers.forEach((p, i) => {{
      lines.push("## " + (i+1) + ". " + (p.title || "Untitled") + "\\n");
      lines.push("- **Type:** " + (CLASSIFICATION[p.id] || "unknown"));
      lines.push("- **Year:** " + (p.year || "N/A"));
      lines.push("- **Authors:** " + ((p.authors||[]).join(", ") || "Unknown"));
      lines.push("- **Citations:** " + (p.citation_count || 0));
      if (p.source) lines.push("- **Source:** " + p.source);
      if (p.url) lines.push("- **URL:** " + p.url);
      if (p.doi) lines.push("- **DOI:** " + p.doi);
      if (p.abstract) lines.push("- **Abstract:** " + p.abstract.substring(0, 300) + (p.abstract.length > 300 ? "..." : ""));
      lines.push("");
    }});
    content = lines.join("\\n");
    filename = "papers.md"; mime = "text/markdown";
  }}
  const blob = new Blob([content], {{ type: mime }});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = filename;
  a.click();
  URL.revokeObjectURL(a.href);
}}

function csvEscape(str) {{
  if (!str) return "";
  if (str.includes(",") || str.includes('"') || str.includes("\\n")) {{
    return '"' + str.replace(/"/g, '""') + '"';
  }}
  return str;
}}

function copyForLLM() {{
  const seeds = papers.filter(p => SEED_SET.has(p.id));
  const nonSeeds = papers.filter(p => !SEED_SET.has(p.id));

  let text = "# Paper Graph Summary\\n\\n";
  text += "Total: " + papers.length + " papers, " + EDGES.length + " edges, " + seeds.length + " seed papers\\n\\n";

  text += "## Seed Papers\\n\\n";
  seeds.forEach((p, i) => {{
    text += (i+1) + ". " + (p.title || "Untitled") + " (" + (p.year || "?") + ")\\n";
    text += "   Authors: " + ((p.authors||[]).join(", ") || "Unknown") + "\\n";
    text += "   Citations: " + (p.citation_count || 0);
    if (p.doi) text += " | DOI: " + p.doi;
    if (p.url) text += " | URL: " + p.url;
    text += "\\n";
    if (p.abstract) text += "   Abstract: " + p.abstract + "\\n";
    text += "\\n";
  }});

  text += "## Related Papers\\n\\n";
  const sorted = [...nonSeeds].sort((a,b) => (b.citation_count||0) - (a.citation_count||0));
  sorted.forEach((p, i) => {{
    const type = CLASSIFICATION[p.id] || "unknown";
    text += (i+1) + ". [" + type.toUpperCase() + "] " + (p.title || "Untitled") + " (" + (p.year || "?") + ")\\n";
    text += "   Authors: " + ((p.authors||[]).join(", ") || "Unknown");
    text += " | Citations: " + (p.citation_count || 0);
    if (p.doi) text += " | DOI: " + p.doi;
    text += "\\n";
    if (p.abstract) text += "   Abstract: " + p.abstract + "\\n";
    text += "\\n";
  }});

  text += "## Citation Edges\\n\\n";
  text += "Format: [citing paper] -> [cited paper]\\n\\n";
  EDGES.forEach(e => {{
    const src = papers.find(p => p.id === e.from);
    const tgt = papers.find(p => p.id === e.to);
    if (src && tgt) {{
      text += "- " + (src.title||src.id).substring(0,60) + " -> " + (tgt.title||tgt.id).substring(0,60) + "\\n";
    }}
  }});

  navigator.clipboard.writeText(text).then(() => {{
    showToast("Copied " + papers.length + " papers to clipboard — ready to paste into any LLM");
  }}).catch(() => {{
    // Fallback: download as file
    const blob = new Blob([text], {{ type: "text/plain" }});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "papers_for_llm.txt";
    a.click();
    URL.revokeObjectURL(a.href);
    showToast("Downloaded papers_for_llm.txt (clipboard not available)");
  }});
}}

// ====== Summary Panel ======
(function initFab() {{
  const fab = document.getElementById("summary-fab");
  if (PRE_SUMMARY) {{
    fab.title = "View AI Summary (pre-generated)";
  }} else {{
    fab.title = "AI Summary - click to configure";
  }}
}})();

function toggleSummary() {{
  document.getElementById("summary-overlay").classList.add("visible");
  document.getElementById("summary-panel").classList.add("visible");
  if (summaryState === "idle") {{
    if (PRE_SUMMARY) {{
      summaryCache = PRE_SUMMARY;
      summaryState = "done";
      renderSummary(PRE_SUMMARY);
    }} else {{
      showApiKeyForm();
    }}
  }}
}}

function closeSummary() {{
  document.getElementById("summary-overlay").classList.remove("visible");
  document.getElementById("summary-panel").classList.remove("visible");
}}

function resetSummaryForm() {{
  summaryCache = null;
  summaryState = "idle";
  showApiKeyForm();
}}

const LLM_PROVIDERS = [
  {{ name: "openai",     label: "OpenAI",                url: "https://api.openai.com/v1",                                  model: "gpt-4o-mini" }},
  {{ name: "anthropic",  label: "Anthropic (Claude)",     url: "https://api.anthropic.com/v1/",                              model: "claude-sonnet-4-20250514" }},
  {{ name: "gemini",     label: "Google (Gemini)",        url: "https://generativelanguage.googleapis.com/v1beta/openai/",   model: "gemini-2.0-flash" }},
  {{ name: "deepseek",   label: "DeepSeek",               url: "https://api.deepseek.com",                                  model: "deepseek-chat" }},
  {{ name: "groq",       label: "Groq",                   url: "https://api.groq.com/openai/v1",                            model: "llama-3.1-8b-instant" }},
  {{ name: "together",   label: "Together AI",             url: "https://api.together.xyz/v1",                               model: "meta-llama/Llama-3.1-8B-Instruct-Turbo" }},
  {{ name: "fireworks",  label: "Fireworks AI",            url: "https://api.fireworks.ai/inference/v1",                      model: "accounts/fireworks/models/llama-v3p1-8b-instruct" }},
  {{ name: "mistral",    label: "Mistral",                 url: "https://api.mistral.ai/v1",                                 model: "mistral-small-latest" }},
  {{ name: "xai",        label: "xAI (Grok)",             url: "https://api.x.ai/v1",                                       model: "grok-3-mini-fast" }},
  {{ name: "perplexity", label: "Perplexity",              url: "https://api.perplexity.ai",                                 model: "sonar" }},
  {{ name: "openrouter", label: "OpenRouter",              url: "https://openrouter.ai/api/v1",                              model: "meta-llama/llama-3.1-8b-instruct:free" }},
  {{ name: "qwen",       label: "Qwen",                   url: "https://dashscope.aliyuncs.com/compatible-mode/v1",          model: "qwen-turbo" }},
  {{ name: "qwen-code",  label: "Qwen Coding",            url: "https://coding.dashscope.aliyuncs.com/v1",                  model: "qwen-turbo" }},
  {{ name: "zhipu",      label: "Zhipu",                   url: "https://open.bigmodel.cn/api/paas/v4/",                     model: "glm-4-flash" }},
  {{ name: "moonshot",   label: "Moonshot",                url: "https://api.moonshot.cn/v1",                                model: "moonshot-v1-8k" }},
  {{ name: "baichuan",   label: "Baichuan",                url: "https://api.baichuan-ai.com/v1",                            model: "Baichuan2-Turbo" }},
  {{ name: "yi",         label: "Yi",                      url: "https://api.lingyiwanwu.com/v1",                            model: "yi-lightning" }},
  {{ name: "doubao",     label: "Doubao",                  url: "https://ark.cn-beijing.volces.com/api/v3",                  model: "doubao-lite-32k" }},
  {{ name: "minimax",    label: "MiniMax",                 url: "https://api.minimax.io/v1",                                 model: "MiniMax-Text-01" }},
  {{ name: "stepfun",    label: "Stepfun",                 url: "https://api.stepfun.com/v1",                                model: "step-1-flash" }},
  {{ name: "sensenova",  label: "SenseTime",               url: "https://api.sensenova.cn/compatible-mode/v1",               model: "SenseChat-Turbo" }},
  {{ name: "custom",     label: "Custom / Self-hosted",    url: "",                                                          model: "" }},
];

function parseJsonResponse(raw) {{
  let text = raw.trim();
  text = text.replace(/^```(?:json|JSON|javascript|js)?\\s*\\n?/m, "");
  text = text.replace(/\\n?\\s*```\\s*$/m, "");
  text = text.trim();
  try {{ return JSON.parse(text); }} catch(e) {{}}
  const firstBrace = text.indexOf("{{");
  const lastBrace = text.lastIndexOf("}}");
  if (firstBrace !== -1 && lastBrace > firstBrace) {{
    const candidate = text.substring(firstBrace, lastBrace + 1);
    try {{ return JSON.parse(candidate); }} catch(e) {{}}
  }}
  if (firstBrace !== -1) {{
    let candidate = text.substring(firstBrace);
    let cutPoints = [];
    let openBraces = 0, openBrackets = 0, inStr = false, esc = false;
    for (let i = 0; i < candidate.length; i++) {{
      const ch = candidate[i];
      if (esc) {{ esc = false; continue; }}
      if (ch === "\\\\") {{ esc = true; continue; }}
      if (ch === '"') {{ if (inStr) cutPoints.push(i); inStr = !inStr; continue; }}
      if (inStr) continue;
      if (ch === "{{") openBraces++;
      else if (ch === "}}") {{ openBraces--; cutPoints.push(i); }}
      else if (ch === "[") openBrackets++;
      else if (ch === "]") {{ openBrackets--; cutPoints.push(i); }}
    }}
    for (let ci = cutPoints.length - 1; ci >= 0; ci--) {{
      let truncated = candidate.substring(0, cutPoints[ci] + 1);
      truncated = truncated.replace(/,\s*$/, "");
      let ob = 0, ok = 0, ins = false, es = false;
      for (let i = 0; i < truncated.length; i++) {{
        const ch = truncated[i];
        if (es) {{ es = false; continue; }}
        if (ch === "\\\\") {{ es = true; continue; }}
        if (ch === '"') {{ ins = !ins; continue; }}
        if (ins) continue;
        if (ch === "{{") ob++;
        else if (ch === "}}") ob--;
        else if (ch === "[") ok++;
        else if (ch === "]") ok--;
      }}
      let closed = truncated;
      while (ok > 0) {{ closed += "]"; ok--; }}
      while (ob > 0) {{ closed += "}}"; ob--; }}
      try {{
        const recovered = JSON.parse(closed);
        recovered._truncated = true;
        return recovered;
      }} catch(e) {{ continue; }}
    }}
  }}
  const preview = raw.length > 500 ? raw.substring(0, 500) + "..." : raw;
  throw new Error("Could not extract valid JSON from response.\\n\\nResponse preview:\\n" + preview);
}}

function buildAnalysisPrompt() {{
  const topPapers = [...ALL_PAPERS].sort((a,b) => (b.citation_count||0) - (a.citation_count||0)).slice(0, 10);
  const years = ALL_PAPERS.map(p => p.year).filter(Boolean);
  const yearRange = years.length ? Math.min(...years) + "-" + Math.max(...years) : "unknown";
  let paperList = topPapers.map((p, i) => {{
    let entry = (i+1) + '. "' + p.title + '" (' + (p.year || "N/A") + ", " + (p.citation_count || 0) + " cites)";
    if (p.authors && p.authors.length) entry += " - " + p.authors.slice(0,2).join(", ");
    if (p.abstract) entry += "\\n   " + p.abstract.substring(0, 150);
    return entry;
  }}).join("\\n");
  const remainingPapers = [...ALL_PAPERS].sort((a,b) => (b.citation_count||0) - (a.citation_count||0)).slice(10, 50);
  let remainingList = "";
  if (remainingPapers.length > 0) {{
    remainingList = "\\n\\nOther papers:\\n" + remainingPapers.map(p => "- " + p.title + " (" + (p.year || "?") + ")").join("\\n");
  }}
  return "Analyze " + ALL_PAPERS.length + " academic papers (" + yearRange + ").\\n\\nTop papers:\\n" + paperList + remainingList +
    "\\n\\nYears: " + YEAR_DIST.map(function(d){{ return d[0]+":"+d[1]; }}).join(", ") +
    "\\nSources: " + SOURCE_DIST.map(function(d){{ return d[0]+":"+d[1]; }}).join(", ") +
    "\\n\\nRespond with ONLY a JSON object (no markdown, no extra text). Keep each value concise." +
    '\\nRequired keys: "overview" (3-5 sentences), "main_topics" (array of {{"topic","description"}}), "research_trends" (array of 3-5 strings), "notable_venues" (array), "potential_gaps" (array of 2-4 strings).';
}}

let currentTab = "manual";

function showApiKeyForm() {{
  const body = document.getElementById("summary-body");
  const tabs = document.createElement("div");
  tabs.className = "mode-tabs";
  const btnManual = document.createElement("button");
  btnManual.className = "mode-tab" + (currentTab === "manual" ? " active" : "");
  btnManual.textContent = "Manual (Copy/Paste)";
  btnManual.addEventListener("click", function() {{ switchTab("manual"); }});
  const btnAuto = document.createElement("button");
  btnAuto.className = "mode-tab" + (currentTab === "auto" ? " active" : "");
  btnAuto.textContent = "Auto (API Call)";
  btnAuto.addEventListener("click", function() {{ switchTab("auto"); }});
  tabs.appendChild(btnManual);
  tabs.appendChild(btnAuto);
  body.innerHTML = "";
  body.appendChild(tabs);
  const tabContent = document.createElement("div");
  tabContent.id = "tab-content";
  body.appendChild(tabContent);
  renderTab();
}}

function switchTab(tab) {{
  currentTab = tab;
  document.querySelectorAll(".mode-tab").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(".mode-tab").forEach(el => {{
    if ((tab === "manual" && el.textContent.includes("Manual")) ||
        (tab === "auto" && el.textContent.includes("Auto")))
      el.classList.add("active");
  }});
  renderTab();
}}

function renderTab() {{
  const c = document.getElementById("tab-content");
  if (currentTab === "manual") renderManualTab(c);
  else renderAutoTab(c);
}}

function renderManualTab(c) {{
  const prompt = buildAnalysisPrompt();
  c.innerHTML = '<div class="manual-mode">' +
    '<div class="step">' +
      '<div class="step-label"><span class="step-num">1</span> Copy this prompt</div>' +
      '<textarea id="prompt-text" rows="5" readonly>' + escapeHtml(prompt) + '</textarea>' +
      '<div class="btn-row"><button class="btn-primary" onclick="copyPrompt()">Copy</button>' +
      '<span class="copied-toast" id="copy-toast">Copied!</span></div>' +
    '</div>' +
    '<div class="step">' +
      '<div class="step-label"><span class="step-num">2</span> Paste into any LLM and get the JSON response</div>' +
    '</div>' +
    '<div class="step">' +
      '<div class="step-label"><span class="step-num">3</span> Paste the response here</div>' +
      '<textarea id="response-text" rows="6" placeholder="Paste JSON response here..."></textarea>' +
      '<div class="btn-row"><button class="btn-primary" onclick="submitManualResponse()">Show Summary</button>' +
      '<button class="btn-secondary" onclick="resetSummaryForm()">Reset</button></div>' +
    '</div></div>';
}}

function renderAutoTab(c) {{
  const savedKey = sessionStorage.getItem("_opg_api_key") || "";
  const savedUrl = sessionStorage.getItem("_opg_base_url") || "";
  const savedModel = sessionStorage.getItem("_opg_model") || "";
  const savedProvider = sessionStorage.getItem("_opg_provider") || "openai";
  const opts = LLM_PROVIDERS.map(p =>
    '<option value="' + p.name + '"' + (p.name === savedProvider ? " selected" : "") + '>' + p.label + '</option>'
  ).join("");
  c.innerHTML = '<div class="api-key-form">' +
    '<p>Select provider and enter API key. Key is stored <strong>only in session</strong>.<br>' +
    '<span style="color:#E74C3C;font-size:11px;">May fail due to CORS on local files. Use Manual tab if needed.</span></p>' +
    '<div class="form-row"><select id="provider-select" onchange="onProviderChange()">' + opts + '</select></div>' +
    '<input type="password" id="api-key-input" placeholder="API Key" value="' + escapeHtml(savedKey) + '">' +
    '<div class="form-row"><input type="text" id="base-url-input" placeholder="Base URL" value="' + escapeHtml(savedUrl) + '">' +
    '<input type="text" id="model-input" placeholder="Model" value="' + escapeHtml(savedModel) + '"></div>' +
    '<button class="submit-btn" onclick="submitApiKey()">Generate Summary</button>' +
    '<p class="hint">Supports 20+ providers. Use <code>export-html --summary</code> to pre-generate (recommended).</p></div>';
  if (!savedUrl) onProviderChange();
}}

function copyPrompt() {{
  const text = document.getElementById("prompt-text").value;
  navigator.clipboard.writeText(text).then(() => {{
    const toast = document.getElementById("copy-toast");
    toast.classList.add("show");
    setTimeout(() => toast.classList.remove("show"), 2000);
  }}).catch(() => {{
    document.getElementById("prompt-text").select();
    document.execCommand("copy");
  }});
}}

function submitManualResponse() {{
  const raw = document.getElementById("response-text").value.trim();
  if (!raw) {{ alert("Please paste the LLM response."); return; }}
  try {{
    const result = parseJsonResponse(raw);
    summaryCache = result;
    summaryState = "done";
    renderSummary(result);
  }} catch (e) {{
    alert("Failed to parse response as JSON.\\n\\n" + e.message);
  }}
}}

function onProviderChange() {{
  const sel = document.getElementById("provider-select");
  const provider = LLM_PROVIDERS.find(p => p.name === sel.value);
  if (provider) {{
    document.getElementById("base-url-input").value = provider.url;
    document.getElementById("model-input").value = provider.model;
  }}
}}

function submitApiKey() {{
  const key = document.getElementById("api-key-input").value.trim();
  const url = document.getElementById("base-url-input").value.trim();
  const model = document.getElementById("model-input").value.trim();
  const provider = document.getElementById("provider-select").value;
  if (!key) {{ alert("Please enter an API key."); return; }}
  if (!url) {{ alert("Please select a provider or enter a Base URL."); return; }}
  if (!model) {{ alert("Please enter a model name."); return; }}
  sessionStorage.setItem("_opg_api_key", key);
  sessionStorage.setItem("_opg_base_url", url);
  sessionStorage.setItem("_opg_model", model);
  sessionStorage.setItem("_opg_provider", provider);
  generateSummaryWithKey(key, url, model);
}}

async function generateSummaryWithKey(apiKey, baseUrl, model) {{
  if (summaryCache) {{ renderSummary(summaryCache); return; }}
  summaryState = "loading";
  const body = document.getElementById("summary-body");
  body.innerHTML = '<div class="summary-loading"><div class="spinner"></div><p>Generating summary...</p></div>';
  try {{
    const prompt = buildAnalysisPrompt();
    const endpoint = baseUrl + (baseUrl.endsWith("/") ? "" : "/") + "chat/completions";
    const response = await fetch(endpoint, {{
      method: "POST",
      headers: {{ "Content-Type": "application/json", "Authorization": "Bearer " + apiKey }},
      body: JSON.stringify({{
        model: model,
        messages: [
          {{ role: "system", content: "You are a research assistant. Respond with ONLY a valid JSON object. No markdown, no extra text. Keep descriptions concise." }},
          {{ role: "user", content: prompt }},
        ],
        temperature: 0.3,
        max_tokens: 8000,
      }}),
    }});
    if (!response.ok) throw new Error("API returned " + response.status + ": " + response.statusText);
    const data = await response.json();
    const text = data.choices[0].message.content;
    const result = parseJsonResponse(text);
    summaryCache = result;
    summaryState = "done";
    renderSummary(result);
  }} catch (err) {{
    summaryState = "error";
    const body = document.getElementById("summary-body");
    const isCors = err.message === "Load failed" || err.message === "Failed to fetch" || err.message.includes("NetworkError");
    body.innerHTML = '<div class="summary-error">' +
      '<p>Failed to generate summary</p>' +
      '<p style="font-size:12px;color:#64748B;margin-top:8px;">' + escapeHtml(err.message) + '</p>' +
      (isCors ? '<p style="font-size:12px;color:#64748B;margin-top:4px;">This is likely a <strong>CORS error</strong>. Use the <strong>Manual</strong> tab instead.</p>' : '') +
      '<button onclick="resetSummaryForm()">' + (isCors ? 'Switch to Manual' : 'Retry') + '</button></div>';
    if (isCors) currentTab = "manual";
  }}
}}

function renderSummary(result) {{
  const body = document.getElementById("summary-body");
  let h = '';
  const years = ALL_PAPERS.map(p => p.year).filter(Boolean);
  h += '<div class="summary-section"><h4>Collection Stats</h4>' +
    '<p><strong>Total:</strong> ' + ALL_PAPERS.length + ' papers &middot; <strong>Years:</strong> ' +
    (years.length ? Math.min(...years) + "-" + Math.max(...years) : "N/A") +
    ' &middot; <strong>Sources:</strong> ' + SOURCE_DIST.length + '</p></div>';
  if (result.overview || result.summary) {{
    h += '<div class="summary-section"><h4>Overview</h4><p>' + escapeHtml(result.overview || result.summary) + '</p></div>';
  }}
  if (result.main_topics && result.main_topics.length) {{
    h += '<div class="summary-section"><h4>Main Topics</h4><ul>';
    result.main_topics.forEach(t => {{
      const topic = typeof t === "string" ? t : (t.topic || t.label || "");
      const desc = typeof t === "string" ? "" : (t.description || "");
      h += '<li><strong>' + escapeHtml(topic) + '</strong>' + (desc ? ": " + escapeHtml(desc) : "") + '</li>';
    }});
    h += '</ul></div>';
  }}
  if (result.research_trends && result.research_trends.length) {{
    h += '<div class="summary-section"><h4>Research Trends</h4><ul>';
    result.research_trends.forEach(t => {{
      h += '<li>' + escapeHtml(typeof t === "string" ? t : t.description || JSON.stringify(t)) + '</li>';
    }});
    h += '</ul></div>';
  }}
  if (result.notable_venues && result.notable_venues.length) {{
    h += '<div class="summary-section"><h4>Notable Venues</h4><ul>';
    result.notable_venues.forEach(v => {{
      h += '<li>' + escapeHtml(typeof v === "string" ? v : v.venue || v.name || JSON.stringify(v)) + '</li>';
    }});
    h += '</ul></div>';
  }}
  if (result.potential_gaps && result.potential_gaps.length) {{
    h += '<div class="summary-section"><h4>Potential Gaps</h4><ul>';
    result.potential_gaps.forEach(g => {{
      h += '<li>' + escapeHtml(typeof g === "string" ? g : g.gap || g.description || JSON.stringify(g)) + '</li>';
    }});
    h += '</ul></div>';
  }}
  if (result.suggested_directions && result.suggested_directions.length) {{
    h += '<div class="summary-section"><h4>Suggested Directions</h4><ul>';
    result.suggested_directions.forEach(d => {{
      h += '<li>' + escapeHtml(typeof d === "string" ? d : JSON.stringify(d)) + '</li>';
    }});
    h += '</ul></div>';
  }}
  if (result.key_findings && result.key_findings.length) {{
    h += '<div class="summary-section"><h4>Key Findings</h4><ul>';
    result.key_findings.forEach(f => {{
      h += '<li>' + escapeHtml(typeof f === "string" ? f : JSON.stringify(f)) + '</li>';
    }});
    h += '</ul></div>';
  }}
  const expectedKeys = ["overview", "main_topics", "research_trends", "notable_venues", "potential_gaps"];
  const presentKeys = expectedKeys.filter(k => result[k] && (!Array.isArray(result[k]) || result[k].length > 0));
  if (result._truncated || presentKeys.length < 3) {{
    h += '<div class="summary-section" style="background:#FFF8E1;padding:12px;border-radius:8px;border:1px solid #FFE082;">' +
      '<p style="margin:0;font-size:13px;color:#F57F17;">Response appears truncated (' + presentKeys.length + '/' + expectedKeys.length + ' sections). ' +
      'Try the Manual tab with a web-based LLM for complete output.</p>' +
      '<button style="margin-top:8px;font-size:12px;padding:6px 14px;border:1px solid #F57F17;border-radius:6px;background:#fff;color:#F57F17;cursor:pointer;" onclick="resetSummaryForm()">Retry</button></div>';
  }}
  body.innerHTML = h;
}}

// ====== Init ======
renderPaperList();
</script>
</body>
</html>'''
