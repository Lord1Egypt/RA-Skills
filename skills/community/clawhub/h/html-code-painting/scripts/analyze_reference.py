#!/usr/bin/env python3
"""
analyze_reference.py — 画作参照图分析工具（html-code-painting 技能配套）

对参照图片做临摹前的量化分析：
  1. 九宫格/16宫格平均色（构图与色块分布参考）
  2. 全图暗部 / 中间调 / 亮部代表色
  3. 平均明度、平均饱和度（判断画面基调）
  4. 建议画布宽高比

用法:
    python analyze_reference.py <image> [--grid 3] [--json]

依赖: Pillow (pip install pillow)。无 Pillow 时给出手工估色指引并退出。
输出: 终端人类可读报告；--json 时输出机器可读 JSON。

示例输出片段:
  [网格平均色 grid=4]
   row0: #A9BFD0 #93A9C2 #8FA5C1 #9FB4CB
   ...
  [基调] 平均明度 0.52(中) 平均饱和度 0.28(低) -> 整体偏灰雅,忌高饱和平涂
"""

import argparse
import json
import sys


def load_image(path):
    try:
        from PIL import Image
    except ImportError:
        print("缺少 Pillow。安装: pip install pillow\n"
              "无脚本环境时请按 analysis-workflow.md 第二节人工估色。", file=sys.stderr)
        sys.exit(2)
    img = Image.open(path).convert("RGB")
    return img


def avg_color(region):
    """区域缩到 1x1 取平均，等价于均值池化。"""
    tiny = region.resize((1, 1))
    r, g, b = tiny.getpixel((0, 0))
    return (r, g, b)


def hexc(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def luminance(rgb):
    r, g, b = [v / 255 for v in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def saturation(rgb):
    r, g, b = [v / 255 for v in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    return 0 if mx == 0 else (mx - mn) / mx


def main():
    ap = argparse.ArgumentParser(description="画作参照图分析")
    ap.add_argument("image", help="参照图片路径")
    ap.add_argument("--grid", type=int, default=3, choices=range(2, 9),
                    help="网格划分 N（默认 3 -> 九宫格）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    img = load_image(args.image)
    W, H = img.size
    n = args.grid

    cells, cell_colors = [], []
    for gy in range(n):
        row = []
        for gx in range(n):
            box = (
                int(gx * W / n), int(gy * H / n),
                int((gx + 1) * W / n), int((gy + 1) * H / n),
            )
            region = img.crop(box)
            rgb = avg_color(region)
            row.append(rgb)
            cells.append({"grid": f"({gx},{gy})", "rgb": rgb,
                          "luminance": round(luminance(rgb), 3),
                          "saturation": round(saturation(rgb), 3)})
        cell_colors.append(row)

    small = img.resize((200, max(1, int(200 * H / W))))
    pixels = list(small.getdata())
    darks = sorted(pixels, key=luminance)[:len(pixels) // 10]
    brights = sorted(pixels, key=luminance)[-len(pixels) // 10:]
    mids = sorted(pixels, key=lambda p: abs(luminance(p) - 0.5))[:max(1, len(pixels) // 5)]

    def rep_color(lst):
        r = sum(p[0] for p in lst) // len(lst)
        g = sum(p[1] for p in lst) // len(lst)
        b = sum(p[2] for p in lst) // len(lst)
        return (r, g, b)

    dark_c, mid_c, bright_c = rep_color(darks), rep_color(mids), rep_color(brights)

    avg_lum = sum(luminance(p) for p in pixels) / len(pixels)
    avg_sat = sum(saturation(p) for p in pixels) / len(pixels)

    ratio = W / H
    candidates = {
        "1:1": 1.0, "4:5": 0.8, "3:4": 0.75, "2:3": 0.667,
        "4:3": 1.333, "3:2": 1.5, "16:9": 1.778, "21:9": 2.333,
    }
    nearest_ratio = min(candidates, key=lambda k: abs(candidates[k] - ratio))

    lum_word = "暗" if avg_lum < 0.35 else ("亮" if avg_lum > 0.62 else "中")
    sat_word = "高饱和" if avg_sat > 0.45 else ("低饱和/灰雅" if avg_sat < 0.22 else "中饱和")

    result = {
        "size": [W, H],
        "nearest_canvas_ratio": nearest_ratio,
        "actual_ratio": round(ratio, 3),
        "avg_luminance": round(avg_lum, 3),
        "avg_saturation": round(avg_sat, 3),
        "tone": lum_word,
        "palette_note": sat_word,
        "shadow_color": hexc(dark_c),
        "midtone_color": hexc(mid_c),
        "highlight_color": hexc(bright_c),
        "grid_cells": cells,
    }

    if args.json:
        result["grid_rows_hex"] = [[hexc(c) for c in row] for row in cell_colors]
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"[尺寸] {W}x{H}  实际宽高比 {ratio:.2f} ≈ {nearest_ratio}")
    print(f"\n[网格平均色 grid={n}]")
    for row in cell_colors:
        print("   " + " ".join(hexc(c) for c in row))
    print(f"\n[三调代表色]")
    print(f"   暗部   {hexc(dark_c)}   <- 阴影别用纯黑，从这里取")
    print(f"   中间调 {hexc(mid_c)}   <- 主色块基准")
    print(f"   亮部   {hexc(bright_c)}   <- 高光色≈光源色倾向")
    print(f"\n[基调] 平均明度 {avg_lum:.2f}({lum_word})  "
          f"平均饱和度 {avg_sat:.2f}({sat_word})")
    tips = {"暗": "注意保留最亮点制造焦点, 大面积暗部内要有微弱明度起伏防死黑。",
            "中": "拉开至少 4 档明度层次。",
            "亮": "加少量深色锚点(窗洞/树影/人物)稳定画面重量。"}
    print(f"[建议] {tips[lum_word]}")
    if avg_sat > 0.45:
        print("[建议] 原图饱和已偏高, 屏幕绘制时仍建议整体 -10% 饱和防止刺眼。")


if __name__ == "__main__":
    main()
