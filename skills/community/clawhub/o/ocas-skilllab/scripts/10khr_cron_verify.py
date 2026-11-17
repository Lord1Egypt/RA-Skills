#!/usr/bin/env python3
"""
10khr_cron_verify.py — cron-safe eligibility + 5-dimension on-disk verification harness.

WHY this exists: the 10khr grind's biggest trap is the over-scoring heuristic.
A heuristic "49/50" is almost never a real defect — it is the D3 451-500 line
proxy, the D8 ref-count trap, or (observed 2026-07-19) a D5 `- [ ]` checklist
that legitimately lives in a referenced support file, NOT the main SKILL.md.
Grinding these spins a perpetual loop. This script lets a cron pass answer
deterministically: which below-50 targets are REAL gaps to fix, vs over-scoring
traps to skip?

Cron-safe by design:
  * Does NOT call save_state() — preserves the skip-rule's last_run. Running
    `--report-only` would advance last_run and make every skill look "modified",
    defeating the skip rule (state-write pitfall, 2026-07-18).
  * Reads last_run from the runner's REAL STATE_FILE (the ocas-critique path),
    not the stale ocas-skilllab copy (state-file split-brain pitfall).
  * Pure verification — never writes to skills. Genuine D9 gaps are fixed by
    hand-injecting the canonical --help guard documented in SKILL.md Pitfalls.

Usage:
  python3 scripts/10khr_cron_verify.py
"""
import importlib.util
import os
import sys
import subprocess
from datetime import datetime, timezone

# OUTBOUND_SKIP: never run --help on a script that can post/send/trade. An audit
# doing exactly that published "--help" to a live Bluesky account three times.
import re as _re
_OUTBOUND_SKIP = _re.compile(
    r"createRecord|app\.bsky\.feed|com\.atproto|/xrpc/|post\.sh|smtplib"
    r"|requests\.(post|put|patch|delete)|api\.telegram\.org|submit_order|alpaca"
    r"|curl\s+(-[A-Za-z]+\s+)*-X\s*[\"']?(POST|PUT|PATCH|DELETE)", _re.I)


def _can_send(path):
    try:
        return bool(_OUTBOUND_SKIP.search(open(path, encoding="utf-8", errors="ignore").read()))
    except OSError:
        return False



def _runner_path():
    hermes_root = os.environ.get("HERMES_ROOT", os.path.expanduser("~/.hermes"))
    return os.path.join(
        hermes_root, "profiles", "indigo", "skills",
        "ocas-skilllab", "scripts", "critique_10khr_runner.py",
    )


def load_runner():
    spec = importlib.util.spec_from_file_location("runner", _runner_path())
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ondisk_check(skill_name, skill_path, runner):
    """5-dimension ON-DISK verification (ignores the over-scoring heuristic)."""
    d = os.path.dirname(skill_path)
    try:
        content = open(skill_path).read()
    except Exception as e:
        return {"ERROR": f"cannot read SKILL.md: {e}"}
    out = {}

    # D1: frontmatter category
    try:
        import yaml
        fm = yaml.safe_load(content.split("---")[1]) or {}
        cat = fm.get("metadata", {}).get("hermes", {}).get("category")
        out["D1"] = "OK" if cat else "MISSING category"
    except Exception as e:
        out["D1"] = f"YAML ERR {e}"

    # D3: code ratio + line count (line count tells us if it's the 451-500 proxy)
    rc_path = os.path.join(os.path.dirname(_runner_path()), "critique_code_ratio.py")
    try:
        r = subprocess.run([sys.executable, rc_path, skill_path],
                           capture_output=True, text=True, timeout=60)
        out["D3"] = (r.stdout.strip().splitlines()[-1] if r.stdout.strip()
                     else r.stderr.strip())
    except Exception as e:
        out["D3"] = f"ERR {e}"
    out["wc_lines"] = len(content.split("\n"))

    # D5: checklist — search the WHOLE skill dir (main + references/), because
    # a `- [ ]` quality checklist may legitimately live in a referenced file.
    has_cb = "- [ ]" in content
    if not has_cb:
        for root, _, files in os.walk(d):
            if ".archive" in root:
                continue
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                try:
                    if "- [ ]" in open(os.path.join(root, fn)).read():
                        has_cb = True
                        break
                except Exception:
                    continue
            if has_cb:
                break
    out["D5"] = "OK" if has_cb else "NO checklist (main or refs)"

    # D9: every script --help must exit 0
    sd = os.path.join(d, "scripts")
    if os.path.isdir(sd):
        miss = []
        for s in [f for f in os.listdir(sd) if f.endswith((".py", ".sh"))]:
            sp = os.path.join(sd, s)
            try:
                if s.endswith(".py"):
                    if _can_send(str(sp)):
                        continue  # outbound: do not execute
                    rc = subprocess.run([sys.executable, sp, "--help"], input="",
                                        capture_output=True, text=True, timeout=30).returncode
                else:
                    if _can_send(str(sp)):
                        continue  # outbound: do not execute
                    rc = subprocess.run(["bash", sp, "--help"], input="",
                                        capture_output=True, text=True, timeout=30).returncode
            except Exception:
                rc = -1
            if rc != 0:
                miss.append((s, rc))
        out["D9"] = "OK (all exit 0)" if not miss else f"MISSING --help: {miss}"
    else:
        out["D9"] = "N/A (no scripts)"
    return out


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Cron-safe 10khr eligibility plus on-disk 5-dimension "
                    "verification harness. Assesses all ocas/util skills, applies "
                    "the skip-rule against the runner STATE_FILE, and prints real "
                    "gaps vs over-scoring traps. No state mutation.")
    parser.parse_args()
    runner = load_runner()
    state = runner.load_state()
    last_run = (datetime.fromisoformat(state["last_run"])
                if state.get("last_run") else datetime.min.replace(tzinfo=timezone.utc))
    assessment = runner.run_full_assessment()
    below = [r for r in assessment if r["total"] < runner.TARGET_SCORE]
    print(f"Total assessed: {len(assessment)} | below 50/50: {len(below)} | last_run: {state.get('last_run')}")

    rows = []
    for r in below:
        p = r["path"]
        mtime = datetime.fromtimestamp(os.stat(p).st_mtime, timezone.utc)
        eligible = (mtime > last_run) or (r["total"] < 44)
        rows.append((r["total"], r["skill"], p, eligible, mtime.isoformat()))
    rows.sort(key=lambda x: (x[0], 0 if x[3] else 1))

    for sc, name, p, elig, mt in rows:
        if not elig:
            continue
        chk = ondisk_check(name, p, runner)
        print(f"\n### {name}  (heuristic {sc}/50, mtime {mt})")
        for k, v in chk.items():
            print(f"  {k}: {v}")
        real_gap = any(str(v).startswith(("MISSING", "NO ", "YAML ERR", "ERR "))
                      for k, v in chk.items())
        print(f"  >> {'REAL GAP — grind it' if real_gap else 'OVER-SCORING TRAP — skip'}")

    print("\n(Skipped: below-50 skills unmodified since last_run AND heuristic>=44 "
          "— these are over-scoring traps; do NOT re-grind them.)")


if __name__ == "__main__":
    main()