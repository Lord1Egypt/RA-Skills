#!/usr/bin/env python3
"""
poster-forge: Universal image/poster generator.

Two engines:
  1. AI engine (Pollinations.ai) — generates artistic base images
  2. HTML engine (fallback) — renders HTML/CSS via headless browser screenshot

Both engines support Chinese text overlay via PIL.

Usage:
  # AI-generated base + text overlay
  python3 scripts/generate.py --title "标题" --mode ai --prompt "watercolor landscape" --output poster.jpg

  # HTML template rendered as image (fallback)
  python3 scripts/generate.py --title "标题" --mode html --template split --output poster.jpg

  # Pure text poster (no base image)
  python3 scripts/generate.py --title "标题" --mode text --bg-color "70,130,255" --output poster.jpg
"""
import argparse, os, sys, subprocess, tempfile, hashlib, json, shutil
from pathlib import Path

# ─── Font Management ───
FONT_URLS = {
    "bold": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf",
    "regular": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf",
}
FONT_DIR = Path(tempfile.gettempdir()) / "poster-forge-fonts"

def ensure_font(weight="bold"):
    FONT_DIR.mkdir(exist_ok=True)
    name = f"NotoSansCJKsc-{'Bold' if weight == 'bold' else 'Regular'}.otf"
    path = FONT_DIR / name
    if path.exists() and path.stat().st_size > 1_000_000:
        return str(path)
    url = FONT_URLS[weight]
    print(f"Downloading {weight} font...")
    subprocess.run(["curl", "-sL", url, "-o", str(path), "--max-time", "120"], check=True)
    return str(path)

def font(size, weight="bold"):
    from PIL import ImageFont
    return ImageFont.truetype(ensure_font(weight), size)

# ─── AI Engine (Pollinations.ai) ───
def ai_generate_base(prompt, width, height):
    import urllib.parse
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}?width={width}&height={height}&model=flux&nologo=true"
    tmp = Path(tempfile.gettempdir()) / f"pf_ai_{hashlib.md5(prompt.encode()).hexdigest()}.jpg"
    result = subprocess.run(["curl", "-sL", url, "-o", str(tmp), "--max-time", "180"],
                           capture_output=True)
    if result.returncode != 0 or not tmp.exists() or tmp.stat().st_size < 1000:
        return None
    return str(tmp)

# ─── HTML Engine (Headless Screenshot) ───
def html_render(html_content, width, height, output_path):
    """Render HTML to image via headless Chromium screenshot."""
    # Use output directory for temp files (snap chromium has sandbox restrictions)
    out_dir = os.path.dirname(os.path.abspath(output_path)) or "."
    html_file = os.path.join(out_dir, "pf_render_tmp.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not chromium:
        snap_chromium = "/snap/bin/chromium"
        if os.path.exists(snap_chromium):
            chromium = snap_chromium

    if not chromium:
        print("WARNING: No Chromium found, HTML engine unavailable")
        return False

    tmp_name = "pf_screenshot.png"
    result = subprocess.run([
        chromium, "--headless", "--disable-gpu", "--no-sandbox",
        f"--window-size={width},{height}",
        f"--screenshot={tmp_name}",
        f"file://{html_file}"
    ], capture_output=True, timeout=30, cwd=out_dir)
    
    tmp_path = os.path.join(out_dir, tmp_name)
    # Clean up temp html
    try: os.remove(html_file)
    except: pass
    
    if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 500:
        abs_output = os.path.abspath(output_path)
        if tmp_path != abs_output:
            shutil.move(tmp_path, abs_output)
        return True
    return False

# ─── HTML Templates ───
def get_template(name, args):
    """Return HTML string for a named template."""
    w, h = args.width, args.height
    templates = {
        "split": f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Noto Sans CJK SC','PingFang SC','Microsoft YaHei',sans-serif;display:flex;flex-direction:column;overflow:hidden}}
.top{{position:relative;display:flex;flex:1}}
.left{{flex:1;background:linear-gradient(180deg,{args.left_css_color},{args.left_css_color2});display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;color:white}}
.right{{flex:1;background:linear-gradient(180deg,{args.right_css_color},{args.right_css_color2});display:flex;flex-direction:column;align-items:center;justify-content:center;padding:40px;color:white}}
.label{{font-size:48px;font-weight:900;margin-bottom:24px}}
.chat{{background:rgba(255,255,255,0.2);border-radius:18px;padding:22px;margin:8px 0;width:90%;font-size:24px;line-height:1.6}}
.vs{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:100px;height:100px;background:linear-gradient(135deg,#ffa502,#ff6348);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:900;color:white;border:4px solid white;box-shadow:0 6px 20px rgba(0,0,0,0.3);z-index:10}}
.bottom{{background:linear-gradient(90deg,{args.left_css_color},{args.right_css_color});padding:40px;text-align:center}}
.title{{font-size:46px;font-weight:900;color:white;text-shadow:2px 2px 6px rgba(0,0,0,0.3);line-height:1.5}}
.subtitle{{font-size:28px;color:rgba(255,255,255,0.9);margin-top:10px}}
</style></head><body>
<div class="top">
<div class="left"><div class="label">{args.left_label}</div>{_chat_items(args.left_items)}</div>
<div class="vs">VS</div>
<div class="right"><div class="label">{args.right_label}</div>{_chat_items(args.right_items)}</div>
</div>
<div class="bottom"><div class="title">{args.title}</div><div class="subtitle">{args.subtitle}</div></div>
</body></html>""",

        "gradient": f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Noto Sans CJK SC','PingFang SC',sans-serif;
background:linear-gradient(135deg,{args.left_css_color},{args.right_css_color});
display:flex;flex-direction:column;align-items:center;justify-content:center;color:white;text-align:center;padding:60px}}
.title{{font-size:56px;font-weight:900;text-shadow:2px 2px 8px rgba(0,0,0,0.3);margin-bottom:30px;line-height:1.4}}
.subtitle{{font-size:34px;opacity:0.9;line-height:1.5}}
</style></head><body>
<div class="title">{args.title}</div>
<div class="subtitle">{args.subtitle}</div>
</body></html>""",

        "card": f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Noto Sans CJK SC','PingFang SC',sans-serif;
background:linear-gradient(135deg,{args.left_css_color},#f0f0f5);display:flex;align-items:center;justify-content:center}}
.card{{background:white;border-radius:30px;padding:60px;width:85%;box-shadow:0 20px 60px rgba(0,0,0,0.15);text-align:center}}
.title{{font-size:48px;font-weight:900;color:#333;margin-bottom:20px;line-height:1.4}}
.subtitle{{font-size:30px;color:#888;line-height:1.5}}
</style></head><body>
<div class="card"><div class="title">{args.title}</div><div class="subtitle">{args.subtitle}</div></div>
</body></html>""",

        "tutorial": f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w}px;height:{h}px;font-family:'Noto Sans CJK SC','PingFang SC',sans-serif;
background:#f8f7ff;padding:40px;display:flex;flex-direction:column}}
.header{{background:{args.left_css_color};padding:30px;border-radius:16px;text-align:center;color:white;font-size:42px;font-weight:900;margin-bottom:30px}}
.step{{font-size:28px;color:#555;margin:15px 0;line-height:1.6}}
.code{{background:#23233a;border-radius:14px;padding:30px;color:#b4ffb4;font-size:24px;line-height:1.8;margin:20px 0;white-space:pre-wrap}}
.footer{{background:#fff5dc;border-radius:16px;padding:25px;text-align:center;font-size:28px;color:#b46400;margin-top:auto}}
</style></head><body>
<div class="header">{args.title}</div>
<div class="step">{args.subtitle}</div>
<div class="code">{args.code_content or ''}</div>
<div class="footer">{args.tagline or ''}</div>
</body></html>""",
    }
    return templates.get(name, templates["gradient"])

def _chat_items(items_str):
    if not items_str:
        return ""
    items = [i.strip() for i in items_str.split("|") if i.strip()]
    return "\n".join(f'<div class="chat">{item}</div>' for item in items)

# ─── Text Overlay (PIL) ───
def add_text_overlay(img_path, args, output_path):
    from PIL import Image, ImageDraw
    base = Image.open(img_path).convert("RGBA")
    w, h = base.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    f_title = font(args.font_title_size)
    f_sub = font(args.font_sub_size)

    if args.text_position == "bottom":
        draw.rectangle([0, h - 240, w, h], fill=(0, 0, 0, 185))
        draw.text((w // 2, h - 170), args.title, fill="white", font=f_title, anchor="mm")
        if args.subtitle:
            draw.text((w // 2, h - 100), args.subtitle, fill="white", font=f_title, anchor="mm")
        if args.tagline:
            draw.text((w // 2, h - 45), args.tagline, fill=(255, 255, 200, 255), font=f_sub, anchor="mm")
    elif args.text_position == "center":
        draw.rectangle([0, h // 3, w, 2 * h // 3], fill=(0, 0, 0, 150))
        draw.text((w // 2, h // 2 - 30), args.title, fill="white", font=f_title, anchor="mm")
        if args.subtitle:
            draw.text((w // 2, h // 2 + 40), args.subtitle, fill=(255, 255, 200, 255), font=f_sub, anchor="mm")
    elif args.text_position == "top":
        draw.rectangle([0, 0, w, 200], fill=(0, 0, 0, 185))
        draw.text((w // 2, 70), args.title, fill="white", font=f_title, anchor="mm")
        if args.subtitle:
            draw.text((w // 2, 140), args.subtitle, fill=(255, 255, 200, 255), font=f_sub, anchor="mm")

    result = Image.alpha_composite(base, overlay).convert("RGB")
    result.save(output_path, quality=95)

# ─── Presets ───
PRESETS = {
    "xiaohongshu": {"width": 1080, "height": 1440},
    "wechat": {"width": 900, "height": 500},
    "instagram": {"width": 1080, "height": 1080},
    "twitter": {"width": 1200, "height": 675},
    "a4": {"width": 2480, "height": 3508},
}

# ─── Main ───
def main():
    p = argparse.ArgumentParser(description="Universal poster/image generator")
    p.add_argument("--title", required=True)
    p.add_argument("--subtitle", default="")
    p.add_argument("--tagline", default="")
    p.add_argument("--mode", choices=["ai", "html", "text", "auto"], default="auto",
                   help="ai=Pollinations, html=Chromium screenshot, text=PIL only, auto=ai with html fallback")
    p.add_argument("--template", choices=["split", "gradient", "card", "tutorial"], default="gradient")
    p.add_argument("--prompt", default="", help="English prompt for AI base image")
    p.add_argument("--preset", choices=list(PRESETS.keys()), default=None)
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1440)
    p.add_argument("--output", default="poster.jpg")

    # Split mode options
    p.add_argument("--left-label", default="")
    p.add_argument("--right-label", default="")
    p.add_argument("--left-items", default="", help="Pipe-separated items for left side")
    p.add_argument("--right-items", default="", help="Pipe-separated items for right side")
    p.add_argument("--left-color", default="255,70,80", help="R,G,B for left")
    p.add_argument("--right-color", default="40,200,110", help="R,G,B for right")

    # Text overlay options
    p.add_argument("--text-position", choices=["bottom", "center", "top", "none"], default="bottom")
    p.add_argument("--font-title-size", type=int, default=44)
    p.add_argument("--font-sub-size", type=int, default=30)
    p.add_argument("--bg-color", default="70,130,255", help="R,G,B for text/gradient mode background")
    p.add_argument("--code-content", default="", help="Code block content for tutorial template")
    p.add_argument("--no-overlay", action="store_true", help="Skip PIL text overlay (HTML already has text)")

    args = p.parse_args()

    # Apply preset
    if args.preset:
        ps = PRESETS[args.preset]
        args.width = ps["width"]
        args.height = ps["height"]

    # Parse colors to CSS
    lc = [int(x) for x in args.left_color.split(",")]
    rc = [int(x) for x in args.right_color.split(",")]
    bgc = [int(x) for x in args.bg_color.split(",")]
    args.left_css_color = f"rgb({lc[0]},{lc[1]},{lc[2]})"
    args.left_css_color2 = f"rgb({max(0,lc[0]-30)},{max(0,lc[1]-20)},{max(0,lc[2]-20)})"
    args.right_css_color = f"rgb({rc[0]},{rc[1]},{rc[2]})"
    args.right_css_color2 = f"rgb({max(0,rc[0]-30)},{max(0,rc[1]-20)},{max(0,rc[2]-20)})"
    args.bg_css_color = f"rgb({bgc[0]},{bgc[1]},{bgc[2]})"

    mode = args.mode
    success = False

    if mode in ("ai", "auto"):
        prompt = args.prompt or f"aesthetic poster background for topic: {args.title}"
        print(f"Trying AI engine (Pollinations.ai)...")
        base_path = ai_generate_base(prompt, args.width, args.height)
        if base_path:
            if args.no_overlay or args.text_position == "none":
                from PIL import Image
                Image.open(base_path).convert("RGB").save(args.output, quality=95)
            else:
                add_text_overlay(base_path, args, args.output)
            success = True
            print(f"AI engine succeeded.")

    if not success and mode in ("html", "auto"):
        print(f"Trying HTML engine (Chromium)...")
        html = get_template(args.template, args)
        out_dir = os.path.dirname(os.path.abspath(args.output)) or "."
        tmp_png = os.path.join(out_dir, "pf_html_tmp.png")
        if html_render(html, args.width, args.height, tmp_png):
            from PIL import Image
            Image.open(tmp_png).convert("RGB").save(args.output, quality=95)
            success = True
            print(f"HTML engine succeeded.")

    if not success and mode in ("text", "auto"):
        print(f"Using text-only engine (PIL)...")
        from PIL import Image
        bg = [int(x) for x in args.bg_color.split(",")]
        base = Image.new("RGBA", (args.width, args.height), tuple(bg + [255]))
        tmp = str(Path(tempfile.gettempdir()) / "pf_textbase.png")
        base.save(tmp)
        add_text_overlay(tmp, args, args.output)
        success = True

    if success:
        print(f"Saved: {args.output} ({os.path.getsize(args.output)} bytes)")
    else:
        print("ERROR: All engines failed.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
