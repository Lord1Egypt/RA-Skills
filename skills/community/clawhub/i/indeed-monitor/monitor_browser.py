#!/usr/bin/env python3
"""
Indeed Monitor (Browser Version) — Gracie Lead Generator
Uses OpenClaw browser relay to pull clean Indeed job cards.
Requires Chrome relay to be active.
"""

import subprocess, json, re, argparse, sys
from datetime import datetime

LEADS_FILE = "/Users/wlc-studio/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md"

SEARCHES = [
    ("receptionist", "Staten Island, NY"),
    ("receptionist", "Brooklyn, NY"),
    ("receptionist", "Bronx, NY"),
    ("HVAC receptionist", "Staten Island, NY"),
    ("dental receptionist", "Staten Island, NY"),
    ("auto repair customer service", "Staten Island, NY"),
    ("customer service representative", "Staten Island, NY"),
]

CITIES = [
    "Staten Island", "Brooklyn", "Bronx", "Queens", "Manhattan", "New York",
    "Flushing", "Kew Gardens", "Jamaica", "Manalapan", "Glen Ridge", "Denville",
    "Englewood", "Wallington", "Linden", "Livingston", "Amityville", "Manhasset",
    "Parsippany-Troy Hills", "Parsippany", "Jersey City", "Newark", "Parlin",
    "Monsey", "Rockville Centre", "White Plains", "Ramsey", "Saddle Brook",
    "Township of Monroe", "North Bergen", "New Hyde Park", "Stamford",
    "Park Slope", "Sunset Park", "Bay Ridge", "Astoria", "Long Island City",
    "Hoboken", "Secaucus", "Bayonne", "Elizabeth", "Woodbridge", "Edison",
]
CITIES.sort(key=len, reverse=True)

SKIP_COMPANIES = [
    "staffmark", "manpower", "randstad", "robert half", "kelly services",
    "adecco", "staffing", "recruiting", "talent solutions", "hire quest",
    "solomon page", "indeed", "avis budget", "conduent", "u-haul",
    "abm industries", "shj international",
]

TARGET_INDUSTRIES = {
    "dental": ["dental", "dentist", "orthodont"],
    "hvac": ["hvac", "heating", "cooling", "mechanical", "plumb"],
    "auto": ["auto", "automotive", "car repair", "tire", "motor"],
    "medical": ["medical", "clinic", "health", "chiro", "physical therapy"],
    "insurance": ["insurance", "state farm", "allstate"],
    "legal": ["law", "attorney", "legal"],
    "real_estate": ["real estate", "realt", "property"],
}


def openclaw_snapshot(target_id):
    """Get aria snapshot of current browser tab."""
    r = subprocess.run(
        ["node", "-e", f"""
const {{OpenClawBrowser}} = require('/opt/homebrew/lib/node_modules/openclaw/dist/tools/browser.js');
// Just use curl to the local API
"""],
        capture_output=True, text=True, timeout=15
    )
    return r.stdout


def fetch_indeed_via_relay(query, location):
    """Navigate to Indeed and snapshot via OpenClaw browser relay CLI."""
    import time
    url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+').replace(',', '%2C')}&sort=date&fromage=7"
    
    subprocess.run(
        ["openclaw", "browser", "navigate", "--url", url, "--profile", "chrome"],
        capture_output=True, text=True, timeout=20
    )
    time.sleep(2)
    
    s = subprocess.run(
        ["openclaw", "browser", "snapshot", "--profile", "chrome", "--compact"],
        capture_output=True, text=True, timeout=20
    )
    return s.stdout


def parse_company_location(raw):
    """Extract clean company + location from Indeed's concatenated text."""
    line = re.sub(r'^Easily apply (?:New )?', '', raw.strip())
    line = re.sub(r'\s*\([^)]+\).*$', '', line).strip()
    
    for city in CITIES:
        pattern = rf'^(.+?)\s+{re.escape(city)},?\s+(NY|NJ|CT|PA)\s*(\d{{5}})?'
        m = re.search(pattern, line, re.IGNORECASE)
        if m:
            company = m.group(1).strip().rstrip(',')
            state = m.group(2)
            zip_ = m.group(3) or ""
            return company, f"{city}, {state} {zip_}".strip()
    return None, None


def parse_snapshot(snapshot_text):
    """Parse Indeed aria snapshot for clean job leads."""
    jobs = []

    # Pattern: heading "full details of <Title>" followed by text with company+location
    cards = re.finditer(
        r'heading "full details of ([^"]{5,100})".*?text[:\s]+"?([^"\n]{10,120})',
        snapshot_text, re.DOTALL
    )

    for match in cards:
        title = re.sub(r'\s*-\s*job post$', '', match.group(1)).strip()
        raw_text = match.group(2).strip()
        
        company, location = parse_company_location(raw_text)
        if company and location:
            jobs.append({"title": title, "company": company, "location": location})

    return jobs


def score_lead(job):
    company_lower = job["company"].lower()
    title_lower = job["title"].lower()
    score = 0
    signals = []
    
    for industry, keywords in TARGET_INDUSTRIES.items():
        if any(k in company_lower or k in title_lower for k in keywords):
            score += 3
            signals.append(f"{industry.upper()} business")
            break

    if "receptionist" in title_lower:
        score += 2
        signals.append("Hiring receptionist")
    if "customer service" in title_lower:
        score += 2
        signals.append("Hiring CSR")
    if any(w in title_lower for w in ["bilingual", "spanish", "english"]):
        score += 2
        signals.append("Bilingual needed → Sofia angle")
    if any(w in title_lower for w in ["24", "evening", "weekend", "overnight"]):
        score += 3
        signals.append("After-hours coverage needed")

    job["score"] = score
    job["signals"] = signals if signals else ["Hiring front desk staff"]
    return job


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", action="store_true", help="Append to master lead list")
    args = parser.parse_args()

    print(f"\n🔍 Indeed Monitor (Browser) — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("   Requires Chrome relay to be active.\n")

    all_leads = []
    seen = set()

    for query, location in SEARCHES:
        print(f"  Scanning: {query} in {location}...", flush=True)
        snapshot = fetch_indeed_via_relay(query, location)
        jobs = parse_snapshot(snapshot)
        
        for job in jobs:
            if any(skip in job["company"].lower() for skip in SKIP_COMPANIES):
                continue
            key = f"{job['company'].lower()}|{job['title'].lower()}"
            if key not in seen:
                seen.add(key)
                all_leads.append(score_lead(job))

    all_leads.sort(key=lambda x: x.get("score", 0), reverse=True)

    if not all_leads:
        print("❌ No leads found. Make sure Chrome relay is active.")
        return

    print(f"\n✅ Found {len(all_leads)} clean leads:\n")
    print(f"{'#':<4} {'Company':<35} {'Title':<35} {'Location':<20} {'Signals'}")
    print("-" * 130)

    for i, lead in enumerate(all_leads, 1):
        signals = ", ".join(lead.get("signals", []))
        print(f"{i:<4} {lead['company'][:34]:<35} {lead['title'][:34]:<35} {lead['location'][:19]:<20} {signals}")

    if args.save:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        with open(LEADS_FILE, "a") as f:
            f.write(f"\n\n---\n\n## 📋 Indeed Scan (Browser) — {timestamp}\n\n")
            f.write("| Company | Title | Location | Signals |\n")
            f.write("|---------|-------|----------|---------|\n")
            for lead in all_leads:
                signals = ", ".join(lead.get("signals", []))
                f.write(f"| {lead['company']} | {lead['title']} | {lead['location']} | {signals} |\n")
        print(f"\n💾 Saved {len(all_leads)} leads → MASTER_LEAD_LIST.md")

    print(f"\n🔥 Top targets:")
    for lead in all_leads[:5]:
        print(f"   • {lead['company']} — {lead['title']} ({lead['location']})")
        print(f"     Signals: {', '.join(lead.get('signals', []))}")


if __name__ == "__main__":
    run()
