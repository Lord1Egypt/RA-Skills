"""
mac-reminder-bridge / listener.py  v2.1
========================================
Run this script on your Mac.
Listens for HTTP requests from Docker (OpenClaw) and controls macOS Reminders.app.

Changes in v2.1 (security & bug-fix pass):
  🔴 Fixed AppleScript injection via newline chars in as_escape()
  🔴 Fixed update_reminder new_due AppleScript structure bug
  🟡 Replaced ||| delimiter with \x1E (ASCII Record Separator, safe in AS output)
  🟡 batch: return 207 Multi-Status when some items fail
  🟡 DEFAULT_LIST: lazy init with thread-safe lock
  🟢 run_script: catches TimeoutExpired + FileNotFoundError
  🟢 Log path uses Path.resolve() for launchd safety
  🟢 requirements.txt version cap

Environment variables:
  BRIDGE_SECRET        Shared secret for X-Bridge-Secret header (recommended)
  BRIDGE_PORT          Port (default: 5000)
  BRIDGE_ALLOWED_IPS   Comma-separated IPs/CIDRs (default: 172.0.0.0/8,127.0.0.1,::1)
                       Example: "1.2.3.4,192.168.1.0/24" for Cloud/Home mixed setups.
                       Set to "0.0.0.0/0" to disable IP check (NOT recommended unless BRIDGE_SECRET is set).
  DRY_RUN              Set to "1" to log without writing to Reminders
"""

from __future__ import annotations
import ipaddress
import logging
import logging.handlers
import os
import subprocess
import threading
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, request, jsonify

# ══════════════════════════════════════════════════════════════════════════════
# Config
# ══════════════════════════════════════════════════════════════════════════════

API_SECRET = os.environ.get("BRIDGE_SECRET", "")
PORT       = int(os.environ.get("BRIDGE_PORT", 5000))
DRY_RUN    = os.environ.get("DRY_RUN", "").strip() == "1"

_raw_ips = os.environ.get("BRIDGE_ALLOWED_IPS", "172.0.0.0/8,127.0.0.1,::1")
from typing import Union, List
ALLOWED_NETWORKS: List[Union[ipaddress.IPv4Network, ipaddress.IPv6Network]] = []
for _entry in _raw_ips.split(","):
    _entry = _entry.strip()
    if _entry:
        try:
            ALLOWED_NETWORKS.append(ipaddress.ip_network(_entry, strict=False))
        except ValueError:
            pass

# ASCII Record Separator — extremely unlikely to appear in reminder text
_SEP = "\x1e"

# ══════════════════════════════════════════════════════════════════════════════
# Logging (console + rotating file)
# ══════════════════════════════════════════════════════════════════════════════

# Use Path.resolve() so launchd (cwd="/") doesn't write logs to "/"
_LOG_DIR  = Path(__file__).resolve().parent
_LOG_FILE = _LOG_DIR / "reminder_bridge.log"

log = logging.getLogger("bridge")
log.setLevel(logging.DEBUG)

_fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")

_ch = logging.StreamHandler()
_ch.setFormatter(_fmt)
log.addHandler(_ch)

_fh = logging.handlers.RotatingFileHandler(
    _LOG_FILE, maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
_fh.setFormatter(_fmt)
log.addHandler(_fh)

# ══════════════════════════════════════════════════════════════════════════════
# Flask
# ══════════════════════════════════════════════════════════════════════════════

app = Flask(__name__)


def require_auth(f):
    """IP allowlist + optional shared-secret check."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        client_ip = request.remote_addr or ""
        try:
            addr    = ipaddress.ip_address(client_ip)
            allowed = any(addr in net for net in ALLOWED_NETWORKS)
        except ValueError:
            allowed = False

        if not allowed:
            log.warning("Rejected %s — not in IP allowlist", client_ip)
            return jsonify({"error": "Forbidden"}), 403

        if API_SECRET and request.headers.get("X-Bridge-Secret") != API_SECRET:
            log.warning("Rejected %s — bad or missing X-Bridge-Secret", client_ip)
            return jsonify({"error": "Unauthorized"}), 401

        return f(*args, **kwargs)
    return wrapper


# ══════════════════════════════════════════════════════════════════════════════
# AppleScript helpers
# ══════════════════════════════════════════════════════════════════════════════

def as_escape(s: str) -> str:
    """
    Escape a Python string for safe embedding inside AppleScript double quotes.

    🔴 Fix v2.1: also strip \\n and \\r — without this, a newline in `task`
    could inject arbitrary AppleScript statements after the string literal.
    """
    return (
        s.replace("\\", "\\\\")
         .replace('"', '\\"')
         .replace("\n", " ")   # newline → space (injection prevention)
         .replace("\r", " ")   # CR      → space
    )


def run_script(script: str) -> tuple:
    """
    Execute an AppleScript string via osascript.
    Returns (stdout, stderr, returncode).

    🟢 Fix v2.1: catch TimeoutExpired and FileNotFoundError explicitly.
    """
    if DRY_RUN:
        log.debug("[DRY-RUN] AppleScript:\n%s", script.strip())
        return "0", "", 0

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=15
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode

    except subprocess.TimeoutExpired:
        log.error("osascript timed out after 15 s")
        return "", "AppleScript timed out", 1

    except FileNotFoundError:
        log.error("osascript not found — are you running on macOS?")
        return "", "osascript not found", 1


def build_date_block(var: str, dt: datetime) -> str:
    """
    Return an AppleScript block that assigns a datetime to variable `var`.
    Uses numeric components (locale-safe).
    Each line is at the same indentation level — safe to embed anywhere.
    """
    return (
        f"set {var} to current date\n"
        f"        set year of {var} to {dt.year}\n"
        f"        set month of {var} to {dt.month}\n"
        f"        set day of {var} to {dt.day}\n"
        f"        set hours of {var} to {dt.hour}\n"
        f"        set minutes of {var} to {dt.minute}\n"
        f"        set seconds of {var} to 0"
    )


def parse_datetime(value: str, field_name: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM or YYYY-MM-DD; raises ValueError with a clear message."""
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Invalid '{field_name}' — use YYYY-MM-DD HH:MM or YYYY-MM-DD")


# ══════════════════════════════════════════════════════════════════════════════
# Reminders list helpers  (lazy DEFAULT_LIST with thread-safe lock)
# ══════════════════════════════════════════════════════════════════════════════

PRIORITY_MAP   = {"none": 0, "low": 9, "medium": 5, "high": 1,
                  "0": 0, "1": 1, "5": 5, "9": 9}
PRIORITY_LABEL = {0: "none", 9: "low", 5: "medium", 1: "high"}

_default_list_lock  = threading.Lock()
_default_list_cache: Union[str, None] = None


def get_all_list_names() -> list[str]:
    out, _, rc = run_script('tell application "Reminders" to return name of every list')
    if rc == 0 and out:
        return [n.strip() for n in out.split(",") if n.strip()]
    return []


def _fetch_default_list() -> str:
    out, _, rc = run_script(
        'tell application "Reminders" to return name of item 1 of lists'
    )
    return out if rc == 0 else ""


def get_default_list() -> str:
    """
    🟡 Fix v2.1: lazy init — only query Reminders when first needed,
    so startup before the user grants permission doesn't permanently cache "".
    Thread-safe via a lock.
    """
    global _default_list_cache
    with _default_list_lock:
        if _default_list_cache is None:
            _default_list_cache = _fetch_default_list()
    return _default_list_cache


def invalidate_default_list():
    """Force re-detection on next access (e.g. after permission grant)."""
    global _default_list_cache
    with _default_list_lock:
        _default_list_cache = None


def check_reminders_permission() -> bool:
    _, err, rc = run_script('tell application "Reminders" to return count of lists')
    if rc != 0:
        log.error("Reminders permission check failed: %s", err)
    return rc == 0


def list_clause(list_name: str) -> str:
    name = (list_name or "").strip() or get_default_list()
    if name:
        return f'set targetList to list "{as_escape(name)}"'
    return "set targetList to item 1 of lists"


def scope_clause(list_name: str) -> str:
    name = (list_name or "").strip()
    if name:
        return f'set searchLists to {{list "{as_escape(name)}"}}'
    return "set searchLists to every list"


# ══════════════════════════════════════════════════════════════════════════════
# Routes
# ══════════════════════════════════════════════════════════════════════════════

@app.route("/health", methods=["GET"])
@require_auth
def health():
    # Invalidate cache so /health always reflects current state
    invalidate_default_list()
    ok    = check_reminders_permission()
    lists = get_all_list_names()
    return jsonify({
        "status":               "ok" if ok else "error",
        "reminders_permission": ok,
        "dry_run":              DRY_RUN,
        "time":                 datetime.now().isoformat(),
        "default_list":         get_default_list(),
        "all_lists":            lists,
    }), 200 if ok else 503


# ── Create ─────────────────────────────────────────────────────────────────────

def _create_reminder(data: dict) -> tuple[dict, int]:
    """
    Core create logic shared by /add_reminder and /add_reminder_batch.

    Fields:
      task        str  required
      list        str  optional  target list name
      due         str  optional  YYYY-MM-DD HH:MM
      remind_at   str  optional  YYYY-MM-DD HH:MM  (alarm)
      notes       str  optional
      priority    str  optional  none/low/medium/high
    """
    task      = (data.get("task")      or "").strip()
    list_name = (data.get("list")      or "").strip()
    due       = (data.get("due")       or "").strip()
    remind_at = (data.get("remind_at") or "").strip()
    notes     = (data.get("notes")     or "").strip()
    priority  = str(data.get("priority") or "none").lower().strip()

    if not task:
        return {"error": "Missing 'task'"}, 400

    prio_val = PRIORITY_MAP.get(priority, 0)
    lc       = list_clause(list_name)

    props = [f'name:"{as_escape(task)}"', f"priority:{prio_val}"]
    if notes:
        props.append(f'body:"{as_escape(notes)}"')

    dt_due = dt_alarm = None
    if due:
        try:
            dt_due = parse_datetime(due, "due")
        except ValueError as e:
            return {"error": str(e)}, 400
    if remind_at:
        try:
            dt_alarm = parse_datetime(remind_at, "remind_at")
        except ValueError as e:
            return {"error": str(e)}, 400

    due_block   = build_date_block("dueDate",   dt_due)   if dt_due   else ""
    alarm_block = build_date_block("alarmDate", dt_alarm) if dt_alarm else ""
    due_set     = "set due date of newReminder to dueDate"                          if dt_due   else ""
    alarm_set   = ("make new reminder alarm at end of alarms of newReminder "
                   "with properties {trigger date:alarmDate}")                       if dt_alarm else ""

    script = f"""
tell application "Reminders"
    {lc}
    set newReminder to make new reminder at end of targetList ¬
        with properties {{{", ".join(props)}}}
    {due_block}
    {due_set}
    {alarm_block}
    {alarm_set}
end tell
"""
    _, err, rc = run_script(script)
    if rc != 0:
        log.error("Error creating '%s': %s", task, err)
        return {"error": err}, 500

    log.info("Created: '%s'  due=%s alarm=%s priority=%s list=%s",
             task, due or "—", remind_at or "—", priority, list_name or get_default_list())
    return {
        "status":    "created",
        "task":      task,
        "due":       due or None,
        "remind_at": remind_at or None,
        "priority":  priority,
        "list":      list_name or get_default_list(),
    }, 200


@app.route("/add_reminder", methods=["POST"])
@require_auth
def add_reminder():
    data = request.get_json(silent=True) or {}
    body, status = _create_reminder(data)
    return jsonify(body), status


@app.route("/add_reminder_batch", methods=["POST"])
@require_auth
def add_reminder_batch():
    """
    🟡 Fix v2.1: return 207 Multi-Status when some items fail (not always 200).
    """
    data  = request.get_json(silent=True) or {}
    items = data.get("items") or []
    if not items:
        return jsonify({"error": "Missing 'items'"}), 400

    results = []
    for item in items:
        body, status = _create_reminder(item)
        results.append({"ok": status == 200, **body})

    ok_count = sum(1 for r in results if r["ok"])
    all_ok   = ok_count == len(results)
    http_status = 200 if all_ok else (207 if ok_count > 0 else 500)

    return jsonify({
        "results": results,
        "created": ok_count,
        "total":   len(results),
    }), http_status


# ── Update ─────────────────────────────────────────────────────────────────────

@app.route("/update_reminder", methods=["POST"])
@require_auth
def update_reminder():
    """
    Update fields of an existing reminder.

    🔴 Fix v2.1: build_date_block is now emitted as a properly indented
    standalone block *before* the set_lines loop, avoiding AppleScript
    syntax errors from multi-line strings inside a join().

    Body:
      task          str  required  current title (find key)
      list          str  optional  limit search to this list
      fuzzy         bool optional  contains-match (default false)
      new_task      str  optional  new title
      new_due       str  optional  YYYY-MM-DD HH:MM, or "" to clear
      new_notes     str  optional
      new_priority  str  optional
    """
    data      = request.get_json(silent=True) or {}
    task      = (data.get("task") or "").strip()
    fuzzy     = bool(data.get("fuzzy", False))
    list_name = (data.get("list") or "").strip()

    if not task:
        return jsonify({"error": "Missing 'task'"}), 400

    op = "contains" if fuzzy else "is"
    te = as_escape(task)
    sc = scope_clause(list_name)

    # Collect simple single-line set statements
    set_lines: list[str] = []

    if "new_task" in data and data["new_task"]:
        set_lines.append(f'set name of r to "{as_escape(str(data["new_task"]))}"')

    if "new_notes" in data:
        set_lines.append(f'set body of r to "{as_escape(str(data["new_notes"] or ""))}"')

    if "new_priority" in data:
        pv = PRIORITY_MAP.get(str(data["new_priority"]).lower(), 0)
        set_lines.append(f"set priority of r to {pv}")

    # 🔴 Fix: build due-date block separately as a preamble, keep set_lines clean
    due_preamble = ""
    if "new_due" in data:
        val = (data["new_due"] or "").strip()
        if val:
            try:
                dt = parse_datetime(val, "new_due")
                # Emit the date-building block before the repeat loop
                due_preamble = build_date_block("newDue", dt)
                set_lines.append("set due date of r to newDue")
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        else:
            set_lines.append("set due date of r to missing value")

    if not set_lines:
        return jsonify({"error": "No fields to update provided"}), 400

    # Each set_line is a single line — safe to join with newline + indent
    updates_block = "\n                ".join(set_lines)

    script = f"""
tell application "Reminders"
    {sc}
    {due_preamble}
    set updatedCount to 0
    repeat with l in searchLists
        repeat with r in (reminders of l)
            if name of r {op} "{te}" then
                {updates_block}
                set updatedCount to updatedCount + 1
            end if
        end repeat
    end repeat
    return updatedCount
end tell
"""
    out, err, rc = run_script(script)
    if rc != 0:
        log.error("Error updating '%s': %s", task, err)
        return jsonify({"error": err}), 500

    count = int(out or 0)
    log.info("Updated %d reminder(s) matching '%s'", count, task)
    return jsonify({"status": "updated", "task": task, "count": count}), 200


# ── Delete ─────────────────────────────────────────────────────────────────────

@app.route("/delete_reminder", methods=["POST"])
@require_auth
def delete_reminder():
    data      = request.get_json(silent=True) or {}
    task      = (data.get("task") or "").strip()
    fuzzy     = bool(data.get("fuzzy", False))
    list_name = (data.get("list") or "").strip()

    if not task:
        return jsonify({"error": "Missing 'task'"}), 400

    op = "contains" if fuzzy else "is"
    te = as_escape(task)
    sc = scope_clause(list_name)

    script = f"""
tell application "Reminders"
    {sc}
    set deletedCount to 0
    repeat with l in searchLists
        set toDelete to {{}}
        repeat with r in (reminders of l)
            if name of r {op} "{te}" then
                set end of toDelete to r
            end if
        end repeat
        repeat with r in toDelete
            delete r
            set deletedCount to deletedCount + 1
        end repeat
    end repeat
    return deletedCount
end tell
"""
    out, err, rc = run_script(script)
    if rc != 0:
        log.error("Error deleting '%s': %s", task, err)
        return jsonify({"error": err}), 500

    count = int(out or 0)
    log.info("Deleted %d reminder(s) matching '%s'", count, task)
    return jsonify({"status": "deleted", "task": task, "count": count}), 200


# ── Complete / Uncomplete ──────────────────────────────────────────────────────

@app.route("/complete_reminder", methods=["POST"])
@require_auth
def complete_reminder():
    data      = request.get_json(silent=True) or {}
    task      = (data.get("task") or "").strip()
    fuzzy     = bool(data.get("fuzzy", False))
    completed = bool(data.get("completed", True))
    list_name = (data.get("list") or "").strip()

    if not task:
        return jsonify({"error": "Missing 'task'"}), 400

    op    = "contains" if fuzzy else "is"
    te    = as_escape(task)
    c_val = "true" if completed else "false"
    sc    = scope_clause(list_name)

    script = f"""
tell application "Reminders"
    {sc}
    set doneCount to 0
    repeat with l in searchLists
        repeat with r in (reminders of l)
            if name of r {op} "{te}" then
                set completed of r to {c_val}
                set doneCount to doneCount + 1
            end if
        end repeat
    end repeat
    return doneCount
end tell
"""
    out, err, rc = run_script(script)
    if rc != 0:
        log.error("Error completing '%s': %s", task, err)
        return jsonify({"error": err}), 500

    count  = int(out or 0)
    action = "completed" if completed else "uncompleted"
    log.info("%s %d reminder(s) matching '%s'", action, count, task)
    return jsonify({"status": action, "task": task, "count": count}), 200


# ── List reminders ─────────────────────────────────────────────────────────────

@app.route("/list_reminders", methods=["GET"])
@require_auth
def list_reminders():
    """
    🟡 Fix v2.1: replaced ||| delimiter with ASCII 0x1E (Record Separator).
    This character cannot appear in Reminders text, making parsing reliable.

    Query params:
      list=       filter by list name
      completed=  false (default) | true | all
    """
    list_name     = (request.args.get("list") or "").strip()
    completed_arg = (request.args.get("completed") or "false").lower()
    sc            = scope_clause(list_name)

    if completed_arg == "all":
        filter_open = filter_close = ""
    elif completed_arg == "true":
        filter_open  = "if completed of r is true then"
        filter_close = "end if"
    else:
        filter_open  = "if completed of r is false then"
        filter_close = "end if"

    # Use ASCII RS (0x1E) as field separator — safe in AppleScript string literals
    rs = "\\u001e"  # AppleScript doesn't support \x escapes; embed literal below

    script = f"""
tell application "Reminders"
    {sc}
    set RS to (ASCII character 30)
    set output to {{}}
    repeat with l in searchLists
        repeat with r in (reminders of l)
            {filter_open}
                set rName to name of r
                try
                    set rDue to (due date of r) as string
                on error
                    set rDue to ""
                end try
                try
                    set rNotes to body of r
                on error
                    set rNotes to ""
                end try
                set rPrio to priority of r as string
                set rDone to completed of r as string
                set rList to name of l
                set end of output to rName & RS & rDue & RS & rNotes & RS & rPrio & RS & rDone & RS & rList
            {filter_close}
        end repeat
    end repeat
    set AppleScript's text item delimiters to linefeed
    return output as string
end tell
"""
    out, err, rc = run_script(script)
    if rc != 0:
        log.error("Error listing reminders: %s", err)
        return jsonify({"error": err}), 500

    reminders = []
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\x1e")   # ASCII RS
        if len(parts) < 6:
            continue
        name, due, notes, prio_raw, done_raw, lst = parts[:6]
        try:
            prio_int = int(prio_raw.strip())
        except ValueError:
            prio_int = 0
        reminders.append({
            "task":      name.strip(),
            "due":       due.strip()   or None,
            "notes":     notes.strip() or None,
            "priority":  PRIORITY_LABEL.get(prio_int, "none"),
            "completed": done_raw.strip() == "true",
            "list":      lst.strip(),
        })

    return jsonify({"reminders": reminders, "count": len(reminders)}), 200


# ── List all lists ─────────────────────────────────────────────────────────────

@app.route("/list_lists", methods=["GET"])
@require_auth
def list_lists():
    script = """
tell application "Reminders"
    set RS to (ASCII character 30)
    set output to {}
    repeat with l in lists
        set pending to count of (reminders of l whose completed is false)
        set total   to count of reminders of l
        set end of output to name of l & RS & (pending as string) & RS & (total as string)
    end repeat
    set AppleScript's text item delimiters to linefeed
    return output as string
end tell
"""
    out, err, rc = run_script(script)
    if rc != 0:
        return jsonify({"error": err}), 500

    lists = []
    for line in out.split("\n"):
        if not line.strip():
            continue
        parts = line.split("\x1e")
        if len(parts) < 3:
            continue
        lists.append({
            "name":    parts[0].strip(),
            "pending": int(parts[1].strip() or 0),
            "total":   int(parts[2].strip() or 0),
        })

    return jsonify({"lists": lists, "default": get_default_list()}), 200


# ══════════════════════════════════════════════════════════════════════════════
# Startup
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    log.info("🍎  Mac Reminder Bridge  v2.1")
    log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    log.info("Port     : %d", PORT)
    log.info("Dry-run  : %s", DRY_RUN)
    log.info("Log file : %s", _LOG_FILE)

    if not check_reminders_permission():
        log.error("❌  Cannot access Reminders.app")
        log.error("    → System Settings → Privacy & Security → Reminders → grant access")
    else:
        log.info("✅  Reminders permission OK")
        default = get_default_list()
        log.info("📋  Default list : '%s'", default or "(index fallback)")
        all_l = get_all_list_names()
        log.info("📚  All lists    : %s", ", ".join(all_l) if all_l else "(none)")

    if API_SECRET:
        log.info("🔒  Auth         : X-Bridge-Secret required")
    else:
        log.warning("⚠️   Auth         : No BRIDGE_SECRET — anyone on allowed IPs can call this API")

    if ALLOWED_NETWORKS:
        log.info("🛡️   IP allowlist  : %s", ", ".join(str(n) for n in ALLOWED_NETWORKS))

    log.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    app.run(host="0.0.0.0", port=PORT, debug=False)
