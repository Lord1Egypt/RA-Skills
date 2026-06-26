from __future__ import annotations

from pathlib import Path

from openclaw_sec.models import AuditContext, Finding
from openclaw_sec.utils import find_secret_hits, read_text, run_command, unique_preserve


def scan_git(context: AuditContext) -> tuple[list[Finding], dict[str, str]]:
    if not context.enable_git:
        return [], {}
    root_result = run_command(["git", "-C", str(context.current_dir), "rev-parse", "--show-toplevel"])
    if not root_result.ok:
        return [], {}
    git_root = Path(root_result.stdout)
    files_result = run_command(["git", "-C", str(git_root), "ls-files"])
    if not files_result.ok:
        return [], {"git_root": str(git_root)}

    evidence: list[str] = []
    masked_examples: list[str] = []
    for rel_path in files_result.stdout.splitlines():
        path = git_root / rel_path
        hits = find_secret_hits(read_text(path))
        for hit in hits[:10]:
            evidence.append(f"{path}:{hit.line_no} ({hit.pattern_name})")
            masked_examples.append(hit.masked_value)

    findings: list[Finding] = []
    if evidence:
        findings.append(
            Finding(
                id="GIT-001",
                title="Secrets detected in git-tracked files",
                category="secrets",
                severity="critical",
                confidence="high",
                heuristic=False,
                evidence=evidence[:20],
                risk="Tracked secrets can leak through pushes, pull requests, forks, and local clones even after later deletion.",
                recommendation="Remove and rotate exposed secrets, then scrub them from the repository history if they were ever pushed.",
                masked_examples=unique_preserve(masked_examples)[:20],
                references=["Git tracked file scan", str(git_root)],
            )
        )
    return findings, {"git_root": str(git_root)}
