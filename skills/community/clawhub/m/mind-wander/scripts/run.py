#!/usr/bin/env python3
"""
run.py — Mind-wander agent entry point.

Usage:
    python3 mind-wander/run.py                         # auto-select from ON_YOUR_MIND.md
    python3 mind-wander/run.py --anchor "Phase 5b"     # focus on specific item
    python3 mind-wander/run.py --model q8              # use Q8 model
    python3 mind-wander/run.py --verbose               # show agent reasoning
    python3 mind-wander/run.py --dry-run               # show what would happen
    python3 mind-wander/run.py --compare               # run both Q4 and Q8, compare results
    python3 mind-wander/run.py --status                # show system status
"""

import argparse
import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "memory-upgrade"))

from mind_wander_config import (
    WANDER_MODEL_Q4, WANDER_MODEL_Q8, WANDER_OLLAMA,
    ON_YOUR_MIND_FILE, MENTAL_EXPLORATION_FILE, WANDER_LOG_FILE,
    WANDER_STATE_FILE, WORKSPACE,
)


def check_status():
    """Print system status."""
    print("\n=== Mind-Wander Status ===\n")

    # Model availability
    import httpx
    for model_name, label in [(WANDER_MODEL_Q4, "Q4_K_M"), (WANDER_MODEL_Q8, "Q8_0")]:
        try:
            resp = httpx.get(f"{WANDER_OLLAMA}/api/tags", timeout=5)
            models = [m["name"] for m in resp.json().get("models", [])]
            loaded = any(model_name in m for m in models)
            print(f"  {'✅' if loaded else '❌'} {label} ({model_name}): {'loaded' if loaded else 'not found'}")
        except Exception as e:
            print(f"  ❌ {label}: {e}")

    # Files
    print(f"\n  {'✅' if ON_YOUR_MIND_FILE.exists() else '⚠️ '} ON_YOUR_MIND.md: "
          f"{'exists' if ON_YOUR_MIND_FILE.exists() else 'NOT FOUND — create this file!'}")
    print(f"  {'✅' if MENTAL_EXPLORATION_FILE.exists() else '📝'} MENTAL_EXPLORATION.md: "
          f"{'exists' if MENTAL_EXPLORATION_FILE.exists() else 'not yet (will be created on first elevation)'}")

    # State
    if WANDER_STATE_FILE.exists():
        state = json.loads(WANDER_STATE_FILE.read_text())
        runs = state.get("runs", {})
        elevated = state.get("elevated", [])
        print(f"\n  📊 Previous runs: {len(runs)}")
        print(f"  ✨ Total elevations: {len(elevated)}")
        if elevated:
            last = elevated[-1]
            print(f"  Last elevated: '{last['title']}' at {last['ts']}")
    else:
        print("\n  📊 No previous runs yet")

    # Log
    if WANDER_LOG_FILE.exists():
        lines = WANDER_LOG_FILE.read_text().strip().split("\n")
        print(f"\n  📝 Log entries: {len(lines)}")
        if lines:
            print(f"  Last: {lines[-1][:100]}")

    print()


def compare_models(anchor: str = None, verbose: bool = False):
    """Run both Q4 and Q8 and compare output."""
    import os
    results = {}
    for model_key, model_name in [("Q4", WANDER_MODEL_Q4), ("Q8", WANDER_MODEL_Q8)]:
        print(f"\n{'='*50}")
        print(f"Running {model_key} ({model_name})...")
        os.environ["WANDER_MODEL"] = model_name
        # Re-import to pick up env change
        import importlib
        import mind_wander_config as mwc
        importlib.reload(mwc)
        import agent as ag
        importlib.reload(ag)
        result = ag.run(anchor_item=anchor, verbose=verbose)
        results[model_key] = result
        print(f"\n{model_key} result: elevated={result['elevated']}, "
              f"tool_calls={result['tool_calls']}, duration={result['duration']:.1f}s")

    print(f"\n{'='*50}")
    print("Comparison:")
    for k, r in results.items():
        print(f"  {k}: {'✨ elevated' if r['elevated'] else 'no elevation'} | "
              f"{r['tool_calls']} tool calls | {r['duration']:.1f}s")
    return results


def main():
    parser = argparse.ArgumentParser(description="Mind-wander agent")
    parser.add_argument("--anchor", help="Focus on a specific ON_YOUR_MIND item")
    parser.add_argument("--model", choices=["q4", "q8"], default="q4",
                        help="Which quantization to use (default: q4)")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show agent reasoning and tool calls")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without running")
    parser.add_argument("--compare", action="store_true",
                        help="Run both Q4 and Q8 and compare")
    parser.add_argument("--status", action="store_true",
                        help="Show system status")
    args = parser.parse_args()

    if args.status:
        check_status()
        return

    if args.compare:
        compare_models(args.anchor, args.verbose)
        return

    model = WANDER_MODEL_Q4 if args.model == "q4" else WANDER_MODEL_Q8

    # Check ON_YOUR_MIND.md exists
    if not ON_YOUR_MIND_FILE.exists() and not args.dry_run:
        print(f"❌ ON_YOUR_MIND.md not found at {ON_YOUR_MIND_FILE}")
        print("   Create it with your open questions and unresolved tangents.")
        sys.exit(1)

    from agent import run
    result = run(
        anchor_item=args.anchor,
        dry_run=args.dry_run,
        verbose=args.verbose or args.dry_run,
        model_override=model,
    )

    if not args.dry_run:
        print(f"\n{'✨ Elevated!' if result['elevated'] else '💭 No elevation'} | "
              f"{result['tool_calls']} tool calls | {result['duration']:.1f}s")
        if result["elevated"]:
            print(f"   → '{result['title']}' written to MENTAL_EXPLORATION.md")


if __name__ == "__main__":
    main()
