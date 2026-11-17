#!/usr/bin/env python3
"""抓取 GitHub Trending（周榜 / 月榜），并为榜单中的每个仓库抓取元数据与 README。

GitHub 没有 Trending 官方 API。榜单优先取第三方接口 gitstock.org（JSON），失败时回退为解析 https://github.com/trending 页面 HTML（仅标准库）。
仓库详情通过 GitHub Core API 获取（可选 GITHUB_TOKEN / GH_TOKEN），README 失败时回退 raw.githubusercontent.com。

输出：
- stdout：榜单 Markdown（含总览表），以及详情素材文件路径、最终报告应保存的路径。
- 详情素材（元数据 + README 摘录）写入系统临时目录，供逐个仓库撰写详细介绍。
- 输出分两部分，由调用方撰写后保存：
  1. 每个仓库一个详情文件：assets/{weekly|monthly}/{YYYY-Wnn|YYYY-Mnn}/Rank-NN_owner_repo.md
  2. 一个总览文件（含各仓库简介与详情跳转链接），与详情同目录：assets/{weekly|monthly}/{YYYY-Wnn|YYYY-Mnn}/Overview.md
"""
import argparse
import html
import http.client
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from typing import Optional

BASE_URL = "https://github.com/trending"
API_URL = "https://gitstock.org/api/v1/github/trending"  # 第三方 JSON 接口，优先使用
GITHUB_API = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
SINCE_LABEL = {"weekly": "周榜", "monthly": "月榜"}
SINCE_GAIN = {"weekly": "本周新增", "monthly": "本月新增"}
ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = ROOT / "assets"
MATERIAL_DIR = Path(tempfile.gettempdir()) / "github-trending-explorer"
USER_AGENT = "Mozilla/5.0 (compatible; github-trending-explorer/2.0)"

ARTICLE_RE = re.compile(r"<article class=\"Box-row\">(.*?)</article>", re.S)
NAME_RE = re.compile(r"<h2[^>]*>.*?href=\"/([^\"/]+/[^\"/]+)\"", re.S)
DESC_RE = re.compile(r"<p class=\"col-9[^>]*>(.*?)</p>", re.S)
LANG_RE = re.compile(r"itemprop=\"programmingLanguage\">(.*?)</span>", re.S)
STARS_RE = re.compile(r"href=\"/[^\"]+/stargazers\"[^>]*>.*?</svg>\s*([\d,]+)\s*</a>", re.S)
FORKS_RE = re.compile(r"href=\"/[^\"]+/forks\"[^>]*>.*?</svg>\s*([\d,]+)\s*</a>", re.S)
GAIN_RE = re.compile(r"([\d,]+)\s+stars\s+(?:today|this week|this month)")


def build_url(since: str) -> str:
    return f"{BASE_URL}?since={since}"


def period_stem(since: str, today: str) -> str:
    """周期名：周榜为 YYYY-Wnn（ISO 周数），月榜为 YYYY-Mnn。"""
    d = date.fromisoformat(today)
    if since == "weekly":
        iso = d.isocalendar()
        return f"{iso[0]}-W{iso[1]:02d}"
    return f"{d.year}-M{d.month:02d}"


def overview_path(since: str, today: str) -> Path:
    """总览文件路径：assets/{since}/{周期}/Overview.md，与各仓库详情同目录。"""
    return detail_dir(since, today) / "Overview.md"


def detail_dir(since: str, today: str) -> Path:
    """周期目录：assets/{since}/{周期}/，存放总览与各仓库详情。"""
    return ASSETS_DIR / since / period_stem(since, today)


def detail_name(full_name: str, rank: int) -> str:
    """仓库详情文件名：Rank-NN_owner_repo.md（各信息用下划线分隔，NN 为本期榜单排名，两位补零）。"""
    return f"Rank-{rank:02d}_{full_name.replace('/', '_')}.md"


def clean_period_dir(out_dir: Path) -> int:
    """清理周期目录中上一次运行留下的 Rank-NN_*.md 与 Overview.md，避免榜单变化后残留旧文件；返回删除数量。

    仅在榜单与详情均抓取成功后调用；只删除上述命名的文件，且目录必须位于 assets 之下。
    """
    if not out_dir.is_dir() or ASSETS_DIR.resolve() not in out_dir.resolve().parents:
        return 0
    old = list(out_dir.glob("Rank-[0-9][0-9]_*.md")) + [p for p in [out_dir / "Overview.md"] if p.is_file()]
    for p in old:
        p.unlink()
    return len(old)


def fetch_html(url: str, retries: int = 3, fatal: bool = True) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    last = ""
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if fatal:
                sys.exit(f"请求失败：HTTP {e.code}（{url}）")
            print(f"请求失败：HTTP {e.code}（{url}）", file=sys.stderr)
            return ""
        except (urllib.error.URLError, OSError, http.client.HTTPException) as e:  # 含超时与 IncompleteRead
            last = str(getattr(e, "reason", e))
            print(f"第 {attempt}/{retries} 次请求失败：{last}", file=sys.stderr)
    if fatal:
        sys.exit(f"网络错误：{last}（{url}）")
    return ""


def to_int(text: Optional[str]) -> int:
    return int(text.replace(",", "")) if text else 0


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", text))).strip()


def parse(page: str) -> list:
    repos = []
    for block in ARTICLE_RE.findall(page):
        name = NAME_RE.search(block)
        if not name:
            continue
        full_name = name.group(1)
        desc, lang = DESC_RE.search(block), LANG_RE.search(block)
        stars, forks, gain = STARS_RE.search(block), FORKS_RE.search(block), GAIN_RE.search(block)
        repos.append({
            "rank": len(repos) + 1,
            "full_name": full_name,
            "url": f"https://github.com/{full_name}",
            "description": clean(desc.group(1)) if desc else "",
            "language": clean(lang.group(1)) if lang else "",
            "stars": to_int(stars.group(1) if stars else None),
            "forks": to_int(forks.group(1) if forks else None),
            "gain": to_int(gain.group(1) if gain else None),
        })
    return repos


def fetch_api_list(since: str) -> list:
    """从第三方接口获取榜单；失败或数据异常时返回空列表，由调用方回退到解析 HTML。"""
    url = f"{API_URL}?period={since}"
    text = fetch_html(url, retries=2, fatal=False)
    try:
        items = json.loads(text)["items"] if text else []
    except (ValueError, KeyError, TypeError):
        items = []
    repos = []
    for it in items:
        try:
            full_name = f"{it['owner']}/{it['repo']}"
            repos.append({
                "rank": len(repos) + 1,
                "full_name": full_name,
                "url": it.get("github_url") or f"https://github.com/{full_name}",
                "description": clean(it.get("description") or ""),
                "language": it.get("language") or "",
                "stars": int(it.get("stars") or 0),
                "forks": int(it.get("forks") or 0),
                "gain": int(it.get("stars_gained") or 0),
            })
        except (KeyError, TypeError, ValueError):
            continue
    return repos


# ---------- 仓库详情（元数据 + README） ----------

def api_get(url: str, accept: str) -> str:
    headers = {"Accept": accept, "X-GitHub-Api-Version": "2022-11-28", "User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token and url.startswith(GITHUB_API):
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")


def clean_readme(text: str, limit: int) -> str:
    """去掉注释、徽章与纯图片行，压缩空行，并截断到 limit 字符。"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    lines = [ln for ln in text.splitlines() if not ln.lstrip().startswith(("![", "[![", "<img"))]
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()
    return text[:limit] + "\n... (truncated)" if len(text) > limit else text


def fetch_detail(full_name: str, readme_chars: int) -> dict:
    detail = {"created_at": "", "pushed_at": "", "topics": [], "license": "", "readme": "", "errors": []}
    try:
        meta = json.loads(api_get(f"{GITHUB_API}/repos/{full_name}", "application/vnd.github+json"))
        detail["created_at"] = (meta.get("created_at") or "")[:10]
        detail["pushed_at"] = (meta.get("pushed_at") or "")[:10]
        detail["topics"] = meta.get("topics") or []
        detail["license"] = (meta.get("license") or {}).get("spdx_id") or ""
    except Exception as e:
        detail["errors"].append(f"元数据获取失败：{e}")
    readme = ""
    try:
        readme = api_get(f"{GITHUB_API}/repos/{full_name}/readme", "application/vnd.github.raw")
    except Exception as e:
        detail["errors"].append(f"README（API）获取失败：{e}")
        try:
            readme = api_get(f"{RAW_BASE}/{full_name}/HEAD/README.md", "text/plain")
        except Exception as e2:
            detail["errors"].append(f"README（raw）获取失败：{e2}")
    detail["readme"] = clean_readme(readme, readme_chars) if readme else ""
    return detail


def fetch_details(repos: list, readme_chars: int, workers: int) -> None:
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for repo, detail in zip(repos, ex.map(lambda r: fetch_detail(r["full_name"], readme_chars), repos)):
            repo.update(detail)


def render_material(repos: list, since: str, today: str, readme_chars: int) -> str:
    out_dir = detail_dir(since, today)
    lines = [f"# GitHub Trending {SINCE_LABEL[since]} 详情素材（{today}）", ""]
    for r in repos:
        lines += [
            f"## [{r['rank']}] {r['full_name']}",
            "",
            f"- 链接：{r['url']}",
            f"- 总 Stars：{r['stars']:,}",
            f"- {SINCE_GAIN[since]} Stars：+{r['gain']:,}",
            f"- Forks：{r['forks']:,}",
            f"- 主语言：{r['language'] or '-'}",
            f"- 创建时间：{r['created_at'] or '-'}",
            f"- 最近推送：{r['pushed_at'] or '-'}",
            f"- 许可证：{r['license'] or '-'}",
            f"- Topics：{', '.join(r['topics']) or '-'}",
            f"- 简介：{r['description'] or '-'}",
            f"- 详情保存路径：`{out_dir / detail_name(r['full_name'], r['rank'])}`",
        ]
        lines += [f"- 抓取异常：{err}" for err in r["errors"]]
        if r["readme"]:
            lines += ["", f"=== README (前 {readme_chars} 字符) ===", r["readme"], "=== README END ==="]
        else:
            lines += ["", "> README 不可用：信息有限，基于元数据推断。"]
        lines.append("")
    return "\n".join(lines)


# ---------- 榜单渲染 ----------

def render(repos: list, since: str, today: str, source: str) -> str:
    lines = [
        f"# GitHub Trending {SINCE_LABEL[since]}",
        "",
        f"> 数据日期：{today}，来源：<{source}>，共 {len(repos)} 个仓库",
        "",
        "## 一、榜单总览",
        "",
        f"| 排名 | 仓库 | 总 Stars | {SINCE_GAIN[since]} | Forks | 简介 | 详情 |",
        "| ---- | ---- | -------- | -------- | ----- | ---- | ---- |",
    ]
    for r in repos:
        desc = r["description"].replace("|", "\\|") or "-"
        lines.append(
            f"| {r['rank']} | [{r['full_name']}]({r['url']}) "
            f"| {r['stars']:,} | +{r['gain']:,} | {r['forks']:,} | {desc} "
            f"| [查看详情]({detail_name(r['full_name'], r['rank'])}) |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="抓取 GitHub Trending 周榜 / 月榜及仓库详情")
    ap.add_argument("--since", choices=list(SINCE_LABEL), default="weekly", help="周期，默认 weekly")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个，默认全部")
    ap.add_argument("--readme-chars", type=int, default=6000, help="每个仓库保留的 README 字符数，默认 6000")
    ap.add_argument("--workers", type=int, default=6, help="并发抓取详情的线程数，默认 6")
    ap.add_argument("--brief", action="store_true", help="只输出榜单总览，不抓取仓库详情")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而不是 Markdown")
    ap.add_argument("--html", help="从本地 HTML 文件解析榜单（离线调试），不请求接口与 Trending 页面")
    args = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    repos, source = [], build_url(args.since)
    if args.html:
        repos = parse(Path(args.html).read_text(encoding="utf-8"))
    else:
        repos = fetch_api_list(args.since)
        if repos:
            source = f"{API_URL}?period={args.since}"
        else:
            print("第三方接口不可用，回退到解析 github.com/trending 页面。", file=sys.stderr)
            repos = parse(fetch_html(source))
    if args.limit > 0:
        repos = repos[: args.limit]
    if not repos:
        sys.exit("未解析到任何仓库：接口与页面均无数据，GitHub 页面结构可能已变化，请检查 scripts/fetch_trending.py 的正则。")

    today = date.today().isoformat()
    if not args.brief:
        fetch_details(repos, args.readme_chars, args.workers)

    if args.json:
        print(json.dumps(repos, ensure_ascii=False, indent=2))
        return
    print(render(repos, args.since, today, source))
    if args.brief:
        return

    removed = clean_period_dir(detail_dir(args.since, today))

    MATERIAL_DIR.mkdir(parents=True, exist_ok=True)
    material = MATERIAL_DIR / f"{today}-{args.since}.md"
    material.write_text(render_material(repos, args.since, today, args.readme_chars), encoding="utf-8")

    failed = [r["full_name"] for r in repos if r["errors"]]
    if failed:
        print(f"> 详情抓取存在异常的仓库（{len(failed)} 个）：{', '.join(failed)}\n")
    if removed:
        print(f"> 已清理周期目录中上一次运行的旧结果（{removed} 个文件），请重新写入全部详情与总览。\n")
    print(f"> 详情素材（元数据 + README 摘录）：`{material}`")
    print(f"> 须按 `references/repo-output_template.md`（详情）与 `references/overview-output_template.md`（总览）保存两部分输出：")
    print(f"> （1）周期目录（各仓库详情与总览均保存在此）：`{detail_dir(args.since, today)}`（各详情文件路径见详情素材）")
    print(f"> （2）总览文件：`{overview_path(args.since, today)}`")


if __name__ == "__main__":
    main()
