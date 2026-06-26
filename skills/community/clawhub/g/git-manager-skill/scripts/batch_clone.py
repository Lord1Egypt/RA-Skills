#!/usr/bin/env python3
"""
batch_clone.py - 批量克隆 Git 仓库
支持 GitHub / GitLab / Gitea / Bitbucket / Azure DevOps 批量克隆
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import quote


# ─────────────────────────────────────────────
# HTTP 辅助
# ─────────────────────────────────────────────

def http_get(url: str, token: str = None, accept: str = "application/json",
             auth_type: str = "bearer") -> dict | list:
    """发送 GET 请求，返回解析后的 JSON
    auth_type: 'bearer'（GitHub/GitLab/Gitea/Bitbucket）或 'basic'（Azure DevOps）
    """
    headers = {"Accept": accept, "User-Agent": "git-manager-skill/1.0"}
    if token:
        if auth_type == "basic":
            # Azure DevOps: Basic Base64(":PAT")
            encoded = base64.b64encode(f":{token}".encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        else:
            headers["Authorization"] = f"Bearer {token}"
            headers["PRIVATE-TOKEN"] = token  # GitLab 兼容
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except HTTPError as e:
        body = e.read().decode(errors="replace")
        print(f"[HTTP {e.code}] {url}\n  {body[:300]}")
        return None
    except URLError as e:
        print(f"[URL Error] {url}: {e.reason}")
        return None


def paginate(base_url: str, token: str = None, page_param: str = "page",
             per_page_param: str = "per_page", per_page: int = 100) -> list:
    """自动分页获取所有数据"""
    results = []
    page = 1
    sep = "&" if "?" in base_url else "?"
    while True:
        url = f"{base_url}{sep}{page_param}={page}&{per_page_param}={per_page}"
        data = http_get(url, token)
        if not data:
            break
        if isinstance(data, dict):
            # Gitea 风格：{"data": [...]}
            items = data.get("data", [])
        else:
            items = data
        if not items:
            break
        results.extend(items)
        if len(items) < per_page:
            break
        page += 1
        time.sleep(0.2)  # 避免频率限制
    return results


# ─────────────────────────────────────────────
# GitHub
# ─────────────────────────────────────────────

def github_list_org_repos(org: str, token: str = None) -> list:
    """列出 GitHub Organization 下所有仓库"""
    url = f"https://api.github.com/orgs/{quote(org)}/repos"
    return paginate(url, token, per_page_param="per_page")


def github_list_user_repos(username: str, token: str = None) -> list:
    """列出 GitHub 用户下所有仓库"""
    url = f"https://api.github.com/users/{quote(username)}/repos"
    return paginate(url, token, per_page_param="per_page")


def github_get_repo(owner: str, repo: str, token: str = None) -> dict:
    """获取单个 GitHub 仓库信息"""
    url = f"https://api.github.com/repos/{quote(owner)}/{quote(repo)}"
    return http_get(url, token)


# ─────────────────────────────────────────────
# GitLab
# ─────────────────────────────────────────────

def gitlab_list_group_repos(host: str, group_id: str, token: str = None, recursive: bool = True) -> list:
    """列出 GitLab Group 下所有仓库"""
    gid = quote(str(group_id), safe="")
    include_subgroups = "true" if recursive else "false"
    url = f"{host}/api/v4/groups/{gid}/projects?include_subgroups={include_subgroups}"
    return paginate(url, token)


def gitlab_list_user_repos(host: str, user_id: str, token: str = None) -> list:
    """列出 GitLab User 下所有仓库"""
    uid = quote(str(user_id), safe="")
    url = f"{host}/api/v4/users/{uid}/projects"
    return paginate(url, token)


def gitlab_get_repo(host: str, project_id: str, token: str = None) -> dict:
    """通过 project_id 获取单个 GitLab 仓库"""
    pid = quote(str(project_id), safe="")
    url = f"{host}/api/v4/projects/{pid}"
    return http_get(url, token)


# ─────────────────────────────────────────────
# Gitea
# ─────────────────────────────────────────────

def gitea_list_org_repos(host: str, org: str, token: str = None) -> list:
    """列出 Gitea Organization 下所有仓库"""
    url = f"{host}/api/v1/orgs/{quote(org)}/repos"
    return paginate(url, token, page_param="page", per_page_param="limit")


def gitea_list_user_repos(host: str, username: str, token: str = None) -> list:
    """列出 Gitea 用户下所有仓库"""
    url = f"{host}/api/v1/users/{quote(username)}/repos"
    return paginate(url, token, page_param="page", per_page_param="limit")


def gitea_list_org_teams(host: str, org: str, token: str = None) -> list:
    """列出 Gitea 组织下所有 Team"""
    url = f"{host}/api/v1/orgs/{quote(org)}/teams"
    return paginate(url, token, page_param="page", per_page_param="limit")


# ─────────────────────────────────────────────
# Bitbucket
# ─────────────────────────────────────────────

def bitbucket_list_workspace_repos(workspace: str, token: str = None) -> list:
    """列出 Bitbucket Workspace 下所有仓库"""
    url = f"https://api.bitbucket.org/2.0/repositories/{quote(workspace)}"
    repos = paginate(url, token, page_param="page", per_page_param="pagelen")
    # 标准化字段，便于后续统一处理
    for r in repos:
        r["name"] = r.get("name", r.get("slug", "unknown"))
        r["archived"] = r.get("is_private", False)  # Bitbucket 无 archived 字段
        # 提取 clone URL
        clone_links = r.get("links", {}).get("clone", [])
        for c in clone_links:
            if c.get("name") == "https":
                r["clone_url"] = c.get("href", "")
            elif c.get("name") == "ssh":
                r["ssh_url"] = c.get("href", "")
    return repos


# ─────────────────────────────────────────────
# Azure DevOps
# ─────────────────────────────────────────────

def azure_list_project_repos(organization: str, project: str, token: str = None) -> list:
    """列出 Azure DevOps Project 下所有 Git 仓库"""
    url = (f"https://dev.azure.com/{quote(organization)}/"
           f"{quote(project)}/_apis/git/repositories?api-version=6.0")
    data = http_get(url, token, auth_type="basic")
    if not data:
        return []
    repos = data.get("value", [])
    # 标准化字段
    for r in repos:
        r["name"] = r.get("name", "unknown")
        r["archived"] = False
        # 构造 clone URL（Azure DevOps API 不直接返回 clone URL）
        proj = r.get("project", {}).get("name", project)
        repo_name = r.get("name", "unknown")
        r["clone_url"] = f"https://dev.azure.com/{organization}/{proj}/_git/{quote(repo_name)}"
        r["ssh_url"] = f"git@ssh.dev.azure.com:v3/{organization}/{proj}/{quote(repo_name)}"
    return repos


# ─────────────────────────────────────────────
# 提取 clone URL
# ─────────────────────────────────────────────

def extract_clone_url(repo_info: dict, platform: str, use_ssh: bool) -> tuple[str, str]:
    """从仓库信息中提取克隆 URL 和仓库名"""
    if platform == "github":
        name = repo_info.get("name", "unknown")
        url = repo_info.get("ssh_url" if use_ssh else "clone_url", "")
    elif platform == "gitlab":
        name = repo_info.get("path", repo_info.get("name", "unknown"))
        url = repo_info.get("ssh_url_to_repo" if use_ssh else "http_url_to_repo", "")
    elif platform == "gitea":
        name = repo_info.get("name", "unknown")
        url = repo_info.get("ssh_url" if use_ssh else "clone_url", "")
    elif platform == "bitbucket":
        name = repo_info.get("name", "unknown")
        url = repo_info.get("ssh_url" if use_ssh else "clone_url", "")
    elif platform == "azure":
        name = repo_info.get("name", "unknown")
        url = repo_info.get("ssh_url" if use_ssh else "clone_url", "")
    else:
        name = repo_info.get("name", "unknown")
        url = repo_info.get("clone_url", repo_info.get("html_url", ""))
    return name, url


# ─────────────────────────────────────────────
# 克隆单个仓库
# ─────────────────────────────────────────────

def clone_repo(url: str, dest_dir: str, branch: str = None, depth: int = None,
               skip_existing: bool = True, lfs: bool = False) -> str:
    """克隆或更新单个仓库，返回 'cloned' / 'updated' / 'skipped' / 'failed'"""
    dest_path = Path(dest_dir)

    # 已存在时拉取更新
    if (dest_path / ".git").exists():
        if skip_existing:
            print(f"  [SKIP] 已存在，跳过: {dest_dir}")
            return "skipped"
        print(f"  [UPDATE] 已存在，执行 git pull: {dest_dir}")
        result = subprocess.run(
            ["git", "pull", "--ff-only"],
            cwd=dest_dir, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"  [OK] 更新成功")
            if lfs:
                _run_lfs_install(dest_dir)
            return "updated"
        else:
            print(f"  [WARN] 更新失败: {result.stderr.strip()}")
            return "failed"

    cmd = ["git", "clone", "--progress"]
    if branch:
        cmd += ["-b", branch]
    if depth:
        cmd += ["--depth", str(depth)]
    cmd += [url, dest_dir]

    print(f"  [CLONE] {url}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  [OK] 克隆成功 -> {dest_dir}")
        if lfs:
            _run_lfs_install(dest_dir)
        return "cloned"
    else:
        err = result.stderr.strip()
        print(f"  [FAIL] 克隆失败: {err[:200]}")
        return "failed"


def _run_lfs_install(repo_dir: str):
    """对已克隆的仓库初始化 Git LFS"""
    result = subprocess.run(
        ["git", "lfs", "install", "--quiet"],
        cwd=repo_dir, capture_output=True, text=True
    )
    if result.returncode == 0:
        # 追加 .gitattributes（如果存在 LFS 跟踪规则）
        gitattributes = Path(repo_dir) / ".gitattributes"
        if gitattributes.exists():
            with open(gitattributes, "r", encoding="utf-8") as f:
                content = f.read()
            if "filter=lfs" not in content:
                # 追加 LFS 相关规则
                lfs_patterns = ["*.zip", "*.tar", "*.gz", "*.bin", "*.exe",
                                "*.dmg", "*.pkg", "*.iso", "*.img",
                                "*.pdf", "*.png", "*.jpg", "*.jpeg",
                                "*.mp4", "*.mp3", "*.wav", "*.mov",
                                "*.psd", "*.ai", "*.sketch", "*.fig"]
                new_rules = "\n".join(
                    f"{p} filter=lfs diff=lfs merge=lfs -text"
                    for p in lfs_patterns if p not in content
                )
                with open(gitattributes, "a", encoding="utf-8") as f:
                    f.write(f"\n# Git LFS\n{new_rules}\n")
                print(f"  [LFS] 已更新 .gitattributes")
        else:
            print(f"  [LFS] 已初始化（无 .gitattributes）")
    else:
        print(f"  [LFS] 初始化失败（git-lfs 可能未安装）")


# ─────────────────────────────────────────────
# 批量克隆入口
# ─────────────────────────────────────────────

def batch_clone(repos: list, platform: str, output_dir: str,
                use_ssh: bool = False, branch: str = None,
                depth: int = None, skip_existing: bool = True,
                dry_run: bool = False, lfs: bool = False,
                workers: int = 1, output_format: str = "text") -> dict:
    """批量克隆仓库列表"""
    stats = {"cloned": 0, "updated": 0, "skipped": 0, "failed": 0, "total": len(repos)}
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    results = []  # 用于 JSON 输出

    def clone_one(repo):
        name, url = extract_clone_url(repo, platform, use_ssh)
        dest = str(output_path / name)
        if dry_run:
            lfs_tag = " [LFS]" if lfs else ""
            msg = f"  [DRY-RUN] 将克隆: {url} -> {dest}{lfs_tag}"
            print(f"\n[{repos.index(repo)+1}/{len(repos)}] {name}\n  {msg}")
            return {"name": name, "url": url, "dest": dest, "status": "dry-run"}
        status = clone_repo(url, dest, branch, depth, skip_existing, lfs=lfs)
        return {"name": name, "url": url, "dest": dest, "status": status}

    if workers > 1:
        # 并发模式
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {executor.submit(clone_one, repo): repo for repo in repos}
            done = 0
            for future in as_completed(futures):
                done += 1
                res = future.result()
                results.append(res)
                status = res["status"]
                stats[status] = stats.get(status, 0) + 1
                if output_format == "text":
                    icon = {"cloned": "✅", "updated": "🔄", "skipped": "⏭️", "failed": "❌", "dry-run": "🔍"}.get(status, "?")
                    print(f"  [{done}/{len(repos)}] {icon} {res['name']}")
    else:
        # 顺序模式
        for i, repo in enumerate(repos, 1):
            res = clone_one(repo)
            results.append(res)
            stats[res["status"]] = stats.get(res["status"], 0) + 1

    # JSON 输出
    if output_format == "json":
        output = {"stats": stats, "repos": results}
        print(json.dumps(output, ensure_ascii=False, indent=2))

    return stats


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="批量克隆 Git 仓库（GitHub/GitLab/Gitea/Bitbucket/Azure DevOps）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # GitHub organization 下所有仓库
  python batch_clone.py --platform github --type org --id my-org --output ./repos

  # GitLab group（需要 token）
  python batch_clone.py --platform gitlab --host https://gitlab.com --type group --id 123 --token glpat-xxx

  # Gitea 用户仓库（使用 SSH）
  python batch_clone.py --platform gitea --host https://gitea.example.com --type user --id johndoe --ssh

  # Bitbucket workspace 下所有仓库
  python batch_clone.py --platform bitbucket --type workspace --id my-workspace --token BB_TOKEN

  # Azure DevOps 项目下所有仓库
  python batch_clone.py --platform azure --org my-org --project MyProject --token AZURE_PAT

  # Dry run 预览
  python batch_clone.py --platform github --type org --id my-org --dry-run
"""
    )
    parser.add_argument("--platform",
                        choices=["github", "gitlab", "gitea", "bitbucket", "azure"],
                        required=True, help="Git 平台类型")
    parser.add_argument("--host", default=None,
                        help="GitLab/Gitea 主机地址（如 https://gitlab.com），GitHub/Bitbucket 不需要")
    parser.add_argument("--org", dest="organization", default=None,
                        help="Azure DevOps 组织名（--platform azure 时必填）")
    parser.add_argument("--project", default=None,
                        help="Azure DevOps 项目名（--platform azure 时必填）")
    parser.add_argument("--type", dest="id_type",
                        choices=["org", "group", "user", "project"],
                        required=True, help="ID 类型（org/group/user/project）")
    parser.add_argument("--id", dest="target_id", required=True,
                        help="组织名/组 ID/用户 ID/项目 ID")
    parser.add_argument("--token", default=None,
                        help="API 访问令牌，也可通过环境变量 GITHUB_TOKEN / GITLAB_TOKEN / GITEA_TOKEN 传入")
    parser.add_argument("--output", default="./repos", help="本地存储目录（默认 ./repos）")
    parser.add_argument("--branch", default=None, help="指定克隆分支")
    parser.add_argument("--depth", type=int, default=None, help="浅克隆深度")
    parser.add_argument("--ssh", action="store_true", help="使用 SSH 克隆（默认 HTTPS）")
    parser.add_argument("--update", action="store_true",
                        help="仓库已存在时执行 pull 更新（默认跳过）")
    parser.add_argument("--dry-run", action="store_true", help="仅列出仓库，不实际克隆")
    parser.add_argument("--filter", default=None,
                        help="按仓库名过滤（支持子字符串匹配，如 --filter api）")
    parser.add_argument("--archived", action="store_true",
                        help="包含已归档仓库（默认排除）")
    parser.add_argument("--limit", type=int, default=None,
                        help="最多处理前 N 个仓库（如 --limit 5）")
    parser.add_argument("--lfs", action="store_true",
                        help="克隆后初始化 Git LFS 并追加常见二进制文件跟踪规则到 .gitattributes")
    parser.add_argument("--workers", type=int, default=1,
                        help="并发克隆线程数（默认 1，设为 4 可显著加速大批量克隆）")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式：text（默认）或 json（便于程序化处理）")
    parser.add_argument("--recursive", action="store_true", default=True,
                        help="包含 GitLab 子组（默认开启，使用 --no-recursive 禁用）")
    parser.add_argument("--no-recursive", dest="recursive", action="store_false",
                        help="禁用 GitLab 子组递归")

    args = parser.parse_args()

    # 设置默认 host / organization / project
    if args.platform == "github":
        host = "https://api.github.com"
    elif args.platform == "gitlab":
        host = args.host.rstrip("/") if args.host else "https://gitlab.com"
    elif args.platform == "gitea":
        if not args.host:
            print("[ERROR] Gitea 需要指定 --host 参数")
            sys.exit(1)
        host = args.host.rstrip("/")
    elif args.platform == "azure":
        if not args.organization or not args.project:
            print("[ERROR] Azure DevOps 需要指定 --org 和 --project 参数")
            sys.exit(1)

    # 获取仓库列表
    # Token 优先使用显式参数，其次使用环境变量
    env_map = {
        "github": "GITHUB_TOKEN",
        "gitlab": "GITLAB_TOKEN",
        "gitea": "GITEA_TOKEN",
    }
    env_token = os.environ.get(env_map.get(args.platform.upper(), ""), "")
    token = args.token or env_token
    if not token and args.platform != "github":
        print("[提示] 未指定 token，部分私有仓库可能无法访问")
    elif not token:
        print("[提示] 未指定 token，GitHub API 限速 60次/小时，建议设置 GITHUB_TOKEN")

    print(f"\n{'='*60}")
    print(f"平台: {args.platform.upper()}  |  类型: {args.id_type}  |  ID: {args.target_id}")
    print(f"输出目录: {args.output}")
    print(f"Token: {'✅ 已设置' if token else '❌ 未设置'}")
    if args.workers > 1:
        print(f"并发: {args.workers} 线程")
    print(f"{'='*60}")
    print("\n[正在获取仓库列表...]")

    repos = []
    platform = args.platform
    tid = args.target_id

    if platform == "github":
        if args.id_type in ("org", "group"):
            repos = github_list_org_repos(tid, token)
        elif args.id_type == "user":
            repos = github_list_user_repos(tid, token)
        elif args.id_type == "project":
            r = github_get_repo(tid.split("/")[0], tid.split("/")[-1], token)
            if r:
                repos = [r]

    elif platform == "gitlab":
        if args.id_type in ("group",):
            repos = gitlab_list_group_repos(host, tid, token, recursive=args.recursive)
        elif args.id_type == "user":
            repos = gitlab_list_user_repos(host, tid, token)
        elif args.id_type in ("project",):
            r = gitlab_get_repo(host, tid, token)
            if r:
                repos = [r]
        elif args.id_type == "org":
            repos = gitlab_list_group_repos(host, tid, token, recursive=args.recursive)

    elif platform == "gitea":
        if args.id_type in ("org", "group"):
            repos = gitea_list_org_repos(host, tid, token)
        elif args.id_type == "user":
            repos = gitea_list_user_repos(host, tid, token)

    elif platform == "bitbucket":
        if args.id_type in ("workspace", "org", "group"):
            repos = bitbucket_list_workspace_repos(tid, args.token)
        elif args.id_type == "user":
            repos = bitbucket_list_workspace_repos(tid, args.token)

    elif platform == "azure":
        if args.id_type in ("project",):
            repos = azure_list_project_repos(args.organization, args.project, args.token)
        elif args.id_type in ("org",):
            # Azure 没有 org 级别的 repo，只能按 project 操作
            print("[ERROR] Azure DevOps 不支持 org 级别，请使用 --type project --project <项目名>")
            sys.exit(1)

    if repos is None:
        repos = []

    print(f"[获取完成] 共 {len(repos)} 个仓库")

    # 过滤归档仓库
    if not args.archived:
        before = len(repos)
        repos = [r for r in repos if not r.get("archived", False)]
        filtered = before - len(repos)
        if filtered:
            print(f"[过滤] 排除 {filtered} 个已归档仓库")

    # 名称过滤
    if args.filter:
        before = len(repos)
        repos = [r for r in repos if args.filter.lower() in r.get("name", "").lower()]
        print(f"[过滤] 名称含 '{args.filter}': {before} -> {len(repos)} 个")

    # 数量限制
    if args.limit and args.limit > 0:
        repos = repos[:args.limit]
        print(f"[限制] 只处理前 {args.limit} 个仓库")

    if not repos:
        print("[WARN] 没有找到任何仓库，请检查 ID、权限或 token")
        sys.exit(0)

    # 打印仓库列表
    print(f"\n{'─'*60}")
    print(f"待处理仓库列表（共 {len(repos)} 个）:")
    for i, r in enumerate(repos, 1):
        name = r.get("name", r.get("path", "?"))
        print(f"  {i:3}. {name}")
    print(f"{'─'*60}")

    # 执行批量克隆
    stats = batch_clone(
        repos=repos,
        platform=platform,
        output_dir=args.output,
        use_ssh=args.ssh,
        branch=args.branch,
        depth=args.depth,
        skip_existing=not args.update,
        dry_run=args.dry_run,
        lfs=args.lfs,
        workers=args.workers,
        output_format=args.format,
    )

    # 统计结果
    if args.format == "text":
        print(f"\n{'='*60}")
        print("批量操作完成！")
        print(f"  总计: {stats['total']}")
        if not args.dry_run:
            print(f"  克隆: {stats.get('cloned', 0)}")
            print(f"  更新: {stats.get('updated', 0)}")
            print(f"  跳过: {stats.get('skipped', 0)}")
            print(f"  失败: {stats.get('failed', 0)}")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
