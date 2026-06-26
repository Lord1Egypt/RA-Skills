#!/usr/bin/env python3
"""Palest Ink - VS Code Edit History Collector

Reads VS Code's state database to track recently opened/edited files.
"""

import json
import os
import sqlite3
import tempfile
import shutil
from datetime import datetime, timezone

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")

# VS Code state database location on macOS
VSCODE_STATE_DB = os.path.expanduser(
    "~/Library/Application Support/Code/User/globalStorage/state.vscdb"
)


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
    """Guess programming language from file extension."""
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


def collect():
    if not os.path.exists(VSCODE_STATE_DB):
        return

    config = load_config()
    if not config.get("collectors", {}).get("vscode", True):
        return

    last_ts = config.get("vscode_last_ts", 0)

    # Copy DB to avoid lock
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".db")
    os.close(tmp_fd)
    try:
        shutil.copy2(VSCODE_STATE_DB, tmp_path)
    except (PermissionError, OSError):
        os.unlink(tmp_path)
        return

    try:
        conn = sqlite3.connect(tmp_path)
        conn.row_factory = sqlite3.Row

        # VS Code stores state as key-value pairs
        # Key: "history.recentlyOpenedPathsList" contains recently opened files/workspaces
        row = conn.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            ("history.recentlyOpenedPathsList",)
        ).fetchone()

        if not row:
            conn.close()
            return

        recent_data = json.loads(row["value"])
        entries = recent_data.get("entries", [])

        now = datetime.now(timezone.utc)
        datafile = get_datafile(now)
        count = 0

        # Also try to get file modification times for better timestamps
        new_entries = []
        for entry in entries:
            file_uri = entry.get("fileUri") or entry.get("folderUri") or ""
            # Convert file URI to path
            if file_uri.startswith("file://"):
                filepath = file_uri[7:]  # Remove file:// prefix
            else:
                continue

            # Get file modification time as proxy for "edit time"
            try:
                mtime = os.path.getmtime(filepath)
            except OSError:
                continue

            # Only record files modified since last check
            if mtime <= last_ts:
                continue

            dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
            workspace = ""
            # Try to find the workspace/project root
            for parent in [os.path.dirname(filepath)]:
                if os.path.exists(os.path.join(parent, ".git")):
                    workspace = parent
                    break

            record = {
                "ts": dt.isoformat(),
                "type": "vscode_edit",
                "source": "vscode_collector",
                "data": {
                    "file_path": filepath,
                    "workspace": workspace,
                    "language": guess_language(filepath),
                    "is_folder": entry.get("folderUri") is not None
                }
            }
            new_entries.append((mtime, record))
            count += 1

        conn.close()

        if new_entries:
            # Group by date
            records_by_file = {}
            max_ts = last_ts
            for mtime, record in new_entries:
                dt = datetime.fromisoformat(record["ts"])
                df = get_datafile(dt)
                if df not in records_by_file:
                    records_by_file[df] = []
                records_by_file[df].append(record)
                max_ts = max(max_ts, mtime)

            for df, records in records_by_file.items():
                with open(df, "a") as f:
                    for record in records:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")

            config["vscode_last_ts"] = max_ts
            save_config(config)
            print(f"[vscode] Collected {count} file edits")

    finally:
        os.unlink(tmp_path)


if __name__ == "__main__":
    collect()
