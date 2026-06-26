#!/usr/bin/env python3
"""
extract_palette.py — 从图片提取主色调并生成配色卡
"""

import sys
import os
import io
import requests
import colorsys
from PIL import Image, ImageDraw, ImageFont

PALETTES = {
    "爱马仕橙": {"primary": "#FF8A00", "secondary1": "#363636", "secondary2": "#FFF2DF"},
    "普拉得蓝": {"primary": "#0175CC", "secondary1": "#B78D77", "secondary2": "#FCF5E2"},
    "长春花蓝": {"primary": "#5357A0", "secondary1": "#FED81F", "secondary2": "#FEFFEF"},
    "孔雀蓝": {"primary": "#0B7E9D", "secondary1": "#D7B9A1", "secondary2": "#F9F6E5"},
    "古驰绿": {"primary": "#1F4433", "secondary1": "#FF8B31", "secondary2": "#FFFBF0"},
    "烈焰红": {"primary": "#E53935", "secondary1": "#212121", "secondary2": "#FAFAFA"},
    "极光紫": {"primary": "#8E24AA", "secondary1": "#D4AF37", "secondary2": "#F8F8FF"},
    "薄荷绿": {"primary": "#26A69A", "secondary1": "#455A64", "secondary2": "#F0FFF0"},
    "琥珀黄": {"primary": "#FFB300", "secondary1": "#4E342E", "secondary2": "#FFF8E1"},
    "玫瑰粉": {"primary": "#EC407A", "secondary1": "#7B1FA2", "secondary2": "#FFF0F5"},
    "海洋青": {"primary": "#00ACC1", "secondary1": "#C9A227", "secondary2": "#FDF5E6"},
    "抹茶绿": {"primary": "#7CB342", "secondary1": "#F5F5DC", "secondary2": "#2E7D32"},
}


def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r, g, b):
    return f"#{r:02X}{g:02X}{b:02X}"


def get_text_color(bg_rgb):
    luminance = 0.299*bg_rgb[0] + 0.587*bg_rgb[1] + 0.114*bg_rgb[2]
    return (255, 255, 255) if luminance < 128 else (0, 0, 0)


def load_font(size):
    paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def extract_colors(img_path, n=6):
    """用像素采样 + K-Means 提取 n 种主色"""
    try:
        img = Image.open(img_path)
    except Exception:
        resp = requests.get(img_path, timeout=10)
        img = Image.open(io.BytesIO(resp.content))
    
    img = img.convert("RGB")
    img_small = img.resize((60, 60), Image.LANCZOS)
    
    # 采样所有像素
    pixels = list(img_small.getdata())
    
    # 简版 K-Means（固定种子）
    import random
    random.seed(42)
    centroids = random.sample(pixels, min(n, len(pixels)))
    for _ in range(8):
        clusters = [[] for _ in range(n)]
        for px in pixels:
            dists = [sum((px[c]-cc[c])**2 for c in range(3)) for cc in centroids]
            clusters[dists.index(min(dists))].append(px)
        new_c = []
        for cl in clusters:
            if cl:
                avg = tuple(sum(cl[i]//len(cl) for i in range(3)))
                new_c.append(avg)
            else:
                new_c.append(centroids[clusters.index(cl)])
        centroids = new_c
    
    # 按频率排序
    cluster_sizes = [len(cl) for cl in clusters]
    sorted_idx = sorted(range(n), key=lambda i: cluster_sizes[i], reverse=True)
    
    results = []
    for idx in sorted_idx:
        r, g, b = centroids[idx]
        h, s, l = colorsys.rgb_to_hls(r/255, g/255, b/255)
        results.append({
            "rgb": (r, g, b),
            "hex": rgb_to_hex(r, g, b),
            "hsl": (round(h*360), round(s*100), round(l*100)),
        })
    return results


def find_similar(primary_hex, top_n=3):
    """找最接近的预置配色"""
    rgb = hex_to_rgb(primary_hex)
    h, s, l = colorsys.rgb_to_hls(rgb[0]/255, rgb[1]/255, rgb[2]/255)
    
    scores = {}
    for name, pal in PALETTES.items():
        prgb = hex_to_rgb(pal["primary"])
        ph, ps, pl = colorsys.rgb_to_hls(prgb[0]/255, prgb[1]/255, prgb[2]/255)
        dist = abs(h - ph) * 0.5 + abs(l - pl) * 0.5
        scores[name] = dist
    
    return [name for name, _ in sorted(scores.items(), key=lambda x: x[1])[:top_n]]


def generate_card(colors, output_path=None):
    """生成提取颜色的配色卡"""
    W, H = 900, 600
    img = Image.new("RGB", (W, H), "#000000")
    draw = ImageDraw.Draw(img)
    
    font_name = load_font(28)
    font_hex = load_font(20)
    font_small = load_font(16)
    
    # 显示提取的颜色（两排，每排3个）
    for i, color in enumerate(colors[:6]):
        row, col = i // 3, i % 3
        x = 60 + col * 270
        y = 60 + row * 150
        rgb = color["rgb"]
        draw.rounded_rectangle([x, y, x+240, y+120], radius=16, fill=rgb)
        tc = get_text_color(rgb)
        draw.text((x+15, y+15), "Color " + str(i+1), font=font_small, fill=tc)
        draw.text((x+15, y+40), color["hex"], font=font_hex, fill=tc)
        draw.text((x+15, y+70), "RGB" + str(rgb), font=font_small, fill=tc)
    
    # 辅助色推荐
    if colors:
        primary_rgb = colors[0]["rgb"]
        h, s, l = colorsys.rgb_to_hls(primary_rgb[0]/255, primary_rgb[1]/255, primary_rgb[2]/255)
        
        # 互补色
        comp_h = (h + 0.5) % 1.0
        comp_rgb = colorsys.hls_to_rgb(comp_h, l, s)
        comp_hex = rgb_to_hex(int(comp_rgb[0]*255), int(comp_rgb[1]*255), int(comp_rgb[2]*255))
        
        # 相似色
        similar_h = (h + 0.08) % 1.0
        similar_rgb = colorsys.hls_to_rgb(similar_h, min(l+0.1, 1.0), s)
        similar_hex = rgb_to_hex(int(similar_rgb[0]*255), int(similar_rgb[1]*255), int(similar_rgb[2]*255))
        
        draw.text((60, 380), "Recommended Palette", font=font_name, fill=(180, 180, 180))
        
        rec = [("Complementary", comp_hex), ("Analogous", similar_hex)]
        rx = 60
        for label, hex_c in rec:
            rgb_c = hex_to_rgb(hex_c)
            draw.rounded_rectangle([rx, 430, rx+380, 540], radius=16, fill=rgb_c)
            tc = get_text_color(rgb_c)
            draw.text((rx+15, 440), label, font=font_hex, fill=tc)
            draw.text((rx+15, 475), hex_c, font=font_hex, fill=tc)
            rx += 400
    
    if output_path is None:
        output_path = "/tmp/extracted-palette.png"
    img.save(output_path, "PNG")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: extract_palette.py <image_path_or_url> [--card output_path]")
        sys.exit(1)
    
    img_arg = sys.argv[1]
    
    # 下载URL图片
    if img_arg.startswith("http"):
        resp = requests.get(img_arg, timeout=10)
        img_path = "/tmp/extracted_source.png"
        with open(img_path, "wb") as f:
            f.write(resp.content)
    else:
        img_path = img_arg
    
    if "--card" in sys.argv:
        idx = sys.argv.index("--card")
        out_path = sys.argv[idx+1] if idx+1 < len(sys.argv) else None
        colors = extract_colors(img_path)
        path = generate_card(colors, out_path)
        print("Card:", path)
    else:
        colors = extract_colors(img_path)
        print("Extracted colors:")
        for i, c in enumerate(colors):
            print("  " + str(i+1) + ". HEX=" + c["hex"] + " RGB=" + str(c["rgb"]))
