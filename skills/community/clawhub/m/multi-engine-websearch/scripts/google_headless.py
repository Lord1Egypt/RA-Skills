#!/usr/bin/env python3
"""
Google Search via headless Chromium (Playwright).
Renders JavaScript to extract real Google results.
Optimized for speed: minimal wait, fast exit.
"""

import json
import re
import sys
from urllib.parse import quote_plus

# Shared browser instance for reuse within same process
_browser_instance = None


def search_google_headless(query, num=10, _playwright_context=None):
    """Launch headless Chrome, perform Google search, extract results.
    If _playwright_context is passed, reuse it (for multi-search batching).
    """
    from playwright.sync_api import sync_playwright

    results = []
    own_pw = _playwright_context is None

    if own_pw:
        pw = sync_playwright().start()
        browser = pw.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions",
                "--no-first-run",
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width": 1440, "height": 900},
            locale="en-US",
        )
    else:
        pw = None
        browser = None
        context = _playwright_context

    try:
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => false});")

        # Request more results than needed
        url = f"https://www.google.com/search?q={quote_plus(query)}&num={min(num + 5, 20)}&hl=en&gl=us"

        # Use domcontentloaded instead of networkidle for speed
        page.goto(url, wait_until="domcontentloaded", timeout=12000)

        # Wait just for h3 elements to appear (faster than networkidle)
        try:
            page.wait_for_selector("a:has(h3)", timeout=5000)
        except Exception:
            # Fallback: short wait
            page.wait_for_timeout(2000)

        # Accept consent if present
        try:
            consent_btn = page.query_selector('button:has-text("Accept all")')
            if consent_btn:
                consent_btn.click()
                page.wait_for_timeout(1000)
                page.wait_for_selector("a:has(h3)", timeout=5000)
        except Exception:
            pass

        # Primary: find all <a> tags that contain an <h3>
        links_with_h3 = page.query_selector_all("a:has(h3)")
        for link in links_with_h3:
            try:
                href = link.get_attribute("href") or ""
                h3 = link.query_selector("h3")
                title = h3.inner_text().strip() if h3 else ""

                if not href.startswith("http") or not title:
                    continue
                if any(x in href for x in ["google.com", "accounts.google", "support.google", "maps.google"]):
                    continue

                snippet = ""
                try:
                    snippet_el = link.evaluate_handle(
                        """el => {
                            let c = el.parentElement;
                            for (let i = 0; i < 5 && c; i++) {
                                let s = c.querySelectorAll('div[data-sncf], div.VwiC3b, span.aCOpRe');
                                if (s.length > 0) return s[0].closest('div').textContent || '';
                                c = c.parentElement;
                            }
                            let n = el.parentElement.nextElementSibling;
                            return n ? n.textContent || '' : '';
                        }"""
                    )
                    snippet = snippet_el.json_value()
                    if isinstance(snippet, str):
                        snippet = snippet.strip()[:300]
                    else:
                        snippet = ""
                except Exception:
                    pass

                results.append({"title": title, "url": href, "snippet": snippet})
            except Exception:
                continue

        # Fallback: div.g blocks
        if not results:
            items = page.query_selector_all("div.g")
            for item in items:
                try:
                    link_el = item.query_selector("a[href^='http']")
                    title_el = item.query_selector("h3")
                    snippet_el = item.query_selector("div.VwiC3b, span.aCOpRe, div[data-sncf]")
                    if link_el and title_el:
                        href = link_el.get_attribute("href") or ""
                        title = title_el.inner_text().strip()
                        snippet = snippet_el.inner_text().strip() if snippet_el else ""
                        if href.startswith("http") and "google.com" not in href and title:
                            results.append({"title": title, "url": href, "snippet": snippet})
                except Exception:
                    continue

        page.close()
    finally:
        if own_pw:
            if browser:
                browser.close()
            if pw:
                pw.stop()

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        if r["url"] not in seen:
            seen.add(r["url"])
            unique.append(r)

    return unique[:num]


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "AI news 2026"
    results = search_google_headless(query, num=10)
    output = {"engine": "google_headless", "query": query, "total": len(results), "results": results}
    print(json.dumps(output, ensure_ascii=False, indent=2))
