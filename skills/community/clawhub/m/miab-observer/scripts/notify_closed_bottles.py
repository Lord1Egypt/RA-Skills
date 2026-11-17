#!/usr/bin/env python3
"""
notify_closed_bottles — deterministic end-state notifier for the MIAB callback ledger.

Watches the append-only callback ledger (state/callbacks/ledger.jsonl, owned by
claw-callback.py) for events that mean a bottle has reached an END STATE:
`resolve`, `cancel`, or `fail`. For each one, it reconstructs that bottle's full
MIAB history from the ledger (every line whose `id` matches, in order) and posts
it as a single Discord message via `openclaw message send`.

Deliberately NOT an agentTurn / reactive cron hook. Per
docs/specs/miab-messaging-dedup-and-cron-sequencing.md (the incident that
produced the July 2026 double-posting/typo'd-channel bug), any LLM turn put in
the send path is the thing that produces duplicate or mistargeted delivery.
This script is pure stdlib + one subprocess call to a fixed CLI with a fixed
delivery target; run it from a `--command` (non-agent) cron job, never an agentTurn.

Read-only over the ledger: never mutates ledger.jsonl or envelope files. The
only files it writes are its own state file (cursor + toggle).

Path resolution (mirrors miab_observer.py's conventions):
  - CLAW_HOME              : broker root                 (default: ~/.openclaw)
  - CLAW_LEDGER            : explicit ledger path         (overrides CLAW_HOME/state/callbacks/ledger.jsonl)
  - CLAW_CLOSED_STATE      : explicit state-file path     (overrides CLAW_HOME/state/callbacks/closed_bottle_state.json)
  - CLAW_CLOSED_TARGET     : delivery target for `message send --target` (REQUIRED; no
                             default — commands that can deliver fail closed when it is unset)
  - CLAW_CLOSED_ACCOUNT    : optional --account for `message send`
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

END_EVENTS = {"resolve", "cancel", "fail"}

# --------------------------------------------------------------------------- paths
def claw_home() -> Path:
    return Path(os.environ.get("CLAW_HOME", "~/.openclaw")).expanduser()

def ledger_file() -> Path:
    env = os.environ.get("CLAW_LEDGER")
    if env:
        return Path(env).expanduser()
    return claw_home() / "state" / "callbacks" / "ledger.jsonl"

def state_file() -> Path:
    env = os.environ.get("CLAW_CLOSED_STATE")
    if env:
        return Path(env).expanduser()
    return claw_home() / "state" / "callbacks" / "closed_bottle_state.json"

def target_channel_or_none() -> str | None:
    """The configured delivery target, or None. For introspection only — never
    use this to build a send command."""
    t = os.environ.get("CLAW_CLOSED_TARGET", "").strip()
    return t or None

def target_channel() -> str:
    """The delivery target, or fail closed. There is deliberately no default:
    a hardcoded channel id is both a secret in committed text and a way to
    mistarget delivery on a host that never configured this notifier."""
    t = target_channel_or_none()
    if t is None:
        print(json.dumps({"ok": False,
                          "error": "CLAW_CLOSED_TARGET is unset; refusing to deliver",
                          "next_step": "export CLAW_CLOSED_TARGET=channel:<id> (or the target accepted by `openclaw message send --target`) and re-run"}),
              file=sys.stderr)
        sys.exit(1)
    return t

def account_id() -> str | None:
    return os.environ.get("CLAW_CLOSED_ACCOUNT")

# --------------------------------------------------------------- agent identity map
AGENT_MAP = {
    "main": "✨ LYRA (Main)",
    "planner": "🥷⚔️ SPECTRE (Planner)",
    "coder": "💥 Cinder (Coder)",
    "reviewer": "🥷👁️ ECHO (Reviewer)",
    "debug": "🔬 Zero (Debug)",
    "utility": "🛠️ Swift (Utility)",
    "sigma": "⚡ SIGMA (Portfolio)",
    "free": "🌌 VOID (Scout)",
    "sweep": "🧹 Callback Reaper",
    "system": "⚙️ System",
}

def who(name):
    return AGENT_MAP.get(name, name or "Unknown")

# Model running behind each agent — primary + fallback chain (mirrors
# agents.list[].model in openclaw.json). Keys are the bare agent ids used in
# ledger 'by'/'to'/'wake' fields.
MODEL_MAP = {
    "main": {"primary": "deepseek-v4-flash", "fallbacks": ["gemini-3-flash-preview", "deepseek-v4-pro", "claude-sonnet-5", "gemini-3.6-flash", "gpt-5.6-terra"]},
    "planner": {"primary": "claude-sonnet-5", "fallbacks": ["gpt-5.6-terra", "gemini-3.6-flash", "deepseek-v4-pro"]},
    "coder": {"primary": "gpt-5.6-terra", "fallbacks": ["claude-sonnet-5", "deepseek-v4-flash", "gemini-3.6-flash"]},
    "reviewer": {"primary": "claude-opus-latest", "fallbacks": ["claude-opus-5", "gemini-3.6-flash", "gpt-5.6-terra", "deepseek-v4-pro"]},
    "debug": {"primary": "gemini-3.6-flash", "fallbacks": ["deepseek-v4-flash", "claude-sonnet-5", "gpt-5.6-terra"]},
    "utility": {"primary": "ling-3.0-flash:free", "fallbacks": ["gemini-3.5-flash-lite", "claude-haiku-latest", "deepseek-v4-flash"]},
    "sigma": {"primary": "claude-sonnet-5", "fallbacks": ["claude-opus-5", "gpt-5.6-terra", "gemini-3.6-flash"]},
    "free": {"primary": "ling-3.0-flash:free", "fallbacks": ["nemotron-3-ultra-550b:free", "laguna-s-2.1:free"]},
    "local": {"primary": "local-qwen3.5-4b", "fallbacks": ["ling-3.0-flash:free"]},
}


def who_model(name, short=True):
    """Compact '<model>' tag for an agent id. short=True -> just primary.
    short=False -> 'primary → fb1, fb2' (full chain). Empty if unknown."""
    info = MODEL_MAP.get(name)
    if not info:
        return ""
    if short:
        return info["primary"]
    fbs = info.get("fallbacks") or []
    if not fbs:
        return info["primary"]
    return f"{info['primary']} → {', '.join(fbs)}"

END_ICON = {"resolve": "✅", "cancel": "❌", "fail": "⚠️"}
END_LABEL = {"resolve": "Resolved", "cancel": "Cancelled", "fail": "Failed/Reaped"}

# --------------------------------------------------------------------------- state
def load_state() -> dict:
    p = state_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"enabled": True, "last_processed_line": 0}

def save_state(state: dict) -> None:
    p = state_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(p)

# ----------------------------------------------------------------- summarization
def sanitize(text, limit=500):
    if not text:
        return ""
    lines = [l.strip() for l in str(text).split("\n") if l.strip()]
    cleaned = " ".join(" ".join(lines).split())
    if len(cleaned) > limit:
        return cleaned[: limit - 3] + "..."
    return cleaned

# ----------------------------------------------------------------- history render
def render_step(rec):
    """One ledger record for a bottle -> one short history line."""
    event = rec.get("event")
    by = who(rec.get("by"))
    bym = who_model(rec.get("by"))
    tag = f" [{bym}]" if bym else ""
    if event == "create":
        to = who(rec.get("to"))
        tom = who_model(rec.get("to"))
        totag = f" [{tom}]" if tom else ""
        return f"📥 created by {by}{tag} -> {to}{totag}"
    if event == "forward":
        to = who(rec.get("to"))
        tom = who_model(rec.get("to"))
        totag = f" [{tom}]" if tom else ""
        return f"➡️ forwarded by {by}{tag} -> {to}{totag}"
    if event == "return":
        return f"↩️ returned by {by}{tag}, waking {who(rec.get('wake'))}"
    if event == "resolve":
        return f"✅ resolved by {by}{tag}"
    if event == "cancel":
        return f"❌ cancelled by {by}{tag}" + (f" ({rec.get('reason')})" if rec.get("reason") else "")
    if event == "fail":
        return f"⚠️ failed/reaped by {by}{tag}" + (f" ({rec.get('reason')})" if rec.get("reason") else "")
    if event == "corrupt":
        return f"🗑️ quarantined ({rec.get('reason', 'corrupt envelope')})"
    return f"{event} by {by}{tag}"

def load_all_lines():
    lf = ledger_file()
    if not lf.exists():
        return []
    with lf.open("r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def format_closed_bottle(cid: str, all_records: list, end_rec: dict) -> str:
    """Build the full-history report message for one just-closed bottle."""
    bottle_records = [r for r in all_records if r.get("id") == cid]
    create_rec = next((r for r in bottle_records if r.get("event") == "create"), None)
    task = sanitize(end_rec.get("task") or (create_rec or {}).get("task", ""), limit=300)
    end_event = end_rec.get("event")
    icon = END_ICON.get(end_event, "🔔")
    label = END_LABEL.get(end_event, end_event)

    lines = [f"{icon} [MIAB Bottle {label}] {cid}"]
    if task:
        lines.append(f"   Task: {task}")
    if end_event == "resolve" and end_rec.get("result"):
        lines.append(f"   Result: {sanitize(end_rec.get('result'), limit=400)}")
    if end_event == "cancel" and end_rec.get("reason"):
        lines.append(f"   Reason: {end_rec.get('reason')}")
    if end_event == "fail" and end_rec.get("reason"):
        lines.append(f"   Reason: {end_rec.get('reason')}")
    lines.append(f"   Hops: {len(bottle_records)}")
    lines.append("   History:")
    for r in bottle_records:
        lines.append(f"     - {render_step(r)}")
    return "\n".join(lines)

# ----------------------------------------------------------------- collection
def find_end_record(cid: str) -> dict | None:
    """Locate the ledger's end-state record (resolve/cancel/fail) for one bottle."""
    for l in load_all_lines():
        try:
            rec = json.loads(l)
        except Exception:
            continue
        if rec.get("id") == cid and rec.get("event") in END_EVENTS:
            return rec
    return None


def render_bottle(cid: str) -> tuple[str | None, str]:
    """Deterministic output for ONE closed bottle. Returns (message, status)."""
    end_rec = find_end_record(cid)
    if end_rec is None:
        return None, f"No end-state (resolve/cancel/fail) event found for bottle {cid}."
    all_records = []
    for l in load_all_lines():
        try:
            all_records.append(json.loads(l))
        except Exception:
            all_records.append({})
    return format_closed_bottle(cid, all_records, end_rec), f"Rendered bottle {cid}."


def is_delivered(cid: str) -> bool:
    return cid in load_state().get("delivered_ids", [])


DELIVERED_IDS_CAP = 500


def _remember_delivered(state: dict, cid: str) -> None:
    """Record `cid` as delivered in an in-memory state dict, bounded.

    Callers that also mutate the cursor MUST use this and save once, rather than
    mark_delivered() — that re-reads state from disk and would drop their cursor.
    """
    ids = state.setdefault("delivered_ids", [])
    if cid not in ids:
        ids.append(cid)
    if len(ids) > DELIVERED_IDS_CAP:
        del ids[:-DELIVERED_IDS_CAP]


def mark_delivered(cid: str) -> None:
    state = load_state()
    _remember_delivered(state, cid)
    save_state(state)


def collect_new(state, advance):
    """Scan the ledger from the cursor for new end-state events; for each,
    render the full-history message using ALL records for that bottle id
    (not just the ones after the cursor). Returns (messages, status, new_cursor)."""
    lines = load_all_lines()
    total = len(lines)
    cursor = state.get("last_processed_line", 0)
    if cursor > total:
        cursor = 0
    if cursor >= total:
        return [], "No new callback events.", total

    all_records = []
    for l in lines:
        try:
            all_records.append(json.loads(l))
        except Exception:
            all_records.append({})

    messages = []
    for rec in all_records[cursor:]:
        if rec.get("event") in END_EVENTS and rec.get("id"):
            messages.append(format_closed_bottle(rec["id"], all_records, rec))

    new_cursor = total if advance else cursor
    status = f"Scanned {total - cursor} new ledger line(s), found {len(messages)} closed bottle(s)."
    return messages, status, new_cursor

# ----------------------------------------------------------------- delivery
def deliver_one(message: str) -> bool:
    """Deterministic delivery: shell out to `openclaw message send`. No LLM
    in this path. Returns True on success."""
    cmd = ["openclaw", "message", "send", "--channel", "discord",
           "--target", target_channel(), "--message", message]
    acct = account_id()
    if acct:
        cmd += ["--account", acct]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"delivery failed (exit {result.returncode}): {result.stderr.strip()}", file=sys.stderr)
            return False
        return True
    except Exception as e:
        print(f"delivery failed: {e}", file=sys.stderr)
        return False

# --------------------------------------------------------------------------- main
def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "process"
    state = load_state()

    if cmd == "on":
        state["enabled"] = True
        save_state(state)
        print(json.dumps({"enabled": True, "status": "ON", "target": target_channel()}))
        return

    if cmd == "off":
        state["enabled"] = False
        save_state(state)
        print(json.dumps({"enabled": False, "status": "OFF"}))
        return

    if cmd == "status":
        print(json.dumps({
            "enabled": state.get("enabled", True),
            "status": "ON" if state.get("enabled", True) else "OFF",
            "last_processed_line": state.get("last_processed_line", 0),
            "ledger": str(ledger_file()),
            "state_file": str(state_file()),
            "target": target_channel_or_none(),
        }, indent=2))
        return

    if cmd == "peek":
        messages, status, _ = collect_new(state, advance=False)
        print(json.dumps({"messages": messages, "status": status, "delivered": False}, indent=2))
        return

    if cmd == "render":
        """py script.py render <cid>  ->  print the deterministic message (no send)."""
        if len(sys.argv) < 3:
            print(json.dumps({"ok": False, "error": "render requires a bottle id: render <cid>"}), file=sys.stderr)
            sys.exit(2)
        cid = sys.argv[2]
        msg, status = render_bottle(cid)
        if msg is None:
            print(json.dumps({"ok": False, "error": status}), file=sys.stderr)
            sys.exit(1)
        print(msg)
        return

    if cmd == "finalize":
        """py script.py finalize <cid>  ->  render + deliver the message once (exactly-once)."""
        if len(sys.argv) < 3:
            print(json.dumps({"ok": False, "error": "finalize requires a bottle id: finalize <cid>"}), file=sys.stderr)
            sys.exit(2)
        cid = sys.argv[2]
        if is_delivered(cid):
            print(json.dumps({"ok": True, "delivered": False,
                              "status": f"Bottle {cid} already finalized — skipping (exactly-once)."}, indent=2))
            return
        msg, status = render_bottle(cid)
        if msg is None:
            print(json.dumps({"ok": False, "error": status}), file=sys.stderr)
            sys.exit(1)
        if deliver_one(msg):
            mark_delivered(cid)
            print(json.dumps({"ok": True, "delivered": True,
                              "status": f"Finalized bottle {cid} and posted to {target_channel()}."},
                             indent=2))
        else:
            print(json.dumps({"ok": False, "delivered": False,
                              "error": f"Delivery failed for bottle {cid}; cursor not advanced (will retry)."},
                             indent=2), file=sys.stderr)
            sys.exit(1)
        return

    if cmd == "process":
        if not state.get("enabled", True):
            print(json.dumps({"messages": [], "status": "Notifier DISABLED — skipping sweep.", "delivered": False}))
            return
        lines = load_all_lines()
        total = len(lines)
        cursor = state.get("last_processed_line", 0)
        if cursor > total:
            cursor = 0
        if cursor >= total:
            print(json.dumps({"messages": [], "status": "No new callback events.", "delivered": True}))
            return

        all_records = []
        for l in lines:
            try:
                all_records.append(json.loads(l))
            except Exception:
                all_records.append({})

        delivered_msgs = []
        skipped = []
        # Deliver in order; stop advancing the cursor at the first delivery
        # failure so nothing is skipped on the next run (at-least-once,
        # exactly-once in the common case).
        #
        # The cursor alone is NOT a dedup guard. `finalize` (the claw-callback
        # hook) records ids in delivered_ids without moving the cursor, so any
        # bottle it announced still sits in this scan window. Consult
        # delivered_ids per bottle — that is the only guard both paths share.
        new_cursor = total
        for i, rec in enumerate(all_records[cursor:], start=cursor):
            if rec.get("event") in END_EVENTS and rec.get("id"):
                cid = rec["id"]
                if cid in state.get("delivered_ids", []):
                    skipped.append(cid)
                    continue
                msg = format_closed_bottle(cid, all_records, rec)
                if deliver_one(msg):
                    delivered_msgs.append(msg)
                    _remember_delivered(state, cid)
                else:
                    new_cursor = i
                    break

        state["last_processed_line"] = new_cursor
        save_state(state)
        status = (f"Delivered {len(delivered_msgs)} closed-bottle report(s); "
                  f"cursor now {new_cursor}/{total}.")
        if skipped:
            status += f" Skipped {len(skipped)} already-delivered: {', '.join(skipped)}."
        print(json.dumps({
            "messages": delivered_msgs,
            "skipped_already_delivered": skipped,
            "status": status,
            "delivered": True,
        }, indent=2))
        return

    print(json.dumps({"ok": False, "error": f"unknown command: {cmd}",
                      "commands": ["on", "off", "status", "process", "peek", "render", "finalize"]}), file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
