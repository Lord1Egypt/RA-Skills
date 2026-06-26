#!/usr/bin/env python3
"""
Knowledge Card Renderer - Convert Markdown to beautiful card images.

Dependencies: pip install markdown html2image pillow
Optional:     pip install Pygments  (for syntax highlighting)
"""

import argparse
import os
import sys
import tempfile
from pathlib import Path
from PIL import Image

THEMES = {
    "warm": {
        "bg": "#FFF8F0",
        "card": "#FDBA74",
        "accent": "#E8734A",
        "accent_light": "#FFF0E8",
        "text": "#2D2D2D",
        "text_secondary": "#6B6B6B",
        "border": "#E8DDD4",
        "code_bg": "#F5EDE5",
        "shadow": "0 4px 12px rgba(0,0,0,0.1)",
    },
    "cool": {
        "bg": "#F0F4F8",
        "card": "white",
        "accent": "#3B82F6",
        "accent_light": "#EBF4FF",
        "text": "#1E293B",
        "text_secondary": "#64748B",
        "border": "#CBD5E1",
        "code_bg": "#E2E8F0",
    },
    "minimal": {
        "bg": "#FFFFFF",
        "card": "white",
        "accent": "#333333",
        "accent_light": "#F5F5F5",
        "text": "#1A1A1A",
        "text_secondary": "#777777",
        "border": "#E5E5E5",
        "code_bg": "#F9F9F9",
    },
    "girly": {
        "bg": "#FFF0F5",              # 淡粉背景
        "card": "white",
        "accent": "#FF6FA5",          # 玫粉主色
        "accent_light": "#FFE3EC",    # 浅粉辅助
        "text": "#4A2C2A",            # 温柔棕色文字
        "text_secondary": "#A67C8A",  # 灰粉次级文字
        "border": "#FFD1DC",          # 粉色边框
        "code_bg": "#FFF7FA",         # 很浅的粉背景
    },
    "metal": {
        "bg": "#0A1F33",              
        "card": "#2A3440",
        "accent": "#8FA3B8",          # 冷钢蓝主色
        "accent_light": "#2A3440",    # 深灰金属辅助
        "text": "#E6EDF3",            # 银白文字
        "text_secondary": "#9AA4AE",  # 冷灰次级文字
        "border": "#3B4752",          # 金属灰边框
        "code_bg": "#161B22",         # 深色代码背景
    },

    "tech": {
        # 背景层
        "bg": "#020617",            # 更深的黑蓝（拉开层级）
        "card": "#0B1220",          # 卡片背景（明显区分）
        "section": "#111827",       # 模块块背景
        "accent_light": "#111827",
        # 主色系统
        "accent": "#3B82F6",        # 主蓝（更稳）
        "highlight": "#22D3EE",     # 科技青（关键点缀🔥）
        "glow": "#60A5FA",          # 柔和发光

        # 文本
        "text": "#F1F5F9",          # 提亮（更清晰）
        "text_secondary": "#94A3B8",

        # 边框 / 分割
        "border": "#1F2937",        # 更暗一点，避免抢眼

        # 特殊区域
        "code_bg": "#020617",       # 直接统一更干净
    }
}

CSS_TEMPLATE = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700&display=swap');

* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    background: {bg};
    color: {text};
    padding: 40px;
    line-height: 1.7;
    -webkit-font-smoothing: antialiased;
}}

.card {{
    max-width: {width}px;
    margin: 0 auto;
    background: {card};
    border-radius: 16px;
    padding: 40px 48px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06), 0 1px 4px rgba(0,0,0,0.04);
    border: 1px solid {border};
}}

h1 {{
    font-size: 28px;
    font-weight: 700;
    color: {accent};
    text-shadow: 0 0 12px rgba(59,130,246,0.4);
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 3px solid {accent};
    letter-spacing: -0.5px;
}}

h2 {{
    font-size: 18px;
    font-weight: 600;
    color: {text};
    margin-top: 28px;
    margin-bottom: 12px;
    padding-left: 12px;
    border-left: 4px solid {accent};
}}

h3 {{
    font-size: 15px;
    font-weight: 600;
    color: {text_secondary};
    margin-top: 20px;
    margin-bottom: 8px;
}}

p {{
    margin-bottom: 12px;
    font-size: 15px;
    color: {text};
}}

blockquote {{
    background: {accent_light};
    border-left: 4px solid {accent};
    margin: 16px 0;
    padding: 14px 20px;
    border-radius: 0 8px 8px 0;
    font-size: 15px;
    color: {text};
}}

blockquote p {{
    margin-bottom: 0;
}}

ul, ol {{
    margin: 12px 0;
    padding-left: 24px;
}}

li {{
    margin-bottom: 8px;
    font-size: 15px;
}}

li strong {{
    color: {accent};
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0;
    font-size: 14px;
    border-radius: 8px;
    overflow: hidden;
    border: 1px dashed {border};
}}

thead {{
    background: {accent};
    color: white;
}}

th {{
    padding: 12px 16px;
    text-align: left;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

td {{
    padding: 10px 16px;
    border-bottom: 1px solid {border};
    vertical-align: top;
}}

tr:last-child td {{
    border-bottom: none;
}}

tr:nth-child(even) {{
    background: {accent_light};
}}

code {{
    font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
    background: {code_bg};
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
    color: {accent};
}}

pre {{
    background: {code_bg};
    border-radius: 8px;
    padding: 16px 20px;
    margin: 16px 0;
    overflow-x: auto;
    border: 1px solid {border};
}}

pre code {{
    background: none;
    padding: 0;
    font-size: 13px;
    color: {text};
}}

hr {{
    border: none;
    border-top: 2px dashed {border};
    margin: 24px 0;
}}

strong {{
    font-weight: 600;
    color: {text};
}}

em {{
    font-style: italic;
    color: {text_secondary};
}}

.footer {{
    text-align: center;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid {border};
    font-size: 12px;
    color: {text_secondary};
    letter-spacing: 1px;
}}
"""


def convert_md_to_html(md_path: str, theme_name: str = "warm", width: int = 800) -> str:
    """Convert a Markdown file to styled HTML."""
    import markdown

    theme = THEMES.get(theme_name, THEMES["warm"])

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML with extensions
    extensions = ["tables", "fenced_code", "codehilite", "toc", "sane_lists"]
    try:
        md_html = markdown.markdown(md_content, extensions=extensions)
    except ImportError:
        # Fallback without codehilite if Pygments not installed
        extensions = ["tables", "fenced_code", "toc", "sane_lists"]
        md_html = markdown.markdown(md_content, extensions=extensions)

    css = CSS_TEMPLATE.format(width=width, **theme)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>{css}</style>
</head>
<body>
    <div class="card">
        {md_html}
    </div>
</body>
</html>"""
    return html


def _find_browser() -> str:
    """Find Chrome or Edge executable on the system."""
    import shutil

    candidates = [
        os.environ.get("CHROME_PATH"),
        os.environ.get("EDGE_PATH"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium-browser",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    # Try PATH
    for name in ["chrome", "chromium", "google-chrome", "msedge"]:
        found = shutil.which(name)
        if found:
            return found
    raise FileNotFoundError(
        "No Chrome/Edge executable found. Set CHROME_PATH or EDGE_PATH env var."
    )


def render_html_to_png(html: str, output_path: str, width: int = 820) -> str:
    """Render HTML string to PNG using html2image."""
    from html2image import Html2Image

    browser_path = _find_browser()
    hti = Html2Image(
        browser_executable=browser_path,
        size=(width + 80, 10),
        output_path=os.path.dirname(output_path) or ".",
    )

    # Write HTML to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        temp_html = f.name

    try:
        screenshot_path = hti.screenshot(
            html_file=temp_html,
            save_as=os.path.basename(output_path),
            size=(width + 80, 1600),  # Will auto-crop
        )
        # html2image returns a list
        result = screenshot_path[0] if isinstance(screenshot_path, list) else screenshot_path
        if os.path.exists(result):
            return result
        # Try to find it in output_path directory
        if os.path.exists(output_path):
            return output_path
        return result
    finally:
        os.unlink(temp_html)

def color_distance(c1, c2):
    return sum(abs(a - b) for a, b in zip(c1, c2))


def detect_background_color_robust(image_path: str, sample_step: int = 10, tolerance: int = 20):
    from collections import defaultdict
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    w, h = img.size

    clusters = []

    # 采样边缘
    samples = []
    for x in range(0, w, sample_step):
        samples.append(pixels[x, 0])
        samples.append(pixels[x, h - 1])

    for y in range(0, h, sample_step):
        samples.append(pixels[0, y])
        samples.append(pixels[w - 1, y])

    # 聚类颜色
    for color in samples:
        found = False
        for cluster in clusters:
            if color_distance(color, cluster["color"]) < tolerance:
                cluster["count"] += 1
                found = True
                break
        if not found:
            clusters.append({"color": color, "count": 1})

    # 取最大 cluster
    bg_color = max(clusters, key=lambda x: x["count"])["color"]
    return bg_color

def crop_image(image_path: str) -> None:
    """Crop image to remove excess whitespace at the bottom."""
    try:
        #from PIL import Image

        img = Image.open(image_path)
        # Auto-crop: find the bounding box of non-background pixels
        # Use a simple approach: crop to content height
        pixels = img.load()
        w, h = img.size
        # Find last non-white row (approximate)
        #bg_color = (255, 248, 240)  # warm bg
        bg_color = detect_background_color_robust(image_path)
        
        for y in range(h - 1, 0, -1):
            row_pixels = [pixels[x, y] for x in range(0, w, 50)]
            # Check if any pixel differs from background significantly
            if any(
                abs(p[0] - bg_color[0]) + abs(p[1] - bg_color[1]) + abs(p[2] - bg_color[2]) > 30
                for p in row_pixels
                if len(p) >= 3
            ):
                crop_h = min(y + 40, h)
                img.crop((0, 0, w, crop_h)).save(image_path)
                return
    except Exception as e:
        print(f"[crop_image ERROR] {e}")
        pass  # Skip cropping if PIL not available or any error


def main():
    # Fix Windows console encoding for emoji output
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Render Markdown Knowledge Card to PNG")
    parser.add_argument("input", help="Path to Markdown file")
    parser.add_argument("--output", "-o", help="Output PNG path (default: same as input with .png)")
    parser.add_argument("--theme", "-t", choices=["warm", "cool", "minimal", "girly", "tech", "metal"], default="warm")
    parser.add_argument("--width", "-w", type=int, default=800, help="Card width in pixels")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output = args.output or str(Path(args.input).with_suffix(".png"))

    print(f"[1/3] Converting Markdown to HTML...")
    html = convert_md_to_html(args.input, args.theme, args.width)

    print(f"[2/3] Rendering to image...")
    result = render_html_to_png(html, output, args.width)

    print(f"[3/3] Finalizing...")
    crop_image(result)

    print(f"\n✅ Card rendered: {result}")
    print(result)


if __name__ == "__main__":
    main()
