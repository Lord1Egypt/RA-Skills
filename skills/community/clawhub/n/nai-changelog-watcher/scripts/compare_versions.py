#!/usr/bin/env python3
"""
compare_versions.py - Compare watchlist against state.json to find new releases.

Usage:
    python3 compare_versions.py [--watchlist PATH] [--state PATH] [--update-state]

Reads:
  watchlist.json  - user's list of repos/packages to watch
  state.json      - last-seen versions (auto-created if missing)

Outputs: JSON array of NEW releases only (unseen since last run).
Pass --update-state to write updated last-seen versions back to state.json.

Exit codes:
  0 - success (may have 0 new releases)
  1 - general error
"""

import json
import sys
import os
import subprocess
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WATCHLIST = os.path.join(os.path.dirname(SCRIPT_DIR), "watchlist.json")
DEFAULT_STATE = os.path.join(os.path.dirname(SCRIPT_DIR), "state.json")


def load_json(path: str, default=None):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"[warn] Could not read {path}: {e}", file=sys.stderr)
        return default


def save_json(path: str, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"[warn] Could not write {path}: {e}", file=sys.stderr)


def run_script(script_name: str, *args) -> list | dict | None:
    script_path = os.path.join(SCRIPT_DIR, script_name)
    cmd = [sys.executable, script_path] + list(args)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 2:
            print(f"[warn] Rate limited while running {script_name}. Skipping.", file=sys.stderr)
            return None
        if result.returncode == 3:
            print(f"[warn] Not found: {' '.join(args)}", file=sys.stderr)
            return None
        if result.returncode != 0:
            print(f"[warn] {script_name} error: {result.stderr.strip()}", file=sys.stderr)
            return None
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        print(f"[warn] Timeout running {script_name} {' '.join(args)}", file=sys.stderr)
        return None
    except (json.JSONDecodeError, Exception) as e:
        print(f"[warn] Failed to parse output from {script_name}: {e}", file=sys.stderr)
        return None


def check_github_entry(entry: dict, state: dict) -> list:
    """Check a GitHub repo entry, return list of new releases."""
    owner = entry.get("owner", "")
    repo = entry.get("repo", "")
    if not owner or not repo:
        print(f"[warn] Invalid github entry: {entry}", file=sys.stderr)
        return []

    key = f"github:{owner}/{repo}"
    last_seen = state.get(key)
    include_prereleases = entry.get("include_prereleases", False)

    releases = run_script("check_github.py", owner, repo, "--limit", "10")
    if not releases:
        return []

    # Filter out drafts; optionally filter prereleases
    releases = [
        r for r in releases
        if not r.get("draft", False)
        and (include_prereleases or not r.get("prerelease", False))
    ]

    if not releases:
        return []

    latest_tag = releases[0]["tag"]

    if last_seen is None:
        # First run: record current latest, don't report as "new"
        state[key] = latest_tag
        return []

    if last_seen == latest_tag:
        return []

    # Collect all releases newer than last_seen
    new_releases = []
    for r in releases:
        if r["tag"] == last_seen:
            break
        new_releases.append({
            **r,
            "key": key,
            "display_name": entry.get("name", f"{owner}/{repo}"),
            "previous_version": last_seen,
        })

    # Update state to latest
    state[key] = latest_tag
    return new_releases


def check_npm_entry(entry: dict, state: dict) -> list:
    """Check an npm package entry, return list of new releases."""
    package = entry.get("package", "")
    if not package:
        print(f"[warn] Invalid npm entry: {entry}", file=sys.stderr)
        return []

    key = f"npm:{package}"
    last_seen = state.get(key)

    result = run_script("check_npm.py", package)
    if not result:
        return []

    latest = result.get("latest", "")
    if not latest:
        return []

    if last_seen is None:
        # First run: record current version
        state[key] = latest
        return []

    if last_seen == latest:
        return []

    # Find versions between last_seen and latest
    recent = result.get("recent_versions", [])
    new_releases = []
    for v in recent:
        if v["tag"] == last_seen:
            break
        new_releases.append({
            **v,
            "key": key,
            "display_name": entry.get("name", package),
            "previous_version": last_seen,
            "name": f"{package}@{v['tag']}",
            "body": "",
            "url": f"https://www.npmjs.com/package/{package}/v/{v['tag']}",
            "prerelease": False,
        })

    state[key] = latest
    return new_releases


def main():
    watchlist_path = DEFAULT_WATCHLIST
    state_path = DEFAULT_STATE
    update_state = False

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--watchlist" and i + 1 < len(args):
            watchlist_path = args[i + 1]
            i += 2
        elif args[i] == "--state" and i + 1 < len(args):
            state_path = args[i + 1]
            i += 2
        elif args[i] == "--update-state":
            update_state = True
            i += 1
        else:
            print(f"Unknown argument: {args[i]}", file=sys.stderr)
            i += 1

    watchlist = load_json(watchlist_path)
    if watchlist is None:
        print(f"[error] watchlist.json not found at {watchlist_path}", file=sys.stderr)
        print(f"Copy assets/watchlist.example.json to {watchlist_path} and edit it.", file=sys.stderr)
        sys.exit(1)

    state = load_json(state_path, default={})
    all_new = []

    entries = watchlist.get("watch", [])
    for entry in entries:
        source = entry.get("source", "").lower()
        if source == "github":
            new = check_github_entry(entry, state)
            all_new.extend(new)
        elif source == "npm":
            new = check_npm_entry(entry, state)
            all_new.extend(new)
        else:
            print(f"[warn] Unknown source '{source}' in entry: {entry}", file=sys.stderr)

    if update_state:
        save_json(state_path, state)

    print(json.dumps(all_new, indent=2))

    # Summary to stderr so stdout stays clean JSON
    print(f"\n[info] Found {len(all_new)} new release(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
