#!/usr/bin/env python3
"""
Indeed Monitor — Gracie Lead Generator
Scrapes Indeed for businesses hiring front-desk/receptionist roles.
Each posting = confirmed Gracie lead.
"""

import subprocess, json, re, argparse, sys
from datetime import datetime

SCRAPLING_SCRIPT = "/Users/wlc-studio/StudioBrain/00_SYSTEM/skills/scrapling/scrape.py"
LEADS_FILE = "/Users/wlc-studio/StudioBrain/30_INTERNAL/WLC-Services/LEADS/MASTER_LEAD_LIST.md"

QUERIES = [
    "receptionist",
    "customer service representative",
    "front desk",
]

LOCATIONS = [
    "Staten Island, NY",
    "Brooklyn, NY",
    "Bronx, NY",
]

# Industries we care about — filter out staffing agencies
TARGET_INDUSTRIES = [
    "dental", "dentist", "orthodont",
    "plumb", "hvac", "heating", "cooling", "mechanical",
    "auto", "automotive", "car repair", "tire",
    "chiro", "physical therapy", "medical", "clinic", "health",
    "real estate", "realt",
    "law", "attorney", "legal",
    "insurance",
    "restaurant", "cafe", "catering",
    "salon", "spa", "beauty",
    "construction", "contractor", "roofing",
]

# Skip these — staffing agencies, not real businesses
SKIP_COMPANIES = [
    "staffmark", "manpower", "randstad", "robert half", "kelly services",
    "adecco", "temp", "staffing", "recruiting", "talent", "hire quest",
    "indeed prime", "solomon page",
]


def fetch(url):
    r = subprocess.run(
        ["python3", SCRAPLING_SCRIPT, "web", url],
        capture_output=True, text=True, timeout=30
    )
    try:
        d = json.loads(r.stdout)
        return d.get("content", [""])[0]
    except:
        return ""


def parse_jobs(html):
    """Extract job cards from Indeed search results."""
    jobs = []
    
    target_titles = ["receptionist", "front desk", "customer service", "office manager", "call center", "administrative assistant"]
    
    # Split into lines and find job title lines, then extract surrounding context
    lines = [l.strip() for l in html.split('\n') if l.strip()]
    
    # These are Indeed UI elements / benefit labels — not company names
    NOISE_COMPANY = [
        "salary search", "get email", "indeed", "sign in", "skip to", "post job",
        "sort by", "new update", "view all", "see popular", "people also",
        "how to hire", "upload your", "previous", "next", "filter", "by creating",
        "terms", "privacy", "dental insurance", "vision insurance", "life insurance",
        "health insurance", "paid time off", "paid holidays", "401(k)",
        "flexible spending", "employee discount", "opportunities for",
        "supporting daily", "previous experience", "manage mail",
        "escort guests", "find out how", "our growing", "great compensation",
        "day shift", "night shift", "remote", "hybrid", "full-time", "part-time",
        "salary", "jobs in", "salaries in", "salaries -", "questions &",
        "slightly farther", "stamford, ct", "new york jobs", "brooklyn jobs",
        "bronx jobs", "newark jobs", "jersey city jobs", "livingston jobs",
        "wallington jobs", "flushing jobs", "kew gardens jobs", "glen ridge jobs",
        "rockville centre jobs", "township of monroe jobs", "ramsey jobs",
        "parlin jobs", "monsey jobs", "front desk agent jobs", "front desk aide",
        "office clerk jobs", "bellman jobs", "concierge-pd", "administrative associate",
    ]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # This line is a job title
        if not any(t in line_lower for t in target_titles):
            continue
        
        # Too long = probably a description
        if len(line) > 70:
            continue
        
        # Skip noise title lines
        skip_title = ["salary search", "get email", "sort by", "jobs in", "salaries in",
                      "people also", "how to hire", "upload your", "view all", "see popular",
                      "by creating", "find out how", "filter", "previous", "terms"]
        if any(p in line_lower for p in skip_title):
            continue
        
        title = line
        
        # Look backwards for company name
        company = None
        for j in range(max(0, i-4), i):
            candidate = lines[j]
            if len(candidate) < 4 or len(candidate) > 55:
                continue
            if not candidate[0].isupper() and not candidate[0].isdigit():
                continue
            candidate_lower = candidate.lower()
            # Must not be noise
            if any(n in candidate_lower for n in NOISE_COMPANY):
                continue
            # Must not be a location-only line
            if re.match(r'^[A-Z][a-z]+,\s+[A-Z]{2}', candidate):
                continue
            # Reject lines that look like job requirements/descriptions
            requirement_patterns = [
                r'^\d+\s+hours', r'^expected hours', r'^monday', r'^tuesday',
                r'^ability to', r'^must be', r'^calling ', r'^support$',
                r'^return to', r'^professional dev', r'^training', r'^seasonal$',
                r'^per diem', r'^maintain a', r'^customer service:\s+\d',
                r'^boutique associate', r'^40 hours', r'^35 per',
                r'^prior experience', r'^profile insights', r'^englewood jobs',
                r'^parsippany', r'^white plains jobs', r'^staten island, ny$',
            ]
            if any(re.match(p, candidate_lower) for p in requirement_patterns):
                continue
            # Must look like a company name — letters, possibly numbers, Inc/LLC/DDS etc
            if re.search(r'[A-Za-z]{3,}', candidate):
                company = candidate
                break
        
        if not company:
            continue
            
        # Skip staffing agencies
        if any(skip.lower() in company.lower() for skip in SKIP_COMPANIES):
            continue
        
        # Skip if company looks like a noise line
        if any(n in company.lower() for n in NOISE_COMPANY):
            continue

        # Look forward for location
        location = "Staten Island area"
        for j in range(i+1, min(len(lines), i+4)):
            candidate = lines[j]
            loc_signals = ["island", "brooklyn", "bronx", "queens", "manhattan", "new york", "ny ", ", ny", ", nj"]
            if any(s in candidate.lower() for s in loc_signals) and len(candidate) < 50:
                # Skip if it's a jobs/salaries link line
                if "jobs in" not in candidate.lower() and "salaries in" not in candidate.lower():
                    location = candidate
                    break
        
        # Look for salary
        salary = None
        for j in range(i-2, min(len(lines), i+5)):
            if 0 <= j < len(lines) and "$" in lines[j] and "hour" in lines[j].lower():
                salary = lines[j].strip()[:40]
                break

        jobs.append({
            "company": company,
            "title": title,
            "location": location,
            "salary": salary,
        })

    # Deduplicate
    seen = set()
    unique = []
    for j in jobs:
        k = f"{j['company'].lower()}|{j['title'].lower()}"
        if k not in seen:
            seen.add(k)
            unique.append(j)
    
    return unique


def score_lead(job):
    """Score lead quality based on industry signals."""
    company_lower = job["company"].lower()
    title_lower = job["title"].lower()
    
    score = 0
    pain_signals = []

    # Industry match
    for industry in TARGET_INDUSTRIES:
        if industry in company_lower:
            score += 3
            pain_signals.append(f"Industry match: {industry}")
            break

    # Title signals
    if "receptionist" in title_lower:
        score += 2
        pain_signals.append("Hiring receptionist")
    if "customer service" in title_lower:
        score += 2
        pain_signals.append("Hiring CSR")
    if "24" in title_lower or "evening" in title_lower or "weekend" in title_lower:
        score += 3
        pain_signals.append("After-hours coverage needed")

    job["score"] = score
    job["pain_signals"] = pain_signals if pain_signals else ["Hiring front desk staff"]
    return job


def run(query, location, verbose=False):
    url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+').replace(',', '%2C')}&sort=date&fromage=14"
    
    if verbose:
        print(f"  Scanning: {query} in {location}...", flush=True)
    
    html = fetch(url)
    if not html:
        return []
    
    jobs = parse_jobs(html)
    scored = [score_lead(j) for j in jobs]
    return scored


def main():
    parser = argparse.ArgumentParser(description="Indeed Monitor — Gracie Lead Generator")
    parser.add_argument("--query", type=str, help="Override search query")
    parser.add_argument("--location", type=str, help="Override location")
    parser.add_argument("--save", action="store_true", help="Append results to master lead list")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    queries = [args.query] if args.query else QUERIES
    locations = [args.location] if args.location else LOCATIONS

    print(f"\n🔍 Indeed Monitor — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"   Scanning {len(queries)} queries × {len(locations)} locations...\n")

    all_leads = []
    seen = set()

    for location in locations:
        for query in queries:
            jobs = run(query, location, verbose=args.verbose)
            for job in jobs:
                key = f"{job['company'].lower()}_{job['location'].lower()}"
                if key not in seen:
                    seen.add(key)
                    all_leads.append(job)

    # Sort by score
    all_leads.sort(key=lambda x: x.get("score", 0), reverse=True)

    if not all_leads:
        print("❌ No leads found. Indeed may be blocking — try again later.")
        return

    print(f"✅ Found {len(all_leads)} leads:\n")
    print(f"{'#':<4} {'Company':<35} {'Title':<30} {'Location':<25} {'Pain Signals'}")
    print("-" * 120)

    for i, lead in enumerate(all_leads, 1):
        signals = ", ".join(lead.get("pain_signals", []))
        print(f"{i:<4} {lead['company'][:34]:<35} {lead['title'][:29]:<30} {lead['location'][:24]:<25} {signals}")

    if args.save:
        timestamp = datetime.now().strftime("%Y-%m-%d")
        with open(LEADS_FILE, "a") as f:
            f.write(f"\n\n---\n\n## 📋 Indeed Scan — {timestamp}\n\n")
            f.write("| Company | Title | Location | Pain Signal |\n")
            f.write("|---------|-------|----------|-------------|\n")
            for lead in all_leads:
                signals = ", ".join(lead.get("pain_signals", []))
                f.write(f"| {lead['company']} | {lead['title']} | {lead['location']} | {signals} |\n")
        print(f"\n💾 Saved {len(all_leads)} leads to master list.")

    print(f"\n📞 Top 5 to call first:")
    for lead in all_leads[:5]:
        print(f"   • {lead['company']} — {lead['title']} ({lead['location']})")
        print(f"     Pain: {', '.join(lead.get('pain_signals', []))}")


if __name__ == "__main__":
    main()
