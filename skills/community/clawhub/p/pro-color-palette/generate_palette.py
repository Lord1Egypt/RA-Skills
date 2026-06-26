#!/usr/bin/env python3
"""
color-palette card generator v2
生成专业配色卡图片（黑底 + 1大2小色块 + 中文色名 + Hex）
支持：本地生成 / 智能选色 / 批量导出 / 色值格式转换
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont

# ============================================================
# 配色方案库（12组，扩充至12组）
# ============================================================
PALETTES = {
    "爱马仕橙": {
        "primary": {"name": "爱马仕橙", "hex": "#FF8A00"},
        "secondary1": {"name": "深灰", "hex": "#363636"},
        "secondary2": {"name": "白粉", "hex": "#FFF2DF"},
    },
    "普拉得蓝": {
        "primary": {"name": "普拉得蓝", "hex": "#0175CC"},
        "secondary1": {"name": "睿智金", "hex": "#B78D77"},
        "secondary2": {"name": "米汤骄", "hex": "#FCF5E2"},
    },
    "长春花蓝": {
        "primary": {"name": "长春花蓝", "hex": "#5357A0"},
        "secondary1": {"name": "佛手黄", "hex": "#FED81F"},
        "secondary2": {"name": "荔枝白", "hex": "#FEFFEF"},
    },
    "孔雀蓝": {
        "primary": {"name": "孔雀蓝", "hex": "#0B7E9D"},
        "secondary1": {"name": "浅驼色", "hex": "#D7B9A1"},
        "secondary2": {"name": "月苍白", "hex": "#F9F6E5"},
    },
    "古驰绿": {
        "primary": {"name": "古驰绿", "hex": "#1F4433"},
        "secondary1": {"name": "杏红", "hex": "#FF8B31"},
        "secondary2": {"name": "象牙白", "hex": "#FFFBF0"},
    },
    "烈焰红": {
        "primary": {"name": "烈焰红", "hex": "#E53935"},
        "secondary1": {"name": "炭黑", "hex": "#212121"},
        "secondary2": {"name": "珍珠白", "hex": "#FAFAFA"},
    },
    "极光紫": {
        "primary": {"name": "极光紫", "hex": "#8E24AA"},
        "secondary1": {"name": "香槟金", "hex": "#D4AF37"},
        "secondary2": {"name": "雪白", "hex": "#F8F8FF"},
    },
    "薄荷绿": {
        "primary": {"name": "薄荷绿", "hex": "#26A69A"},
        "secondary1": {"name": "深空灰", "hex": "#455A64"},
        "secondary2": {"name": "泡沫白", "hex": "#F0FFF0"},
    },
    "琥珀黄": {
        "primary": {"name": "琥珀黄", "hex": "#FFB300"},
        "secondary1": {"name": "咖啡棕", "hex": "#4E342E"},
        "secondary2": {"name": "奶白", "hex": "#FFF8E1"},
    },
    "玫瑰粉": {
        "primary": {"name": "玫瑰粉", "hex": "#EC407A"},
        "secondary1": {"name": "莓果紫", "hex": "#7B1FA2"},
        "secondary2": {"name": "淡粉白", "hex": "#FFF0F5"},
    },
    "海洋青": {
        "primary": {"name": "海洋青", "hex": "#00ACC1"},
        "secondary1": {"name": "沙滩金", "hex": "#C9A227"},
        "secondary2": {"name": "贝壳白", "hex": "#FDF5E6"},
    },
    "抹茶绿": {
        "primary": {"name": "抹茶绿", "hex": "#7CB342"},
        "secondary1": {"name": "米白", "hex": "#F5F5DC"},
        "secondary2": {"name": "竹青", "hex": "#2E7D32"},
    },
}

# 场景关键词 → 配色映射
SCENE_KEYWORDS = {
    "时尚": ["爱马仕橙", "古驰绿", "玫瑰粉"],
    "奢侈": ["爱马仕橙", "极光紫", "古驰绿"],
    "科技": ["普拉得蓝", "长春花蓝", "海洋青"],
    "商务": ["普拉得蓝", "长春花蓝", "极光紫"],
    "金融": ["普拉得蓝", "海洋青", "古驰绿"],
    "咖啡": ["孔雀蓝", "抹茶绿", "琥珀黄"],
    "餐饮": ["孔雀蓝", "烈焰红", "爱马仕橙"],
    "自然": ["抹茶绿", "薄荷绿", "孔雀蓝"],
    "健康": ["薄荷绿", "海洋青", "玫瑰粉"],
    "儿童": ["玫瑰粉", "薄荷绿", "琥珀黄"],
    "节日": ["烈焰红", "爱马仕橙", "琥珀黄"],
    "商务正式": ["普拉得蓝", "长春花蓝", "极光紫"],
    "默认": ["普拉得蓝"],
}


# ============================================================
# 工具函数
# ============================================================

def hex_to_rgb(hex_color: str) -> tuple:
    """HEX -> RGB"""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsl(rgb: tuple) -> tuple:
    """RGB -> HSL (H=0-360, S/L=0-100)"""
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    max_c, min_c = max(r, g, b), min(r, g, b)
    l = (max_c + min_c) / 2 * 100
    if max_c == min_c:
        return (0, 0, l)
    d = max_c - min_c
    s = d / (2 - max_c - min_c) * 100 if l > 50 else d / (max_c + min_c) * 100
    if max_c == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif max_c == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return (round(h * 60), round(s), round(l))


def get_text_color(bg_rgb: tuple) -> tuple:
    """根据背景亮度返回黑白文字"""
    luminance = 0.299*bg_rgb[0] + 0.587*bg_rgb[1] + 0.114*bg_rgb[2]
    return (255, 255, 255) if luminance < 128 else (0, 0, 0)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """加载中文字体"""
    font_paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",  # Mac 黑体中粗体
        "/System/Library/Fonts/STHeiti Light.ttc",   # Mac 黑体细
        "/System/Library/Fonts/Supplemental/Songti.ttc",  # 宋体
        "/System/Library/Fonts/PingFang.ttc",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ============================================================
# 图片生成
# ============================================================

def generate_palette_card(palette_name: str, output_path: str = None) -> str:
    """生成单张配色卡"""
    if palette_name not in PALETTES:
        available = ", ".join(PALETTES.keys())
        raise ValueError(f"Unknown palette: {palette_name}. Available: {available}")

    palette = PALETTES[palette_name]

    W, H = 900, 620
    BG_COLOR = "#000000"

    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # 字体（粗体用于色名，细体用于hex）
    font_name = load_font(32, bold=True)
    font_hex = load_font(24, bold=False)
    font_small = load_font(18, bold=False)

    # ---- 主色块（上方大）----
    mx, my, mw, mh = 50, 50, 800, 310
    main_rgb = hex_to_rgb(palette["primary"]["hex"])
    draw.rounded_rectangle([mx, my, mx + mw, my + mh], radius=28, fill=main_rgb)
    text_color = get_text_color(main_rgb)
    draw.text((mx + 30, my + 30), palette["primary"]["name"], font=font_name, fill=text_color)
    draw.text((mx + 30, my + 85), palette["primary"]["hex"], font=font_hex, fill=text_color)

    # ---- 辅助色1 & 2（下方小）----
    sw, sh = 370, 170
    sy = 420

    # 辅助色1
    s1x = 50
    s1_rgb = hex_to_rgb(palette["secondary1"]["hex"])
    draw.rounded_rectangle([s1x, sy, s1x + sw, sy + sh], radius=18, fill=s1_rgb)
    t1_color = get_text_color(s1_rgb)
    draw.text((s1x + 20, sy + 20), palette["secondary1"]["name"], font=font_name, fill=t1_color)
    draw.text((s1x + 20, sy + 65), palette["secondary1"]["hex"], font=font_hex, fill=t1_color)

    # 辅助色2
    s2x = 480
    s2_rgb = hex_to_rgb(palette["secondary2"]["hex"])
    draw.rounded_rectangle([s2x, sy, s2x + sw, sy + sh], radius=18, fill=s2_rgb)
    t2_color = get_text_color(s2_rgb)
    draw.text((s2x + 20, sy + 20), palette["secondary2"]["name"], font=font_name, fill=t2_color)
    draw.text((s2x + 20, sy + 65), palette["secondary2"]["hex"], font=font_hex, fill=t2_color)

    # ---- 色值格式标注（右下角）----
    draw.text((W - 200, H - 40), "HEX · RGB · HSL", font=font_small, fill=(100, 100, 100))

    if output_path is None:
        output_path = f"/tmp/color-palette-{palette_name}.png"
    img.save(output_path, "PNG", quality=95)
    return output_path


def smart_select_palette(keywords: str) -> list:
    """根据关键词智能选择配色（返回最匹配的1-3个）"""
    keywords = keywords.lower()
    matched = []
    for scene, palettes in SCENE_KEYWORDS.items():
        if any(k in keywords for k in scene.lower()):
            matched.extend(palettes)
    # 去重，保持顺序
    seen = set()
    result = []
    for p in matched:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result if result else SCENE_KEYWORDS["默认"]


# ============================================================
# 色值导出
# ============================================================

def export_color_formats(palette_name: str) -> dict:
    """导出三种格式"""
    palette = PALETTES[palette_name]
    result = {}
    for role, data in palette.items():
        hex_c = data["hex"]
        rgb = hex_to_rgb(hex_c)
        hsl = rgb_to_hsl(rgb)
        result[role] = {
            "name": data["name"],
            "HEX": hex_c.upper(),
            "RGB": f"rgb({rgb[0]},{rgb[1]},{rgb[2]})",
            "HSL": f"hsl({hsl[0]},{hsl[1]}%,{hsl[2]}%)",
            "CSS": f"--color-{role}: {hex_c.upper()};"
        }
    return result


# ============================================================
# 批量生成
# ============================================================

def generate_all_cards(output_dir: str = "/tmp") -> dict:
    """生成所有配色卡"""
    results = {}
    for name in PALETTES:
        path = os.path.join(output_dir, f"color-palette-{name}.png")
        try:
            generated = generate_palette_card(name, path)
            results[name] = generated
        except Exception as e:
            results[name] = f"ERROR: {e}"
    return results


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    usage = """
color-palette generator v2

Usage:
  python3 generate_palette.py <palette_name> [output_path]
  python3 generate_palette.py --list
  python3 generate_palette.py --export <palette_name>
  python3 generate_palette.py --all [output_dir]
  python3 generate_palette.py --smart <keywords>

Examples:
  python3 generate_palette.py 普拉得蓝
  python3 generate_palette.py 科技感 --all /tmp/cards/
  python3 generate_palette.py --export 孔雀蓝
  python3 generate_palette.py --smart 咖啡餐饮
"""

    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "--list":
        print("Available palettes:")
        for name in PALETTES:
            p = PALETTES[name]
            print(f"  {name}: {p['primary']['hex']} | {p['secondary1']['hex']} | {p['secondary2']['hex']}")

    elif cmd == "--export":
        if len(sys.argv) < 3:
            print("Usage: --export <palette_name>")
            sys.exit(1)
        name = sys.argv[2]
        if name not in PALETTES:
            print(f"Unknown: {name}")
            sys.exit(1)
        formats = export_color_formats(name)
        print(json.dumps(formats, indent=2, ensure_ascii=False))

    elif cmd == "--all":
        out_dir = sys.argv[2] if len(sys.argv) >= 3 else "/tmp"
        results = generate_all_cards(out_dir)
        print(f"Generated {len(results)} cards in {out_dir}:")
        for name, path in results.items():
            status = "✓" if os.path.exists(path) else "✗"
            print(f"  {status} {name}: {path}")

    elif cmd == "--smart":
        if len(sys.argv) < 3:
            print("Usage: --smart <keywords>")
            sys.exit(1)
        keywords = sys.argv[2]
        selected = smart_select_palette(keywords)
        print(f"Matched palettes for '{keywords}':")
        for name in selected:
            p = PALETTES[name]
            print(f"  → {name}: {p['primary']['hex']} | {p['secondary1']['hex']} | {p['secondary2']['hex']}")

    else:
        # 单张生成
        palette_name = cmd
        output_path = sys.argv[2] if len(sys.argv) >= 3 else None
        if palette_name not in PALETTES:
            print(f"Unknown palette: {palette_name}")
            print(f"Available: {', '.join(PALETTES.keys())}")
            sys.exit(1)
        path = generate_palette_card(palette_name, output_path)
        print(f"Generated: {path}")
