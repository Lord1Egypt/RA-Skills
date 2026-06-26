#!/usr/bin/env python3
"""
Capture 1920×1080 screenshots of the skill demos for ClawHub.
Requires: pip install playwright && playwright install chromium

Run from repo root or from skills/joyyy-landings:
  python3 skills/joyyy-landings/capture_screenshots.py
  cd skills/joyyy-landings && python3 capture_screenshots.py
"""

import asyncio
import sys
from pathlib import Path

# URLs to capture (live GitHub Pages)
BASE = "https://vziatkov.github.io/neuro"
PAGES = [
    ("01_landing", f"{BASE}/landing-with-art-cards.html"),
    ("02_crash_engine", f"{BASE}/crash-engine.html"),
    ("03_crash_probability_explorer", f"{BASE}/crash-probability-explorer.html"),
    ("04_mmo_map", f"{BASE}/mmo-map.html"),
    ("05_dice_room", f"{BASE}/dice-room.html"),
]

VIEWPORT = {"width": 1920, "height": 1080}
WAIT_MS = 2500  # let canvas/animations settle


async def main():
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("❌ Install: pip install playwright && playwright install chromium")
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    out_dir = script_dir / "screenshots"
    out_dir.mkdir(exist_ok=True)

    print("📸 Capturing skill demo screenshots (1920×1080)\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport=VIEWPORT,
            device_scale_factor=1,
        )
        page = await context.new_page()

        for name, url in PAGES:
            print(f"  {name}: {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=15000)
                await asyncio.sleep(WAIT_MS / 1000)
                path = out_dir / f"{name}.png"
                await page.screenshot(path=path, type="png")
                print(f"    ✓ {path.name}")
            except Exception as e:
                print(f"    ⚠ {e}")

        await context.close()
        await browser.close()

    print(f"\n✅ Done. Screenshots in {out_dir}")


if __name__ == "__main__":
    asyncio.run(main())
