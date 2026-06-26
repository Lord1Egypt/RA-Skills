#!/usr/bin/env python3
"""HTML -> PNG 高清截图转换

支持两种后端（自动检测，优先 Playwright）：
  1. Playwright (Python) -- 无需 Node.js
  2. Puppeteer (Node.js)  -- 备选

视口 1280x720，设备像素比 2x -> 输出 2560x1440 PNG

用法：
    python3 html2png.py <html_dir_or_file> [-o output_dir] [--scale 2] [--backend auto|playwright|puppeteer]
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

SCREENSHOT_SCRIPT = r"""
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
    const config = JSON.parse(process.argv[2]);
    const scale = config.scale || 2;
    const browser = await puppeteer.launch({
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu',
               '--font-render-hinting=none']
    });

    for (const item of config.files) {
        const page = await browser.newPage();
        await page.setViewport({
            width: 1280,
            height: 720,
            deviceScaleFactor: scale
        });

        await page.goto('file://' + item.html, {
            waitUntil: 'networkidle0',
            timeout: 30000
        });
        await new Promise(r => setTimeout(r, 500));

        await page.screenshot({
            path: item.png,
            type: 'png',
            fullPage: false,
            clip: { x: 0, y: 0, width: 1280, height: 720 }
        });
        console.log('PNG: ' + path.basename(item.html) + ' -> ' + path.basename(item.png));
        await page.close();
    }

    await browser.close();
    console.log('Done: ' + config.files.length + ' PNGs');
})();
"""


def _natural_key(p):
    parts = re.split(r'(\d+)', p.stem)
    return [int(x) if x.isdigit() else x.lower() for x in parts]


def _check_playwright() -> bool:
    try:
        import playwright.sync_api
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            path = p.chromium.executable_path
            if path and Path(path).exists():
                return True
            try:
                browser = p.chromium.launch(headless=True)
                browser.close()
                return True
            except Exception:
                return False
    except ImportError:
        return False
    except Exception:
        return False


def _check_puppeteer(work_dir: Path) -> bool:
    try:
        r = subprocess.run(
            ["node", "-e", "require('puppeteer')"],
            capture_output=True, text=True, timeout=10, cwd=str(work_dir)
        )
        return r.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _convert_playwright(html_files: list, output_dir: Path, scale: int) -> bool:
    from playwright.sync_api import sync_playwright

    print(f"[Playwright] Converting {len(html_files)} HTML -> PNG ({scale}x)...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=[
            '--no-sandbox', '--disable-gpu', '--font-render-hinting=none'
        ])

        for f in html_files:
            page = browser.new_page(viewport={"width": 1280, "height": 720},
                                    device_scale_factor=scale)
            page.goto(f"file://{f}", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(500)

            png_path = output_dir / (f.stem + ".png")
            page.screenshot(path=str(png_path), type="png",
                            clip={"x": 0, "y": 0, "width": 1280, "height": 720})
            print(f"  PNG: {f.name} -> {png_path.name}")
            page.close()

        browser.close()

    print(f"Done! {len(html_files)} PNGs -> {output_dir}")
    return True


def _convert_puppeteer(html_files: list, output_dir: Path, scale: int, work_dir: Path) -> bool:
    if not _check_puppeteer(work_dir):
        print("Installing puppeteer...")
        try:
            r = subprocess.run(
                ["npm", "install", "puppeteer"],
                capture_output=True, text=True, timeout=180, cwd=str(work_dir)
            )
            if r.returncode != 0:
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    config = {
        "scale": scale,
        "files": [
            {"html": str(f), "png": str(output_dir / (f.stem + ".png"))}
            for f in html_files
        ]
    }

    script_path = work_dir / ".html2png_tmp.js"
    script_path.write_text(SCREENSHOT_SCRIPT)

    try:
        print(f"[Puppeteer] Converting {len(html_files)} HTML -> PNG ({scale}x)...")
        r = subprocess.run(
            ["node", str(script_path), json.dumps(config)],
            cwd=str(work_dir), timeout=300
        )
        if r.returncode != 0:
            return False
        print(f"Done! {len(html_files)} PNGs -> {output_dir}")
        return True
    except subprocess.TimeoutExpired:
        print("Timeout: screenshot took too long", file=sys.stderr)
        return False
    finally:
        if script_path.exists():
            script_path.unlink()


def detect_backend(work_dir: Path, preferred: str = "auto") -> str:
    if preferred == "playwright":
        return "playwright" if _check_playwright() else "none"
    if preferred == "puppeteer":
        return "puppeteer" if _check_puppeteer(work_dir) else "none"

    if _check_playwright():
        return "playwright"
    if _check_puppeteer(work_dir):
        return "puppeteer"
    return "none"


def convert(html_dir: Path, output_dir: Path, scale: int = 2,
            backend: str = "auto") -> bool:
    if html_dir.is_file():
        html_files = [html_dir]
        work_dir = html_dir.parent.parent
    else:
        html_files = sorted(html_dir.glob("*.html"), key=_natural_key)
        work_dir = html_dir.parent

    if not html_files:
        print(f"No HTML files in {html_dir}", file=sys.stderr)
        return False

    output_dir.mkdir(parents=True, exist_ok=True)

    chosen = detect_backend(work_dir, backend)

    if chosen == "playwright":
        return _convert_playwright(html_files, output_dir, scale)
    elif chosen == "puppeteer":
        return _convert_puppeteer(html_files, output_dir, scale, work_dir)
    else:
        print("Error: No screenshot backend available.", file=sys.stderr)
        print("Install one of:", file=sys.stderr)
        print("  pip install playwright && playwright install chromium", file=sys.stderr)
        print("  npm install puppeteer", file=sys.stderr)
        return False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 html2png.py <html_dir_or_file> [-o output_dir] "
              "[--scale 2] [--backend auto|playwright|puppeteer]")
        sys.exit(1)

    html_path = Path(sys.argv[1]).resolve()
    output_dir = None
    scale = 2
    backend = "auto"

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "-o" and i + 1 < len(args):
            output_dir = Path(args[i + 1]).resolve()
            i += 2
        elif args[i] == "--scale" and i + 1 < len(args):
            scale = int(args[i + 1])
            i += 2
        elif args[i] == "--backend" and i + 1 < len(args):
            backend = args[i + 1]
            i += 2
        else:
            i += 1

    if output_dir is None:
        output_dir = (html_path.parent if html_path.is_file() else html_path.parent) / "png"

    success = convert(html_path, output_dir, scale, backend)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
