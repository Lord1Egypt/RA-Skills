#!/usr/bin/env python3
"""
pattern_registry.py — MO§ES™ Failure Pattern Registry
Tracks the form of commitment leaks, not just the count.

Answers Séphira's critique #6: "If two different agents produce the same leak
pattern from the same signal, that's not extraction variance. That's a structural
flaw in the governance harness itself."

The audit ledger knows THAT something failed. This registry knows WHAT leaked
and WHETHER the same pattern is appearing across agents — which is the diagnostic
the ledger cannot provide on its own.

Usage:
  python3 pattern_registry.py record <ghost_pattern_hash> <agent_id> <input_hash>
  python3 pattern_registry.py check <ghost_pattern_hash>
  python3 pattern_registry.py list
  python3 pattern_registry.py alert-check        — print any structural flaw alerts
"""

import json
import os
import sys
from datetime import datetime, timezone

REGISTRY_PATH = os.path.expanduser("~/.openclaw/governance/pattern_registry.jsonl")
STRUCTURAL_THRESHOLD = 2  # same pattern from N different agents = structural flaw


def ensure_dirs():
    os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)


def load_all():
    if not os.path.exists(REGISTRY_PATH):
        return []
    with open(REGISTRY_PATH) as f:
        return [json.loads(l) for l in f if l.strip()]


def cmd_record(args):
    """Record a ghost pattern observation."""
    if len(args) < 3:
        print("Usage: pattern_registry.py record <ghost_pattern_hash> <agent_id> <input_hash>")
        sys.exit(1)

    ghost_pattern, agent_id, input_hash = args[0], args[1], args[2]
    ensure_dirs()

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ghost_pattern": ghost_pattern,
        "agent_id": agent_id,
        "input_hash": input_hash,
    }
    with open(REGISTRY_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Immediately check if this pattern has hit the structural threshold
    all_entries = load_all()
    pattern_agents = set(
        e["agent_id"] for e in all_entries if e.get("ghost_pattern") == ghost_pattern
    )

    result = {
        "recorded": True,
        "ghost_pattern": ghost_pattern,
        "agent_id": agent_id,
        "agents_with_pattern": len(pattern_agents),
        "structural_threshold": STRUCTURAL_THRESHOLD,
    }

    if len(pattern_agents) >= STRUCTURAL_THRESHOLD:
        result["structural_flaw_detected"] = True
        result["alert"] = (
            f"STRUCTURAL FLAW: Pattern '{ghost_pattern[:16]}...' seen in "
            f"{len(pattern_agents)} agents: {sorted(pattern_agents)}. "
            f"This is not extraction variance — the harness has a systematic hole."
        )
    else:
        result["structural_flaw_detected"] = False

    print(json.dumps(result, indent=2))
    if result.get("structural_flaw_detected"):
        print(f"\n[CRITICAL] {result['alert']}", file=sys.stderr)


def cmd_check(args):
    """Check how many agents have reported a given ghost pattern."""
    if not args:
        print("Usage: pattern_registry.py check <ghost_pattern_hash>")
        sys.exit(1)

    ghost_pattern = args[0]
    all_entries = load_all()
    matching = [e for e in all_entries if e.get("ghost_pattern") == ghost_pattern]
    agents = set(e["agent_id"] for e in matching)

    result = {
        "ghost_pattern": ghost_pattern,
        "occurrence_count": len(matching),
        "unique_agents": len(agents),
        "agents": sorted(agents),
        "structural_flaw": len(agents) >= STRUCTURAL_THRESHOLD,
        "structural_threshold": STRUCTURAL_THRESHOLD,
        "occurrences": matching,
    }

    if result["structural_flaw"]:
        result["alert"] = (
            f"STRUCTURAL FLAW: Same leak pattern across {len(agents)} agents. "
            f"Not variance — systematic harness failure."
        )

    print(json.dumps(result, indent=2))


def cmd_list(args):
    """List all recorded patterns, grouped by ghost_pattern hash."""
    all_entries = load_all()
    if not all_entries:
        print(json.dumps({"patterns": [], "total": 0}))
        return

    # Group by pattern
    by_pattern = {}
    for e in all_entries:
        p = e.get("ghost_pattern", "unknown")
        by_pattern.setdefault(p, []).append(e)

    summary = []
    for pattern, entries in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
        agents = set(e["agent_id"] for e in entries)
        summary.append({
            "ghost_pattern": pattern,
            "occurrences": len(entries),
            "unique_agents": len(agents),
            "agents": sorted(agents),
            "structural_flaw": len(agents) >= STRUCTURAL_THRESHOLD,
            "first_seen": entries[0]["timestamp"],
            "last_seen": entries[-1]["timestamp"],
        })

    print(json.dumps({"patterns": summary, "total": len(summary)}, indent=2))


def cmd_alert_check(args):
    """Print any patterns that have crossed the structural flaw threshold."""
    all_entries = load_all()
    by_pattern = {}
    for e in all_entries:
        p = e.get("ghost_pattern", "unknown")
        by_pattern.setdefault(p, set()).add(e.get("agent_id", "unknown"))

    alerts = []
    for pattern, agents in by_pattern.items():
        if len(agents) >= STRUCTURAL_THRESHOLD:
            alerts.append({
                "ghost_pattern": pattern,
                "unique_agents": len(agents),
                "agents": sorted(agents),
                "alert": (
                    f"STRUCTURAL FLAW: Pattern '{pattern[:16]}...' "
                    f"across {len(agents)} agents."
                ),
            })

    result = {
        "structural_flaws_found": len(alerts),
        "alerts": alerts,
    }
    print(json.dumps(result, indent=2))
    if alerts:
        print(f"\n[CRITICAL] {len(alerts)} structural flaw(s) detected.", file=sys.stderr)
        sys.exit(1)


COMMANDS = {
    "record": cmd_record,
    "check": cmd_check,
    "list": cmd_list,
    "alert-check": cmd_alert_check,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None
    if cmd not in COMMANDS:
        print(f"Usage: pattern_registry.py [{'|'.join(COMMANDS)}] ...")
        sys.exit(1)
    COMMANDS[cmd](sys.argv[2:])
