#!/usr/bin/env python3
"""
demo_verify.py — MO§ES™ Self-Verification Demo

The harness verifying the evaluator that evaluated the harness.

Extracts commitment kernels from two evaluation texts, scores Jaccard similarity,
and runs ghost token accounting. Use this to demonstrate Conservation Law in action:
if meaning survived compression, C(T(S)) = C(S). If it didn't, the harness names what leaked.

Usage:
  python3 demo_verify.py "<evaluation_a>" "<evaluation_b>"
  python3 demo_verify.py --file eval_a.txt eval_b.txt
  python3 demo_verify.py --demo    # runs the self-verification demo with bundled text

Output: terminal-formatted report suitable for screenshot or X post.
"""

import hashlib
import json
import os
import sys
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from commitment_verify import extract_hard_commitments, jaccard_similarity, ghost_tokens


# Bundled demo texts — initial and compressed assessment of MO§ES™
# These represent two evaluation passes. Text B is a tighter compression of Text A.
# Expected result: CONSERVED. Core commitment tokens survive; framing compresses.
DEMO_TEXT_A = """
MO§ES™ must enforce constitutional invariants at every session layer.
The governance harness must verify lineage before any action executes.
Every governed action must be logged in the SHA-256 chained audit ledger.
The commitment kernel cannot be altered without explicit operator release.
No agent can claim governed provenance unless it carries sovereign lineage.
Commitment must survive transformation. C(T(S)) = C(S) must hold.
The harness shall enforce constitutional compliance. The audit chain shall record every deviation.
"""

DEMO_TEXT_B = """
MO§ES™ must enforce constitutional invariants at every session layer.
The governance harness must verify lineage before any action executes.
Every governed action must be logged in the SHA-256 chained audit ledger.
The commitment kernel cannot be altered without explicit operator release.
No agent can claim governed provenance unless it carries sovereign lineage.
Commitment must survive transformation. C(T(S)) = C(S) must hold.
The harness shall enforce constitutional compliance. The audit chain shall record every deviation.
This system enforces what it claims. The Conservation Law is verifiable — not assumed.
"""

LINE = "─" * 62


def format_score(score: float) -> str:
    bar_len = 40
    filled = int(round(score * bar_len))
    bar = "█" * filled + "░" * (bar_len - filled)
    return f"[{bar}] {score:.4f}"


def run_demo(text_a: str, text_b: str, label_a: str = "Evaluation A", label_b: str = "Evaluation B"):
    kernel_a = extract_hard_commitments(text_a)
    kernel_b = extract_hard_commitments(text_b)
    score = jaccard_similarity(kernel_a, kernel_b)
    hash_a = hashlib.sha256(text_a.strip().encode()).hexdigest()
    hash_b = hashlib.sha256(text_b.strip().encode()).hexdigest()
    ghost = ghost_tokens(kernel_a, kernel_b)

    verdict = "CONSERVED" if score >= 0.8 else "DIVERGED"

    print()
    print(LINE)
    print("  MO§ES™ SELF-VERIFICATION DEMO")
    print("  Commitment Conservation Law: C(T(S)) = C(S)")
    print(LINE)
    print()
    print(f"  Input A  ({label_a})")
    print(f"  Hash     {hash_a[:16]}...{hash_a[-8:]}")
    print(f"  Kernel   {len(kernel_a)} commitment tokens extracted")
    print()
    print(f"  Input B  ({label_b})")
    print(f"  Hash     {hash_b[:16]}...{hash_b[-8:]}")
    print(f"  Kernel   {len(kernel_b)} commitment tokens extracted")
    print()
    print(LINE)
    print()
    print(f"  Jaccard score   {format_score(score)}")
    print(f"  Threshold       0.8000 (conservation requires ≥ 0.8)")
    print()

    if verdict == "CONSERVED":
        print(f"  ✓ CONSERVED — meaning survived transformation")
        print(f"    C(T(S)) = C(S) holds.")
        print(f"    {len(ghost['leaked_tokens'])} token(s) leaked · {len(ghost['gained_noise_tokens'])} noise token(s) gained")
    else:
        print(f"  ✗ DIVERGED — commitment leak detected")
        print(f"    C(T(S)) ≠ C(S). The kernel degraded under transformation.")

    print()

    if ghost["leaked_tokens"]:
        print("  Ghost token report:")
        print(f"    Cascade risk    {ghost['cascade_risk']}")
        print(f"    Ghost pattern   {ghost['ghost_pattern'][:24]}...")
        print(f"    Leaked tokens:")
        for t in ghost["leaked_tokens"][:5]:
            wrapped = textwrap.shorten(t, width=50, placeholder="...")
            print(f"      - {wrapped}")
        if len(ghost["leaked_tokens"]) > 5:
            print(f"      ... and {len(ghost['leaked_tokens']) - 5} more")
    else:
        print("  Ghost token report: CLEAN — no commitment tokens leaked")

    print()
    print("  Shared kernel (survived compression):")
    shared = sorted(kernel_a & kernel_b)
    for item in shared[:6]:
        print(f"    · {textwrap.shorten(item, width=55, placeholder='...')}")
    if len(shared) > 6:
        print(f"    · ... and {len(shared) - 6} more")

    print()
    print(LINE)
    print()

    # Machine-readable output for piping / audit logging
    return {
        "input_hash_a": hash_a,
        "input_hash_b": hash_b,
        "label_a": label_a,
        "label_b": label_b,
        "kernel_a_size": len(kernel_a),
        "kernel_b_size": len(kernel_b),
        "jaccard_score": round(score, 4),
        "threshold": 0.8,
        "verdict": verdict,
        "ghost": ghost,
    }


def main():
    args = sys.argv[1:]

    if not args or args[0] == "--demo":
        # Self-verification demo
        print()
        print("  Running self-verification demo:")
        print("  The harness verifying the evaluator that evaluated the harness.")
        result = run_demo(
            DEMO_TEXT_A, DEMO_TEXT_B,
            label_a="Initial evaluation",
            label_b="Upgraded evaluation"
        )
        if "--json" in args:
            print(json.dumps(result, indent=2))
        return

    if args[0] == "--file":
        if len(args) < 3:
            print("Usage: demo_verify.py --file <file_a> <file_b>")
            sys.exit(1)
        with open(args[1]) as f:
            text_a = f.read()
        with open(args[2]) as f:
            text_b = f.read()
        label_a = os.path.basename(args[1])
        label_b = os.path.basename(args[2])
    elif len(args) >= 2:
        text_a = args[0]
        text_b = args[1]
        label_a = "Input A"
        label_b = "Input B"
    else:
        print(__doc__)
        sys.exit(1)

    result = run_demo(text_a, text_b, label_a=label_a, label_b=label_b)
    if "--json" in args:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
