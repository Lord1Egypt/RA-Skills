#!/usr/bin/env python3
"""Palest Ink - Filesystem Change Collector

Detects recently modified files using a marker file + find -newer.
Monitors watched_dirs from config, or falls back to tracked_repos.
"""

import json
import os
import subprocess
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")
MARKER_FILE = os.path.join(PALEST_INK_DIR, "tmp", "fsevent_marker")


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


def guess_language(filepath):
    """Guess programming language from file extension (shared logic with collect_vscode.py)."""
    ext_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".tsx": "typescript-react", ".jsx": "javascript-react",
        ".java": "java", ".go": "go", ".rs": "rust", ".rb": "ruby",
        ".php": "php", ".c": "c", ".cpp": "cpp", ".h": "c-header",
        ".cs": "csharp", ".swift": "swift", ".kt": "kotlin",
        ".scala": "scala", ".r": "r", ".R": "r",
        ".sql": "sql", ".sh": "shell", ".bash": "shell", ".zsh": "shell",
        ".html": "html", ".css": "css", ".scss": "scss", ".less": "less",
        ".json": "json", ".yaml": "yaml", ".yml": "yaml", ".toml": "toml",
        ".xml": "xml", ".md": "markdown", ".rst": "restructuredtext",
        ".vue": "vue", ".svelte": "svelte",
    }
    _, ext = os.path.splitext(filepath)
    return ext_map.get(ext.lower(), "unknown")


def find_workspace(filepath):
    """Walk up directory tree to find nearest .git directory."""
    directory = os.path.dirname(os.path.abspath(filepath))
    while directory != os.path.dirname(directory):  # stop at filesystem root
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        directory = os.path.dirname(directory)
    return ""


def find_changed_files(watch_dir, marker_path):
    """Use find -newer to get files changed since marker mtime."""
    try:
        result = subprocess.run(
            [
                "find", watch_dir,
                "-newer", marker_path,
                "-maxdepth", "4",
                "-type", "f",
                "!", "-path", "*/.git/*",
                "!", "-path", "*/node_modules/*",
                "!", "-path", "*/__pycache__/*",
                "!", "-name", ".DS_Store",
            ],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return []
        return [p for p in result.stdout.strip().split("\n") if p]
    except (subprocess.TimeoutExpired, OSError):
        return []


def collect():
    config = load_config()
    if not config.get("collectors", {}).get("fsevent", True):
        return

    # Determine watched directories
    watched_dirs = config.get("watched_dirs", [])
    if not watched_dirs:
        watched_dirs = config.get("tracked_repos", [])

    if not watched_dirs:
        return

    # First run: create marker and exit
    first_run = not os.path.exists(MARKER_FILE)
    if first_run:
        os.makedirs(os.path.dirname(MARKER_FILE), exist_ok=True)
        open(MARKER_FILE, "w").close()
        return

    now = datetime.now(timezone.utc)
    changed_files = []
    for watch_dir in watched_dirs:
        if os.path.isdir(watch_dir):
            changed_files.extend(find_changed_files(watch_dir, MARKER_FILE))

    # Update marker timestamp before writing records
    os.utime(MARKER_FILE, None)

    if not changed_files:
        return

    records_by_file = {}
    count = 0
    seen_paths = set()

    for filepath in changed_files:
        filepath = os.path.normpath(filepath)
        if filepath in seen_paths:
            continue
        seen_paths.add(filepath)

        # Skip binary-like files and hidden system files
        filename = os.path.basename(filepath)
        if filename.startswith(".") and filename not in {".env", ".gitignore", ".eslintrc"}:
            continue

        workspace = find_workspace(filepath)
        language = guess_language(filepath)

        record = {
            "ts": now.isoformat(),
            "type": "file_change",
            "source": "fsevent_collector",
            "data": {
                "path": filepath,
                "workspace": workspace,
                "language": language,
                "event": "modified",
            }
        }

        datafile = get_datafile(now)
        if datafile not in records_by_file:
            records_by_file[datafile] = []
        records_by_file[datafile].append(record)
        count += 1

    for datafile, records in records_by_file.items():
        with open(datafile, "a") as f:
            for record in records:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")

    if count > 0:
        print(f"[fsevent] Recorded {count} file changes")


if __name__ == "__main__":
    collect()
