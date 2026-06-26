#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path


def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)


def env(name: str, default: str) -> str:
    return os.environ.get(name, default)


VAULT_ROOT = Path(env("NOTES_VAULT_ROOT", "/root/obsidian-vault"))
BACKUP_SCRIPT = env("NOTES_BACKUP_SCRIPT", str(Path(__file__).with_name("backup.sh")))
INBOX_NOTE = env("NOTES_INBOX_NOTE", "inbox.md")
OBS_CMD = env("NOTES_OBS_CMD", "obs")


def resolve_day(label: str) -> datetime:
    now = datetime.now()
    text = (label or "today").lower()
    if "before yesterday" in text or "前天" in text:
        return now - timedelta(days=2)
    if "yesterday" in text or "昨天" in text:
        return now - timedelta(days=1)
    return now


def obs_available() -> bool:
    return shutil.which(OBS_CMD) is not None


def sync_backup() -> tuple[bool, str]:
    if not os.path.exists(BACKUP_SCRIPT):
        return False, "backup script not found"
    result = run([BACKUP_SCRIPT])
    return result.returncode == 0, (result.stdout + result.stderr).strip()


def normalize_note(note: str) -> Path:
    p = Path(note)
    if p.suffix == "":
        p = p.with_suffix(".md")
    return p


def ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def append_plain(path: Path, content: str):
    ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


def daily_fallback(content: str, when: str) -> str:
    target = resolve_day(when).strftime("%Y-%m-%d")
    path = VAULT_ROOT / "daily" / f"{target}.md"
    ensure_parent(path)
    new_file = not path.exists()
    timestamp = datetime.now().strftime("%H:%M")
    with path.open("a", encoding="utf-8") as f:
        if new_file:
            f.write(f"# {target}\n\n")
        f.write(f"## {timestamp}\n\n{content}\n\n---\n\n")
    return str(path.relative_to(VAULT_ROOT))


def create_via_cli(note: Path, content: str) -> bool:
    if not obs_available():
        return False
    # Keep the CLI path conservative: create only at vault root by note name.
    if len(note.parts) != 1:
        return False
    result = run([OBS_CMD, "create", f"name={note.stem}", f"content={content}"])
    return result.returncode == 0


def do_daily(args):
    target = resolve_day(args.when).strftime("%Y-%m-%d")
    today = resolve_day("today").strftime("%Y-%m-%d")
    if target == today and obs_available() and not args.force_fallback:
        r = run([OBS_CMD, "daily:append", f"content={args.content}"])
        if r.returncode == 0:
            return "cli", f"daily/{target}.md", True
    return "fallback", daily_fallback(args.content, args.when), True


def do_memo(args):
    path = VAULT_ROOT / normalize_note(INBOX_NOTE)
    append_plain(path, args.content + "\n")
    return "fallback", str(path.relative_to(VAULT_ROOT)), True


def do_append(args):
    path = VAULT_ROOT / normalize_note(args.note)
    append_plain(path, args.content + "\n")
    return "fallback", str(path.relative_to(VAULT_ROOT)), True


def do_create(args):
    note = normalize_note(args.note)
    full = VAULT_ROOT / note
    if create_via_cli(note, args.content) and not args.force_fallback:
        return "cli", str(note), True
    if full.exists() and not args.overwrite:
        raise SystemExit(f"Note already exists: {full}")
    ensure_parent(full)
    full.write_text(args.content + ("" if args.content.endswith("\n") else "\n"), encoding="utf-8")
    return "fallback", str(full.relative_to(VAULT_ROOT)), True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True, choices=["daily", "memo", "append", "create"])
    parser.add_argument("--content", required=True)
    parser.add_argument("--when", default="today")
    parser.add_argument("--note")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--force-fallback", action="store_true")
    args = parser.parse_args()

    if args.mode in {"append", "create"} and not args.note:
        raise SystemExit("--note is required for append/create mode")

    if args.mode == "daily":
        method, target, should_sync = do_daily(args)
    elif args.mode == "memo":
        method, target, should_sync = do_memo(args)
    elif args.mode == "append":
        method, target, should_sync = do_append(args)
    else:
        method, target, should_sync = do_create(args)

    synced = False
    sync_msg = ""
    if should_sync:
        synced, sync_msg = sync_backup()

    print(f"WORKFLOW_OK method={method} target={target} sync={'ok' if synced else 'failed'}")
    if should_sync and (not synced) and sync_msg:
        print(sync_msg)


if __name__ == "__main__":
    main()
