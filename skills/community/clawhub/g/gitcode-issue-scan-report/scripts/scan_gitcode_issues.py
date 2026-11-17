#!/usr/bin/env python3
"""Scan GitCode issues, classify linked PR status, and generate Markdown reports."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

DEFAULT_TYPES = {"rfc", "feature", "bug", "roadmap"}


def _labels(issue: dict[str, Any]) -> list[str]:
    return [str(item.get("name", "")) for item in issue.get("labels", [])]


def _primary_type(issue: dict[str, Any], type_labels: set[str]) -> str:
    labels = set(_labels(issue))
    for name in ("rfc", "feature", "bug", "roadmap"):
        if name in type_labels and name in labels:
            return name
    return "other"


def _record(
    issue: dict[str, Any],
    relations: list[dict[str, Any]],
    merged_bases: dict[int, str],
    type_labels: set[str],
) -> dict[str, Any]:
    number = int(issue["number"])
    issue_relations = [
        row for row in relations if int(row.get("issue", {}).get("number", -1)) == number
    ]
    merged_rows = [row for row in issue_relations if row.get("pr", {}).get("state") == "merged"]
    open_rows = [row for row in issue_relations if row.get("pr", {}).get("state") == "open"]
    closed_rows = [row for row in issue_relations if row.get("pr", {}).get("state") == "closed"]
    merged_prs = [
        {"number": int(row["pr"]["number"]), "base": merged_bases.get(int(row["pr"]["number"]), "unknown")}
        for row in merged_rows
    ]
    return {
        "number": number,
        "title": str(issue.get("title", "")),
        "state": str(issue.get("state", "open")),
        "type": _primary_type(issue, type_labels),
        "labels": _labels(issue),
        "merged_prs": merged_prs,
        "open_prs": [{"number": int(row["pr"]["number"])} for row in open_rows],
        "closed_prs": [{"number": int(row["pr"]["number"])} for row in closed_rows],
    }


def classify_issues(
    issues: list[dict[str, Any]],
    relations: list[dict[str, Any]],
    merged_prs: list[dict[str, Any]],
    *,
    type_labels: set[str] | None = None,
    include_ids: set[int] | None = None,
    exclude_ids: set[int] | None = None,
    target_branch: str = "master",
) -> dict[str, Any]:
    """Classify each included open issue exactly once and reconcile scope counts."""
    type_labels = set(type_labels or DEFAULT_TYPES)
    include_ids = set(include_ids or set())
    exclude_ids = set(exclude_ids or set())
    merged_bases = {
        int(pr["number"]): str(pr.get("base", {}).get("ref", "unknown")) for pr in merged_prs
    }

    included_issues: list[dict[str, Any]] = []
    excluded_issues: list[dict[str, Any]] = []
    for issue in issues:
        number = int(issue["number"])
        matches_type = bool(set(_labels(issue)) & type_labels)
        if number in exclude_ids:
            excluded_issues.append(issue)
        elif matches_type or number in include_ids:
            included_issues.append(issue)
        else:
            excluded_issues.append(issue)

    categories: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for issue in included_issues:
        item = _record(issue, relations, merged_bases, type_labels)
        if item["type"] in {"rfc", "feature"}:
            target_merged = [pr for pr in item["merged_prs"] if pr["base"] == target_branch]
            if target_merged and not item["open_prs"]:
                categories["close_ready"].append(item)
            elif target_merged and item["open_prs"]:
                categories["mixed"].append(item)
            elif item["merged_prs"]:
                categories["merged_other_branch"].append(item)
            elif item["open_prs"]:
                categories["open_only"].append(item)
            else:
                categories["no_pr"].append(item)
        elif item["type"] == "bug":
            categories["bugs"].append(item)
        elif item["type"] == "roadmap":
            categories["roadmaps"].append(item)
        else:
            categories["other"].append(item)

    for values in categories.values():
        values.sort(key=lambda item: item["number"], reverse=True)

    excluded = [
        {
            "number": int(issue["number"]),
            "title": str(issue.get("title", "")),
            "labels": _labels(issue),
            "explicit": int(issue["number"]) in exclude_ids,
        }
        for issue in excluded_issues
    ]
    excluded.sort(key=lambda item: item["number"], reverse=True)

    result = {
        "counts": {
            "open_total": len(issues),
            "included": len(included_issues),
            "excluded": len(excluded_issues),
        },
        "target_branch": target_branch,
        "type_labels": sorted(type_labels),
        "explicit_include": sorted(include_ids),
        "explicit_exclude": sorted(exclude_ids),
        "excluded": excluded,
    }
    for key in (
        "close_ready",
        "mixed",
        "merged_other_branch",
        "open_only",
        "no_pr",
        "bugs",
        "roadmaps",
        "other",
    ):
        result[key] = categories.get(key, [])
    return result


def _escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _issue_link(repo: str, number: int) -> str:
    return f"[#{number}](https://gitcode.com/{repo}/issues/{number})"


def _pr_link(repo: str, number: int) -> str:
    return f"[#{number}](https://gitcode.com/{repo}/merge_requests/{number})"


def _pr_list(repo: str, prs: Iterable[dict[str, Any]], include_base: bool = False) -> str:
    values = []
    for pr in prs:
        text = _pr_link(repo, int(pr["number"]))
        if include_base:
            text += f" → `{_escape(pr.get('base', 'unknown'))}`"
        values.append(text)
    return "、".join(values) if values else "—"


def _labels_cell(item: dict[str, Any]) -> str:
    return "、".join(f"`{_escape(label)}`" for label in item.get("labels", [])) or "—"


def _append_issue_table(
    lines: list[str],
    repo: str,
    items: list[dict[str, Any]],
    mode: str,
    *,
    target_branch: str | None = None,
) -> None:
    if mode == "close":
        lines.extend(["| 类型 | Issue | 标题 | 已合入目标分支的 PR |", "|---|---|---|---|"])
        for item in items:
            target = [pr for pr in item["merged_prs"] if pr["base"] == target_branch]
            lines.append(
                f"| {item['type'].upper()} | {_issue_link(repo, item['number'])} | {_escape(item['title'])} | {_pr_list(repo, target)} |"
            )
    elif mode == "mixed":
        lines.extend(["| 类型 | Issue | 标题 | 已合入 PR | 开放 PR |", "|---|---|---|---|---|"])
        for item in items:
            lines.append(
                f"| {item['type'].upper()} | {_issue_link(repo, item['number'])} | {_escape(item['title'])} | {_pr_list(repo, item['merged_prs'], True)} | {_pr_list(repo, item['open_prs'])} |"
            )
    elif mode == "other_branch":
        lines.extend(["| 类型 | Issue | 标题 | 已合入 PR 及目标分支 | 开放 PR |", "|---|---|---|---|---|"])
        for item in items:
            lines.append(
                f"| {item['type'].upper()} | {_issue_link(repo, item['number'])} | {_escape(item['title'])} | {_pr_list(repo, item['merged_prs'], True)} | {_pr_list(repo, item['open_prs'])} |"
            )
    elif mode == "open":
        lines.extend(["| 类型 | Issue | 标题 | 开放 PR |", "|---|---|---|---|"])
        for item in items:
            lines.append(
                f"| {item['type'].upper()} | {_issue_link(repo, item['number'])} | {_escape(item['title'])} | {_pr_list(repo, item['open_prs'])} |"
            )
    else:
        lines.extend(["| 类型 | Issue | 标题 | 标签 | PR 状态 |", "|---|---|---|---|---|"])
        for item in items:
            parts = []
            if item["merged_prs"]:
                parts.append(f"已合入：{_pr_list(repo, item['merged_prs'], True)}")
            if item["open_prs"]:
                parts.append(f"开放：{_pr_list(repo, item['open_prs'])}")
            if item["closed_prs"]:
                parts.append(f"已关闭：{_pr_list(repo, item['closed_prs'])}")
            pr_state = "<br>".join(parts) if parts else "无关联 PR"
            lines.append(
                f"| {item['type'].upper()} | {_issue_link(repo, item['number'])} | {_escape(item['title'])} | {_labels_cell(item)} | {pr_state} |"
            )


def render_report(repo: str, scan_date: str, result: dict[str, Any]) -> str:
    """Render a Markdown report where every included issue appears once as a link."""
    counts = result["counts"]
    lines = [
        f"# {repo} Issue 扫描报告",
        "",
        f"- 仓库：[`{repo}`](https://gitcode.com/{repo})",
        f"- 扫描日期：{scan_date}",
        f"- 目标分支：`{result['target_branch']}`",
        f"- 类型标签：{', '.join(f'`{label}`' for label in result['type_labels'])}",
        "",
        "## 范围守恒",
        "",
        "| 口径 | 数量 |",
        "|---|---:|",
        f"| 仓库全部 Open Issue | {counts['open_total']} |",
        f"| 报告纳入 | {counts['included']} |",
        f"| 报告排除 | {counts['excluded']} |",
        "",
        f"校验：`{counts['included']} + {counts['excluded']} = {counts['open_total']}`。",
        "",
        "## 满足关闭条件的 RFC/Feature",
        "",
        "条件：Issue 为 Open；至少一个关联 PR 已合入目标分支；没有开放关联 PR。",
        "",
    ]
    _append_issue_table(
        lines,
        repo,
        result["close_ready"],
        "close",
        target_branch=result["target_branch"],
    )
    lines.extend(["", "## 已合入目标分支但仍有开放 PR", ""])
    _append_issue_table(lines, repo, result["mixed"], "mixed")
    lines.extend(["", "## 仅合入其他分支", ""])
    _append_issue_table(lines, repo, result["merged_other_branch"], "other_branch")
    lines.extend(["", "## 有开放 PR，等待合入", ""])
    _append_issue_table(lines, repo, result["open_only"], "open")
    lines.extend(["", "## 无有效关联 PR 的 RFC/Feature", ""])
    _append_issue_table(lines, repo, result["no_pr"], "generic")
    lines.extend(["", "## Bug", ""])
    _append_issue_table(lines, repo, result["bugs"], "generic")
    lines.extend(["", "## Roadmap", ""])
    _append_issue_table(lines, repo, result["roadmaps"], "generic")
    lines.extend(["", "## 额外纳入", ""])
    _append_issue_table(lines, repo, result["other"], "generic")
    lines.extend(["", "## 排除项", ""])
    if result["excluded"]:
        lines.append("以下 Issue 未进入分类表。显式排除项标记为“显式排除”；其余项未命中类型标签。")
        lines.append("")
        lines.extend(["| Issue | 标题 | 原因 |", "|---|---|---|"])
        for item in result["excluded"]:
            reason = "显式排除" if item["explicit"] else "未命中类型标签且未显式纳入"
            lines.append(f"| `#{item['number']}` | {_escape(item['title'])} | {reason} |")
    else:
        lines.append("无。")
    return "\n".join(lines) + "\n"

def render_close_script(
    repo: str,
    candidates: list[dict[str, Any]],
    *,
    shell: str,
    target_branch: str,
    add_resolved: bool,
    gitcode_command: str = "gitcode-npm",
) -> str:
    """Generate, but never execute, a script that revalidates each candidate before closing."""
    numbers = [int(item["number"]) for item in candidates]
    if shell == "powershell":
        add_label = (
            '        & $gitcode issue label $issue -R $repo --add resolved --json | Out-Null\n'
            if add_resolved
            else ""
        )
        return f'''# Generated GitCode Issue close script. Review before running.
$ErrorActionPreference = "Stop"
$gitcode = "{gitcode_command}"
$repo = "{repo}"
$targetBranch = "{target_branch}"
$issues = @({",".join(str(number) for number in numbers)})

foreach ($issue in $issues) {{
    $issueObj = (& $gitcode issue view $issue -R $repo --json | Out-String | ConvertFrom-Json)
    $prs = @((& $gitcode issue prs $issue -R $repo --mode 1 --json | Out-String | ConvertFrom-Json))
    $hasOpenPr = @($prs | Where-Object {{ $_.state -eq "open" }}).Count -gt 0
    $hasMergedTarget = @($prs | Where-Object {{ $_.state -eq "merged" -and $_.base.ref -eq $targetBranch }}).Count -gt 0

    if ($issueObj.state -eq "open" -and $hasMergedTarget -and -not $hasOpenPr) {{
{add_label}        & $gitcode issue edit $issue -R $repo --state close --yes --json | Out-Null
        $after = (& $gitcode issue view $issue -R $repo --json | Out-String | ConvertFrom-Json)
        if ($after.state -ne "closed") {{ throw "Issue #$issue did not close" }}
        Write-Host "Closed #$issue"
    }} else {{
        Write-Warning "Skipped #$issue: state=$($issueObj.state), merged-target=$hasMergedTarget, open-pr=$hasOpenPr"
    }}
}}
'''
    if shell == "bash":
        add_label = (
            '    "$gitcode_cmd" issue label "$issue" -R "$repo" --add resolved --json >/dev/null\n'
            if add_resolved
            else ""
        )
        number_text = " ".join(str(number) for number in numbers)
        return f'''#!/usr/bin/env bash
# Generated GitCode Issue close script. Review before running.
set -euo pipefail
gitcode_cmd="{gitcode_command}"
repo="{repo}"
target_branch="{target_branch}"
issues=({number_text})

for issue in "${{issues[@]}}"; do
  issue_state=$("$gitcode_cmd" issue view "$issue" -R "$repo" --json | python -c 'import json,sys; print(json.load(sys.stdin)["state"])')
  read -r has_open_pr has_merged_target < <(
    "$gitcode_cmd" issue prs "$issue" -R "$repo" --mode 1 --json |
      python -c 'import json,sys; p=json.load(sys.stdin); target=sys.argv[1]; print(int(any(x.get("state")=="open" for x in p)), int(any(x.get("state")=="merged" and x.get("base",{{}}).get("ref")==target for x in p)))' "$target_branch"
  )
  if [[ "$issue_state" == "open" && "$has_open_pr" == "0" && "$has_merged_target" == "1" ]]; then
{add_label}    "$gitcode_cmd" issue edit "$issue" -R "$repo" --state close --yes --json >/dev/null
    after_state=$("$gitcode_cmd" issue view "$issue" -R "$repo" --json | python -c 'import json,sys; print(json.load(sys.stdin)["state"])')
    [[ "$after_state" == "closed" ]] || {{ echo "Issue #$issue did not close" >&2; exit 1; }}
    echo "Closed #$issue"
  else
    echo "Skipped #$issue: state=$issue_state merged-target=$has_merged_target open-pr=$has_open_pr" >&2
  fi
done
'''
    raise ValueError(f"Unsupported shell: {shell}")


def _parse_ids(value: str) -> set[int]:
    if not value.strip():
        return set()
    return {int(part.strip()) for part in value.split(",") if part.strip()}


def _run_json(command: str, args: list[str], timeout: int = 300) -> Any:
    completed = subprocess.run(
        [command, *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    return json.loads(completed.stdout.lstrip("\ufeff"))


def _detect_command(explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in ("gitcode-npm", "gitcode"):
        found = shutil.which(candidate)
        if found:
            return found
    raise RuntimeError("GitCode CLI not found. Install/configure it before scanning.")


def scan_live(repo: str, command: str, limit: int) -> tuple[list[Any], list[Any], list[Any], dict[str, Any]]:
    auth = _run_json(command, ["auth", "status", "--json"])
    if not auth.get("logged_in"):
        raise RuntimeError("GitCode CLI is not logged in.")
    issues = _run_json(command, ["issue", "list", "-R", repo, "--state", "open", "--limit", str(limit), "--json"])
    relations = _run_json(
        command,
        ["issue", "relations", "-R", repo, "--state", "open", "--limit", str(limit), "--mode", "1", "--json"],
    )
    merged = _run_json(
        command,
        ["pr", "list", "-R", repo, "--state", "merged", "--paginate", "--per-page", "100", "--json"],
    )
    safe_auth = {key: auth.get(key) for key in ("username", "logged_in", "token_source", "git_protocol")}
    return issues, relations, merged, safe_auth


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="GitCode repository, for example Ascend/msinsight")
    parser.add_argument("--output", type=Path, help="Markdown output path")
    parser.add_argument("--types", default=",".join(sorted(DEFAULT_TYPES)), help="Comma-separated label names")
    parser.add_argument("--include", default="", help="Comma-separated Issue numbers to include regardless of labels")
    parser.add_argument("--exclude", default="", help="Comma-separated Issue numbers to exclude")
    parser.add_argument("--target-branch", default="master", help="Branch that merged PRs must target")
    parser.add_argument("--limit", type=int, default=1000, help="Maximum Open Issues inspected by GitCode relations")
    parser.add_argument("--gitcode-command", help="GitCode CLI command; auto-detects gitcode-npm then gitcode")
    parser.add_argument("--emit-close-script", type=Path, help="Write a revalidating close script for close-ready Issues")
    parser.add_argument("--shell", choices=("auto", "powershell", "bash"), default="auto")
    parser.add_argument("--add-resolved", action="store_true", help="Close script adds resolved before closing")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = _detect_command(args.gitcode_command)
    issues, relations, merged, auth = scan_live(args.repo, command, args.limit)
    result = classify_issues(
        issues,
        relations,
        merged,
        type_labels={value.strip() for value in args.types.split(",") if value.strip()},
        include_ids=_parse_ids(args.include),
        exclude_ids=_parse_ids(args.exclude),
        target_branch=args.target_branch,
    )
    output = args.output or Path(f"gitcode-issue-scan-{date.today().isoformat()}.md")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_report(args.repo, date.today().isoformat(), result), encoding="utf-8")

    if args.emit_close_script:
        shell = args.shell
        if shell == "auto":
            shell = "powershell" if platform.system() == "Windows" else "bash"
        close_text = render_close_script(
            args.repo,
            result["close_ready"],
            shell=shell,
            target_branch=args.target_branch,
            add_resolved=args.add_resolved,
            gitcode_command=command,
        )
        args.emit_close_script.parent.mkdir(parents=True, exist_ok=True)
        args.emit_close_script.write_text(close_text, encoding="utf-8", newline="\n")
        if shell == "bash":
            os.chmod(args.emit_close_script, 0o755)

    print(json.dumps({"account": auth, "report": str(output), "counts": result["counts"], "close_ready": len(result["close_ready"]), "close_script": str(args.emit_close_script) if args.emit_close_script else None}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())