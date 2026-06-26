#!/usr/bin/env python3
"""Check and update GitHub-cloned OpenClaw skills."""

from __future__ import annotations

import argparse
import dataclasses
import json
import subprocess
import sys
from pathlib import Path


@dataclasses.dataclass
class SkillReport:
    path: str
    status: str
    tracking: str
    current_ref: str
    latest_ref: str
    remote_url: str
    dirty: bool
    behind_count: int = 0
    ahead_count: int = 0
    message: str = ""

    def to_dict(self) -> dict[str, object]:
        return dataclasses.asdict(self)


def run_git(repo: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        check=check,
        text=True,
        capture_output=True,
    )


def git_output(repo: Path, args: list[str], check: bool = True) -> str:
    return run_git(repo, args, check=check).stdout.strip()


def repo_exists(skill_path: Path) -> bool:
    return skill_path.exists() and (skill_path / "SKILL.md").exists()


def is_git_repo(skill_path: Path) -> bool:
    result = run_git(skill_path, ["rev-parse", "--is-inside-work-tree"], check=False)
    return result.returncode == 0 and result.stdout.strip() == "true"


def fetch_origin(skill_path: Path) -> None:
    run_git(skill_path, ["fetch", "--tags", "--prune", "origin"])


def current_branch(skill_path: Path) -> str:
    return git_output(skill_path, ["symbolic-ref", "--quiet", "--short", "HEAD"], check=False)


def exact_tag(skill_path: Path) -> str:
    return git_output(skill_path, ["describe", "--tags", "--exact-match"], check=False)


def latest_tag(skill_path: Path) -> str:
    tags = git_output(skill_path, ["tag", "--sort=-version:refname"]).splitlines()
    return next((tag for tag in tags if tag.strip()), "")


def dirty(skill_path: Path) -> bool:
    return bool(git_output(skill_path, ["status", "--porcelain"]))


def remote_url(skill_path: Path) -> str:
    return git_output(skill_path, ["remote", "get-url", "origin"], check=False)


def upstream_branch(skill_path: Path, branch: str) -> str:
    upstream = git_output(skill_path, ["rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"], check=False)
    if upstream:
        return upstream
    return f"origin/{branch}"


def branch_report(skill_path: Path, branch: str) -> SkillReport:
    upstream = upstream_branch(skill_path, branch)
    head = git_output(skill_path, ["rev-parse", "HEAD"])
    upstream_head = git_output(skill_path, ["rev-parse", upstream], check=False)
    if not upstream_head:
        return SkillReport(
            path=str(skill_path),
            status="unsupported",
            tracking="branch",
            current_ref=head,
            latest_ref="",
            remote_url=remote_url(skill_path),
            dirty=dirty(skill_path),
            message=f"找不到上游分支 {upstream}",
        )

    behind_count = int(git_output(skill_path, ["rev-list", "--count", f"HEAD..{upstream}"]))
    ahead_count = int(git_output(skill_path, ["rev-list", "--count", f"{upstream}..HEAD"]))
    if dirty(skill_path):
        status = "dirty"
        message = "仓库存在未提交改动，默认不更新。"
    elif behind_count > 0 and ahead_count == 0:
        status = "update-available"
        message = "远端分支有新提交。"
    elif ahead_count > 0 and behind_count == 0:
        status = "ahead"
        message = "本地提交领先远端，跳过自动更新。"
    elif behind_count > 0 and ahead_count > 0:
        status = "diverged"
        message = "本地与远端已分叉，跳过自动更新。"
    else:
        status = "up-to-date"
        message = "已是最新。"

    return SkillReport(
        path=str(skill_path),
        status=status,
        tracking="branch",
        current_ref=head,
        latest_ref=upstream_head,
        remote_url=remote_url(skill_path),
        dirty=dirty(skill_path),
        behind_count=behind_count,
        ahead_count=ahead_count,
        message=message,
    )


def tag_report(skill_path: Path, tag: str) -> SkillReport:
    newest = latest_tag(skill_path)
    if not newest:
        return SkillReport(
            path=str(skill_path),
            status="unsupported",
            tracking="tag",
            current_ref=tag,
            latest_ref="",
            remote_url=remote_url(skill_path),
            dirty=dirty(skill_path),
            message="未找到任何远端 tags。",
        )

    if dirty(skill_path):
        status = "dirty"
        message = "仓库存在未提交改动，默认不更新。"
    elif tag != newest:
        status = "update-available"
        message = "存在更新的 tag。"
    else:
        status = "up-to-date"
        message = "已是最新 tag。"

    return SkillReport(
        path=str(skill_path),
        status=status,
        tracking="tag",
        current_ref=tag,
        latest_ref=newest,
        remote_url=remote_url(skill_path),
        dirty=dirty(skill_path),
        message=message,
    )


def inspect_skill(skill_path: Path | str, fetch: bool = True) -> SkillReport:
    skill = Path(skill_path).resolve()
    if not repo_exists(skill):
        return SkillReport(str(skill), "unsupported", "none", "", "", "", False, message="目录缺少 SKILL.md。")
    if not is_git_repo(skill):
        return SkillReport(str(skill), "unsupported", "none", "", "", "", False, message="目录不是 git 仓库。")
    remote = remote_url(skill)
    if not remote:
        return SkillReport(str(skill), "unsupported", "none", "", "", "", dirty(skill), message="仓库缺少 origin 远端，无法检查更新。")
    if fetch:
        try:
            fetch_origin(skill)
        except subprocess.CalledProcessError as exc:
            detail = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            return SkillReport(str(skill), "unsupported", "none", "", "", remote, dirty(skill), message=f"获取 origin 失败：{detail}")

    branch = current_branch(skill)
    tag = exact_tag(skill)
    if tag and not branch:
        return tag_report(skill, tag)
    if branch:
        return branch_report(skill, branch)
    return SkillReport(
        path=str(skill),
        status="unsupported",
        tracking="detached",
        current_ref=git_output(skill, ["rev-parse", "HEAD"]),
        latest_ref="",
        remote_url=remote_url(skill),
        dirty=dirty(skill),
        message="当前仓库处于 detached HEAD 且没有精确 tag，无法安全判断更新策略。",
    )


def update_skill(skill_path: Path | str, allow_dirty: bool = False) -> SkillReport:
    report = inspect_skill(skill_path, fetch=True)
    skill = Path(skill_path).resolve()

    if report.status == "dirty" and not allow_dirty:
        report.message = "仓库存在未提交改动，默认不更新。"
        return report
    if report.status in {"unsupported", "ahead", "diverged", "up-to-date"}:
        return report

    if report.tracking == "branch":
        branch = current_branch(skill)
        run_git(skill, ["pull", "--ff-only", "origin", branch])
        refreshed = inspect_skill(skill, fetch=False)
        refreshed.status = "updated"
        refreshed.message = f"已快进更新到 {refreshed.latest_ref}。"
        return refreshed

    if report.tracking == "tag":
        run_git(skill, ["checkout", report.latest_ref])
        refreshed = inspect_skill(skill, fetch=False)
        refreshed.status = "updated"
        refreshed.message = f"已切换到最新 tag {refreshed.current_ref}。"
        return refreshed

    return report


def discover_skills(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    skill_dirs = []
    for candidate in sorted(root.iterdir()):
        if candidate.is_dir() and (candidate / "SKILL.md").exists():
            skill_dirs.append(candidate)
    return skill_dirs


def render_text(reports: list[SkillReport]) -> str:
    lines = []
    for report in reports:
        latest = report.latest_ref or "-"
        current = report.current_ref or "-"
        lines.append(f"[{report.status}] {report.path}")
        lines.append(f"  tracking={report.tracking} current={current} latest={latest}")
        if report.remote_url:
            lines.append(f"  remote={report.remote_url}")
        if report.message:
            lines.append(f"  note={report.message}")
    return "\n".join(lines)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check and update GitHub-cloned OpenClaw skills.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("check", "update"):
        sub = subparsers.add_parser(command)
        sub.add_argument("paths", nargs="*", default=["skills"], help="Skill paths or a parent directory.")
        sub.add_argument("--json", action="store_true", help="Print JSON output.")
        if command == "update":
            sub.add_argument("--allow-dirty", action="store_true", help="Allow update even if repo is dirty.")

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = [Path(path).resolve() for path in args.paths]
    skill_paths: list[Path] = []
    for path in paths:
        if path.name == "SKILL.md":
            skill_paths.append(path.parent)
            continue
        discovered = discover_skills(path)
        if discovered:
            skill_paths.extend(discovered)
        else:
            skill_paths.append(path)

    reports = []
    for skill_path in skill_paths:
        if args.command == "check":
            reports.append(inspect_skill(skill_path))
        else:
            reports.append(update_skill(skill_path, allow_dirty=args.allow_dirty))

    if args.json:
        print(json.dumps([report.to_dict() for report in reports], ensure_ascii=False, indent=2))
    else:
        print(render_text(reports))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
