#!/usr/bin/env python3
"""gmail-cleanup - execute an APPROVED action list via gog (v4).

Approval, dry-run, and send gates are ENFORCED IN CODE, not left to convention:

  1. Dry-run is the default. Nothing is mutated unless `--apply` is passed.
  2. `--apply` is REFUSED unless the spec carries an explicit approval artifact:
         "approval": {"approved": true,
                      "approvedBy": "telegram:<owner-id>",
                      "approvedAt": "<ISO-8601>"}
     (all three fields required; approved must be boolean true).
  3. `send-draft` actions execute only when ALL hold:
         --apply AND --send AND safety.blockAllSends == false
         AND the action itself sets "sendApproved": true.
     Otherwise the send is skipped and recorded.
  4. Per-run cap: limits.maxActionsPerRun (refuse if exceeded).

Credentials: read from the GOG_KEYRING_PASSWORD environment variable ONLY. This
script never reads credential files. The Workspace CLI is invoked as `gog` from
PATH; no executable override is honored.

Every attempt, refusal, and skip is appended to state/gmail-cleanup/audit.log.

Usage: cleanup-execute.py <actions.json> [--apply] [--send]

Action spec:
{
  "account": "you@gmail.com",                         # optional; defaults to config.json
  "approval": {"approved": true,
               "approvedBy": "telegram:123456789",    # REQUIRED for --apply (non-empty)
               "approvedAt": "2026-10-12T01:00:00Z"}, # REQUIRED for --apply (ISO-8601)
  "actions": [
    {"type": "archive",     "id": "<msgId>"},
    {"type": "mark-read",   "id": "<msgId>"},
    {"type": "trash",       "id": "<msgId>"},
    {"type": "draft-reply", "id": "<msgId>", "body": "..."},
    {"type": "send-draft",  "draftId": "<draftId>", "sendApproved": true}
  ]
}
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone

GOG = "gog"
STATE = os.environ.get(
    "GMAIL_CLEANUP_STATE",
    os.path.expanduser("~/.openclaw/workspace/state/gmail-cleanup"),
)
CFG = os.environ.get("GMAIL_CLEANUP_CONFIG", os.path.join(STATE, "config.json"))
RETRIES = int(os.environ.get("GMAIL_CLEANUP_RETRIES", "4"))
RATE_HINTS = (
    "ratelimitexceeded",
    "quota exceeded",
    "too many requests",
    "user-rate limit",
    "429",
)


def now():
    return datetime.now(timezone.utc).isoformat()


if not os.environ.get("GOG_KEYRING_PASSWORD"):
    sys.exit(
        "GOG_KEYRING_PASSWORD is not set. Export it before running; this skill "
        "intentionally does not read credential files itself."
    )

positional = [a for a in sys.argv[1:] if not a.startswith("--")]
apply = "--apply" in sys.argv
send_ok = "--send" in sys.argv
if not positional:
    sys.exit("usage: cleanup-execute.py <actions.json> [--apply] [--send]")

spec = json.load(open(positional[0]))

cfg = json.load(open(CFG)) if os.path.exists(CFG) else {}
safety = cfg.get("safety", {}) or {}
cap = cfg.get("limits", {}).get("maxActionsPerRun", 50)
acc = spec.get("account") or cfg.get("account")

# Hard kill-switch: never send while blockAllSends is true.
if safety.get("blockAllSends", False):
    send_ok = False

os.makedirs(STATE, exist_ok=True)
audit = os.path.join(STATE, "audit.log")


def record(line):
    with open(audit, "a") as f:
        f.write(line + "\n")
    print(line)


def gog(cmd_args, mutate=False, retries=RETRIES):
    base = [GOG, *cmd_args]
    if acc:
        base += ["-a", acc]
    if not mutate:
        base.append("--dry-run")
    delay = 2.0
    r = None
    for attempt in range(retries + 1):
        r = subprocess.run(base, capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip()
        if r.returncode == 0 or not any(h in out.lower() for h in RATE_HINTS):
            return r.returncode, out
        if attempt < retries:
            time.sleep(delay)
            delay = min(delay * 2, 30)
    return r.returncode, (r.stdout + r.stderr).strip()


# --- enforced approval gate -------------------------------------------------
approval = spec.get("approval") or {}
approval_ok = (
    isinstance(approval, dict)
    and approval.get("approved") is True
    and isinstance(approval.get("approvedBy"), str)
    and approval["approvedBy"].strip() != ""
    and isinstance(approval.get("approvedAt"), str)
    and approval["approvedAt"].strip() != ""
)

actions = spec.get("actions") or []
if not isinstance(actions, list):
    sys.exit("invalid spec: 'actions' must be a list")

if apply and not approval_ok:
    record(f"{now()} REFUSED apply 'no-approval-artifact' actions={len(actions)}")
    sys.exit(
        "refusing --apply: spec is missing a valid approval artifact "
        "(approval.approved=true, approval.approvedBy, approval.approvedAt)"
    )

if len(actions) > cap:
    record(f"{now()} REFUSED apply 'over-cap' actions={len(actions)} cap={cap}")
    sys.exit(f"refusing: {len(actions)} actions exceeds limits.maxActionsPerRun={cap}")

# --- execute ----------------------------------------------------------------
mode = "APPLY" if apply else "DRYRUN"
by = approval.get("approvedBy", "-") if approval_ok else "-"
record(f"{now()} {mode} start actions={len(actions)} by={by} send={send_ok}")

for a in actions:
    if not isinstance(a, dict):
        record(f"{now()} {mode} skip malformed-action")
        continue
    t = a.get("type")
    ref = a.get("id") or a.get("draftId")

    if t == "send-draft":
        if not (apply and send_ok and a.get("sendApproved") is True):
            record(f"{now()} {mode} SKIP send-draft {ref} reason=send-gate")
            continue
        rc, out = gog(["gmail", "drafts", "send", a["draftId"]], mutate=True)
    elif t == "draft-reply":
        rc, out = gog(
            ["gmail", "drafts", "reply", a["id"], "--body", a.get("body", "")],
            mutate=apply,
        )
    elif t in ("archive", "mark-read", "trash"):
        rc, out = gog(["gmail", t, a["id"]], mutate=apply)
    else:
        rc, out = 1, f"unknown action type: {t}"

    record(f"{now()} {mode} {t} {ref} rc={rc} {out[:300]}")

record(f"{now()} {mode} done")
