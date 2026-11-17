#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
照片转拼豆图纸转换器 (Photo to Perler Bead Pattern Converter)

将一张照片像素化并映射到拼豆调色板，生成可打印的 HTML 图纸、PNG 预览图和材料清单。

依赖: Pillow (PIL)
    pip install Pillow

用法:
    python perler_converter.py <输入图片> [选项]

示例:
    python perler_converter.py photo.jpg --width 29 --output ./result
    python perler_converter.py cat.png --width 50 --palette artkal --show-codes --cell 18
    python perler_converter.py avatar.jpg --width 20 --dither
"""

import argparse
import os
import sys
import html
import json
from collections import Counter

try:
    from PIL import Image, ImageDraw
except ImportError:
    sys.stderr.write(
        "[错误] 缺少 Pillow 库。请先安装:\n"
        "  pip install Pillow\n"
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# 拼豆调色板
# 每个条目: (编号, 颜色名称(中), 颜色名称(英), (R, G, B))
# 基于常见 5mm 拼豆通用颜色 (Artkal C 系列 / Perler 常用色合并去重)
# ---------------------------------------------------------------------------

PERLER_PALETTE = [
    ("P01", "白色",       "White",         (255, 255, 255)),
    ("P02", "奶油色",     "Cream",         (244, 234, 193)),
    ("P03", "浅灰",       "Light Gray",    (200, 200, 200)),
    ("P04", "银灰",       "Silver",        (192, 192, 192)),
    ("P05", "中灰",       "Gray",          (150, 150, 150)),
    ("P06", "深灰",       "Dark Gray",     (95, 95, 95)),
    ("P07", "炭灰",       "Charcoal",      (60, 60, 60)),
    ("P08", "黑色",       "Black",         (20, 20, 20)),
    # 红色系
    ("P09", "浅粉",       "Pink",          (255, 182, 193)),
    ("P10", "粉红",       "Hot Pink",      (255, 105, 180)),
    ("P11", "玫红",       "Magenta",       (200, 30, 120)),
    ("P12", "正红",       "Red",           (220, 40, 40)),
    ("P13", "暗红",       "Dark Red",      (140, 20, 20)),
    ("P14", "砖红",       "Rust",          (170, 70, 40)),
    ("P15", "橙红",       "Orange Red",    (255, 80, 0)),
    # 橙色系
    ("P16", "蜜桃橙",     "Peach",         (255, 180, 120)),
    ("P17", "橙色",       "Orange",        (255, 140, 0)),
    ("P18", "南瓜橙",     "Pumpkin",       (200, 90, 0)),
    # 黄色系
    ("P19", "浅黄",       "Light Yellow",  (255, 235, 150)),
    ("P20", "正黄",       "Yellow",        (255, 210, 0)),
    ("P21", "金黄",       "Gold",          (230, 170, 0)),
    ("P22", "芥末黄",     "Mustard",       (180, 140, 0)),
    # 绿色系
    ("P23", "嫩绿",       "Lime",          (180, 255, 80)),
    ("P24", "浅绿",       "Light Green",   (120, 210, 80)),
    ("P25", "正绿",       "Green",         (40, 160, 40)),
    ("P26", "翠绿",       "Emerald",       (0, 130, 80)),
    ("P27", "橄榄绿",     "Olive",         (100, 110, 30)),
    ("P28", "深绿",       "Dark Green",    (20, 90, 30)),
    ("P29", "青绿",       "Teal",          (0, 150, 150)),
    # 蓝色系
    ("P30", "浅蓝",       "Light Blue",    (150, 210, 255)),
    ("P31", "天蓝",       "Sky Blue",      (80, 170, 230)),
    ("P32", "正蓝",       "Blue",          (0, 100, 200)),
    ("P33", "深蓝",       "Dark Blue",     (0, 50, 130)),
    ("P34", "海军蓝",     "Navy",          (20, 30, 80)),
    # 紫色系
    ("P35", "浅紫",       "Lavender",      (200, 170, 230)),
    ("P36", "紫色",       "Purple",        (130, 80, 180)),
    ("P37", "深紫",       "Dark Purple",   (80, 40, 120)),
    ("P38", "梅子色",     "Plum",          (90, 30, 70)),
    # 棕色系
    ("P39", "卡其",       "Tan",           (210, 170, 120)),
    ("P40", "浅棕",       "Light Brown",   (170, 120, 70)),
    ("P41", "棕色",       "Brown",         (120, 75, 40)),
    ("P42", "深棕",       "Dark Brown",    (80, 50, 25)),
    ("P43", "巧克力色",   "Chocolate",     (60, 35, 20)),
    # 肤色
    ("P44", "肤色",       "Skin",          (255, 210, 170)),
    ("P45", "小麦色",     "Wheat",         (220, 175, 135)),
    # 特殊/中性
    ("P46", "米色",       "Beige",         (230, 210, 180)),
    ("P47", "灰褐",       "Taupe",         (150, 130, 110)),
    ("P48", "红棕",       "Mahogany",      (110, 50, 35)),
]

# 构建快速查找结构
PALETTE_RGB = [item[3] for item in PERLER_PALETTE]


# ---------------------------------------------------------------------------
# 颜色量化: 使用 redmean 感知距离算法
# 比纯 RGB 欧氏距离更贴近人眼感知, 且不需要额外依赖
# ---------------------------------------------------------------------------

def color_distance(c1, c2):
    """redmean 加权颜色距离, 返回值越小越接近"""
    r_mean = (c1[0] + c2[0]) / 2.0
    dr = c1[0] - c2[0]
    dg = c1[1] - c2[1]
    db = c1[2] - c2[2]
    return (
        (2 + r_mean / 256) * dr * dr
        + 4 * dg * dg
        + (2 + (255 - r_mean) / 256) * db * db
    )


def nearest_palette_index(rgb):
    """找到与给定 RGB 最接近的调色板索引"""
    best_idx = 0
    best_dist = float("inf")
    for i, p_rgb in enumerate(PALETTE_RGB):
        d = color_distance(rgb, p_rgb)
        if d < best_dist:
            best_dist = d
            best_idx = i
    return best_idx


# ---------------------------------------------------------------------------
# 图像加载与缩放
# ---------------------------------------------------------------------------

def load_and_resize(image_path, target_w, target_h=None, mode="fit"):
    """
    加载图片并缩放到目标珠子尺寸。

    mode:
      "fit"  - 保持宽高比, 整张图缩放进 target_w x target_h (高度可自适应)
      "cover"- 裁剪填充到指定 target_w x target_h
    """
    img = Image.open(image_path).convert("RGB")

    orig_w, orig_h = img.size

    if mode == "cover" and target_h is not None:
        # 裁剪到目标比例后缩放
        target_ratio = target_w / target_h
        orig_ratio = orig_w / orig_h
        if orig_ratio > target_ratio:
            # 原图更宽, 裁左右
            new_w = int(orig_h * target_ratio)
            left = (orig_w - new_w) // 2
            img = img.crop((left, 0, left + new_w, orig_h))
        else:
            # 原图更高, 裁上下
            new_h = int(orig_w / target_ratio)
            top = (orig_h - new_h) // 2
            img = img.crop((0, top, orig_w, top + new_h))
        out_w, out_h = target_w, target_h
    else:
        # fit 模式: 按宽度等比缩放
        out_w = target_w
        if target_h is not None:
            out_h = target_h
        else:
            out_h = max(1, round(orig_h * target_w / orig_w))

    # 使用 LANCZOS 高质量重采样缩小
    small = img.resize((out_w, out_h), Image.LANCZOS)
    return small, out_w, out_h


# ---------------------------------------------------------------------------
# 量化整张图
# ---------------------------------------------------------------------------

def quantize(img, dither=False):
    """
    将图像每个像素映射到调色板颜色。
    返回: pattern (二维列表, 每格为调色板索引), width, height
    """
    w, h = img.size
    pixels = img.load()

    if dither:
        # Floyd-Steinberg 抖动, 让颜色过渡更自然
        # 在原图副本上操作 (用 float 数组)
        buf = []
        for y in range(h):
            row = []
            for x in range(w):
                r, g, b = pixels[x, y]
                row.append([float(r), float(g), float(b)])
            buf.append(row)

        pattern = []
        for y in range(h):
            row = []
            for x in range(w):
                old = buf[y][x]
                old_tuple = (int(round(old[0])), int(round(old[1])), int(round(old[2])))
                old_tuple = tuple(max(0, min(255, v)) for v in old_tuple)
                idx = nearest_palette_index(old_tuple)
                row.append(idx)
                new_rgb = PALETTE_RGB[idx]
                # 计算误差并扩散
                err = [old[0] - new_rgb[0], old[1] - new_rgb[1], old[2] - new_rgb[2]]
                if x + 1 < w:
                    for c in range(3):
                        buf[y][x + 1][c] += err[c] * 7 / 16
                if y + 1 < h:
                    if x - 1 >= 0:
                        for c in range(3):
                            buf[y + 1][x - 1][c] += err[c] * 3 / 16
                    for c in range(3):
                        buf[y + 1][x][c] += err[c] * 5 / 16
                    if x + 1 < w:
                        for c in range(3):
                            buf[y + 1][x + 1][c] += err[c] * 1 / 16
            pattern.append(row)
    else:
        pattern = []
        for y in range(h):
            row = []
            for x in range(w):
                idx = nearest_palette_index(pixels[x, y])
                row.append(idx)
            pattern.append(row)

    return pattern, w, h


# ---------------------------------------------------------------------------
# 统计材料清单
# ---------------------------------------------------------------------------

def count_materials(pattern):
    """统计每种颜色珠子的使用数量, 返回 [(调色板索引, 数量), ...] 按数量降序"""
    counter = Counter()
    for row in pattern:
        for idx in row:
            counter[idx] += 1
    return sorted(counter.items(), key=lambda x: -x[1])


# ---------------------------------------------------------------------------
# 生成 PNG 预览
# ---------------------------------------------------------------------------

def generate_png(pattern, w, h, cell_px=20, grid=True, output_path="preview.png"):
    """生成像素化预览 PNG, 每个珠子占 cell_px x cell_px 像素"""
    img = Image.new("RGB", (w * cell_px, h * cell_px), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        for x in range(w):
            idx = pattern[y][x]
            color = PALETTE_RGB[idx]
            x0, y0 = x * cell_px, y * cell_px
            draw.rectangle([x0, y0, x0 + cell_px - 1, y0 + cell_px - 1], fill=color)

    if grid and cell_px >= 10:
        grid_color = (210, 210, 210)
        # 竖线
        for x in range(0, w + 1):
            draw.line([(x * cell_px, 0), (x * cell_px, h * cell_px)], fill=grid_color, width=1)
        # 横线
        for y in range(0, h + 1):
            draw.line([(0, y * cell_px), (w * cell_px, y * cell_px)], fill=grid_color, width=1)
        # 每 5 格加粗, 方便手工数数
        bold_color = (120, 120, 120)
        for x in range(0, w + 1, 5):
            draw.line([(x * cell_px, 0), (x * cell_px, h * cell_px)], fill=bold_color, width=1)
        for y in range(0, h + 1, 5):
            draw.line([(0, y * cell_px), (w * cell_px, y * cell_px)], fill=bold_color, width=1)

    img.save(output_path)
    return output_path


# ---------------------------------------------------------------------------
# 生成 HTML 图纸
# ---------------------------------------------------------------------------

def generate_html(pattern, w, h, materials, source_image, output_path, cell_px=18,
                  show_codes=False, show_grid=True, title="拼豆图纸"):
    """生成可打印的 HTML 图纸, 含图纸网格 + 材料清单"""
    total = sum(c for _, c in materials)

    # 构建材料清单行
    mat_rows = []
    for idx, count in materials:
        code, name_cn, name_en, rgb = PERLER_PALETTE[idx]
        hex_color = "#%02X%02X%02X" % rgb
        pct = count / total * 100 if total else 0
        mat_rows.append(
            f"<tr>"
            f'<td class="swatch"><span class="chip" style="background:{hex_color}"></span></td>'
            f"<td class='code'>{html.escape(code)}</td>"
            f"<td>{html.escape(name_cn)}</td>"
            f"<td>{html.escape(name_en)}</td>"
            f"<td class='num'>{count}</td>"
            f"<td class='num'>{pct:.1f}%</td>"
            f"</tr>"
        )
    mat_rows_html = "\n".join(mat_rows)

    # 构建 CSS 网格 (用 table, 兼容打印)
    cell_size = cell_px
    font_size = max(6, cell_px // 2 - 1) if show_codes else 0

    grid_cells = []
    for y in range(h):
        cells = []
        for x in range(w):
            idx = pattern[y][x]
            _, _, _, rgb = PERLER_PALETTE[idx]
            hex_color = "#%02X%02X%02X" % rgb
            code = PERLER_PALETTE[idx][0]
            label = f"<span class='lbl'>{html.escape(code)}</span>" if show_codes else ""
            cells.append(
                f'<td class="bead" style="background:{hex_color};'
                f'width:{cell_size}px;height:{cell_size}px;'
                f'font-size:{font_size}px">{label}</td>'
            )
        grid_cells.append("<tr>" + "".join(cells) + "</tr>")
    grid_html = "\n".join(grid_cells)

    grid_class = "no-grid" if not show_grid else ""

    # 每 5 格标注坐标参考 (顶部列号 + 左侧行号)
    col_header = "".join(
        f'<th class="{"major" if (x % 5 == 0) else ""}">{x if x % 5 == 0 else ""}</th>'
        for x in range(w)
    )

    html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(title)}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    font-family: "PingFang SC", "Microsoft YaHei", "Segoe UI", sans-serif;
    background: #f5f5f7;
    color: #1d1d1f;
    margin: 0;
    padding: 24px;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ font-size: 24px; margin: 0 0 4px; }}
  .meta {{ color: #6e6e73; font-size: 13px; margin-bottom: 20px; }}
  .meta span {{ margin-right: 16px; }}

  .section {{ background: #fff; border-radius: 12px; padding: 20px; margin-bottom: 20px;
              box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}

  .pattern-wrap {{ overflow-x: auto; }}
  table.pattern {{ border-collapse: collapse; }}
  table.pattern th {{
    font-size: 10px; color: #86868b; font-weight: normal; padding: 2px 0;
    text-align: center; min-width: 0;
  }}
  table.pattern th.major {{ color: #1d1d1f; font-weight: 600; }}
  table.pattern tr.row-label th {{
    width: 22px; font-size: 10px; color: #1d1d1f; font-weight: 600; padding-right: 6px;
  }}
  td.bead {{
    border: 1px solid rgba(0,0,0,0.12);
    text-align: center; vertical-align: middle;
    color: rgba(0,0,0,0.55); line-height: 1; padding: 0;
  }}
  td.bead .lbl {{ font-weight: 600; opacity: 0.7; }}
  table.pattern.no-grid td.bead {{ border: none; }}

  table.materials {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  table.materials th {{
    text-align: left; padding: 8px 10px; border-bottom: 2px solid #e5e5ea;
    color: #6e6e73; font-size: 12px; text-transform: uppercase;
  }}
  table.materials td {{ padding: 8px 10px; border-bottom: 1px solid #f0f0f3; }}
  table.materials tr:hover td {{ background: #f5f5f7; }}
  .swatch {{ width: 40px; }}
  .chip {{ display: inline-block; width: 22px; height: 22px; border-radius: 4px;
           border: 1px solid rgba(0,0,0,0.15); vertical-align: middle; }}
  .code {{ font-family: "SF Mono", Consolas, monospace; color: #6e6e73; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}

  .summary {{ display: flex; gap: 24px; margin-bottom: 16px; flex-wrap: wrap; }}
  .stat {{ background: #f5f5f7; border-radius: 8px; padding: 12px 18px; }}
  .stat .v {{ font-size: 22px; font-weight: 700; }}
  .stat .l {{ font-size: 12px; color: #6e6e73; }}

  .legend {{ font-size: 12px; color: #6e6e73; margin-top: 8px; }}

  @media print {{
    body {{ background: #fff; padding: 0; }}
    .section {{ box-shadow: none; border-radius: 0; page-break-inside: avoid; }}
    .no-print {{ display: none; }}
  }}
</style>
</head>
<body>
<div class="container">
  <h1>🎨 {html.escape(title)}</h1>
  <div class="meta">
    <span>源图: {html.escape(os.path.basename(source_image))}</span>
    <span>尺寸: {w} × {h} 颗</span>
    <span>总珠数: {total}</span>
    <span>用色: {len(materials)} 种</span>
  </div>

  <div class="section">
    <div class="summary">
      <div class="stat"><div class="v">{w}×{h}</div><div class="l">图纸尺寸 (颗)</div></div>
      <div class="stat"><div class="v">{total}</div><div class="l">总珠子数</div></div>
      <div class="stat"><div class="v">{len(materials)}</div><div class="l">颜色种类</div></div>
      <div class="stat"><div class="v">{w*5}×{h*5} mm</div><div class="l">成品尺寸 (5mm 豆)</div></div>
    </div>
    <p class="legend">提示: 粗线为每 5 格分隔, 方便对照钉板摆放。用浏览器打印即可获得纸质图纸。</p>
  </div>

  <div class="section">
    <h2 style="font-size:18px;margin:0 0 12px">📐 图纸</h2>
    <div class="pattern-wrap">
      <table class="pattern {grid_class}">
        <thead>
          <tr><th></th>{col_header}<th></th></tr>
        </thead>
        <tbody>
"""
    # 加行号
    body_rows = []
    for y in range(h):
        row_label = f'<tr class="row-label"><th>{y if y % 5 == 0 else ""}</th>'
        body_rows.append(row_label + grid_cells[y].replace("<tr>", "").replace("</tr>", "") + f'<th>{y if y % 5 == 0 else ""}</th></tr>')
    html_doc += "\n".join(body_rows)

    html_doc += f"""
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <h2 style="font-size:18px;margin:0 0 12px">🧮 材料清单</h2>
    <table class="materials">
      <thead>
        <tr>
          <th>色样</th><th>编号</th><th>中文名</th><th>英文名</th>
          <th style="text-align:right">数量</th><th style="text-align:right">占比</th>
        </tr>
      </thead>
      <tbody>
        {mat_rows_html}
      </tbody>
      <tfoot>
        <tr style="font-weight:600">
          <td colspan="4">合计</td>
          <td class="num">{total}</td>
          <td class="num">100.0%</td>
        </tr>
      </tfoot>
    </table>
  </div>

  <div class="section no-print">
    <p style="font-size:13px;color:#6e6e73;margin:0">
      由「照片转拼豆图纸」Skill 生成 · 调色板共 {len(PERLER_PALETTE)} 色 · 算法: redmean 感知距离
    </p>
  </div>
</div>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_doc)
    return output_path


# ---------------------------------------------------------------------------
# 主入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="照片转拼豆图纸: 将照片转换为可打印的拼豆手工图纸与材料清单",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("image", help="输入图片路径 (jpg/png/webp 等)")
    parser.add_argument("-w", "--width", type=int, default=29,
                        help="图纸宽度 (珠子数), 默认 29 (标准方板)")
    parser.add_argument("-H", "--height", type=int, default=None,
                        help="图纸高度 (珠子数), 不指定则按比例自适应")
    parser.add_argument("-m", "--mode", choices=["fit", "cover"], default="fit",
                        help="缩放模式: fit=整图缩放保留(默认), cover=裁剪填充")
    parser.add_argument("-o", "--output", default="./output",
                        help="输出目录, 默认 ./output")
    parser.add_argument("-c", "--cell", type=int, default=18,
                        help="HTML/PNG 中每颗珠子的像素大小, 默认 18")
    parser.add_argument("--codes", action="store_true",
                        help="在图纸格子上显示颜色编号 (适合精确定位)")
    parser.add_argument("--no-grid", action="store_true",
                        help="不显示网格线")
    parser.add_argument("--dither", action="store_true",
                        help="启用 Floyd-Steinberg 抖动 (颜色过渡更自然, 但需更多颜色)")
    parser.add_argument("--png", action="store_true", default=True,
                        help="同时输出 PNG 预览图 (默认开启)")
    parser.add_argument("--title", default="拼豆图纸", help="图纸标题")
    parser.add_argument("--json", action="store_true",
                        help="额外输出 pattern.json (程序化数据)")

    args = parser.parse_args()

    # 校验输入
    if not os.path.isfile(args.image):
        sys.stderr.write(f"[错误] 找不到图片: {args.image}\n")
        sys.exit(1)
    if args.width < 1 or args.width > 200:
        sys.stderr.write("[错误] 宽度应在 1-200 之间\n")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.image))[0]

    # 1. 加载缩放
    print(f"[1/4] 加载图片: {args.image}")
    small, w, h = load_and_resize(args.image, args.width, args.height, args.mode)
    print(f"      缩放至 {w} × {h} 颗")

    # 2. 量化
    print(f"[2/4] 颜色量化 (抖动: {'开' if args.dither else '关'})")
    pattern, w, h = quantize(small, dither=args.dither)
    materials = count_materials(pattern)
    total = sum(c for _, c in materials)
    print(f"      共 {total} 颗珠子, {len(materials)} 种颜色")

    # 3. 生成 HTML
    print("[3/4] 生成 HTML 图纸...")
    html_path = os.path.join(args.output, f"{base}_pattern.html")
    generate_html(pattern, w, h, materials, args.image, html_path,
                  cell_px=args.cell, show_codes=args.codes,
                  show_grid=not args.no_grid, title=args.title)

    # 4. 生成 PNG
    png_path = None
    if args.png:
        print("[4/4] 生成 PNG 预览...")
        png_path = os.path.join(args.output, f"{base}_preview.png")
        generate_png(pattern, w, h, cell_px=args.cell,
                     grid=not args.no_grid, output_path=png_path)

    # 可选 JSON
    if args.json:
        json_path = os.path.join(args.output, f"{base}_pattern.json")
        data = {
            "width": w,
            "height": h,
            "total_beads": total,
            "colors_used": len(materials),
            "palette": [
                {"code": PERLER_PALETTE[i][0], "name_cn": PERLER_PALETTE[i][1],
                 "name_en": PERLER_PALETTE[i][2], "rgb": list(PERLER_PALETTE[i][3])}
                for i in range(len(PERLER_PALETTE))
            ],
            "materials": [
                {"code": PERLER_PALETTE[idx][0], "name_cn": PERLER_PALETTE[idx][1],
                 "name_en": PERLER_PALETTE[idx][2], "rgb": list(PERLER_PALETTE[idx][3]),
                 "count": cnt}
                for idx, cnt in materials
            ],
            "pattern": [[PERLER_PALETTE[idx][0] for idx in row] for row in pattern],
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # 打印材料清单摘要
    print("\n" + "=" * 52)
    print(f"  📋 材料清单 (共 {total} 颗, {len(materials)} 色)")
    print("=" * 52)
    print(f"  {'编号':<6}{'颜色':<12}{'数量':>8}{'占比':>8}")
    print("-" * 52)
    for idx, cnt in materials:
        code, name_cn, _, _ = PERLER_PALETTE[idx]
        pct = cnt / total * 100 if total else 0
        print(f"  {code:<6}{name_cn:<12}{cnt:>8}{pct:>7.1f}%")
    print("-" * 52)
    print(f"  {'合计':<18}{total:>8}{'100.0%':>8}")
    print("=" * 52)

    print(f"\n✅ 完成! 输出目录: {os.path.abspath(args.output)}")
    print(f"   📄 HTML 图纸: {os.path.basename(html_path)}")
    if png_path:
        print(f"   🖼  PNG 预览: {os.path.basename(png_path)}")
    print(f"   💡 用浏览器打开 HTML 文件, Ctrl+P 即可打印纸质图纸。")


if __name__ == "__main__":
    main()
