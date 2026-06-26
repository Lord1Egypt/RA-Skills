"""Post-commit hook logic for git-log-tracker.

Called by .git/hooks/post-commit after each successful commit.
Records commit metadata into SQLite index.
"""

import fnmatch
import subprocess
import sys
from pathlib import Path

from config import read_config, is_excluded_repo
from db import get_connection, DEFAULT_DB_DIR


def get_repo_path() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def get_commit_info(repo_path: str | None = None) -> dict:
    # body (%b) 可能跨多行，必须放在格式串末尾，否则其后的字段会被 body 的
    # 额外行挤位，导致 parent_hashes / ref names 解析错位（branch 丢失）。
    fmt = (
        "%H%n"      # full hash
        "%h%n"      # short hash
        "%an%n"     # author name
        "%ae%n"     # author email
        "%aI%n"     # author date ISO 8601
        "%cn%n"     # committer name
        "%ce%n"     # committer email
        "%s%n"      # subject
        "%P%n"      # parent hashes
        "%D%n"      # ref names
        "%b"        # body（放最后，允许多行）
    )
    cwd = repo_path if repo_path else None
    result = subprocess.run(
        ["git", "log", "-1", f"--format={fmt}"],
        capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=cwd,
    )
    lines = result.stdout.split("\n")
    while len(lines) < 11:
        lines.append("")

    branch = None
    ref_names = lines[9]
    for ref in ref_names.split(","):
        ref = ref.strip()
        if ref.startswith("HEAD -> "):
            branch = ref[len("HEAD -> "):]
            break

    parent_hashes = lines[8].strip()
    body = "\n".join(lines[10:]).strip()

    return {
        "commit_hash": lines[0],
        "short_hash": lines[1],
        "author_name": lines[2],
        "author_email": lines[3],
        "author_ts": lines[4],
        "committer_name": lines[5] or None,
        "committer_email": lines[6] or None,
        "commit_subject": lines[7],
        "commit_body": body or None,
        "branch": branch,
        "parent_hashes": parent_hashes or None,
    }


def record_commit(repo_path: str | None = None) -> bool:
    """Record the latest commit to the database. Returns True if successful."""
    try:
        config = read_config()
        if repo_path is None:
            repo_path = get_repo_path()

        if is_excluded_repo(repo_path, config):
            return False

        info = get_commit_info(repo_path)
        repo_name = Path(repo_path).name

        db_path_setting = config.get("database", {}).get("path", "index.db")
        if Path(db_path_setting).is_absolute():
            db_path = Path(db_path_setting)
        else:
            db_path = DEFAULT_DB_DIR / db_path_setting

        conn = get_connection(db_path)
        try:
            conn.execute("""
                INSERT OR IGNORE INTO commits (
                    commit_hash, short_hash, author_name, author_email, author_ts,
                    committer_name, committer_email, commit_subject, commit_body,
                    branch, repo_path, repo_name, parent_hashes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                info["commit_hash"], info["short_hash"],
                info["author_name"], info["author_email"], info["author_ts"],
                info["committer_name"], info["committer_email"],
                info["commit_subject"], info["commit_body"],
                info["branch"], repo_path, repo_name, info["parent_hashes"],
            ))
            conn.commit()
            return True
        finally:
            conn.close()
    except Exception as e:
        print(f"[git-log-tracker] hook error: {e}", file=sys.stderr)
        return False


def main():
    """Entry point when called as CLI command (git-log-tracker hook)."""
    record_commit()
    # Always exit 0 — never block the commit


if __name__ == "__main__":
    main()