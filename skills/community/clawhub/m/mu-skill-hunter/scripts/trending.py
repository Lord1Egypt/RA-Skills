#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mu-skill-hunter: Skill 猎手周报数据采集脚本
职责：数据采集 + 评分排序 + 输出结构化 JSON
翻译和排版由 AI 消费者负责，脚本不做语言处理
"""
import sys
import os
import json
import math
import urllib.request
import urllib.parse
import subprocess
import argparse
import shutil
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# 自动将 nvm bin 路径加入 PATH（使 npx/clawhub/skills 可用）
_nvm_bin = os.path.expanduser("~/.nvm/versions/node")
if os.path.isdir(_nvm_bin):
    for d in sorted(os.listdir(_nvm_bin), reverse=True):
        _bin = os.path.join(_nvm_bin, d, "bin")
        if os.path.isfile(os.path.join(_bin, "npx")):
            os.environ["PATH"] = _bin + ":" + os.environ.get("PATH", "")
            break


# 默认配置（profile 不存在时兼容Skill市场下载用户）
DEFAULT_GITHUB_QUERIES = [
    ("topic:agent-skill", 10),
    ("topic:mcp-server stars:>=10", 10),
    ('"agent skill" stars:>=5', 8),
    ("agent framework skill stars:>=1", 5),
]
DEFAULT_GITHUB_NEW_QUERIES = [
    ("topic:agent-skill", "created"),
    ("topic:mcp-server stars:>=5", "created"),
]
DEFAULT_CLAWHUB_QUERIES = ["agent skill", "mcp", "automation"]
DEFAULT_SKILLHUB_QUERIES = ["agent", "mcp", "automation", "skill", "calendar", "pdf", "excel"]
DEFAULT_SKILLSSH_QUERIES = ["agent skill", "mcp", "automation"]
DEFAULT_RELEVANCE_KEYWORDS = ["agent-skill", "agent skill", "mcp", "agent-framework", "skill", "automation"]
DEFAULT_EXCLUDED_KEYWORDS = ["game", "gaming", "play", "fun"]


def load_profile():
    """Load user-scene-profile.json if exists, else return None (use defaults)"""
    profile_path = os.path.join(os.path.dirname(__file__), "..", "references", "user-scene-profile.json")
    profile_path = os.path.normpath(profile_path)
    if not os.path.exists(profile_path):
        return None
    try:
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def build_queries_from_profile(profile):
    """从 profile 按 weight 合并生成 GitHub/ClawHub queries 和相关性关键词"""
    if not profile:
        return DEFAULT_GITHUB_QUERIES, DEFAULT_GITHUB_NEW_QUERIES, DEFAULT_CLAWHUB_QUERIES, DEFAULT_RELEVANCE_KEYWORDS, DEFAULT_EXCLUDED_KEYWORDS

    scenes = [s for s in profile.get("scenes", []) if s.get("enabled", True)]
    scenes.sort(key=lambda s: s.get("weight", 0), reverse=True)

    gh_queries = []
    gh_new_queries = []
    ch_queries = []
    rel_keywords = []
    seen_gh = set()
    seen_ch = set()

    for scene in scenes:
        w = scene.get("weight", 0)
        if w == 0:
            continue
        for q_item in scene.get("github_queries", []):
            if isinstance(q_item, (list, tuple)) and len(q_item) == 2:
                q, limit = q_item
                scaled_limit = max(3, int(limit * w))
                if q not in seen_gh:
                    seen_gh.add(q)
                    gh_queries.append((q, scaled_limit))
                    if w >= 0.8:
                        gh_new_queries.append((q, "created"))
        for q in scene.get("clawhub_queries", []):
            if q not in seen_ch:
                seen_ch.add(q)
                ch_queries.append(q)
        for kw in scene.get("relevance_keywords", []):
            if kw not in rel_keywords:
                rel_keywords.append(kw)

    excluded = profile.get("excluded_keywords", DEFAULT_EXCLUDED_KEYWORDS)

    if not gh_queries:
        gh_queries = DEFAULT_GITHUB_QUERIES
    if not gh_new_queries:
        gh_new_queries = DEFAULT_GITHUB_NEW_QUERIES
    if not ch_queries:
        ch_queries = DEFAULT_CLAWHUB_QUERIES
    if not rel_keywords:
        rel_keywords = DEFAULT_RELEVANCE_KEYWORDS

    return gh_queries, gh_new_queries, ch_queries, rel_keywords, excluded


# 加载用户偏好
PROFILE = load_profile()
GITHUB_QUERIES, GITHUB_NEW_QUERIES, CLAWHUB_QUERIES, RELEVANCE_KEYWORDS, EXCLUDED_KEYWORDS = build_queries_from_profile(PROFILE)


def fetch_github_agent_skills(period="weekly", limit=10):
    """获取 GitHub Agent Skill 相关项目
    策略：优先搜「本周新建」项目，再补充「本周 stars 最多」的成熟项目
    """
    days_map = {"daily": 1, "weekly": 7, "monthly": 30}
    days = days_map.get(period, 7)
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

    new_results = []
    hot_results = []
    seen = set()
    headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "mu-skill-hunter"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    def fetch_one(q, sort, per_page):
        params = urllib.parse.urlencode({"q": q, "sort": sort, "order": "desc", "per_page": per_page})
        url = f"https://api.github.com/search/repositories?{params}"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read()).get("items", [])
        except Exception:
            return []

    # GitHub 查询上限：去重后最多10条 new + 10条 hot
    gh_new_queries = list(dict.fromkeys([q for q, _ in GITHUB_NEW_QUERIES]))[:10]
    gh_hot_queries = list(dict.fromkeys([q for q, _ in GITHUB_QUERIES]))[:10]

    def to_item(item):
        desc = item.get("description") or ""
        return {
            "source": "GitHub",
            "name": item["full_name"],
            "display": item["name"],
            "desc": desc,
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language") or "",
            "url": item.get("html_url", ""),
            "created": item.get("created_at", "")[:10],
            "is_new": item.get("created_at", "")[:10] >= since,
        }

    # 1. 本周新建的 Agent Skill 项目
    for q_template in gh_new_queries:
        sort = "created"
        q = f"{q_template} created:>={since}"
        for item in fetch_one(q, "stars", 10):
            if item["full_name"] not in seen:
                seen.add(item["full_name"])
                new_results.append(to_item(item))

    # 2. 补充本周 stars 增长快的
    for q_template in gh_hot_queries:
        q = f"{q_template} pushed:>={since} stars:>=50"
        per_page = 10
        for item in fetch_one(q, "updated", per_page):
            if item["full_name"] not in seen:
                seen.add(item["full_name"])
                hot_results.append(to_item(item))

    new_results.sort(key=lambda x: x["stars"], reverse=True)
    hot_results.sort(key=lambda x: x["stars"], reverse=True)
    combined = new_results + [r for r in hot_results if r["name"] not in {x["name"] for x in new_results}]
    return combined[:limit]


def _run_single_clawhub(q):
    """单次 ClawHub 查询，供并行调度"""
    try:
        result = subprocess.run(
            ["npx", "--yes", "clawhub", "search", q],
            capture_output=True, text=True, timeout=10
        )
        return (q, result.returncode, result.stdout)
    except subprocess.TimeoutExpired:
        return (q, -1, "")
    except Exception:
        return (q, -1, "")


def fetch_clawhub_skills(limit=6):
    """获取 ClawHub Agent Skill（并行 + 单步10s超时 + 查询上限8条）"""
    # 查询数上限：去重后最多8条，避免 npx 累积耗时
    queries = list(dict.fromkeys(CLAWHUB_QUERIES))[:8]

    # 并行启动所有 npx 进程
    procs = []
    for q in queries:
        try:
            p = subprocess.Popen(
                ["npx", "--yes", "clawhub", "search", q],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            procs.append((q, p))
        except Exception:
            continue

    # 收集结果，单进程超时10s
    seen = set()
    results = []
    for q, p in procs:
        try:
            stdout, _ = p.communicate(timeout=10)
            if p.returncode == 0:
                for line in stdout.strip().split("\n"):
                    line = line.strip()
                    if not line or line.startswith("Install") or line.startswith("Found"):
                        continue
                    parts = [p2.strip() for p2 in line.split("  ") if p2.strip()]
                    slug = parts[0] if parts else ""
                    name = parts[2] if len(parts) >= 3 else slug
                    if slug and slug not in seen:
                        seen.add(slug)
                        results.append({
                            "source": "ClawHub",
                            "name": slug,
                            "display": name,
                            "desc": "",
                            "stars": 0,
                            "language": "",
                            "url": f"https://clawhub.ai/skills/{slug}",
                            "created": "",
                            "is_new": False,
                        })
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            continue
        except Exception:
            continue

    return results[:limit]


def fetch_skillhub_skills(limit=6):
    """获取 SkillHub 热门 Skill（公开 HTTP API，无需鉴权）
    API: GET https://api.skillhub.cn/api/skills?keyword=<query>&sortBy=score&pageSize=<N>
    """
    queries = list(dict.fromkeys(DEFAULT_SKILLHUB_QUERIES))[:5]
    seen = set()
    results = []
    for q in queries:
        try:
            params = urllib.parse.urlencode({"keyword": q, "sortBy": "score", "pageSize": "5"})
            url = f"https://api.skillhub.cn/api/skills?{params}"
            req = urllib.request.Request(url, headers={"User-Agent": "mu-skill-hunter"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read())
                items = data.get("data", {}).get("skills", [])
                for item in items:
                    slug = item.get("slug", "")
                    if slug in seen:
                        continue
                    seen.add(slug)
                    downloads = item.get("downloads", 0)
                    installs = item.get("installs", 0)
                    desc = item.get("description_zh", "") or item.get("description", "")
                    desc_parts = desc.split("\n") if desc else []
                    short_desc = desc_parts[0][:80] if desc_parts else ""
                    results.append({
                        "source": "SkillHub",
                        "name": slug,
                        "display": item.get("name", slug),
                        "desc": short_desc,
                        "stars": max(downloads, installs),
                        "language": item.get("category", ""),
                        "url": f"https://skillhub.cn/skills/{slug}",
                        "created": "",
                        "is_new": False,
                    })
                    if len(results) >= limit:
                        break
        except Exception:
            continue
        if len(results) >= limit:
            break
    return results[:limit]


def fetch_skillssh_skills(limit=6):
    """获取 Skills.sh 热门 Skill（通过 npx skills find CLI，无需鉴权）
    Skills.sh HTTP API 需内部鉴权（401），但 CLI 完全公开可用。
    并行查询多个关键词，解析 ANSI 输出提取 slug + installs。
    """
    queries = list(dict.fromkeys(DEFAULT_SKILLSSH_QUERIES))[:5]
    seen = set()
    results = []

    # 并行启动所有 npx skills find 进程
    procs = []
    for q in queries:
        try:
            p = subprocess.Popen(
                ["npx", "--yes", "skills", "find", q],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, stdin=subprocess.PIPE
            )
            procs.append((q, p))
        except Exception:
            continue

    import re
    ansi_re = re.compile(r'\x1b\[[0-9;]*m')

    for q, p in procs:
        try:
            # 向 stdin 发送 'n' 以跳过交互提示，然后关闭
            stdout, _ = p.communicate(input="n\n", timeout=15)
            clean = ansi_re.sub('', stdout)
            # 解析格式："owner/repo@skill  NNK installs"
            # 或 "skill_name  NNK installs" + URL 行
            lines = clean.strip().split('\n')
            current_slug = None
            current_url = None
            current_installs = 0
            for line in lines:
                line = line.strip()
                if not line or line.startswith('Install') or '██' in line:
                    continue
                # 匹配 "owner/repo@skill  123.4K installs" 格式
                m = re.match(r'([\w._-]+/[\w._-]+)@([\w._-]+)\s+([\d.]+[KMB]?)\s*installs?', line)
                if m:
                    owner_repo = m.group(1)
                    skill = m.group(2)
                    installs_str = m.group(3)
                    current_slug = f"{owner_repo}@{skill}"
                    current_installs = _parse_installs(installs_str)
                    current_url = None
                    continue
                # 匹配 URL 行 "└ https://skills.sh/..."
                m_url = re.search(r'https://skills\.sh/([\w._/-]+)', line)
                if m_url and current_slug:
                    current_url = f"https://skills.sh/{m_url.group(1)}"
                    if current_slug not in seen:
                        seen.add(current_slug)
                        display = current_slug.split('@')[-1] if '@' in current_slug else current_slug
                        results.append({
                            "source": "Skills.sh",
                            "name": current_slug,
                            "display": display,
                            "desc": "",
                            "stars": current_installs,
                            "language": "",
                            "url": current_url,
                            "created": "",
                            "is_new": False,
                        })
                    current_slug = None
                    if len(results) >= limit:
                        break
        except subprocess.TimeoutExpired:
            p.kill()
            p.wait()
            continue
        except Exception:
            continue
        if len(results) >= limit:
            break

    # 清理剩余进程
    for q, p in procs:
        if p.poll() is None:
            p.kill()
            p.wait()

    return results[:limit]


def _parse_installs(s):
    """解析 Skills.sh CLI 输出的安装量（如 '95.4K' → 95400）"""
    s = s.strip().upper()
    try:
        if s.endswith('K'):
            return int(float(s[:-1]) * 1000)
        elif s.endswith('M'):
            return int(float(s[:-1]) * 1000000)
        elif s.endswith('B'):
            return int(float(s[:-1]) * 1000000000)
        else:
            return int(float(s))
    except ValueError:
        return 0


def compute_score(item, max_stars, week_since):
    """统一评分：热度50% + 相关性30% + 新鲜度20%"""
    if max_stars > 0 and item["stars"] > 0:
        heat = (math.log(item["stars"] + 1) / math.log(max_stars + 1)) * 50
    else:
        heat = 0

    text = (item.get("display", "") + " " + item.get("desc", "") + " " + item.get("name", "")).lower()
    hits = sum(1 for kw in RELEVANCE_KEYWORDS if kw in text)
    relevance = min(hits * 10, 30)

    if any(kw in text for kw in EXCLUDED_KEYWORDS):
        return 0

    created = item.get("created", "")
    month_since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    if created >= week_since:
        freshness = 20
    elif created >= month_since:
        freshness = 10
    else:
        freshness = 2

    if item["source"] == "ClawHub" and heat == 0:
        heat = 15
    if item["source"] in ("SkillHub", "Skills.sh") and heat == 0:
        heat = 10

    return round(heat + relevance + freshness, 1)


def dedup_items(items):
    """去重：ClawHub/SkillHub/Skills.sh按slug去重，GitHub按owner去重（同作者≤2个）"""
    seen_slugs = set()
    owner_count = {}
    result = []
    for item in items:
        if item["source"] in ("ClawHub", "SkillHub", "Skills.sh"):
            slug = item["name"]
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
        else:
            owner = item["name"].split("/")[0] if "/" in item["name"] else ""
            if owner:
                owner_count[owner] = owner_count.get(owner, 0) + 1
                if owner_count[owner] > 2:
                    continue
        result.append(item)
    return result


def generate_data(period="weekly"):
    """采集数据、评分排序，输出结构化 JSON（不做翻译和排版）"""
    now = datetime.now()
    week_since = (now - timedelta(days=7)).strftime("%Y-%m-%d")

    # 四源采集
    gh_items = fetch_github_agent_skills(period, 10)
    ch_items = fetch_clawhub_skills(6)
    sh_items = fetch_skillhub_skills(6)
    ss_items = fetch_skillssh_skills(4)
    all_items = gh_items + ch_items + sh_items + ss_items

    all_items = dedup_items(all_items)

    new_count = len([x for x in gh_items if x.get("is_new", False)])

    # 统一评分
    max_stars = max((x["stars"] for x in all_items), default=1)
    for item in all_items:
        item["score"] = compute_score(item, max_stars, week_since)
    all_items.sort(key=lambda x: x["score"], reverse=True)

    # 强制混排：精选8个，≥4 GitHub + ≥2 ClawHub + ≥1 SkillHub + ≥1 Skills.sh（有数据时）
    remaining = list(all_items)
    top8 = []
    # 先取评分前4
    for item in all_items[:4]:
        top8.append(item)
        remaining.remove(item)

    # 确保 ≥4 GitHub
    gh_in_top = len([x for x in top8 if x["source"] == "GitHub"])
    if gh_in_top < 4:
        need = 4 - gh_in_top
        gh_remaining = [x for x in remaining if x["source"] == "GitHub"]
        for item in gh_remaining[:need]:
            top8.append(item)
            remaining.remove(item)

    # 确保 ≥2 ClawHub（有数据时）
    ch_in_top = len([x for x in top8 if x["source"] == "ClawHub"])
    if ch_in_top < 2:
        need = 2 - ch_in_top
        ch_remaining = [x for x in remaining if x["source"] == "ClawHub"]
        for item in ch_remaining[:need]:
            top8.append(item)
            remaining.remove(item)

    # 确保 ≥1 SkillHub（有数据时）
    sh_in_top = len([x for x in top8 if x["source"] == "SkillHub"])
    if sh_in_top < 1 and sh_items:
        sh_remaining = [x for x in remaining if x["source"] == "SkillHub"]
        if sh_remaining:
            top8.append(sh_remaining[0])
            remaining.remove(sh_remaining[0])

    # 确保 ≥1 Skills.sh（有数据时）
    ss_in_top = len([x for x in top8 if x["source"] == "Skills.sh"])
    if ss_in_top < 1 and ss_items:
        ss_remaining = [x for x in remaining if x["source"] == "Skills.sh"]
        if ss_remaining:
            top8.append(ss_remaining[0])
            remaining.remove(ss_remaining[0])

    while len(top8) < 8 and remaining:
        top8.append(remaining.pop(0))
    top8 = top8[:8]

    top8_names = {x["name"] for x in top8}
    backup = [x for x in all_items if x["name"] not in top8_names][:8]

    # 数据源汇总
    sources = []
    if gh_items: sources.append("GitHub")
    if ch_items: sources.append("ClawHub")
    if sh_items: sources.append("SkillHub")
    if ss_items: sources.append("Skills.sh")

    # 输出结构化 JSON
    output = {
        "date": now.strftime("%Y.%m.%d"),
        "period": period,
        "new_count": new_count,
        "total_count": len(all_items),
        "sources": " + ".join(sources),
        "top8": top8,
        "backup": backup,
    }

    return json.dumps(output, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="mu-skill-hunter 周报数据采集")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"], default="weekly")
    args = parser.parse_args()
    print(generate_data(args.period))


if __name__ == "__main__":
    main()
