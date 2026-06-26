#!/usr/bin/env python3
"""
detect_charts.py — Extract chart data from HTML and generate pptxgenjs snippets.

Detects:
  Chart.js       — new Chart(ctx, { type, data, options })
  ECharts        — setOption({ series, xAxis, yAxis, ... })
  CSS conic-gradient — pie approximation
  Static SVG     — bar/line/pie shapes from svg_inventory.json (parse_html output)
  Bare <canvas>  — unmatched canvas elements flagged for manual fill

Reads from tmp/ (parse_html.py outputs, if present):
  layout_map.json     → actual canvas x/y/w/h positions (replaces hardcoded defaults)
  svg_inventory.json  → static SVG chart data

Outputs:
  <tmp>/charts.json   — structured data + ready-to-paste gen.js snippets

Usage:
  python3 detect_charts.py input.html
  python3 detect_charts.py input.html --out ./tmp
"""

import sys, os, re, json, argparse

ap = argparse.ArgumentParser()
ap.add_argument("input")
ap.add_argument("--out", default=None)
args = ap.parse_args()

INPUT_HTML = os.path.abspath(args.input)
OUT_DIR    = os.path.abspath(args.out) if args.out \
             else os.path.join(os.path.dirname(INPUT_HTML), "tmp")
os.makedirs(OUT_DIR, exist_ok=True)

with open(INPUT_HTML, "r", encoding="utf-8") as f:
    html = f.read()

# ── Load parse_html.py side-outputs if available ─────────────────────────────
def _load_json(filename):
    p = os.path.join(OUT_DIR, filename)
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return None

layout_map    = _load_json("layout_map.json")
svg_inventory = _load_json("svg_inventory.json")
design_spec   = _load_json("design_spec.json")

SCALE  = (design_spec or {}).get("body", {}).get("scale_factor") or 0.0078125
X_OFF  = (design_spec or {}).get("body", {}).get("x_offset_inches") or 0.0
Y_OFF  = (design_spec or {}).get("body", {}).get("y_offset_inches") or 0.0

# Default palette (fallback only — real colors extracted from HTML first)
PALETTE = ["0891b2","22c55e","7c3aed","f59e0b","ef4444",
           "3b82f6","10b981","f97316","8b5cf6","06b6d4"]

TYPE_MAP = {
    "radar":"radar","line":"line","area":"line","bar":"bar",
    "horizontalBar":"bar","horizontalbar":"bar",
    "pie":"pie","doughnut":"doughnut",
    "scatter":"scatter","bubble":"bubble",
    "gauge":"doughnut","funnel":"bar","heatmap":"bar",
    "effectscatter":"scatter","lines":"line","pictorialbar":"bar",
}


# ═════════════════════════════════════════════════════════════════════════════
# CORE PARSING HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def strip_comments(s):
    s = re.sub(r"//[^\n]*", "", s)
    return re.sub(r"/\*.*?\*/", "", s, flags=re.DOTALL)

def extract_balanced(text, start_pos, open_c, close_c):
    depth = 0
    for i, c in enumerate(text[start_pos:], start_pos):
        if c == open_c:    depth += 1
        elif c == close_c:
            depth -= 1
            if depth == 0: return text[start_pos:i+1]
    return text[start_pos:]

def parse_array(s):
    """Parse a JS array string into Python list, preserving numbers."""
    s = s.strip().strip("[]")
    items = []
    for part in re.split(r",(?![^[{]*[}\]])", s):
        p = part.strip().strip("\"'`").strip()
        if not p: continue
        try:    items.append(int(p))
        except:
            try: items.append(float(p))
            except: items.append(p)
    return items

def find_string(text, *keys):
    for key in keys:
        m = re.search(rf"\b{key}\s*:\s*['\"`]([^'\"`]+)['\"`]", text)
        if m: return m.group(1).strip()
    return ""

def find_number(text, *keys):
    """Find a numeric value for any of the given keys."""
    for key in keys:
        m = re.search(rf"\b{key}\s*:\s*(-?[\d.]+)", text)
        if m:
            try:    return int(m.group(1))
            except: return float(m.group(1))
    return None

def find_array(text, *keys):
    for key in keys:
        m = re.search(rf"\b{key}\s*:\s*(\[)", text, re.DOTALL)
        if m:
            block = extract_balanced(text, m.start(1), "[", "]")
            return parse_array(block)
    return []

def extract_top_objects(s):
    objects, depth, start = [], 0, None
    for i, c in enumerate(s):
        if c == "{":
            if depth == 0: start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and start is not None:
                objects.append(s[start:i+1]); start = None
    return objects

def extract_series_block(snippet):
    m = re.search(r"\bseries\s*:\s*\[", snippet)
    if not m: return None
    return extract_balanced(snippet, m.end()-1, "[", "]")

def normalize_color(s):
    """Normalize a CSS color string to 6-char hex. Returns None if not parseable."""
    s = s.strip().strip("'\"` ")
    if not s or s in ("none","transparent","inherit"): return None
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3: h = h[0]*2 + h[1]*2 + h[2]*2
        return h[:6].lower() if re.match(r"^[0-9a-fA-F]{6}", h) else None
    m = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)", s)
    if m: return "{:02x}{:02x}{:02x}".format(int(m.group(1)),int(m.group(2)),int(m.group(3)))
    return None

def extract_color_array(text, *keys):
    """Extract an array of colors from backgroundColor / borderColor etc."""
    for key in keys:
        m = re.search(rf"\b{key}\s*:\s*(\[)", text, re.DOTALL)
        if m:
            block = extract_balanced(text, m.start(1), "[", "]")
            raw   = parse_array(block)
            cols  = [normalize_color(str(c)) for c in raw]
            cols  = [c for c in cols if c]
            if cols: return cols
        # Single color (not array)
        m2 = re.search(rf"\b{key}\s*:\s*['\"`]([^'\"`]+)['\"`]", text)
        if m2:
            c = normalize_color(m2.group(1))
            if c: return [c]
    return []


# ═════════════════════════════════════════════════════════════════════════════
# POSITION LOOKUP — read actual canvas coords from layout_map.json
# ═════════════════════════════════════════════════════════════════════════════

def canvas_position(canvas_id=None, canvas_index=0):
    """
    Try to find the rendered position of a canvas element.
    Returns (x, y, w, h) in inches for pptxgenjs.
    Falls back to evenly-spaced defaults if layout_map not available.
    """
    if layout_map:
        nodes = layout_map.get("all_nodes", [])
        # Match by html_id
        if canvas_id:
            for n in nodes:
                if n.get("html_id","") == canvas_id:
                    ppt = n.get("ppt_coords", {})
                    if ppt.get("x_in") is not None:
                        return (
                            round(ppt.get("x_in", 0.5), 4),
                            round(ppt.get("y_in", 0.5), 4),
                            round(ppt.get("w_in", 5.5), 4),
                            round(ppt.get("h_in", 3.5), 4),
                        )
        # Match by index order among canvas tags
        canvas_nodes = [n for n in nodes if n.get("tag") == "canvas"]
        if canvas_index < len(canvas_nodes):
            ppt = canvas_nodes[canvas_index].get("ppt_coords", {})
            if ppt.get("x_in") is not None:
                return (
                    round(ppt.get("x_in", 0.5), 4),
                    round(ppt.get("y_in", 0.5), 4),
                    round(ppt.get("w_in", 5.5), 4),
                    round(ppt.get("h_in", 3.5), 4),
                )
    # Default: stack charts vertically
    slide_w = (design_spec or {}).get("body", {}).get("slide_w_inches") or 10.0
    slide_h = (design_spec or {}).get("body", {}).get("slide_h_inches") or 5.625
    w, h = round(slide_w * 0.55, 2), round(slide_h * 0.65, 2)
    x = round((slide_w - w) / 2, 2)
    y = round(0.4 + canvas_index * (h + 0.2), 2)
    return (x, y, w, h)


# ═════════════════════════════════════════════════════════════════════════════
# CHART.JS EXTRACTOR
# ═════════════════════════════════════════════════════════════════════════════

def extract_chartjs(html):
    results = []
    canvas_idx = 0

    for m in re.finditer(r"new\s+Chart\s*\(\s*([^,]+),\s*\{", html):
        canvas_ref = m.group(1).strip().strip("'\"")
        snippet    = strip_comments(extract_balanced(html, m.end()-1, "{", "}"))

        type_m  = re.search(r"\btype\s*:\s*['\"](\w+)['\"]", snippet)
        js_type = type_m.group(1) if type_m else "bar"
        js_type_lc = js_type.lower()
        labels  = find_array(snippet, "labels")
        datasets = []

        # ── Axis options ──────────────────────────────────────────────────
        # Chart.js v2: options.scales.yAxes[0] / Chart.js v3: options.scales.y
        axis_info = {}
        scales_m = re.search(r"\bscales\s*:\s*\{", snippet)
        if scales_m:
            scales_block = extract_balanced(snippet, scales_m.end()-1, "{", "}")
            # v3 style: y: { min, max, title }
            y_m = re.search(r"\by\s*:\s*\{", scales_block)
            if y_m:
                y_block = extract_balanced(scales_block, y_m.end()-1, "{", "}")
                axis_info["val_min"]   = find_number(y_block, "min", "suggestedMin")
                axis_info["val_max"]   = find_number(y_block, "max", "suggestedMax")
                axis_info["val_title"] = find_string(y_block, "text", "label")
            x_m = re.search(r"\bx\s*:\s*\{", scales_block)
            if x_m:
                x_block = extract_balanced(scales_block, x_m.end()-1, "{", "}")
                axis_info["cat_title"] = find_string(x_block, "text", "label")
            # v2 style: yAxes array
            if "val_min" not in axis_info or axis_info["val_min"] is None:
                ya_m = re.search(r"\byAxes\s*:\s*\[", scales_block)
                if ya_m:
                    ya_block = extract_balanced(scales_block, ya_m.end()-1, "[", "]")
                    axis_info["val_min"] = find_number(ya_block, "min", "suggestedMin")
                    axis_info["val_max"] = find_number(ya_block, "max", "suggestedMax")

        # ── Horizontal bar detection ──────────────────────────────────────
        is_horizontal = js_type_lc in ("horizontalbar",)
        # Also detect Chart.js v3 indexAxis:'y'
        if re.search(r"\bindexAxis\s*:\s*['\"]y['\"]", snippet):
            is_horizontal = True
        axis_info["is_horizontal"] = is_horizontal

        # ── Stacking detection ────────────────────────────────────────────
        is_stacked = bool(re.search(r"\bstacked\s*:\s*true", snippet))
        axis_info["is_stacked"] = is_stacked

        # ── Datasets ─────────────────────────────────────────────────────
        ds_m = re.search(r"\bdatasets\s*:\s*\[", snippet)
        if ds_m:
            ds_block = extract_balanced(snippet, ds_m.end()-1, "[", "]")
            for obj in extract_top_objects(ds_block):
                name   = find_string(obj, "label", "name") or f"Series{len(datasets)+1}"
                values = find_array(obj, "data")
                nums   = [v for v in values if isinstance(v,(int,float))]
                if not nums: continue
                # ★ Extract actual colors
                colors = extract_color_array(obj,
                    "backgroundColor","borderColor","pointBackgroundColor")
                datasets.append({"name": name, "values": nums, "colors": colors})

        if not datasets:
            canvas_idx += 1
            continue

        # ★ Canvas position from layout_map
        x, y, w, h = canvas_position(canvas_ref, canvas_idx)
        canvas_idx += 1

        results.append({
            "source":      "chartjs",
            "js_type":     js_type_lc,
            "pptx_type":   TYPE_MAP.get(js_type_lc, "bar"),
            "title":       find_string(snippet, "text", "title"),
            "labels":      labels,
            "datasets":    datasets,
            "axis_info":   {k: v for k, v in axis_info.items() if v is not None and v != False},
            "position":    {"x": x, "y": y, "w": w, "h": h},
        })
    return results


# ═════════════════════════════════════════════════════════════════════════════
# ECHARTS EXTRACTOR
# ═════════════════════════════════════════════════════════════════════════════

def extract_echarts(html):
    results = []
    chart_idx = 0

    for m in re.finditer(r"setOption\s*\(\s*\{", html):
        snippet   = strip_comments(extract_balanced(html, m.end()-1, "{", "}"))

        # ── Type detection ────────────────────────────────────────────────
        type_m    = re.search(r"\bseries\b.*?type\s*:\s*['\"](\w+)['\"]", snippet, re.DOTALL)
        js_type   = type_m.group(1).lower() if type_m else "bar"
        pptx_type = TYPE_MAP.get(js_type, "bar")

        # ── Horizontal bar: yAxis has type:'category' ─────────────────────
        is_horizontal = False
        yaxis_m = re.search(r"\byAxis\b[^{]*\{([^}]+)\}", snippet)
        if yaxis_m and "category" in yaxis_m.group(1):
            is_horizontal = True

        # ── Stacked bar: any series has stack property ────────────────────
        is_stacked = bool(re.search(r"\bstack\s*:\s*['\"\w]", snippet))

        # ── Axis titles ───────────────────────────────────────────────────
        axis_info = {"is_horizontal": is_horizontal, "is_stacked": is_stacked}
        xn_m = re.search(r"\bxAxis\b[^{]*\{([^}]{0,300})\}", snippet)
        if xn_m:
            axis_info["cat_title"] = find_string(xn_m.group(1), "name") or None
        yn_m = re.search(r"\byAxis\b[^{]*\{([^}]{0,300})\}", snippet)
        if yn_m:
            axis_info["val_title"] = find_string(yn_m.group(1), "name") or None
            axis_info["val_min"]   = find_number(yn_m.group(1), "min")
            axis_info["val_max"]   = find_number(yn_m.group(1), "max")

        # ── Labels ───────────────────────────────────────────────────────
        labels = []
        if js_type == "radar":
            ind_m = re.search(r"\bindicator\s*:\s*\[", snippet)
            if ind_m:
                ind_block = extract_balanced(snippet, ind_m.end()-1, "[", "]")
                labels = [find_string(o,"name") for o in extract_top_objects(ind_block)]
                labels = [l for l in labels if l]
        if not labels:
            if is_horizontal:
                # horizontal: categories are on yAxis
                ya_m = re.search(r"\byAxis\b[^[]*\bdata\s*:\s*\[", snippet, re.DOTALL)
                if ya_m:
                    block  = extract_balanced(snippet, ya_m.end()-1, "[", "]")
                    labels = [str(v) for v in parse_array(block)]
            if not labels:
                xa_m = re.search(r"\bxAxis\b[^[]*\bdata\s*:\s*\[", snippet, re.DOTALL)
                if xa_m:
                    block  = extract_balanced(snippet, xa_m.end()-1, "[", "]")
                    labels = [str(v) for v in parse_array(block)]

        # ── Datasets ─────────────────────────────────────────────────────
        datasets = []
        series_block = extract_series_block(snippet)
        if series_block:
            for obj in extract_top_objects(series_block):
                name = find_string(obj, "name") or f"Series{len(datasets)+1}"
                data_m = re.search(r"\bdata\s*:\s*\[", obj)
                if not data_m: continue
                data_block = extract_balanced(obj, data_m.end()-1, "[", "]")
                # Radar: [{value:[...]}]
                val_m = re.search(r"\bvalue\s*:\s*\[([^\]]+)\]", data_block)
                if val_m:
                    values = parse_array(val_m.group(1))
                else:
                    values = parse_array(data_block)
                nums = [v for v in values if isinstance(v,(int,float))]
                if not nums: continue

                # ★ Extract itemStyle.color per series or per data point
                colors = []
                # Per-series color
                item_m = re.search(r"\bitemStyle\s*:\s*\{([^}]+)\}", obj)
                if item_m:
                    c = normalize_color(find_string(item_m.group(1), "color"))
                    if c: colors = [c]
                # Per-point colors (data: [{value:x, itemStyle:{color:'...'}}])
                point_colors = []
                for pt_obj in extract_top_objects(data_block):
                    pt_item = re.search(r"\bitemStyle\s*:\s*\{([^}]+)\}", pt_obj)
                    if pt_item:
                        c = normalize_color(find_string(pt_item.group(1),"color"))
                        point_colors.append(c or "")
                if any(point_colors): colors = [c for c in point_colors if c]

                datasets.append({"name": name, "values": nums, "colors": colors})

        if not datasets: continue

        # ★ Find container div → look up position
        # ECharts mounts to a DOM element; look for the div before setOption
        # Try to find echarts.init(document.getElementById('xxx')) before this match
        pre = html[:m.start()]
        init_m = re.search(r"echarts\.init\s*\([^)]*getElementById\s*\(['\"]([^'\"]+)['\"]",
                           pre[-2000:])
        container_id = init_m.group(1) if init_m else None
        x, y, w, h = canvas_position(container_id, chart_idx)
        chart_idx += 1

        title_m = re.search(r"\btitle\b[^{]*\{([^}]+)\}", snippet)
        title   = find_string(title_m.group(1),"text") if title_m else ""

        results.append({
            "source":    "echarts",
            "js_type":   js_type,
            "pptx_type": pptx_type,
            "title":     title,
            "labels":    labels,
            "datasets":  datasets,
            "axis_info": {k: v for k, v in axis_info.items() if v is not None and v is not False},
            "position":  {"x": x, "y": y, "w": w, "h": h},
        })
    return results


# ═════════════════════════════════════════════════════════════════════════════
# CSS CONIC-GRADIENT → PIE
# ═════════════════════════════════════════════════════════════════════════════

def extract_conic(html):
    results = []
    for conic in re.findall(r"conic-gradient\(([^)]+)\)", html):
        stops = re.findall(r"(#[0-9a-fA-F]{3,8}|rgba?\([^)]+\))\s+([\d.]+)%", conic)
        if len(stops) < 2: continue
        labels = [f"Segment{i+1}" for i in range(len(stops))]
        values, prev = [], 0.0
        for _, pct in stops:
            p = float(pct); values.append(round(p-prev,1)); prev=p
        # ★ Keep actual colors from CSS
        colors = [normalize_color(s[0]) or PALETTE[i%len(PALETTE)]
                  for i,s in enumerate(stops)]
        # Position: find parent element with this gradient
        x, y, w, h = canvas_position(None, len(results))
        results.append({
            "source":   "css_conic",
            "js_type":  "pie", "pptx_type": "pie",
            "title":    "",
            "labels":   labels,
            "datasets": [{"name":"Segments","values":values,"colors":[]}],
            "colors":   colors,
            "position": {"x":x,"y":y,"w":w,"h":h},
            "note":     "Replace Segment labels with real names",
        })
    return results


# ═════════════════════════════════════════════════════════════════════════════
# STATIC SVG CHART RECONSTRUCTION
# ★ NEW: bridges svg_inventory.json → addChart() or addShape() snippets
# ═════════════════════════════════════════════════════════════════════════════

def _group_rects_as_bars(elements):
    """
    Heuristic: if SVG contains multiple <rect> elements with same y-baseline
    and varying heights, treat as a bar chart.
    Returns (labels, values, colors) or None.
    """
    rects = [e for e in elements if e.get("tag") == "rect"]
    if len(rects) < 2: return None

    try:
        bottoms = [float(e.get("y",0)) + float(e.get("height",0)) for e in rects]
        heights = [float(e.get("height",0)) for e in rects]
    except (ValueError, TypeError):
        return None

    # Bars should share a common baseline (within 2px tolerance)
    baseline_counts = {}
    for b in bottoms:
        key = round(b)
        baseline_counts[key] = baseline_counts.get(key,0) + 1
    dominant_baseline = max(baseline_counts, key=baseline_counts.get)
    bar_rects = [r for r,b in zip(rects,bottoms) if abs(round(b)-dominant_baseline)<3]

    if len(bar_rects) < 2: return None

    bar_rects.sort(key=lambda r: float(r.get("x",0)))
    values = [round(float(r.get("height",0)),1) for r in bar_rects]
    colors = [normalize_color(r.get("fill","")) for r in bar_rects]
    colors = [c or PALETTE[i%len(PALETTE)] for i,c in enumerate(colors)]
    labels = [f"Bar{i+1}" for i in range(len(bar_rects))]

    return labels, values, colors

def _group_texts_as_labels(elements, bar_count):
    """Extract <text> elements that look like axis labels."""
    texts = [e for e in elements
             if e.get("tag") in ("text","tspan") and e.get("text_content","").strip()]
    if len(texts) >= bar_count:
        # Sort by x to match bar order
        texts.sort(key=lambda t: float(t.get("x",0)))
        return [t.get("text_content","").strip() for t in texts[:bar_count]]
    return []

def extract_svg_charts(svg_inventory):
    """
    Analyze svg_inventory.json to find chart-like SVG structures.
    Returns list of chart dicts compatible with make_snippet().
    """
    if not svg_inventory: return []
    results = []

    for svg in svg_inventory.get("svgs", []):
        elements = svg.get("elements", [])
        if not elements: continue

        tag_counts = svg.get("tag_counts", {})
        n_rect     = tag_counts.get("rect", 0)
        n_line     = tag_counts.get("line", 0)
        n_text     = tag_counts.get("text", 0) + tag_counts.get("tspan", 0)
        n_path     = tag_counts.get("path", 0)
        n_circle   = tag_counts.get("circle", 0)

        # ── Heuristic: bar chart (rects on same baseline) ─────────────────
        bar_result = None
        if n_rect >= 2:
            bar_result = _group_rects_as_bars(elements)

        if bar_result:
            labels, values, colors = bar_result
            # Try to replace placeholder labels with actual SVG text
            text_labels = _group_texts_as_labels(elements, len(labels))
            if text_labels: labels = text_labels

            # ★ Use SVG's own position (viewBox → actual pixel size → PPT coords)
            vb = svg.get("viewBox","")
            svg_w_px = float(svg.get("width","").replace("px","") or
                             (vb.split()[2] if len(vb.split())>=3 else "0") or 0)
            svg_h_px = float(svg.get("height","").replace("px","") or
                             (vb.split()[3] if len(vb.split())>=4 else "0") or 0)

            # Find this SVG's position via layout_map inline_styled_elements or positioned_elements
            svg_x, svg_y = X_OFF, Y_OFF
            if layout_map:
                for n in layout_map.get("all_nodes",[]):
                    if n.get("tag") == "svg":
                        ppt = n.get("ppt_coords",{})
                        if ppt.get("x_in") is not None:
                            svg_x = ppt.get("x_in", X_OFF)
                            svg_y = ppt.get("y_in", Y_OFF)
                            break

            w_in = round(svg_w_px * SCALE, 4) if svg_w_px else 4.5
            h_in = round(svg_h_px * SCALE, 4) if svg_h_px else 2.8

            results.append({
                "source":    f"svg_static_{svg['svg_index']}",
                "js_type":   "bar",
                "pptx_type": "bar",
                "title":     "",
                "labels":    labels,
                "datasets":  [{"name":"Series1","values":values,"colors":[]}],
                "colors":    colors,
                "position":  {"x": svg_x, "y": svg_y, "w": w_in, "h": h_in},
                "axis_info": {},
                "note":      (f"Reconstructed from static SVG #{svg['svg_index']}. "
                              f"Verify bar values — heights used as proxy for data values. "
                              f"Replace with actual data if available."),
            })
            continue

        # ── Heuristic: line chart (lines + circles) ───────────────────────
        if n_line >= 3 and (n_circle >= 2 or n_text >= 2):
            lines_els = [e for e in elements if e.get("tag") == "line"]
            # Data lines: exclude long horizontal/vertical axis lines
            data_lines = []
            for ln in lines_els:
                try:
                    dx = abs(float(ln.get("x2",0)) - float(ln.get("x1",0)))
                    dy = abs(float(ln.get("y2",0)) - float(ln.get("y1",0)))
                    if dy > 2 or (dx < 5 and dy > 0):  # non-horizontal = data segment
                        data_lines.append(ln)
                except (ValueError, TypeError):
                    pass

            if len(data_lines) >= 2:
                values = [round(abs(float(ln.get("y1",0)) - float(ln.get("y2",0))),1)
                          for ln in data_lines]
                labels = _group_texts_as_labels(elements, len(values))
                if not labels: labels = [f"Point{i+1}" for i in range(len(values))]
                stroke_colors = [normalize_color(ln.get("stroke","")) for ln in data_lines]
                colors = [c or PALETTE[0] for c in stroke_colors]
                vb = svg.get("viewBox","")
                svg_w_px = float(svg.get("width","").replace("px","") or
                                 (vb.split()[2] if len(vb.split())>=3 else "0") or 0)
                svg_h_px = float(svg.get("height","").replace("px","") or
                                 (vb.split()[3] if len(vb.split())>=4 else "0") or 0)
                w_in = round(svg_w_px * SCALE, 4) if svg_w_px else 4.5
                h_in = round(svg_h_px * SCALE, 4) if svg_h_px else 2.8
                results.append({
                    "source":    f"svg_static_{svg['svg_index']}",
                    "js_type":   "line",
                    "pptx_type": "line",
                    "title":     "",
                    "labels":    labels,
                    "datasets":  [{"name":"Series1","values":values,"colors":[]}],
                    "colors":    [c for c in set(colors) if c][:1] or [PALETTE[0]],
                    "position":  {"x": X_OFF, "y": Y_OFF, "w": w_in, "h": h_in},
                    "axis_info": {},
                    "note":      (f"Reconstructed from static SVG #{svg['svg_index']} (line chart heuristic). "
                                  f"Values = segment heights as proxy. Verify with source data."),
                })
                continue

        # ── Fallback: flag SVG for manual handling ─────────────────────────
        if n_path > 0 or (n_rect >= 2 and n_line >= 1):
            results.append({
                "source":    f"svg_static_{svg['svg_index']}",
                "js_type":   "unknown",
                "pptx_type": "bar",
                "title":     "",
                "labels":    [],
                "datasets":  [],
                "colors":    [],
                "position":  {"x": X_OFF, "y": Y_OFF, "w": 4.5, "h": 2.8},
                "axis_info": {},
                "note":      (f"SVG #{svg['svg_index']} contains chart-like elements "
                              f"({n_rect} rects, {n_line} lines, {n_path} paths, {n_circle} circles) "
                              f"but could not be auto-reconstructed. "
                              f"Options: (A) use slide.addImage() with SVG→PNG export, "
                              f"(B) manually write addChart() with data from source."),
            })

    return results


# ═════════════════════════════════════════════════════════════════════════════
# UNMATCHED CANVAS
# ═════════════════════════════════════════════════════════════════════════════

def extract_canvas(html, found):
    results = []
    all_json = json.dumps(found)
    for i, m in enumerate(re.finditer(r"<canvas[^>]*\bid=['\"]([^'\"]+)['\"]", html, re.I)):
        cid = m.group(1)
        if cid not in all_json:
            x, y, w, h = canvas_position(cid, i)
            results.append({
                "source":   "canvas_unmatched",
                "js_type":  "unknown", "pptx_type": "bar",
                "title":    f"Canvas #{cid}",
                "labels":   [], "datasets":  [], "colors":   [],
                "position": {"x":x,"y":y,"w":w,"h":h},
                "axis_info":{},
                "note":     f"<canvas id='{cid}'> found but no chart library matched — fill data manually",
            })
    return results


# ═════════════════════════════════════════════════════════════════════════════
# SNIPPET GENERATOR — full pptxgenjs options
# ═════════════════════════════════════════════════════════════════════════════

def make_snippet(ch, idx):
    pos = ch.get("position", {})
    x   = pos.get("x", 0.5); y = pos.get("y", 0.5)
    w   = pos.get("w", 5.5); h = pos.get("h", 3.5)

    if not ch["datasets"]:
        return (f"// Chart {idx+1} ({ch['source']} / {ch['js_type']}): data not extracted\n"
                f"// Position: x:{x}, y:{y}, w:{w}, h:{h}\n"
                f"// slide.addChart(pres.ChartType.bar, data, {{ x:{x}, y:{y}, w:{w}, h:{h} }});")

    pt   = ch["pptx_type"]
    labs = list(ch["labels"])
    sets = [dict(ds) for ds in ch["datasets"]]
    ai   = ch.get("axis_info", {})

    # ── Resolve colors ────────────────────────────────────────────────────
    # For pie/doughnut: need one color per data point → use ch["colors"]
    # For bar/line:     one color per dataset → per-dataset colors
    if pt in ("pie","doughnut"):
        # Colors are per-segment: ch["colors"] (from conic) or datasets[0].colors
        seg_colors = (ch.get("colors") or
                      (sets[0].get("colors") if sets else None) or
                      PALETTE[:len(sets[0]["values"]) if sets else 0])
        chart_colors = seg_colors
    else:
        # One color per dataset — prefer per-dataset color if available
        chart_colors = []
        for i, ds in enumerate(sets):
            dc = ds.get("colors")
            if dc:
                chart_colors.append(dc[0])  # first color in dataset
            else:
                chart_colors.append(PALETTE[i % len(PALETTE)])

    # ── Align label/value lengths ─────────────────────────────────────────
    for ds in sets:
        if not labs:
            labs = [f"Item{i+1}" for i in range(len(ds["values"]))]
        while len(ds["values"]) < len(labs): ds["values"].append(0)
        ds["values"] = ds["values"][:len(labs)]

    # ── Dataset lines ─────────────────────────────────────────────────────
    ds_lines = [
        f'  {{ name:{json.dumps(ds["name"],ensure_ascii=False)}, '
        f'labels:[{",".join(json.dumps(str(l),ensure_ascii=False) for l in labs)}], '
        f'values:[{",".join(str(v) for v in ds["values"])}] }}'
        for ds in sets
    ]
    data_str = "[\n" + ",\n".join(ds_lines) + "\n]"

    # ── Options ───────────────────────────────────────────────────────────
    opts = [f"  x:{x}, y:{y}, w:{w}, h:{h}"]

    # ★ Chart title
    title = ch.get("title","")
    if title:
        opts.append(f"  title: {{ title: {json.dumps(title,ensure_ascii=False)}, fontSize: 14, bold: true }}")

    # ★ Colors — correct format per chart type
    if pt in ("pie","doughnut"):
        # pptxgenjs pie: chartColors is array per segment
        opts.append(f"  chartColors: [{','.join(repr(str(c)) for c in chart_colors[:len(labs)])}]")
    else:
        opts.append(f"  chartColors: [{','.join(repr(str(c)) for c in chart_colors[:len(sets)])}]")

    # Legend
    if pt in ("pie","doughnut"):
        opts.append("  showLegend: true, legendPos: 'r'")
    else:
        opts.append("  showLegend: true, legendPos: 'b', legendFontSize: 10")

    # Data labels
    opts.append("  showValue: true")
    if pt == "bar":
        opts.append("  dataLabelPosition: 'outEnd', dataLabelFontSize: 9")
    elif pt == "line":
        opts.append("  dataLabelPosition: 'top', dataLabelFontSize: 9")
    elif pt in ("pie","doughnut"):
        opts.append("  dataLabelPosition: 'bestFit', dataLabelFontSize: 9")
        opts.append("  showPercent: true")
    else:
        opts.append("  dataLabelFontSize: 9")

    # ★ Bar direction
    if pt == "bar":
        bar_dir = "bar" if ai.get("is_horizontal") else "col"
        grouping = "stacked" if ai.get("is_stacked") else "clustered"
        opts.append(f"  barDir: '{bar_dir}', barGrouping: '{grouping}'")
        if ai.get("is_stacked"):
            opts.append("  barGapWidthPct: 70")

    # Doughnut hole
    if pt == "doughnut":
        opts.append("  holeSize: 50")

    # Line symbols
    if pt == "line":
        opts.append("  lineDataSymbol: 'circle', lineDataSymbolSize: 6, lineSize: 2")

    # Radar
    if pt == "radar":
        opts.append("  radarStyle: 'filled'")

    # ★ Axis min/max
    if ai.get("val_min") is not None:
        opts.append(f"  valAxisMinVal: {ai['val_min']}")
    if ai.get("val_max") is not None:
        opts.append(f"  valAxisMaxVal: {ai['val_max']}")

    # ★ Axis titles
    if ai.get("cat_title"):
        opts.append(f"  catAxisTitle: {json.dumps(ai['cat_title'],ensure_ascii=False)}, showCatAxisTitle: true")
    if ai.get("val_title"):
        opts.append(f"  valAxisTitle: {json.dumps(ai['val_title'],ensure_ascii=False)}, showValAxisTitle: true")

    # Gridlines (subtle)
    if pt not in ("pie","doughnut","radar"):
        opts.append("  valGridLine: { style: 'solid', color: 'D0D0D0', pt: 0.5 }")
        opts.append("  valAxisLabelFontSize: 9, catAxisLabelFontSize: 9")

    title_display = title or f"{pt} chart"
    return (f"// Chart {idx+1}: {title_display}  [{ch['source']}]\n"
            f"slide.addChart(pres.ChartType.{pt}, {data_str}, {{\n"
            + ",\n".join(opts) + ",\n}});")


# ═════════════════════════════════════════════════════════════════════════════
# RUN
# ═════════════════════════════════════════════════════════════════════════════

detected  = extract_chartjs(html)
detected += extract_echarts(html)
detected += extract_conic(html)
detected += extract_svg_charts(svg_inventory)   # ★ NEW
detected += extract_canvas(html, detected)

for i, ch in enumerate(detected):
    if "colors" not in ch:
        ds = ch.get("datasets", [])
        if ch.get("pptx_type") in ("pie", "doughnut"):
            n_colors = len(ds[0].get("values", [])) if ds else 1
        else:
            n_colors = len(ds) if ds else 1
        ch["colors"] = PALETTE[:max(1, n_colors)]
    ch["genjs_snippet"] = make_snippet(ch, i)

out_path = os.path.join(OUT_DIR, "charts.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(detected, f, ensure_ascii=False, indent=2)

# ── Console output ─────────────────────────────────────────────────────────
print(f"\n{'='*62}")
print(f"  Chart Detection: {os.path.basename(INPUT_HTML)}")
print(f"{'='*62}")
print(f"  Found {len(detected)} chart(s)"
      + (f"  [layout_map: {'yes' if layout_map else 'no — positions are estimates'}]" ) )
print()

for i, ch in enumerate(detected):
    note = ch.get("note","")
    pos  = ch.get("position",{})
    print(f"  [{i+1}] {ch['source']:<22} type={ch['pptx_type']:<10} "
          f"datasets={len(ch['datasets'])}  labels={len(ch['labels'])}  "
          f"pos=({pos.get('x','?')},{pos.get('y','?')}) "
          f"{pos.get('w','?')}x{pos.get('h','?')}\"")
    if note:
        print(f"       ⚠  {note[:80]}")

if any(ch["datasets"] for ch in detected):
    print(f"\n{'─'*62}")
    print(f"  gen.js snippets:")
    print(f"  (positions read from layout_map.json; adjust if needed)")
    print(f"{'─'*62}")
    for ch in detected:
        if ch["datasets"]:
            print(); print(ch["genjs_snippet"])

print(f"\n  Output: {out_path}")
if not layout_map:
    print(f"  TIP: Run parse_html.py first to get accurate chart positions.")
if svg_inventory and svg_inventory.get("svg_count",0) > 0 and not any("svg_static" in c["source"] for c in detected):
    print(f"  TIP: SVGs found in svg_inventory.json but no bar/line patterns detected.")
    print(f"       Consider exporting SVGs as PNG and using slide.addImage().")
print(f"{'='*62}\n")
