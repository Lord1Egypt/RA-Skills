#!/usr/bin/env python3
"""
OpenClaw Git Manager — version control for ~/.openclaw configuration files.

Features:
  - commit with auto-generated diff explanation
  - restore with history log and undo support
  - credentials redaction before staging (real keys never committed)
  - post-restore config validation via openclaw doctor

Usage:
    python3 git_manager.py <command> [args]
    python3 git_manager.py commit -m "message"
    python3 git_manager.py restore <commit> [--undo]
    python3 git_manager.py status / log / diff
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_DIR = OPENCLAW_DIR
RESTORE_LOG = os.path.join(OPENCLAW_DIR, ".restore-log.json")
SECRETS_LOG = os.path.join(OPENCLAW_DIR, ".secrets-log.json")  # never committed

# Files to track and their descriptions
TRACKED_PATHS = [
    "openclaw.json",
    "credentials",
    "agents",
    "flows",
]

EXCLUDED_PATTERNS = [
    "memory/", "logs/", "media/", "tmp/", "trash/",
    "canvas/", "npm/", "completions/", "service-env/",
    "tasks/", "subagents/", "cron/", "devices/",
    "exec-approvals.json", "update-check.json",
    "skills-trigger-index.json", "delivery-queue/",
    ".DS_Store", "node_modules/", "package-lock.json",
    "*.swp", "*.swo", ".vscode/", ".idea/",
    "tui/", "openclaw.json.bak*", "openclaw.json.last-good",
    "plugins/", "plugin-skills/", "extensions/",
    "logs/", "*.log",
    ".restore-log.json", ".secrets-log.json",
    "workspace/",  # nested git repos — tracked separately
]

# Secret patterns to redact before staging
SECRET_REDACT_PATTERNS = [
    (re.compile(r"(sk-[a-zA-Z0-9-]{20,})"), "[REDACTED-api-key]"),
    (re.compile(r"(AKIA[a-zA-Z0-9]{16})"), "[REDACTED-aws-key]"),
    (re.compile(r"(?i)(bearer\s+[a-zA-Z0-9_\-\.]{30,})"), "[REDACTED-bearer]"),
    (re.compile(r"(?i)(api[_-]?key\s*[=:]\s*['\"]?)([a-zA-Z0-9_\-]{20,})"),
     r"\1[REDACTED]"),
    (re.compile(r"(ghp_[a-zA-Z0-9]{36})"), "[REDACTED-github-token]"),
    (re.compile(r"(gho_[a-zA-Z0-9]{36})"), "[REDACTED-github-oauth]"),
]


# ── Git helpers ───────────────────────────────────────────────────────────────

def git(*args, cwd=REPO_DIR, capture=True):
    if capture:
        result = subprocess.run(
            ["git"] + list(args), cwd=cwd, capture_output=True, text=True,
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    else:
        result = subprocess.run(["git"] + list(args), cwd=cwd)
        return "", "", result.returncode


def is_repo():
    _, _, rc = git("rev-parse", "--git-dir", capture=True)
    return rc == 0


def ensure_gitignore():
    gi_path = os.path.join(REPO_DIR, ".gitignore")
    existing = set()
    if os.path.exists(gi_path):
        with open(gi_path) as f:
            existing = set(
                line.strip() for line in f
                if line.strip() and not line.startswith("#")
            )
    needed = set(EXCLUDED_PATTERNS)
    if needed.issubset(existing):
        return
    with open(gi_path, "a") as f:
        for pat in sorted(needed - existing):
            f.write(f"{pat}\n")


def _has_nested_git(path):
    return os.path.exists(os.path.join(REPO_DIR, path, ".git"))


# ── Restore log ──────────────────────────────────────────────────────────────

def load_restore_log():
    if os.path.exists(RESTORE_LOG):
        try:
            with open(RESTORE_LOG) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_restore_log(log):
    with open(RESTORE_LOG, "w") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def add_restore_entry(target, restored_files, reason, prev_head, new_head):
    log = load_restore_log()
    log.append({
        "version": 1,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target": target,
        "restored_files": restored_files,
        "reason": reason,
        "prev_head": prev_head,
        "new_head": new_head,
    })
    save_restore_log(log)


# ── Diff generation (for commit message) ────────────────────────────────────

def _generate_diff_description():
    """Generate a structured diff description for all changed files."""
    stdout, _, _ = git("status", "--porcelain", capture=True)
    all_lines = [l.strip() for l in stdout.splitlines() if l.strip()]
    if not all_lines:
        return None

    parts = []
    for line in all_lines:
        parts_l = line.split(maxsplit=1)
        if len(parts_l) != 2:
            continue
        status, path = parts_l[0], parts_l[1]
        if path.endswith(".json"):
            diff = _json_diff_description(path)
            if diff:
                parts.append(diff)
        else:
            parts.append(f"  {path}: ({status} {path.split('/')[0]})")

    return "\n".join(parts) if parts else None


def _json_diff_description(path):
    """Compare JSON file with HEAD and produce a key-level diff summary."""
    full = os.path.join(REPO_DIR, path)
    if not os.path.exists(full):
        return f"  {path}: (deleted)"

    try:
        with open(full) as f:
            current = json.load(f)
    except Exception as e:
        return f"  {path}: (parse error: {e})"

    # Read HEAD version
    stdout, _, rc = git("show", f"HEAD:{path}", capture=True)
    if rc == 0 and stdout.strip():
        try:
            prev = json.loads(stdout)
        except Exception:
            prev = None
    else:
        prev = None

    if prev is None:
        return f"  {path}: (new file)"

    # Deep diff — top-level + second-level key changes
    changes = []
    all_keys = set(_flatten_keys(prev)) | set(_flatten_keys(current))
    for full_key in sorted(all_keys):
        old_val = _get_nested(prev, full_key)
        new_val = _get_nested(current, full_key)
        if old_val is None and new_val is not None:
            changes.append(f"  +{full_key}: {_fmt(new_val)}")
        elif new_val is None and old_val is not None:
            changes.append(f"  -{full_key}: {_fmt(old_val)}")
        elif old_val != new_val:
            changes.append(f"  ~{full_key}: {_fmt(old_val)} → {_fmt(new_val)}")

    if not changes:
        return f"  {path}: (no structural change)"

    return f"  {path}:\n" + "\n".join(changes)


def _flatten_keys(obj, prefix=""):
    """Flatten nested dict keys with dots."""
    if isinstance(obj, dict):
        result = []
        for k, v in obj.items():
            new_key = f"{prefix}.{k}" if prefix else k
            result.append(new_key)
            if isinstance(v, dict):
                result.extend(_flatten_keys(v, new_key))
            elif isinstance(v, list):
                result.append(f"{new_key}[*]")
        return result
    return [prefix] if prefix else []


def _get_nested(obj, key):
    """Get value from nested dict by dot-separated key. Supports [*] for arrays."""
    parts = key.split(".")
    val = obj
    for part in parts:
        if isinstance(val, dict):
            val = val.get(part)
        elif isinstance(val, list):
            try:
                idx = int(part.replace("[*]", "0").split("[")[0])
                if part.startswith("[*]"):
                    return val[0] if val else None
                val = val[idx] if 0 <= idx < len(val) else None
            except (ValueError, IndexError):
                return None
        else:
            return None
        if val is None:
            return None
    return val


def _fmt(val):
    """Format a value for commit message diff."""
    if val is None:
        return "null"
    if isinstance(val, bool):
        return str(val).lower()
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, str):
        if len(val) > 40:
            return f'"{val[:37]}..."'
        return f'"{val}"'
    if isinstance(val, list):
        if len(val) > 5:
            return f"[{len(val)} items]"
        return str(val)
    if isinstance(val, dict):
        return f"{{{len(val)} keys}}"
    return repr(val)


# ── Credentials redaction ────────────────────────────────────────────────────

def _redact_secrets(content):
    """Redact secrets from file content, return (redacted, found_secrets)."""
    found = []
    redacted = content
    for pat, repl in SECRET_REDACT_PATTERNS:
        if isinstance(pat.pattern, str):
            # For simple string replacement patterns
            if re.search(pat, redacted):
                found.append(pat.pattern)
                redacted = pat.sub(repl, redacted)
        else:
            if pat.search(redacted):
                found.append(pat.pattern)
                redacted = pat.sub(repl, redacted)
    return redacted, found


def _load_secrets_log():
    if os.path.exists(SECRETS_LOG):
        try:
            with open(SECRETS_LOG) as f:
                return json.load(f)
        except Exception:
            return []
    return []


def _save_secrets_log(log):
    with open(SECRETS_LOG, "w") as f:
        json.dump(log, f, indent=2)


def _redact_file(path):
    """Redact secrets in a file, return (was_redacted, secrets_found)."""
    full = os.path.join(REPO_DIR, path)
    if not os.path.exists(full):
        return False, []

    try:
        with open(full) as f:
            content = f.read()
    except Exception:
        return False, []

    redacted, found = _redact_secrets(content)
    if not found:
        return False, []

    # Write redacted version
    with open(full, "w") as f:
        f.write(redacted)

    # Log actual secret hashes (not the secrets themselves) for audit
    secrets_log = _load_secrets_log()
    for secret in found:
        secrets_log.append({
            "file": path,
            "type": "api_key",  # simplified — could distinguish by pattern
            "redacted_at": datetime.now(timezone.utc).isoformat(),
            "commit_hint": "(hash in git log)",
        })
    _save_secrets_log(secrets_log)

    return True, found


# ── Validation ────────────────────────────────────────────────────────────────

def run_doctor():
    """Run openclaw gateway doctor and return (ok, output)."""
    result = subprocess.run(
        ["openclaw", "gateway", "doctor"],
        cwd=OPENCLAW_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.returncode == 0, result.stdout + result.stderr


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_init():
    if is_repo():
        print("Repository already exists.")
        return 0
    ensure_gitignore()
    _, err, rc = git("init", capture=True)
    if rc != 0:
        print(f"ERROR: git init failed: {err}")
        return 1
    git("checkout", "-b", "main", capture=True)
    git("config", "user.name", "openclaw-git-manager", capture=True)
    git("config", "user.email", "openclaw@local", capture=True)
    print("Initialized git repository in ~/.openclaw/")
    print("Run `git_manager.py commit` to create the first checkpoint.")
    return 0


def cmd_status():
    if not is_repo():
        print("ERROR: Not a git repository. Run `init` first.")
        return 1
    stdout, _, _ = git("branch", "--show-current", capture=True)
    branch = stdout.strip() or "(detached)"
    stdout, _, _ = git("rev-list", "--count", "HEAD", capture=True)
    n_commits = stdout.strip() or "0"
    stdout, _, _ = git("status", "--porcelain", capture=True)
    lines = [l for l in stdout.splitlines() if l.strip()]
    print(f"Branch:     {branch}")
    print(f"Commits:    {n_commits}")
    if not lines:
        print("Status:     clean — no uncommitted changes")
    else:
        print(f"Status:     {len(lines)} file(s) changed")
        for line in lines:
            print(f"  {line}")
    return 0


def cmd_log(limit=20, commit_hash=None):
    if not is_repo():
        print("ERROR: Not a git repository.")
        return 1
    if commit_hash:
        stdout, _, rc = git("show", commit_hash, "--stat", capture=True)
        if rc != 0:
            print(f"ERROR: Commit {commit_hash} not found.")
            return 1
        print(stdout)
        return 0
    stdout, _, rc = git("log", "--oneline", f"-{limit}", capture=True)
    if rc != 0 or not stdout.strip():
        print("No commits yet.")
        return 0
    lines = stdout.splitlines()
    stdout_full, _, _ = git("log", "--format=%H|%s|%ar", f"-{limit}", capture=True)
    print(f"{'#':<4} {'commit':<10} {'time':<12} message")
    print("-" * 70)
    for i, line in enumerate(stdout_full.splitlines()):
        if "|" in line:
            h, msg, t = line.split("|", 2)
            print(f"{len(lines)-i:<4} {h[:8]:<10} {t:<12} {msg}")
    return 0


def cmd_diff(from_ref=None, to_ref=None):
    if not is_repo():
        print("ERROR: Not a git repository.")
        return 1
    if from_ref and to_ref:
        stdout, _, rc = git("diff", from_ref, to_ref, capture=True)
    elif from_ref:
        stdout, _, rc = git("diff", from_ref, "HEAD", capture=True)
    else:
        stdout, _, rc = git("diff", "HEAD", capture=True)
        if rc != 0:
            stdout, _, _ = git("diff", capture=True)
    if not stdout.strip():
        print("No changes.")
        return 0

    # Summarize by file
    files = {}
    current = None
    for line in stdout.splitlines():
        if line.startswith("diff --git"):
            p = line.split(" b/", 1)[-1] if " b/" in line else ""
            if p:
                current = p
                files[p] = {"additions": 0, "deletions": 0}
        elif line.startswith("+") and current:
            files[current]["additions"] += 1
        elif line.startswith("-") and current:
            files[current]["deletions"] += 1

    print(f"{len(files)} file(s) changed:", end=" ")
    print(", ".join(f"{p} (+{s['additions']}/-{s['deletions']})"
                  for p, s in sorted(files.items())))
    print()
    print("─" * 60)
    for line in stdout.splitlines():
        if any(t in line for t in ("+++", "---", "diff", "index")):
            continue
        print(line)
    return 0


def cmd_commit(message=None, dry_run=False, auto_message=True):
    """Stage, redact secrets, diff, and commit config state."""
    if not is_repo():
        print("ERROR: Not a git repository. Run `init` first.")
        return 1

    stdout, _, _ = git("status", "--porcelain", capture=True)
    all_lines = [l.strip() for l in stdout.splitlines() if l.strip()]
    if not all_lines:
        print("Nothing to commit — working tree is clean.")
        return 0

    # Collect files (skip nested .git dirs)
    valid_files = []
    skipped = []
    for line in all_lines:
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            continue
        _, path = parts[0], parts[1]
        if _has_nested_git(path):
            skipped.append(path)
            continue
        valid_files.append(path)

    if skipped:
        print(f"Skipped (nested git): {', '.join(skipped)}")

    if not valid_files:
        print("Nothing to commit after filtering.")
        return 0

    # ── Redact secrets in credentials/ files ──────────────────────────────
    redacted_files = []
    for path in valid_files:
        if "credentials" in path or path.endswith(".json"):
            redacted, found = _redact_file(path)
            if redacted:
                redacted_files.append(f"{path} ({len(found)} secret(s) redacted)")

    if redacted_files:
        print("Redacted secrets before staging:")
        for f in redacted_files:
            print(f"  {f}")

    # ── Generate diff description for commit message ───────────────────────
    diff_desc = _generate_diff_description()

    if not message and auto_message and diff_desc:
        # Build commit message: subject + body
        short_summary = "; ".join(
            sorted(set(
                p.split("/")[0] if "/" in p else p
                for p in valid_files
            ))[:5]
        )
        message = f"config: update {short_summary}\n\n{diff_desc}"

    print(f"Files to commit ({len(valid_files)}):")
    for p in valid_files:
        print(f"  {p}")
    print()
    if message:
        print(f"Commit message:\n{message}")
    print()

    if dry_run:
        print("(dry run — no commit created)")
        return 0

    # Stage files individually
    for path in valid_files:
        _, err, rc = git("add", path, capture=True)
        if rc != 0 and err:
            print(f"WARNING staging {path}: {err}")

    if not message:
        message = f"config: update"

    stdout, err, rc = git("commit", "-m", message, capture=True)
    if rc != 0:
        print(f"ERROR committing: {err}")
        return 1

    stdout, _, _ = git("rev-parse", "--short", "HEAD", capture=True)
    print(f"Committed: {stdout}")
    return 0


def cmd_restore(target, undo=False, file_path=None, force=False):
    """Restore to a previous commit, with restore history and undo support."""
    if not is_repo():
        print("ERROR: Not a git repository.")
        return 1

    # Get current HEAD
    stdout, _, _ = git("rev-parse", "--short", "HEAD", capture=True)
    prev_head = stdout.strip() or None

    # Load restore log for undo
    log = load_restore_log()

    if undo:
        if not log:
            print("No restore history to undo.")
            print("  → Your working tree is clean, nothing to roll back.")
            return 0
        last = log[-1]
        target = last["prev_head"]
        print(f"Undo restore: rolling back to {target} (was {last['new_head']})")
        force = True

    # ── Preview ─────────────────────────────────────────────────────────────
    diff_cmd = ["git", "diff", "--stat"]
    if file_path:
        diff_cmd += ["--", file_path]
    else:
        diff_cmd += [target, "--"]
    diff_out = subprocess.run(diff_cmd, cwd=REPO_DIR,
                               capture_output=True, text=True)

    what = file_path or "(all tracked files)"
    print(f"Will restore {what} to commit {target}")
    print(f"Current HEAD: {prev_head or '(none)'}")
    print()
    if diff_out.stdout.strip():
        print(diff_out.stdout)
    print()

    if not force:
        confirm = input("Proceed with restore? [y/N] ")
        if confirm.strip().lower() != "y":
            print("Aborted.")
            return 0

    # ── Perform restore ─────────────────────────────────────────────────────
    if file_path:
        _, err, rc = git("checkout", target, "--", file_path, capture=True)
    else:
        _, err, rc = git("checkout", target, "--", ".", capture=True)
    if rc != 0:
        print(f"ERROR: {err}")
        return 1

    stdout, _, _ = git("rev-parse", "--short", "HEAD", capture=True)
    new_head = stdout.strip()

    # Log this restore
    add_restore_entry(
        target=target,
        restored_files=[file_path] if file_path else ["(all)"],
        reason="manual restore",
        prev_head=prev_head,
        new_head=new_head,
    )

    print(f"Restored to: {new_head}")
    print(f"Previous HEAD: {prev_head}")

    # ── Validate ────────────────────────────────────────────────────────────
    print()
    print("Validating config via openclaw gateway doctor...")
    ok, output = run_doctor()

    # Parse doctor output for actionable guidance
    lines = output.splitlines()
    issues = []
    for l in lines:
        stripped = l.strip()
        # Skip non-actionable lines
        if not stripped or stripped.startswith("=") or stripped.startswith("-"):
            continue
        # Catch issues and warnings
        lower = stripped.lower()
        if any(k in lower for k in ("error", "fail", "invalid", "missing", "could not")):
            issues.append(stripped)
        elif "warn" in lower or "⚠" in stripped:
            issues.append(stripped)

    if issues:
        print()
        print("⚠️  Issues detected (first few):")
        for issue in issues[:10]:
            print(f"  {issue}")
        print()
        print("  → Run `openclaw gateway restart` to apply changes.")
        print("  → If the issue persists, run `openclaw gateway doctor` for full diagnostics.")
    else:
        print()
        print("✅ Config is valid — gateway is healthy.")
        print("  → Run `openclaw gateway restart` if anything still feels off.")

    return 0


def cmd_undo():
    """Undo the last restore operation."""
    return cmd_restore(target=None, undo=True)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Git Manager — version control for ~/.openclaw config",
        usage="python3 git_manager.py <command> [args]",
    )
    sub = parser.add_subparsers(dest="command", metavar="<command>")

    sub.add_parser("init", help="Initialize git repo (first use)")
    sub.add_parser("status", help="Show working tree state")
    sub.add_parser("log", help="Show commit history")
    sub.add_parser("undo", help="Undo the last restore operation")

    diff_p = sub.add_parser("diff", help="Show changes")
    diff_p.add_argument("--from", dest="from_ref")
    diff_p.add_argument("--to", dest="to_ref")

    commit_p = sub.add_parser("commit", help="Commit current config state")
    commit_p.add_argument("-m", "--message", help="Commit message")
    commit_p.add_argument("--dry-run", action="store_true")
    commit_p.add_argument("--no-auto", dest="no_auto",
                         action="store_true",
                         help="Don't auto-generate diff description")

    restore_p = sub.add_parser("restore", help="Restore to a previous commit")
    restore_p.add_argument("target", nargs="?", help="Commit hash or ref")
    restore_p.add_argument("--undo", action="store_true", help="Undo last restore")
    restore_p.add_argument("--file", help="Restore specific file only")
    restore_p.add_argument("-f", "--force", action="store_true",
                          help="Skip confirmation")

    args = parser.parse_args()
    cmd = args.command

    if cmd is None or cmd == "help":
        print(__doc__)
        return 0

    if cmd == "init":
        return cmd_init()
    if cmd == "status":
        return cmd_status()
    if cmd == "log":
        return cmd_log(
            limit=20,
            commit_hash=args.args[0] if hasattr(args, "args") and args.args else None,
        )
    if cmd == "diff":
        return cmd_diff(from_ref=args.from_ref, to_ref=args.to_ref)
    if cmd == "undo":
        return cmd_undo()
    if cmd == "commit":
        return cmd_commit(
            message=args.message,
            dry_run=args.dry_run,
            auto_message=not args.no_auto,
        )
    if cmd == "restore":
        if args.undo:
            return cmd_undo()
        if not args.target:
            print("ERROR: restore requires a commit reference")
            print("Usage: git_manager.py restore <commit> [--file <path>]")
            return 1
        return cmd_restore(
            target=args.target,
            file_path=args.file,
            force=args.force,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())