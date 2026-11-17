#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pre-flight checker for a Literature Evidence Package before pasting into the Cloud.
Purely local; no request, no order, no cost.
Usage: python3 check_evidence.py <evidence.json>   (or pipe: ... | python3 check_evidence.py -)
Exit code 0 = package looks ready; nonzero = reasons listed.
"""
import json
import sys

REQUIRED = [
    "record_id", "title", "authors", "publication_year",
    "evidence_availability_level", "metadata_status",
]

def slurp():
    if len(sys.argv) > 1 and sys.argv[1] != "-":
        raw = open(sys.argv[1], encoding="utf-8").read()
    else:
        raw = sys.stdin.read()
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.strip("`").lstrip("json").strip()
    return raw

def main():
    try:
        data = json.loads(slurp())
    except json.JSONDecodeError as e:
        print("INVALID — not valid JSON:", e); sys.exit(1)

    issues = []
    rc = data.get("run_context")
    if not isinstance(rc, dict) or not str(rc.get("research_question", "")).strip():
        issues.append("run_context.research_question is empty (required).")

    papers = data.get("papers")
    if not isinstance(papers, list) or not papers:
        issues.append("papers must be a non-empty array.")
    else:
        for i, p in enumerate(papers):
            if not isinstance(p, dict):
                issues.append(f"papers[{i}] is not an object."); continue
            for k in REQUIRED:
                if not str(p.get(k, "")).strip():
                    issues.append(f"papers[{i}] missing/empty '{k}'.")
            lvl = str(p.get("evidence_availability_level", "")).strip()
            if lvl and lvl[0] not in "ABCD":
                issues.append(f"papers[{i}] evd_level starts with '{lvl[0]}' (expect A/B/C/D).")
    if issues:
        print("INVALID — fix before pasting to cloud:"); [print("  -", x) for x in issues]; sys.exit(1)
    print("OK — evidence package looks ready (one record = one paper / row).")

if __name__ == "__main__":
    main()