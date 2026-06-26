#!/usr/bin/env python3
"""
Lead Enrichment & Scoring Tool
Usage: python3 enrich_leads.py --input leads.json [--output leads_scored.csv]
       python3 enrich_leads.py --interactive

Input JSON format:
[
  {
    "name": "Jane Smith",
    "title": "VP Marketing",
    "company": "Acme Corp",
    "industry": "SaaS",
    "size": "51-200",
    "email": "jane@acme.com",
    "linkedin": "https://linkedin.com/in/janesmith",
    "signals": ["recently_funded", "hiring"],
    "notes": "Series B in Jan 2026"
  }
]
"""

import json
import csv
import sys
import argparse
from datetime import datetime

# ICP scoring weights
ICP_INDUSTRIES = []  # Set via --icp-industries
ICP_TITLES = []      # Set via --icp-titles
ICP_SIZES = []       # Set via --icp-sizes

BUYING_SIGNALS = {
    "recently_funded": 1.0,
    "hiring": 1.0,
    "uses_competitor": 1.0,
    "new_exec": 0.5,
    "product_launch": 0.5,
    "expansion": 0.5,
    "rebranding": 0.5,
}

Q1_MONTHS = [1, 2, 3]
Q3_MONTHS = [7, 8, 9]


def score_icp_fit(lead, icp_industries, icp_titles, icp_sizes):
    score = 0
    industry = lead.get("industry", "").lower()
    title = lead.get("title", "").lower()
    size = lead.get("size", "")

    if icp_industries and any(i.lower() in industry for i in icp_industries):
        score += 1
    elif not icp_industries:
        score += 1  # No filter = assume fit

    if icp_titles and any(t.lower() in title for t in icp_titles):
        score += 1
    elif not icp_titles:
        score += 1

    if icp_sizes and any(s.lower() in size.lower() for s in icp_sizes):
        score += 1
    elif not icp_sizes:
        score += 1

    return min(score, 3)


def score_buying_signals(lead):
    signals = lead.get("signals", [])
    score = 0
    for signal in signals:
        score += BUYING_SIGNALS.get(signal.lower().replace(" ", "_"), 0)
    return min(score, 3)


def score_reachability(lead):
    score = 0
    if lead.get("email"):
        score += 1
    if lead.get("linkedin"):
        score += 0.5
    if lead.get("phone"):
        score += 0.5
    return min(score, 2)


def score_timing(lead):
    score = 0
    current_month = datetime.now().month
    if current_month in Q1_MONTHS or current_month in Q3_MONTHS:
        score += 1

    signals = lead.get("signals", [])
    notes = lead.get("notes", "").lower()

    # Recent trigger events
    for signal in signals:
        if signal in ("recently_funded", "new_exec", "product_launch"):
            score += 1
            break

    return min(score, 2)


def get_priority(total_score):
    if total_score >= 8:
        return "🔴 STRIKE NOW"
    elif total_score >= 6:
        return "🟡 HIGH PRIORITY"
    elif total_score >= 4:
        return "🟢 PIPELINE"
    else:
        return "⬜ NURTURE"


def enrich_and_score(leads, icp_industries=None, icp_titles=None, icp_sizes=None):
    icp_industries = icp_industries or []
    icp_titles = icp_titles or []
    icp_sizes = icp_sizes or []

    scored = []
    for lead in leads:
        icp = score_icp_fit(lead, icp_industries, icp_titles, icp_sizes)
        signals = score_buying_signals(lead)
        reachability = score_reachability(lead)
        timing = score_timing(lead)

        raw = icp + signals + reachability + timing  # max 10
        total = round(min(raw, 10), 1)

        enriched = dict(lead)
        enriched["score_icp"] = icp
        enriched["score_signals"] = signals
        enriched["score_reachability"] = reachability
        enriched["score_timing"] = timing
        enriched["total_score"] = total
        enriched["priority"] = get_priority(total)
        scored.append(enriched)

    # Sort by score descending
    scored.sort(key=lambda x: x["total_score"], reverse=True)
    return scored


def to_csv(leads, output_path=None):
    if not leads:
        return ""

    fieldnames = [
        "name", "title", "company", "industry", "size",
        "email", "linkedin", "signals", "notes",
        "score_icp", "score_signals", "score_reachability", "score_timing",
        "total_score", "priority"
    ]

    import io
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    for lead in leads:
        row = dict(lead)
        if isinstance(row.get("signals"), list):
            row["signals"] = ", ".join(row["signals"])
        writer.writerow(row)

    csv_content = output.getvalue()

    if output_path:
        with open(output_path, "w") as f:
            f.write(csv_content)
        print(f"Saved to {output_path}", file=sys.stderr)

    return csv_content


def print_summary(leads):
    total = len(leads)
    strike = sum(1 for l in leads if l["total_score"] >= 8)
    high = sum(1 for l in leads if 6 <= l["total_score"] < 8)
    pipeline = sum(1 for l in leads if 4 <= l["total_score"] < 6)
    nurture = sum(1 for l in leads if l["total_score"] < 4)

    print(f"\n📊 Lead Scoring Summary — {total} leads processed")
    print(f"  🔴 Strike Now (8–10):    {strike}")
    print(f"  🟡 High Priority (6–7):  {high}")
    print(f"  🟢 Pipeline (4–5):       {pipeline}")
    print(f"  ⬜ Nurture (<4):         {nurture}")

    if strike > 0:
        print(f"\n🎯 Top {min(5, strike)} leads to contact today:")
        for lead in leads[:min(5, strike)]:
            print(f"  • {lead['name']} ({lead['title']} @ {lead['company']}) — Score: {lead['total_score']}/10")
            if lead.get('notes'):
                print(f"    → {lead['notes']}")


def main():
    parser = argparse.ArgumentParser(description="Lead Enrichment & Scoring")
    parser.add_argument("--input", help="JSON file with lead data")
    parser.add_argument("--output", help="Output CSV file path")
    parser.add_argument("--icp-industries", help="Comma-separated target industries")
    parser.add_argument("--icp-titles", help="Comma-separated target job titles")
    parser.add_argument("--icp-sizes", help="Comma-separated target company sizes")
    parser.add_argument("--format", default="summary", choices=["summary", "csv", "json"])
    args = parser.parse_args()

    icp_industries = [x.strip() for x in args.icp_industries.split(",")] if args.icp_industries else []
    icp_titles = [x.strip() for x in args.icp_titles.split(",")] if args.icp_titles else []
    icp_sizes = [x.strip() for x in args.icp_sizes.split(",")] if args.icp_sizes else []

    if args.input:
        with open(args.input) as f:
            leads = json.load(f)
    elif not sys.stdin.isatty():
        stdin_data = sys.stdin.read().strip()
        if not stdin_data:
            # Fall through to demo
            stdin_data = None
        if stdin_data:
            leads = json.loads(stdin_data)
        else:
            leads = None
    else:
        leads = None

    if leads is None:
        # Demo mode — no input provided
        print("Demo mode. Showing sample output.\n", file=sys.stderr)
        leads = [
            {"name": "Alice Johnson", "title": "VP Marketing", "company": "GrowthCo", "industry": "SaaS", "size": "51-200", "email": "alice@growthco.com", "linkedin": "https://linkedin.com/in/alicejohnson", "signals": ["recently_funded", "hiring"], "notes": "Series A Feb 2026"},
            {"name": "Bob Chen", "title": "Head of Sales", "company": "RetailTech", "industry": "E-commerce", "size": "11-50", "email": "", "linkedin": "https://linkedin.com/in/bobchen", "signals": ["uses_competitor"], "notes": ""},
            {"name": "Carol Wu", "title": "Founder", "company": "NicheStartup", "industry": "Consulting", "size": "1-10", "email": "carol@niche.io", "linkedin": "", "signals": [], "notes": ""},
        ]

    scored = enrich_and_score(leads, icp_industries, icp_titles, icp_sizes)

    if args.format == "json":
        print(json.dumps(scored, indent=2))
    elif args.format == "csv":
        print(to_csv(scored, args.output))
    else:
        print_summary(scored)
        if args.output:
            to_csv(scored, args.output)


if __name__ == "__main__":
    main()
