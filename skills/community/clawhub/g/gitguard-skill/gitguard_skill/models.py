"""Data models for GitGuard repo intelligence."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class SecretFinding:
    """A potential secret detected via entropy + pattern analysis."""
    file: str
    line_number: int
    line_preview: str      # redacted preview, never the raw secret
    entropy: float
    pattern_matched: str    # which detector fired: "high_entropy", "aws_key", "private_key", etc.
    severity: Severity
    confidence: float       # 0-1


@dataclass
class CommitQuality:
    sha: str
    message: str
    is_conventional: bool
    type_: str | None       # feat, fix, chore, docs, refactor...
    score: float            # 0-100
    issues: list[str] = field(default_factory=list)


@dataclass
class BranchInfo:
    name: str
    last_commit_date: str
    days_stale: int
    is_merged: bool
    ahead: int
    behind: int
    recommendation: str    # "keep", "merge", "delete", "review"


@dataclass
class DependencyStatus:
    name: str
    current_version: str
    latest_version: str | None
    versions_behind: int | None
    ecosystem: str          # "npm", "pypi", "cargo"
    is_stale: bool
    risk_note: str | None = None


@dataclass
class RepoHealthReport:
    repo_path: str
    health_score: float           # 0-100 composite score
    grade: str                    # A/B/C/D/F
    secret_findings: list[SecretFinding] = field(default_factory=list)
    stale_branches: list[BranchInfo] = field(default_factory=list)
    commit_quality_avg: float = 0.0
    stale_dependencies: list[DependencyStatus] = field(default_factory=list)
    uncommitted_changes: int = 0
    untracked_files: int = 0
    days_since_last_commit: int = 0
    summary: str = ""


@dataclass
class PullRequestInfo:
    number: int
    title: str
    author: str
    days_open: int
    is_stale: bool
    review_status: str
    url: str


@dataclass
class IssueInfo:
    number: int
    title: str
    labels: list[str]
    days_open: int
    is_stale: bool
    url: str
