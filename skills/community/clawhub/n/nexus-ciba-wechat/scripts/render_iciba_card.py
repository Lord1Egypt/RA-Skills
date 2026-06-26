#!/usr/bin/env python3
"""Render 词霸每日一句 HTML/PNG cards with selectable templates.

The renderer prefers API-provided pictures in this order:
    picture -> picture2 -> picture3 -> picture4
It only generates a local fallback image when the API fetch fails or every
picture URL fails to download.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import random
from dataclasses import dataclass
from html import escape
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

try:
    import qrcode
    from PIL import Image, ImageDraw, ImageFilter
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "missing dependency. install with: pip install pillow qrcode playwright && playwright install chromium"
    ) from exc

DEFAULT_API_URL = "https://open.iciba.com/dsapi/"
TEMPLATE_CONFIG = {
    "moments_vertical": {
        "file": "moments_vertical.html",
        "width": 540,
        "height": 960,
        "output_stem": "iciba_moments_card",
        "description": "9:16 friends-circle vertical card with image above and text below",
    },
    "postcard_horizontal": {
        "file": "postcard_horizontal.html",
        "width": 1200,
        "height": 760,
        "output_stem": "iciba_postcard_horizontal",
        "description": "horizontal postcard-style card with image left and message/right stamp area",
    },
}

FALLBACK_DATA = {
    "caption": "词霸每日一句",
    "content": "Youth like morning light holds endless promise.",
    "note": "青年如晨光，充满无限可能。",
    "translation": "新版每日一句",
    "dateline": "2026-05-04",
    "tts": "https://staticedu-wps-cache.iciba.com/audio/d06fbfd1d5352c544a22486c5d92d073.mp3",
    "picture": "https://staticedu-wps-cache.iciba.com/image/218d00efb82a82e3e5fece78507d7273.png",
}


def get_path_separator() -> str:
    """Return the native path separator requested by the host OS."""
    return "\\" if os.name == "nt" else "/"


def format_path_for_os(path: Path | str) -> str:
    """Format a path string with the separator convention of the host OS."""
    separator = get_path_separator()
    return str(path).replace("\\", separator).replace("/", separator)


@dataclass
class RenderPaths:
    output_dir: Path
    html: Path
    png: Path
    data_json: Path
    hero_image: Path
    fallback_image: Path
    hero_source: Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="render an iciba daily sentence card")
    parser.add_argument("--output-dir", default="/mnt/data/iciba-card", help="directory for generated files")
    parser.add_argument("--api-url", default=DEFAULT_API_URL, help="iciba daily sentence endpoint")
    parser.add_argument("--input-json", help="optional local JSON file instead of live API fetch")
    parser.add_argument("--template", default="moments_vertical", choices=sorted(TEMPLATE_CONFIG), help="html template to render")
    parser.add_argument("--template-dir", help="optional directory containing html templates")
    parser.add_argument("--list-templates", action="store_true", help="print available templates and exit")
    parser.add_argument("--width", type=int, help="card width in css pixels; defaults to template width")
    parser.add_argument("--height", type=int, help="card height in css pixels; defaults to template height")
    parser.add_argument("--output-stem", help="base filename for html/png/json outputs; defaults to template stem")
    parser.add_argument("--device-scale-factor", type=float, default=2.0, help="playwright screenshot scale")
    parser.add_argument("--chromium", default="/usr/bin/chromium", help="chromium executable path")
    parser.add_argument("--seed", type=int, default=5945, help="fallback image random seed")
    return parser.parse_args()


def list_templates() -> None:
    for name, config in TEMPLATE_CONFIG.items():
        print(f"{name}: {config['width']}x{config['height']} - {config['description']}")


def template_dir_from_args(args: argparse.Namespace) -> Path:
    if args.template_dir:
        return Path(args.template_dir)
    return Path(__file__).resolve().parents[1] / "templates"


def template_path(args: argparse.Namespace) -> Path:
    config = TEMPLATE_CONFIG[args.template]
    path = template_dir_from_args(args) / config["file"]
    if not path.exists():
        raise FileNotFoundError(f"template not found: {path}")
    return path


def make_paths(output_dir: Path, output_stem: str) -> RenderPaths:
    output_dir.mkdir(parents=True, exist_ok=True)
    return RenderPaths(
        output_dir=output_dir,
        html=output_dir / f"{output_stem}.html",
        png=output_dir / f"{output_stem}.png",
        data_json=output_dir / f"{output_stem}_data.json",
        hero_image=output_dir / "iciba_api_picture.png",
        fallback_image=output_dir / "iciba_generated_fallback.png",
        hero_source=output_dir / "hero_source.txt",
    )


def fetch_json(url: str, timeout: int = 20) -> dict:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def load_data(args: argparse.Namespace) -> dict:
    data = dict(FALLBACK_DATA)
    if args.input_json:
        input_path = Path(args.input_json)
        live = json.loads(input_path.read_text(encoding="utf-8"))
        data.update({k: v for k, v in live.items() if v not in (None, "")})
        data["_data_source"] = f"input_json:{input_path.name}"
        return data

    try:
        live = fetch_json(args.api_url)
        if not isinstance(live, dict):
            raise ValueError("api did not return a JSON object")
        data.update({k: v for k, v in live.items() if v not in (None, "")})
        data["_data_source"] = "live_api"
    except Exception as exc:
        data["_data_source"] = f"fallback_data:{exc.__class__.__name__}"
    return data


def picture_candidates(data: dict) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []
    for key in ("picture", "picture2", "picture3", "picture4"):
        value = data.get(key)
        if isinstance(value, str) and value.startswith("http") and all(value != url for _, url in candidates):
            candidates.append((key, value))
    return candidates


def download_image_to_png(url: str, path: Path, timeout: int = 30) -> bool:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as response:
            raw = response.read()
        image = Image.open(BytesIO(raw)).convert("RGB")
        image.save(path, format="PNG", optimize=True)
        return True
    except Exception:
        return False


def generate_fallback_hero(path: Path, seed: int) -> None:
    random.seed(seed)
    width, height = 1080, 900
    img = Image.new("RGB", (width, height), "#e7d2ac")
    px = img.load()
    top = (104, 148, 187)
    mid = (238, 189, 112)
    bottom = (92, 99, 82)
    for y in range(height):
        t = y / (height - 1)
        if t < 0.56:
            k = t / 0.56
            color = tuple(int(top[i] * (1 - k) + mid[i] * k) for i in range(3))
        else:
            k = (t - 0.56) / 0.44
            color = tuple(int(mid[i] * (1 - k) + bottom[i] * k) for i in range(3))
        for x in range(width):
            px[x, y] = color

    draw = ImageDraw.Draw(img, "RGBA")
    cx, cy = int(width * 0.27), int(height * 0.40)
    for radius in range(360, 20, -12):
        alpha = max(0, int(70 * (1 - radius / 360)))
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=(255, 226, 145, alpha))
    draw.ellipse((cx - 82, cy - 82, cx + 82, cy + 82), fill=(255, 225, 142, 190))

    for i in range(9):
        y = int(height * (0.18 + i * 0.045))
        draw.rounded_rectangle((-80 + i * 25, y, width + 80, y + 38), radius=30, fill=(255, 244, 220, 18))

    mountains = [
        [(0, height * 0.60), (160, height * 0.48), (340, height * 0.61), (500, height * 0.43), (720, height * 0.63), (930, height * 0.49), (width, height * 0.61), (width, height), (0, height)],
        [(0, height * 0.70), (210, height * 0.56), (420, height * 0.72), (650, height * 0.52), (870, height * 0.70), (width, height * 0.58), (width, height), (0, height)],
        [(0, height * 0.80), (180, height * 0.70), (360, height * 0.82), (590, height * 0.66), (820, height * 0.82), (width, height * 0.72), (width, height), (0, height)],
    ]
    fills = [(56, 75, 79, 150), (62, 89, 83, 175), (55, 72, 55, 210)]
    for polygon, fill in zip(mountains, fills):
        draw.polygon([(int(x), int(y)) for x, y in polygon], fill=fill)

    for _ in range(900):
        x = random.randint(0, width - 1)
        y = random.randint(int(height * 0.72), height - 1)
        length = random.randint(8, 38)
        alpha = random.randint(20, 70)
        draw.line((x, y, x + random.randint(-8, 8), y - length), fill=(31, 52, 34, alpha), width=random.choice([1, 1, 2]))

    noise = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    nd = ImageDraw.Draw(noise, "RGBA")
    for _ in range(17000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        alpha = random.randint(5, 15)
        color = (255, 248, 225, alpha) if random.random() < 0.5 else (40, 32, 24, alpha)
        nd.point((x, y), fill=color)
    img = Image.alpha_composite(img.convert("RGBA"), noise).convert("RGB")
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(path, quality=95)


def choose_hero(data: dict, paths: RenderPaths, seed: int) -> tuple[Path, str, str, str]:
    for field_name, url in picture_candidates(data):
        if download_image_to_png(url, paths.hero_image):
            return paths.hero_image, "api_picture", field_name, url
    generate_fallback_hero(paths.fallback_image, seed)
    return paths.fallback_image, "generated_fallback", "fallback", ""


def data_uri(path: Path, mime: str = "image/png") -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def qr_data_uri(text: str) -> str:
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    qimg = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    buf = BytesIO()
    qimg.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")


def issue_parts(dateline: str) -> tuple[str, str]:
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    try:
        year, month, day = dateline.split("-")
        return day.zfill(2), f"{months[int(month) - 1]} · {year}"
    except Exception:
        return "01", "Daily"


def fit_font_size(text: str, template: str) -> int:
    length = len(text or "")
    if template == "postcard_horizontal":
        if length > 130:
            return 30
        if length > 100:
            return 35
        if length > 70:
            return 42
        return 52
    if length > 115:
        return 30
    if length > 90:
        return 34
    if length > 70:
        return 37
    return 42


def build_context(data: dict, hero_uri: str, qr_uri: str, hero_source: str, hero_field: str, hero_url: str, args: argparse.Namespace, width: int, height: int) -> dict[str, str]:
    dateline = str(data.get("dateline", FALLBACK_DATA["dateline"]))
    issue_day, issue_text = issue_parts(dateline)
    status = f"playwright png · {data.get('_data_source', 'fallback_data')} · template={args.template} · hero={hero_source}"
    return {
        "WIDTH": str(width),
        "HEIGHT": str(height),
        "TEMPLATE_NAME": args.template,
        "CAPTION": escape(str(data.get("caption", FALLBACK_DATA["caption"]))),
        "CONTENT": escape(str(data.get("content", FALLBACK_DATA["content"]))),
        "NOTE": escape(str(data.get("note", FALLBACK_DATA["note"]))),
        "TRANSLATION": escape(str(data.get("translation", FALLBACK_DATA["translation"]))),
        "DATELINE": escape(dateline),
        "ISSUE_DAY": escape(issue_day),
        "ISSUE_TEXT": escape(issue_text),
        "QUOTE_SIZE": str(fit_font_size(str(data.get("content", "")), args.template)),
        "HERO_URI": hero_uri,
        "HERO_ALT": escape(f"{data.get('caption', '词霸每日一句')}配图"),
        "QR_URI": qr_uri,
        "TTS_URL": escape(str(data.get("tts", FALLBACK_DATA["tts"]))),
        "STATUS": escape(status),
        "HERO_SOURCE": escape(hero_source),
        "HERO_FIELD": escape(hero_field),
        "HERO_URL": escape(hero_url),
    }


def render_template(template_text: str, context: dict[str, str]) -> str:
    rendered = template_text
    for key, value in context.items():
        rendered = rendered.replace(f"[[{key}]]", value)
    return rendered


def write_html(args: argparse.Namespace, paths: RenderPaths, context: dict[str, str]) -> None:
    source = template_path(args).read_text(encoding="utf-8")
    html = render_template(source, context)
    paths.html.write_text(html, encoding="utf-8")


def render_png(paths: RenderPaths, width: int, height: int, scale: float, chromium_path: str) -> None:
    with sync_playwright() as p:
        launch_kwargs = {"headless": True, "args": ["--no-sandbox"]}
        if chromium_path and Path(chromium_path).exists():
            launch_kwargs["executable_path"] = chromium_path
        browser = p.chromium.launch(**launch_kwargs)
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=scale)
        page.set_content(paths.html.read_text(encoding="utf-8"), wait_until="load")
        page.locator("#card").screenshot(path=str(paths.png))
        browser.close()


def main() -> None:
    args = parse_args()
    if args.list_templates:
        list_templates()
        return

    config = TEMPLATE_CONFIG[args.template]
    width = args.width or int(config["width"])
    height = args.height or int(config["height"])
    output_stem = args.output_stem or str(config["output_stem"])

    paths = make_paths(Path(args.output_dir), output_stem)
    data = load_data(args)
    hero_path, hero_source, hero_field, hero_url = choose_hero(data, paths, args.seed)
    hero_uri = data_uri(hero_path)
    qr_uri = qr_data_uri(str(data.get("tts", FALLBACK_DATA["tts"])))
    context = build_context(data, hero_uri, qr_uri, hero_source, hero_field, hero_url, args, width, height)

    data["_template"] = args.template
    data["_path_separator"] = get_path_separator()
    data["_output_dir"] = format_path_for_os(paths.output_dir)
    data["_hero_source"] = hero_source
    data["_hero_field"] = hero_field
    data["_hero_url"] = hero_url
    data["_picture_priority"] = ["picture", "picture2", "picture3", "picture4"]
    paths.data_json.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    paths.hero_source.write_text(f"{hero_source}\n{hero_field}\n{hero_url}\n", encoding="utf-8")

    write_html(args, paths, context)
    render_png(paths, width, height, args.device_scale_factor, args.chromium)

    print(f"[OK] template: {args.template}")
    print(f"[OK] data source: {data.get('_data_source')}")
    print(f"[OK] hero source: {hero_source}")
    print(f"[OK] hero field: {hero_field}")
    if hero_url:
        print(f"[OK] hero url: {hero_url}")
    print(f"[OK] wrote {format_path_for_os(paths.html)}")
    print(f"[OK] wrote {format_path_for_os(paths.png)}")
    print(f"[OK] wrote {format_path_for_os(paths.data_json)}")
    print(f"[OK] wrote {format_path_for_os(paths.hero_source)}")


if __name__ == "__main__":
    main()
