#!/usr/bin/env python3
import json
import subprocess


def run_script(lines: list[str]) -> str:
    cmd = ["osascript"]
    for line in lines:
        cmd.extend(["-e", line])
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if proc.returncode != 0:
        raise SystemExit(proc.stderr.strip() or proc.stdout.strip() or "list mail sources failed")
    return proc.stdout


def main() -> int:
    script = [
        'set output to ""',
        'tell application "Mail"',
        'repeat with acc in every account',
        'set accName to name of acc as string',
        'repeat with box in mailboxes of acc',
        'set boxName to name of box as string',
        'set output to output & accName & tab & boxName & linefeed',
        'end repeat',
        'end repeat',
        'end tell',
        'return output',
    ]
    raw = run_script(script)
    rows = []
    seen = set()
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        key = tuple(parts)
        if key in seen:
            continue
        seen.add(key)
        rows.append({"account": parts[0], "mailbox": parts[1]})
    print(json.dumps(rows, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
