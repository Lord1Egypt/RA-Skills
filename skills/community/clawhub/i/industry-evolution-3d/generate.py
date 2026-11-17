#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
industry-evolution-3d generator
================================
Reads an input.json (domain milestone data), inlines person avatars / brand
logos / the world map as base64, injects them into template.html, and produces
a self-contained, offline-openable index.html (a 3D spatiotemporal graph:
world map as base + a raised time axis + geo-coordinated nodes + hover cards).

Usage:
    python3 generate.py input.json [output.html]

Dependencies (first run):
    pip install Pillow requests

See SKILL.md or examples/ai_history_sample.json for the input.json schema.
"""
import sys, json, base64, io, os, mimetypes, urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Missing Pillow. Run first: pip install Pillow requests")


def fetch_bytes(src: str):
    """src may be a local path or an http(s) URL; returns (bytes, content_type)."""
    if src.startswith("http://") or src.startswith("https://"):
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.read(), (r.headers.get_content_type() or "")
    p = Path(src)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {src}")
    return p.read_bytes(), (mimetypes.guess_type(str(p))[0] or "")


def inline_image(src: str, kind: str = "logo") -> str:
    """Convert an image into a data URI. A portrait is cropped to a circle and
    resized to 256; logos / map are shrunk as much as possible."""
    raw, ctype = fetch_bytes(src)
    is_svg = ("svg" in ctype) or str(src).lower().endswith(".svg")
    if is_svg:
        b64 = base64.b64encode(raw).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"

    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    if kind == "portrait":
        s = min(img.width, img.height)
        img = img.crop(((img.width - s) // 2, (img.height - s) // 2,
                        (img.width + s) // 2, (img.height + s) // 2))
        img = img.resize((256, 256))
    else:  # logo / map
        max_side = 1024 if kind == "map" else 512
        img.thumbnail((max_side, max_side), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_data_block(data: dict) -> str:
    meta = data.get("meta", {})
    ymin = int(meta.get("yearMin", 1940))
    ymax = int(meta.get("yearMax", 2026))
    axis_h = int(meta.get("axisH", 120))
    axis_base = int(meta.get("axisBase", 10))
    map_w = int(meta.get("mapWidth", 200))
    map_d = int(meta.get("mapDepth", 100))

    ticks = data.get("yearTicks")
    if not ticks:
        ticks = list(range((ymin // 10) * 10, ymax + 1, 10))
        if ticks[-1] != ymax:
            ticks.append(ymax)

    portraits, logos = {}, {}
    for pid, src in data.get("portraits", {}).items():
        portraits[pid] = inline_image(src, "portrait")
    for key, src in data.get("logos", {}).items():
        logos[key] = inline_image(src, "logo")
    map_src = inline_image(data["map"], "map") if data.get("map") else None

    block = f"""
const YEAR_MIN = {ymin}, YEAR_MAX = {ymax};
const AXIS_H = {axis_h}, AXIS_BASE = {axis_base};
const MAP_W = {map_w}, MAP_D = {map_d};
const YEARS_TICKS = {json.dumps(ticks, ensure_ascii=False)};
const MILESTONES = {json.dumps(data.get('milestones', []), ensure_ascii=False)};
const PORTRAITS = {json.dumps(portraits, ensure_ascii=False)};
const LOGO_SVGS = {json.dumps(logos, ensure_ascii=False)};
const BRAND_MAP = {json.dumps(data.get('brandMap', {}), ensure_ascii=False)};
const WIKI = {json.dumps(data.get('wiki', {}), ensure_ascii=False)};
const BAIKE = {json.dumps(data.get('baike', {}), ensure_ascii=False)};
const MAP_SRC = {json.dumps(map_src)};
"""
    return block


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 generate.py input.json [output.html]")
    inp = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("index.html")
    data = json.loads(inp.read_text(encoding="utf-8"))

    tpl_path = Path(__file__).parent / "template.html"
    tpl = tpl_path.read_text(encoding="utf-8")

    meta = data.get("meta", {})
    tpl = tpl.replace("{{TITLE}}", meta.get("title", "Industry Evolution Spatiotemporal Graph"))
    tpl = tpl.replace("{{SUBTITLE}}", meta.get("subtitle", ""))
    tpl = tpl.replace("/*__DATA__*/", build_data_block(data))

    if "/*__DATA__*/" in tpl:
        raise RuntimeError("Data injection marker was not replaced; check template.html")
    if "{{TITLE}}" in tpl or "{{SUBTITLE}}" in tpl:
        raise RuntimeError("Title placeholder was not replaced")

    out.write_text(tpl, encoding="utf-8")
    print(f"✓ Generated: {out}  ({out.stat().st_size/1024:.1f} KB)")
    print(f"  Nodes: {len(data.get('milestones', []))}  Map: {'yes' if data.get('map') else 'no (solid-color base)'}")


if __name__ == "__main__":
    main()
