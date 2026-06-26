#!/usr/bin/env python3
"""
LinkedIn Job Scraper - searches LinkedIn public API for jobs.
No login required. Configure search queries in config.json.
"""
import urllib.request
import urllib.parse
import re
import html as html_mod
import json
import sqlite3
import time
import hashlib
from datetime import datetime
from pathlib import Path


CONFIG_PATH = Path(__file__).parent / "config.json"
DB_PATH = Path(__file__).parent / "jobs.db"

SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def init_db(db_path=None):
    """Create jobs table if not exists."""
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT, company TEXT, location TEXT,
            url TEXT, career_url TEXT,
            description TEXT, requirements TEXT,
            required_years INTEGER,
            published_date TEXT,
            found_date TEXT DEFAULT (datetime('now')),
            status TEXT DEFAULT 'new'
        )
    """)
    conn.commit()
    return conn


def extract_years(text):
    """Extract required years of experience from text."""
    patterns = [
        r'(\d+)\+?\s*(?:years?|שנ)',
        r'(\d+)-(\d+)\s*(?:years?|שנ)',
    ]
    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            return int(m.group(1))
    return 0


def search_jobs(query, location="Israel", start=0):
    """Search LinkedIn for jobs."""
    params = urllib.parse.urlencode({
        "keywords": query,
        "location": location,
        "start": start,
        "f_TPR": "r604800",  # past week
    })
    url = f"{SEARCH_URL}?{params}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Search error: {e}")
        return ""


def parse_job_cards(html_text):
    """Parse job cards from LinkedIn HTML response."""
    jobs = []
    cards = re.findall(r'<li[^>]*>.*?</li>', html_text, re.DOTALL)

    for card in cards:
        title_m = re.search(r'class="base-search-card__title[^"]*"[^>]*>(.*?)</\w+>', card, re.DOTALL)
        company_m = re.search(r'class="base-search-card__subtitle[^"]*"[^>]*>(.*?)</\w+>', card, re.DOTALL)
        location_m = re.search(r'class="job-search-card__location[^"]*"[^>]*>(.*?)</\w+>', card, re.DOTALL)
        link_m = re.search(r'href="(https://\w+\.linkedin\.com/jobs/view/[^"?]+)', card)

        if not title_m:
            continue

        title = html_mod.unescape(title_m.group(1).strip())
        company = html_mod.unescape(company_m.group(1).strip()) if company_m else "Unknown"
        location = html_mod.unescape(location_m.group(1).strip()) if location_m else "Unknown"
        url = link_m.group(1) if link_m else ""

        job_id_m = re.search(r'/view/(\d+)', url)
        job_id = job_id_m.group(1) if job_id_m else hashlib.md5(f"{title}{company}".encode()).hexdigest()[:12]

        jobs.append({
            "job_id": job_id,
            "title": title,
            "company": company,
            "location": location,
            "url": url,
        })

    return jobs


def scrape_and_store():
    """Run full scrape cycle."""
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    candidate = config.get("candidate", {})
    queries = candidate.get("search_queries", candidate.get("target_titles", []))
    location = candidate.get("search_location", "Israel")

    conn = init_db()
    new_count = 0

    for query in queries:
        print(f"Searching: {query}...")
        html = search_jobs(query, location)
        jobs = parse_job_cards(html)
        print(f"  Found {len(jobs)} cards")

        for job in jobs:
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO jobs (job_id, title, company, location, url, description, requirements, required_years)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (job["job_id"], job["title"], job["company"], job["location"],
                      job["url"], "", "[]", 0))
                if conn.total_changes:
                    new_count += 1
            except sqlite3.IntegrityError:
                pass

        conn.commit()
        time.sleep(2)

    conn.close()
    print(f"\nDone! {new_count} new jobs added.")
    return new_count


if __name__ == "__main__":
    scrape_and_store()
