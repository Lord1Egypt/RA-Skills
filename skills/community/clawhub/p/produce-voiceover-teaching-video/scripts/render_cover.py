#!/usr/bin/env python3
"""Render an exact-text portrait cover with a deterministic technology style."""

import argparse
import html
import json
import os
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path


def display_width(text: str) -> float:
    return sum(0.58 if ord(char) < 128 else 1.0 for char in text)


def wrap_title(title: str, limit: float = 9.0):
    if "|" in title:
        return [part.strip() for part in title.split("|") if part.strip()][:3]
    lines, current = [], ""
    for char in title:
        if current and display_width(current + char) > limit:
            lines.append(current)
            current = char
        else:
            current += char
    if current:
        lines.append(current)
    return lines[:3]


def find_browser():
    program_files = os.environ.get("ProgramFiles", "")
    program_files_x86 = os.environ.get("ProgramFiles(x86)", "")
    candidates = [
        shutil.which("chrome"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("msedge"),
        str(Path(program_files) / "Google" / "Chrome" / "Application" / "chrome.exe")
        if program_files
        else None,
        str(Path(program_files_x86) / "Microsoft" / "Edge" / "Application" / "msedge.exe")
        if program_files_x86
        else None,
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return str(candidate)
    return None


def png_dimensions(path: Path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("Browser did not create a PNG")
    return struct.unpack(">II", data[16:24])


def make_svg(title: str, subtitle: str, points, style):
    palette = style["palette"]
    lines = wrap_title(title)
    title_svg = []
    for index, line in enumerate(lines):
        fill = palette["primary"] if index == len(lines) - 1 else palette["foreground"]
        base_size = 92 if index == len(lines) - 1 else 82
        estimated_width = max(display_width(line) * base_size, 1)
        size = max(62, min(base_size, int(base_size * 840 / estimated_width)))
        title_svg.append(
            f'<text x="132" y="{390 + index * 112}" fill="{fill}" '
            f'font-size="{size}" font-weight="900">{html.escape(line)}</text>'
        )
    point_svg = []
    for index, point in enumerate(points[:2]):
        y = 1050 + index * 224
        accent = palette["primary"] if index == 0 else palette["secondary"]
        point_svg.append(
            f'<g><rect x="90" y="{y}" width="900" height="180" rx="8" '
            f'fill="{palette["panel"]}" stroke="{accent}" stroke-width="3"/>'
            f'<rect x="90" y="{y}" width="14" height="180" rx="7" fill="{accent}"/>'
            f'<text x="150" y="{y + 76}" fill="{palette["foreground"]}" font-size="43" '
            f'font-weight="900">{html.escape(point)}</text>'
            f'<path d="M150 {y + 125} H820" stroke="{palette["line"]}" stroke-width="3"/>'
            f'<circle cx="855" cy="{y + 125}" r="9" fill="{accent}"/></g>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">
<defs><pattern id="grid" width="54" height="54" patternUnits="userSpaceOnUse"><path d="M54 0H0V54" fill="none" stroke="#17232d" stroke-width="1"/></pattern></defs>
<rect width="1080" height="1920" fill="{palette['background']}"/><rect width="1080" height="1920" fill="url(#grid)"/>
<g font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, sans-serif" letter-spacing="0">
<rect x="90" y="170" width="330" height="58" rx="8" fill="{palette['panel']}" stroke="{palette['primary']}" stroke-width="2"/>
<circle cx="122" cy="199" r="8" fill="{palette['primary']}"/><text x="150" y="210" fill="{palette['foreground']}" font-size="27" font-weight="700">视频精华 · 一眼看懂</text>
<rect x="88" y="300" width="10" height="360" rx="5" fill="{palette['primary']}"/>{''.join(title_svg)}
<text x="90" y="800" fill="{palette['muted']}" font-size="32" font-weight="700">{html.escape(subtitle)}</text>
<path d="M90 870H990" stroke="{palette['line']}" stroke-width="2"/>
<path d="M130 920H700" stroke="{palette['primary']}" stroke-width="5"/><path d="M680 897L710 920L680 943" fill="none" stroke="{palette['primary']}" stroke-width="5"/>
{''.join(point_svg)}
<path d="M90 1580H990" stroke="{palette['line']}" stroke-width="2"/><circle cx="104" cy="1642" r="9" fill="{palette['primary']}"/>
<text x="135" y="1654" fill="{palette['muted']}" font-size="29" font-weight="700">步骤、画面和口播已经完整整理</text>
</g></svg>'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True, help="Use | for explicit line breaks")
    parser.add_argument("--subtitle", required=True)
    parser.add_argument("--point", action="append", default=[])
    parser.add_argument("--style", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    style = json.loads(Path(args.style).read_text(encoding="utf-8"))
    output = Path(args.out).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    svg_path = output.with_suffix(".svg")
    svg_path.write_text(make_svg(args.title, args.subtitle, args.point, style), encoding="utf-8")

    browser = find_browser()
    if not browser:
        raise SystemExit(f"No Chrome/Edge browser found; SVG retained at {svg_path}")
    with tempfile.TemporaryDirectory(prefix="cover-render-") as profile:
        command = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw",
            f"--user-data-dir={profile}",
            "--window-size=1080,1920",
            f"--screenshot={output}",
            svg_path.as_uri(),
        ]
        subprocess.run(command, check=False, capture_output=True, timeout=60)
    if not output.is_file():
        raise SystemExit(f"Cover render failed; SVG retained at {svg_path}")
    if png_dimensions(output) != (1080, 1920):
        raise SystemExit("Cover dimensions are not 1080x1920")
    print(json.dumps({"png": output.name, "svg": svg_path.name, "size": [1080, 1920]}))


if __name__ == "__main__":
    main()
