#!/usr/bin/env python3
"""Unified entry point for Pharma Market Intel: FAERS + ClinicalTrials.gov.

Usage:
    python chain_entry.py --drug "sotorasib" --metrics faers,trials --output ./output
    python chain_entry.py --drug "aspirin" --metrics trials --condition "pain" --output ./output
"""
import argparse
import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable


def run_faers(drug, output, limit_events=20):
    """Run query_faers.py and return success bool."""
    cmd = [PYTHON, os.path.join(SCRIPT_DIR, "query_faers.py"),
           "--drug", drug, "--output", output,
           "--limit-events", str(limit_events)]
    print(f"[chain] Running FAERS query...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stderr, file=sys.stderr, end='')
    print(result.stdout, end='')
    return result.returncode == 0


def run_trials(drug=None, condition=None, status=None, phase=None, limit=20, output="."):
    """Run query_trials.py and return success bool."""
    cmd = [PYTHON, os.path.join(SCRIPT_DIR, "query_trials.py"), "--output", output]
    if drug:
        cmd.extend(["--drug", drug])
    if condition:
        cmd.extend(["--condition", condition])
    if status:
        cmd.extend(["--status", status])
    if phase:
        cmd.extend(["--phase", phase])
    cmd.extend(["--limit", str(limit)])
    print(f"[chain] Running ClinicalTrials.gov query...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stderr, file=sys.stderr, end='')
    print(result.stdout, end='')
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Pharma Market Intel unified entry point.")
    parser.add_argument("--drug", required=True, help="Drug name or SMILES")
    parser.add_argument("--metrics", default="faers,trials",
                        help="Comma-separated: faers, trials, clinical_trials (default: faers,trials)")
    parser.add_argument("--condition", help="Condition for trials search")
    parser.add_argument("--status", help="Trial status filter")
    parser.add_argument("--phase", help="Trial phase filter")
    parser.add_argument("--limit", type=int, default=20, help="Limit for trials/events")
    parser.add_argument("--output", default="./market_intel_output", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)
    metrics = [m.strip().lower() for m in args.metrics.split(",")]

    results = {"drug": args.drug, "metrics_requested": metrics, "outputs": {}}

    if "faers" in metrics:
        faers_dir = os.path.join(args.output, "faers")
        os.makedirs(faers_dir, exist_ok=True)
        ok = run_faers(args.drug, faers_dir, args.limit)
        results["outputs"]["faers"] = {"success": ok, "directory": faers_dir}

    if "trials" in metrics or "clinical_trials" in metrics:
        trials_dir = os.path.join(args.output, "trials")
        os.makedirs(trials_dir, exist_ok=True)
        ok = run_trials(
            drug=args.drug, condition=args.condition,
            status=args.status, phase=args.phase,
            limit=args.limit, output=trials_dir
        )
        results["outputs"]["trials"] = {"success": ok, "directory": trials_dir}

    # Write combined manifest
    manifest_path = os.path.join(args.output, "chain_manifest.json")
    with open(manifest_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n[chain] Complete. Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
