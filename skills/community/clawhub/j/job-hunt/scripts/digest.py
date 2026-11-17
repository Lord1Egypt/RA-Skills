#!/usr/bin/env python3
"""Weekly job digest: state, schedule and the deterministic steps around one run.

An hourly scheduler entry calls `tick`; it starts the agent only when a digest is
due. The agent runs a discover round on no-login sources, then uses `inbox`,
`compose` and `sent` here. Procedure: references/weekly-digest.md. Design:
docs/superpowers/specs/2026-11-02-weekly-digest-design.md.
"""
from __future__ import annotations

import argparse
import datetime
import os
import pathlib
import plistlib
import shlex
import subprocess
import sys
import tempfile

import journal
import paths

LOCK_STALE = datetime.timedelta(hours=3)
MIN_GAP = datetime.timedelta(days=6)
ATTEMPTS_PER_DAY = 3
UNCONFIRMED_AFTER = datetime.timedelta(hours=3)
DEFAULT_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
STUCK_AFTER_DAYS = 3


def empty_settings() -> dict:
    return {"enabled": False, "cancelled": None, "paused_until": None,
            "schedule": None, "recipient": None, "transport": "email",
            "budget_usd": None, "agent": None, "standing_brief": None,
            "last_sent": None, "threads": [], "processed_messages": [],
            "attempts": {}, "failed_days": [], "stuck_until": None,
            "pending_questions": [], "answers": [], "pending_send": None,
            "sent_digests": {}, "sent_subjects": {}, "setup_at": None}


def load_settings(name: str) -> dict:
    """The settings, or a disabled empty shape when absent. Unreadable raises YamlUnreadable."""
    path = paths.digest_settings(name)
    settings = empty_settings()
    if path.exists():
        settings.update(journal.load_yaml(path))
    return settings


def save_settings(name: str, data: dict) -> None:
    import yaml
    path = paths.digest_settings(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    full = empty_settings()
    full.update(data)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".digest-", suffix=".yaml")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        yaml.safe_dump(full, fh, allow_unicode=True, sort_keys=False)
    os.replace(tmp, path)


def _parse_dt(value):
    if not value:
        return None
    return datetime.datetime.fromisoformat(str(value))


def next_slot(schedule: dict, start: datetime.datetime) -> datetime.datetime:
    """The first scheduled weekday/hour at or after `start` (local time, minute 0)."""
    weekday, hour = int(schedule["weekday"]), int(schedule["hour"])
    if not (0 <= weekday <= 6 and 0 <= hour <= 23):
        raise ValueError(f"schedule needs weekday 0-6 and hour 0-23, got {schedule!r}")
    day = start.replace(minute=0, second=0, microsecond=0, hour=hour)
    day += datetime.timedelta(days=(weekday - day.weekday()) % 7)
    if day < start:
        day += datetime.timedelta(days=7)
    return day


def due(settings: dict, now: datetime.datetime) -> tuple[bool, str]:
    """(is a digest due now, why). Reasons other than "due" say what holds it back."""
    if settings.get("cancelled"):
        return False, "cancelled"
    if not settings.get("enabled"):
        return False, "disabled"
    paused = settings.get("paused_until")
    if paused and now.date() < datetime.date.fromisoformat(str(paused)):
        return False, "paused"
    stuck = _parse_dt(settings.get("stuck_until"))
    if stuck and now < stuck:
        return False, "stuck"
    if int((settings.get("attempts") or {}).get(now.date().isoformat(), 0)) >= ATTEMPTS_PER_DAY:
        return False, "attempt_cap"
    reminded = _parse_dt(settings.get("reminded_at"))
    if reminded is not None:
        wait = REASK_AFTER_START if settings.get("reminder_outcome") in ("started", "notified") else REASK_AFTER
        if now - reminded < wait:
            return False, "reminded"
    pending = settings.get("pending_send")
    if pending:
        # A digest was recorded as about to be sent and never confirmed: the run
        # crashed between presend and sent. The next run must find out whether the
        # email left (confirm it) or not (roll back), never send a second copy blind.
        at = _parse_dt(pending.get("at"))
        if at is None or now - at >= UNCONFIRMED_AFTER:
            return True, "unconfirmed_send"
        return False, "sending"
    last = _parse_dt(settings.get("last_sent"))
    if last is None:
        setup_at = _parse_dt(settings.get("setup_at"))
        if setup_at is None or now >= next_slot(settings["schedule"], setup_at):
            return True, "due"
        return False, "not_yet"
    if now >= next_slot(settings["schedule"], last + MIN_GAP):
        return True, "due"
    return False, "not_yet"


def record_attempt(name: str, now: datetime.datetime, ok: bool) -> None:
    """Count one run; three failed days in a row park the digest until the next slot."""
    settings = load_settings(name)
    today = now.date().isoformat()
    attempts = dict(settings.get("attempts") or {})
    attempts[today] = int(attempts.get(today, 0)) + 1
    # Only the last week of counts matters to the due rule.
    settings["attempts"] = {d: n for d, n in attempts.items()
                            if (now.date() - datetime.date.fromisoformat(d)).days < 7}
    if ok:
        settings["failed_days"], settings["stuck_until"] = [], None
    else:
        days = list(settings.get("failed_days") or [])
        if days and (now.date() - datetime.date.fromisoformat(days[-1])).days > 1:
            days = []
        if today not in days:
            days.append(today)
        settings["failed_days"] = days
        if len(days) >= STUCK_AFTER_DAYS and settings.get("schedule"):
            settings["stuck_until"] = next_slot(
                settings["schedule"], now + datetime.timedelta(seconds=1)).isoformat(timespec="minutes")
    save_settings(name, settings)


def _lock_path(name: str) -> pathlib.Path:
    return paths.profile_dir(name) / "digest.lock"


def acquire_lock(name: str, now: datetime.datetime) -> bool:
    path = _lock_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                held = datetime.datetime.fromisoformat(path.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                held = None
            if held is not None and now - held < LOCK_STALE:
                return False
            path.unlink(missing_ok=True)  # stale or unreadable: a crashed run left it
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(now.isoformat())
        return True
    return False


def release_lock(name: str) -> None:
    _lock_path(name).unlink(missing_ok=True)


def _answer(settings: dict, field: str, words: str, today: datetime.date) -> None:
    settings.setdefault("answers", []).append(
        {"date": today.isoformat(), "field": field, "words": words})


def cancel(name: str, words: str, today: datetime.date) -> None:
    settings = load_settings(name)
    settings["cancelled"] = {"date": today.isoformat(), "words": words}
    settings["enabled"] = False
    _answer(settings, "cancel", words, today)
    save_settings(name, settings)


def pause(name: str, weeks: int, words: str, today: datetime.date) -> None:
    if int(weeks) < 1:
        raise ValueError("pause needs at least one week")
    settings = load_settings(name)
    settings["paused_until"] = (today + datetime.timedelta(weeks=int(weeks))).isoformat()
    _answer(settings, "pause", words, today)
    save_settings(name, settings)


REASK_AFTER = datetime.timedelta(hours=3)
REASK_AFTER_START = datetime.timedelta(hours=12)
DIALOG_SECONDS = 1800
QUESTION = {"zh": "现在运行本周的求职推送吗？会打开一个 Claude Code 会话。",
            "en": "Run this week's job digest now? It opens a Claude Code session."}
PROMPT = ("Run the job-hunt weekly digest for {name}: read {skill}/references/weekly-digest.md "
          "and follow its section 'The run'. I am here if a page needs my consent or a login.")


def _slug(name: str) -> str:
    slug = paths.slugify(name)
    if not slug:
        raise ValueError(f"{name!r} has no letters or digits to name a schedule after")
    return slug


def log_path(name: str) -> pathlib.Path:
    return paths.profile_dir(name) / "digest-runs.log"


def notify(title: str, message: str) -> None:
    """A desktop notification; never raises (a failed notice must not hide the failure log)."""
    try:
        if sys.platform == "darwin":
            script = 'display notification {} with title {}'.format(
                _applescript(message), _applescript(title))
            subprocess.run(["osascript", "-e", script], check=False, timeout=10,
                           capture_output=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["notify-send", title, message], check=False, timeout=10,
                           capture_output=True)
    except (OSError, subprocess.SubprocessError):
        pass


def _applescript(text: str) -> str:
    return '"' + str(text).replace("\\", "\\\\").replace('"', '\\"') + '"'


def _log(name: str, line: str) -> None:
    path = log_path(name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now().isoformat(timespec='seconds')} {line}\n")



def session_command(settings: dict, name: str, skill_root, profiles_root) -> str:
    """The shell line that starts an interactive agent session for this week's digest."""
    agent = settings.get("agent") or {}
    command, cwd = agent.get("command"), agent.get("cwd")
    if not command or not os.path.isabs(str(command)) or not cwd or not os.path.isabs(str(cwd)):
        raise ValueError("digest.yaml agent.command and agent.cwd must be absolute paths")
    prompt = PROMPT.format(name=name, skill=pathlib.Path(skill_root))
    return (f"cd {shlex.quote(str(cwd))} && JOBHUNT_PROFILES_ROOT={shlex.quote(str(profiles_root))} "
            f"{shlex.quote(str(command))} {shlex.quote(prompt)}")


def ask_user(question: str, platform: str = sys.platform, run=subprocess.run) -> str:
    """"run" | "later" | "no_answer". macOS shows a dialog; elsewhere there is none to show."""
    if platform != "darwin":
        return "run"  # launch_session then sends a notification with the command
    script = (f"display dialog {_applescript(question)} with title \"job-hunt\" "
              f"buttons {{\"Later\", \"Run now\"}} default button \"Run now\" "
              f"giving up after {DIALOG_SECONDS}")
    try:
        result = run(["osascript", "-e", script], capture_output=True, text=True,
                     timeout=DIALOG_SECONDS + 120, check=False)
    except (OSError, subprocess.SubprocessError):
        return "later"
    out = getattr(result, "stdout", "") or ""
    if getattr(result, "returncode", 1) != 0:
        return "later"  # the dialog was closed or could not be shown
    if "gave up:true" in out:
        return "no_answer"
    return "run" if "button returned:Run now" in out else "later"


def launch_session(command: str, platform: str = sys.platform, run=subprocess.run, notify=notify) -> str:
    """Open the session in a terminal the user can see: "started", "notified" or "failed"."""
    if platform == "darwin":
        script = ('tell application "Terminal"\n  activate\n  do script '
                  f'{_applescript(command)}\nend tell')
        try:
            result = run(["osascript", "-e", script], capture_output=True, text=True, timeout=60,
                         check=False)
        except (OSError, subprocess.SubprocessError):
            return "failed"
        return "started" if getattr(result, "returncode", 1) == 0 else "failed"
    notify("job-hunt weekly digest", f"Run this week's digest in a terminal: {command}")
    return "notified"


def tick(name: str, now: datetime.datetime, ask=None, launch=None, notify=notify) -> str:
    """At the weekly slot, ask the user; on "Run now" open an interactive session. Cheap otherwise."""
    settings = load_settings(name)
    ok, reason = due(settings, now)
    if not ok:
        return f"not_due:{reason}"
    if not acquire_lock(name, now):
        return "locked"
    ask = ask or (lambda question: ask_user(question))
    launch = launch or (lambda command, platform: launch_session(command, platform))
    try:
        question = QUESTION.get(settings.get("language") or "en", QUESTION["en"])
        outcome = ask(question)
        if outcome == "run":
            try:
                command = session_command(settings, name, paths.SKILL_ROOT, paths.PROFILES_ROOT)
                outcome = launch(command, sys.platform)
            except ValueError as exc:
                outcome = "failed"
                _log(name, f"cannot start the session: {exc}")
        settings = load_settings(name)
        settings["reminded_at"] = now.isoformat(timespec="minutes")
        settings["reminder_outcome"] = outcome
        save_settings(name, settings)
        was_stuck = settings.get("stuck_until")
        record_attempt(name, now, ok=False)  # cleared when `sent` confirms a digest
        stuck = load_settings(name).get("stuck_until")
        if stuck and not was_stuck:
            notify("job-hunt weekly digest",
                   f"No digest for three days, so I stopped reminding until {stuck}. "
                   "Ask job-hunt in a conversation to run it sooner.")
        _log(name, f"reminder: {outcome}")
        if outcome == "failed":
            notify("job-hunt weekly digest", f"Could not open the digest session. Log: {log_path(name)}")
        return outcome
    finally:
        release_lock(name)


def scheduler_entry(name: str, platform: str, python, skill_root, profiles_root,
                    path: str = DEFAULT_PATH) -> str:
    """launchd plist (macOS) or crontab lines (Linux) that run `tick` every hour.

    Absolute paths only: launchd and cron start with a minimal environment.
    """
    slug = _slug(name)
    script = f"{pathlib.Path(skill_root)}/scripts/digest.py"
    log = str(pathlib.Path(profiles_root) / slug / "digest-runs.log")
    if platform == "darwin":
        return plistlib.dumps({
            "Label": f"com.jobhunt.digest.{slug}",
            "ProgramArguments": [str(python), script, "tick", "--name", name],
            "StartInterval": 3600, "RunAtLoad": True,
            "EnvironmentVariables": {"JOBHUNT_PROFILES_ROOT": str(profiles_root),
                                     "PATH": path},
            "StandardOutPath": log, "StandardErrorPath": log,
        }).decode()
    if platform.startswith("linux"):
        command = (f"PATH={shlex.quote(path)} JOBHUNT_PROFILES_ROOT={shlex.quote(str(profiles_root))} "
                   f"{shlex.quote(str(python))} {shlex.quote(script)} tick --name {shlex.quote(name)} "
                   f">> {shlex.quote(log)} 2>&1 # job-hunt digest {slug}")
        return f"0 * * * * {command}\n@reboot {command}\n"
    raise ValueError(f"no scheduler for platform {platform!r}; macOS and Linux only")


def _plist_path(name: str) -> pathlib.Path:
    return pathlib.Path(os.path.expanduser("~")) / "Library" / "LaunchAgents" / \
        f"com.jobhunt.digest.{_slug(name)}.plist"


def _without_ours(table: str, name: str) -> str:
    marker = f"# job-hunt digest {_slug(name)}"
    return "".join(line for line in table.splitlines(keepends=True) if not line.rstrip().endswith(marker))


def install(name: str, platform: str = sys.platform, run=subprocess.run):
    settings = load_settings(name)
    agent = settings.get("agent") or {}
    python = agent.get("python") or sys.executable
    entry = scheduler_entry(name, platform, python, paths.SKILL_ROOT, paths.PROFILES_ROOT,
                            path=agent.get("path") or DEFAULT_PATH)
    if platform == "darwin":
        plist = _plist_path(name)
        plist.parent.mkdir(parents=True, exist_ok=True)
        plist.write_text(entry, encoding="utf-8")
        domain = f"gui/{os.getuid()}"
        run(["launchctl", "bootout", f"{domain}/com.jobhunt.digest.{_slug(name)}"], check=False,
            capture_output=True)
        result = run(["launchctl", "bootstrap", domain, str(plist)], check=False, capture_output=True)
        if getattr(result, "returncode", 0) != 0:
            raise ValueError(f"launchctl bootstrap failed: {getattr(result, 'stderr', '')}")
        return plist
    current = run(["crontab", "-l"], check=False, capture_output=True, text=True)
    table = current.stdout if getattr(current, "returncode", 1) == 0 else ""
    table = _without_ours(table, name)
    if table and not table.endswith("\n"):
        table += "\n"
    result = run(["crontab", "-"], input=table + entry, check=False, capture_output=True, text=True)
    if getattr(result, "returncode", 0) != 0:
        raise ValueError(f"crontab update failed: {getattr(result, 'stderr', '')}")
    return pathlib.Path("crontab")


def uninstall(name: str, platform: str = sys.platform, run=subprocess.run) -> None:
    if platform == "darwin":
        run(["launchctl", "bootout", f"gui/{os.getuid()}/com.jobhunt.digest.{_slug(name)}"],
            check=False, capture_output=True)
        _plist_path(name).unlink(missing_ok=True)
        return
    current = run(["crontab", "-l"], check=False, capture_output=True, text=True)
    if getattr(current, "returncode", 1) != 0:
        return
    run(["crontab", "-"], input=_without_ours(current.stdout, name), check=False,
        capture_output=True, text=True)


def setup(name: str, args, today: datetime.date) -> None:
    """Validate everything first, then write once: a refused setup leaves no file."""
    import re
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", args.recipient.strip()):
        raise ValueError(f"{args.recipient!r} is not an email address")
    next_slot({"weekday": args.weekday, "hour": args.hour}, datetime.datetime.now())
    for label, value in (("--agent-command", args.agent_command), ("--python", args.python),
                         ("--agent-cwd", args.agent_cwd)):
        if not os.path.isabs(value):
            raise ValueError(f"{label} must be an absolute path, got {value!r}")
    brief = journal.load_yaml(args.brief)
    settings = load_settings(name)
    settings.update(enabled=True, cancelled=None, recipient=args.recipient.strip(),
                    schedule={"weekday": args.weekday, "hour": args.hour},
                    language=args.language, transport=args.transport, standing_brief=brief,
                    agent={"command": args.agent_command, "cwd": args.agent_cwd, "python": args.python,
                           "path": args.path or os.environ.get("PATH", DEFAULT_PATH)},
                    setup_at=datetime.datetime.now().isoformat(timespec="minutes"))
    session_command(settings, name, paths.SKILL_ROOT, paths.PROFILES_ROOT)  # refuses bad paths first
    _answer(settings, "setup", args.words, today)
    save_settings(name, settings)


def _run_workspace(name: str, workspace) -> pathlib.Path:
    """A digest run's workspace must be one of this person's discover workspaces."""
    workspace = pathlib.Path(workspace).resolve()
    searches = (paths.profile_dir(name) / "searches").resolve()
    if workspace.parent != searches or not workspace.is_dir():
        raise ValueError(f"{workspace} is not a discover workspace under {searches}")
    return workspace


def presend(name: str, workspace, now: datetime.datetime) -> dict:
    """Record the digest as sent BEFORE the email tool sends it; returns the email.

    Recording first means a run that dies after sending cannot send the same roles
    again next hour. The record is provisional (`pending_send`) until `sent` confirms
    it or `send-failed` rolls it back; an unconfirmed one makes the next run check
    the Sent folder first (due(): "unconfirmed_send").
    """
    import json
    import shutil
    import digest_compose
    import digest_ledger
    workspace = pathlib.Path(workspace)
    settings = load_settings(name)
    if settings.get("pending_send"):
        raise ValueError(f"an earlier send is unconfirmed ({settings['pending_send'].get('workspace')}); "
                         "confirm it with `sent` or roll it back with `send-failed` first")
    mail = json.loads((workspace / "digest-email.json").read_text(encoding="utf-8"))
    ledger_path = paths.digest_seen(name)
    before = workspace / "digest-ledger-before.yaml"
    if ledger_path.exists():
        shutil.copy2(ledger_path, before)
    else:
        before.write_text("roles: []\n", encoding="utf-8")
    _, _, rows = digest_compose.load_inputs(workspace)
    sent_rows = [rows[i] for i in mail.get("role_ids") or [] if i in rows]
    ledger = digest_ledger.load_ledger(name)
    digest_ledger.save_ledger(name, digest_ledger.prune(
        digest_ledger.record_sent(ledger, sent_rows, now.date()), now.date()))
    settings["pending_send"] = {"workspace": str(workspace), "subject": mail["subject"],
                                "at": now.isoformat(timespec="minutes"),
                                "previous_last_sent": settings.get("last_sent"),
                                "previous_questions": [dict(q) for q in settings.get("pending_questions") or []]}
    settings["last_sent"] = now.isoformat(timespec="minutes")
    shown = set(mail.get("question_ids") or [])
    for question in settings.get("pending_questions") or []:
        if question.get("id") in shown:
            question["asked"] = int(question.get("asked", 0)) + 1
    save_settings(name, settings)
    journal.append(workspace, {"action": "digest_presend", "subject": mail["subject"],
                               "roles": mail.get("role_ids"), "date": now.isoformat(timespec="minutes")})
    return mail


def _pending_for(settings: dict, workspace: pathlib.Path) -> dict:
    pending = settings.get("pending_send")
    if not pending or pathlib.Path(pending.get("workspace", "")).resolve() != workspace.resolve():
        raise ValueError(f"no unconfirmed send for {workspace}; run `presend` before sending")
    return pending


def confirm_sent(name: str, workspace, message_id, thread_id) -> None:
    import json
    workspace = pathlib.Path(workspace)
    settings = load_settings(name)
    pending = _pending_for(settings, workspace)
    mail = json.loads((workspace / "digest-email.json").read_text(encoding="utf-8"))
    labels = list(mail.get("role_labels") or [])
    if thread_id:
        threads = [t for t in settings.get("threads") or [] if t != thread_id] + [thread_id]
        settings["threads"] = threads[-20:]
        sent = dict(settings.get("sent_digests") or {})
        sent[thread_id] = labels
        settings["sent_digests"] = {t: sent[t] for t in settings["threads"] if t in sent}
    subjects = dict(settings.get("sent_subjects") or {})
    subjects[pending["subject"]] = labels
    settings["sent_subjects"] = dict(list(subjects.items())[-20:])
    settings["pending_send"] = None
    settings["failed_days"], settings["stuck_until"] = [], None
    settings["reminded_at"] = settings["reminder_outcome"] = None
    save_settings(name, settings)
    journal.append(workspace, {"action": "digest_sent", "message_id": message_id, "thread_id": thread_id,
                               "roles": mail.get("role_ids"), "subject": pending["subject"]})


def rollback_send(name: str, workspace, reason: str) -> None:
    import shutil
    workspace = pathlib.Path(workspace)
    settings = load_settings(name)
    pending = _pending_for(settings, workspace)
    before = workspace / "digest-ledger-before.yaml"
    if before.exists():
        shutil.copy2(before, paths.digest_seen(name))
    settings["last_sent"] = pending.get("previous_last_sent")
    settings["pending_questions"] = pending.get("previous_questions") or []
    settings["pending_send"] = None
    save_settings(name, settings)
    journal.append(workspace, {"action": "digest_send_failed", "reason": reason})
    _log(name, f"send rolled back: {reason}")


def status_report(name: str, now: datetime.datetime) -> dict:
    settings = load_settings(name)
    is_due, reason = due(settings, now)
    return {"due": is_due, "reason": reason, "pending_send": settings.get("pending_send"),
            "last_sent": settings.get("last_sent"), "paused_until": settings.get("paused_until"),
            "cancelled": settings.get("cancelled"), "recipient": settings.get("recipient"),
            "transport": settings.get("transport")}


def _write_file(workspace, today: datetime.date) -> pathlib.Path:
    import html
    import json
    mail = json.loads((pathlib.Path(workspace) / "digest-email.json").read_text(encoding="utf-8"))
    folder = pathlib.Path(os.path.expanduser("~")) / "Downloads" / "job-digest"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{today.isoformat()}.html"
    path.write_text("<!doctype html><meta charset=\"utf-8\"><title>{}</title><pre style=\"font: 15px/1.5 "
                    "system-ui; white-space: pre-wrap; max-width: 46em\">{}</pre>\n".format(
                        html.escape(mail["subject"]), html.escape(mail["body"])), encoding="utf-8")
    notify("job-hunt weekly digest", f"This week's digest is ready: {path}")
    return path


def _parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    tk = sub.add_parser("tick", help="at the weekly slot, ask the user and open the digest session")
    tk.add_argument("--name", required=True)
    for cmd, text in (("install", "add the hourly scheduler entry"),
                      ("uninstall", "remove the scheduler entry")):
        sp = sub.add_parser(cmd, help=text)
        sp.add_argument("--name", required=True)
    cn = sub.add_parser("cancel", help="stop the digest for good (the user's words are kept)")
    cn.add_argument("--name", required=True)
    cn.add_argument("--words", required=True)
    cn.add_argument("--no-uninstall", action="store_true", help="keep the scheduler entry (tests)")
    ib = sub.add_parser("inbox", help="apply the user's replies (cancel / pause / feedback / yes)")
    ib.add_argument("--name", required=True)
    group = ib.add_mutually_exclusive_group(required=True)
    group.add_argument("--messages", type=pathlib.Path,
                       help="JSON list of {id, thread_id, from, date, body} found by the email tool")
    group.add_argument("--unreadable", metavar="REASON",
                       help="the inbox could not be read: stop, notify, send nothing")
    su = sub.add_parser("setup", help="record the user's digest answers and enable it")
    su.add_argument("--name", required=True)
    su.add_argument("--recipient", required=True, help="the user's own address")
    su.add_argument("--weekday", required=True, type=int, help="0=Monday … 6=Sunday")
    su.add_argument("--hour", required=True, type=int, help="0-23, local time")
    su.add_argument("--brief", required=True, type=pathlib.Path, help="the discover brief.yaml to reuse")
    su.add_argument("--language", required=True, choices=("zh", "en"))
    su.add_argument("--agent-command", required=True, help="absolute path of the agent binary")
    su.add_argument("--agent-cwd", required=True, help="directory whose config holds the email tool")
    su.add_argument("--python", required=True, help="absolute path of the prepared interpreter")
    su.add_argument("--transport", choices=("email", "file"), default="email")
    su.add_argument("--path", help="PATH for scheduled runs (default: this shell's PATH, which finds "
                                   "the agent, node/npx for its email tool, and opencli)")
    su.add_argument("--words", required=True, help="the user's answers, verbatim")
    wk = sub.add_parser("workspace", help="create and print a fresh workspace for this run")
    wk.add_argument("--name", required=True)
    wk.add_argument("--today")
    fl = sub.add_parser("filter", help="print the shortlist row ids not sent in an earlier digest")
    fl.add_argument("--name", required=True)
    fl.add_argument("--workspace", required=True, type=pathlib.Path)
    cp = sub.add_parser("compose", help="render digest-email.json/.txt from the run's picks and sources")
    cp.add_argument("--name", required=True)
    cp.add_argument("--workspace", required=True, type=pathlib.Path)
    cp.add_argument("--today")
    pr = sub.add_parser("presend", help="gate the email and record it as sent, just before sending")
    pr.add_argument("--name", required=True)
    pr.add_argument("--workspace", required=True, type=pathlib.Path)
    st = sub.add_parser("sent", help="after the email tool sent it: confirm the presend record")
    st.add_argument("--name", required=True)
    st.add_argument("--workspace", required=True, type=pathlib.Path)
    st.add_argument("--message-id", required=True)
    st.add_argument("--thread-id", help="the Gmail thread id, when the tool reports one")
    sf = sub.add_parser("send-failed", help="the email did not go out: roll the presend record back")
    sf.add_argument("--name", required=True)
    sf.add_argument("--workspace", required=True, type=pathlib.Path)
    sf.add_argument("--reason", required=True)
    ss = sub.add_parser("status", help="print whether a digest is due and any unconfirmed send")
    ss.add_argument("--name", required=True)
    df = sub.add_parser("deliver-file", help="no email tool: write the digest to ~/Downloads/job-digest/ and record it")
    df.add_argument("--name", required=True)
    df.add_argument("--workspace", required=True, type=pathlib.Path)
    ps = sub.add_parser("pause", help="pause the digest for N weeks")
    ps.add_argument("--name", required=True)
    ps.add_argument("--weeks", required=True, type=int)
    ps.add_argument("--words", required=True)
    return ap


def main(argv=None) -> int:
    ap = _parser()
    ap.epilog = "subcommands:\n" + "\n".join(
        "  " + parser.format_usage().replace("usage: ", "").strip()
        for parser in ap._subparsers._group_actions[0].choices.values())
    args = ap.parse_args(argv)
    today = datetime.date.today()
    try:
        if args.command == "tick":
            print(tick(args.name, datetime.datetime.now()))
        elif args.command == "install":
            print(install(args.name))
        elif args.command == "uninstall":
            uninstall(args.name)
        elif args.command == "cancel":
            cancel(args.name, args.words, today)
            if not args.no_uninstall:
                uninstall(args.name)
        elif args.command == "inbox":
            import json
            if args.unreadable:
                _log(args.name, f"inbox unreadable, nothing sent: {args.unreadable}")
                notify("job-hunt weekly digest",
                       f"Could not read your inbox, so nothing was sent this time: {args.unreadable}")
                print(json.dumps({"action": "stop", "reason": args.unreadable}, ensure_ascii=False))
                return 0
            import digest_inbox
            messages = json.loads(args.messages.read_text(encoding="utf-8"))
            if not isinstance(messages, list):
                raise ValueError(f"{args.messages}: expected a JSON list of messages")
            print(json.dumps(digest_inbox.apply_messages(args.name, messages, today), ensure_ascii=False))
        elif args.command == "setup":
            setup(args.name, args, today)
        elif args.command == "workspace":
            day = args.today or today.isoformat()
            path = paths.digest_workspace(args.name, day)
            path.mkdir(parents=True)
            print(path)
        elif args.command == "filter":
            import json
            import digest_compose
            import digest_ledger
            shortlist = journal.load_yaml(_run_workspace(args.name, args.workspace) / "shortlist.yaml")
            rows = [r for r in shortlist.get("rows") or [] if isinstance(r, dict)]
            fresh = digest_ledger.filter_new(rows, digest_ledger.load_ledger(args.name))
            print(json.dumps({"new": [r.get("id") for r in fresh]}, ensure_ascii=False))
        elif args.command == "compose":
            import digest_compose
            day = datetime.date.fromisoformat(args.today) if args.today else today
            mail = digest_compose.compose(load_settings(args.name), _run_workspace(args.name, args.workspace), day)
            print(mail["subject"])
        elif args.command in ("presend", "deliver-file"):
            import json
            workspace = _run_workspace(args.name, args.workspace)
            import check_digest
            if check_digest.main(["--workspace", str(workspace), "--name", args.name]) != 0:
                print("DIGEST_NOT_RECORDED: the gate failed; nothing was recorded — do not send",
                      file=sys.stderr)
                return 1
            mail = presend(args.name, workspace, datetime.datetime.now())
            if args.command == "deliver-file":
                print(_write_file(workspace, today))
                confirm_sent(args.name, workspace, None, None)
            else:
                print(json.dumps({k: mail[k] for k in ("to", "subject", "body")}, ensure_ascii=False))
        elif args.command == "sent":
            confirm_sent(args.name, _run_workspace(args.name, args.workspace), args.message_id, args.thread_id)
        elif args.command == "send-failed":
            rollback_send(args.name, _run_workspace(args.name, args.workspace), args.reason)
        elif args.command == "status":
            import json
            print(json.dumps(status_report(args.name, datetime.datetime.now()), ensure_ascii=False))
        elif args.command == "pause":
            pause(args.name, args.weeks, args.words, today)
        return 0
    except journal.YamlUnreadable as exc:
        print(f"DIGEST_UNREADABLE: {exc}; fix or remove the file — it was not changed", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"DIGEST_BAD_INPUT: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    from cli_io import configure_output
    configure_output()
    raise SystemExit(main())
