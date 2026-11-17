# -*- coding: utf-8 -*-
"""
拼豆色板与颜色匹配。
自带 5 大品牌（MARD / COCO / 漫漫 / 盼盼 / 咪小窝）共 205 色号的真实对照表，
开箱即用，无需联网或额外服务。
"""
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_PALETTE_PATH = os.path.join(_HERE, "palette.json")

with open(_PALETTE_PATH, "r", encoding="utf-8") as _f:
    COLOR_MAP = json.load(_f)  # {"#RRGGBB": {"MARD": "A01", ...}, ...}

# 调色板支持的全部色号系统
COLOR_SYSTEMS = ["MARD", "COCO", "漫漫", "盼盼", "咪小窝"]

# 全部可用 HEX（调色板颜色）
ALL_HEX = list(COLOR_MAP.keys())

# 空格标记：表示这一格不拼豆（留空不买豆）
BLANK = "#FFFFFF"


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return "#%02X%02X%02X" % (int(r) & 255, int(g) & 255, int(b) & 255)


def get_code(hex_color, system):
    """返回某 HEX 在指定品牌下的色号；不在调色板则回退 None。"""
    return COLOR_MAP.get(hex_color.upper(), {}).get(system)


# ---------- 颜色距离 ----------

def _rgb_distance(a, b):
    """欧氏距离（RGB 空间）。"""
    return sum((x - y) ** 2 for x, y in zip(hex_to_rgb(a), hex_to_rgb(b)))


def _srgb_to_xyz(r, g, b):
    def lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = lin(r), lin(g), lin(b)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    return x * 100, y * 100, z * 100


def _xyz_to_lab(x, y, z):
    # D65 参考白
    xn, yn, zn = 95.047, 100.0, 108.883

    def f(t):
        return t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    bb = 200 * (fy - fz)
    return L, a, bb


def _to_lab(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    x, y, z = _srgb_to_xyz(r, g, b)
    return _xyz_to_lab(x, y, z)


_LAB_CACHE = {}


def _lab_distance(a, b):
    """CIE76 感知色差（Lab 空间欧氏距离），比 RGB 更接近人眼判断。"""
    if a not in _LAB_CACHE:
        _LAB_CACHE[a] = _to_lab(a)
    if b not in _LAB_CACHE:
        _LAB_CACHE[b] = _to_lab(b)
    return sum((x - y) ** 2 for x, y in zip(_LAB_CACHE[a], _LAB_CACHE[b]))


def find_closest_color(hex_color, mode="rgb"):
    """在调色板中找与给定颜色最接近的 HEX。

    mode: 'rgb'（欧氏距离，快）/ 'lab'（感知色差，通常更准）。
    返回调色板中的 HEX 字符串。
    """
    hex_color = hex_color.upper()
    if hex_color in COLOR_MAP:
        return hex_color
    dist = _lab_distance if mode == "lab" else _rgb_distance
    best, best_d = None, None
    for cand in ALL_HEX:
        d = dist(hex_color, cand)
        if best_d is None or d < best_d:
            best, best_d = cand, d
    return best


def limit_colors(pixel_data, max_colors, mode="rgb"):
    """收敛色数：保留用量最多的 max_colors 种颜色，其余合并到最接近的保留色。

    空格 BLANK 永远保留且不计色数。
    """
    if max_colors <= 0:
        return pixel_data
    counts = {}
    for c in pixel_data:
        if c == BLANK:
            continue
        counts[c] = counts.get(c, 0) + 1
    # 用量降序，取前 max_colors
    keep = [c for c, _ in sorted(counts.items(), key=lambda x: -x[1])[:max_colors]]
    keep_set = set(keep)
    # 为被淘汰的颜色，找保留色中最接近者
    remap = {}
    for c in counts:
        if c in keep_set:
            remap[c] = c
            continue
        best, best_d = None, None
        dist = _lab_distance if mode == "lab" else _rgb_distance
        for k in keep:
            d = dist(c, k)
            if best_d is None or d < best_d:
                best, best_d = k, d
        remap[c] = best
    return [BLANK if c == BLANK else remap.get(c, c) for c in pixel_data]


def build_stats(pixel_data, system):
    """统计每种色号用量。返回 [(hex, code, count), ...] 按数量降序。"""
    counts = {}
    for c in pixel_data:
        if c == BLANK:
            continue
        counts[c] = counts.get(c, 0) + 1
    rows = []
    for hexc, cnt in counts.items():
        rows.append((hexc, get_code(hexc, system) or "?", cnt))
    rows.sort(key=lambda x: -x[2])
    return rows


def luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    return 0.299 * r + 0.587 * g + 0.114 * b


def readable_text_color(hex_color):
    """根据背景亮度返回黑/白文字色，保证格内色号清晰可读。"""
    return "#000000" if luminance(hex_color) > 150 else "#FFFFFF"
