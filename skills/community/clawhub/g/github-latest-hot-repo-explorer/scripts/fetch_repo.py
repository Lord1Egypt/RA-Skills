#!/usr/bin/env python3
"""获取 GitHub 最新热门仓库，支持自动扩窗、历史去重，严格选取最高 star 仓库。"""
import argparse
import calendar
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Union

SEARCH_URL = "https://api.github.com/search/repositories"
README_URL_TMPL = "https://api.github.com/repos/{owner}/{repo}/readme"
PER_PAGE = 100
README_MAX_CHARS = 8000
WINDOW_STEPS = [1, 2, 3, 6, 12, 24, 36, 48, 60]
EARLIEST_DATE = date(2023, 3, 14)  # GPT-4 发布日，扩窗最早回溯到此日期
ROOT = Path(__file__).resolve().parent.parent
REPORT_DIR = ROOT / "assets" / "history"
HISTORY_FILE = REPORT_DIR / "history.json"


def subtract_months(d: date, months: int) -> date:
    y, m, day = d.year, d.month - months, d.day
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, min(day, calendar.monthrange(y, m)[1]))


def load_token() -> str:
    """优先读环境变量；读不到再从 ~/.openclaw/.env 读（OpenClaw exec 快照会过滤 token 类环境变量，故需文件回退）。"""
    token = os.environ.get("GITHUB_TOKEN", "")
    if token:
        return token
    env_file = os.path.expanduser("~/.openclaw/.env")
    try:
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("GITHUB_TOKEN="):
                    value = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if value:
                        return value
    except OSError:
        pass
    return ""


def rate_limit_message(token: str, status: int, detail: str) -> str:
    if token:
        return f"❌ GitHub API 请求受限（HTTP {status}）：已使用 GITHUB_TOKEN，但认证请求仍被限流或拒绝。请稍后重试。详情：{detail[:200]}"
    return f"❌ GitHub API 请求受限（HTTP {status}）：当前使用匿名请求，可能已触发限流。请在系统环境变量中配置 GITHUB_TOKEN 后重试。详情：{detail[:200]}"


def http_get(url: str, token: str, headers: Optional[dict] = None) -> Union[dict, str, None]:
    request_headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "github-latest-hot-repo-explorer"}
    if token:
        request_headers["Authorization"] = f"Bearer {token}"
    if headers:
        request_headers.update(headers)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=request_headers), timeout=30) as response:
            body = response.read()
            return json.loads(body.decode("utf-8")) if "json" in response.headers.get("Content-Type", "") else body.decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        if error.code == 401:
            sys.exit("❌ 401 Unauthorized：系统环境变量 GITHUB_TOKEN 无效、已撤销或没有访问权限。")
        if error.code in (403, 429):
            sys.exit(rate_limit_message(token, error.code, detail))
        if error.code == 404:
            return None
        sys.exit(f"❌ HTTP {error.code}: {error.reason}")


def load_history() -> list:
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8")).get("shown", []) if HISTORY_FILE.exists() else []
    except Exception:
        return []


def save_history(repo: dict) -> None:
    data = {"shown": load_history()}
    data["shown"].append({"full_name": repo["full_name"], "shown_at": datetime.now().isoformat(timespec="seconds"), "stars": repo.get("stargazers_count"), "html_url": repo.get("html_url")})
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def search_repos(token: str, stars: int, since: date) -> list:
    query = f"stars:>{stars} created:>{since.isoformat()}"
    print(f"🔍 查询条件：{query}  (按 stars 降序)")
    url = f"{SEARCH_URL}?{urllib.parse.urlencode({'q': query, 'sort': 'stars', 'order': 'desc', 'per_page': PER_PAGE})}"
    data = http_get(url, token)
    if not isinstance(data, dict) or "items" not in data:
        sys.exit(f"❌ 搜索接口返回异常：{str(data)[:200]}")
    print(f"📊 命中总数：{data.get('total_count', 0)}, 本次拉取：{len(data['items'])}\n")
    return data["items"]


def fetch_readme(repo: dict, token: str) -> str:
    readme = http_get(README_URL_TMPL.format(owner=repo["owner"]["login"], repo=repo["name"]), token, {"Accept": "application/vnd.github.raw"})
    if not readme:
        return ""
    return readme[:README_MAX_CHARS] + (f"\n\n... (truncated, total {len(readme)} chars)" if len(readme) > README_MAX_CHARS else "")


def pick_with_auto_expand(token: str, stars: int, start_months: int, exclude: set) -> tuple:
    start = next((i for i, months in enumerate(WINDOW_STEPS) if months >= start_months), len(WINDOW_STEPS) - 1)
    for index in range(start, len(WINDOW_STEPS)):
        months = WINDOW_STEPS[index]
        since = subtract_months(date.today(), months)
        capped = since <= EARLIEST_DATE
        if capped:
            since = EARLIEST_DATE
        label = f"回溯至截止日期 {EARLIEST_DATE.isoformat()}" if capped else f"最近 {months} 个自然月"
        print(f"⏱️  {'起始窗口' if index == start else '自动扩窗'}: {label} (created>{since.isoformat()})")
        candidates = [item for item in search_repos(token, stars, since) if item["full_name"] not in exclude]
        if candidates:
            return max(candidates, key=lambda x: x.get("stargazers_count", 0)), months
        if capped:
            break
        print("   当前窗口无未播报仓库，尝试更大窗口...\n")
    sys.exit(f"❌ 已回溯到最早截止日期 {EARLIEST_DATE.isoformat()} 仍无新仓库可抽。用 --reset-history 重置或调整 --stars。")


def report_path(full_name: str) -> Path:
    """返回 assets/history/YYYY-MM-DD-owner-repo.md（本地日期）。"""
    return REPORT_DIR / f"{date.today().isoformat()}-{full_name.replace('/', '-')}.md"


def present(repo: dict, token: str, dry_run: bool, months: int) -> None:
    print(f"🔖 最近 {months} 月热门仓库：{repo['full_name']}\n")
    print(f"📦 **{repo['full_name']}**\n⭐ stars: {repo['stargazers_count']}\n🍴 forks: {repo['forks_count']}\n💻 language: {repo.get('language') or 'N/A'}\n📅 created: {repo['created_at']}\n🔗 {repo['html_url']}\n📝 {repo.get('description') or '(无描述)'}\n")
    readme = "(dry-run: 跳过 README 抓取)" if dry_run else fetch_readme(repo, token)
    print("=== README (前 8000 字符) ===\n" + (readme or "(无 README 或抓取失败)") + "\n=== README END ===\n")
    print("=== 请基于以上信息回答 ===\n1) 这个仓库的项目是什么？\n2) 解决了什么问题？\n3) 如何解决？")
    if not dry_run:
        print(f"\n> 回答完三个问题后，须将完整回答（不含 README 原文）保存为：{report_path(repo['full_name'])}")


def main() -> None:
    parser = argparse.ArgumentParser(description="获取一个 GitHub 最新热门仓库并打印元数据和 README")
    parser.add_argument("--stars", type=int, default=5000)
    parser.add_argument("--months", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true", help="预览：使用本地样例，不请求 GitHub，不写历史")
    parser.add_argument("--reset-history", action="store_true")
    args = parser.parse_args()
    if args.reset_history:
        HISTORY_FILE.unlink(missing_ok=True)
        print("✅ 历史已清空")
        return
    history = load_history()
    exclude = {item["full_name"] for item in history}
    token = "" if args.dry_run else load_token()
    if not args.dry_run and not token:
        print("ℹ️ 未配置 GITHUB_TOKEN，将使用 GitHub 匿名请求。若遇到 API 限流，请配置系统环境变量 GITHUB_TOKEN 后重试。", file=sys.stderr)
    if args.dry_run:
        fixture = ROOT / "scripts" / "fixtures" / "items.json"
        items = json.loads(fixture.read_text(encoding="utf-8"))
        candidates = [item for item in items if item["full_name"] not in exclude] or items
        repo = max(candidates, key=lambda x: x.get("stargazers_count", 0))
        months = args.months
    else:
        repo, months = pick_with_auto_expand(token, args.stars, args.months, exclude)
    present(repo, token, args.dry_run, months)
    if args.dry_run:
        print("\nℹ️ dry-run 模式：不写入历史，不保存回答。")
        return
    save_history(repo)
    print(f"\n✅ 已记录到 {HISTORY_FILE}  (actual_months={months})")


if __name__ == "__main__":
    main()
