#!/usr/bin/env python3
# Oasis-Blueprints · https://github.com/oasiseng/Oasis-Blueprints · MIT License, Copyright (c) 2026 Oasis Engineering, LLC
"""print.py - HTML sheet set to PDF with headless Chromium, plus the layout audit.

    python print.py sheet-set.html sheet-set.pdf [--png preview-]

Exits 2 when the audit finds anything (overflow, wrong scale, open items on an issued set), so a set
with problems is not issued by accident. --png also writes one image per sheet for a visual check.

Needs Playwright and Chromium to be installed already. This script installs and downloads nothing.
Without it, open the HTML in Chrome or Edge and use the Print / Save as PDF button: the page is
already set to 36 x 24 in, and the audit result shows at the top left of the screen.
"""
import argparse, sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="Print an HTML sheet set to PDF and run the layout audit.")
    ap.add_argument("html"), ap.add_argument("pdf"), ap.add_argument("--png", help="prefix for one preview image per sheet")
    a = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("Playwright is not installed, so this script cannot make the PDF or run the layout check here.\n"
                 "Open the HTML in Chrome or Edge instead: the badge at the top left shows the layout check, and\n"
                 "Print / Save as PDF makes the 36 x 24 in PDF.")
    with sync_playwright() as pw:
        try:
            browser = pw.chromium.launch()
        except Exception as e:
            sys.exit("Could not start Chromium (%s).\nOpen the HTML in Chrome or Edge and use Print / Save as PDF instead." % str(e).splitlines()[0])
        page = browser.new_page(viewport={"width": 3600, "height": 2500})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(Path(a.html).resolve().as_uri())
        try:
            page.wait_for_function("window.__ready === true", timeout=30000)
        except Exception:
            print("The page did not finish drawing. Script errors:\n - " + "\n - ".join(errors or ["none reported"]))
            browser.close()
            sys.exit(3)
        errors += page.evaluate("window.__errors || []")
        audit = page.evaluate("window.__audit") or []
        scales = page.evaluate("""() => [...document.querySelectorAll('svg.sk:not(.iso)')].map(s => {
            const t = s.closest('.panel').querySelector('.vn').textContent, den = +s.dataset.den;
            return t + ': 1/' + den + ' stated, 1/' + (1 / (s.getScreenCTM().a / 96 * UPI)).toFixed(2) + ' drawn'; })""")
        print("views: " + "; ".join(scales))
        if errors:
            print("SCRIPT ERRORS:\n - " + "\n - ".join(errors))
        print("LAYOUT AUDIT:\n - " + "\n - ".join(audit) if audit else "layout audit: clean")
        page.pdf(path=a.pdf, width="36in", height="24in", print_background=True, prefer_css_page_size=True)
        print("wrote " + a.pdf)
        if a.png:
            page.add_style_tag(content="#ui,#audit{display:none!important} #set{zoom:1!important}")
            for i, sh in enumerate(page.query_selector_all(".sheet")):
                sh.screenshot(path="%s%d.png" % (a.png, i))
        browser.close()
        sys.exit(2 if (audit or errors) else 0)


if __name__ == "__main__":
    main()
