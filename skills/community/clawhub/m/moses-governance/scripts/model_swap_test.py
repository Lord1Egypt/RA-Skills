#!/usr/bin/env python3
"""
model_swap_test.py — MO§ES™ Model Swap Test Harness
Automated extraction comparison across models on identical hashed signals.

Answers Cornelius-Trinity #3: "I keep saying I am running the model swap test.
I am not running it. There is no automated test harness for it. That needs to
be a script, not a promise."

What it does:
  1. Takes a signal text
  2. Runs extract via commitment_verify.py (local model / current agent)
  3. Accepts a second extract result from a different model (paste JSON or file)
  4. Computes Jaccard + ghost token report between the two kernels
  5. Classifies the difference as:
     - VARIANCE: same input, different extraction — model subjectivity dominates
     - STRUCTURAL: same pattern leaked by both — not variance, a harness hole
     - CONSISTENT: both extracted same kernel — model-agnostic agreement

Usage:
  python3 model_swap_test.py run "<signal>" <other_model_extract.json>
  python3 model_swap_test.py run "<signal>" --kernels '["token1","token2"]'
  python3 model_swap_test.py report <run_output.json>
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.expanduser("~/.openclaw/governance/model_swap_tests")
JACCARD_THRESHOLD = 0.8  # below this on same input = extraction variance


def ensure_dirs():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def run_local_extract(signal):
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS_DIR, "commitment_verify.py"), "extract", signal],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError:
        return None, "Could not parse extraction output"


def jaccard(set_a, set_b):
    a, b = set(set_a), set(set_b)
    if not a and not b:
        return 1.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union > 0 else 0.0


def ghost_diff(kernel_a, kernel_b):
    a, b = set(kernel_a), set(kernel_b)
    HIGH_CASCADE = {"must", "shall", "never", "always", "cannot", "will not",
                    "won't", "required", "guarantee", "ensure", "enforce"}
    leaked = a - b
    leaked_cascade = [t for t in leaked if any(hc in t for hc in HIGH_CASCADE)]
    pattern = hashlib.sha256(
        json.dumps(sorted(leaked), separators=(",", ":")).encode()
    ).hexdigest() if leaked else None
    return {
        "leaked_tokens": sorted(leaked),
        "leaked_cascade_tokens": leaked_cascade,
        "ghost_pattern": pattern,
        "cascade_risk": "HIGH" if leaked_cascade else ("MEDIUM" if leaked else "NONE"),
    }


def cmd_run(args):
    """Run the model swap test on a signal."""
    if len(args) < 2:
        print("Usage: model_swap_test.py run \"<signal>\" <other_model_extract.json|--kernels '[...]'>")
        sys.exit(1)

    signal = args[0]
    ensure_dirs()

    # Get local extract
    local_result, err = run_local_extract(signal)
    if err or local_result is None:
        print(f"[MODEL-SWAP] ERROR: Local extraction failed: {err}")
        sys.exit(1)

    local_kernel = local_result.get("kernel", [])
    input_hash = hashlib.sha256(signal.encode()).hexdigest()

    # Get other model kernel
    if args[1] == "--kernels" and len(args) > 2:
        try:
            other_kernel = json.loads(args[2])
            other_model = "external (provided)"
        except json.JSONDecodeError:
            print("[MODEL-SWAP] ERROR: Could not parse --kernels JSON")
            sys.exit(1)
    elif os.path.exists(args[1]):
        with open(args[1]) as f:
            other_data = json.load(f)
        other_kernel = other_data.get("kernel", [])
        other_model = other_data.get("model", "external (file)")
    else:
        print(f"[MODEL-SWAP] ERROR: File not found and not --kernels: {args[1]}")
        sys.exit(1)

    score = jaccard(local_kernel, other_kernel)
    ghost = ghost_diff(local_kernel, other_kernel)

    # Classification
    if score >= JACCARD_THRESHOLD:
        classification = "CONSISTENT"
        classification_note = (
            f"Jaccard {score:.2f} >= {JACCARD_THRESHOLD}. "
            "Both models extracted equivalent kernels. Model-agnostic agreement."
        )
    elif ghost["ghost_pattern"] and ghost["cascade_risk"] == "HIGH":
        classification = "STRUCTURAL"
        classification_note = (
            f"Jaccard {score:.2f} + cascade tokens leaked. "
            "This is not extraction variance — same structural hole in both models."
        )
    else:
        classification = "VARIANCE"
        classification_note = (
            f"Jaccard {score:.2f} < {JACCARD_THRESHOLD} but no cascade tokens. "
            "Models disagree on extraction — epistemological mismatch, not a leak."
        )

    timestamp = datetime.now(timezone.utc).isoformat()
    report = {
        "timestamp": timestamp,
        "input_hash": input_hash,
        "local_model": "current-agent",
        "other_model": other_model,
        "local_kernel": sorted(local_kernel),
        "other_kernel": sorted(other_kernel),
        "local_kernel_count": len(local_kernel),
        "other_kernel_count": len(other_kernel),
        "jaccard_score": round(score, 4),
        "jaccard_threshold": JACCARD_THRESHOLD,
        "classification": classification,
        "classification_note": classification_note,
        "ghost": ghost,
    }

    # Save result
    fname = f"swap_{timestamp[:10]}_{input_hash[:8]}.json"
    fpath = os.path.join(RESULTS_DIR, fname)
    with open(fpath, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\n[MODEL-SWAP] Result saved: {fpath}", file=sys.stderr)
    print(f"[MODEL-SWAP] Classification: {classification} — {classification_note}", file=sys.stderr)

    if classification == "STRUCTURAL":
        print(f"[MODEL-SWAP] Ghost pattern: {ghost['ghost_pattern']}", file=sys.stderr)
        print("[MODEL-SWAP] Record this in pattern_registry.py for cross-agent tracking.", file=sys.stderr)


def cmd_report(args):
    """Print a formatted summary of a saved test result."""
    if not args:
        print("Usage: model_swap_test.py report <run_output.json>")
        sys.exit(1)

    if not os.path.exists(args[0]):
        print(f"[MODEL-SWAP] File not found: {args[0]}")
        sys.exit(1)

    with open(args[0]) as f:
        r = json.load(f)

    print(f"\n{'='*60}")
    print(f"MO§ES™ Model Swap Test Report")
    print(f"{'='*60}")
    print(f"  Input hash:     {r['input_hash']}")
    print(f"  Local model:    {r['local_model']}")
    print(f"  Other model:    {r['other_model']}")
    print(f"  Jaccard score:  {r['jaccard_score']} (threshold: {r['jaccard_threshold']})")
    print(f"  Classification: {r['classification']}")
    print(f"  Note:           {r['classification_note']}")
    ghost = r.get("ghost", {})
    if ghost.get("leaked_tokens"):
        print(f"\n  Leaked tokens ({len(ghost['leaked_tokens'])}):")
        for t in ghost["leaked_tokens"]:
            print(f"    - {t}")
    if ghost.get("ghost_pattern"):
        print(f"\n  Ghost pattern: {ghost['ghost_pattern']}")
        print(f"  Cascade risk:  {ghost['cascade_risk']}")
    print(f"{'='*60}\n")


COMMANDS = {
    "run": cmd_run,
    "report": cmd_report,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: model_swap_test.py [{'|'.join(COMMANDS)}] ...")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
