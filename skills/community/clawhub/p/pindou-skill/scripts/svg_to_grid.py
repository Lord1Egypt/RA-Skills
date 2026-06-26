"""
svg_to_grid: raw.svg (一格一个 <rect fill="rgb(R,G,B)">) -> grid.json + quantized.png

把 "vision 阶段" 和 "snap+render 阶段" 解耦的胶水脚本:
  - vision 阶段产出 raw.svg (Claude/VLM/extract_svg 都行, 只要遵守同样的 SVG 形状)
  - 本脚本: SVG -> grid_rgb (gh, gw, 3) -> 复用 quantize 里的 snap pipeline -> grid.json
  - 然后 render_pattern.py 拿 grid.json 出最终图纸

usage:
    python scripts/svg_to_grid.py \\
        --svg outputs/run/raw.svg \\
        --spec outputs/run/spec.json \\
        --palette palettes/mard_221.csv \\
        --out-dir outputs/run/
"""

import argparse
import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from quantize import (
    build_grid_json,
    detect_bg_and_pure_fg_masks,
    enforce_must_include,
    filter_palette,
    load_palette,
    palette_first_topk,
    palette_idx_of_color,
    quantize_to_palette,
    render_quantized_png,
)

SVG_NS = "{http://www.w3.org/2000/svg}"
RGB_RE = re.compile(r"rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)")
HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})")


def parse_fill(fill: str) -> tuple[int, int, int]:
    m = RGB_RE.match(fill or "")
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3))
    m = HEX_RE.match(fill or "")
    if m:
        h = m.group(1)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    raise ValueError(f"unrecognised fill: {fill!r} (need rgb(R,G,B) or #RRGGBB)")


def parse_svg_to_grid(svg_path: Path) -> np.ndarray:
    """
    解析 raw.svg, 返回 (gh, gw, 3) uint8 数组。

    SVG 必须满足 extract_svg.py 的形状:
      <g data-grid-w=".." data-grid-h="..">
        <rect data-row=".." data-col=".." fill="rgb(R,G,B)"/>
        ...
      </g>
    """
    root = ET.parse(svg_path).getroot()
    g = root.find(f"{SVG_NS}g")
    if g is None:
        raise ValueError(f"{svg_path}: no <g> wrapper found")
    gw = int(g.get("data-grid-w", "0"))
    gh = int(g.get("data-grid-h", "0"))
    if gw <= 0 or gh <= 0:
        raise ValueError(f"{svg_path}: <g> missing data-grid-w/data-grid-h")

    out = np.zeros((gh, gw, 3), dtype=np.uint8)
    seen = np.zeros((gh, gw), dtype=bool)
    for rect in g.findall(f"{SVG_NS}rect"):
        try:
            r = int(rect.get("data-row"))
            c = int(rect.get("data-col"))
        except (TypeError, ValueError):
            raise ValueError(
                f"{svg_path}: <rect> missing data-row/data-col"
            )
        if not (0 <= r < gh and 0 <= c < gw):
            raise ValueError(
                f"{svg_path}: cell ({r},{c}) outside {gh}x{gw}"
            )
        out[r, c] = parse_fill(rect.get("fill"))
        seen[r, c] = True

    if not seen.all():
        miss = int((~seen).sum())
        raise ValueError(f"{svg_path}: {miss}/{gh * gw} cells missing")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--palette", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    palette_full = load_palette(Path(args.palette))
    palette = filter_palette(
        palette_full,
        spec.get("palette_subset"),
        spec.get("forbid_colors"),
    )

    grid_rgb = parse_svg_to_grid(Path(args.svg))
    gh, gw, _ = grid_rgb.shape
    print(f"[svg_to_grid] parsed grid: {gw} x {gh} = {gw * gh} cells")

    bg_mask = None
    pure_fg_mask = None
    bg_hex = spec.get("background_color")
    if spec.get("background_mode") in ("solid", "remove") and bg_hex:
        bg_mask, pure_fg_mask = detect_bg_and_pure_fg_masks(grid_rgb, bg_hex)
        print(
            f"[svg_to_grid] bg (跳过): {int(bg_mask.sum())} cells | "
            f"内部白窟窿 (强制 snap): {int(pure_fg_mask.sum())} cells"
        )

    quant_exclude = bg_mask
    if pure_fg_mask is not None:
        quant_exclude = (bg_mask | pure_fg_mask) if bg_mask is not None else pure_fg_mask
    fg_mask_quant = ~quant_exclude if quant_exclude is not None else None

    max_colors = spec.get("max_colors")
    if max_colors:
        idx_grid = palette_first_topk(
            grid_rgb, palette, int(max_colors), fg_mask=fg_mask_quant
        )
    else:
        idx_grid = quantize_to_palette(grid_rgb, palette)

    if pure_fg_mask is not None and pure_fg_mask.any() and bg_hex:
        bg_pal_idx = palette_idx_of_color(palette, bg_hex)
        idx_grid[pure_fg_mask] = bg_pal_idx

    idx_grid = enforce_must_include(idx_grid, palette, spec.get("must_include_colors") or [])

    # spec 里 grid_w/grid_h 仅作"建议", 真值以 SVG 为准
    spec["grid_w"] = gw
    spec["grid_h"] = gh

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    grid_json = build_grid_json(idx_grid, palette, spec, bg_mask=bg_mask)
    (out_dir / "grid.json").write_text(
        json.dumps(grid_json, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    render_quantized_png(
        idx_grid, palette, spec.get("cell_px", 40),
        out_dir / "quantized.png", bg_mask=bg_mask,
    )
    print(f"[svg_to_grid] grid -> {out_dir / 'grid.json'}")
    print(f"[svg_to_grid] quantized.png -> {out_dir / 'quantized.png'}")
    print(
        f"[svg_to_grid] {len(grid_json['bom'])} distinct colors; "
        f"{grid_json['bead_count']} beads (skipped {grid_json['bg_cells']} bg cells); "
        f"top 5: {[b['code'] for b in grid_json['bom'][:5]]}"
    )


if __name__ == "__main__":
    main()
