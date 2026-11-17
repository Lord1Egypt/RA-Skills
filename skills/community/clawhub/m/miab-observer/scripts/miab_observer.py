#!/usr/bin/env python3
"""
miab_observer — live transaction observer and file logger for the MIAB callback ledger.

PREREQUISITE: Requires the `miab-broker` skill to be installed and active.
It tails the append-only callback ledger (state/callbacks/ledger.jsonl) managed by miab-broker,
converts raw create / forward / return / resolve / cancel / fail / corrupt events into
human-readable log entries using the agent identity map, advances a once-only cursor, and — when the live
toggle is on — writes the formatted batch to the log file ($CLAW_HOME/logs/interagent-queue.log).

This is a READ-ONLY observer over the ledger: it never mutates the ledger or envelopes.
The only files it writes are its own queue_state.json (toggle + cursor) and the output log file.

Path resolution (portable, sovereign):
  - CLAW_HOME      : broker root          (default: ~/.openclaw)
  - CLAW_LEDGER    : explicit ledger path (overrides CLAW_HOME/state/callbacks/ledger.jsonl)
  - CLAW_QUEUE_LOG : explicit log path    (overrides CLAW_HOME/logs/interagent-queue.log)
  - LYRA_WORKSPACE / CLAW_QUEUE_STATE : where queue_state.json lives
                     (default: ~/.openclaw/workspace/state/callbacks/queue_state.json)
"""
import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- paths
def claw_home() -> Path:
    return Path(os.environ.get("CLAW_HOME", "~/.openclaw")).expanduser()

def workspace_dir() -> Path:
    return Path(os.environ.get("LYRA_WORKSPACE", "~/.openclaw/workspace")).expanduser()

def ledger_file() -> Path:
    env = os.environ.get("CLAW_LEDGER")
    if env:
        return Path(env).expanduser()
    return claw_home() / "state" / "callbacks" / "ledger.jsonl"

def state_file() -> Path:
    env = os.environ.get("CLAW_QUEUE_STATE")
    if env:
        return Path(env).expanduser()
    return workspace_dir() / "state" / "callbacks" / "queue_state.json"

def log_file() -> Path:
    env = os.environ.get("CLAW_QUEUE_LOG")
    if env:
        return Path(env).expanduser()
    # Deliberately still "interagent-queue.log" after the 2.0.0 rename. Renaming it would
    # start a second log beside the user's existing one, orphan the first, and break any
    # rotation or shipping pointed at that path. State names do not follow the skill name.
    return claw_home() / "logs" / "interagent-queue.log"

def check_prerequisites() -> tuple[bool, str]:
    """Verify that miab-broker is active and the callback state directory exists."""
    cb_dir = claw_home() / "state" / "callbacks"
    if not cb_dir.exists():
        return False, f"Prerequisite check failed: miab-broker state directory not found at {cb_dir}. Please ensure miab-broker is installed and initialized."
    return True, "OK"

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
    "sweep": "🧹 Callback Reaper"
}

def registry_file() -> Path:
    env = os.environ.get("CLAW_REGISTRY")
    if env:
        return Path(env).expanduser()
    return claw_home() / "state" / "callbacks" / "agent-registry.json"


_REGISTRY_NAMES = None


def registry_display_names() -> dict:
    """canonical-name -> displayName, read from miab-broker's agent-registry.json. (Q9)

    AGENT_MAP below duplicated exactly the persona<->function mapping the broker's
    registry now owns (miab-broker T14). Two sources of truth for one fact is why
    `SPECTRE` and `ECHO` rendered inconsistently: this file's copy silently fell back
    to the raw name on a miss. The registry is authoritative; AGENT_MAP is the
    fallback for agents that have never been registered.

    Read-only, and cached for the process — this observer never mutates broker state.
    """
    global _REGISTRY_NAMES
    if _REGISTRY_NAMES is not None:
        return _REGISTRY_NAMES
    names = {}
    try:
        reg = json.loads(registry_file().read_text(encoding="utf-8"))
        for key, entry in (reg.get("agents") or {}).items():
            if not isinstance(entry, dict):
                continue
            label = entry.get("displayName")
            canonical = str(key).strip().casefold()
            if label:
                names[canonical] = label
            for alias in entry.get("aliases") or []:
                if label:
                    names[str(alias).strip().casefold()] = label
                else:
                    # No displayName, but the alias should still land on whatever
                    # AGENT_MAP knows the canonical name as.
                    names.setdefault(str(alias).strip().casefold(),
                                     AGENT_MAP.get(canonical, canonical))
    except (OSError, ValueError, AttributeError):
        names = {}
    _REGISTRY_NAMES = names
    return names


def who(name):
    """Friendly display for a logical agent name.

    Registry displayName wins, then this module's AGENT_MAP fallback, then the raw
    name. Lookups are case-insensitive to match the broker's canonical form, so a
    ledger record written as `ECHO` and one written as `echo` render identically. (Q9)
    """
    if not name:
        return "Unknown"
    canonical = str(name).strip().casefold()
    hit = registry_display_names().get(canonical)
    if hit:
        return hit
    return AGENT_MAP.get(canonical, name)

# --------------------------------------------------------------------------- state
def _refuse_unusable_state(p: Path, reason: str) -> None:
    """Exit 1 rather than silently resetting the cursor. See load_state()."""
    print(json.dumps({
        "ok": False,
        "error": f"state file unusable: {reason}",
        "state_file": str(p),
        "refusing": "resetting the cursor here would replay the entire ledger into the log",
        "remedy": "inspect the file, then repair it or delete it to start a fresh sweep",
    }, indent=2), file=sys.stderr)
    sys.exit(1)


def load_state() -> dict:
    """Load the sweep cursor and the live toggle.

    A MISSING state file is a genuine fresh start, and `last_processed_line: 0`
    is the right answer for it.

    An UNUSABLE one is not, and must never be treated as one. Until 1.3.0 this
    function swallowed every exception and fell through to that same fresh-start
    default, so a corrupt or truncated queue_state.json silently rewound the
    cursor to 0 and the next `process` replayed the ENTIRE ledger into the log —
    the failure mode duplicated the output this observer exists to produce, which
    is worse than not running at all. Fail closed instead and let the operator
    repair or remove the file deliberately.
    """
    p = state_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        return {"enabled": False, "last_processed_line": 0}
    try:
        state = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        _refuse_unusable_state(p, str(e))
    if not isinstance(state, dict):
        _refuse_unusable_state(p, f"expected a JSON object, found {type(state).__name__}")
    cursor = state.get("last_processed_line", 0)
    if isinstance(cursor, bool) or not isinstance(cursor, int) or cursor < 0:
        _refuse_unusable_state(
            p, f"last_processed_line must be a non-negative integer, found {cursor!r}")
    return state

def save_state(state: dict) -> None:
    p = state_file()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(p)

# ----------------------------------------------------------------- summarization
def sanitize_and_summarize(text, limit=350):
    """Clean up and produce a concise summary of task/result text."""
    if not text:
        return ""
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        l = line.strip()
        if not l:
            continue
        # Exclude bulky checklist / setup blueprints in summaries
        if any(kw in l.lower() for kw in ["callback://", "python3", "claw-callback", "mkdir", "chmod", "curl"]):
            continue
        cleaned_lines.append(line)
        
    cleaned_text = " ".join(cleaned_lines)
    cleaned_text = " ".join(cleaned_text.split())
    
    if len(cleaned_text) > limit:
        return cleaned_text[:limit-3] + "..."
    return cleaned_text

# ----------------------------------------------------------------- event rendering
def format_event(rec):
    """Render one ledger record into a human-readable log entry (or None)."""
    event = rec.get("event")
    cid = rec.get("id", "unknown")[:14]
    by = who(rec.get("by"))

    if event == "create":
        target = who(rec.get("to"))
        task_summary = sanitize_and_summarize(rec.get("task", ""))
        return (
            f"📥 [Enqueued Task] {cid}\n"
            f"   From: {by}\n"
            f"   To: {target}\n"
            f"   Task Assigned: {task_summary}"
        )
    if event == "forward":
        target = who(rec.get("to"))
        return (
            f"➡️ [Forwarded Task] {cid}\n"
            f"   By: {by}\n"
            f"   Forwarded To: {target}\n"
            f"   Note: Packaged parent callback frame onto LIFO stack."
        )
    if event == "return":
        wake_target = who(rec.get("wake"))
        return (
            f"↩️ [Returning Task] {cid}\n"
            f"   From: {by}\n"
            f"   Waking: {wake_target}\n"
            f"   Note: Handing execution results back up the stack."
        )
    if event == "resolve":
        task_summary = sanitize_and_summarize(rec.get("task", ""))
        result_summary = sanitize_and_summarize(rec.get("result", ""))
        return (
            f"✅ [Resolved Task] {cid}\n"
            f"   By: {by}\n"
            f"   Task: {task_summary}\n"
            f"   Resolution Outcome: {result_summary}"
        )
    if event == "cancel":
        reason = rec.get("reason", "Cancelled by user / system command")
        return (
            f"❌ [Cancelled Task] {cid}\n"
            f"   By: {by}\n"
            f"   Reason: {reason}"
        )
    if event == "fail":
        reason = rec.get("reason", "stale")
        holder = who(rec.get("holder"))
        return (
            f"⚠️ [Callback Failed/Reaped] {cid}\n"
            f"   By: {by}\n"
            f"   Reason: {reason}\n"
            f"   Last Holder: {holder}"
        )
    if event == "authority-override":
        # miab-broker T15. A call that would have been refused was forced through.
        # Rendering this is not optional: the ledger is the only place it is recorded,
        # and an unrendered event type is invisible rather than broken.
        action = rec.get("action", "unknown action")
        expected = who(rec.get("expected"))
        remaining = rec.get("stack_remaining")
        lines = [
            f"🔓 [Authority Override] {cid}",
            f"   By: {by}",
            f"   Forced: {action} (entitled agent was {expected})",
        ]
        if remaining:
            lines.append(f"   Warning: {remaining} frame(s) still waiting on the stack.")
        return "\n".join(lines)
    if event == "corrupt":
        reason = rec.get("reason", "unparseable or inconsistent envelope")
        dest = rec.get("quarantined_to", "unknown")
        return (
            f"🗑️ [Quarantined Envelope] {cid}\n"
            f"   By: {by}\n"
            f"   Reason: {reason}\n"
            f"   Quarantined To: {dest}"
        )
    return None

# ----------------------------------------------------------------- ledger sweep
def collect_new(state, advance):
    """Read the ledger from the cursor, return (messages, status, new_cursor).
    If advance is False the cursor is returned unchanged (peek mode)."""
    lf = ledger_file()
    cursor = state.get("last_processed_line", 0)
    if not lf.exists():
        return [], f"Ledger not found at {lf}; miab-broker prerequisite missing or ledger not yet created.", cursor
    try:
        with lf.open("r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
    except Exception as e:
        return [], f"Error reading ledger: {e}", cursor

    total = len(lines)
    if cursor > total:
        cursor = 0
    if cursor >= total:
        return [], "No new callback events.", total

    messages = []
    for line in lines[cursor:]:
        try:
            msg = format_event(json.loads(line))
            if msg:
                messages.append(msg)
        except Exception as e:
            print(f"skip malformed ledger line: {e}", file=sys.stderr)

    new_cursor = total if advance else cursor
    status = f"Read {total - cursor} new entries, rendered {len(messages)} message(s)."
    return messages, status, new_cursor

# ----------------------------------------------------------------- Log delivery
def deliver(messages):
    """Append formatted logs to the target log file ($CLAW_HOME/logs/interagent-queue.log)."""
    if not messages:
        return True
    lf = log_file()
    lf.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    try:
        with lf.open("a", encoding="utf-8") as f:
            for msg in messages:
                f.write(f"[{ts}]\n{msg}\n\n")
        return True
    except Exception as e:
        print(f"log file delivery failed: {e}", file=sys.stderr)
        return False

# --------------------------------------------------------------------------- main
def main():
    cmd = sys.argv[1].lower() if len(sys.argv) > 1 else "process"

    ok, err_msg = check_prerequisites()
    if not ok and cmd in ["on", "process"]:
        print(json.dumps({"ok": False, "error": err_msg, "prerequisite": "miab-broker"}, indent=2), file=sys.stderr)
        sys.exit(1)

    state = load_state()

    if cmd == "on":
        state["enabled"] = True
        save_state(state)
        print(json.dumps({"enabled": True, "status": "ON", "log_file": str(log_file()), "prerequisite": "miab-broker (verified)"}))
        return

    if cmd == "off":
        state["enabled"] = False
        save_state(state)
        print(json.dumps({"enabled": False, "status": "OFF"}))
        return

    if cmd == "status":
        prereq_ok, _ = check_prerequisites()
        print(json.dumps({
            "enabled": state.get("enabled", False),
            "status": "ON" if state.get("enabled") else "OFF",
            "last_processed_line": state.get("last_processed_line", 0),
            "log_file": str(log_file()),
            "ledger": str(ledger_file()),
            "state_file": str(state_file()),
            "prerequisites": {
                "miab-broker": "ok" if prereq_ok else "missing"
            }
        }, indent=2))
        return

    if cmd == "peek":
        messages, status, _ = collect_new(state, advance=False)
        print(json.dumps({"messages": messages, "status": status, "delivered": False, "log_file": str(log_file())}, indent=2))
        return

    if cmd == "process":
        if not state.get("enabled", False):
            print(json.dumps({"messages": [], "status": "Queue DISABLED — skipping sweep.",
                              "delivered": False, "log_file": str(log_file())}))
            return
        messages, status, new_cursor = collect_new(state, advance=True)
        delivered = deliver(messages)
        if delivered or not messages:
            state["last_processed_line"] = new_cursor
            save_state(state)
        print(json.dumps({"messages": messages, "status": status, "delivered": delivered, "log_file": str(log_file())},
                         indent=2))
        return

    print(json.dumps({"ok": False, "error": f"unknown command: {cmd}",
                      "commands": ["on", "off", "status", "process", "peek"]}), file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()
