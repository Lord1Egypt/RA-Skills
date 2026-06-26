#!/usr/bin/env python3
"""Export an HTML report to image(s) for IM / CLI / Agent use.

Usage:
    python export-image.py <report.html> [options]

Options:
    --mode      desktop | mobile | im   (default: im)
                desktop : full-page PNG, 1.5× scale
                mobile  : 750 px wide JPEG 92%, full content height
                im      : 800 px wide JPEG 92%, full content height (WeChat / IM optimised)
    --output    output file path        (default: same dir as input, auto-named)
    --all       export all three modes  (overrides --mode)
    --width     override target width in pixels

Requirements:
    pip install playwright
    playwright install chromium
"""

import argparse
import sys
from pathlib import Path
from datetime import date


# Module-level config — importable by tests
EXPORT_CONFIGS = {
    "desktop": {"viewport_w": 1440, "scale": 2.5,  "jpeg": False},
    "mobile":  {"viewport_w": 750,  "scale": 2,    "jpeg": True,  "target_w": 750},
    "im":      {"viewport_w": 800,  "scale": 2,    "jpeg": True,  "target_w": 800},
}


def parse_args():
    p = argparse.ArgumentParser(description="Export HTML report to image")
    p.add_argument("html", help="Path to the HTML report file")
    p.add_argument("--mode", choices=["desktop", "mobile", "im"], default="im",
                   help="Export mode (default: im)")
    p.add_argument("--output", help="Output file path")
    p.add_argument("--all", action="store_true", help="Export all three modes")
    p.add_argument("--width", type=int, help="Override target width in pixels")
    return p.parse_args()


def export_image(html_path: Path, mode: str, output_path: Path | None, width_override: int | None):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    html_path = html_path.resolve()
    if not html_path.exists():
        print(f"Error: file not found: {html_path}")
        sys.exit(1)

    # Determine output path
    today = date.today().strftime("%Y%m%d")
    stem = html_path.stem
    if output_path is None:
        ext = "png" if mode == "desktop" else "jpg"
        suffix = "" if mode == "desktop" else f"-{mode}"
        output_path = html_path.parent / f"{stem}_{today}{suffix}.{ext}"
    output_path = Path(output_path)

    cfg = dict(EXPORT_CONFIGS[mode])
    if width_override:
        cfg = {**cfg, "target_w": width_override, "viewport_w": width_override}

    print(f"Exporting [{mode}] → {output_path}")

    with sync_playwright() as pw:
        dpr = cfg.get("scale", 2)
        browser = pw.chromium.launch(channel="chrome")
        context = browser.new_context(
            viewport={"width": cfg["viewport_w"], "height": 900},
            device_scale_factor=dpr,
        )
        page = context.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle")

        # Hide UI chrome (TOC button, export button) — not needed in screenshots
        page.evaluate("""
            document.querySelectorAll(
                '.toc-toggle, .export-btn, .export-menu, .edit-toggle, .edit-hotzone'
            ).forEach(el => el.style.display = 'none');
        """)

        # Force all fade-in-up elements visible
        page.evaluate("""
            document.querySelectorAll('.fade-in-up').forEach(el => el.classList.add('visible'));
            document.querySelectorAll('[id^="kpi"]').forEach(el => {
                const v = el.dataset.targetValue;
                if (v !== undefined) el.textContent = (el.dataset.prefix||'') + v + (el.dataset.suffix||'');
            });
        """)
        page.wait_for_timeout(500)  # let counter animations settle

        # Get full content height
        full_height = page.evaluate("""
            Math.max(
                document.body.scrollHeight,
                document.querySelector('.report-wrapper')?.scrollHeight || 0
            )
        """)

        if mode == "desktop":
            page.set_viewport_size({"width": cfg["viewport_w"], "height": full_height})
            screenshot_opts = {
                "path": str(output_path),
                "full_page": True,
                "type": "png",
                "scale": "device",  # uses device_scale_factor=2.5 set on context
            }
        else:
            # For mobile/im: set viewport to target width, then re-measure full height
            target_w = cfg.get("target_w", 800)
            page.set_viewport_size({"width": target_w, "height": full_height})
            full_height = page.evaluate("""
                Math.max(document.body.scrollHeight,
                         document.querySelector('.report-wrapper')?.scrollHeight || 0)
            """)
            page.set_viewport_size({"width": target_w, "height": full_height})
            screenshot_opts = {
                "path": str(output_path),
                "full_page": True,
                "type": "jpeg" if cfg["jpeg"] else "png",
                "quality": 92 if cfg["jpeg"] else None,
                "scale": "device",  # uses device_scale_factor=2 set on context
            }
            if screenshot_opts.get("quality") is None:
                del screenshot_opts["quality"]

        page.screenshot(**screenshot_opts)
        browser.close()

    size_kb = output_path.stat().st_size // 1024
    print(f"  Saved: {output_path} ({size_kb} KB)")
    return output_path


def main():
    args = parse_args()
    html_path = Path(args.html)
    modes = ["desktop", "mobile", "im"] if args.all else [args.mode]

    outputs = []
    for mode in modes:
        out = Path(args.output) if (args.output and len(modes) == 1) else None
        result = export_image(html_path, mode, out, args.width)
        outputs.append(result)

    print(f"\nDone. {len(outputs)} file(s) exported.")
    for o in outputs:
        print(f"  {o}")


if __name__ == "__main__":
    main()
