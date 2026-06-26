#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import subprocess
import sys


PRIORITY_MAP = {
    "none": 0,
    "low": 9,
    "medium": 5,
    "high": 1,
}

MONTH_MAP = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def run_applescript(lines: list[str]) -> subprocess.CompletedProcess[str]:
    cmd = ["osascript"]
    for line in lines:
        cmd.extend(["-e", line])
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def applescript_text_expr(text: str) -> str:
    if not text:
        return '""'
    parts = text.splitlines()
    return " & linefeed & ".join(f'"{escape(part)}"' for part in parts)


def due_lines(raw_due: str) -> list[str]:
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            parsed = dt.datetime.strptime(raw_due, fmt)
            break
        except ValueError:
            continue
    else:
        raise SystemExit(f"unsupported due format: {raw_due}")

    return [
        "set dueDate to current date",
        f"set year of dueDate to {parsed.year}",
        f"set month of dueDate to {MONTH_MAP[parsed.month]}",
        f"set day of dueDate to {parsed.day}",
        f"set hours of dueDate to {parsed.hour}",
        f"set minutes of dueDate to {parsed.minute}",
        f"set seconds of dueDate to {parsed.second}",
    ]


def ensure_list(list_name: str, account_name: str) -> None:
    escaped_list = escape(list_name)
    escaped_account = escape(account_name)
    script = [
        'tell application "Reminders"',
        f'if not (exists list "{escaped_list}") then',
        f'  tell account "{escaped_account}" to make new list with properties {{name:"{escaped_list}"}}',
        "end if",
        "end tell",
    ]
    proc = run_applescript(script)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or "failed to ensure list")


def not_found_error() -> int:
    print("NOT_FOUND", file=sys.stderr)
    return 2


def create_reminder(
    list_name: str,
    account_name: str,
    title: str,
    due: str | None,
    notes: str,
    priority: str,
) -> subprocess.CompletedProcess[str]:
    ensure_list(list_name, account_name)

    escaped_list = escape(list_name)
    escaped_title = escape(title)
    priority_value = PRIORITY_MAP[priority]

    script: list[str] = []
    if due:
        script.extend(due_lines(due))
    script.append(f"set noteText to {applescript_text_expr(notes)}")
    script.extend(
        [
            'tell application "Reminders"',
            f'set r to make new reminder at list "{escaped_list}" with properties {{name:"{escaped_title}"}}',
            "set body of r to noteText",
            f"set priority of r to {priority_value}",
        ]
    )
    if due:
        script.extend(
            [
                "set due date of r to dueDate",
                "set remind me date of r to dueDate",
            ]
        )
    script.extend(
        [
            'return id of r & tab & name of container of r & tab & name of r',
            "end tell",
        ]
    )
    return run_applescript(script)


def update_reminder(
    list_name: str,
    account_name: str,
    reminder_id: str,
    title: str,
    due: str | None,
    notes: str,
    priority: str,
) -> subprocess.CompletedProcess[str]:
    ensure_list(list_name, account_name)

    escaped_list = escape(list_name)
    escaped_id = escape(reminder_id)
    escaped_title = escape(title)
    priority_value = PRIORITY_MAP[priority]

    script: list[str] = []
    if due:
        script.extend(due_lines(due))
    script.append(f"set noteText to {applescript_text_expr(notes)}")
    script.extend(
        [
            'tell application "Reminders"',
            f'tell list "{escaped_list}"',
            f'set hits to (every reminder whose id is "{escaped_id}")',
            'if (count of hits) is 0 then error "NOT_FOUND"',
            "set r to item 1 of hits",
            f'set name of r to "{escaped_title}"',
            "set body of r to noteText",
            f"set priority of r to {priority_value}",
        ]
    )
    if due:
        script.extend(
            [
                "set due date of r to dueDate",
                "set remind me date of r to dueDate",
            ]
        )
    else:
        script.extend(
            [
                "set due date of r to missing value",
                "set remind me date of r to missing value",
            ]
        )
    script.extend(
        [
            'return id of r & tab & name of container of r & tab & name of r',
            "end tell",
            "end tell",
        ]
    )
    return run_applescript(script)


def delete_reminder(
    list_name: str,
    account_name: str,
    reminder_id: str,
) -> subprocess.CompletedProcess[str]:
    ensure_list(list_name, account_name)

    escaped_list = escape(list_name)
    escaped_id = escape(reminder_id)
    script = [
        'tell application "Reminders"',
        f'tell list "{escaped_list}"',
        f'set hits to (every reminder whose id is "{escaped_id}")',
        'if (count of hits) is 0 then error "NOT_FOUND"',
        "set r to item 1 of hits",
        "set deletedId to id of r",
        "delete r",
        "return deletedId",
        "end tell",
        "end tell",
    ]
    return run_applescript(script)


def add_reminder_cmd(args: argparse.Namespace) -> int:
    proc = create_reminder(
        list_name=args.list,
        account_name=args.account,
        title=args.title,
        due=args.due,
        notes=args.notes,
        priority=args.priority,
    )
    output = (proc.stdout or proc.stderr).strip()
    if output:
        print(output)
    return proc.returncode


def update_reminder_cmd(args: argparse.Namespace) -> int:
    proc = update_reminder(
        list_name=args.list,
        account_name=args.account,
        reminder_id=args.id,
        title=args.title,
        due=args.due,
        notes=args.notes,
        priority=args.priority,
    )
    output = (proc.stdout or proc.stderr).strip()
    if proc.returncode != 0 and "NOT_FOUND" in output:
        return not_found_error()
    if output:
        print(output)
    return proc.returncode


def delete_reminder_cmd(args: argparse.Namespace) -> int:
    proc = delete_reminder(
        list_name=args.list,
        account_name=args.account,
        reminder_id=args.id,
    )
    output = (proc.stdout or proc.stderr).strip()
    if proc.returncode != 0 and "NOT_FOUND" in output:
        return not_found_error()
    if output:
        print(output)
    return proc.returncode


def clear_list(args: argparse.Namespace) -> int:
    ensure_list(args.list, args.account)
    escaped_list = escape(args.list)
    script = [
        'tell application "Reminders"',
        f'tell list "{escaped_list}"',
        "set itemCount to count every reminder",
        "repeat while (count every reminder) > 0",
        "delete reminder 1",
        "end repeat",
        "return itemCount",
        "end tell",
        "end tell",
    ]
    proc = run_applescript(script)
    output = (proc.stdout or proc.stderr).strip()
    if output:
        print(output)
    return proc.returncode


def list_reminders(args: argparse.Namespace) -> int:
    ensure_list(args.list, args.account)
    escaped_list = escape(args.list)
    script = [
        'tell application "Reminders"',
        f'tell list "{escaped_list}"',
        "set rows to {}",
        "set theReminders to every reminder",
        "repeat with r in theReminders",
        "set end of rows to (id of r & tab & name of r)",
        "end repeat",
        'set AppleScript\'s text item delimiters to linefeed',
        "return rows as text",
        "end tell",
        "end tell",
    ]
    proc = run_applescript(script)
    output = (proc.stdout or proc.stderr).strip()
    if output:
        print(output)
    return proc.returncode


def sync_plan(args: argparse.Namespace) -> int:
    with open(args.file, "r", encoding="utf-8") as fh:
        plan = json.load(fh)

    list_name = args.list or plan.get("list", "OpenClaw")
    account_name = args.account or plan.get("account", "iCloud")

    if args.clear:
        clear_code = clear_list(argparse.Namespace(list=list_name, account=account_name))
        if clear_code != 0:
            return clear_code

    processed = plan.get("processed", {})
    for event_id, entry in processed.items():
        if entry.get("status") not in (None, "active"):
            continue
        note = entry.get("note", "")
        main = entry.get("mainReminder")
        if not main:
            continue

        proc = create_reminder(
            list_name=list_name,
            account_name=account_name,
            title=main["title"],
            due=main.get("due"),
            notes=note,
            priority=main.get("priority", "none"),
        )
        if proc.returncode != 0:
            output = (proc.stderr or proc.stdout).strip()
            if output:
                print(output, file=sys.stderr)
            return proc.returncode
        output = (proc.stdout or proc.stderr).strip()
        if output:
            print(f"{event_id}\tmain\t{output}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Native Apple Reminders bridge")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add = sub.add_parser("add")
    add.add_argument("--title", required=True)
    add.add_argument("--list", default="OpenClaw")
    add.add_argument("--account", default="iCloud")
    add.add_argument("--due")
    add.add_argument("--notes", default="")
    add.add_argument("--priority", choices=sorted(PRIORITY_MAP), default="none")
    add.set_defaults(func=add_reminder_cmd)

    update = sub.add_parser("update")
    update.add_argument("--id", required=True)
    update.add_argument("--title", required=True)
    update.add_argument("--list", default="OpenClaw")
    update.add_argument("--account", default="iCloud")
    update.add_argument("--due")
    update.add_argument("--notes", default="")
    update.add_argument("--priority", choices=sorted(PRIORITY_MAP), default="none")
    update.set_defaults(func=update_reminder_cmd)

    delete = sub.add_parser("delete")
    delete.add_argument("--id", required=True)
    delete.add_argument("--list", default="OpenClaw")
    delete.add_argument("--account", default="iCloud")
    delete.set_defaults(func=delete_reminder_cmd)

    clear = sub.add_parser("clear-list")
    clear.add_argument("--list", default="OpenClaw")
    clear.add_argument("--account", default="iCloud")
    clear.set_defaults(func=clear_list)

    ls = sub.add_parser("list")
    ls.add_argument("--list", default="OpenClaw")
    ls.add_argument("--account", default="iCloud")
    ls.set_defaults(func=list_reminders)

    sync = sub.add_parser("sync-plan")
    sync.add_argument("--file", required=True)
    sync.add_argument("--list")
    sync.add_argument("--account")
    sync.add_argument("--clear", action="store_true")
    sync.set_defaults(func=sync_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
