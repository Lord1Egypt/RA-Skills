#!/usr/bin/env python3
"""
SkillHub.cn 数据抓取脚本 v1.5.0（自依赖版）

v1.5.0 改造：移除 `skillhub` CLI 外部二进制依赖，直接调用 SkillHub HTTP API。
  - 排行榜：GET https://api.skillhub.cn/api/v1/showcase/{type}
  - 搜索：   GET https://api.skillhub.cn/api/v1/search?q={kw}&limit={n}

覆盖：
  - 6 排行榜（hot / featured / newest / recommended / trending / paid）
  - 11 分类搜索（用分类中文名作为关键词）
  - 6 记忆关键词搜索

目标覆盖：1000+ 条候选
"""
import argparse
import json
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from pathlib import Path


# SkillHub API 端点（与 skillhub CLI 同源，从 CLI 源码 RANKING_ENDPOINTS 提取）
SKILLHUB_API_HOST = "https://api.skillhub.cn"
RANKING_ENDPOINTS = {
    "hot": "/api/v1/showcase/hot",
    "featured": "/api/v1/showcase/featured",
    "newest": "/api/v1/showcase/newest",
    "recommended": "/api/v1/showcase/recommended",
    "trending": "/api/v1/showcase/trending",
    "paid": "/api/v1/showcase/paid",
}
SEARCH_ENDPOINT = "/api/v1/search"

# 兼容旧版 fetch_skillhub.py 中 7 个 RANKING_TYPES（"all" 没有对应端点，跳过）
RANKING_TYPES = ["hot", "newest", "trending", "featured", "recommended", "paid"]

CATEGORY_SLUGS = {
    "knowledge-management": "知识管理",
    "office-efficiency": "办公效率",
    "content-creation": "内容创作",
    "data-analysis": "数据分析",
    "ai-agent": "AI Agent",
    "design-media": "设计多媒体",
    "professional": "行业专业",
    "dev-programming": "开发编程",
    "life-service": "生活服务",
    "it-ops-security": "IT运维安全",
    "business-ops": "商业运营",
}

MEMORY_SEARCH_KEYWORDS = ["飞书", "Python", "定时任务", "审计", "财务", "GitHub"]

DEFAULT_HEADERS = {
    "User-Agent": "global-skill-daily/1.5.0",
    "Accept": "application/json",
}


def _http_get_json(url: str, timeout: int = 20) -> dict | list | None:
    """发起 GET 请求，返回 JSON。失败返回 None。"""
    req = urllib.request.Request(url, headers=DEFAULT_HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
        return json.loads(body)
    except urllib.error.HTTPError as e:
        print(f"  [HTTP {e.code}] {e.reason}")
        return None
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        print(f"  [Error] {e}")
        return None


def fetch_rankings() -> list:
    """抓取 6 大排行榜（每个端点返回 {section, skills, total} 结构）。"""
    print("[1/3] 抓取排行榜...")
    all_skills: dict[str, dict] = {}

    for rt in RANKING_TYPES:
        print(f"  {rt:15s}", end="", flush=True)
        url = SKILLHUB_API_HOST + RANKING_ENDPOINTS[rt]
        data = _http_get_json(url, timeout=30)

        if data and isinstance(data, dict) and "skills" in data:
            skills = data["skills"]
        elif isinstance(data, list):
            skills = data
        else:
            print(f" FAIL")
            continue

        for s in skills:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_rankings"] = [rt]
            elif slug and rt not in all_skills[slug].get("_rankings", []):
                all_skills[slug].setdefault("_rankings", []).append(rt)

        print(f" OK ({len(skills)})")
        time.sleep(0.3)  # 礼貌限流

    return list(all_skills.values())


def fetch_category_search() -> list:
    """按 11 个分类搜索补充长尾。"""
    print("\n[2/3] 按分类搜索...")
    all_skills: dict[str, dict] = {}
    for cat_slug, cat_zh in CATEGORY_SLUGS.items():
        print(f"  {cat_zh:10s}", end="", flush=True)
        params = urllib.parse.urlencode({"q": cat_zh, "limit": 20})
        url = f"{SKILLHUB_API_HOST}{SEARCH_ENDPOINT}?{params}"
        data = _http_get_json(url, timeout=15)

        if data and isinstance(data, dict) and "results" in data:
            results = data["results"]
        elif isinstance(data, list):
            results = data
        else:
            print(f" FAIL")
            continue

        for s in results:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_source"] = "category_search"
                all_skills[slug]["_search_category"] = cat_slug

        print(f" OK ({len(results)})")
        time.sleep(0.3)

    return list(all_skills.values())


def fetch_keyword_search(keywords=None) -> list:
    """按记忆关键词精准搜索。"""
    kws = keywords or MEMORY_SEARCH_KEYWORDS
    print(f"\n[3/3] 关键词搜索（{len(kws)} 个）...")
    all_skills: dict[str, dict] = {}

    for kw in kws:
        print(f"  {kw:10s}", end="", flush=True)
        params = urllib.parse.urlencode({"q": kw, "limit": 20})
        url = f"{SKILLHUB_API_HOST}{SEARCH_ENDPOINT}?{params}"
        data = _http_get_json(url, timeout=15)

        if data and isinstance(data, dict) and "results" in data:
            results = data["results"]
        elif isinstance(data, list):
            results = data
        else:
            print(f" FAIL")
            continue

        for s in results:
            slug = s.get("slug", "")
            if slug and slug not in all_skills:
                all_skills[slug] = s
                all_skills[slug]["_source"] = "keyword_search"
                all_skills[slug]["_search_keyword"] = kw

        print(f" OK ({len(results)})")
        time.sleep(0.3)

    return list(all_skills.values())


def normalize_skill(skill):
    """标准化技能数据。"""
    labels = skill.get("labels", {})
    if isinstance(labels, str):
        try:
            labels = json.loads(labels)
        except (json.JSONDecodeError, ValueError):
            labels = {}

    return {
        "slug": skill.get("slug", ""),
        "name": skill.get("name", skill.get("displayName", "")),
        "ownerName": skill.get("ownerName", ""),
        "version": skill.get("version", ""),
        "source": skill.get("source", ""),
        "category": skill.get("category", ""),
        "category_zh": CATEGORY_SLUGS.get(skill.get("category", ""), skill.get("category", "")),
        "subCategories": skill.get("subCategories", []),
        "description": skill.get("description", ""),
        "description_zh": skill.get("description_zh", ""),
        "downloads": skill.get("downloads", 0),
        "installs": skill.get("installs", 0),
        "stars": skill.get("stars", 0),
        "score": skill.get("score", 0),
        "requires_api_key": labels.get("requires_api_key", "false") == "true" if isinstance(labels, dict) else False,
        "verified": skill.get("verified", False),
        "claimable": skill.get("claimable", False),
        "created_at": skill.get("created_at", 0),
        "updated_at": skill.get("updated_at", 0),
        "homepage": skill.get("homepage", ""),
        "_rankings": skill.get("_rankings", []),
        "_source": skill.get("_source", "rankings"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/snapshots", help="输出目录")
    parser.add_argument("--date", default=None)
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    # 1. 排行榜
    ranking_skills = fetch_rankings()

    # 2. 分类搜索
    category_skills = fetch_category_search()

    # 3. 关键词搜索
    keyword_skills = fetch_keyword_search()

    # 合并去重
    all_skills = {}
    for s in ranking_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)

    for s in category_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)
            all_skills[slug]["_source"] = "category_search"
        elif slug and slug in all_skills:
            if "category_search" not in all_skills[slug].get("_source", ""):
                all_skills[slug]["_source"] = all_skills[slug].get("_source", "") + "+category_search"

    for s in keyword_skills:
        slug = s.get("slug", "")
        if slug and slug not in all_skills:
            all_skills[slug] = normalize_skill(s)
            all_skills[slug]["_source"] = "keyword_search"
        elif slug and slug in all_skills:
            all_skills[slug]["_source"] = all_skills[slug].get("_source", "") + "+keyword_search"

    skills = list(all_skills.values())
    print(f"\n合并去重后: {len(skills)} 个独立技能")

    # 保存
    output_path = Path(args.output) / f"{date_str}.skillhub.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    snapshot = {
        "snapshot_date": date_str,
        "fetched_at": datetime.now().isoformat(),
        "platform": "skillhub.cn",
        "total_count": len(skills),
        "source_breakdown": {
            "rankings_only": sum(1 for s in skills if "+" not in s.get("_source", "") and s.get("_source") == "rankings"),
            "with_category_search": sum(1 for s in skills if "category_search" in s.get("_source", "")),
            "with_keyword_search": sum(1 for s in skills if "keyword_search" in s.get("_source", "")),
        },
        "skills": skills
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    print(f"已保存: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
