#!/usr/bin/env python3
"""memory-guardian: Violation event logger and rule health monitor.

Tracks when memory rules are violated (e.g., importance 0.8 memory decayed to 0.15),
maintains structured logs and per-rule health summaries.

Data files:
  - .memory-guardian/violation_events.jsonl   — append-only event stream
  - .memory-guardian/rule_health.json          — per-rule health summaries

Usage:
  python3 memory_violations.py log --rule <id> --event <desc> [--context <text>] [--workspace <path>]
  python3 memory_violations.py check [--workspace <path>] [--days <N>] [--min-count <N>]
  python3 memory_violations.py health [--workspace <path>]
"""
import json, os, sys, argparse, hashlib
from datetime import datetime, timedelta
from mg_utils import _now_iso, CST, save_meta as _save_meta, read_text_file, safe_print, file_lock_acquire
from collections import defaultdict

print = safe_print

DEFAULT_WORKSPACE = os.environ.get(
    "OPENCLAW_WORKSPACE", os.path.expanduser("~/workspace/agent/workspace")
)


def guard_dir(workspace):
    d = os.path.join(workspace, ".memory-guardian")
    os.makedirs(d, exist_ok=True)
    return d


def events_path(workspace):
    return os.path.join(guard_dir(workspace), "violation_events.jsonl")


def health_path(workspace):
    return os.path.join(guard_dir(workspace), "rule_health.json")


def context_hash(text):
    """Lightweight hash for context similarity grouping."""
    if not text:
        return "none"
    return hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def load_events(workspace, days=None):
    """Load violation events, optionally filtered by recent N days."""
    path = events_path(workspace)
    if not os.path.exists(path):
        return []
    events = []
    cutoff = None
    if days:
        cutoff = datetime.now(CST) - timedelta(days=days)
    for line in read_text_file(path).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
            if cutoff:
                ts = datetime.fromisoformat(ev.get("timestamp", "2000-01-01"))
                if ts < cutoff:
                    continue
            events.append(ev)
        except json.JSONDecodeError:
            continue
    return events


def load_health(workspace):
    """Load rule health summaries."""
    path = health_path(workspace)
    if not os.path.exists(path):
        return {"rules": {}, "last_updated": None}
    return json.loads(read_text_file(path))


def save_health(workspace, health):
    path = health_path(workspace)
    health["last_updated"] = _now_iso()
    _save_meta(path, health)


MAX_VIOLATION_FILE_SIZE = 500 * 1024  # 500KB
MAX_VIOLATION_EVENTS = 500
RECENT_VIOLATIONS_WINDOW_DAYS = 7


def cmd_log(rule_id, event, context, severity, workspace):
    """Append a violation event."""
    path = events_path(workspace)

    # Bug 4: Rotate if file exceeds size limit
    if os.path.exists(path) and os.path.getsize(path) > MAX_VIOLATION_FILE_SIZE:
        with file_lock_acquire(path):
            events = load_events(workspace)
            events = events[-MAX_VIOLATION_EVENTS:]
            with open(path, "w", encoding="utf-8") as f:
                for e in events:
                    f.write(json.dumps(e, ensure_ascii=True) + "\n")

    ev = {
        "rule_id": rule_id,
        "event": event,
        "context": context or "",
        "context_hash": context_hash(context),
        "severity": severity,
        "timestamp": _now_iso(),
    }

    # Bug 3: Use file lock for concurrent append protection
    with file_lock_acquire(path):
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(ev, ensure_ascii=True) + "\n")

    # Update health
    health = load_health(workspace)
    rules = health.setdefault("rules", {})
    rule = rules.setdefault(rule_id, {
        "total_violations": 0,
        "recent_violations": 0,
        "last_violation": None,
        "scene_hashes": [],
        "revision_history": [],
        "cooldown_until": None,
        "status": "active",
    })
    rule["total_violations"] += 1

    # Bug 5: Recount recent_violations using a 7-day time window
    cutoff = datetime.now(CST) - timedelta(days=RECENT_VIOLATIONS_WINDOW_DAYS)
    rule_events = load_events(workspace, days=RECENT_VIOLATIONS_WINDOW_DAYS)
    rule["recent_violations"] = sum(
        1 for e in rule_events if e.get("rule_id") == rule_id
    )

    rule["last_violation"] = ev["timestamp"]
    if context:
        ch = ev["context_hash"]
        if ch not in rule["scene_hashes"]:
            rule["scene_hashes"].append(ch)
    save_health(workspace, health)

    print(f"[LOG] Violation recorded: {rule_id}")
    print(f"  Event: {event[:80]}")
    print(f"  Severity: {severity}")
    print(f"  Total violations for rule: {rule['total_violations']}")


def cmd_check(workspace, days, min_count):
    """Check for rules that need revision based on violation patterns."""
    events = load_events(workspace, days=days)
    health = load_health(workspace)

    if not events:
        print(f"No violation events in the last {days} days.")
        return {"action": "none", "rules_needing_revision": []}

    # Group by rule
    by_rule = defaultdict(list)
    for ev in events:
        by_rule[ev["rule_id"]].append(ev)

    print(f"=== Violation Check (last {days} days) ===")
    print(f"Total events: {len(events)}")
    print(f"Rules with violations: {len(by_rule)}")
    print()

    needs_revision = []
    for rule_id, evs in sorted(by_rule.items(), key=lambda x: -len(x[1])):
        rule_health = health.get("rules", {}).get(rule_id, {})
        cooldown_until = rule_health.get("cooldown_until")

        # Check cooldown
        if cooldown_until:
            cd = datetime.fromisoformat(cooldown_until)
            if datetime.now(CST) < cd:
                print(f"  [{rule_id}] {len(evs)} violations — ON COOLDOWN until {cooldown_until[:10]}")
                continue

        # Check scene similarity
        hashes = [ev["context_hash"] for ev in evs]
        unique_hashes = set(hashes)
        similarity_ratio = len(unique_hashes) / max(len(hashes), 1)

        print(f"  [{rule_id}] {len(evs)} violations, {len(unique_hashes)} unique scenes")

        if len(evs) >= min_count and similarity_ratio <= 0.7:
            # High violation count + similar scenes → needs revision
            needs_revision.append({
                "rule_id": rule_id,
                "count": len(evs),
                "unique_scenes": len(unique_hashes),
                "similarity_ratio": similarity_ratio,
                "latest_event": evs[-1]["event"][:80],
            })
            print(f"    ⚠️  REVISION RECOMMENDED — {len(evs)} violations with similar scenes")
            print(f"    Latest: {evs[-1]['event'][:60]}")
        else:
            print(f"    ✅ No revision needed (similar scenes: {similarity_ratio:.0%})")

    print()
    if needs_revision:
        print(f"=== {len(needs_revision)} rule(s) need revision ===")
        for r in needs_revision:
            print(f"  • {r['rule_id']}: {r['count']} violations, {r['unique_scenes']} unique scenes")
    else:
        print("All rules are healthy. No revisions needed.")

    return {"action": "check", "rules_needing_revision": needs_revision}


def cmd_health(workspace):
    """Show rule health summary."""
    health = load_health(workspace)
    rules = health.get("rules", {})

    if not rules:
        print("No rule health data yet. Run 'log' to record violations.")
        return

    print(f"=== Rule Health Summary ===")
    print(f"Last updated: {health.get('last_updated', 'never')}")
    print()

    for rule_id, rule in sorted(rules.items(), key=lambda x: -x[1].get("total_violations", 0)):
        status_icon = "🔴" if rule.get("status") == "needs_revision" else ("🟡" if rule.get("cooldown_until") else "🟢")
        print(f"  {status_icon} [{rule_id}]")
        print(f"     Total violations: {rule.get('total_violations', 0)}")
        print(f"     Recent: {rule.get('recent_violations', 0)}")
        print(f"     Last: {rule.get('last_violation', 'never')}")
        print(f"     Unique scenes: {len(rule.get('scene_hashes', []))}")
        print(f"     Revisions: {len(rule.get('revision_history', []))}")
        if rule.get("cooldown_until"):
            print(f"     Cooldown until: {rule['cooldown_until'][:10]}")
        print()

    return {"action": "health", "rules": rules}


def cmd_revise(rule_id, workspace, days_cooldown):
    """Mark a rule as revised and set cooldown period."""
    health = load_health(workspace)
    rules = health.setdefault("rules", {})
    rule = rules.get(rule_id)

    if not rule:
        print(f"Rule '{rule_id}' not found in health data.")
        return

    now = datetime.now(CST)
    cooldown_until = (now + timedelta(days=days_cooldown)).isoformat()
    rule["cooldown_until"] = cooldown_until
    rule["recent_violations"] = 0
    rule["status"] = "active"
    rule.setdefault("revision_history", []).append({
        "revised_at": now.isoformat(),
        "cooldown_days": days_cooldown,
        "previous_violations": rule.get("total_violations", 0),
    })

    save_health(workspace, health)
    print(f"[REVISE] {rule_id} marked as revised")
    print(f"  Cooldown: {days_cooldown} days (until {cooldown_until[:10]})")
    print(f"  Recent violations reset to 0")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="memory-guardian violation logger")
    sub = p.add_subparsers(dest="command")

    # log
    log_p = sub.add_parser("log", help="Log a violation event")
    log_p.add_argument("--rule", required=True, help="Rule ID that was violated")
    log_p.add_argument("--event", required=True, help="Description of the violation")
    log_p.add_argument("--context", default="", help="Context of the violation")
    log_p.add_argument("--severity", default="warning", choices=["info", "warning", "error"])
    log_p.add_argument("--workspace", default=DEFAULT_WORKSPACE)

    # check
    check_p = sub.add_parser("check", help="Check rules needing revision")
    check_p.add_argument("--days", type=int, default=7, help="Look back N days")
    check_p.add_argument("--min-count", type=int, default=3, help="Min violations to trigger revision")
    check_p.add_argument("--workspace", default=DEFAULT_WORKSPACE)

    # health
    health_p = sub.add_parser("health", help="Show rule health summary")
    health_p.add_argument("--workspace", default=DEFAULT_WORKSPACE)

    # revise
    revise_p = sub.add_parser("revise", help="Mark rule as revised")
    revise_p.add_argument("--rule", required=True, help="Rule ID")
    revise_p.add_argument("--cooldown-days", type=int, default=14, help="Cooldown period in days")
    revise_p.add_argument("--workspace", default=DEFAULT_WORKSPACE)

    args = p.parse_args()

    if args.command == "log":
        cmd_log(args.rule, args.event, args.context, args.severity, args.workspace)
    elif args.command == "check":
        cmd_check(args.workspace, args.days, args.min_count)
    elif args.command == "health":
        cmd_health(args.workspace)
    elif args.command == "revise":
        cmd_revise(args.rule, args.workspace, args.cooldown_days)
    else:
        p.print_help()
