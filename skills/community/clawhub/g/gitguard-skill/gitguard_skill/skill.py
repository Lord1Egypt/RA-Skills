"""GitGuard: advanced Git/GitHub repo intelligence for AI agents."""
from __future__ import annotations

import os
from enum import Enum

from .commits import analyze_commits, average_score
from .deps import check_dependencies
from .entropy import scan_repo
from .git_local import list_branches, recent_commits
from .github_api import get_open_issues, get_open_pull_requests
from .health import analyze_repo_health


def _to_dict(obj):
    """Recursively convert dataclasses/Enums/lists into plain JSON-safe
    dicts. Deliberately avoids dataclasses.asdict() because it flattens
    nested dataclasses/Enums into plain values in one pass, which skips
    our Enum-to-string conversion for nested fields."""
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, list):
        return [_to_dict(o) for o in obj]
    if isinstance(obj, dict):
        return {k: _to_dict(v) for k, v in obj.items()}
    if hasattr(obj, "__dataclass_fields__"):
        return {f: _to_dict(getattr(obj, f)) for f in obj.__dataclass_fields__}
    return obj


class GitGuard:
    """Main entrypoint. One instance per session; all methods are stateless
    beyond an optional GitHub token pulled from the environment."""

    def scan_secrets(self, repo_path: str, entropy_threshold: float = 4.0) -> dict:
        """Scan a repository for exposed secrets (API keys, tokens, private
        keys) using entropy analysis + known credential patterns. Never
        returns raw secret values -- only redacted previews and locations."""
        findings = scan_repo(repo_path, entropy_threshold)
        return {
            "repo_path": repo_path,
            "total_findings": len(findings),
            "critical": len([f for f in findings if f.severity.value == "critical"]),
            "high": len([f for f in findings if f.severity.value == "high"]),
            "findings": _to_dict(findings),
        }

    def health_report(self, repo_path: str, check_dependencies: bool = True) -> dict:
        """Full composite health report: secrets, branches, commit quality,
        dependencies, and activity, rolled into a single 0-100 score."""
        report = analyze_repo_health(repo_path, check_deps=check_dependencies)
        return _to_dict(report)

    def multi_repo_dashboard(self, repo_paths: list[str]) -> dict:
        """Run health_report across many local repos and rank them by score
        -- built for people juggling a dozen+ active projects at once."""
        reports = []
        for path in repo_paths:
            if os.path.isdir(path):
                reports.append(analyze_repo_health(path))
        reports.sort(key=lambda r: r.health_score)
        return {
            "repo_count": len(reports),
            "average_score": round(sum(r.health_score for r in reports) / len(reports), 1) if reports else 0,
            "worst_first": _to_dict(reports),
        }

    def commit_quality(self, repo_path: str, limit: int = 30) -> dict:
        """Analyze the last N commits for Conventional Commits compliance
        and message quality (subject length, imperative mood, body presence)."""
        commits = recent_commits(repo_path, limit=limit)
        results = analyze_commits(commits)
        return {
            "repo_path": repo_path,
            "commits_analyzed": len(results),
            "average_score": average_score(results),
            "commits": _to_dict(results),
        }

    def stale_branches(self, repo_path: str) -> dict:
        """List local branches with staleness/merge-status and a
        keep/review/delete/merge recommendation for each."""
        raw = list_branches(repo_path)
        return {"repo_path": repo_path, "branches": raw}

    def dependency_check(self, repo_path: str, staleness_threshold: int = 5) -> dict:
        """Check package.json / requirements.txt against the live npm/PyPI
        registries and flag dependencies that are meaningfully out of date."""
        deps = check_dependencies(repo_path, staleness_threshold=staleness_threshold)
        return {
            "repo_path": repo_path,
            "total_dependencies": len(deps),
            "stale_count": len([d for d in deps if d.is_stale]),
            "dependencies": _to_dict(deps),
        }

    def github_triage(self, owner: str, repo: str, pr_stale_days: int = 14,
                       issue_stale_days: int = 30) -> dict:
        """Fetch open PRs and issues from GitHub and flag which ones have
        gone stale, so you know what actually needs attention."""
        prs = get_open_pull_requests(owner, repo, stale_days=pr_stale_days)
        issues = get_open_issues(owner, repo, stale_days=issue_stale_days)
        return {
            "repo": f"{owner}/{repo}",
            "open_pull_requests": len(prs),
            "stale_pull_requests": len([p for p in prs if p.is_stale]),
            "open_issues": len(issues),
            "stale_issues": len([i for i in issues if i.is_stale]),
            "pull_requests": _to_dict(prs),
            "issues": _to_dict(issues),
        }
