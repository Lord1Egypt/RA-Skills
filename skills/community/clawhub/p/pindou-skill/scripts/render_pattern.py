"""
render_pattern: grid.json + palette -> pattern.svg + pattern.png + bom.csv

SVG 结构:
  <g id="cells">       每格 <rect fill=hex data-code=A4>
  <g id="grid_lines">  浅灰 1px
  <g id="row_labels">  左侧行号 1..H
  <g id="col_labels">  顶部列号 1..W
  <g id="color_codes"> 每格中心色号文本 (字体大小自动适应 cell_px)
  <g id="bom">         右侧色号清单 + 数量

usage:
    python scripts/render_pattern.py \\
        --grid outputs/run/grid.json \\
        --palette palettes/mard_221.csv \\
        --out-dir outputs/run/ \\
        --cell-px 40
"""

import argparse
import csv
import json
from pathlib import Path
from xml.sax.saxutils import escape

CELL_PX_DEFAULT = 40
LABEL_BAND_PX = 36   # left/top label strip
BOM_BAND_PX = 320    # right side BOM panel

GRID_LINE_COLOR = "#D0D0D0"
GRID_LINE_W = 1
LABEL_FONT = "'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', 'Noto Sans', Arial, sans-serif"
LABEL_FONT_PX = 14
CODE_FONT_PX_RATIO = 0.42  # text height = cell_px * 0.42 (was 0.32 — bumped for legibility)
BOM_TITLE_PX = 22
BOM_LINE_PX = 18


def load_palette_lookup(csv_path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with csv_path.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["code"]] = {
                "code": row["code"],
                "hex": row["hex"],
                "name_zh": row.get("name_zh", ""),
                "name_en": row.get("name_en", ""),
            }
    return out


def luminance(hex_color: str) -> float:
    """Perceived luminance 0..1; used to pick black/white text on each cell."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def build_svg(
    grid: dict,
    palette: dict[str, dict],
    cell_px: int,
    show_grid_numbers: bool,
    show_color_codes: bool,
    bom_required: bool,
) -> str:
    W, H = grid["size"]
    cells = grid["cells"]

    label_w = LABEL_BAND_PX if show_grid_numbers else 0
    label_h = LABEL_BAND_PX if show_grid_numbers else 0
    bom_w = BOM_BAND_PX if bom_required else 0

    canvas_w = label_w + W * cell_px + bom_w
    canvas_h = label_h + H * cell_px

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{canvas_w}" height="{canvas_h}" '
        f'viewBox="0 0 {canvas_w} {canvas_h}" '
        f'font-family="{LABEL_FONT}">'
    )
    parts.append(f'<rect width="{canvas_w}" height="{canvas_h}" fill="white"/>')

    # cells (skip None = background)
    parts.append('<g id="cells">')
    for r, row in enumerate(cells):
        for c, code in enumerate(row):
            if code is None:
                continue
            color = palette.get(code, {"hex": "#FF00FF"})["hex"]
            x = label_w + c * cell_px
            y = label_h + r * cell_px
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_px}" height="{cell_px}" '
                f'fill="{color}" data-code="{escape(code)}"/>'
            )
    parts.append("</g>")

    # color codes (skip None = background)
    if show_color_codes:
        font_px = max(8, round(cell_px * CODE_FONT_PX_RATIO))
        parts.append(f'<g id="color_codes" font-size="{font_px}" text-anchor="middle">')
        for r, row in enumerate(cells):
            for c, code in enumerate(row):
                if code is None:
                    continue
                color = palette.get(code, {"hex": "#FF00FF"})["hex"]
                fill = "#000000" if luminance(color) > 0.55 else "#FFFFFF"
                cx = label_w + c * cell_px + cell_px / 2
                cy = label_h + r * cell_px + cell_px / 2 + font_px * 0.35
                parts.append(
                    f'<text x="{cx:.1f}" y="{cy:.1f}" fill="{fill}">{escape(code)}</text>'
                )
        parts.append("</g>")

    # grid lines
    parts.append(
        f'<g id="grid_lines" stroke="{GRID_LINE_COLOR}" '
        f'stroke-width="{GRID_LINE_W}" shape-rendering="crispEdges">'
    )
    for c in range(W + 1):
        x = label_w + c * cell_px
        parts.append(
            f'<line x1="{x}" y1="{label_h}" x2="{x}" y2="{label_h + H * cell_px}"/>'
        )
    for r in range(H + 1):
        y = label_h + r * cell_px
        parts.append(
            f'<line x1="{label_w}" y1="{y}" x2="{label_w + W * cell_px}" y2="{y}"/>'
        )
    parts.append("</g>")

    # row + col labels
    if show_grid_numbers:
        parts.append(
            f'<g id="col_labels" font-size="{LABEL_FONT_PX}" '
            f'text-anchor="middle" fill="#444">'
        )
        for c in range(W):
            x = label_w + c * cell_px + cell_px / 2
            y = label_h - 8
            parts.append(f'<text x="{x:.1f}" y="{y}">{c + 1}</text>')
        parts.append("</g>")
        parts.append(
            f'<g id="row_labels" font-size="{LABEL_FONT_PX}" '
            f'text-anchor="end" fill="#444">'
        )
        for r in range(H):
            x = label_w - 8
            y = label_h + r * cell_px + cell_px / 2 + LABEL_FONT_PX * 0.35
            parts.append(f'<text x="{x}" y="{y:.1f}">{r + 1}</text>')
        parts.append("</g>")

    # BOM panel
    if bom_required:
        bom = grid.get("bom", [])
        bead_count = grid.get("bead_count", sum(b["count"] for b in bom))
        bx = label_w + W * cell_px + 20
        title_y = label_h + BOM_TITLE_PX + 4
        parts.append(f'<g id="bom" font-size="{BOM_LINE_PX}" fill="#222">')
        parts.append(
            f'<text x="{bx}" y="{title_y}" font-size="{BOM_TITLE_PX}" font-weight="bold">'
            f'色号清单 (共 {len(bom)} 色 · {bead_count} 颗豆)</text>'
        )
        line_h = BOM_LINE_PX + 12
        sw_size = BOM_LINE_PX + 6
        for i, b in enumerate(bom):
            yy = title_y + BOM_LINE_PX + 4 + i * line_h
            sw_x = bx
            tx = bx + sw_size + 12
            parts.append(
                f'<rect x="{sw_x}" y="{yy - sw_size + 2}" width="{sw_size}" height="{sw_size}" '
                f'fill="{b["hex"]}" stroke="#888"/>'
            )
            name = palette.get(b["code"], {}).get("name_zh", "")
            label = f'{b["code"]}  ×{b["count"]}'
            if name:
                label += f'  · {name}'
            parts.append(f'<text x="{tx}" y="{yy + 2}">{escape(label)}</text>')
        parts.append("</g>")

    parts.append("</svg>")
    return "".join(parts)


def write_bom_csv(grid: dict, palette: dict[str, dict], out_path: Path) -> None:
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["code", "hex", "name_zh", "name_en", "count"])
        for b in grid.get("bom", []):
            p = palette.get(b["code"], {})
            w.writerow([b["code"], b["hex"], p.get("name_zh", ""),
                        p.get("name_en", ""), b["count"]])


def try_render_png(svg_path: Path, png_path: Path) -> bool:
    try:
        import cairosvg
    except ImportError:
        print("[render] cairosvg not installed; skipping pattern.png "
              "(SVG itself is the source of truth, open it in a browser).")
        return False
    cairosvg.svg2png(url=str(svg_path), write_to=str(png_path))
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grid", required=True)
    ap.add_argument("--palette", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--cell-px", type=int, default=CELL_PX_DEFAULT)
    ap.add_argument("--no-grid-numbers", action="store_true")
    ap.add_argument("--no-color-codes", action="store_true")
    ap.add_argument("--no-bom", action="store_true")
    args = ap.parse_args()

    grid = json.loads(Path(args.grid).read_text(encoding="utf-8"))
    palette = load_palette_lookup(Path(args.palette))

    svg = build_svg(
        grid, palette, args.cell_px,
        show_grid_numbers=not args.no_grid_numbers,
        show_color_codes=not args.no_color_codes,
        bom_required=not args.no_bom,
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    svg_path = out_dir / "pattern.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(f"[render] SVG -> {svg_path}")

    if not args.no_bom:
        bom_csv = out_dir / "bom.csv"
        write_bom_csv(grid, palette, bom_csv)
        print(f"[render] BOM -> {bom_csv}")

    png_path = out_dir / "pattern.png"
    if try_render_png(svg_path, png_path):
        print(f"[render] PNG -> {png_path}")


if __name__ == "__main__":
    main()
