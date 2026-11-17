"""
Commit-quality analysis using Conventional Commits classification
plus a weighted scoring heuristic.

Score formula (0-100):
    base            = 40 if conventional-commit type detected else 10
    subject_length  = +20 if 10 <= len(subject) <= 72 else +5
    imperative_mood = +15 if subject starts with an imperative verb-like token
    body_present    = +15 if commit has a body beyond the subject line
    no_wip_marker   = +10 if not a "wip"/"fixup"/"tmp" style commit

The heuristic intentionally rewards commits that would pass a typical
open-source project's CONTRIBUTING.md checklist, without needing an
LLM call -- pure static analysis, so it works fully offline.
"""
from __future__ import annotations

import re

from .models import CommitQuality

CONVENTIONAL_RE = re.compile(
    r"^(?P<type>feat|fix|chore|docs|style|refactor|perf|test|build|ci|revert)"
    r"(?:\((?P<scope>[^)]+)\))?(?P<breaking>!)?:\s*(?P<subject>.+)$"
)

WIP_MARKERS = ("wip", "fixup!", "squash!", "tmp", "temp", "asdf", "test123", "xxx")

# A short list of common imperative-mood verb stems used in good commit
# subjects ("Add x", "Fix y", "Remove z") vs past-tense ("Added x").
IMPERATIVE_STEMS = (
    "add", "fix", "remove", "update", "refactor", "improve", "implement",
    "create", "delete", "rename", "move", "bump", "revert", "merge",
    "clean", "optimize", "document", "deprecate", "support", "enable",
    "disable", "handle", "prevent", "guard", "validate", "expose",
)


def _is_imperative(subject: str) -> bool:
    first_word = subject.strip().split(" ", 1)[0].lower()
    return first_word in IMPERATIVE_STEMS


def analyze_commit(sha: str, full_message: str) -> CommitQuality:
    lines = full_message.strip().splitlines()
    subject = lines[0] if lines else ""
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

    issues: list[str] = []
    m = CONVENTIONAL_RE.match(subject)
    is_conventional = m is not None
    commit_type = m.group("type") if m else None
    check_subject = m.group("subject") if m else subject

    score = 40.0 if is_conventional else 10.0
    if not is_conventional:
        issues.append("Not a Conventional Commit (expected e.g. 'fix: ...', 'feat: ...')")

    if 10 <= len(check_subject) <= 72:
        score += 20
    else:
        score += 5
        issues.append(f"Subject line length {len(check_subject)} chars (recommended 10-72)")

    if _is_imperative(check_subject):
        score += 15
    else:
        issues.append("Subject doesn't start with an imperative verb (e.g. 'Add', not 'Added')")

    if body:
        score += 15
    else:
        issues.append("No commit body -- consider explaining *why*, not just *what*")

    lowered = subject.lower()
    if not any(marker in lowered for marker in WIP_MARKERS):
        score += 10
    else:
        issues.append("Looks like a WIP/temporary commit message")

    return CommitQuality(
        sha=sha,
        message=subject,
        is_conventional=is_conventional,
        type_=commit_type,
        score=round(min(score, 100.0), 1),
        issues=issues,
    )


def analyze_commits(commits: list[tuple[str, str]]) -> list[CommitQuality]:
    """commits: list of (sha, full_message) tuples."""
    return [analyze_commit(sha, msg) for sha, msg in commits]


def average_score(results: list[CommitQuality]) -> float:
    if not results:
        return 0.0
    return round(sum(r.score for r in results) / len(results), 1)
