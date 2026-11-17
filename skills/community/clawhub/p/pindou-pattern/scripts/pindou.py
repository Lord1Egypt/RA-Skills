# -*- coding: utf-8 -*-
"""
拼豆图纸生成器（简易版，纯标准库，无外部依赖）

把任意图片或像素数据量化为真实拼豆色号的拼豆施工图，并输出：
  - 一张可缩放/可打印的 SVG 图纸（格内色号 + 行列坐标 + 每 10 格加重线 + 配色清单）
  - 一个 HTML 预览页（内嵌 SVG + 交互式配色表 + 下载入口）
  - 一份 CSV 物料清单（Excel 直接打开，色号 + 数量）
  - 一份 JSON 网格数据（便于二次处理）

颜色匹配与色号对照使用同目录下的 palette.py / palette.json（205 色 × 5 品牌）。

依赖：仅 Python 3.8+ 标准库。
  - 图片输入默认用内置 PNG 解码器（支持 8-bit RGB/RGBA/灰度/调色板，非隔行）。
  - 若环境中已安装 Pillow，则自动支持 JPG / WebP / BMP / GIF 等更多格式。
"""

import argparse
import csv
import json
import math
import os
import struct
import sys
import zlib

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from palette import (  # noqa: E402
    COLOR_SYSTEMS,
    BLANK,
    hex_to_rgb,
    find_closest_color,
    limit_colors,
    build_stats,
    get_code,
    readable_text_color,
)


# ----------------------------------------------------------------------------
# 图像读取（优先 Pillow，否则内置 PNG 解码器）
# ----------------------------------------------------------------------------

def _load_pixels_pillow(path):
    """用 Pillow 读图，返回 (width, height, pixels[(r,g,b), ...])，透明区域合成白底。"""
    from PIL import Image
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    px = img.load()
    out = []
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            # 透明 / 半透明：与白色混合
            if a < 255:
                t = a / 255.0
                r = int(r * t + 255 * (1 - t))
                g = int(g * t + 255 * (1 - t))
                b = int(b * t + 255 * (1 - t))
            out.append((r, g, b))
    return w, h, out


def _read_png(path):
    """极简 PNG 解码器：仅支持 8-bit、非隔行、常见颜色类型。返回 (w,h,pixels)。"""
    with open(path, "rb") as f:
        data = f.read()

    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是合法的 PNG 文件（当前仅支持 PNG；JPG/WebP 需安装 Pillow）")

    pos = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    palette = None
    trns = None

    while pos < len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        chunk = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            width, height, bit_depth, color_type, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"PLTE":
            palette = chunk
        elif ctype == b"tRNS":
            trns = chunk
        elif ctype == b"IEND":
            break
        pos += 12 + length

    if width is None:
        raise ValueError("PNG 缺少 IHDR 块")
    if interlace != 0:
        raise ValueError("不支持隔行 PNG（Adam7），请重新导出为非隔行 PNG")
    if bit_depth != 8:
        raise ValueError("仅支持 8-bit PNG，当前 bit_depth=%s" % bit_depth)

    # 颜色类型 -> 每像素字节数 & 是否含 alpha
    if color_type == 0:    # 灰度
        bpp, has_alpha, ct = 1, False, "gray"
    elif color_type == 2:  # RGB
        bpp, has_alpha, ct = 3, False, "rgb"
    elif color_type == 3:  # 调色板
        bpp, has_alpha, ct = 1, trns is not None, "pal"
    elif color_type == 4:  # 灰度+alpha
        bpp, has_alpha, ct = 2, True, "ga"
    elif color_type == 6:  # RGBA
        bpp, has_alpha, ct = 4, True, "rgba"
    else:
        raise ValueError("不支持的 PNG 颜色类型 %s" % color_type)

    raw = zlib.decompress(bytes(idat))
    stride = width * bpp
    out = bytearray()
    prev = bytearray(stride)

    def paeth(a, b, c):
        p = a + b - c
        pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
        if pa <= pb and pa <= pc:
            return a
        if pb <= pc:
            return b
        return c

    p = 0
    for y in range(height):
        ftype = raw[p]
        p += 1
        line = bytearray(raw[p:p + stride])
        p += stride
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if ftype == 1:       # Sub
                line[i] = (line[i] + a) & 255
            elif ftype == 2:     # Up
                line[i] = (line[i] + b) & 255
            elif ftype == 3:     # Average
                line[i] = (line[i] + ((a + b) >> 1)) & 255
            elif ftype == 4:     # Paeth
                line[i] = (line[i] + paeth(a, b, c)) & 255
            # ftype == 0: None，无需处理
        out += line
        prev = line

    pixels = []
    for y in range(height):
        for x in range(width):
            o = y * stride + x * bpp
            if ct == "gray":
                r = g = b = out[o]
            elif ct == "rgb":
                r, g, b = out[o], out[o + 1], out[o + 2]
            elif ct == "rgba":
                r, g, b, a = out[o], out[o + 1], out[o + 2], out[o + 3]
                t = a / 255.0
                r = int(r * t + 255 * (1 - t))
                g = int(g * t + 255 * (1 - t))
                b = int(b * t + 255 * (1 - t))
            elif ct == "ga":
                v, a = out[o], out[o + 1]
                t = a / 255.0
                r = g = b = int(v * t + 255 * (1 - t))
            else:  # pal
                idx = out[o]
                r, g, b = palette[idx * 3], palette[idx * 3 + 1], palette[idx * 3 + 2]
                if trns and idx < len(trns):
                    a = trns[idx]
                    t = a / 255.0
                    r = int(r * t + 255 * (1 - t))
                    g = int(g * t + 255 * (1 - t))
                    b = int(b * t + 255 * (1 - t))
            pixels.append((r, g, b))

    return width, height, pixels


def load_image(path):
    """读取图片为 (w, h, pixels)。优先 Pillow（多格式），否则内置 PNG 解码。"""
    lower = path.lower()
    if not lower.endswith(".png"):
        try:
            return _load_pixels_pillow(path)
        except ImportError:
            raise ValueError(
                "非 PNG 格式需要 Pillow 支持：请 `pip install pillow`，"
                "或把图片导出为 PNG 后重试。"
            )
    try:
        return _read_png(path)
    except ValueError:
        # PNG 解析失败（如隔行/16-bit），尝试退回 Pillow
        try:
            return _load_pixels_pillow(path)
        except ImportError:
            raise


# ----------------------------------------------------------------------------
# 网格量化
# ----------------------------------------------------------------------------

def image_to_grid(pixels, w, h, size):
    """将图片 contain 缩放进 size×size 网格，逐格取区域平均色。返回 (r,g,b) 列表。

    以「输出格」为循环单位、反向采样其覆盖的源像素区域，对放大（scale>1）
    与缩小（scale<1）两种情况都正确（缩小=区块平均，放大=就近取源像素）。
    """
    if size <= 0:
        raise ValueError("网格尺寸必须 > 0")
    scale = min(size / w, size / h)
    draw_w = w * scale
    draw_h = h * scale
    off_x = (size - draw_w) / 2.0
    off_y = (size - draw_h) / 2.0

    grid = []
    for oy in range(size):
        # 该输出行覆盖的源 y 区间
        sy0 = (oy - off_y) * h / draw_h
        sy1 = (oy + 1 - off_y) * h / draw_h
        y0 = max(0, int(math.floor(sy0)))
        y1 = min(h, int(math.ceil(sy1)))
        for ox in range(size):
            sx0 = (ox - off_x) * w / draw_w
            sx1 = (ox + 1 - off_x) * w / draw_w
            x0 = max(0, int(math.floor(sx0)))
            x1 = min(w, int(math.ceil(sx1)))
            if x1 <= x0 or y1 <= y0:
                grid.append((255, 255, 255))  # 留白区域（contain 空缺）
                continue
            r = g = b = n = 0
            for yy in range(y0, y1):
                base = yy * w
                for xx in range(x0, x1):
                    pr, pg, pb = pixels[base + xx]
                    r += pr
                    g += pg
                    b += pb
                    n += 1
            grid.append((r // n, g // n, b // n))
    return grid


def is_near_white(rgb, threshold):
    return all(c >= threshold for c in rgb)


def quantize(grid_rgb, system, mode, blank_white, white_threshold):
    """将 RGB 网格转成色号 HEX 网格。near-white 可选置为 BLANK。"""
    out = []
    for rgb in grid_rgb:
        if blank_white and is_near_white(rgb, white_threshold):
            out.append(BLANK)
            continue
        hexc = "#%02X%02X%02X" % rgb
        out.append(find_closest_color(hexc, mode))
    return out


def load_json_input(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    size = int(data["gridSize"])
    pixel_data = data["pixelData"]
    if len(pixel_data) != size * size:
        raise ValueError(
            "pixelData 长度 %d 与 gridSize²=%d 不一致" % (len(pixel_data), size * size)
        )
    # 标准化为 HEX 大写；非调色板颜色吸附到最近色号（除 BLANK 空格）
    norm = []
    for c in pixel_data:
        c = c.upper()
        if c == BLANK:
            norm.append(BLANK)
        else:
            norm.append(find_closest_color(c, "rgb"))
    return size, norm


# ----------------------------------------------------------------------------
# SVG 图纸
# ----------------------------------------------------------------------------

def build_svg(grid_hex, size, system, title, stats,
              cell=24, margin=34, title_h=46, show_coords=True,
              show_cellnumbers=True, show_stats=True, interval=10):
    """生成 SVG 字符串：标题栏 + 网格(格内色号) + 行列坐标 + 加重线 + 配色清单。"""
    grid_w = size * cell
    grid_h = size * cell

    # 配色清单区（底部，按 8 个一排换行）
    swatch = 20
    gap = 10
    per_row = max(1, (size * cell) // (swatch + 110))
    if per_row < 1:
        per_row = 1
    stats_rows = (len(stats) + per_row - 1) // per_row if stats else 0
    stats_h = 30 + stats_rows * (swatch + gap) if (show_stats and stats) else 0

    width = margin * 2 + grid_w
    height = title_h + margin + grid_h + stats_h + margin
    grid_x = margin
    grid_y = title_h + margin

    parts = []
    parts.append(
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" font-family="Consolas,Menlo,SimHei,sans-serif">' % (
            width, height, width, height)
    )
    # 背景
    parts.append('<rect x="0" y="0" width="%d" height="%d" fill="#ffffff"/>' % (width, height))

    # 标题栏
    parts.append('<rect x="0" y="0" width="%d" height="%d" fill="#2b2b2b"/>' % (width, title_h))
    tcolor = "#ffffff"
    tsize = 18 if len(title) <= 18 else 14
    parts.append(
        '<text x="%d" y="%d" fill="%s" font-size="%d" font-weight="bold">%s</text>' % (
            margin, title_h // 2 + 6, tcolor, tsize, _esc(title))
    )
    parts.append(
        '<text x="%d" y="%d" fill="#9aa0a6" font-size="11" text-anchor="end">%dx%d · %s</text>' % (
            width - margin, title_h // 2 + 5, size, size, _esc(system))
    )

    # 行列坐标
    if show_coords:
        for i in range(size):
            heavy = (i % interval == 0) or (i == size - 1)
            col_c = "#111111" if heavy else "#9aa0a6"
            col_s = 13 if heavy else 10
            cx = grid_x + i * cell + cell / 2
            ry = grid_y + i * cell + cell / 2 + 4
            parts.append(
                '<text x="%.1f" y="%d" fill="%s" font-size="%d" text-anchor="middle">%d</text>' % (
                    cx, int(grid_y - 8), col_c, col_s, i + 1)
            )
            parts.append(
                '<text x="%d" y="%.1f" fill="%s" font-size="%d" text-anchor="end">%d</text>' % (
                    int(grid_x - 8), ry, col_c, col_s, i + 1)
            )

    # 单元格
    font_sz = max(8, int(cell * 0.5))
    for idx, hexc in enumerate(grid_hex):
        r = idx // size
        c = idx % size
        x = grid_x + c * cell
        y = grid_y + r * cell
        if hexc == BLANK:
            fill = "#ffffff"
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#e3e3e3" stroke-width="0.5"/>'
                         % (x, y, cell, cell, fill))
            # 空格画一个浅色小圆点提示“不拼”
            parts.append('<circle cx="%.1f" cy="%.1f" r="1.6" fill="#d0d0d0"/>' % (x + cell / 2, y + cell / 2))
            continue
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, cell, cell, hexc))
        if show_cellnumbers:
            code = get_code(hexc, system) or "?"
            tc = readable_text_color(hexc)
            parts.append(
                '<text x="%.1f" y="%.1f" fill="%s" font-size="%d" text-anchor="middle" '
                'font-weight="bold">%s</text>' % (
                    x + cell / 2, y + cell / 2 + font_sz * 0.35, tc, font_sz, _esc(code))
            )

    # 网格线（每 10 格加重）
    for i in range(size + 1):
        heavy = (i % interval == 0) or (i == size)
        lw = 2.0 if heavy else 0.5
        col = "#000000" if heavy else "#cccccc"
        x = grid_x + i * cell
        parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="%s" stroke-width="%.1f"/>'
                     % (x, grid_y, x, grid_y + grid_h, col, lw))
        y = grid_y + i * cell
        parts.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="%.1f"/>'
                     % (grid_x, y, grid_x + grid_w, y, col, lw))

    # 配色清单
    if show_stats and stats:
        sy0 = grid_y + grid_h + 24
        parts.append('<text x="%d" y="%d" fill="#111111" font-size="14" font-weight="bold">配色清单</text>' % (margin, sy0))
        parts.append('<text x="%d" y="%d" fill="#555555" font-size="12" text-anchor="end">共 %d 色 · 总豆数 %d 颗</text>'
                     % (width - margin, sy0, len(stats), sum(s[2] for s in stats)))
        row_y = sy0 + 16
        for i, (hexc, code, cnt) in enumerate(stats):
            rx = margin + (i % per_row) * (swatch + 110)
            ry = row_y + (i // per_row) * (swatch + gap)
            parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" stroke="#888" stroke-width="0.5"/>'
                         % (rx, ry, swatch, swatch, hexc))
            parts.append('<text x="%d" y="%d" fill="#111" font-size="12">%s × %d</text>'
                         % (rx + swatch + 6, ry + 14, _esc(code), cnt))
        # 边框
        bx = margin - 6
        by = sy0 - 14
        bw = width - margin * 2 + 12
        bh = (stats_rows) * (swatch + gap) + 20
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="#dddddd"/>'
                     % (bx, by, bw, bh))

    parts.append('</svg>')
    return "".join(parts)


def _esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# ----------------------------------------------------------------------------
# HTML 预览
# ----------------------------------------------------------------------------

def build_html(svg, title, stats, system, size):
    total = sum(s[2] for s in stats)
    rows = "".join(
        '<tr><td><span class="sw" style="background:%s"></span></td>'
        '<td><code>%s</code></td><td>%s</td><td>%d</td></tr>' % (
            _esc(h), _esc(c), _esc(h), n)
        for h, c, n in stats
    )
    html = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s · 拼豆图纸</title>
<style>
  body{font-family:system-ui,'Microsoft YaHei',sans-serif;background:#f6f7f9;color:#222;margin:0;padding:24px;}
  h1{font-size:20px;margin:0 0 4px;}
  .sub{color:#777;font-size:13px;margin-bottom:16px;}
  .wrap{display:flex;gap:24px;flex-wrap:wrap;align-items:flex-start;}
  .sheet{background:#fff;border:1px solid #e2e2e2;border-radius:8px;padding:8px;box-shadow:0 1px 4px rgba(0,0,0,.06);overflow:auto;max-width:100%%;}
  .panel{background:#fff;border:1px solid #e2e2e2;border-radius:8px;padding:16px;min-width:260px;}
  h2{font-size:15px;margin:0 0 10px;}
  table{border-collapse:collapse;width:100%%;font-size:13px;}
  th,td{border-bottom:1px solid #eee;padding:6px 8px;text-align:left;}
  th{color:#888;font-weight:600;}
  .sw{display:inline-block;width:16px;height:16px;border:1px solid #999;border-radius:3px;vertical-align:middle;margin-right:6px;}
  code{background:#f0f0f0;padding:1px 5px;border-radius:4px;font-family:Consolas,monospace;}
  .total{margin-top:12px;font-weight:700;}
  .btns{margin:14px 0;}
  button{font:inherit;padding:7px 14px;border:1px solid #ccc;border-radius:6px;background:#fff;cursor:pointer;margin-right:8px;}
  button:hover{background:#f0f0f0;}
  @media print{.btns{display:none;}body{background:#fff;}}
</style></head>
<body>
  <h1>%s</h1>
  <div class="sub">%dx%d · 品牌色号：%s · 用色 %d 种 · 总豆数 %d 颗</div>
  <div class="btns">
    <button onclick="window.print()">打印图纸</button>
  </div>
  <div class="wrap">
    <div class="sheet">%s</div>
    <div class="panel">
      <h2>配色清单（照着买豆）</h2>
      <table><thead><tr><th>颜色</th><th>色号</th><th>HEX</th><th>数量</th></tr></thead>
      <tbody>%s</tbody></table>
      <div class="total">合计：%d 颗</div>
    </div>
  </div>
</body></html>""" % (
        _esc(title), _esc(title), size, size, _esc(system), len(stats), total,
        svg, rows, total
    )
    return html


# ----------------------------------------------------------------------------
# CSV / JSON
# ----------------------------------------------------------------------------

def write_csv(path, stats):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["色号", "颜色HEX", "数量"])
        for hexc, code, cnt in stats:
            w.writerow([code, hexc, cnt])


def write_json(path, size, system, grid_hex, stats):
    payload = {
        "gridSize": size,
        "system": system,
        "grid": grid_hex,
        "stats": [{"hex": h, "code": c, "count": n} for h, c, n in stats],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------------
# 主流程
# ----------------------------------------------------------------------------

def default_out(input_path, ext):
    base, _ = os.path.splitext(input_path)
    return base + "_pattern." + ext


def run(args):
    is_json = args.input.lower().endswith(".json")

    if is_json:
        size, grid_hex = load_json_input(args.input)
        title = args.title or os.path.splitext(os.path.basename(args.input))[0]
    else:
        w, h, pixels = load_image(args.input)
        if args.size is None:
            args.size = 32
        grid_rgb = image_to_grid(pixels, w, h, args.size)
        grid_hex = quantize(grid_rgb, args.system, args.match,
                            args.blank_white, args.white_threshold)
        title = args.title or os.path.splitext(os.path.basename(args.input))[0]
        size = args.size

    if args.max_colors:
        grid_hex = limit_colors(grid_hex, args.max_colors, args.match)

    stats = build_stats(grid_hex, args.system)
    total = sum(c for _, _, c in stats)

    svg = build_svg(
        grid_hex, size, args.system, title, stats,
        cell=args.cell, show_coords=not args.no_coordinates,
        show_cellnumbers=not args.no_cellnumbers,
        show_stats=not args.no_stats, interval=args.interval,
    )

    out_svg = args.out or default_out(args.input, "svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg)

    out_html = args.html or default_out(args.input, "html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(build_html(svg, title, stats, args.system, size))

    if args.csv:
        write_csv(args.csv, stats)
    if args.json_out:
        write_json(args.json_out, size, args.system, grid_hex, stats)

    # stdout 统计
    print("=" * 42)
    print("拼豆图纸已生成")
    print("  图纸 SVG : %s" % out_svg)
    print("  预览 HTML: %s" % out_html)
    print("  网格规格 : %dx%d" % (size, size))
    print("  品牌色号 : %s" % args.system)
    print("  用色数   : %d 种" % len(stats))
    print("  总豆数   : %d 颗" % total)
    if args.csv:
        print("  物料清单 : %s" % args.csv)
    if args.json_out:
        print("  网格数据 : %s" % args.json_out)
    print("-" * 42)
    for hexc, code, cnt in stats:
        print("  %s  %s × %d" % (code.ljust(6), hexc, cnt))
    print("=" * 42)
    return out_svg, out_html


def main(argv=None):
    p = argparse.ArgumentParser(
        description="拼豆图纸生成器（简易版）：图片/像素数据 → 拼豆施工图",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python pindou.py 猫.png --size 48 --system 盼盼 --blank-white --max-colors 16 --csv 清单.csv\n"
               "  python pindou.py 作品.json --out 图纸.svg\n",
    )
    p.add_argument("input", help="输入：图片(png/jpg/...) 或 JSON 像素数据")
    p.add_argument("--size", type=int, default=None, help="网格 N×N（仅图片输入生效，默认 32）")
    p.add_argument("--system", choices=COLOR_SYSTEMS, default="MARD", help="色号品牌（默认 MARD）")
    p.add_argument("--match", choices=["rgb", "lab"], default="rgb", help="颜色匹配算法（lab 更准）")
    p.add_argument("--blank-white", action="store_true", help="近白色当作空格（不买白豆）")
    p.add_argument("--white-threshold", type=int, default=240, help="近白判定阈值（默认 240）")
    p.add_argument("--max-colors", type=int, default=None, help="色数收敛：保留用量前 N 色")
    p.add_argument("--title", default=None, help="图纸标题（默认取文件名）")
    p.add_argument("--cell", type=int, default=24, help="SVG 每格像素（默认 24）")
    p.add_argument("--interval", type=int, default=10, help="加重网格线间隔（默认 10）")
    p.add_argument("--no-coordinates", action="store_true", help="关闭行列坐标")
    p.add_argument("--no-cellnumbers", action="store_true", help="关闭格内色号")
    p.add_argument("--no-stats", action="store_true", help="关闭底部配色清单")
    p.add_argument("--out", default=None, help="SVG 输出路径")
    p.add_argument("--html", default=None, help="HTML 输出路径")
    p.add_argument("--csv", default=None, help="导出色号用量 CSV（Excel 友好）")
    p.add_argument("--json-out", default=None, help="导出 JSON 网格数据")
    args = p.parse_args(argv)

    try:
        run(args)
    except Exception as e:
        print("错误：%s" % e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
