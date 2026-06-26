#!/usr/bin/env python3
"""Operate GitHub mirror repositories that use a safe-sync workflow.

The script expects a GitHub token in the environment:
  GITHUB_TOKEN=... ./scripts/github_safe_sync.py status --owner ... --repo ...
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


API_ROOT = "https://api.github.com"
DEFAULT_WORKFLOW = "safe-sync.yml"
FORCE_PUSH_TITLE = "检测到上游强制推送"


def api_request(
    path: str,
    token: str,
    method: str = "GET",
    body: dict[str, Any] | None = None,
) -> Any:
    url = path if path.startswith("http") else f"{API_ROOT}{path}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    if body is not None:
        req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise SystemExit(f"GitHub API error {exc.code} for {url}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error for {url}: {exc}") from exc

    if not raw:
        return None
    return json.loads(raw.decode("utf-8"))


def paginate(path: str, token: str) -> list[dict[str, Any]]:
    page = 1
    items: list[dict[str, Any]] = []
    while True:
      separator = "&" if "?" in path else "?"
      data = api_request(f"{path}{separator}per_page=100&page={page}", token)
      if not isinstance(data, list) or not data:
          return items
      items.extend(data)
      page += 1


def get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        raise SystemExit("Set GITHUB_TOKEN before running this script.")
    return token


def metadata_only_files(files: list[str]) -> bool:
    return bool(files) and all(f.startswith(".github/") for f in files)


def fetch_commit_files(owner: str, repo: str, sha: str, token: str) -> list[str]:
    data = api_request(f"/repos/{owner}/{repo}/commits/{sha}", token)
    return [item["filename"] for item in data.get("files", [])]


def range_is_metadata_only(owner: str, repo: str, base: str | None, head: str, token: str) -> bool:
    if base:
        data = api_request(f"/repos/{owner}/{repo}/compare/{base}...{head}", token)
        commits = data.get("commits", [])
    else:
        data = api_request(f"/repos/{owner}/{repo}/commits?sha={head}&per_page=100", token)
        commits = data

    if not commits:
        return False

    for commit in commits:
        sha = commit["sha"]
        files = fetch_commit_files(owner, repo, sha, token)
        if not metadata_only_files(files):
            return False
    return True


def compare_branches(
    mirror_owner: str,
    mirror_repo: str,
    upstream_owner: str,
    upstream_repo: str,
    branch: str,
    token: str,
) -> dict[str, Any]:
    mirror_branch = api_request(f"/repos/{mirror_owner}/{mirror_repo}/branches/{branch}", token)
    mirror_sha = mirror_branch["commit"]["sha"]

    try:
        upstream_branch = api_request(f"/repos/{upstream_owner}/{upstream_repo}/branches/{branch}", token)
        upstream_branch_name = branch
    except SystemExit:
        upstream_repo_meta = api_request(f"/repos/{upstream_owner}/{upstream_repo}", token)
        upstream_branch_name = upstream_repo_meta["default_branch"]
        upstream_branch = api_request(
            f"/repos/{upstream_owner}/{upstream_repo}/branches/{upstream_branch_name}",
            token,
        )

    upstream_sha = upstream_branch["commit"]["sha"]
    compare = api_request(
        f"/repos/{mirror_owner}/{mirror_repo}/compare/{upstream_sha}...{mirror_sha}",
        token,
    )

    ahead_by = compare.get("ahead_by", 0)
    behind_by = compare.get("behind_by", 0)
    status = compare.get("status")
    merge_base = compare.get("merge_base_commit", {}).get("sha")

    effective = "diverged"
    if behind_by == 0 and ahead_by == 0:
        effective = "exact"
    elif behind_by > 0 and ahead_by == 0:
        effective = "behind"
    elif ahead_by > 0 and behind_by == 0:
        if merge_base and range_is_metadata_only(mirror_owner, mirror_repo, merge_base, mirror_sha, token):
            effective = "metadata-ahead"
        else:
            effective = "local-ahead"
    else:
        if merge_base and range_is_metadata_only(mirror_owner, mirror_repo, merge_base, mirror_sha, token):
            effective = "metadata-diverged"

    return {
        "mirror_branch": branch,
        "upstream_branch": upstream_branch_name,
        "mirror_sha": mirror_sha,
        "upstream_sha": upstream_sha,
        "compare_status": status,
        "ahead_by": ahead_by,
        "behind_by": behind_by,
        "effective_state": effective,
    }


def cmd_status(args: argparse.Namespace) -> int:
    token = get_token()
    repo_path = f"/repos/{args.owner}/{args.repo}"
    workflows = api_request(f"{repo_path}/actions/workflows", token).get("workflows", [])
    workflow = next((w for w in workflows if w["path"].endswith(args.workflow)), None)
    runs = api_request(f"{repo_path}/actions/runs?per_page=5", token).get("workflow_runs", [])
    backup_branches = [
        item["name"]
        for item in paginate(f"{repo_path}/branches", token)
        if item["name"].startswith(args.backup_prefix)
    ]
    open_issues = [
        item
        for item in paginate(f"{repo_path}/issues?state=open", token)
        if FORCE_PUSH_TITLE in item.get("title", "") and "pull_request" not in item
    ]

    result: dict[str, Any] = {
        "repository": f"{args.owner}/{args.repo}",
        "workflow": workflow and {
            "id": workflow["id"],
            "name": workflow["name"],
            "state": workflow["state"],
            "path": workflow["path"],
        },
        "latest_runs": [
            {
                "id": run["id"],
                "event": run["event"],
                "status": run["status"],
                "conclusion": run.get("conclusion"),
                "created_at": run["created_at"],
                "html_url": run["html_url"],
            }
            for run in runs
        ],
        "open_force_push_issue_count": len(open_issues),
        "backup_branch_count": len(backup_branches),
        "backup_branch_examples": backup_branches[:10],
    }

    if args.upstream:
        upstream_owner, upstream_repo = args.upstream.split("/", 1)
        result["branch_comparison"] = compare_branches(
            args.owner,
            args.repo,
            upstream_owner,
            upstream_repo,
            args.branch,
            token,
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_dispatch(args: argparse.Namespace) -> int:
    token = get_token()
    body = {"ref": args.ref, "inputs": {"force_sync": bool(args.force_sync)}}
    api_request(
        f"/repos/{args.owner}/{args.repo}/actions/workflows/{args.workflow}/dispatches",
        token,
        method="POST",
        body=body,
    )
    print(json.dumps({"ok": True, "repository": f"{args.owner}/{args.repo}", "workflow": args.workflow}))
    return 0


def cmd_close_force_push_issues(args: argparse.Namespace) -> int:
    token = get_token()
    repo_path = f"/repos/{args.owner}/{args.repo}"
    issues = [
        item
        for item in paginate(f"{repo_path}/issues?state=open", token)
        if FORCE_PUSH_TITLE in item.get("title", "") and "pull_request" not in item
    ]
    closed: list[int] = []
    for issue in issues[: args.limit]:
        api_request(
            f"{repo_path}/issues/{issue['number']}",
            token,
            method="PATCH",
            body={"state": "closed"},
        )
        closed.append(issue["number"])
    print(json.dumps({"closed_count": len(closed), "issue_numbers": closed}, ensure_ascii=False, indent=2))
    return 0


def cmd_delete_backups(args: argparse.Namespace) -> int:
    token = get_token()
    repo_path = f"/repos/{args.owner}/{args.repo}"
    branches = [
        item["name"]
        for item in paginate(f"{repo_path}/branches", token)
        if item["name"].startswith(args.backup_prefix)
    ]
    deleted: list[str] = []
    for name in branches[: args.limit]:
        if args.dry_run:
            deleted.append(name)
            continue
        encoded = urllib.parse.quote(f"heads/{name}", safe="")
        api_request(f"{repo_path}/git/refs/{encoded}", token, method="DELETE")
        deleted.append(name)
    print(json.dumps({"matched_count": len(branches), "processed_count": len(deleted), "branches": deleted}, ensure_ascii=False, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Inspect workflow, runs, issues, backups, and optional upstream comparison.")
    status.add_argument("--owner", required=True)
    status.add_argument("--repo", required=True)
    status.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    status.add_argument("--branch", default="main")
    status.add_argument("--upstream", help="Optional upstream repository in owner/repo form.")
    status.add_argument("--backup-prefix", default="backup/")
    status.set_defaults(func=cmd_status)

    dispatch = sub.add_parser("dispatch", help="Trigger a workflow_dispatch run.")
    dispatch.add_argument("--owner", required=True)
    dispatch.add_argument("--repo", required=True)
    dispatch.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    dispatch.add_argument("--ref", default="main")
    dispatch.add_argument("--force-sync", action="store_true")
    dispatch.set_defaults(func=cmd_dispatch)

    close_issues = sub.add_parser("close-force-push-issues", help="Close open force-push alert issues.")
    close_issues.add_argument("--owner", required=True)
    close_issues.add_argument("--repo", required=True)
    close_issues.add_argument("--limit", type=int, default=500)
    close_issues.set_defaults(func=cmd_close_force_push_issues)

    delete_backups = sub.add_parser("delete-backups", help="Delete backup/* branches.")
    delete_backups.add_argument("--owner", required=True)
    delete_backups.add_argument("--repo", required=True)
    delete_backups.add_argument("--backup-prefix", default="backup/")
    delete_backups.add_argument("--limit", type=int, default=1000)
    delete_backups.add_argument("--dry-run", action="store_true")
    delete_backups.set_defaults(func=cmd_delete_backups)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
