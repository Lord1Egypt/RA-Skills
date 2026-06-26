#!/usr/bin/env python3
"""Dev executor for pm-dev-orchestrator.

Purpose:
- Run on the DEV OpenClaw server.
- Watch a single Telegram group for commands that start with "DEV ".
- Only accept commands authored by PM_FROM_ID.
- Execute allowlisted operations:
  - clawhub install/update/search
  - openclaw cron add/update/remove/run/list
- Reply back into the same group via OpenClaw (by printing instructions for the operator).

IMPORTANT:
This script intentionally does NOT auto-send messages via provider APIs directly.
It runs local `openclaw` / `clawhub` commands and prints a short result.
Hooking its output back into Telegram should be done by running it inside an OpenClaw agent session
or by a small wrapper that posts the output.

This is a scaffold: it parses commands and executes local CLIs.
"""

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass


ALLOW_SKILL_CMDS = {"install", "update", "search", "list"}
ALLOW_CRON_CMDS = {"list", "add", "enable", "remove", "run"}


def run(cmd: list[str], cwd: str | None = None) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    out = (p.stdout or "").strip()
    return p.returncode, out


def ensure_workspace() -> str:
    # Default OpenClaw workspace
    ws = os.environ.get("OPENCLAW_WORKSPACE") or os.path.expanduser("~/.openclaw/workspace")
    return ws


def handle_skill(args: list[str]) -> tuple[bool, str]:
    if not args:
        return False, "ERR: missing skill subcommand"
    sub = args[0]
    if sub not in ALLOW_SKILL_CMDS:
        return False, f"ERR: skill subcommand not allowed: {sub}"

    ws = ensure_workspace()

    if sub == "list":
        # List local skills folder
        skills_dir = os.path.join(ws, "skills")
        try:
            entries = sorted([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])
        except FileNotFoundError:
            entries = []
        return True, "OK skills: " + (", ".join(entries) if entries else "(none)")

    if len(args) < 2:
        return False, f"ERR: missing slug for skill {sub}"
    slug = args[1]

    # Use clawhub CLI
    if sub == "install":
        cmd = ["clawhub", "install", slug, "--dir", os.path.join(ws, "skills")]
    elif sub == "update":
        cmd = ["clawhub", "update", slug]
    else:  # search
        query = " ".join(args[1:])
        cmd = ["clawhub", "search", query]

    rc, out = run(cmd, cwd=ws)
    if rc != 0:
        return False, f"ERR: {sub} failed ({rc}): {out[-800:]}"
    # keep response short
    return True, f"OK: {sub} {slug if sub != 'search' else ''} {out[-800:]}".strip()


def parse_kv(s: str) -> dict:
    # Parse key=value pairs with quotes using shlex
    lex = shlex.shlex(s, posix=True)
    lex.whitespace_split = True
    tokens = list(lex)
    d = {}
    for t in tokens:
        if "=" not in t:
            continue
        k, v = t.split("=", 1)
        d[k.strip()] = v.strip()
    return d


def handle_cron(args: list[str]) -> tuple[bool, str]:
    if not args:
        return False, "ERR: missing cron subcommand"
    sub = args[0]
    if sub not in ALLOW_CRON_CMDS:
        return False, f"ERR: cron subcommand not allowed: {sub}"

    ws = ensure_workspace()

    if sub == "list":
        rc, out = run(["openclaw", "cron", "list"], cwd=ws)
        return (rc == 0), ("OK\n" + out[-1200:]) if rc == 0 else ("ERR: " + out[-1200:])

    # Everything else uses key=value args
    kv = parse_kv(" ".join(args[1:]))

    if sub == "enable":
        job_id = kv.get("id")
        on = kv.get("on")
        if not job_id or on not in ("on", "off"):
            return False, "ERR: usage DEV cron enable id=<jobId> on=on|off"
        patch = json.dumps({"enabled": (on == "on")})
        rc, out = run(["openclaw", "cron", "update", "--id", job_id, "--patch", patch], cwd=ws)
        return (rc == 0), ("OK " + out[-800:]) if rc == 0 else ("ERR " + out[-800:])

    if sub == "remove":
        job_id = kv.get("id")
        if not job_id:
            return False, "ERR: usage DEV cron remove id=<jobId>"
        rc, out = run(["openclaw", "cron", "remove", "--id", job_id], cwd=ws)
        return (rc == 0), ("OK " + out[-800:]) if rc == 0 else ("ERR " + out[-800:])

    if sub == "run":
        job_id = kv.get("id")
        if not job_id:
            return False, "ERR: usage DEV cron run id=<jobId>"
        rc, out = run(["openclaw", "cron", "run", "--id", job_id], cwd=ws)
        return (rc == 0), ("OK " + out[-800:]) if rc == 0 else ("ERR " + out[-800:])

    if sub == "add":
        name = kv.get("name") or "dev-cron"
        message = kv.get("message")
        if not message:
            return False, "ERR: cron add requires message=\"...\""

        # schedule
        every = kv.get("every")
        cron_expr = kv.get("cron")
        if not every and not cron_expr:
            return False, "ERR: cron add requires every=10m or cron=\"*/5 * * * *\""

        # Translate every=10m to ms
        schedule = None
        if every:
            m = re.fullmatch(r"(\d+)([smhd])", every)
            if not m:
                return False, "ERR: every must match <num><s|m|h|d> e.g. 10m"
            n = int(m.group(1))
            unit = m.group(2)
            mult = {"s": 1000, "m": 60_000, "h": 3_600_000, "d": 86_400_000}[unit]
            schedule = {"kind": "every", "everyMs": n * mult}
        else:
            schedule = {"kind": "cron", "expr": cron_expr}

        job = {
            "name": name,
            "sessionTarget": "isolated",
            "enabled": True,
            "schedule": schedule,
            "payload": {
                "kind": "agentTurn",
                "timeoutSeconds": 240,
                "message": message,
            },
            "delivery": {"mode": "none"},
        }

        # Use openclaw cron add via stdin json (if supported) else via temp file.
        # We'll write a temp file.
        tmp = os.path.join(ws, "tmp-cron-job.json")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(job, f)
        rc, out = run(["openclaw", "cron", "add", "--file", tmp], cwd=ws)
        try:
            os.remove(tmp)
        except OSError:
            pass
        return (rc == 0), ("OK " + out[-1200:]) if rc == 0 else ("ERR " + out[-1200:])

    return False, "ERR: unreachable"


def handle_line(line: str) -> tuple[bool, str]:
    line = line.strip()
    if not line.startswith("DEV "):
        return False, "SKIP"
    parts = shlex.split(line)
    # parts[0] = DEV
    if len(parts) < 2:
        return False, "ERR: missing command"
    cmd = parts[1]
    rest = parts[2:]

    if cmd == "skill":
        return handle_skill(rest)
    if cmd == "cron":
        return handle_cron(rest)

    return False, f"ERR: unknown command: {cmd}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--group", required=True, help="Allowed Telegram group chat id")
    ap.add_argument("--pm-from", required=True, help="Allowed PM bot numeric from.id")
    ap.add_argument("--stdin", action="store_true", help="Read commands from stdin (for testing)")
    args = ap.parse_args()

    if args.stdin:
        for line in sys.stdin:
            ok, msg = handle_line(line)
            if msg != "SKIP":
                print(msg)
        return

    print(
        "This script is a scaffold. Run with --stdin for parsing tests, or integrate with a Telegram update feed.\n"
        "Expected deployment: a Dev OpenClaw bot receives group messages and forwards the text lines here.\n"
        f"Allowed group: {args.group} | Allowed pm from.id: {args.pm_from}\n"
    )


if __name__ == "__main__":
    main()
