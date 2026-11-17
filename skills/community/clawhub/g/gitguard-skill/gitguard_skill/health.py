"""
Composite repo health scoring.

The health score (0-100) is a weighted blend of five signals, each
normalized to 0-100 before weighting so that no single signal (e.g. a
huge dependency list) can dominate the score by sheer count:

    secret_safety     35%   -- fewer/less-severe exposed secrets = higher
    commit_hygiene     20%   -- average Conventional Commit quality score
    branch_hygiene     20%   -- fraction of branches that are NOT stale/dead
    dependency_health   15%   -- fraction of dependencies that are current
    activity            10%   -- recency of last commit (decays over 90 days)

    health_score = 0.35*secret_safety + 0.20*commit_hygiene
                 + 0.20*branch_hygiene + 0.15*dependency_health
                 + 0.10*activity

Grade bands: A >= 90, B >= 75, C >= 60, D >= 40, F < 40.

This weighting is a heuristic, not a certification -- it's meant to
give a fast, explainable signal for where to focus cleanup effort
across many repos, which is exactly the workflow of someone juggling
a dozen+ active projects.
"""
from __future__ import annotations

from .commits import analyze_commits, average_score
from .deps import check_dependencies
from .entropy import scan_repo
from .git_local import (
    days_since_last_commit,
    is_git_repo,
    list_branches,
    recent_commits,
    uncommitted_changes_count,
    untracked_files_count,
)
from .models import BranchInfo, RepoHealthReport, Severity

SEVERITY_PENALTY = {
    Severity.CRITICAL: 40,
    Severity.HIGH: 20,
    Severity.MEDIUM: 8,
    Severity.LOW: 2,
}


def _secret_safety_score(findings) -> float:
    if not findings:
        return 100.0
    penalty = sum(SEVERITY_PENALTY[f.severity] * f.confidence for f in findings)
    return max(0.0, 100.0 - penalty)


def _branch_recommendation(b: dict) -> str:
    if b["is_merged"] and b["days_stale"] > 14:
        return "delete"
    if b["days_stale"] > 90 and not b["is_merged"]:
        return "review"
    if b["ahead"] > 0 and b["behind"] > 20:
        return "review"
    return "keep"


def _branch_hygiene_score(branches: list[dict]) -> float:
    if not branches:
        return 100.0
    healthy = sum(1 for b in branches if _branch_recommendation(b) == "keep")
    return round(100.0 * healthy / len(branches), 1)


def _dependency_health_score(deps) -> float:
    if not deps:
        return 100.0
    fresh = sum(1 for d in deps if not d.is_stale)
    return round(100.0 * fresh / len(deps), 1)


def _activity_score(days_since_commit: int) -> float:
    if days_since_commit < 0:
        return 50.0  # unknown
    if days_since_commit <= 7:
        return 100.0
    if days_since_commit >= 90:
        return 0.0
    # linear decay between 7 and 90 days
    return round(100.0 * (1 - (days_since_commit - 7) / (90 - 7)), 1)


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    if score >= 60:
        return "C"
    if score >= 40:
        return "D"
    return "F"


def analyze_repo_health(repo_path: str, entropy_threshold: float = 4.0,
                         check_deps: bool = True,
                         stale_branch_days: int = 60) -> RepoHealthReport:
    if not is_git_repo(repo_path):
        return RepoHealthReport(
            repo_path=repo_path, health_score=0.0, grade="F",
            summary="Not a git repository.",
        )

    secret_findings = scan_repo(repo_path, entropy_threshold)
    raw_branches = list_branches(repo_path)
    branches = [
        BranchInfo(
            name=b["name"], last_commit_date="", days_stale=b["days_stale"],
            is_merged=b["is_merged"], ahead=b["ahead"], behind=b["behind"],
            recommendation=_branch_recommendation(b),
        )
        for b in raw_branches
    ]
    stale_branches = [b for b in branches if b.recommendation != "keep"]

    commits_raw = recent_commits(repo_path, limit=30)
    commit_results = analyze_commits(commits_raw)
    commit_avg = average_score(commit_results)

    deps = check_dependencies(repo_path) if check_deps else []
    stale_deps = [d for d in deps if d.is_stale]

    uncommitted = uncommitted_changes_count(repo_path)
    untracked = untracked_files_count(repo_path)
    days_since = days_since_last_commit(repo_path)

    secret_score = _secret_safety_score(secret_findings)
    branch_score = _branch_hygiene_score(raw_branches)
    dep_score = _dependency_health_score(deps)
    activity = _activity_score(days_since)

    health_score = round(
        0.35 * secret_score
        + 0.20 * commit_avg
        + 0.20 * branch_score
        + 0.15 * dep_score
        + 0.10 * activity,
        1,
    )

    summary_bits = []
    if secret_findings:
        summary_bits.append(f"{len(secret_findings)} potential secret(s) found")
    if stale_branches:
        summary_bits.append(f"{len(stale_branches)} branch(es) need attention")
    if stale_deps:
        summary_bits.append(f"{len(stale_deps)} dependency(ies) are stale")
    if uncommitted:
        summary_bits.append(f"{uncommitted} uncommitted change(s)")
    summary = "; ".join(summary_bits) if summary_bits else "Repo looks healthy."

    return RepoHealthReport(
        repo_path=repo_path,
        health_score=health_score,
        grade=_grade(health_score),
        secret_findings=secret_findings,
        stale_branches=stale_branches,
        commit_quality_avg=commit_avg,
        stale_dependencies=stale_deps,
        uncommitted_changes=uncommitted,
        untracked_files=untracked,
        days_since_last_commit=days_since,
        summary=summary,
    )
