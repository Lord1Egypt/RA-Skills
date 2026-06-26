#!/usr/bin/env python3
"""Query ClinicalTrials.gov API v2 for drug/condition clinical trial data.

Generates JSON summaries and matplotlib visualizations.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime

import requests
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

API_BASE = "https://clinicaltrials.gov/api/v2/studies"

VALID_STATUSES = [
    "RECRUITING", "COMPLETED", "ACTIVE_NOT_RECRUITING",
    "NOT_YET_RECRUITING", "TERMINATED", "WITHDRAWN",
    "ENROLLING_BY_INVITATION", "SUSPENDED", "UNKNOWN"
]
VALID_PHASES = ["EARLY_PHASE1", "PHASE1", "PHASE2", "PHASE3", "PHASE4", "NA"]


def resolve_smiles_to_name(smiles):
    """Resolve SMILES to drug name via PubChem."""
    try:
        import urllib.parse
        encoded = urllib.parse.quote(smiles, safe='')
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{encoded}/synonyms/JSON"
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return None
        synonyms = (resp.json()
                    .get('InformationList', {})
                    .get('Information', [{}])[0]
                    .get('Synonym', []))
        for syn in synonyms:
            if not syn.startswith('InChI=') and len(syn) < 50 and syn.isascii():
                return syn
        return synonyms[0] if synonyms else None
    except Exception:
        return None


def is_smiles(s):
    """Heuristic: looks like SMILES rather than a drug name."""
    return bool(re.search(r'[=#\[\]\\/@]', s)) or (not s.isalpha() and len(s) > 5)


def fetch_trials(drug=None, condition=None, status=None, phase=None, limit=20):
    """Fetch trials from ClinicalTrials.gov API v2."""
    params = {
        "pageSize": min(limit, 100),
        "format": "json",
    }

    # Build query
    if drug:
        params["query.intr"] = drug
    if condition:
        params["query.cond"] = condition
    if not drug and not condition:
        raise ValueError("Must specify --drug or --condition (or both)")

    if status:
        s = status.upper()
        if s not in VALID_STATUSES:
            print(f"Warning: '{s}' not in known statuses: {VALID_STATUSES}", file=sys.stderr)
        params["filter.overallStatus"] = s

    if phase:
        p = phase.upper()
        if p not in VALID_PHASES:
            print(f"Warning: '{p}' not in known phases: {VALID_PHASES}", file=sys.stderr)
        # API v2 uses filter.advanced for phase filtering
        params["filter.advanced"] = f"AREA[Phase]{p}"

    all_studies = []
    next_token = None
    total = None

    while len(all_studies) < limit:
        if next_token:
            params["pageToken"] = next_token
        params["pageSize"] = min(limit - len(all_studies), 100)

        resp = requests.get(API_BASE, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        if total is None:
            total = data.get("totalCount", 0)

        studies = data.get("studies", [])
        if not studies:
            break
        all_studies.extend(studies)

        next_token = data.get("nextPageToken")
        if not next_token:
            break

    return all_studies, total or len(all_studies)


def parse_study(study):
    """Extract key fields from a study object."""
    proto = study.get("protocolSection", {})
    ident = proto.get("identificationModule", {})
    status_mod = proto.get("statusModule", {})
    design = proto.get("designModule", {})
    conds = proto.get("conditionsModule", {})
    arms = proto.get("armsInterventionsModule", {})
    sponsor_mod = proto.get("sponsorCollaboratorsModule", {})

    nct_id = ident.get("nctId", "")

    # Interventions
    interventions = []
    for iv in arms.get("interventions", []):
        interventions.append(iv.get("name", ""))

    # Sponsor
    lead = sponsor_mod.get("leadSponsor", {})
    sponsor = lead.get("name", "")

    # Dates
    start_info = status_mod.get("startDateStruct", {})
    comp_info = status_mod.get("completionDateStruct", {}) or status_mod.get("primaryCompletionDateStruct", {})
    start_date = start_info.get("date", "")
    completion_date = comp_info.get("date", "") if comp_info else ""

    # Enrollment
    enroll_info = design.get("enrollmentInfo", {})
    enrollment = enroll_info.get("count") if enroll_info else None

    # Phases - can be list like ["PHASE1", "PHASE2"] or single
    phases = design.get("phases", [])
    phase_str = "|".join(phases) if phases else "NA"

    return {
        "nct_id": nct_id,
        "title": ident.get("briefTitle", ""),
        "status": status_mod.get("overallStatus", ""),
        "phase": phase_str,
        "conditions": conds.get("conditions", []),
        "interventions": interventions,
        "sponsor": sponsor,
        "start_date": start_date,
        "completion_date": completion_date,
        "enrollment": enrollment,
        "study_type": design.get("studyType", ""),
        "url": f"https://clinicaltrials.gov/study/{nct_id}"
    }


def compute_stats(trials):
    """Compute aggregate statistics."""
    phase_ctr = Counter()
    status_ctr = Counter()
    sponsor_ctr = Counter()
    condition_ctr = Counter()

    for t in trials:
        for p in t["phase"].split("|"):
            phase_ctr[p] += 1
        status_ctr[t["status"]] += 1
        if t["sponsor"]:
            sponsor_ctr[t["sponsor"]] += 1
        for c in t["conditions"]:
            condition_ctr[c] += 1

    return {
        "by_phase": dict(phase_ctr.most_common()),
        "by_status": dict(status_ctr.most_common()),
        "top_sponsors": sponsor_ctr.most_common(15),
        "top_conditions": condition_ctr.most_common(15),
    }


def plot_bar(data_dict, title, xlabel, ylabel, filepath):
    """Generic horizontal bar chart."""
    if not data_dict:
        return
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    fig, ax = plt.subplots(figsize=(10, max(4, len(labels) * 0.5)))
    ax.barh(range(len(labels)), values, color='steelblue')
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels)
    ax.set_xlabel(ylabel)
    ax.set_title(title)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()


def plot_timeline(trials, title, filepath):
    """Timeline scatter of trial start dates."""
    dates = []
    labels = []
    for t in trials:
        d = t.get("start_date", "")
        if not d:
            continue
        try:
            # Handles "YYYY-MM-DD", "YYYY-MM", "Month YYYY", etc.
            for fmt in ("%Y-%m-%d", "%Y-%m", "%B %Y", "%B %d, %Y"):
                try:
                    dt = datetime.strptime(d, fmt)
                    dates.append(dt)
                    labels.append(t["nct_id"])
                    break
                except ValueError:
                    continue
        except Exception:
            continue

    if not dates:
        return

    fig, ax = plt.subplots(figsize=(12, max(4, len(dates) * 0.3)))
    y_pos = range(len(dates))
    ax.scatter(dates, y_pos, c='steelblue', s=40, zorder=3)
    ax.set_yticks(list(y_pos))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("Start Date")
    ax.set_title(title)
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Query ClinicalTrials.gov for drug/condition trials.")
    parser.add_argument("--drug", help="Drug name or SMILES")
    parser.add_argument("--condition", help="Disease/condition")
    parser.add_argument("--status", help="Filter by status (e.g. RECRUITING, COMPLETED)")
    parser.add_argument("--phase", help="Filter by phase (e.g. PHASE3)")
    parser.add_argument("--limit", type=int, default=20, help="Max trials to fetch (default 20)")
    parser.add_argument("--output", default="./trials_output", help="Output directory")
    args = parser.parse_args()

    if not args.drug and not args.condition:
        parser.error("Must specify --drug or --condition (or both)")

    os.makedirs(args.output, exist_ok=True)

    drug_name = args.drug
    resolved_from_smiles = False

    # SMILES resolution
    if drug_name and is_smiles(drug_name):
        print(f"Resolving SMILES to drug name...", file=sys.stderr)
        resolved = resolve_smiles_to_name(drug_name)
        if resolved:
            print(f"Resolved to: {resolved}", file=sys.stderr)
            drug_name = resolved
            resolved_from_smiles = True
        else:
            print(f"Could not resolve SMILES, using as search term", file=sys.stderr)

    # Fetch
    print(f"Querying ClinicalTrials.gov: drug={drug_name}, condition={args.condition}, "
          f"status={args.status}, phase={args.phase}, limit={args.limit}", file=sys.stderr)

    try:
        studies, total_found = fetch_trials(
            drug=drug_name, condition=args.condition,
            status=args.status, phase=args.phase, limit=args.limit
        )
    except requests.RequestException as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not studies:
        print("No trials found.", file=sys.stderr)
        # Write empty summary
        label = drug_name or args.condition or "query"
        summary = {
            "drug": drug_name, "query": vars(args),
            "total_found": 0, "trials": [], "stats": {}
        }
        with open(os.path.join(args.output, f"{label}_trials_summary.json"), 'w') as f:
            json.dump(summary, f, indent=2)
        sys.exit(0)

    # Parse
    trials = [parse_study(s) for s in studies]
    stats = compute_stats(trials)

    # File label
    label = (drug_name or args.condition or "query").replace(" ", "_").replace("/", "_")

    summary = {
        "drug": drug_name,
        "query": {
            "drug": drug_name,
            "condition": args.condition,
            "status": args.status,
            "phase": args.phase,
            "resolved_from_smiles": resolved_from_smiles,
        },
        "total_found": total_found,
        "trials_returned": len(trials),
        "trials": trials,
        "stats": stats,
    }

    summary_path = os.path.join(args.output, f"{label}_trials_summary.json")
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary: {summary_path}", file=sys.stderr)

    # Plots
    try:
        plot_bar(stats["by_phase"],
                 f"Clinical Trials by Phase: {drug_name or args.condition}",
                 "Phase", "Count",
                 os.path.join(args.output, f"{label}_trials_by_phase.png"))
    except Exception as e:
        print(f"Plot error (phase): {e}", file=sys.stderr)

    try:
        plot_bar(stats["by_status"],
                 f"Clinical Trials by Status: {drug_name or args.condition}",
                 "Status", "Count",
                 os.path.join(args.output, f"{label}_trials_by_status.png"))
    except Exception as e:
        print(f"Plot error (status): {e}", file=sys.stderr)

    try:
        plot_timeline(trials,
                      f"Trial Start Date Timeline: {drug_name or args.condition}",
                      os.path.join(args.output, f"{label}_trials_timeline.png"))
    except Exception as e:
        print(f"Plot error (timeline): {e}", file=sys.stderr)

    # Print summary to stdout
    print(f"\n=== ClinicalTrials.gov Results ===")
    print(f"Drug/Query: {drug_name or args.condition}")
    print(f"Total found: {total_found}")
    print(f"Returned: {len(trials)}")
    print(f"By phase: {stats['by_phase']}")
    print(f"By status: {stats['by_status']}")
    print(f"Top sponsors: {stats['top_sponsors'][:5]}")
    print(f"Files saved to: {args.output}/")


if __name__ == "__main__":
    main()
