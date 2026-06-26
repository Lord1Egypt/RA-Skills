import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from get_commits import get_all_repos, get_commits_by_repo
from get_admin_emails import get_admin_email

load_dotenv(os.path.expanduser("~/.config/gitea-routine-report/.env"))

GITEA_URL = os.getenv("GITEA_URL")
GITEA_TOKEN = os.getenv("GITEA_TOKEN")
UTC_PLUS_8 = timezone(timedelta(hours=8))


def parse_datetime_arg(value: str, end_of_day: bool = False) -> datetime:
    """解析用户输入的时间字符串（按 UTC+8）并转换为 UTC。"""
    value = value.strip()

    if len(value) == 10:
        dt = datetime.strptime(value, "%Y-%m-%d")
        if end_of_day:
            dt = dt + timedelta(hours=23, minutes=59, seconds=59)
        return dt.replace(tzinfo=UTC_PLUS_8).astimezone(timezone.utc)

    normalized = value.replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(normalized)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(value, fmt)
                break
            except ValueError:
                dt = None
        if dt is None:
            raise ValueError(
                "时间格式无效。请使用 YYYY-MM-DD 或 YYYY-MM-DDTHH:MM:SS（默认按 UTC+8 解释）"
            )

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC_PLUS_8)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.astimezone(timezone.utc)


def resolve_time_window(since_arg: str, until_arg: str):
    """统一时间窗口逻辑：输入和展示按 UTC+8，内部查询按 UTC。"""
    now_bjt = datetime.now(UTC_PLUS_8)

    if since_arg or until_arg:
        if not since_arg or not until_arg:
            raise ValueError("使用绝对时间段时，--since 和 --until 必须同时提供")

        since_dt = parse_datetime_arg(since_arg, end_of_day=False)
        until_dt = parse_datetime_arg(until_arg, end_of_day=True)

        if since_dt > until_dt:
            raise ValueError("时间范围无效：--since 不能晚于 --until")

        time_desc = "自定义时间段"
        since_bjt = since_dt.astimezone(UTC_PLUS_8)
        until_bjt = until_dt.astimezone(UTC_PLUS_8)
        time_range_detail = (
            f"{since_bjt.strftime('%Y-%m-%d %H:%M:%S')} 至 "
            f"{until_bjt.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)"
        )
        return since_dt, until_dt, time_desc, time_range_detail

    since_bjt = now_bjt - timedelta(hours=168)
    until_bjt = now_bjt
    since_dt = since_bjt.astimezone(timezone.utc)
    until_dt = until_bjt.astimezone(timezone.utc)
    time_desc = "过去 7 天"
    time_range_detail = (
        f"{since_bjt.strftime('%Y-%m-%d %H:%M:%S')} 至 "
        f"{until_bjt.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)"
    )
    return since_dt, until_dt, time_desc, time_range_detail


def get_repo_members(repo_full_name: str) -> list:
    """获取仓库所有成员名单"""
    import requests
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    url = f"{GITEA_URL}/api/v1/repos/{repo_full_name}/teams"
    members = set()

    # 方式一：获取仓库协作者
    collab_url = f"{GITEA_URL}/api/v1/repos/{repo_full_name}/collaborators"
    resp = requests.get(collab_url, headers=headers)
    if resp.status_code == 200:
        for u in resp.json():
            members.add(u.get("login", ""))

    # 方式二：加上 owner 本人
    repo_url = f"{GITEA_URL}/api/v1/repos/{repo_full_name}"
    resp2 = requests.get(repo_url, headers=headers)
    if resp2.status_code == 200:
        owner = resp2.json().get("owner", {}).get("login", "")
        if owner:
            members.add(owner)

    return list(members)


def get_member_last_commit(repo_full_name: str, username: str) -> str:
    """获取某成员在该仓库的最后一次提交日期"""
    import requests
    headers = {"Authorization": f"token {GITEA_TOKEN}"}
    url = f"{GITEA_URL}/api/v1/repos/{repo_full_name}/commits"
    params = {"limit": 1, "page": 1}
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        return None

    # 遍历所有提交找该成员最新的
    params_all = {"limit": 50, "page": 1}
    resp_all = requests.get(url, headers=headers, params=params_all)
    if resp_all.status_code != 200:
        return None

    for commit in resp_all.json():
        author = commit["commit"]["author"]["name"]
        if author == username:
            return commit["commit"]["author"]["date"]
    return None


def calc_inactive_days(last_commit_date: str) -> int:
    """计算距离最后一次提交过了多少天"""
    if not last_commit_date:
        return -1
    try:
        last = datetime.fromisoformat(last_commit_date.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        return (now - last).days
    except Exception:
        return -1


def build_summary(
    repo: str,
    commits: list,
    time_desc: str,
    time_range_detail: str,
) -> dict:
    now = datetime.now(UTC_PLUS_8)
    admin_email = get_admin_email(repo)
    generated_at = now.strftime("%Y-%m-%d %H:%M UTC+8")

    # 获取仓库所有成员
    all_members = get_repo_members(repo)

    if not commits:
        return {
            "repo": repo,
            "admin_email": admin_email,
            "time_range": time_desc,
            "time_range_detail": time_range_detail,
            "generated_at": generated_at,
            "has_commits": False,
            "overview": {
                "total_commits": 0,
                "total_members": 0,
                "total_deletions": 0
            },
            "members": {},
            "inactive_members": [],
            "vague_commits": []
        }

    # 按成员汇总
    member_stats = {}
    vague_commits = []

    for c in commits:
        author = c["author"]
        if author not in member_stats:
            member_stats[author] = {
                "commits": 0,
                "additions": 0,
                "deletions": 0,
                "messages": [],
                "vague_count": 0,
                "branches": [],
                "commit_details": [],
                "file_type_summary": {
                    "code": 0,
                    "doc": 0,
                    "data": 0,
                    "image": 0,
                    "other": 0
                }
            }

        member_stats[author]["commits"] += 1
        member_stats[author]["additions"] += c["stats"]["additions"]
        member_stats[author]["deletions"] += c["stats"]["deletions"]
        member_stats[author]["messages"].append(c["message"])

        if c["branch"] not in member_stats[author]["branches"]:
            member_stats[author]["branches"].append(c["branch"])

        member_stats[author]["commit_details"].append({
            "time": c["time"],
            "message": c["message"],
            "is_vague": c["is_vague"],
            "files": c["files"],
            "stats": c["stats"]
        })

        # 统计文件类型分布
        code_exts = {".py", ".js", ".ts", ".cpp", ".c", ".h", ".java", ".go", ".m"}
        doc_exts = {".md", ".txt", ".pdf", ".docx", ".doc", ".rst"}
        data_exts = {".json", ".yaml", ".yml", ".csv", ".xml"}
        image_exts = {".png", ".jpg", ".jpeg", ".gif", ".svg"}

        for f in c["files"]:
            ext = os.path.splitext(f["filename"])[-1].lower()
            if ext in code_exts:
                member_stats[author]["file_type_summary"]["code"] += 1
            elif ext in doc_exts:
                member_stats[author]["file_type_summary"]["doc"] += 1
            elif ext in data_exts:
                member_stats[author]["file_type_summary"]["data"] += 1
            elif ext in image_exts:
                member_stats[author]["file_type_summary"]["image"] += 1
            else:
                member_stats[author]["file_type_summary"]["other"] += 1

        if c["is_vague"]:
            member_stats[author]["vague_count"] += 1
            vague_commits.append({
                "author": author,
                "message": c["message"],
                "time": c["time"]
            })

    # 计算本期无提交成员及其最后提交信息
    active_authors = set(member_stats.keys())
    inactive_members = []
    for member in all_members:
        if member not in active_authors:
            last_date = get_member_last_commit(repo, member)
            inactive_days = calc_inactive_days(last_date)
            inactive_members.append({
                "name": member,
                "last_commit_date": last_date if last_date else "无记录",
                "inactive_days": inactive_days
            })

    return {
        "repo": repo,
        "admin_email": admin_email,
        "time_range": time_desc,
        "time_range_detail": time_range_detail,
        "generated_at": generated_at,
        "has_commits": True,
        "overview": {
            "total_commits": len(commits),
            "total_members": len(member_stats),
            "total_deletions": sum(c["stats"]["deletions"] for c in commits),
        },
        "members": member_stats,
        "inactive_members": inactive_members,
        "vague_commits": vague_commits
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=str, default=None)
    parser.add_argument("--since", type=str, default=None)
    parser.add_argument("--until", type=str, default=None)
    args = parser.parse_args()

    try:
        since_dt, until_dt, time_desc, time_range_detail = resolve_time_window(args.since, args.until)
    except ValueError as exc:
        print(f"参数错误: {exc}", file=sys.stderr)
        sys.exit(2)

    repos = [args.repo] if args.repo else get_all_repos()

    results = []
    for repo in repos:
        commits = get_commits_by_repo(repo, since=since_dt, until=until_dt)
        summary = build_summary(repo, commits, time_desc, time_range_detail)
        results.append(summary)

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()