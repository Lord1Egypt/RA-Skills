"""Git log parsing and conventional commit analysis."""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .config import COMMIT_TYPE_MAPPING, CHANGE_TYPES


def parse_git_log(repo_path: str, since: Optional[str] = None, until: Optional[str] = None) -> List[Dict]:
    """
    Parse git log from a repository.

    Args:
        repo_path: Path to git repository
        since: Start date (e.g., "2026-03-01")
        until: End date (e.g., "2026-04-01")

    Returns:
        List of dicts with keys: hash, date, author, message, body
    """
    if not Path(repo_path).is_dir():
        raise ValueError(f"Invalid repository path: {repo_path}")

    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%H%n%aI%n%an%n%s%n%b%n---COMMIT_END---"]

    if since:
        cmd.extend(["--since", since])
    if until:
        cmd.extend(["--until", until])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git command failed: {e.stderr}")

    commits = []
    commit_blocks = output.split("---COMMIT_END---")

    for block in commit_blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split("\n", 3)
        if len(lines) < 3:
            continue

        commit = {
            "hash": lines[0].strip(),
            "date": lines[1].strip(),
            "author": lines[2].strip(),
            "message": lines[3].strip() if len(lines) > 3 else "",
            "body": lines[4].strip() if len(lines) > 4 else ""
        }
        commits.append(commit)

    return commits


def parse_conventional_commit(message: str) -> Dict:
    """
    Parse a conventional commit message.

    Returns dict with: type, scope, description, breaking
    """
    pattern = r"^(\w+)(?:\(([^)]*)\))?!?: (.+)$"
    match = re.match(pattern, message)

    if not match:
        return {
            "type": None,
            "scope": None,
            "description": message,
            "breaking": False
        }

    commit_type, scope, description = match.groups()
    breaking = message.find("!:") != -1

    return {
        "type": commit_type.lower(),
        "scope": scope,
        "description": description,
        "breaking": breaking
    }


def categorize_commit(message: str, body: str = "") -> Dict:
    """
    Categorize a commit into change_type and audience.

    Returns dict with: change_type, audience, scope
    """
    parsed = parse_conventional_commit(message)
    commit_type = parsed.get("type", "").lower()

    # Map commit type to change type
    change_type = COMMIT_TYPE_MAPPING.get(commit_type, "CHANGED")

    # Determine audience from commit type and body
    audience = "INTERNAL"  # Default to internal

    # Client-facing by default for feat and fix
    if commit_type in ["feat", "feature", "fix", "bugfix"]:
        audience = "CLIENT"

    # Check for audience hints in body
    if body:
        body_lower = body.lower()
        if "breaking" in body_lower or "breaking change" in body_lower:
            change_type = "REMOVED"
            parsed["breaking"] = True
        if "client" in body_lower or "user" in body_lower:
            audience = "CLIENT"
        if "internal" in body_lower or "refactor" in body_lower:
            audience = "INTERNAL"

    # Security commits are always important
    if commit_type == "security":
        audience = "CLIENT"

    return {
        "change_type": change_type,
        "audience": audience,
        "scope": parsed.get("scope"),
        "breaking": parsed.get("breaking", False)
    }


def generate_entries_from_git(repo_path: str, since_tag: Optional[str] = None) -> List[Dict]:
    """
    Full pipeline: git log -> parse -> categorize -> return structured entries.

    Args:
        repo_path: Path to git repository
        since_tag: Only include commits after this tag (e.g., "v1.2.0")

    Returns:
        List of structured entry dicts
    """
    # Get commits since tag if provided
    if since_tag:
        commits = parse_git_log(repo_path, since=f"{since_tag}^")
    else:
        commits = parse_git_log(repo_path)

    entries = []
    for commit in commits:
        categorization = categorize_commit(commit["message"], commit["body"])
        parsed = parse_conventional_commit(commit["message"])

        entry = {
            "description": parsed["description"],
            "change_type": categorization["change_type"],
            "audience": categorization["audience"],
            "author": commit["author"],
            "commit_hash": commit["hash"],
            "breaking": categorization["breaking"],
            "details": commit["body"] if commit["body"] else None,
            "scope": categorization["scope"]
        }
        entries.append(entry)

    return entries


def get_latest_tag(repo_path: str) -> Optional[str]:
    """Get the latest git tag."""
    cmd = ["git", "-C", repo_path, "describe", "--tags", "--abbrev=0"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def get_commits_since_tag(repo_path: str, tag: str) -> List[Dict]:
    """Get all commits since a specific tag."""
    return parse_git_log(repo_path, since=f"{tag}^")


def validate_semver(version: str) -> bool:
    """Validate semantic versioning format (major.minor.patch)."""
    pattern = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    return bool(re.match(pattern, version))


def increment_version(version: str, bump_type: str = "patch") -> str:
    """
    Increment a semantic version.

    Args:
        version: Current version (e.g., "1.2.3")
        bump_type: "major", "minor", or "patch"

    Returns:
        New version string
    """
    parts = version.split(".")
    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}"
