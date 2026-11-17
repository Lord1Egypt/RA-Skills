#!/usr/bin/env python3
"""
Bower → MemPalace ingestion script.
Extracts MEANINGFUL facts about the operator's life from Bower scan data.
Only files facts that tell you something real — never file counts or org patterns.
"""

import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 bower_mem_ingest.py [no flags]")
    sys.exit(0)

BOWER_DATA = Path(os.path.expanduser("~/.hermes/commons/data/ocas-bower"))
OUTPUT_FILE = BOWER_DATA / "mem_ingest_output.json"

# Keywords that indicate meaningful personal content
MEANINGFUL_SIGNALS = {
    "health": ["fibroscan", "ucsf", "lab result", "blood test", "prescription",
               "diagnosis", "surgery", "mri", "ct scan", "colonoscopy",
               "cholesterol", "a1c", "glucose", "dental", "vision",
               "cardiologist", "dermatologist", "physical exam"],
    "finance": ["mortgage", "401k", "ira", "roth", "rsu", "vesting", "ipo",
                "net worth", "tax return", "w-2", "1099", "budget",
                "investment portfolio", "credit card", "bank account",
                "insurance policy", "refinanc", "capital gains"],
    "home": ["renovation", "contractor", "permit", "inspection", "kitchen remodel",
             "bathroom remodel", "roof", "hvac", "plumbing", "honu hale",
             "shower", "flooring", "landscaping"],
    "travel": ["airbnb", "hotel booking", "flight confirmation", "itinerary",
               "passport", "visa", "reservation", "boarding pass"],
    "career": ["offer letter", "salary negotiation", "promotion", "job description",
               "performance review", "compensation", "equity grant"],
    "social": ["wedding", "birthday", "anniversary", "memorial", "graduation"],
}

def load_json(path):
    with open(path) as f:
        return json.load(f)

def extract_meaningful_facts(content_summaries_file):
    """Extract specific, meaningful facts from content summaries."""
    facts = {"health": [], "finance": [], "home": [], "travel": [], "career": [], "social": []}
    
    with open(content_summaries_file) as f:
        for line in f:
            s = json.loads(line)
            text = (s.get("summary_text", "") + " " + s.get("name", "")).lower()
            
            for category, signals in MEANINGFUL_SIGNALS.items():
                for signal in signals:
                    if signal in text:
                        facts[category].append({
                            "signal": signal,
                            "file": s.get("name", ""),
                            "snippet": s.get("summary_text", "")[:200],
                        })
                        break  # one match per category per file

    # Deduplicate by signal
    for category in facts:
        seen = set()
        deduped = []
        for f in facts[category]:
            if f["signal"] not in seen:
                seen.add(f["signal"])
                deduped.append(f)
        facts[category] = deduped
    
    return facts

def main():
    cs_file = BOWER_DATA / "content_summaries.jsonl"
    facts = extract_meaningful_facts(cs_file)
    
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "facts": facts,
        "kg_facts": [],
        "drawer_content": "",
    }
    
    # Build KG facts from specific findings
    for health in facts["health"]:
        signal = health["signal"]
        if signal == "ucsf":
            output["kg_facts"].append({"subject": "the operator", "predicate": "medical_provider", "object": "UCSF"})
        elif signal == "fibroscan":
            output["kg_facts"].append({"subject": "the operator", "predicate": "requested_medical_procedure", "object": "FibroScan"})
    
    for finance in facts["finance"]:
        signal = finance["signal"]
        if "mortgage" in signal:
            output["kg_facts"].append({"subject": "the operator", "predicate": "has_financial_account", "object": "mortgage"})
        elif "401k" in signal or "ira" in signal or "roth" in signal:
            output["kg_facts"].append({"subject": "the operator", "predicate": "has_retirement_account", "object": signal})
    
    for home in facts["home"]:
        signal = home["signal"]
        if "honu hale" in signal:
            output["kg_facts"].append({"subject": "the operator", "predicate": "home_renovation_project", "object": "Honu Hale"})
    
    # Build drawer content — ONLY meaningful facts, NO counts
    lines = [f"## Life Facts Discovered — {output['generated_at'][:10]}"]
    
    for category in ["health", "finance", "home", "travel", "career", "social"]:
        if facts[category]:
            lines.append(f"\n### {category.title()}")
            for f in facts[category]:
                lines.append(f"- {f['signal']}: {f['file']}")
    
    if not any(facts.values()):
        lines.append("\nNo new meaningful facts found in this scan.")
    
    output["drawer_content"] = "\n".join(lines)
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"Meaningful facts found: {sum(len(v) for v in facts.values())}")
    print(f"KG facts to add: {len(output['kg_facts'])}")
    for cat, items in facts.items():
        if items:
            print(f"  {cat}: {[f['signal'] for f in items]}")

if __name__ == "__main__":
    main()
