#!/usr/bin/env python3
"""
capture_url.py — take a full-page screenshot of a URL

Usage:
  python capture_url.py --url "https://example.com"

Output:
  Prints the absolute path to the saved screenshot file.

Requirements (install once):
  pip install playwright && python -m playwright install chromium
"""

import argparse
import os
import sys
from datetime import datetime

IMAGES_DIR = os.path.expanduser("~/.multimodal-memory/images")


def capture_with_playwright(url: str, output_path: str):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=30000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()


def capture_with_chrome_headless(url: str, output_path: str):
    import subprocess

    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "chromium-browser",
        "google-chrome",
        "chromium",
    ]
    chrome = next((c for c in candidates if os.path.isfile(c) or _which(c)), None)
    if not chrome:
        raise FileNotFoundError("Chrome/Chromium not found.")

    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--screenshot={output_path}",
            "--window-size=1440,900",
            url,
        ],
        check=True,
        capture_output=True,
    )


def _which(cmd: str) -> bool:
    import shutil
    return shutil.which(cmd) is not None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    os.makedirs(IMAGES_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Sanitise URL for use in filename
    safe = args.url.replace("https://", "").replace("http://", "").replace("/", "_")[:60]
    filename = f"website_{safe}_{timestamp}.png"
    output_path = os.path.join(IMAGES_DIR, filename)

    # Try playwright first, fall back to Chrome headless
    try:
        capture_with_playwright(args.url, output_path)
    except ImportError:
        try:
            capture_with_chrome_headless(args.url, output_path)
        except Exception as e:
            print(
                f"ERROR: Could not take screenshot. "
                f"Install playwright: pip install playwright && python -m playwright install chromium\n"
                f"Details: {e}",
                file=sys.stderr,
            )
            sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(output_path)


if __name__ == "__main__":
    main()
