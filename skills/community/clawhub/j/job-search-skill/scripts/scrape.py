#!/usr/bin/env python3
"""
scrape.py v3 — Job scraper for:
  1. LinkedIn  — public guest API (jobs-guest/seeMoreJobPostings)
  2. Infostud  — Next.js __NEXT_DATA__ from /oglasi-za-posao-{keyword}
  3. HelloWorld.rs — listing pages (title, company, location, tags, seniority)

All three sources are HEAVILY filtered and scored with the resume in mind, not bulk-collected.
Output: data/raw_jobs.json (unseen jobs only)
"""

import json
import sqlite3
import time
import hashlib
import re
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "workspace" / "config.json"
OUTPUT_PATH = BASE_DIR / "data" / "raw_jobs.json"
DB_PATH = BASE_DIR / "data" / "seen_jobs.db"

BROWSER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def log(msg): print(msg, flush=True)


def fetch_html(url, timeout=15):
    req = urllib.request.Request(url, headers=BROWSER_HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS seen_jobs (
            job_id TEXT PRIMARY KEY, seen_at TEXT
        )
    """)
    conn.commit()
    return conn


def get_id(url):
    return hashlib.md5(url.encode()).hexdigest()


# =========================================================================
# RESUME-KEYWORD-BASED FILTER — keeps ONLY jobs that match the resume
# =========================================================================

RESUME_KEYWORDS = [
    "c#", ".net", "azure", "sql", "fintech",
    "application support", "technical support",
    "senior", "lead", "technical lead",
]

def is_relevant_for_resume(title, tags=None):
    """Quick pre-filter: does the job even touch the resume's domain?"""
    t = title.lower()
    tag_text = " ".join(t.lower() for t in (tags or []))
    combined = f"{t} {tag_text}"

    # MUST have at least one of these core matches
    core_hits = 0
    for kw in [".net", "c#", "azure", "senior", "lead", "support"]:
        if kw in combined:
            core_hits += 1

    return core_hits >= 1


# =========================================================================
# LinkedIn
# =========================================================================

LINKEDIN_QUERIES = [
    ("software engineer", "Serbia"),
    (".net developer", "Serbia"),
    ("senior software engineer", "Serbia"),
    ("technical lead", "Serbia"),
    ("c# developer", "Serbia"),
    ("azure developer", "Serbia"),
    ("application support", "Serbia"),
    ("fintech", "Serbia"),
]


def scrape_linkedin():
    all_jobs = []

    for keywords, location in LINKEDIN_QUERIES:
        q = f"{keywords} {location}".strip()
        try:
            params = urllib.parse.urlencode({
                "keywords": q, "location": location,
                "f_TPR": "r86400", "start": 0
            })
            url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?{params}"
            html = fetch_html(url, timeout=15)

            cards = re.findall(
                r'<div class="base-card[^>]*data-entity-urn="urn:li:jobPosting:(\d+)"[^>]*>'
                r'(.*?)</div>\s*</li>',
                html, re.DOTALL,
            )
            for jid, card_html in cards:
                title_m = re.search(r'<h3[^>]*>(.*?)</h3>', card_html, re.DOTALL)
                title = re.sub(r"<[^>]+>", "", title_m.group(1)).strip() if title_m else q

                if not is_relevant_for_resume(title):
                    continue

                comp_m = re.search(
                    r'class="[^"]*base-search-card__subtitle[^"]*"[^>]*>(.*?)</a>',
                    card_html, re.DOTALL,
                )
                company = re.sub(r"<[^>]+>", "", comp_m.group(1)).strip() if comp_m else ""

                loc_m = re.search(r'class="[^"]*base-search-card__metadata[^"]*"[^>]*>\s*<span[^>]*>(.*?)</span>',
                                  card_html, re.DOTALL)
                loc = loc_m.group(1).strip() if loc_m else location

                link_m = re.search(r'href="(https://[^"]+)"', card_html)
                url_final = link_m.group(1).split("?")[0] if link_m else ""
                if not url_final or "jobs/view/" not in url_final:
                    continue

                date_m = re.search(r'datetime="([^"]+)"', card_html)
                posted = date_m.group(1) if date_m else ""

                all_jobs.append({
                    "id": get_id(url_final),
                    "title": title,
                    "company": company,
                    "location": loc,
                    "url": url_final,
                    "source": "LinkedIn",
                    "description": "",
                    "tags": [],
                    "posted": posted,
                })
        except Exception as e:
            log(f"  [LinkedIn] error '{keywords}': {e}")

        time.sleep(1.5)

    log(f"  [LinkedIn] {len(all_jobs)} relevant jobs")
    return all_jobs


# =========================================================================
# Infostud — best source, rich structured data
# =========================================================================

INFOSTUD_QUERIES = [
    ".net", "software-engineer", "senior-software-engineer",
    "azure", "c#", "application-support",
    "senior-.net-developer", "fintech",
    "lead-software-engineer", "technical-lead",
]


def scrape_infostud():
    all_jobs = []

    for query in INFOSTUD_QUERIES:
        url = f"https://poslovi.infostud.com/oglasi-za-posao-{query}"
        try:
            html = fetch_html(url, timeout=15)
        except urllib.error.HTTPError:
            alt = f"https://poslovi.infostud.com/search?q={urllib.parse.quote(query)}"
            try:
                html = fetch_html(alt, timeout=15)
            except Exception:
                continue
        except Exception:
            continue

        match = re.search(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
        if not match:
            continue

        try:
            data = json.loads(match.group(1))
            primary = (data.get("props", {}).get("pageProps", {})
                       .get("initialSearchResults", {}).get("jobs", {})
                       .get("primary", []))
        except (KeyError, json.JSONDecodeError):
            continue

        for j in primary:
            url_job = j.get("url", "") or ""
            if url_job and not url_job.startswith("http"):
                url_job = f"https://poslovi.infostud.com{url_job}" if url_job.startswith("/") else url_job

            title = j.get("title", "")
            if not is_relevant_for_resume(title, j.get("itTags", [])):
                continue

            location_raw = j.get("location", {})
            city = (location_raw.get("city", "") if isinstance(location_raw, dict)
                    else str(location_raw) if location_raw else "")
            if not city:
                city = j.get("cityNames", "") or ""

            if j.get("workFromHome"):
                loc_str = f"{city} | Remote" if city else "Remote"
            elif j.get("hybridWork"):
                loc_str = f"{city} | Hybrid" if city else "Hybrid"
            else:
                loc_str = city or "Serbia"

            summary = (j.get("jobSummary") or {}).get("summary") or ""

            all_jobs.append({
                "id": get_id(url_job),
                "title": title,
                "company": j.get("companyName", ""),
                "location": loc_str,
                "url": url_job,
                "source": "Infostud",
                "description": summary,
                "tags": j.get("itTags", []),
                "posted": j.get("onlineViewDate", ""),
            })

        time.sleep(0.8)

    log(f"  [Infostud] {len(all_jobs)} relevant jobs")
    return all_jobs


# =========================================================================
# HelloWorld.rs — listing pages only, no detail page per-job
# =========================================================================

HW_PAGES = [
    ("Programming", "/oglasi-za-posao/programiranje"),
    ("Support", "/oglasi-za-posao/podrska"),
    ("AI/ML", "/oglasi-za-posao/aiml"),
    ("Systems", "/oglasi-za-posao/sistemska-administracija"),
    ("Management", "/oglasi-za-posao/menadzment"),
]

HW_SEARCH_KWS = [".net", "c%23", "azure", "senior", "application+support", "fintech"]


def scrape_helloworld():
    """Scrape HelloWorld listing pages. Title + company + tags from list view only."""
    all_cards = []
    seen_ids = set()
    company_cache = {}
    location_cache = {}
    tags_cache = {}
    seniority_cache = {}
    date_cache = {}

    for cat_name, cat_path in HW_PAGES + [(f"search {kw}", f"/oglasi-za-posao/?keyword={kw}")
                                           for kw in HW_SEARCH_KWS]:
        url = f"https://www.helloworld.rs{cat_path}"
        try:
            html = fetch_html(url, timeout=15)
        except Exception:
            continue

        # Pull all job cards with their HTML context
        blocks = re.findall(
            r'<h3><a data-job-id="(\d+)" href="(/posao/[^"]+)"[^>]*class="__ga4_job_title[^"]*"[^>]*>([^<]+)</a></h3>(.*?)(?=<h3><a data-job-id=|\Z)',
            html, re.DOTALL,
        )

        for jid, href, title, remainder in blocks:
            title = title.strip()
            if not is_relevant_for_resume(title):
                continue
            if jid in seen_ids:
                continue
            seen_ids.add(jid)

            # Company — note: href= sometimes lacks quotes in raw HTML
            comp_m = re.search(r'__ga4_job_company[^>]*>\s*([^<]+)\s*</a>', remainder)
            company = comp_m.group(1).strip() if comp_m else ""

            # Location
            loc_m = re.search(r'<i class="las la-map-marker[^>]*></i>\s*<p[^>]*>([^<]+)</p>', remainder)
            location = loc_m.group(1).strip() if loc_m else ""

            # Date
            date_m = re.search(r'<i class="las la-clock[^>]*></i>\s*<p[^>]*>([^<]+)</p>', remainder)
            date = date_m.group(1).strip() if date_m else ""

            # Tags
            tags = re.findall(
                r'__ga4_job_tech_tag[^>]*>\s*([^<]+)\s*</a>', remainder
            )
            tags = [re.sub(r'\s+', ' ', t).strip() for t in tags if t.strip()]

            # Seniority
            seniority = re.findall(
                r'__quick_senioritet[^>]*>\s*([^<]+)\s*</button>', remainder
            )

            seniority = [re.sub(r'\s+', ' ', s).strip() for s in seniority if s.strip()]
            # Clean query params from href
            href_clean = href.split('?')[0]
            job_url = f"https://www.helloworld.rs{href_clean}"

            all_cards.append({
                "id": get_id(f"hw://{jid}"),
                "title": title,
                "company": company,
                "location": location,
                "url": job_url,
                "source": "HelloWorld",
                "description": "",
                "tags": tags + seniority,
                "posted": date,
            })

        time.sleep(1)

    log(f"  [HelloWorld] {len(all_cards)} relevant jobs")
    return all_cards


# =========================================================================
# Main
# =========================================================================


def main():
    log("=== Job Scraper v3 (LinkedIn + Infostud + HelloWorld.rs) ===")
    log("Filtering by resume relevance during scrape.")

    conn = init_db()
    all_jobs = []

    log("\n--- LinkedIn ---")
    all_jobs.extend(scrape_linkedin())

    log("\n--- Infostud ---")
    all_jobs.extend(scrape_infostud())

    log("\n--- HelloWorld.rs ---")
    all_jobs.extend(scrape_helloworld())

    # Deduplicate by URL
    seen_urls = set()
    unique = []
    for job in all_jobs:
        if job["url"] and job["url"] not in seen_urls:
            seen_urls.add(job["url"])
            unique.append(job)

    # Filter out previously sent
    new_jobs = []
    for job in unique:
        jid = job["id"]
        if not conn.execute("SELECT 1 FROM seen_jobs WHERE job_id = ?", (jid,)).fetchone():
            new_jobs.append(job)
            conn.execute("INSERT OR IGNORE INTO seen_jobs (job_id, seen_at) VALUES (?, ?)",
                         (jid, datetime.utcnow().isoformat()))
            conn.commit()

    log(f"\nTotal unique: {len(unique)} | New (unseen): {len(new_jobs)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(new_jobs, f, indent=2, ensure_ascii=False)

    log(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
