#!/usr/bin/env python3
"""
setup-tasks.py — register the single tick task for med reminders.

Since issue #1 PR 2 the tick engine owns all per-dose logic: dispatch.py
`tick` evaluates every med's occurrences on each run, so exactly ONE
repeating scheduler entry is registered per state file — keyed by a short
hash of the resolved state path (task name, cron markers, registry), so
two state files never collide.

Register-verify-remove (issue #1 §5): the tick is registered and queried
back BEFORE any legacy per-dose job is removed. If registration or
verification fails this exits non-zero, prints REMINDERS ARE NOT
SCHEDULED, and leaves every legacy job in place.

Platform schedulers:
  Windows — Task Scheduler folder \\MedReminder\\, task tick-<hash>, run
            with pythonw.exe (no console flash), StartWhenAvailable,
            MultipleInstancesPolicy IgnoreNew, ExecutionTimeLimit PT10M.
            Legacy cleanup enumerates the folder via
            `schtasks /query /fo csv /nh` — never only the registry file.
  macOS   — launchd user agent (StartInterval; cron has a Full Disk
            Access problem on modern macOS); cron is the fallback.
  Linux   — cron by default; --scheduler systemd opts into a user timer
            (OnCalendar=*:0/5, Persistent=true).

Usage:
    python setup-tasks.py                      # register the tick (default 5 min)
    python setup-tasks.py --tick-minutes 1
    python setup-tasks.py --scheduler systemd  # Linux only
    python setup-tasks.py --clear              # remove this state's tick + legacy jobs
    python setup-tasks.py --dry-run
"""

import argparse
import csv
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

if sys.version_info < (3, 9):
    sys.exit(f"Python 3.9+ required — found {sys.version.split()[0]}")

# Console output includes unicode (arrows, em-dashes) that cp1252 consoles
# can't encode — degrade gracefully instead of crashing
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# ── Paths ─────────────────────────────────────────────────────────────────────

SCRIPT_DIR    = Path(__file__).parent.resolve()
STATE_FILE    = Path(os.environ.get("MEDS_STATE_FILE", SCRIPT_DIR / "meds-state.json"))
DISPATCH_FILE = SCRIPT_DIR / "dispatch.py"
LEGACY_REGISTRY_FILE = SCRIPT_DIR / ".registered-tasks.json"   # pre-PR3; deleted on migration

TASK_FOLDER = "MedReminder"    # Windows Task Scheduler subfolder
CRON_MARKER = "# MedReminder"  # pre-PR3 crontab section marker (legacy)
TICK_MINUTES_DEFAULT = 5


def _run(cmd, **kw):
    """Single seam for OS scheduler commands — tests mock this, never the OS."""
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


# ── State-file identity (issue #1 §5: two state files never collide) ─────────

def state_hash(state_path) -> str:
    """Short hash of the resolved state path — keys every registered name."""
    raw = str(Path(state_path).resolve()).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:8]

def registry_file(h: str) -> Path:
    return SCRIPT_DIR / f".registered-tasks.{h}.json"

def load_registry(h: str) -> dict:
    try:
        data = json.loads(registry_file(h).read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}

def save_registry(h: str, entry: dict) -> None:
    registry_file(h).write_text(json.dumps(entry, indent=2), encoding="utf-8")

def tick_task_name(h: str) -> str:
    return f"tick-{h}"

def tick_task_full_name(h: str) -> str:
    return f"\\{TASK_FOLDER}\\{tick_task_name(h)}"

def launchd_label(h: str) -> str:
    return f"com.medreminder.tick.{h}"

def systemd_unit(h: str) -> str:
    return f"medreminder-tick-{h}"


# ── Edit-time quiet-hours check (kept from v1; doctor + PR 4 add/edit use it) ─

def in_quiet_window(hhmm: str, quiet: dict) -> bool:
    """True if HH:MM falls inside the quiet window (handles midnight-spanning)."""
    def mins(s: str) -> int:
        h, m = map(int, s.split(":"))
        return h * 60 + m
    t, start, end = mins(hhmm), mins(quiet["start"]), mins(quiet["end"])
    if start <= end:
        return start <= t < end
    return t >= start or t < end


# ── The tick command ──────────────────────────────────────────────────────────

def tick_arguments(dispatch: str, state_path, tick_minutes: int) -> str:
    """Arguments after the interpreter — the state path is baked in because
    scheduled tasks don't inherit shell env vars (MEDS_STATE_FILE set in a
    profile never reaches them)."""
    return (f'"{Path(dispatch).resolve()}" --state "{Path(state_path).resolve()}" '
            f"tick --tick-minutes {tick_minutes}")

def cron_entry(python: str, arguments: str, tick_minutes: int) -> str:
    return f'*/{tick_minutes} * * * * "{python}" {arguments}'


# ── crontab: BEGIN/END block + legacy strip (issue #1 §5) ─────────────────────

def cron_begin(h: str) -> str:
    return f"# MedReminder BEGIN {h}"

def cron_end(h: str) -> str:
    return f"# MedReminder END {h}"

def build_cron_block(h: str, entry_line: str) -> list:
    """The whole managed block, markers included — one per state file."""
    return [
        cron_begin(h),
        "# managed by setup-tasks.py — edit there, not with crontab -e",
        entry_line,
        cron_end(h),
    ]

def strip_crontab(lines: list, state_path, h: str) -> list:
    """
    Remove everything this install owns (issue #1 §5):
      1. our delimited BEGIN/END blocks (so re-registration never duplicates),
      2. legacy marker-only blocks: a bare '# MedReminder' through the last
         consecutive MedReminder label/entry of the pre-PR3 format,
      3. any stray line containing dispatch.py plus this state's --state path
         (a per-dose job that lost its marker).
    Foreign lines — including another state file's block — survive.
    """
    state_flag = str(Path(state_path).resolve())
    out, i, n = [], 0, len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()

        if s == cron_begin(h):                          # rule 1
            i += 1
            while i < n and lines[i].strip() != cron_end(h):
                i += 1
            i += 1                                      # past END (or EOF if unterminated)
            if i < n and not lines[i].strip():
                i += 1                                  # the block's one trailing blank
            continue

        if s == CRON_MARKER:                            # rule 2
            i += 1
            j, last_entry_end = i, i
            while j < n:
                t = lines[j].strip()
                if "dispatch.py" in t and state_flag in t:
                    j += 1
                    last_entry_end = j                  # an entry confirms the block
                elif t.startswith("#"):                 # label — block member only if
                    j += 1                              # an entry follows it
                else:
                    break
            i = last_entry_end                          # unconfirmed trailing comments survive
            if i < n and not lines[i].strip():
                i += 1                                  # the block's one trailing blank
            continue

        if "dispatch.py" in line and state_flag in line:    # rule 3
            i += 1
            continue

        out.append(line)
        i += 1
    return out

def _strip_own_blocks(lines: list, h: str) -> list:
    """Remove ONLY our delimited blocks (rule 1) — registration's idempotency
    pass. Legacy lines must survive registration untouched: they are removed
    only after the tick verifies (issue #1 §5 register-verify-remove)."""
    out, i, n = [], 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s == cron_begin(h):
            i += 1
            while i < n and lines[i].strip() != cron_end(h):
                i += 1
            i += 1
            if i < n and not lines[i].strip():
                i += 1                      # the block's one trailing blank
            continue
        out.append(lines[i])
        i += 1
    return out

def find_legacy_cron(lines: list, state_path, h: str) -> list:
    """Lines this install owns that are NOT inside our delimited tick block."""
    state_flag = str(Path(state_path).resolve())
    legacy, inside = [], False
    for line in lines:
        s = line.strip()
        if s == cron_begin(h):
            inside = True
            continue
        if s == cron_end(h):
            inside = False
            continue
        if inside:
            continue
        if s == CRON_MARKER or ("dispatch.py" in line and state_flag in line):
            legacy.append(line)
    return legacy

def read_crontab(run=_run):
    """Crontab lines; [] when none exists; None when unreadable."""
    r = run(["crontab", "-l"])
    if r.returncode == 0:
        return (r.stdout or "").splitlines()
    if "no crontab for" in (r.stderr or "").lower():
        return []
    return None

def write_crontab(lines: list, run=_run) -> bool:
    content = "\n".join(lines) + "\n" if lines else ""
    return run(["crontab", "-"], input=content).returncode == 0

def register_cron(h: str, state_path, tick_minutes: int, run=_run,
                  dry_run: bool = False) -> bool:
    entry = cron_entry(sys.executable, tick_arguments(DISPATCH_FILE, state_path, tick_minutes),
                       tick_minutes)
    if dry_run:
        print(f"  [DRY RUN] crontab would gain:\n    " + "\n    ".join(build_cron_block(h, entry)))
        return True
    lines = read_crontab(run)
    if lines is None:
        print("Error reading crontab — cannot register.")
        return False
    # replace only OUR block: re-runs never duplicate, and legacy jobs stay
    # in place until the tick verifies (issue #1 §5)
    cleaned = _strip_own_blocks(lines, h)
    if not write_crontab(cleaned + build_cron_block(h, entry) + [""], run):
        print("Error writing crontab — registration failed.")
        return False
    print(f"  Registered crontab tick (every {tick_minutes} min, state {state_path})")
    return True

def verify_cron(h: str, run=_run) -> bool:
    lines = read_crontab(run)
    if lines is None:
        return False
    inside = False
    for line in lines:
        s = line.strip()
        if s == cron_begin(h):
            inside = True
        elif s == cron_end(h):
            inside = False
        elif inside and "dispatch.py" in line and " tick --tick-minutes " in line:
            return True
    return False

def _cron_block_entry(lines: list, h: str):
    """The dispatch entry inside our delimited block, verbatim (or None)."""
    inside = False
    for line in lines:
        s = line.strip()
        if s == cron_begin(h):
            inside = True
        elif s == cron_end(h):
            inside = False
        elif inside and "dispatch.py" in line:
            return line
    return None

def remove_legacy_cron(h: str, state_path, run=_run, dry_run: bool = False) -> int:
    """
    Remove legacy per-dose entries from the crontab. A verified cron tick
    block is kept (re-added verbatim); when the tick lives in launchd or
    systemd nothing cron-side is added back — one tick, one scheduler.
    Returns the count still outstanding (0 = clean, -1 = unreadable).
    """
    lines = read_crontab(run)
    if lines is None:
        print("  WARNING: could not read crontab — legacy entries left as-is.")
        return -1
    legacy = find_legacy_cron(lines, state_path, h)
    if not legacy:
        return 0
    if dry_run:
        for line in legacy:
            print(f"  [DRY RUN] crontab remove: {line.strip()}")
        return 0
    entry = _cron_block_entry(lines, h)                # keep the verified block …
    cleaned = strip_crontab(lines, state_path, h)      # … ours + legacy out …
    out = cleaned + (build_cron_block(h, entry) + [""] if entry else [])
    if not write_crontab(out, run):
        print("  WARNING: could not rewrite crontab — legacy entries remain.")
        return len(legacy)
    for line in legacy:
        print(f"  Removed legacy crontab line: {line.strip()}")
    return 0


# ── Windows Task Scheduler ────────────────────────────────────────────────────

def _pythonw() -> str:
    """pythonw.exe from sys.executable's directory — no console flash (issue #1 §5)."""
    cand = Path(sys.executable).parent / "pythonw.exe"
    return str(cand) if cand.exists() else sys.executable

def parse_task_folder_names(csv_text: str) -> list:
    """Task names inside \\MedReminder\\ parsed from `schtasks /query /fo csv /nh`."""
    names = []
    for row in csv.reader(io.StringIO(csv_text or "")):
        if row:
            name = row[0].strip()
            if name.startswith(f"\\{TASK_FOLDER}\\"):
                names.append(name)
    return names

def list_medreminder_tasks(run=_run):
    """Enumerate the folder live — the registry file is never trusted for cleanup."""
    r = run(["schtasks", "/query", "/fo", "csv", "/nh"])
    if r.returncode != 0:
        return None                                    # caller must not blind-delete
    return parse_task_folder_names(r.stdout)

def tick_task_xml(python: str, dispatch: str, state_path, tick_minutes: int,
                  start_date: str) -> str:
    """
    Task Scheduler 2.0 XML for the repeating tick. StartWhenAvailable gives
    missed-run catch-up on wake; battery settings are relaxed so laptops on
    battery still remind; IgnoreNew + the tick-instance lock make overlaps
    harmless; PT10M kills a hung tick (60s send timeout + tick lock means
    longer than 10 min is hung).
    """
    arguments = tick_arguments(dispatch, state_path, tick_minutes)
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>med-reminder tick every {tick_minutes} min</Description>
  </RegistrationInfo>
  <Triggers>
    <TimeTrigger>
      <StartBoundary>{start_date}T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
      <Repetition>
        <Interval>PT{tick_minutes}M</Interval>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
    </TimeTrigger>
  </Triggers>
  <Settings>
    <StartWhenAvailable>true</StartWhenAvailable>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <Enabled>true</Enabled>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{xml_escape(python)}</Command>
      <Arguments>{xml_escape(arguments)}</Arguments>
    </Exec>
  </Actions>
</Task>
"""

def register_windows(h: str, state_path, tick_minutes: int, run=_run,
                     dry_run: bool = False) -> bool:
    xml = tick_task_xml(_pythonw(), str(DISPATCH_FILE), state_path, tick_minutes,
                        datetime.now().strftime("%Y-%m-%d"))
    if dry_run:
        print(f"  [DRY RUN] schtasks /create /f /tn {tick_task_full_name(h)} /xml <tick>")
        return True
    # Task Scheduler's XML reader requires UTF-16 (with BOM) for /xml imports
    tmp = Path(tempfile.gettempdir()) / f"medreminder-tick-{h}.xml"
    tmp.write_text(xml, encoding="utf-16")
    try:
        r = run(["schtasks", "/create", "/f", "/tn", tick_task_full_name(h),
                 "/xml", str(tmp)])
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        print(f"  schtasks /create failed: {(r.stderr or '').strip()}")
        return False
    print(f"  Registered {tick_task_full_name(h)} (every {tick_minutes} min)")
    return True

def verify_windows(h: str, run=_run) -> bool:
    return run(["schtasks", "/query", "/tn", tick_task_full_name(h)]).returncode == 0

def remove_legacy_windows(h: str, run=_run, dry_run: bool = False) -> int:
    """
    Delete every task in \\MedReminder\\ except this state's tick. Returns the
    number of legacy tasks that could NOT be removed (0 = clean, -1 = the
    folder could not be enumerated).
    """
    names = list_medreminder_tasks(run)
    if names is None:
        print("  WARNING: could not enumerate \\" + TASK_FOLDER + "\\ — legacy tasks left as-is.")
        return -1
    keep = {tick_task_full_name(h)}
    remaining = 0
    for name in names:
        if name in keep:
            continue
        if dry_run:
            print(f"  [DRY RUN] schtasks /delete /tn {name} /f")
            continue
        r = run(["schtasks", "/delete", "/tn", name, "/f"])
        if r.returncode == 0:
            print(f"  Removed legacy task: {name}")
        else:
            print(f"  WARNING: could not remove {name}: {(r.stderr or '').strip()}")
            remaining += 1
    if not dry_run:
        LEGACY_REGISTRY_FILE.unlink(missing_ok=True)   # stale pre-PR3 registry
    return remaining


# ── macOS launchd user agent ──────────────────────────────────────────────────

def launchd_plist_path(label: str) -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"

def build_plist(label: str, python: str, dispatch: str, state_path,
                tick_minutes: int) -> str:
    args = "".join(f"    <string>{xml_escape(a)}</string>\n" for a in (
        python, dispatch, "--state", str(Path(state_path).resolve()),
        "tick", "--tick-minutes", str(tick_minutes)))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>{label}</string>
  <key>ProgramArguments</key>
  <array>
{args}  </array>
  <key>StartInterval</key>
  <integer>{tick_minutes * 60}</integer>
</dict>
</plist>
"""

def register_launchd(h: str, state_path, tick_minutes: int, run=_run,
                     dry_run: bool = False) -> bool:
    label = launchd_label(h)
    if dry_run:
        print(f"  [DRY RUN] launchd agent {label} (StartInterval {tick_minutes * 60}s)")
        return True
    plist = launchd_plist_path(label)
    plist.parent.mkdir(parents=True, exist_ok=True)
    plist.write_text(build_plist(label, sys.executable, str(DISPATCH_FILE),
                                 state_path, tick_minutes), encoding="utf-8")
    run(["launchctl", "unload", str(plist)])           # reload if it was already loaded
    r = run(["launchctl", "load", str(plist)])
    if r.returncode != 0:
        print(f"  launchctl load failed: {(r.stderr or '').strip()}")
        return False
    print(f"  Registered launchd agent {label} (StartInterval {tick_minutes * 60}s)")
    return True

def verify_launchd(h: str, run=_run) -> bool:
    return run(["launchctl", "list", launchd_label(h)]).returncode == 0


# ── Linux systemd user timer (opt-in: --scheduler systemd) ────────────────────

def systemd_unit_dir() -> Path:
    return Path.home() / ".config" / "systemd" / "user"

def build_service(unit: str, python: str, dispatch: str, state_path,
                  tick_minutes: int) -> str:
    return f"""[Unit]
Description=med-reminder tick ({unit})

[Service]
Type=oneshot
ExecStart={python} {dispatch} --state {Path(state_path).resolve()} tick --tick-minutes {tick_minutes}
"""

def build_timer(unit: str, tick_minutes: int) -> str:
    return f"""[Unit]
Description=med-reminder tick timer ({unit})

[Timer]
OnCalendar=*:0/{tick_minutes}
Persistent=true
Unit={unit}.service

[Install]
WantedBy=timers.target
"""

def register_systemd(h: str, state_path, tick_minutes: int, run=_run,
                     dry_run: bool = False) -> bool:
    unit = systemd_unit(h)
    if dry_run:
        print(f"  [DRY RUN] systemctl --user enable --now {unit}.timer "
              f"(OnCalendar=*:0/{tick_minutes})")
        return True
    d = systemd_unit_dir()
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{unit}.service").write_text(
        build_service(unit, sys.executable, str(DISPATCH_FILE), state_path, tick_minutes),
        encoding="utf-8")
    (d / f"{unit}.timer").write_text(build_timer(unit, tick_minutes), encoding="utf-8")
    if run(["systemctl", "--user", "daemon-reload"]).returncode != 0:
        print("  systemctl --user daemon-reload failed")
        return False
    r = run(["systemctl", "--user", "enable", "--now", f"{unit}.timer"])
    if r.returncode != 0:
        print(f"  systemctl enable failed: {(r.stderr or '').strip()}")
        return False
    print(f"  Registered systemd --user {unit}.timer (OnCalendar=*:0/{tick_minutes})")
    return True

def verify_systemd(h: str, run=_run) -> bool:
    return run(["systemctl", "--user", "is-enabled",
                f"{systemd_unit(h)}.timer"]).returncode == 0


# ── Register-verify-remove + clear (issue #1 §5) ──────────────────────────────

def migrate(h: str, state_path, tick_minutes: int, scheduler_hint: str = "cron",
            run=_run, dry_run: bool = False) -> int:
    """
    Register the tick, query it back, and only then remove legacy jobs.
    Any registration/verification failure leaves the legacy jobs in place,
    prints REMINDERS ARE NOT SCHEDULED and returns exit code 1.
    """
    is_windows = sys.platform == "win32"
    is_mac = sys.platform == "darwin"

    if dry_run:
        if is_windows:
            register_windows(h, state_path, tick_minutes, run, dry_run=True)
        elif is_mac:
            register_launchd(h, state_path, tick_minutes, run, dry_run=True)
        elif scheduler_hint == "systemd":
            register_systemd(h, state_path, tick_minutes, run, dry_run=True)
        else:
            register_cron(h, state_path, tick_minutes, run, dry_run=True)
        print("\nDry run complete. No changes made.")
        return 0

    scheduler = task = None

    if is_windows:
        if register_windows(h, state_path, tick_minutes, run) \
                and verify_windows(h, run):
            scheduler, task = "windows", tick_task_full_name(h)
    elif is_mac:
        # launchd first (cron can't get Full Disk Access on modern macOS);
        # cron is the fallback when launchd won't register or verify.
        if register_launchd(h, state_path, tick_minutes, run) \
                and verify_launchd(h, run):
            scheduler, task = "launchd", launchd_label(h)
        else:
            print("launchd unavailable — falling back to cron.")
            if register_cron(h, state_path, tick_minutes, run) \
                    and verify_cron(h, run):
                scheduler, task = "cron", "crontab"
    elif scheduler_hint == "systemd":
        if register_systemd(h, state_path, tick_minutes, run) \
                and verify_systemd(h, run):
            scheduler, task = "systemd", systemd_unit(h)
    else:
        if register_cron(h, state_path, tick_minutes, run) \
                and verify_cron(h, run):
            scheduler, task = "cron", "crontab"

    if scheduler is None:
        print("\nREMINDERS ARE NOT SCHEDULED")
        print("Registration or verification failed — legacy jobs were left in place.")
        return 1

    if is_windows:
        outstanding = remove_legacy_windows(h, run)
    else:
        # legacy jobs were crontab per-dose entries on every Unix flavor
        outstanding = remove_legacy_cron(h, state_path, run)

    save_registry(h, {
        "scheduler": scheduler,
        "task": task,
        "tick_minutes": tick_minutes,
        "state": str(Path(state_path).resolve()),
        "registered_utc": datetime.now(timezone.utc).isoformat(),
    })

    if outstanding == 0:
        print(f"\nTick scheduled every {tick_minutes} min via {scheduler} "
              f"(state: {state_path}).")
        print("Legacy per-dose jobs removed.")
    elif outstanding == -1:
        print(f"\nTick scheduled every {tick_minutes} min via {scheduler} "
              f"(state: {state_path}).")
        print("WARNING: legacy jobs could not be scanned — run doctor.py.")
    else:
        print(f"\nTick scheduled every {tick_minutes} min via {scheduler} "
              f"(state: {state_path}).")
        print(f"WARNING: {outstanding} legacy job(s) could not be removed — "
              "run doctor.py.")
    return 0


def _other_registered_windows_tasks(h: str) -> set:
    """Tick task names registered by OTHER state files (their registries)."""
    out = set()
    for p in SCRIPT_DIR.glob(".registered-tasks.*.json"):
        if p.name == registry_file(h).name:
            continue
        try:
            entry = json.loads(p.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if entry.get("scheduler") == "windows" and entry.get("task"):
            out.add(entry["task"])
    return out

def clear(h: str, state_path, run=_run, dry_run: bool = False) -> int:
    """Remove this state's tick and every legacy job. Other state files'
    ticks (found via their registries) are left alone."""
    if sys.platform == "win32":
        names = list_medreminder_tasks(run)
        if names is not None:
            protected = _other_registered_windows_tasks(h)
            for name in names:
                if name in protected:
                    continue
                if dry_run:
                    print(f"  [DRY RUN] schtasks /delete /tn {name} /f")
                    continue
                if run(["schtasks", "/delete", "/tn", name, "/f"]).returncode == 0:
                    print(f"  Removed: {name}")
                else:
                    print(f"  WARNING: could not remove {name}")
    else:
        lines = read_crontab(run)
        if lines is None:
            print("WARNING: crontab unreadable — cron entries left as-is.")
        else:
            cleaned = strip_crontab(lines, state_path, h)
            if dry_run or write_crontab(cleaned, run):
                if dry_run:
                    print("  [DRY RUN] crontab: MedReminder lines removed")
                else:
                    print("Removed MedReminder crontab lines.")
        # launchd / systemd registration (macOS / Linux opt-in)
        label, unit = launchd_label(h), systemd_unit(h)
        if not dry_run:
            run(["launchctl", "unload", str(launchd_plist_path(label))])
            launchd_plist_path(label).unlink(missing_ok=True)
            run(["systemctl", "--user", "disable", "--now", f"{unit}.timer"])
            (systemd_unit_dir() / f"{unit}.timer").unlink(missing_ok=True)
            (systemd_unit_dir() / f"{unit}.service").unlink(missing_ok=True)
    if not dry_run:
        registry_file(h).unlink(missing_ok=True)
        LEGACY_REGISTRY_FILE.unlink(missing_ok=True)   # stale pre-PR3 registry
        print("MedReminder scheduling cleared.")
    return 0


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Register the med reminder tick task (one entry per state file).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--tick-minutes", type=int, default=TICK_MINUTES_DEFAULT,
                        metavar="N",
                        help="tick cadence in minutes (default 5; 1-59, cron "
                             "minute-field limit)")
    parser.add_argument("--scheduler", choices=("cron", "systemd"), default="cron",
                        help="Linux scheduler: cron (default) or a systemd user "
                             "timer. Ignored on Windows/macOS.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would be registered without making changes")
    parser.add_argument("--clear", action="store_true",
                        help="Remove this state's tick and all legacy jobs, then exit")
    args = parser.parse_args()

    if not 1 <= args.tick_minutes <= 59:
        sys.exit("--tick-minutes must be 1-59 (cron minute-field limit)")
    if not STATE_FILE.exists():
        sys.exit(f"State file not found: {STATE_FILE}\n"
                 "Run: cp meds-state.template.json meds-state.json")
    if not DISPATCH_FILE.exists():
        sys.exit(f"dispatch.py not found: {DISPATCH_FILE}")

    h = state_hash(STATE_FILE)

    if args.clear:
        return clear(h, STATE_FILE, dry_run=args.dry_run)
    return migrate(h, STATE_FILE, args.tick_minutes, args.scheduler,
                   dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
