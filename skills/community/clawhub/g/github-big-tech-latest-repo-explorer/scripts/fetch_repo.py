#!/usr/bin/env python3
"""github-big-tech-latest-repo-explorer

Explore the most recently created public repos from a user-provided list of
big-tech GitHub organizations, pick one (random) that has not been shown
before, and output a structured summary in the style of
`github-latest-hot-repo-explorer`.

Organization config is a JSON object: { "<Company>": ["<org-url>", ...], ... }
The script flattens that to a list of (company, org_login) pairs and queries
each org individually via the GitHub Core API, then filters, dedupes and ranks.

Hard filter: only repos with stargazers_count > MIN_STARS are considered.
Default time window is 3 months, auto-expanding to 6 / 12 / 24 / 36 / 48 / 60 months
(same as github-latest-hot-repo-explorer), capped at the GPT-4 release date
(2023-03-14) when no candidates match.
no unseen repo satisfies the star threshold.

Usage:
  python3 fetch_repo.py [--months 3] [--count 1]
                        [--org-config references/organizations.json]
                        [--reset-history] [--dry-run]
"""

from __future__ import annotations

import argparse
import calendar
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_ORG_CONFIG = SKILL_DIR / "references" / "organizations.json"
HISTORY_FILE = SKILL_DIR / "assets" / "history" / "history.json"
REPORT_DIR = SKILL_DIR / "assets" / "history"

GITHUB_API = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"

# Hard filter: repos must have more stars than this to be considered a candidate at all.
MIN_STARS = 1000

# Auto-expanding window ladder in calendar months (same as github-latest-hot-repo-explorer).
# The user-supplied --months (default 3) is the first step; these follow it.
WINDOW_STEPS_MONTHS = (3, 6, 12, 24, 36, 48, 60)
# GPT-4 release date: the earliest allowed window start.
EARLIEST_DATE = date(2023, 3, 14)


def subtract_months(d: date, months: int) -> date:
    y, m = d.year, d.month - months
    while m <= 0:
        m += 12
        y -= 1
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))

# Ensure direct connection to api.github.com to avoid local HTTP proxy handshake timeouts
if "no_proxy" not in os.environ:
    os.environ["no_proxy"] = "github.com,api.github.com"


# ---------- config / history I/O ----------

def load_org_config(path: Path) -> list[tuple[str, str]]:
    """Return [(company, org_login), ...] preserving the input order.

    Supports two shapes:
      { "Company": ["https://github.com/<org>", ...], ... }
      { "organizations": ["<org>", ...] }            # fallback
    Raises on missing file / bad JSON / empty / unknown shape.
    """
    if not path.exists():
        raise SystemExit(f"组织配置文件不存在：{path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"组织配置文件 JSON 解析失败：{e}")

    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()

    if isinstance(data, dict) and "organizations" in data and not any(
        isinstance(v, list) for v in data.values()
    ):
        # flat shape
        for org in data["organizations"]:
            login = normalize_org(org)
            if login and login not in seen:
                seen.add(login)
                pairs.append(("", login))
    elif isinstance(data, dict):
        for company, urls in data.items():
            if not isinstance(urls, list):
                raise SystemExit(
                    f"组织配置错误：公司 '{company}' 对应的值不是列表"
                )
            for url in urls:
                login = normalize_org(url)
                if login and login not in seen:
                    seen.add(login)
                    pairs.append((company, login))
    else:
        raise SystemExit("组织配置结构不支持：需要 JSON 对象")

    if not pairs:
        raise SystemExit("组织配置为空，请先提供组织名单")
    return pairs


def normalize_org(value: str) -> str | None:
    """Accept 'foo', 'github.com/foo', or a full https URL; return 'foo' or None."""
    if not isinstance(value, str):
        return None
    s = value.strip().rstrip("/")
    if not s:
        return None
    # Strip scheme
    s = re.sub(r"^https?://", "", s)
    # Strip host
    if s.startswith("github.com/"):
        s = s[len("github.com/"):]
    # First path segment is the org login
    login = s.split("/")[0]
    # GitHub login rules: 1-39 chars, alnum or single hyphens, no leading/trailing hyphen
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?", login):
        return None
    return login


def load_history(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"shown": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if "shown" not in data or not isinstance(data["shown"], list):
            return {"shown": []}
        return data
    except json.JSONDecodeError:
        return {"shown": []}


def save_history(path: Path, history: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(history, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ---------- GitHub API ----------

def _env_file_token() -> str:
    """从 ~/.openclaw/.env 读 GITHUB_TOKEN（OpenClaw exec 快照会过滤 token 类环境变量，故需文件回退）。"""
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


def get_token() -> str:
    return os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or _env_file_token()


def gh_headers() -> dict[str, str]:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "github-big-tech-latest-repo-explorer",
    }
    token = get_token()
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def require_github_token() -> None:
    if not get_token():
        raise SystemExit(
            "未检测到 GITHUB_TOKEN 或 GH_TOKEN。全量扫描必须配置 GitHub token，"
            "不会执行匿名请求。"
        )


def http_get_json(url: str, timeout: int = 20) -> Any:
    req = urllib.request.Request(url, headers=gh_headers())
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(f"HTTP {e.code} {e.reason} for {url}: {body[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"URL error for {url}: {e.reason}")


def list_org_recent_repos(
    org: str, since: str, per_page: int = 100
) -> list[dict[str, Any]]:
    """List public repos through Core API and filter created_at locally."""
    matched: list[dict[str, Any]] = []
    page = 1
    boundary = f"{since}T00:00:00Z"
    while True:
        params = {
            "type": "public",
            "sort": "created",
            "direction": "desc",
            "per_page": str(per_page),
            "page": str(page),
        }
        url = (
            f"{GITHUB_API}/orgs/{urllib.parse.quote(org)}/repos?"
            f"{urllib.parse.urlencode(params)}"
        )
        repos = http_get_json(url, timeout=30)
        if not isinstance(repos, list):
            raise RuntimeError(f"Core API 返回格式异常：{url}")
        if not repos:
            break
        for repo in repos:
            if (repo.get("created_at") or "") > boundary:
                matched.append(repo)
        oldest = repos[-1].get("created_at") or ""
        if oldest <= boundary or len(repos) < per_page:
            break
        page += 1
    return matched


def fetch_readme(full_name: str, default_branch: str) -> str | None:
    """Fetch README via the authenticated GitHub Core API.

    Uses GET /repos/{owner}/{repo}/readme which requires a token; falls back
    to None on any failure. We never call anonymous raw.githubusercontent.com
    because the host's anonymous rate limit is unrelated to the user's token.
    """
    if not full_name:
        return None
    url = f"{GITHUB_API}/repos/{full_name}/readme"
    headers = dict(gh_headers())
    headers["Accept"] = "application/vnd.github.raw"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        text = data.decode("utf-8", errors="replace")
        if len(text) > 50_000:
            text = text[:50_000] + "\n\n... (truncated)"
        return text
    except Exception:
        return None


# ---------- selection & summary ----------

def parse_readme_sections(readme: str) -> dict[str, str]:
    """Best-effort: extract the first 1-2 sentence description block and split
    'What is it / What problem / How' from a GitHub-latest-hot-repo-explorer
    style summary. This is a thin heuristic; the agent re-interprets anyway.
    """
    if not readme:
        return {}
    # Drop badges / image-only lines
    lines = [ln for ln in readme.splitlines() if ln.strip() and not ln.lstrip().startswith(("![", "[![", "<img"))]
    out: dict[str, str] = {}
    # First non-heading paragraph = description
    desc_parts: list[str] = []
    for ln in lines:
        if ln.lstrip().startswith("#"):
            if desc_parts:
                break
            continue
        desc_parts.append(ln.strip())
        if sum(len(p) for p in desc_parts) > 400:
            break
    if desc_parts:
        out["description"] = " ".join(desc_parts).strip()
    return out


def collect_candidates(
    org_pairs: list[tuple[str, str]],
    since: str,
    per_org: int = 100,
    max_workers: int = 8,
) -> tuple[list[dict[str, Any]], list[tuple[str, str, str]]]:
    """Query each org in parallel, return (candidates, failures).

    Candidates are filtered to stargazers_count > MIN_STARS in addition to
    the created_at >= since boundary already applied by list_org_recent_repos.
    """
    candidates: list[dict[str, Any]] = []
    failures: list[tuple[str, str, str]] = []
    seen_full: set[str] = set()

    def _query(company_org):
        company, org = company_org
        try:
            items = list_org_recent_repos(org, since, per_page=per_org)
            return company, org, items, None
        except Exception as e:
            return company, org, None, str(e)

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(_query, p) for p in org_pairs]
        for fut in as_completed(futures):
            company, org, items, err = fut.result()
            if err is not None:
                failures.append((company or org, org, err))
                continue
            assert items is not None
            for it in items:
                fn = it.get("full_name")
                if not fn or fn in seen_full:
                    continue
                if (it.get("stargazers_count") or 0) <= MIN_STARS:
                    continue
                seen_full.add(fn)
                it["_company"] = company
                candidates.append(it)

    candidates.sort(key=lambda x: x.get("created_at") or "", reverse=True)
    return candidates, failures


def pick_unseen(
    candidates: list[dict[str, Any]],
    history: dict[str, Any],
    count: int,
    strategy: str = "random",
) -> list[dict[str, Any]]:
    shown_keys = {item.get("full_name") for item in history.get("shown", [])}
    unseen = [c for c in candidates if c.get("full_name") not in shown_keys]
    if not unseen:
        return []
    if strategy == "stars":
        # Highest star count first; use creation time as deterministic tie-breaker.
        unseen.sort(
            key=lambda item: (
                item.get("stargazers_count", 0) or 0,
                item.get("created_at", "") or "",
            ),
            reverse=True,
        )
        return unseen[:count]
    if strategy == "oldest":
        # candidates is sorted by created_at desc; pick the earliest ones
        return list(reversed(unseen))[:count]
    random.shuffle(unseen)
    return unseen[:count]


def report_path(full_name: str) -> Path:
    """Return assets/history/YYYY-MM-DD-<owner>-<repo>.md (local date)."""
    safe = re.sub(r'[\\/:*?"<>|\s]+', "-", full_name).strip("-")
    return REPORT_DIR / f"{date.today().isoformat()}-{safe}.md"


def format_repo_block(r: dict[str, Any]) -> str:
    name = r.get("full_name", "")
    company = r.get("_company") or ""
    url = r.get("html_url", "")
    stars = r.get("stargazers_count", 0)
    lang = r.get("language") or "—"
    desc = (r.get("description") or "").strip()
    created_iso = r.get("created_at", "") or ""
    created_date = created_iso[:10] if created_iso else "—"
    return (
        f"- **名称**：{name}\n"
        f"- **Stars**:{stars}\n"
        f"- **主语言**：{lang}\n"
        f"- **创建时间**：{created_date}\n"
        f"- **链接**：{url}\n"
        f"- **简介**：{desc or '（无）'}\n"
        f"- **所属组织**：{company or '（未标注）'}"
    )


def render_output(
    selected: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    history: dict[str, Any],
    failures: list[tuple[str, str, str]],
    since: str,
    months: int,
    capped: bool = False,
) -> str:
    shown_keys = {item.get("full_name") for item in history.get("shown", [])}
    candidate_total = len(candidates)
    shown_in_window = sum(1 for c in candidates if c.get("full_name") in shown_keys)
    unseen_in_window = candidate_total - shown_in_window

    window_label = (
        f"回溯至截止日期 {EARLIEST_DATE.isoformat()}" if capped else f"最近 {months} 个月"
    )

    parts: list[str] = []
    parts.append("# 大厂最新仓库探索\n")
    parts.append(
        f"> **筛选条件：{window_label}创建（created > {since}），stars > {MIN_STARS}，"
        f"候选 {candidate_total} / 已输出 {shown_in_window} / 未输出 {unseen_in_window}**"
    )

    if failures:
        parts.append("\n## 查询失败的组织")
        for company, org, err in failures:
            parts.append(f"- {company} → `{org}`: {err}")

    if not selected:
        parts.append("\n## 结果")
        if candidate_total == 0:
            parts.append(f"- {window_label}内没有 stars > {MIN_STARS} 的仓库。")
        else:
            parts.append(
                f"- 所有 {candidate_total} 个满足 stars > {MIN_STARS} 的候选均已输出过。请重置历史 (`--reset-history`) "
                f"或扩大时间范围 (`--months`)。"
            )
        return "\n".join(parts) + "\n"

    for r in selected:
        full_name = r.get("full_name", "")
        stars = r.get("stargazers_count", 0) or 0
        title_window = f"回溯至 {EARLIEST_DATE.isoformat()}" if capped else f"最近 {months} 月"
        title = f"### {title_window}国内外大厂热门仓库：{full_name}"
        parts.append(f"\n{title}")
        parts.append(
            f"> **筛选条件：{title_window}创建，stars > {MIN_STARS}，且在未输出候选中 stars 最多**"
        )
        parts.append(format_repo_block(r))

        parts.append("\n### 统计")
        parts.append(f"- **候选总数**：{candidate_total}")
        parts.append(f"- **已输出**：{shown_in_window}")
        parts.append(f"- **未输出**：{unseen_in_window}")
        parts.append(
            f"\n> 回答完三个问题后，须将完整回答（不含 README 原文）保存为：`{report_path(full_name)}`"
        )

        readme = fetch_readme(full_name, r.get("default_branch") or "main")
        if not readme:
            parts.append(
                "\n> 信息有限，基于元数据推断（README 不可用或未披露）。"
            )
        else:
            parts.append(
                "\n=== README (前 50000 字符) ===\n"
                + readme
                + "\n=== README END ==="
            )

        parts.append("\n### 这个仓库的项目是什么？")
        parts.append(
            "用 1–3 句话讲清楚项目定位、产品/工具类别和目标用户。"
        )
        parts.append("\n### 解决了什么问题？")
        parts.append(
            "说明具体痛点场景：用户原来怎么做，以及为什么麻烦、慢、贵或复杂。"
            "不要泛泛说“提升效率”。"
        )
        parts.append("\n### 如何解决？")
        parts.append(
            "列出最多 5 条核心实现思路：技术方案、关键设计或差异化。"
            "可从 README 的 Features/Architecture 段抽取；README 未披露时明确写“README 未披露”。"
        )

    return "\n".join(parts) + "\n"


# ---------- main ----------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--months", type=int, default=3, help="时间范围（自然月），默认 3")
    ap.add_argument("--count", type=int, default=1, help="选择几个未输出的仓库，默认 1")
    ap.add_argument(
        "--org-config",
        type=Path,
        default=DEFAULT_ORG_CONFIG,
        help=f"组织配置 JSON 路径，默认 {DEFAULT_ORG_CONFIG}",
    )
    ap.add_argument(
        "--reset-history",
        action="store_true",
        help="清空历史记录（assets/history/history.json）后退出",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="只统计候选数量与失败组织，不选择 / 不写历史",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=8,
        help="并发搜索的线程数，默认 8",
    )
    ap.add_argument(
        "--pick",
        choices=("stars", "oldest", "random"),
        default="stars",
        help="从满足 stars>1000 且未输出的候选中选择仓库：stars=Stars 最多（默认）；oldest=最早发布；random=随机",
    )
    args = ap.parse_args(argv)

    require_github_token()

    if args.months < 1:
        raise SystemExit("--months 必须 >= 1")
    if args.count < 1:
        raise SystemExit("--count 必须 >= 1")

    org_pairs = load_org_config(args.org_config)
    history = load_history(HISTORY_FILE)

    if args.reset_history:
        history = {"shown": []}
        save_history(HISTORY_FILE, history)
        print(f"已重置历史：{HISTORY_FILE}")
        return 0

    now = datetime.now(timezone.utc)
    # Build the auto-expanding window ladder (calendar months):
    #   user-supplied --months (default 3) → 6 → 12 → 24 → 36 → 48 → 60
    # A window whose start date reaches EARLIEST_DATE (GPT-4 release day,
    # 2023-03-14) is clamped to that date and becomes the final window.
    # Duplicate / non-increasing steps are dropped.
    ladder: list[tuple[int, str, bool]] = []  # (months, since_iso, capped)
    prev_months = 0
    for m in (args.months, *WINDOW_STEPS_MONTHS):
        if m <= prev_months:
            continue
        prev_months = m
        start = subtract_months(now.date(), m)
        if start <= EARLIEST_DATE:
            ladder.append((m, EARLIEST_DATE.isoformat(), True))
            break
        ladder.append((m, start.isoformat(), False))

    windows: list[dict[str, Any]] = []
    selected: list[dict[str, Any]] = []
    last_candidates: list[dict[str, Any]] = []
    last_failures: list[tuple[str, str, str]] = []
    used_months, used_since, used_capped = ladder[-1]

    for months, since, capped in ladder:
        candidates, failures = collect_candidates(
            org_pairs, since, max_workers=max(1, args.workers)
        )
        # candidates already filtered to stargazers_count > MIN_STARS inside collect_candidates
        unseen = [
            c for c in candidates
            if c.get("full_name") not in {x.get("full_name") for x in history.get("shown", [])}
        ]
        windows.append(
            {
                "months": months,
                "since": since,
                "capped": capped,
                "min_stars": MIN_STARS,
                "candidate_total": len(candidates),
                "shown_in_window": len(candidates) - len(unseen),
                "unseen_in_window": len(unseen),
                "failures": failures,
            }
        )
        last_candidates = candidates
        last_failures = failures
        if unseen:
            used_months, used_since, used_capped = months, since, capped
            selected = pick_unseen(
                candidates, history, args.count, strategy=args.pick
            )
            break

    if args.dry_run:
        out = {
            "pick": args.pick,
            "min_stars": MIN_STARS,
            "initial_months": args.months,
            "ladder": [{"months": m, "since": s, "capped": c} for m, s, c in ladder],
            "windows": windows,
            "used_months": used_months,
            "used_since": used_since,
            "used_capped": used_capped,
            "selected": [
                {
                    "full_name": r.get("full_name"),
                    "company": r.get("_company") or None,
                    "created_at": r.get("created_at"),
                    "stars": r.get("stargazers_count"),
                    "html_url": r.get("html_url"),
                }
                for r in selected
            ],
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    out = render_output(
        selected, last_candidates, history, last_failures, used_since, used_months, used_capped
    )
    print(out)

    if selected:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        now_iso = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        history.setdefault("shown", [])
        for r in selected:
            history["shown"].append(
                {
                    "full_name": r.get("full_name"),
                    "shown_at": now_iso,
                    "stars": r.get("stargazers_count", 0),
                    "html_url": r.get("html_url"),
                    "company": r.get("_company") or None,
                }
            )
        save_history(HISTORY_FILE, history)

    return 0


if __name__ == "__main__":
    sys.exit(main())
