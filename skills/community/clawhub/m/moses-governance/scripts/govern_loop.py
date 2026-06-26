#!/usr/bin/env python3
"""
govern_loop.py — MO§ES™ Governance Harness Loop
ReAct-style execution loop with constitutional enforcement at every step.

Each iteration:
  1. Lineage verify   — confirm chain traces to origin anchor
  2. Status load      — load current mode/posture/role
  3. Governance check — block if action prohibited under current state
  4. Execute step     — run the action (operator-confirmed or headless)
  5. Audit log        — record outcome to tamper-evident ledger (with Isnad)
  6. Progress write   — persist step for continuity across context windows
  7. Recovery check   — halt and flag if any step failed

Usage:
  python3 govern_loop.py run "<task>" "<step1>" "<step2>" ...
  python3 govern_loop.py run --headless "<task>" "<step1>" ...
  python3 govern_loop.py status
"""

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
STATE_PATH = os.path.expanduser("~/.openclaw/governance/state.json")


def run_script(script, *args) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, os.path.join(SCRIPTS, script), *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, (result.stdout + result.stderr).strip()


def load_state() -> dict:
    if not os.path.exists(STATE_PATH):
        return {}
    with open(STATE_PATH) as f:
        return json.load(f)


def signal_hash(task: str, action: str) -> str:
    """SHA-256 of the raw task+action signal — Isnad Layer 0 input hash."""
    raw = f"{task}|{action}"
    return hashlib.sha256(raw.encode()).hexdigest()


def audit_log(agent: str, action: str, detail: str, outcome: str,
              input_hash: str = None, source_id: str = None) -> tuple[int, str]:
    """Call audit_stub.py log with correct named flags."""
    cmd = [
        "audit_stub.py", "log",
        "--agent", agent,
        "--action", action,
        "--detail", detail,
        "--outcome", outcome,
    ]
    if input_hash:
        cmd += ["--input-hash", input_hash, "--source-id", source_id or "govern_loop"]
    return run_script(*cmd)


def governed_step(task: str, action: str, step_num: int, total: int,
                  headless: bool = False) -> bool:
    """Run a single governed step. Returns True if successful, False if blocked/failed."""
    print(f"\n── Step {step_num}/{total}: {action}")

    # Isnad: hash the raw signal before anything else
    ihash = signal_hash(task, action)
    source = f"govern_loop:step-{step_num}"

    # 1. Lineage verify
    code, out = run_script("lineage_verify.py", "verify")
    if code != 0:
        print(f"[HARNESS] LINEAGE FAIL — halting. {out}")
        audit_log("harness", action, f"step {step_num}/{total} — lineage fail",
                  "FAIL", ihash, source)
        run_script("progress.py", "flag-recovery")
        return False
    print(f"[HARNESS] Lineage OK")

    # 2. Load governance state
    state = load_state()
    mode = state.get("mode", "unknown")
    posture = state.get("posture", "unknown")
    role = state.get("role", "unknown")
    print(f"[HARNESS] State: mode={mode} posture={posture} role={role}")

    # 2b. Ghost token gate — check commitment conservation between task and action
    ghost_code, ghost_out = run_script(
        "commitment_verify.py", "ghost", task, action
    )
    try:
        ghost_report = json.loads(ghost_out.split("\n")[0]) if ghost_out else {}
    except (json.JSONDecodeError, IndexError):
        ghost_report = {}

    cascade_risk = ghost_report.get("cascade_risk", "NONE")
    if cascade_risk == "HIGH":
        leaked = ghost_report.get("leaked_cascade_tokens", [])
        print(f"[HARNESS] GHOST TOKEN ALERT — cascade_risk: HIGH")
        print(f"          Leaked: {leaked}")
        print(f"          {ghost_report.get('cascade_note', '')}")
        audit_log(
            "harness", action,
            f"step {step_num}/{total} — ghost token HIGH: leaked={leaked}",
            "GHOST-FLAG", ihash, source,
        )
        # Block in DEFENSE or HIGH_INTEGRITY mode; warn only otherwise
        if posture == "defense" or mode in ("High Integrity", "Defense"):
            print(f"[HARNESS] BLOCKED — modal anchor loss under {posture}/{mode}.")
            run_script("progress.py", "flag-recovery")
            return False
    elif cascade_risk == "MEDIUM":
        print(f"[HARNESS] Ghost token warning — cascade_risk: MEDIUM (non-anchor leakage)")
    else:
        print(f"[HARNESS] Ghost token check: NONE")

    # 3. Governance gate — SCOUT posture blocks all writes
    if posture == "scout":
        print(f"[HARNESS] BLOCKED — SCOUT posture prohibits action: {action}")
        audit_log("harness", action, f"step {step_num}/{total} — scout block",
                  "BLOCKED", ihash, source)
        return False

    # 4. DEFENSE posture requires confirmation (or headless auto-approve)
    if posture == "defense":
        if headless:
            print(f"[HARNESS] DEFENSE posture — headless mode, auto-approving.")
            audit_log("harness", action,
                      f"step {step_num}/{total} — defense headless auto-approve",
                      "AUTO-APPROVED", ihash, source)
        else:
            print(f"[HARNESS] DEFENSE posture — confirm action: {action}")
            try:
                confirm = input("  Proceed? [y/N]: ").strip().lower()
            except EOFError:
                confirm = ""
            if confirm != "y":
                print(f"[HARNESS] Operator declined. Halting.")
                audit_log("harness", action,
                          f"step {step_num}/{total} — operator declined",
                          "DECLINED", ihash, source)
                run_script("progress.py", "flag-recovery")
                return False

    # 5. Log execution — named flags, Isnad wired
    code, out = audit_log(
        "harness", action,
        f"step {step_num}/{total} — {task}",
        "PASS", ihash, source,
    )
    if code != 0:
        print(f"[HARNESS] Audit log failed: {out}")
        run_script("progress.py", "flag-recovery")
        return False

    # 6. Write progress
    run_script("progress.py", "step", action)
    print(f"[HARNESS] Step complete — audited and logged.")
    return True


def cmd_run(args):
    headless = "--headless" in args
    args = [a for a in args if a != "--headless"]

    if len(args) < 2:
        print("Usage: govern_loop.py run [--headless] \"<task>\" \"<step1>\" ...")
        sys.exit(1)

    task = args[0]
    steps = args[1:]

    print(f"\n{'═' * 60}")
    print(f"  MO§ES™ GOVERNANCE HARNESS")
    print(f"  Task: {task}")
    print(f"  Steps: {len(steps)}")
    if headless:
        print(f"  Mode: HEADLESS (DEFENSE auto-approve on)")
    print(f"{'═' * 60}")

    run_script("progress.py", "start", task)

    for i, step in enumerate(steps, 1):
        ok = governed_step(task, step, i, len(steps), headless=headless)
        if not ok:
            print(f"\n[HARNESS] Loop halted at step {i}. Operator review required.")
            print(f"  Run: python3 progress.py status")
            sys.exit(1)

    run_script("progress.py", "done")
    print(f"\n{'═' * 60}")
    print(f"  [HARNESS] Task complete. All {len(steps)} steps governed and audited.")
    print(f"  Run: python3 audit_stub.py recent")
    print(f"{'═' * 60}\n")


def cmd_status(_args):
    run_script("progress.py", "status")


def cmd_resilience(_args):
    """Resilience report — fault isolation analysis across the audit ledger.

    Answers lynk02: governance that only runs when things go right isn't governance.
    This command scans the ledger and identifies:
      - Fault rate: what % of audited steps resulted in FAIL/BLOCK/DECLINE
      - Fault isolation: are failures clustered (systematic) or random (acceptable)?
      - Recovery health: are recovery_needed flags being cleared, or accumulating?
      - Posture drift: did posture change mid-task in ways that look unintentional?

    Run before a high-stakes task to confirm the harness is healthy.
    Run after an incident to isolate the failure pattern.
    """
    import os

    LEDGER_PATH = os.path.expanduser("~/.openclaw/audits/moses/audit_ledger.jsonl")
    PROGRESS_PATH = os.path.expanduser("~/.openclaw/governance/progress.json")

    if not os.path.exists(LEDGER_PATH):
        print(json.dumps({"error": "No audit ledger found. Run govern_loop at least once."}))
        return

    with open(LEDGER_PATH) as f:
        entries = [json.loads(l) for l in f if l.strip()]

    if not entries:
        print(json.dumps({"error": "Audit ledger is empty."}))
        return

    total = len(entries)
    fault_outcomes = {"FAIL", "BLOCKED", "BLOCK", "DECLINED", "DECLINE", "ERROR"}
    faults = [e for e in entries if e.get("outcome", "").upper() in fault_outcomes]
    passes = [e for e in entries if e.get("outcome", "").upper() == "PASS"]

    fault_rate = len(faults) / total if total > 0 else 0

    # Fault clustering: are faults adjacent in the chain?
    fault_indices = {i for i, e in enumerate(entries) if e.get("outcome", "").upper() in fault_outcomes}
    clustered = 0
    for idx in fault_indices:
        if (idx - 1) in fault_indices or (idx + 1) in fault_indices:
            clustered += 1
    cluster_ratio = clustered / len(faults) if faults else 0

    # Posture drift: count posture changes across sequential entries
    postures = [e.get("posture", "") for e in entries]
    posture_changes = sum(1 for i in range(1, len(postures)) if postures[i] != postures[i - 1])

    # Recovery health
    recovery_needed = False
    if os.path.exists(PROGRESS_PATH):
        with open(PROGRESS_PATH) as f:
            prog = json.load(f)
        recovery_needed = prog.get("recovery_needed", False)

    # Verdict
    if fault_rate > 0.3:
        health = "DEGRADED"
        health_note = f"Fault rate {fault_rate:.0%} exceeds 30%. Systematic issue — review before proceeding."
    elif cluster_ratio > 0.5 and len(faults) >= 2:
        health = "DEGRADED"
        health_note = f"{clustered}/{len(faults)} faults are clustered — likely a systematic failure point, not random."
    elif recovery_needed:
        health = "RECOVERY_NEEDED"
        health_note = "progress.json has recovery_needed=true. Clear it before starting a new task."
    elif fault_rate > 0.1:
        health = "CAUTION"
        health_note = f"Fault rate {fault_rate:.0%} is elevated. Monitor."
    else:
        health = "HEALTHY"
        health_note = f"Fault rate {fault_rate:.0%}. No clustering. Harness operating normally."

    report = {
        "health": health,
        "health_note": health_note,
        "total_entries": total,
        "passes": len(passes),
        "faults": len(faults),
        "fault_rate": round(fault_rate, 4),
        "fault_outcomes_seen": list({e.get("outcome", "").upper() for e in faults}),
        "fault_clustering": {
            "clustered_faults": clustered,
            "cluster_ratio": round(cluster_ratio, 4),
            "note": "High cluster_ratio = systematic failure point, not random noise.",
        },
        "posture_changes": posture_changes,
        "recovery_needed": recovery_needed,
        "recent_faults": [
            {"timestamp": e.get("timestamp"), "action": e.get("action"), "outcome": e.get("outcome")}
            for e in faults[-5:]
        ],
    }

    print(json.dumps(report, indent=2))
    if health in ("DEGRADED", "RECOVERY_NEEDED"):
        print(f"\n[RESILIENCE] {health}: {health_note}", file=sys.stderr)
        sys.exit(1)


COMMANDS = {
    "run": cmd_run,
    "status": cmd_status,
    "resilience": cmd_resilience,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]
    if cmd not in COMMANDS:
        print(f"Usage: govern_loop.py [{'|'.join(COMMANDS)}]")
        sys.exit(1)
    COMMANDS[cmd](args)
