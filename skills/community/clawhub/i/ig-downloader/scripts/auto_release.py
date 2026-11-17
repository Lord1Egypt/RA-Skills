#!/usr/bin/env python3
"""
auto_release.py — Generate changelog, bump version, prepare GitHub Release.

Scans conventional commits since the last git tag, categorises them,
determines the appropriate semver bump (major/minor/patch), generates a
changelog section matching the Keep a Changelog format, updates
pyproject.toml and CHANGELOG.md in-place, and writes GitHub Actions
output (version, changelog, tag_name) so the workflow can consume them.

Usage
-----
    python scripts/auto_release.py [--dry-run]

Environment variables consumed
-------------------------------
    GITHUB_OUTPUT       — GitHub Actions output file (appended to)
    GITHUB_STEP_SUMMARY — GitHub Actions step summary (appended to)
    SKIP_RELEASE        — if set to "1", exits silently without making changes

Exit codes
----------
    0   — release ready (or no release needed, outputs include skip_reason)
    1   — unexpected error
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Reusable type for a parsed commit dict.
Commit = Dict[str, Any]

# ──────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent

PYPROJECT = REPO_ROOT / "pyproject.toml"
CHANGELOG = REPO_ROOT / "CHANGELOG.md"

CONVENTIONAL_RE = re.compile(
    r"^(?P<type>\w+)"        # type: feat, fix, docs, …
    r"(?:\((?P<scope>[^)]*)\))?"  # optional scope
    r"(?P<breaking>!)?\s*:\s*"    # optional ! for breaking
    r"(?P<subject>.+)$",          # subject
)

BREAKING_RE = re.compile(r"BREAKING[-\s]CHANGE:", re.IGNORECASE)

# Commit types that trigger a version bump — order determines which
# bump wins when multiple types are present (first wins).
BUMP_PRIORITY: Dict[str, str] = {
    "BREAKING": "major",
    "feat": "minor",
    "fix": "patch",
    "perf": "patch",
}

# Human-readable labels for the changelog section headings.
CATEGORY_LABELS: Dict[str, str] = {
    "feat": "Added",
    "fix": "Fixed",
    "perf": "Changed",      # perf = user-visible improvement
    "docs": "Changed",
    "refactor": "Changed",
    "test": "Changed",
    "chore": "Changed",
    "ci": "Changed",
    "BREAKING": "Changed",
}


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def run_git(*args: str) -> str:
    """Run a git sub‑command and return stdout stripped."""
    cmd = ["git"] + list(args)
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )
    except subprocess.CalledProcessError as exc:
        print(f"❌ git {' '.join(args)} failed:\n{exc.stderr}", file=sys.stderr)
        raise
    return result.stdout.strip()


def get_latest_tag() -> Optional[str]:
    """Return the most recent tag reachable from HEAD, or None."""
    try:
        tag = run_git("describe", "--tags", "--abbrev=0", "--match", "v*")
        return tag if tag else None
    except subprocess.CalledProcessError:
        return None


def parse_commit(line: str) -> Optional[Dict[str, object]]:
    """
    Parse a single line of ``git log --oneline``.

    Returns dict with keys: sha, type, scope, subject, breaking
    or None if the line can't be parsed.
    """
    line = line.strip()
    if not line:
        return None

    # SHA is everything before the first space
    parts = line.split(maxsplit=1)
    if len(parts) < 2:
        return None
    sha, msg = parts[0], parts[1]

    # Check for BREAKING CHANGE footer on its own line won't appear
    # in --oneline format, so we also look for the `!` marker.
    m = CONVENTIONAL_RE.match(msg)
    if not m:
        # Still include the commit but unclassified
        return {
            "sha": sha,
            "type": "other",
            "scope": "",
            "subject": msg,
            "breaking": False,
        }

    breaking = bool(m.group("breaking")) or bool(BREAKING_RE.search(msg))
    return {
        "sha": sha,
        "type": m.group("type"),
        "scope": m.group("scope") or "",
        "subject": m.group("subject").rstrip("."),
        "breaking": breaking,
    }


def get_commits_since(tag: Optional[str]) -> List[Commit]:
    """Return list of parsed commits between *tag* and HEAD."""
    if tag:
        rev_range = f"{tag}..HEAD"
    else:
        # No tag yet — include ALL commits reachable from HEAD
        rev_range = "HEAD"

    raw = run_git("log", "--oneline", rev_range)
    if not raw:
        return []

    commits: List[Commit] = []
    for line in raw.splitlines():
        parsed = parse_commit(line)
        if parsed:
            commits.append(parsed)
    return commits


def classify_commits(commits: List[Commit]) -> Dict[str, List[str]]:
    """
    Group *commits* by their changelog section label.

    Returns dict like {"Added": [...entries...], "Fixed": [...], ...}
    """
    groups: Dict[str, List[str]] = defaultdict(list)

    for c in commits:
        ctype = str(c["type"])

        # Promote to BREAKING if marked
        if c["breaking"]:
            label = "⚠ BREAKING CHANGES"
        elif ctype in ("feat", "fix", "perf"):
            label = CATEGORY_LABELS.get(ctype, "Changed")
        else:
            label = "Other"

        scope = f"**{c['scope']}:** " if c["scope"] else ""
        entry = f"{scope}{c['subject']} ([{c['sha'][:7]}](https://github.com/CripterHack/ig-downloader-skill/commit/{c['sha']}))"
        groups[label].append(entry)

    return dict(groups)


def determine_bump(
    commits: List[Commit],
    manual_bump: Optional[str] = None,
) -> str:
    """
    Determine the semver bump type from *commits*.

    Priority (highest wins):
        1. manual_bump if provided and != "auto"
        2. BREAKING → major
        3. feat → minor
        4. fix / perf → patch
        5. otherwise → None (no bump / patch)

    Returns one of: "major", "minor", "patch", or None.
    """
    if manual_bump and manual_bump != "auto":
        return manual_bump

    bump_order = ["major", "minor", "patch"]
    current_priority = -1  # no bump

    for c in commits:
        if c.get("breaking"):
            current_priority = max(current_priority, bump_order.index("major"))
            continue
        btype = BUMP_PRIORITY.get(str(c.get("type", "")))
        if btype:
            current_priority = max(current_priority, bump_order.index(btype))

    if current_priority >= 0:
        return bump_order[current_priority]
    return "patch"  # default to patch for safety


def bump_version(current: str, bump_type: str) -> str:
    """
    Bump a semver string (X.Y.Z) by *bump_type* (major|minor|patch).

    Returns the new version string (without 'v' prefix).
    """
    parts = current.lstrip("v").split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1

    return f"{major}.{minor}.{patch}"


def generate_changelog_section(
    version: str,
    groups: Dict[str, List[str]],
) -> str:
    """
    Generate a single version section in Keep a Changelog format.
    """
    today = date.today()
    lines = [
        f"## [{version}] - {today}",
        "",
    ]

    # Order: BREAKING → Added → Fixed → Changed → Other
    section_order = [
        "⚠ BREAKING CHANGES",
        "Added",
        "Fixed",
        "Changed",
        "Other",
    ]

    has_content = False
    for section in section_order:
        items = groups.get(section, [])
        if not items:
            continue
        has_content = True
        lines.append(f"### {section}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    if not has_content:
        lines.append("- Maintenance and dependency updates.")
        lines.append("")

    return "\n".join(lines)


def read_pyproject_version() -> Optional[str]:
    """Read the current version from pyproject.toml."""
    content = PYPROJECT.read_text(encoding="utf-8")
    m = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    return m.group(1) if m else None


def write_pyproject_version(new_version: str) -> None:
    """Replace the version string in pyproject.toml."""
    content = PYPROJECT.read_text(encoding="utf-8")
    updated = re.sub(
        r'^version\s*=\s*"[^"]+"',
        f'version = "{new_version}"',
        content,
        count=1,
        flags=re.MULTILINE,
    )
    PYPROJECT.write_text(updated, encoding="utf-8")


def update_changelog(new_version: str, section: str) -> None:
    """
    Insert the new version *section* into CHANGELOG.md right after the
    "# Changelog" heading and its description lines.
    """
    content = CHANGELOG.read_text(encoding="utf-8")

    # Find the first "## [" line (existing release) and insert before it
    insert_before = content.find("\n## [")
    if insert_before == -1:
        # No existing releases — append after header
        insert_before = content.find("# Changelog")
        if insert_before >= 0:
            # Skip to after the header block
            after_header = content.find("\n\n", insert_before)
            if after_header >= 0:
                insert_before = after_header + 1
            else:
                insert_before = len(content)
        else:
            insert_before = len(content)

    new_content = (
        content[:insert_before]
        + "\n"
        + section
        + "\n"
        + content[insert_before:].lstrip("\n")
    )

    CHANGELOG.write_text(new_content, encoding="utf-8")


def is_release_commit() -> bool:
    """Check if the most recent commit is already a release commit."""
    msg = run_git("log", "-1", "--format=%s")
    return bool(re.match(r"^chore\(release\):", msg))


# ──────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────

def main() -> int:
    dry_run = "--dry-run" in sys.argv
    manual_bump = os.environ.get("INPUT_BUMP", "auto")
    skip_env = os.environ.get("SKIP_RELEASE", "0")

    if skip_env == "1" and not dry_run:
        # Workflow controls skipping — output nothing
        print("🔇 SKIP_RELEASE=1 → exiting without changes.")
        return 0

    # ── Gather commits ───────────────────────────────────────────
    latest_tag = get_latest_tag()
    commits = get_commits_since(latest_tag)

    print(f"📦 Last tag:        {latest_tag or '(none)'}")
    print(f"📝 Commits to scan: {len(commits)}")

    if not commits:
        print("✅ No new commits since last tag — nothing to release.")
        _set_output("skip_reason", "no_new_commits")
        return 0

    if is_release_commit() and len(commits) <= 1:
        print("✅ Latest commit is already a release — nothing to do.")
        _set_output("skip_reason", "already_release")
        return 0

    # ── Classify & bump ──────────────────────────────────────────
    groups = classify_commits(commits)
    bump_type = determine_bump(commits, manual_bump)

    current_version = read_pyproject_version()
    if not current_version:
        print("❌ Could not read version from pyproject.toml", file=sys.stderr)
        return 1

    new_version = bump_version(current_version, bump_type)
    tag_name = f"v{new_version}"

    print(f"🏷  Current:         v{current_version}")
    print(f"⬆️  Bump:            {bump_type}")
    print(f"🏷  New version:     {tag_name}")
    print()

    # Only print bump types if we would make a release
    for section, items in groups.items():
        print(f"  {section}:")
        for item in items:
            print(f"    • {item}")

    # ── Generate changelog ───────────────────────────────────────
    changelog_section = generate_changelog_section(new_version, groups)
    print("\n── Changelog section ──────────────────────")
    print(changelog_section)
    print("───────────────────────────────────────────\n")

    if dry_run:
        print("🏁 Dry-run — no files modified.")
        _set_output("version", new_version)
        _set_output("tag_name", tag_name)
        _set_output("bump", bump_type)
        return 0

    # ── Update files ─────────────────────────────────────────────
    write_pyproject_version(new_version)
    print(f"✅ Updated pyproject.toml → {new_version}")

    update_changelog(new_version, changelog_section)
    print(f"✅ Updated CHANGELOG.md  → [{new_version}] added")

    # ── Stage for commit ─────────────────────────────────────────
    run_git("add", str(PYPROJECT), str(CHANGELOG))
    print("✅ Staged pyproject.toml + CHANGELOG.md")

    # ── Write changelog body to a temp file (multiline-safe) ────
    changelog_path = os.path.join(
        os.environ.get("RUNNER_TEMP", "/tmp"),
        "release_body.md",
    )
    with open(changelog_path, "w", encoding="utf-8") as f:
        f.write(changelog_section)

    # ── GitHub Actions output ────────────────────────────────────
    _set_output("version", new_version)
    _set_output("tag_name", tag_name)
    _set_output("changelog_path", changelog_path)
    _set_output("bump", bump_type)

    # Step summary
    _append_summary(
        f"## 🚀 Release {tag_name}\n\n"
        f"- **Bump**: {bump_type}\n"
        f"- **Commits**: {len(commits)}\n"
        f"- **Sections**: {', '.join(groups.keys())}\n"
    )

    print(f"\n✅ Release {tag_name} ready to commit and tag.")
    return 0


# ──────────────────────────────────────────────────────────────────────
# GitHub Actions helpers
# ──────────────────────────────────────────────────────────────────────

def _set_output(key: str, value: str) -> None:
    """Append ``{key}={value}`` to ``$GITHUB_OUTPUT``."""
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return  # local run, no-op
    with open(output_path, "a", encoding="utf-8") as f:
        # GitHub Actions requires multiline values to use a delimiter
        if "\n" in value:
            delimiter = f"EOF_{key}_{os.urandom(4).hex()}"
            f.write(f"{key}<<{delimiter}\n{value}\n{delimiter}\n")
        else:
            f.write(f"{key}={value}\n")


def _append_summary(md: str) -> None:
    """Append *md* to ``$GITHUB_STEP_SUMMARY``."""
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(md + "\n")


# ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.exit(main())
