#!/usr/bin/env python3
"""Palest Ink - Git Repository Scanner

Scans tracked git repositories for recent commits by the current user.
Supplements git hooks by catching commits made without hooks (IDE, etc).
"""

import json
import os
import subprocess
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_datafile(dt):
    path = os.path.join(DATA_DIR, dt.strftime("%Y"), dt.strftime("%m"), f"{dt.strftime('%d')}.jsonl")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def get_existing_hashes(datafile):
    """Read existing commit hashes from today's data to avoid duplicates."""
    hashes = set()
    if not os.path.exists(datafile):
        return hashes
    with open(datafile, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                if record.get("type") == "git_commit":
                    h = record.get("data", {}).get("hash", "")
                    if h:
                        hashes.add(h)
            except json.JSONDecodeError:
                pass
    return hashes


def run_git(repo_path, args):
    """Run a git command in the specified repo."""
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, OSError):
        return ""


def scan_repo(repo_path, since_ts, existing_hashes):
    """Scan a single repo for recent commits."""
    if not os.path.isdir(os.path.join(repo_path, ".git")):
        return []

    # Get current user's email
    user_email = run_git(repo_path, ["config", "user.email"])
    if not user_email:
        return []

    since_arg = since_ts if since_ts else "1 day ago"

    # Get recent commits by this user
    log_format = "%H|||%s|||%aI|||%D"
    log_output = run_git(repo_path, [
        "log", "--all",
        f"--author={user_email}",
        f"--since={since_arg}",
        f"--format={log_format}"
    ])

    if not log_output:
        return []

    records = []
    for line in log_output.split("\n"):
        if not line.strip():
            continue
        parts = line.split("|||")
        if len(parts) < 3:
            continue

        commit_hash = parts[0].strip()
        message = parts[1].strip()
        iso_date = parts[2].strip()
        refs = parts[3].strip() if len(parts) > 3 else ""

        if commit_hash in existing_hashes:
            continue

        # Get changed files
        files_output = run_git(repo_path, [
            "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash
        ])
        files_changed = [f for f in files_output.split("\n") if f.strip()] if files_output else []

        # Get diff stats
        stat_output = run_git(repo_path, [
            "diff", "--stat", f"{commit_hash}~1", commit_hash
        ])
        insertions = 0
        deletions = 0
        if stat_output:
            last_line = stat_output.split("\n")[-1]
            import re
            ins_match = re.search(r'(\d+) insertion', last_line)
            del_match = re.search(r'(\d+) deletion', last_line)
            insertions = int(ins_match.group(1)) if ins_match else 0
            deletions = int(del_match.group(1)) if del_match else 0

        # Parse branch from refs
        branch = ""
        if refs:
            for ref in refs.split(","):
                ref = ref.strip()
                if ref.startswith("HEAD -> "):
                    branch = ref[8:]
                    break
        if not branch:
            branch = run_git(repo_path, ["rev-parse", "--abbrev-ref", "HEAD"])

        try:
            dt = datetime.fromisoformat(iso_date)
        except ValueError:
            dt = datetime.now(timezone.utc)

        record = {
            "ts": dt.isoformat(),
            "type": "git_commit",
            "source": "git_scan",
            "data": {
                "repo": repo_path,
                "branch": branch,
                "hash": commit_hash,
                "message": message,
                "files_changed": files_changed,
                "insertions": insertions,
                "deletions": deletions
            }
        }
        records.append(record)

    return records


def collect():
    config = load_config()
    if not config.get("collectors", {}).get("git_scan", True):
        return

    tracked_repos = config.get("tracked_repos", [])
    last_ts = config.get("git_scan_last_ts", "")

    if not tracked_repos:
        return

    now = datetime.now(timezone.utc)
    datafile = get_datafile(now)
    existing_hashes = get_existing_hashes(datafile)

    total_count = 0
    for repo_path in tracked_repos:
        repo_path = os.path.expanduser(repo_path)
        if not os.path.isdir(repo_path):
            continue

        records = scan_repo(repo_path, last_ts, existing_hashes)
        if records:
            records_by_file = {}
            for record in records:
                dt = datetime.fromisoformat(record["ts"])
                df = get_datafile(dt)
                if df not in records_by_file:
                    records_by_file[df] = []
                records_by_file[df].append(record)

            for df, recs in records_by_file.items():
                with open(df, "a") as f:
                    for rec in recs:
                        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                        existing_hashes.add(rec["data"]["hash"])

            total_count += len(records)

    config["git_scan_last_ts"] = now.isoformat()
    save_config(config)

    if total_count > 0:
        print(f"[git_scan] Found {total_count} new commits across {len(tracked_repos)} repos")


if __name__ == "__main__":
    collect()
