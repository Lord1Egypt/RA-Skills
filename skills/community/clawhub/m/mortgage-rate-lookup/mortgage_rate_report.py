"""
mortgage_rate_report.py — Multi-lender mortgage rate comparison

Compares 13 lenders + 2 national benchmarks.
  - 6 lenders automated via patchright stealth browser (headless)
  - 7 lenders anti-bot protected (use --headed to attempt with visible browser)
  - Freddie Mac PMMS via direct CSV API
  - Mortgage News Daily via urllib (no browser needed)

Reliability:
  - Parallel first pass (all automated lenders at once)
  - Sequential retry for any that fail (resource contention on parallel)
  - urllib fallback for MND and Freddie Mac (no browser needed)
  - 2 attempts per lender before marking as failed

Usage:
  python mortgage_rate_report.py                  # headless, automated lenders only
  python mortgage_rate_report.py --headed         # visible browser, attempts ALL 13 lenders
  python mortgage_rate_report.py --zip 90210      # override ZIP code from config.json
"""

import argparse
import asyncio
import json
import os
import re
import ssl
import urllib.request
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

ZIP_CODE = "32224"  # default, overridden by config.json or --zip


def load_zip_code(cli_zip=None):
    """Resolve ZIP code: --zip flag > config.json > default."""
    if cli_zip:
        return cli_zip
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
        zip_val = cfg.get("zip_code", "")
        if zip_val and zip_val != "YOUR_ZIP":
            return zip_val
    return "32224"
HISTORY_FILE = os.path.join(DATA_DIR, "mortgage_rates_history.json")
WAIT_MS = 10000

BENCHMARKS = {"Freddie Mac (natl avg)", "MND Index"}


# ─── RATE EXTRACTION ────────────────────────────────────────────────────────

def extract_rates(text, lender):
    """Extract rate/APR pairs from page text."""
    results = []
    for label, product in [
        (r'30[- ]?[Yy]ear(?:\s*[Ff]ixed)?', "30yr"),
        (r'15[- ]?[Yy]ear(?:\s*[Ff]ixed)?', "15yr"),
        (r'(?:7/6|7/1|5/1)\s*(?:ARM|Adj)', "ARM"),
    ]:
        m = re.search(label + r'.*?(\d\.\d{2,3})%.*?(?:APR|apr)[:\s]*(\d\.\d{2,3})%', text, re.DOTALL | re.IGNORECASE)
        if m:
            results.append({"lender": lender, "product": product, "rate": float(m.group(1)), "apr": float(m.group(2))})
            continue

        m = re.search(label + r'[\t\s]+(\d\.\d{2,3})%[\t\s]+(\d\.\d{2,3})%', text, re.IGNORECASE)
        if m:
            results.append({"lender": lender, "product": product, "rate": float(m.group(1)), "apr": float(m.group(2))})
            continue

        # Pattern 3: "label ... is X.XXX% (X.XXX% APR)"
        m = re.search(label + r'.*?is\s+(\d\.\d{2,3})%\s*\((\d\.\d{2,3})%\s*APR\)', text, re.DOTALL | re.IGNORECASE)
        if m:
            results.append({"lender": lender, "product": product, "rate": float(m.group(1)), "apr": float(m.group(2))})
            continue

        # Pattern 3b: "label ... Rate ... X.XXX% ... APR ... X.XXX%" (Mr. Cooper style)
        m = re.search(label + r'.*?Rate.*?(\d\.\d{2,3})%.*?APR.*?(\d\.\d{2,3})%', text, re.DOTALL | re.IGNORECASE)
        if m:
            results.append({"lender": lender, "product": product, "rate": float(m.group(1)), "apr": float(m.group(2))})
            continue

        m = re.search(label + r'[^\d]*?(\d\.\d{2,3})%', text, re.DOTALL | re.IGNORECASE)
        if m and 3.0 <= float(m.group(1)) <= 12.0:
            results.append({"lender": lender, "product": product, "rate": float(m.group(1)), "apr": None})
    return results


# ─── TIER 1: DIRECT APIs (no browser) ───────────────────────────────────────

def fetch_freddie_mac_csv():
    """Freddie Mac PMMS — national benchmark via free CSV endpoint."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            "https://www.freddiemac.com/pmms/docs/PMMS_history.csv",
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            lines = r.read().decode().strip().split("\n")
        last = lines[-1].split(",")
        results = []
        if len(last) >= 2 and last[1]:
            results.append({"lender": "Freddie Mac (natl avg)", "product": "30yr", "rate": float(last[1]), "apr": None})
        if len(last) >= 4 and last[3]:
            results.append({"lender": "Freddie Mac (natl avg)", "product": "15yr", "rate": float(last[3]), "apr": None})
        return results
    except Exception:
        return []


def fetch_mnd_urllib():
    """Mortgage News Daily — daily index via plain HTML (no browser needed)."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            "https://www.mortgagenewsdaily.com/mortgage-rates",
            headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            html = r.read().decode("utf-8", errors="replace")
        text = re.sub(r'<[^>]+>', ' ', html)
        return extract_rates(text, "MND Index")
    except Exception:
        return []


# ─── TIER 2: STEALTH BROWSER SCRAPING ────────────────────────────────────────

BROWSER_SOURCES = [
    ("Bank of America", "https://promotions.bankofamerica.com/homeloans/homebuying-hub/home-loan-options?subCampCode=41490&dmcode=18099675931"),
    ("Wells Fargo", "https://www.wellsfargo.com/mortgage/rates/"),
    ("Citi", "https://www.citi.com/mortgage/purchase-rates"),
    ("Navy Federal CU", "https://www.navyfederal.org/loans-cards/mortgage/mortgage-rates/"),
    ("SoFi", "https://www.sofi.com/home-loans/mortgage-rates/"),
    ("US Bank", "https://www.usbank.com/home-loans/mortgage/mortgage-rates.html"),
    ("Guaranteed Rate", "https://www.rate.com/mortgage-rates"),
    ("Truist", "https://www.truist.com/mortgage/current-mortgage-rates"),
    ("Mr. Cooper", "https://www.mrcooper.com/get-started/rates?internal_ref=rates_home"),
]

# No browser-assisted lenders remaining — all 10 are automated
BROWSER_ASSISTED = []

# Headed mode has no additional sources — everything is in BROWSER_SOURCES
HEADED_SOURCES = []


MAX_RETRIES = 3
BATCH_SIZE = 4
WAIT_SCHEDULE = [8000, 12000, 15000]  # increasing wait per attempt


async def scrape_lender(browser, name, url, wait_ms=None):
    """Scrape a single lender with stealth browser."""
    wait = wait_ms or WAIT_MS
    try:
        ctx = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-US",
        )
        page = await ctx.new_page()
        await page.goto(url, timeout=25000, wait_until="domcontentloaded")
        await page.wait_for_timeout(wait)

        # Try ZIP input if present
        for sel in ['input[name*="zip" i]', 'input[placeholder*="ZIP" i]', 'input[id*="zip" i]']:
            el = await page.query_selector(sel)
            if el:
                await el.fill(ZIP_CODE)
                await page.wait_for_timeout(500)
                for btn_sel in ['button[type="submit"]', 'button:has-text("Update")', 'button:has-text("Get")', 'button:has-text("View")']:
                    btn = await page.query_selector(btn_sel)
                    if btn:
                        await btn.click()
                        await page.wait_for_timeout(5000)
                        break
                break

        text = await page.inner_text("body")
        await ctx.close()
        return name, extract_rates(text, name)
    except Exception:
        try:
            await ctx.close()
        except Exception:
            pass
        return name, []


async def scrape_with_retries(browser, name, url):
    """Try up to MAX_RETRIES times with increasing wait."""
    for attempt in range(MAX_RETRIES):
        wait = WAIT_SCHEDULE[min(attempt, len(WAIT_SCHEDULE) - 1)]
        result_name, rates = await scrape_lender(browser, name, url, wait_ms=wait)
        if rates:
            if attempt > 0:
                print(f"  {name}: succeeded on attempt {attempt + 1}")
            return result_name, rates
    return name, []


async def scrape_all_browser(headed=False):
    """Scrape lenders in batches of 4, retry failures up to 3x with increasing wait."""
    from patchright.async_api import async_playwright

    sources = list(BROWSER_SOURCES)
    if headed:
        sources.extend(HEADED_SOURCES)

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=not headed)

        final = []
        failed = []

        # Process in batches of BATCH_SIZE
        for batch_start in range(0, len(sources), BATCH_SIZE):
            batch = sources[batch_start:batch_start + BATCH_SIZE]
            batch_names = [name for name, _ in batch]
            print(f"  Batch {batch_start // BATCH_SIZE + 1}: {', '.join(batch_names)}")

            # Parallel scrape this batch
            tasks = [scrape_lender(browser, name, url) for name, url in batch]
            results = await asyncio.gather(*tasks)

            # Sort into success / needs retry
            for (name, rates), (orig_name, orig_url) in zip(results, batch):
                if rates:
                    final.append((name, rates))
                else:
                    failed.append((orig_name, orig_url))

        # Retry all failures sequentially with increasing wait
        if failed:
            print(f"  Retrying {len(failed)} failed: {', '.join(n for n, _ in failed)}")
            for name, url in failed:
                result_name, rates = await scrape_with_retries(browser, name, url)
                final.append((result_name, rates))

        await browser.close()
    return final


# ─── HISTORY ─────────────────────────────────────────────────────────────────

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return []


def save_history(history):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


# ─── REPORT FORMATTING ──────────────────────────────────────────────────────

def format_report(unique, successes, failures, history):
    """Build the formatted rate comparison report."""
    last_rates = history[-1].get("rates", {}) if history else {}

    total_lenders = len(BROWSER_SOURCES)  # 10 automated lenders
    reporting = len(set(r["lender"] for r in unique if r["lender"] not in BENCHMARKS))

    today = datetime.now().strftime("%b %d, %Y")
    lines = [
        f"MORTGAGE RATE COMPARISON \u2014 {today}",
        f"   {total_lenders} lenders tracked + 2 benchmarks | {reporting} reporting now",
        "",
    ]

    for product in ["30yr", "15yr", "ARM", "FHA 30yr", "VA 30yr"]:
        product_rates = sorted(
            [r for r in unique if r["product"] == product],
            key=lambda r: r["rate"]
        )
        if not product_rates:
            continue

        label = {
            "30yr": "30-YEAR FIXED", "15yr": "15-YEAR FIXED", "ARM": "ARM",
            "FHA 30yr": "FHA 30-YEAR", "VA 30yr": "VA 30-YEAR",
        }.get(product, product)
        lines.append(f"--- {label} " + "-" * (48 - len(label)))
        lines.append("")

        for i, r in enumerate(product_rates):
            rate_str = f"{r['rate']:.3f}%"
            apr_str = f"  ({r['apr']:.3f}% APR)" if r.get("apr") else ""
            is_benchmark = r["lender"] in BENCHMARKS
            benchmark_tag = "  \u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7\u00B7 benchmark" if is_benchmark else ""

            # Best = first non-benchmark lender
            is_best = (i == 0 and len(product_rates) > 1 and not is_benchmark)
            if not is_best and i > 0:
                # Check if this is the first non-benchmark
                prior_non_bench = [r2 for r2 in product_rates[:i] if r2["lender"] not in BENCHMARKS]
                if not prior_non_bench and not is_benchmark:
                    is_best = True

            if is_best:
                lines.append(f"  >>> {r['lender']:28s} {rate_str}{apr_str}{'':>20s} BEST")
            else:
                lines.append(f"     {r['lender']:28s} {rate_str}{apr_str}{benchmark_tag}")

        # Day-over-day
        prev = last_rates.get(product, [])
        if prev and product_rates:
            curr_avg = sum(r["rate"] for r in product_rates) / len(product_rates)
            prev_avg = sum(r["rate"] for r in prev) / len(prev)
            diff = curr_avg - prev_avg
            avg_str = f"{curr_avg:.3f}%"
            if abs(diff) >= 0.005:
                arrow = "^" if diff > 0 else "v"
                lines.append("")
                lines.append(f"  Avg: {avg_str}  |  vs yesterday: {arrow} {abs(diff):.3f}%")
            else:
                lines.append("")
                lines.append(f"  Avg: {avg_str}  |  vs yesterday: unchanged")

        lines.append("")

    # Browser-assisted lenders (only show if not already attempted)
    attempted = set(successes + failures)
    needs_browser = [l for l in BROWSER_ASSISTED if l not in attempted]
    script_failures = [f for f in failures if f not in ("Freddie Mac", "MND") and f not in BROWSER_ASSISTED]
    needs_browser.extend(script_failures)
    if needs_browser:
        lines.append(f"Need browser check: {', '.join(needs_browser)}")

    return "\n".join(lines)


# ─── OPENCLAW BROWSER FALLBACK (CDP) ─────────────────────────────────────────

async def scrape_chase_via_cdp(zip_code):
    """
    Fallback: connect to the running OpenClaw browser via CDP (port 18800)
    and extract Chase rates directly via JavaScript — bypasses anti-bot.
    """
    try:
        from patchright.async_api import async_playwright
        async with async_playwright() as pw:
            browser = await pw.chromium.connect_over_cdp("http://127.0.0.1:18800")
            context = browser.contexts[0] if browser.contexts else await browser.new_context()
            page = await context.new_page()

            await page.goto(
                "https://www.chase.com/personal/mortgage/mortgage-rates",
                timeout=20000, wait_until="domcontentloaded"
            )
            await page.wait_for_timeout(3000)

            # Fill ZIP and submit
            try:
                zip_input = await page.query_selector("input[placeholder*='zip' i], input[id*='zip' i]")
                if zip_input:
                    await zip_input.triple_click()
                    await zip_input.type(zip_code)
                    await page.wait_for_timeout(500)
                    btn = await page.query_selector("button:has-text('See rates'), button[type='submit']")
                    if btn:
                        await btn.click()
                        await page.wait_for_timeout(5000)
            except Exception:
                pass

            # Wait for rate table to load (Chase renders it async)
            try:
                await page.wait_for_function(
                    "() => { const t = document.querySelector('table'); return t && t.innerText.includes('%'); }",
                    timeout=10000
                )
            except Exception:
                pass

            # Extract rate table directly from DOM
            table_text = await page.evaluate("""() => {
                const el = document.querySelector('table') ||
                           document.querySelector('[class*="rate"]') ||
                           document.querySelector('[data-testid*="rate"]');
                return el ? el.innerText : '';
            }""")

            await page.close()

            if table_text and "%" in table_text:
                return extract_rates(table_text, "Chase")
    except Exception as e:
        pass
    return []


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Multi-lender mortgage rate comparison")
    parser.add_argument("--headed", action="store_true",
                        help="Run visible browser to attempt all 13 lenders (bypasses anti-bot on some sites)")
    parser.add_argument("--zip", type=str, default=None,
                        help="ZIP code for rate lookup (overrides config.json)")
    args = parser.parse_args()

    global ZIP_CODE
    ZIP_CODE = load_zip_code(args.zip)

    browser_count = len(BROWSER_SOURCES) + (len(HEADED_SOURCES) if args.headed else 0)
    total = browser_count + 2  # + Freddie Mac + MND
    mode = "headed (visible browser)" if args.headed else "headless"
    print(f"Scraping {total} sources in {mode} mode...\n")

    all_rates = []
    successes = []
    failures = []

    # Tier 1: Direct APIs (no browser, instant)
    fm_rates = fetch_freddie_mac_csv()
    if fm_rates:
        all_rates.extend(fm_rates)
        successes.append("Freddie Mac")
    else:
        failures.append("Freddie Mac")

    mnd_rates = fetch_mnd_urllib()
    if mnd_rates:
        all_rates.extend(mnd_rates)
        successes.append("MND")
    else:
        failures.append("MND")

    # Tier 2: Browser scraping (parallel + sequential retry)
    browser_results = asyncio.run(scrape_all_browser(headed=args.headed))

    for name, rates in browser_results:
        if rates:
            all_rates.extend(rates)
            successes.append(name)
        else:
            failures.append(name)


    if not all_rates:
        print("No rates fetched from any source.")
        return

    # Deduplicate
    seen = set()
    unique = []
    for r in all_rates:
        key = (r["lender"], r["product"])
        if key not in seen:
            seen.add(key)
            unique.append(r)

    # History
    history = load_history()

    # Format and print
    report = format_report(unique, successes, failures, history)
    print(report)

    # Save history
    today_key = datetime.now().strftime("%Y-%m-%d")
    rates_by_product = {}
    for product in ["30yr", "15yr", "ARM", "FHA 30yr", "VA 30yr"]:
        pr = [r for r in unique if r["product"] == product]
        if pr:
            rates_by_product[product] = [
                {"lender": r["lender"], "rate": r["rate"], "apr": r.get("apr")}
                for r in pr
            ]

    if history and history[-1].get("date") == today_key:
        history[-1]["rates"] = rates_by_product
    else:
        history.append({"date": today_key, "rates": rates_by_product})

    history = history[-90:]
    save_history(history)


if __name__ == "__main__":
    main()
