#!/usr/bin/env python3
"""
generate_mockup.py
将配色方案应用到真实场景 Mockup：海报 / 手机界面 / PPT背景
支持：纯色背景 + 渐变背景 + 几何图形装饰
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

# 加载配色
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


def load_font(size, bold=False):
    paths = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]
    from PIL import ImageFont
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def get_text_color(bg_hex):
    rgb = hex_to_rgb(bg_hex)
    luminance = 0.299*rgb[0] + 0.587*rgb[1] + 0.114*rgb[2]
    return "#FFFFFF" if luminance < 128 else "#000000"


def draw_gradient(draw, x0, y0, x1, y1, color1, color2, steps=30):
    """绘制渐变矩形"""
    r1,g1,b1 = hex_to_rgb(color1)
    r2,g2,b2 = hex_to_rgb(color2)
    h = y1 - y0
    for i in range(steps):
        ratio = i / (steps - 1)
        r = int(r1 + (r2-r1)*ratio)
        g = int(g1 + (g2-g1)*ratio)
        b = int(b1 + (b2-b1)*ratio)
        y = y0 + int(i * h / steps)
        draw.line([(x0, y), (x1, y)], fill=(r,g,b), width=max(1, h//steps))


# ============================================================
# 海报 Mockup
# ============================================================
def make_poster(palette_name, title="BRAND", subtitle="品牌设计", output_path=None):
    p = PALETTES[palette_name]
    W, H = 600, 860
    img = Image.new("RGB", (W, H), p["primary"])
    draw = ImageDraw.Draw(img)

    font_title = load_font(56, bold=True)
    font_sub = load_font(28)
    font_label = load_font(20)
    font_small = load_font(16)

    # 背景渐变叠加
    draw_gradient(draw, 0, 0, W, H, p["primary"], p["secondary1"])

    # 装饰圆形
    draw.ellipse([W-200, -50, W+50, 200], fill=p["secondary2"]+"40")
    draw.ellipse([-80, H-250, 200, H+50], fill=p["secondary2"]+"30")

    # 主标题
    text_color = get_text_color(p["primary"])
    bbox = draw.textbbox((0,0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 160), title, font=font_title, fill=text_color)

    # 副标题
    bbox = draw.textbbox((0,0), subtitle, font=font_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 240), subtitle, font=font_sub, fill=text_color)

    # 配色条
    bar_y = 560
    bar_h = 6
    bar_w = W // 3
    draw.rectangle([0, bar_y, bar_w, bar_y+bar_h], fill=p["primary"])
    draw.rectangle([bar_w, bar_y, bar_w*2, bar_y+bar_h], fill=p["secondary1"])
    draw.rectangle([bar_w*2, bar_y, W, bar_y+bar_h], fill=p["secondary2"])

    # 配色标注
    labels = [(p["primary"], "主色"), (p["secondary1"], "辅助色1"), (p["secondary2"], "辅助色2")]
    lx = 60
    for hex_c, label in labels:
        rgb = hex_to_rgb(hex_c)
        draw.rounded_rectangle([lx, 610, lx+120, 720], radius=12, fill=rgb)
        tc = get_text_color(hex_c)
        draw.text((lx+10, 620), label, font=font_label, fill=tc)
        draw.text((lx+10, 655), hex_c, font=font_small, fill=tc)
        lx += 140

    # 底部品牌标注
    draw.text((60, H-60), f"COLOR PALETTE · {palette_name}", font=font_small, fill="#FFFFFF80")

    if output_path is None:
        output_path = f"/tmp/mockup-poster-{palette_name}.png"
    img.save(output_path, "PNG")
    return output_path


# ============================================================
# 手机界面 Mockup
# ============================================================
def make_phone_ui(palette_name, app_name="APP", output_path=None):
    p = PALETTES[palette_name]
    W, H = 380, 700
    img = Image.new("RGB", (W, H), p["secondary2"])
    draw = ImageDraw.Draw(img)

    font_title = load_font(30, bold=True)
    font_body = load_font(20)
    font_small = load_font(14)

    # 顶部主色区域（模拟状态栏+导航栏）
    draw.rectangle([0, 0, W, 220], fill=p["primary"])

    # 装饰
    draw.ellipse([W-100, 140, W+30, 270], fill=p["secondary1"]+"60")
    draw.ellipse([-30, -30, 100, 100], fill=p["secondary1"]+"40")

    # APP名称
    text_color = get_text_color(p["primary"])
    bbox = draw.textbbox((0,0), app_name, font=font_title)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, 80), app_name, font=font_title, fill=text_color)

    # 内容卡片区
    card_y = 260
    for i in range(3):
        cy = card_y + i * 130
        draw.rounded_rectangle([30, cy, W-30, cy+100], radius=16, fill="#FFFFFF")
        # 卡片色块
        draw.rounded_rectangle([50, cy+15, 130, cy+85], radius=10, fill=p["primary"] if i==0 else (p["secondary1"] if i==1 else p["secondary2"]))
        # 文字线
        for j in range(2):
            line_w = 100 + (i*20)
            draw.text((150, cy+30+j*25), "─────────────", font=font_small, fill="#CCCCCC")

    # 底部Tab栏
    draw.rectangle([0, H-80, W, H], fill="#FFFFFF")
    draw.rectangle([0, H-82, W, H-80], fill="#E0E0E0")
    tab_colors = [p["primary"], p["secondary1"], p["secondary2"]]
    for i, c in enumerate(tab_colors):
        tx = W//3*i + W//6
        draw.ellipse([tx-15, H-60, tx+15, H-30], fill=c)

    if output_path is None:
        output_path = f"/tmp/mockup-phone-{palette_name}.png"
    img.save(output_path, "PNG")
    return output_path


# ============================================================
# PPT/封面 Mockup
# ============================================================
def make_cover(palette_name, headline="COLOR", output_path=None):
    p = PALETTES[palette_name]
    W, H = 960, 540
    img = Image.new("RGB", (W, H), p["primary"])
    draw = ImageDraw.Draw(img)

    font_hl = load_font(72, bold=True)
    font_body = load_font(24)

    # 渐变背景
    draw_gradient(draw, 0, 0, W, H, p["primary"], p["secondary1"])

    # 几何装饰
    draw.ellipse([W-300, -150, W+100, 250], fill=p["secondary2"]+"50")
    draw.ellipse([-150, H-200, 200, H+100], fill=p["secondary2"]+"30")

    # 左侧大圆形装饰
    draw.ellipse([60, 120, 260, 320], outline=p["secondary2"], width=4)

    # 标题
    text_color = get_text_color(p["primary"])
    bbox = draw.textbbox((0,0), headline, font=font_hl)
    tw = bbox[2] - bbox[0]
    draw.text(((W-tw)//2, H//2-60), headline, font=font_hl, fill=text_color)

    # 配色条
    bar_y = H - 80
    colors = [p["primary"], p["secondary1"], p["secondary2"]]
    names = ["主色", "辅助色1", "辅助色2"]
    x = 60
    for c, nm in zip(colors, names):
        draw.rounded_rectangle([x, bar_y, x+200, bar_y+40], radius=8, fill=c)
        tc = get_text_color(c)
        draw.text((x+10, bar_y+10), nm, font=font_body, fill=tc)
        x += 230

    if output_path is None:
        output_path = f"/tmp/mockup-cover-{palette_name}.png"
    img.save(output_path, "PNG")
    return output_path


if __name__ == "__main__":
    usage = """
generate_mockup.py — 配色场景应用 Mockup 生成器

Usage:
  python3 generate_mockup.py poster <palette_name> [output_path]
  python3 generate_mockup.py phone <palette_name> [output_path]
  python3 generate_mockup.py cover <palette_name> [output_path]
  python3 generate_mockup.py all <palette_name> [output_dir]

Examples:
  python3 generate_mockup.py poster 普拉得蓝
  python3 generate_mockup.py phone 玫瑰粉 /tmp/phone.png
  python3 generate_mockup.py cover 爱马仕橙
  python3 generate_mockup.py all 孔雀蓝 /tmp/
"""
    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    palette = sys.argv[2]
    out = sys.argv[3] if len(sys.argv) >= 4 else None

    if palette not in PALETTES:
        print(f"Unknown palette: {palette}")
        print(f"Available: {', '.join(PALETTES.keys())}")
        sys.exit(1)

    if cmd == "poster":
        path = make_poster(palette, output_path=out)
        print(f"Poster: {path}")
    elif cmd == "phone":
        path = make_phone_ui(palette, output_path=out)
        print(f"Phone UI: {path}")
    elif cmd == "cover":
        path = make_cover(palette, output_path=out)
        print(f"Cover: {path}")
    elif cmd == "all":
        od = out or "/tmp"
        for fn, maker in [("poster", make_poster), ("phone", make_phone_ui), ("cover", make_cover)]:
            maker(palette, output_path=os.path.join(od, f"mockup-{fn}-{palette}.png"))
        print(f"All mockups saved to {od}/")
    else:
        print(usage)
