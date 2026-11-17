#!/usr/bin/env python3
"""
Taste Menu Monitor — scrapes restaurant menus, compares against last snapshot,
and reports new dishes.

Outputs report between __REPORT_START__ and __REPORT_END__ markers to stdout.
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Monitor restaurant menus for changes relevant to taste signals.')
    print("Usage: taste_menu_monitor.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)

import json
import os
import re
import subprocess
import sys
import time
import tempfile
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

_PROF = os.environ.get("HERMES_HOME",
                       os.path.join(os.path.expanduser("~"), ".hermes", "profiles", "indigo"))

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 taste_menu_monitor.py")
    sys.exit(0)


DATA_DIR = Path(_PROF) / "commons" / "data" / "ocas-taste"
SNAPSHOTS_DIR = DATA_DIR / "menu_snapshots"
REPORTS_DIR = DATA_DIR / "menu_reports"
CONFIG_FILE = DATA_DIR / "menu_monitor.json"


def load_json(path):
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2, default=str)

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def snapshot_filename():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return SNAPSHOTS_DIR / f"snapshot_{ts}.json"

def report_filename():
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return REPORTS_DIR / f"report_{ts}.json"

def fetch_url(url, timeout=20):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()

def fetch_text(url, timeout=20):
    return fetch_url(url, timeout).decode("utf-8", errors="replace")

def extract_pdfs(html, base_url, pdf_pattern_str):
    m = re.search(r'https?://[^/]+', base_url)
    base = m.group(0) if m else base_url
    pdf_pattern = re.compile(pdf_pattern_str) if pdf_pattern_str else re.compile(r"\.pdf")
    raw = re.findall(r'href=["\']([^"\']*\.pdf[^"\']*)["\']', html, re.IGNORECASE)
    resolved = []
    for href in raw:
        if href.startswith("http"):
            resolved.append(href)
        elif href.startswith("/"):
            resolved.append(base + href)
        else:
            resolved.append(base + "/" + href)
    matched = list(dict.fromkeys(resolved))
    return [p for p in matched if pdf_pattern.search(p)]

def pdf_to_text(pdf_bytes):
    """Extract text from PDF bytes using pdftotext."""
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(pdf_bytes)
        tmp_path = tmp.name
    try:
        result = subprocess.run(
            ["pdftotext", "-layout", tmp_path, "-"],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout
    finally:
        os.unlink(tmp_path)

def extract_dishes_from_text(text, cfg):
    noise_re = [re.compile(p, re.IGNORECASE) for p in cfg["noise_patterns"]]
    food_kws = [kw.lower() for kw in cfg["food_keywords"]]
    min_len = cfg["min_length"]
    max_len = cfg["max_length"]

    dishes = []
    seen = set()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        line = line.strip("|•-–—·\t ")
        if len(line) < min_len or len(line) > max_len:
            continue
        if any(p.search(line) for p in noise_re):
            continue
        lower = line.lower()
        if not any(kw in lower for kw in food_kws):
            continue
        key = re.sub(r'\s+', ' ', lower).strip()
        if key not in seen:
            seen.add(key)
            dishes.append(line)
    return dishes

def scrape_pdf_page(restaurant, cfg):
    url = restaurant["url"]
    pdf_pattern_str = restaurant.get("pdf_pattern", r"/s/[^'\"\s]+\.pdf")
    exclude = [re.compile(p, re.IGNORECASE) for p in (restaurant.get("exclude_pdf_patterns") or [])]
    pdf_filter = [p.upper() for p in (restaurant.get("pdf_filter") or [])]

    html = fetch_text(url)
    matched = extract_pdfs(html, url, pdf_pattern_str)

    if pdf_filter:
        matched = [p for p in matched if any(f in p.upper() for f in pdf_filter)]
    matched = [p for p in matched if not any(e.search(p) for e in exclude)]

    if not matched:
        return {"status": "no_pdfs", "pdf_count": 0, "pdf_errors": 0, "dishes": [], "pdfs": []}

    dishes = []
    errors = 0
    fetched_pdfs = []
    for pdf_url in matched[:3]:
        fetched_pdfs.append(pdf_url)
        try:
            raw = fetch_url(pdf_url)
            text = pdf_to_text(raw)
            d = extract_dishes_from_text(text, cfg["dish_extraction"])
            dishes.extend(d)
        except Exception as e:
            errors += 1
            print(f"    PDF error: {e}", file=sys.stderr)

    seen = set()
    unique = []
    for d in dishes:
        k = d.lower().strip()
        if k not in seen:
            seen.add(k)
            unique.append(d)

    return {
        "status": "ok" if not errors else "partial",
        "pdf_count": len(matched),
        "pdf_errors": errors,
        "dishes": unique,
        "pdfs": fetched_pdfs,
    }

def scrape_dom(restaurant, cfg):
    url = restaurant["url"]
    try:
        html = fetch_text(url)
        # Remove script/style blocks
        html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove JSON-LD and other data blocks
        html = re.sub(r'<[^>]*type="application/ld\+json"[^>]*>.*?</[^>]*>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
        # Strip all tags
        text = re.sub(r'<[^>]+>', '\n', html)
        text = re.sub(r'&[a-z]+;', ' ', text)
        # Remove lines that look like JSON/JS
        lines = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            # skip lines that are clearly JSON/JS fragments
            if re.match(r'^["\'\[\{]', line):
                continue
            if re.match(r'^[a-zA-Z_]+:', line):
                continue
            if re.search(r'[{}();=]', line) and len(line) > 20:
                continue
            lines.append(line)
        text = '\n'.join(lines)
        dishes = extract_dishes_from_text(text, cfg["dish_extraction"])
        return {"status": "ok", "pdf_count": 0, "pdf_errors": 0, "dishes": dishes, "pdfs": []}
    except Exception as e:
        return {"status": "error", "pdf_count": 0, "pdf_errors": 1, "dishes": [], "pdfs": [], "error": str(e)}

def scrape(restaurant, cfg):
    stype = restaurant.get("scrape_type", "pdf_page")
    if stype == "pdf_page":
        return scrape_pdf_page(restaurant, cfg)
    elif stype == "dom":
        return scrape_dom(restaurant, cfg)
    else:
        return {"status": "unknown_type", "dishes": []}


def main():
    config = load_json(CONFIG_FILE)
    restaurants = [r for r in config["restaurants"] if r.get("enabled", True)]

    snapshots = sorted(SNAPSHOTS_DIR.glob("snapshot_*.json"))
    prev_dishes = {}
    if snapshots:
        prev_snapshot = load_json(snapshots[-1])
        for key, data in prev_snapshot.get("restaurants", {}).items():
            prev_dishes[key] = set(d.lower().strip() for d in data.get("dishes", []))

    new_snapshot = {
        "timestamp": now_iso(),
        "restaurants": {}
    }
    changes = []

    for r in restaurants:
        name = r["name"]
        loc = r.get("location")
        key = f"{name} ({loc})" if loc else name
        print(f"  Scraping {key}...", file=sys.stderr)
        try:
            result = scrape(r, config)
        except Exception as e:
            result = {"status": "error", "pdf_count": 0, "pdf_errors": 1, "dishes": [], "pdfs": [], "error": str(e)}
        new_snapshot["restaurants"][key] = result
        print(f"    -> {result['status']}, {len(result.get('dishes',[]))} dishes", file=sys.stderr)

        new_set = set(d.lower().strip() for d in result.get("dishes", []))
        old_set = prev_dishes.get(key, set())
        new_only = new_set - old_set

        if new_only:
            new_dishes = [d for d in result["dishes"] if d.lower().strip() in new_only]
            removed_dishes = sorted(old_set - new_set)
            changes.append({
                "restaurant": key,
                "new_dishes": new_dishes,
                "removed_dishes": removed_dishes,
                "current_count": len(new_set),
                "previous_count": len(old_set),
            })

        time.sleep(1)

    snap_path = snapshot_filename()
    save_json(snap_path, new_snapshot)
    print(f"  Snapshot saved: {snap_path}", file=sys.stderr)

    report = {
        "timestamp": now_iso(),
        "changes": changes,
    }
    rep_path = report_filename()
    save_json(rep_path, report)
    print(f"  Report saved: {rep_path}", file=sys.stderr)

    if changes:
        lines = []
        for c in changes:
            lines.append(f"**{c['restaurant']}**")
            for d in c["new_dishes"]:
                lines.append(f"• {d}")
            lines.append("")
        report_text = "\n".join(lines).strip()
        print(f"__REPORT_START__\n{report_text}\n__REPORT_END__")
    else:
        print("__NO_CHANGES__", file=sys.stderr)


if __name__ == "__main__":
    main()