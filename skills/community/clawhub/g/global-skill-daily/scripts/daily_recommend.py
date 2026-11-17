"""
daily_recommend.py — 10 维度 12 个推荐引擎

输入：
  data/snapshots/{date}.merged.json    — normalize 输出
  data/user_context_{date}.json        — scan_user_context 输出

输出：
  data/recommended/{date}.json         — 推荐结果（结构化）
  data/recommended/{date}.md           — 推荐简报（markdown）

10 维度设计：
  🔥 trending_both      ×2  双榜都火（ClawHub+SkillHub 同时活跃安装）
  ⭐ quality            ×1  口碑精品（star_rate 高 + 下载≥1000）
  🚀 newcomers          ×1  新星上线（≤30天 + 增长快）
  🇨🇳 china_only        ×1  国内独火（SkillHub高 / ClawHub低，差距比≥5）
  🌍 global_only        ×1  全球独火（ClawHub高 / SkillHub低）
  👤 active_developer   ×1  活跃开发者（跨平台聚合）
  🧠 memory_collision   ×1  记忆碰撞（3级权重，强化版）
  🎯 scene_match        ×2  痛点匹配（7大场景，不同场景各1）
  🛡️ verified           ×1  平台安全审计通过（可选，候选空跳过）
  🏆 panorama           ×1  全景视角（评论≥1，发现长尾）
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path


# ============== 痛点场景库（7 大场景） ==============
PAIN_POINTS = {
    "automation_office": {
        "label": "🤖 自动化办公",
        "weight": 1.5,
        "keywords": [
            "document", "docx", "word", "excel", "xlsx", "spreadsheet", "ppt", "powerpoint",
            "pdf", "form", "approval", "workflow", "office", "notion", "feishu", "lark",
            "dingtalk", "wechat", "work", "文档", "表格", "幻灯片", "审批", "工作流",
        ],
    },
    "dev_tools": {
        "label": "🛠️ 开发工具",
        "weight": 1.5,
        "keywords": [
            "code", "git", "github", "gitlab", "deploy", "debug", "test", "lint", "build",
            "ci", "cd", "docker", "kubernetes", "k8s", "refactor", "review", "terminal",
            "shell", "bash", "powershell", "代码", "部署", "调试", "测试",
        ],
    },
    "content_creation": {
        "label": "✍️ 内容创作",
        "weight": 1.2,
        "keywords": [
            "write", "article", "blog", "markdown", "html", "css", "video", "image",
            "design", "publish", "wechat", "mp", "公众号", "小红书", "抖音", "bilibili",
            "图文", "排版", "设计", "视频", "写作",
        ],
    },
    "data_collection": {
        "label": "🕷️ 数据采集",
        "weight": 1.2,
        "keywords": [
            "scrape", "crawl", "spider", "search", "extract", "parse", "analyze",
            "visualize", "chart", "table", "数据", "爬虫", "搜索", "分析", "可视化",
        ],
    },
    "ai_enhancement": {
        "label": "🧠 AI 增强",
        "weight": 1.3,
        "keywords": [
            "agent", "memory", "workflow", "automation", "llm", "gpt", "claude",
            "gemini", "openai", "anthropic", "rag", "embedding", "prompt", "fine-tune",
            "智能", "代理", "记忆", "工作流", "自动化",
        ],
    },
    "china_first": {
        "label": "🇨🇳 中文支持",
        "weight": 1.0,
        "keywords": [
            "feishu", "lark", "wechat", "weixin", "dingtalk", "xiaohongshu", "douyin",
            "bilibili", "weibo", "zhihu", "tencent", "alibaba", "baidu",
            "飞书", "微信", "钉钉", "小红书", "抖音", "B站", "微博", "知乎",
        ],
    },
    "finance_analysis": {
        "label": "💰 金融分析",
        "weight": 0.8,
        "keywords": [
            "finance", "audit", "tax", "accounting", "treasury", "stock", "fund",
            "bond", "valuation", "report", "财报", "审计", "税务", "财务", "会计",
            "券商", "投行", "估值",
        ],
    },
}


def _match_pain_points(skill: dict) -> list[tuple[str, float, list[str]]]:
    """匹配痛点场景，返回 [(scene_key, weighted_score, matched_keywords)]。"""
    unified = skill["unified"]
    text = " ".join([
        unified.get("name", ""),
        unified.get("description", ""),
        " ".join(unified.get("categories", [])),
        " ".join(unified.get("tags", [])),
    ]).lower()

    matches = []
    for scene_key, scene in PAIN_POINTS.items():
        matched = []
        for kw in scene["keywords"]:
            if len(kw) >= 3:
                if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text):
                    matched.append(kw)
            else:
                if kw.lower() in text:
                    matched.append(kw)
        if matched:
            score = len(matched) * scene["weight"]
            matches.append((scene_key, score, matched))

    matches.sort(key=lambda x: -x[1])
    return matches


def _match_memory(skill: dict, user_context: dict) -> tuple[int, list[str]]:
    """匹配用户上下文关键词，返回 (总权重, matched_words)。"""
    unified = skill["unified"]
    text = " ".join([
        unified.get("name", ""),
        unified.get("description", ""),
        " ".join(unified.get("categories", [])),
        " ".join(unified.get("tags", [])),
    ]).lower()

    matched = []
    total_weight = 0
    for kw_info in user_context.get("keywords", []):
        kw = kw_info["word"].lower()
        weight = kw_info["weight"]
        if len(kw) >= 3:
            if re.search(r"\b" + re.escape(kw) + r"\b", text):
                matched.append(kw_info["word"])
                total_weight += weight
        else:
            if kw in text:
                matched.append(kw_info["word"])
                total_weight += weight

    return total_weight, matched


def _build_chinese_summary(skill: dict, matched_scenes: list, matched_memory: list) -> str:
    """0 token 中文一句话。"""
    unified = skill["unified"]
    tags = unified.get("tags", [])[:3]
    categories = unified.get("categories", [])[:2]

    if matched_memory:
        return f"匹配你的 {len(matched_memory)} 个上下文关键词（关键词已脱敏，仅本地保留），整合 {', '.join(tags) if tags else '通用'} 能力"
    elif matched_scenes:
        scene_label = PAIN_POINTS[matched_scenes[0][0]]["label"]
        return f"面向「{scene_label}」场景，整合 {', '.join(tags) if tags else categories[0] if categories else '通用'} 能力"
    elif tags:
        return f"集成 {', '.join(tags)} 等能力，可作为通用工具使用"
    else:
        return f"{unified.get('name', '')} — 通用工具"


def _load_recent_recommended(data_dir: Path, lookback_days: int = 14) -> set[str]:
    """加载过去 N 天已推荐的 slug 集合（跨维度去重）。
    v1.1: 从 7 天延长到 14 天，配合每 3 天 1 次的频率可覆盖 4-5 次历史推荐。
    """
    recommended_dir = data_dir / "recommended"
    if not recommended_dir.exists():
        return set()

    cutoff = datetime.now() - timedelta(days=lookback_days)
    seen = set()

    for f in recommended_dir.glob("*.json"):
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                continue
            data = json.loads(f.read_text(encoding="utf-8"))
            for rec in data.get("recommendations", []):
                slug = rec.get("slug", "")
                if slug:
                    seen.add(slug.lower())
        except (OSError, json.JSONDecodeError):
            continue

    return seen


# ============== 维度轮换机制（v1.1） ==============
# 10 维度分 3 组轮换，每 3 天 1 个周期，确保每次推荐角度不同
DIMENSION_GROUPS = {
    "A": {
        "name": "趋势组",
        "description": "聚焦双榜热度与跨平台差异",
        "dimensions": ["trending_both", "china_only", "global_only", "panorama"],
        "targets": {"trending_both": 2, "china_only": 2, "global_only": 2, "panorama": 1},
    },
    "B": {
        "name": "质量组",
        "description": "聚焦口碑精品与新人新作",
        "dimensions": ["quality", "newcomers", "active_developer", "verified"],
        "targets": {"quality": 2, "newcomers": 2, "active_developer": 2, "verified": 1},
    },
    "C": {
        "name": "用户组",
        "description": "聚焦记忆碰撞与痛点匹配",
        "dimensions": ["memory_collision", "scene_match", "trending_both"],
        "targets": {"memory_collision": 3, "scene_match": 4, "trending_both": 1},
    },
}


def _pick_dimension_group(date_str: str) -> tuple[str, dict]:
    """根据日期选择本次激活的维度组。
    每 3 天 1 个周期：第 1 天=A，第 2 天=B，第 3 天=C，循环。
    """
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        dt = datetime.now()
    # 从 2026-01-01 起算的偏移天数，3 天 1 周期
    base = datetime(2026, 1, 1)
    days_offset = (dt - base).days
    group_idx = (days_offset // 3) % 3
    group_key = ["A", "B", "C"][group_idx]
    return group_key, DIMENSION_GROUPS[group_key]


def recommend(merged_data: dict, user_context: dict, recent_recommended: set[str] | None = None) -> dict:
    """主推荐函数。
    v1.1: 维度轮换 — 根据日期选择本次激活的维度组，10 维度分 3 组轮换。
    """
    if recent_recommended is None:
        recent_recommended = set()

    skills = merged_data.get("skills", [])
    date_str = merged_data.get("snapshot_date", datetime.now().strftime("%Y-%m-%d"))
    group_key, group_info = _pick_dimension_group(date_str)
    print(f"[recommend] input skills: {len(skills)}, recent recommended: {len(recent_recommended)}, dimension group: {group_key} ({group_info['name']})")

    # 预计算每个 skill 的痛点匹配和记忆匹配
    for skill in skills:
        skill["_pain_points"] = _match_pain_points(skill)
        skill["_memory_match"] = _match_memory(skill, user_context)

    recommendations = []
    seen_slugs = set(recent_recommended)  # 跨维度去重

    def _pick(filter_fn, sort_key, count: int, dim_key: str, dim_label: str, used_fallback: bool = False):
        """从候选池中挑选，跳过已推荐。"""
        candidates = [
            s for s in skills
            if filter_fn(s) and s["unified"]["slug"].lower() not in seen_slugs
        ]
        candidates.sort(key=sort_key, reverse=True)

        picked = candidates[:count]
        for s in picked:
            seen_slugs.add(s["unified"]["slug"].lower())
            recommendations.append(_format_recommendation(s, dim_key, dim_label, used_fallback))

        if len(picked) < count:
            print(f"[recommend] {dim_key}: only picked {len(picked)}/{count} (candidates={len(candidates)})")
        else:
            print(f"[recommend] {dim_key}: picked {len(picked)}/{count}")

        return picked

    # === 维度过滤器定义 ===
    def _filter_trending_both(s):
        u = s["unified"]
        return (
            s["source"] == "both"
            and u["installs"]["clawhub"] >= 50
            and u["installs"]["skillhub"] >= 50
        )

    def _filter_quality(s):
        u = s["unified"]
        return u["downloads"]["total"] >= 500 and u["star_rate"] >= 0.3

    def _filter_newcomers(s):
        u = s["unified"]
        return (
            (u["age_days"] or 999) <= 90  # v1.1: 从 60 放宽到 90 天
            and u["installs"]["total"] >= 5  # v1.1: 从 10 放宽到 5
        )

    def _filter_china_only(s):
        u = s["unified"]
        return (
            u["installs"]["skillhub"] >= 50
            and u["installs"]["clawhub"] <= 10
            and u["platform_gap_ratio"] >= 5.0
        )

    def _filter_global_only(s):
        u = s["unified"]
        return (
            u["installs"]["clawhub"] >= 100
            and u["installs"]["skillhub"] <= 20
            and u["platform_gap_ratio"] <= 0.2
        )

    def _filter_verified(s):
        # v1.1: verified badge 全空，改用"质量代理"——versions>=3 + stars>=30 + 非 suspicious
        u = s["unified"]
        return (
            u["versions_count"] >= 3
            and u["stars"]["total"] >= 30
            and not s.get("clawhub", {}).get("skill", {}).get("isSuspicious", False)
        )

    def _filter_panorama(s):
        return s["unified"]["ratings_count"] >= 1

    def _filter_memory(s):
        return s["_memory_match"][0] >= 3

    # === 根据维度组选择执行哪些维度 ===
    targets = group_info["targets"]

    if "trending_both" in targets:
        _pick(_filter_trending_both, lambda s: s["unified"]["installs"]["total"],
              targets["trending_both"], "trending_both", "🔥 双榜热装")

    if "quality" in targets:
        _pick(_filter_quality, lambda s: (s["unified"]["star_rate"], s["unified"]["downloads"]["total"]),
              targets["quality"], "quality", "⭐ 口碑精品")

    if "newcomers" in targets:
        _pick(_filter_newcomers, lambda s: (s["unified"]["installs"]["total"], s["unified"]["stars"]["total"]),
              targets["newcomers"], "newcomers", "🚀 新星上线")

    if "china_only" in targets:
        _pick(_filter_china_only, lambda s: (s["unified"]["installs"]["skillhub"], s["unified"]["platform_gap_ratio"]),
              targets["china_only"], "china_only", "🇨🇳 国内独火")

    if "global_only" in targets:
        _pick(_filter_global_only, lambda s: (s["unified"]["installs"]["clawhub"], -s["unified"]["platform_gap_ratio"]),
              targets["global_only"], "global_only", "🌍 全球独火")

    if "verified" in targets:
        _pick(_filter_verified, lambda s: (s["unified"]["versions_count"], s["unified"]["stars"]["total"]),
              targets["verified"], "verified", "🛡️ 质量认证")

    if "panorama" in targets:
        _pick(_filter_panorama, lambda s: (s["unified"]["ratings_count"], s["unified"]["installs"]["total"]),
              targets["panorama"], "panorama", "🏆 全景视角")

    # 6. 👤 active_developer
    if "active_developer" in targets:
        owner_stats: dict[str, dict] = defaultdict(lambda: {"skills": [], "total_installs": 0})
        for s in skills:
            owner = s["unified"].get("owner", "")
            if not owner:
                continue
            owner_stats[owner]["skills"].append(s)
            owner_stats[owner]["total_installs"] += s["unified"]["installs"]["total"]

        top_owners = sorted(
            owner_stats.items(),
            key=lambda x: (len(x[1]["skills"]), x[1]["total_installs"]),
            reverse=True
        )[:5]

        target_count = targets["active_developer"]
        picked_dev = 0
        for owner, stats in top_owners:
            if picked_dev >= target_count:
                break
            candidates = [s for s in stats["skills"] if s["unified"]["slug"].lower() not in seen_slugs]
            if not candidates:
                continue
            candidates.sort(key=lambda s: s["unified"]["installs"]["total"], reverse=True)
            s = candidates[0]
            seen_slugs.add(s["unified"]["slug"].lower())
            rec = _format_recommendation(s, "active_developer", "👤 活跃开发者")
            rec["developer_info"] = {
                "owner": owner,
                "skill_count": len(stats["skills"]),
                "total_installs": stats["total_installs"],
                "other_slugs": [s2["unified"]["slug"] for s2 in stats["skills"][:5] if s2["unified"]["slug"] != s["unified"]["slug"]],
            }
            recommendations.append(rec)
            picked_dev += 1
            print(f"[recommend] active_developer: picked {s['unified']['slug']} (owner={owner}, skills={len(stats['skills'])})")

    # 7. 🧠 memory_collision
    if "memory_collision" in targets:
        _pick(_filter_memory, lambda s: s["_memory_match"][0],
              targets["memory_collision"], "memory_collision", "🧠 记忆碰撞")

    # 8. 🎯 scene_match（不同场景各 1，按 targets 数量挑选）
    if "scene_match" in targets:
        scene_picked = set()
        scene_candidates_by_key = defaultdict(list)
        for s in skills:
            if s["unified"]["slug"].lower() in seen_slugs:
                continue
            for scene_key, score, matched in s["_pain_points"]:
                scene_candidates_by_key[scene_key].append((s, score, matched))

        scene_order = sorted(PAIN_POINTS.keys(), key=lambda k: -PAIN_POINTS[k]["weight"])
        scene_target = targets["scene_match"]
        for scene_key in scene_order:
            if scene_target <= 0:
                break
            if scene_key in scene_picked:
                continue
            candidates = scene_candidates_by_key.get(scene_key, [])
            if not candidates:
                continue
            candidates.sort(key=lambda x: -x[1])
            s, score, matched = candidates[0]
            seen_slugs.add(s["unified"]["slug"].lower())
            rec = _format_recommendation(s, "scene_match", f"🎯 痛点匹配（{PAIN_POINTS[scene_key]['label']}）")
            rec["scene_info"] = {
                "scene_key": scene_key,
                "scene_label": PAIN_POINTS[scene_key]["label"],
                "matched_keywords": matched,
                "score": score,
            }
            recommendations.append(rec)
            scene_picked.add(scene_key)
            scene_target -= 1
            print(f"[recommend] scene_match: picked {s['unified']['slug']} (scene={scene_key})")

        # 不足时从其他场景补充
        while scene_target > 0:
            added = False
            for scene_key in scene_order:
                if scene_key in scene_picked:
                    continue
                candidates = [
                    (s, score, matched)
                    for s, score, matched in scene_candidates_by_key.get(scene_key, [])
                    if s["unified"]["slug"].lower() not in seen_slugs
                ]
                if candidates:
                    candidates.sort(key=lambda x: -x[1])
                    s, score, matched = candidates[0]
                    seen_slugs.add(s["unified"]["slug"].lower())
                    rec = _format_recommendation(s, "scene_match_extra", f"🎯 痛点匹配（{PAIN_POINTS[scene_key]['label']}）")
                    rec["scene_info"] = {
                        "scene_key": scene_key,
                        "scene_label": PAIN_POINTS[scene_key]["label"],
                        "matched_keywords": matched,
                        "score": score,
                    }
                    recommendations.append(rec)
                    scene_picked.add(scene_key)
                    scene_target -= 1
                    added = True
                    break
            if not added:
                break

    # 跨平台对比统计
    cross_platform_count = sum(
        1 for r in recommendations
        if r["dimension"] in {"trending_both", "china_only", "global_only"}
    )

    # === 跨平台洞察（v1.1 核心特色） ===
    cross_platform_insights = _build_cross_platform_insights(skills, recommendations)

    return {
        "report_date": date_str,
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "merged_count": merged_data.get("merged_count", 0),
        "both_count": merged_data.get("both_count", 0),
        "clawhub_count": merged_data.get("clawhub_count", 0),
        "skillhub_count": merged_data.get("skillhub_count", 0),
        "recommendations_count": len(recommendations),
        "cross_platform_count": cross_platform_count,
        "dedup_skipped_count": len(recent_recommended),
        "dedup_window_days": 14,
        "dimension_group": group_key,
        "dimension_group_name": group_info["name"],
        "dimension_group_desc": group_info["description"],
        "recommendations": recommendations,
        "top_developers": [
            {
                "owner": owner,
                "skill_count": len(stats["skills"]),
                "total_installs": stats["total_installs"],
                "top_slugs": [s["unified"]["slug"] for s in stats["skills"][:3]],
            }
            for owner, stats in (top_owners if "top_owners" in dir() else [])[:5]
        ] if "top_owners" in dir() else [],
        "china_only_top3": cross_platform_insights["china_only_top5"][:3],
        "global_only_top3": cross_platform_insights["global_only_top5"][:3],
        "trending_both_top3": cross_platform_insights["trending_both_top5"][:3],
        "cross_platform_insights": cross_platform_insights,
    }


def _build_cross_platform_insights(skills: list, recommendations: list) -> dict:
    """v1.1 新增：跨平台生态洞察模块。
    5 个分析章节：
      A. 热度差异榜 Top 5（gap_ratio 排序）
      B. 双榜共有但热度差 >5x
      C. 国内开发者偏好品类
      D. 全球开发者偏好品类
      E. 中文站特色品类
    """
    # A. 热度差异榜 Top 5（双向）
    china_only_top5 = sorted(
        [s for s in skills
         if s["unified"]["installs"]["skillhub"] >= 30
         and s["unified"]["platform_gap_ratio"] >= 5.0],
        key=lambda x: -x["unified"]["installs"]["skillhub"]
    )[:5]

    global_only_top5 = sorted(
        [s for s in skills
         if s["unified"]["installs"]["clawhub"] >= 50
         and s["unified"]["platform_gap_ratio"] <= 0.2],
        key=lambda x: -x["unified"]["installs"]["clawhub"]
    )[:5]

    # B. 双榜共有但热度差 >5x（识别"地区偏好型"skill）
    both_with_gap = []
    for s in skills:
        if s["source"] != "both":
            continue
        u = s["unified"]
        ch = u["installs"]["clawhub"]
        sh = u["installs"]["skillhub"]
        if ch <= 0 or sh <= 0:
            continue
        ratio = max(ch, sh) / min(ch, sh)
        if ratio >= 5.0:
            both_with_gap.append({
                "slug": u["slug"],
                "name": u["name"],
                "clawhub_installs": ch,
                "skillhub_installs": sh,
                "ratio": round(ratio, 1),
                "preference": "🇨🇳 国内偏好" if sh > ch else "🌍 全球偏好",
            })
    both_with_gap.sort(key=lambda x: -x["ratio"])
    both_gap_top5 = both_with_gap[:5]

    # C+D. 品类偏好对比（独占 skill 的 categories 分布）
    china_only_categories = defaultdict(int)
    global_only_categories = defaultdict(int)
    for s in skills:
        u = s["unified"]
        cats = u.get("categories", []) or ["未分类"]
        if not cats:
            cats = ["未分类"]
        if u["installs"]["skillhub"] >= 30 and u["platform_gap_ratio"] >= 5.0:
            for c in cats:
                china_only_categories[c] += 1
        elif u["installs"]["clawhub"] >= 50 and u["platform_gap_ratio"] <= 0.2:
            for c in cats:
                global_only_categories[c] += 1

    china_cat_sorted = sorted(china_only_categories.items(), key=lambda x: -x[1])[:8]
    global_cat_sorted = sorted(global_only_categories.items(), key=lambda x: -x[1])[:8]

    # E. 中文站特色品类（中文平台相关 skill）
    china_platform_keywords = ["bilibili", "douyin", "wechat", "weixin", "taobao", "tmall",
                                "alipay", "xiaohongshu", "weibo", "zhihu", "dingtalk",
                                "feishu", "lark", "qq", "tencent", "alibaba", "baidu",
                                "京东", "淘宝", "微信", "抖音", "B站", "微博", "知乎", "小红书"]
    china_platform_skills = []
    for s in skills:
        u = s["unified"]
        text = f"{u.get('name', '')} {u.get('description', '')} {' '.join(u.get('tags', []))}".lower()
        for kw in china_platform_keywords:
            if kw.lower() in text:
                china_platform_skills.append({
                    "slug": u["slug"],
                    "name": u["name"],
                    "matched_keyword": kw,
                    "skillhub_installs": u["installs"]["skillhub"],
                    "clawhub_installs": u["installs"]["clawhub"],
                    "source": s["source"],
                })
                break
    china_platform_skills.sort(key=lambda x: -x["skillhub_installs"])

    # 洞察结论（基于数据的简单判断）
    insights = []
    if both_gap_top5:
        insights.append(f"发现 {len(both_with_gap)} 个双榜共有但热度差 >5x 的 skill，反映中英文开发者偏好分化")
    if china_cat_sorted:
        top_china_cat = china_cat_sorted[0]
        insights.append(f"国内独火 skill 集中在「{top_china_cat[0]}」品类（{top_china_cat[1]} 个）")
    if global_cat_sorted:
        top_global_cat = global_cat_sorted[0]
        insights.append(f"全球独火 skill 集中在「{top_global_cat[0]}」品类（{top_global_cat[1]} 个）")
    if china_platform_skills:
        insights.append(f"识别出 {len(china_platform_skills)} 个中文平台特色 skill（bilibili/douyin/wechat 等）")

    return {
        "china_only_top5": [
            {
                "slug": s["unified"]["slug"],
                "name": s["unified"]["name"],
                "skillhub_installs": s["unified"]["installs"]["skillhub"],
                "clawhub_installs": s["unified"]["installs"]["clawhub"],
                "gap_ratio": s["unified"]["platform_gap_ratio"] if s["unified"]["platform_gap_ratio"] != float('inf') else None,
            } for s in china_only_top5
        ],
        "global_only_top5": [
            {
                "slug": s["unified"]["slug"],
                "name": s["unified"]["name"],
                "clawhub_installs": s["unified"]["installs"]["clawhub"],
                "skillhub_installs": s["unified"]["installs"]["skillhub"],
                "source_url": s["unified"].get("source_url", ""),
            } for s in global_only_top5
        ],
        "trending_both_top5": [
            {
                "slug": s["unified"]["slug"],
                "name": s["unified"]["name"],
                "clawhub_installs": s["unified"]["installs"]["clawhub"],
                "skillhub_installs": s["unified"]["installs"]["skillhub"],
                "total_installs": s["unified"]["installs"]["total"],
                "source_url": s["unified"].get("source_url", ""),
            } for s in sorted(
                [s for s in skills if s["source"] == "both"],
                key=lambda x: -x["unified"]["installs"]["total"]
            )[:5]
        ],
        "both_with_gap_top5": both_gap_top5,
        "china_preferred_categories": [{"category": c, "count": n} for c, n in china_cat_sorted],
        "global_preferred_categories": [{"category": c, "count": n} for c, n in global_cat_sorted],
        "china_platform_skills": china_platform_skills[:10],
        "insights_summary": insights,
    }


def _format_recommendation(skill: dict, dimension: str, dimension_label: str, used_fallback: bool = False) -> dict:
    """格式化推荐结果。"""
    unified = skill["unified"]
    memory_weight, memory_matched = skill["_memory_match"]
    pain_points = skill["_pain_points"]

    return {
        "slug": unified["slug"],
        "name": unified["name"],
        "description": unified.get("description", "")[:500],
        "source": skill["source"],
        "platforms_active": unified["platforms_active"],
        "dimension": dimension,
        "dimension_label": dimension_label,
        "installs": unified["installs"],
        "stars": unified["stars"],
        "downloads": unified["downloads"],
        "versions_count": unified["versions_count"],
        "age_days": unified["age_days"],
        "days_since_update": unified["days_since_update"],
        "owner": unified["owner"],
        "verified": unified["verified"],
        "categories": unified["categories"][:5],
        "tags": unified["tags"][:8],
        "latest_changelog": unified.get("latest_changelog"),
        "source_url": unified.get("source_url") or (
            skill["clawhub"]["source_url"] if skill.get("clawhub") else
            skill["skillhub"]["source_url"] if skill.get("skillhub") else
            f"https://clawhub.ai/skills/{unified['slug']}"
        ),
        "chinese_summary": _build_chinese_summary(skill, pain_points, memory_matched),
        "memory_match": {
            "weight": memory_weight,
            "matched_count": len(memory_matched),
        },
        "pain_points": [
            {"scene": PAIN_POINTS[k]["label"], "score": s, "matched": m}
            for k, s, m in pain_points[:3]
        ],
        "platform_gap_ratio": unified.get("platform_gap_ratio"),
        "used_fallback": used_fallback,
    }


def generate_markdown(result: dict, user_context: dict, merged_data: dict) -> str:
    """生成 markdown 简报。
    v1.1: 加入跨平台生态洞察章节（5 个分析模块）。
    """
    date = result["report_date"]
    group_name = result.get("dimension_group_name", "")
    group_desc = result.get("dimension_group_desc", "")
    lines = [
        f"# 🌐 全球 Skill 生态日报 | {date}",
        "",
        f"> 合并 ClawHub（{result['clawhub_count']}）+ SkillHub（{result['skillhub_count']}）→ 去重后 {result['merged_count']} 个独立 skill，今日推荐 {result['recommendations_count']} 个。",
        f"> 今日维度组：**{group_name}** — {group_desc}",
        "",
        "## TL;DR",
        "",
        f"- **双榜扫描**：ClawHub {result['clawhub_count']} + SkillHub {result['skillhub_count']} → 合并去重 {result['merged_count']} 个（双榜共有 {result['both_count']} 个）",
        f"- **今日推荐**：{result['recommendations_count']} 个，跨平台对比 {result['cross_platform_count']} 个",
        f"- **去重**：跳过过去 14 天已推荐 {result['dedup_skipped_count']} 个（v1.1 升级）",
        f"- **维度组**：{group_name}（{group_desc}）",
        "",
        "## 👤 用户上下文快照（仅计数，原始扫描仅存本地）",
        "",
        f"- **扫描关键词**：{user_context['total_unique_keywords']} 个（仅计数，不发布关键词列表）",
        f"- **活跃项目**：{len(user_context['active_projects'])} 个（仅计数）",
        f"- **经验文件**：{len(user_context['experience_files'])} 个（仅计数）",
        f"- **已装 skill**：{len(user_context['installed_skills'])} 个（仅计数）",
        "",
        "> 🔒 **隐私声明（v1.4.0）**：本快照只发布聚合计数，**不含任何上下文派生内容**（连关键词列表也不发布）。",
        "> 原始扫描结果（关键词/项目名/经验文件名/已装 skill 列表）仅存本地 `data/user_context_{date}.json`，",
        "> 不会推送至 Obsidian / IMA / 飞书等外部服务。可用 `--no-context-scan` 完全跳过扫描。",
        "",
        "## 🌏 跨平台生态洞察（v1.1 核心特色）",
        "",
    ]

    insights = result.get("cross_platform_insights", {})
    if insights:
        # 洞察结论
        if insights.get("insights_summary"):
            lines.append("### 🎯 数据洞察")
            lines.append("")
            for s in insights["insights_summary"]:
                lines.append(f"- {s}")
            lines.append("")

        # A. 热度差异榜 Top 5（双向）
        lines.extend([
            "### 📊 A. 热度差异榜 — 国内独火 Top 5（SkillHub 高 / ClawHub 低）",
            "",
            "| Skill | SkillHub 安装 | ClawHub 安装 | 差距倍数 |",
            "|-------|-------------|------------|---------|",
        ])
        for item in insights.get("china_only_top5", []):
            gap = item.get("gap_ratio")
            if gap is None:
                gap_display = "∞"
            else:
                gap_display = f"{gap:.1f}x"
            lines.append(f"| [{item['name']}](https://api.skillhub.cn/skills/{item['slug']}) | {item['skillhub_installs']:,} | {item['clawhub_installs']:,} | {gap_display} |")

        lines.extend([
            "",
            "### 📊 B. 热度差异榜 — 全球独火 Top 5（ClawHub 高 / SkillHub 低）",
            "",
            "| Skill | ClawHub 安装 | SkillHub 安装 |",
            "|-------|------------|-------------|",
        ])
        for item in insights.get("global_only_top5", []):
            lines.append(f"| [{item['name']}]({item.get('source_url', '#')}) | {item['clawhub_installs']:,} | {item['skillhub_installs']:,} |")

        # C. 双榜共有但热度差 >5x
        lines.extend([
            "",
            "### 🔄 C. 双榜共有但热度差 >5x — 中英文开发者偏好分化",
            "",
            "| Skill | ClawHub | SkillHub | 倍数 | 偏好方向 |",
            "|-------|---------|----------|------|---------|",
        ])
        for item in insights.get("both_with_gap_top5", []):
            lines.append(f"| {item['name']} | {item['clawhub_installs']:,} | {item['skillhub_installs']:,} | {item['ratio']}x | {item['preference']} |")

        # D. 品类偏好对比
        lines.extend([
            "",
            "### 🏷️ D. 中英文开发者品类偏好对比",
            "",
            "| 维度 | Top 品类分布（独占 skill 数） |",
            "|------|--------------------------|",
        ])
        china_cats = insights.get("china_preferred_categories", [])
        global_cats = insights.get("global_preferred_categories", [])
        china_str = "、".join([f"{c['category']}({c['count']})" for c in china_cats[:5]]) if china_cats else "—"
        global_str = "、".join([f"{c['category']}({c['count']})" for c in global_cats[:5]]) if global_cats else "—"
        lines.append(f"| 🇨🇳 国内独火 | {china_str} |")
        lines.append(f"| 🌍 全球独火 | {global_str} |")

        # E. 中文站特色品类
        lines.extend([
            "",
            "### 🇨🇳 E. 中文平台特色 skill（bilibili/douyin/wechat/小红书 等）",
            "",
            "| Skill | 命中关键词 | SkillHub 安装 | ClawHub 安装 | 来源 |",
            "|-------|----------|-------------|------------|------|",
        ])
        for item in insights.get("china_platform_skills", [])[:10]:
            lines.append(f"| {item['name']} | {item['matched_keyword']} | {item['skillhub_installs']:,} | {item['clawhub_installs']:,} | {item['source']} |")

        lines.append("")

    # 双榜共有 Top 3 表格（保留原表格作为快速浏览）
    lines.extend([
        "## 📊 跨平台趋势速览",
        "",
        "### 双榜共有 Top 3（ClawHub + SkillHub 都火）",
        "",
        "| Skill | ClawHub 安装 | SkillHub 安装 | 总安装 |",
        "|-------|------------|-------------|--------|",
    ])
    for item in result.get("trending_both_top3", []):
        lines.append(f"| [{item['name']}]({item.get('source_url', '#')}) | {item['clawhub_installs']:,} | {item['skillhub_installs']:,} | {item['total_installs']:,} |")

    lines.extend([
        "",
        f"## 🔥 今日推荐（{group_name} · 按维度分组）",
        "",
    ])

    # 按维度分组
    by_dim = defaultdict(list)
    for rec in result["recommendations"]:
        by_dim[rec["dimension"]].append(rec)

    dim_order = [
        "trending_both", "quality", "newcomers", "china_only", "global_only",
        "active_developer", "memory_collision", "scene_match", "scene_match_extra",
        "verified", "panorama",
    ]
    dim_labels = {
        "trending_both": "🔥 双榜热装",
        "quality": "⭐ 口碑精品",
        "newcomers": "🚀 新星上线",
        "china_only": "🇨🇳 国内独火",
        "global_only": "🌍 全球独火",
        "active_developer": "👤 活跃开发者",
        "memory_collision": "🧠 记忆碰撞",
        "scene_match": "🎯 痛点匹配",
        "scene_match_extra": "🎯 痛点匹配（补充）",
        "verified": "🛡️ 质量认证",
        "panorama": "🏆 全景视角",
    }

    for dim in dim_order:
        recs = by_dim.get(dim, [])
        if not recs:
            continue
        lines.append(f"### {dim_labels[dim]} × {len(recs)}")
        lines.append("")
        for rec in recs:
            platforms = " + ".join(rec["platforms_active"])
            lines.append(f"#### {rec['name']}")
            lines.append("")
            lines.append(f"- **Slug**: `{rec['slug']}`")
            lines.append(f"- **平台**: {platforms} | **Owner**: {rec['owner']} | **版本数**: {rec['versions_count']}")
            lines.append(f"- **安装**: ClawHub={rec['installs']['clawhub']:,} / SkillHub={rec['installs']['skillhub']:,} / Total={rec['installs']['total']:,}")
            lines.append(f"- **星标**: ClawHub={rec['stars']['clawhub']} / SkillHub={rec['stars']['skillhub']} / Total={rec['stars']['total']}")
            if rec.get("latest_changelog"):
                changelog = rec["latest_changelog"][:200].replace("\n", " ")
                lines.append(f"- **最近变更**: {changelog}{'...' if len(rec['latest_changelog']) > 200 else ''}")
            lines.append(f"- **中文解读**: {rec['chinese_summary']}")
            if rec["memory_match"]["weight"] > 0:
                lines.append(f"- **记忆命中**: {rec['memory_match']['weight']} 权重，匹配 {rec['memory_match'].get('matched_count', 0)} 个关键词（关键词已脱敏，仅本地保留）")
            if rec.get("pain_points"):
                pp = rec["pain_points"][0]
                lines.append(f"- **痛点场景**: {pp['scene']}（score={pp['score']}）")
            if rec.get("developer_info"):
                dev = rec["developer_info"]
                lines.append(f"- **开发者**: {dev['owner']}（{dev['skill_count']} 个 skill，总安装 {dev['total_installs']:,}）")
                if dev["other_slugs"]:
                    lines.append(f"- **其他作品**: {', '.join(dev['other_slugs'][:3])}")
            if rec.get("scene_info"):
                si = rec["scene_info"]
                lines.append(f"- **场景**: {si['scene_label']} — 匹配关键词: {', '.join(si['matched_keywords'][:5])}")
            lines.append(f"- **链接**: {rec['source_url']}")
            lines.append("")

    # 活跃开发者速览
    if result.get("top_developers"):
        lines.extend([
            "## 👤 活跃开发者速览",
            "",
            "| Owner | 技能数 | 总安装 | Top 3 作品 |",
            "|-------|-------|-------|-----------|",
        ])
        for dev in result.get("top_developers", [])[:5]:
            lines.append(f"| {dev['owner']} | {dev['skill_count']} | {dev['total_installs']:,} | {', '.join(dev['top_slugs'])} |")

    # 痛点匹配分组
    scene_groups = defaultdict(list)
    for rec in result["recommendations"]:
        if rec.get("scene_info"):
            scene_groups[rec["scene_info"]["scene_label"]].append(rec)

    if scene_groups:
        lines.extend([
            "",
            "## 🎯 痛点匹配（按场景）",
            "",
        ])
        for scene, recs in scene_groups.items():
            lines.append(f"### {scene}")
            for rec in recs:
                lines.append(f"- **{rec['name']}** — {rec['chinese_summary']}")
            lines.append("")

    # 数据说明
    lines.extend([
        "## 📌 数据说明",
        "",
        f"- **数据源**：ClawHub Convex API v4（{result['clawhub_count']} 个）+ SkillHub CLI（{result['skillhub_count']} 个）",
        f"- **合并去重**：normalized slug（去 -cn/-zh 后缀）作为合并键",
        f"- **去重窗口**：14 天跨维度去重（v1.1 升级，配合每 3 天 1 次频率）",
        f"- **维度轮换**：10 维度分 3 组（趋势/质量/用户），每 3 天 1 周期",
        f"- **今日维度组**：{group_name}（{group_desc}）",
        f"- **推荐算法**：global-skill-daily v1.1.0 — 维度轮换 + 14天去重 + 跨平台洞察",
        f"- **生成时间**：{result['generated_at']}",
        f"- **三处存放**：Obsidian ✓ | IMA FIM ✓ | 飞书 Card 2.0 ✓",
        "",
        "---",
        f"_由 global-skill-daily v1.1.0 自动生成_",
    ])

    return "\n".join(lines)


def main():
    if len(sys.argv) < 4:
        print("Usage: python daily_recommend.py <merged.json> <user_context.json> <output_dir>")
        sys.exit(1)

    merged_path = Path(sys.argv[1])
    context_path = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])
    output_dir.mkdir(parents=True, exist_ok=True)

    merged_data = json.loads(merged_path.read_text(encoding="utf-8"))
    user_context = json.loads(context_path.read_text(encoding="utf-8"))

    # 加载过去 7 天已推荐
    recent_recommended = _load_recent_recommended(merged_path.parent.parent, lookback_days=7)
    print(f"[recommend] recent recommended: {len(recent_recommended)} slugs")

    result = recommend(merged_data, user_context, recent_recommended)

    # 生成 markdown
    markdown = generate_markdown(result, user_context, merged_data)

    date_str = result["report_date"]
    json_path = output_dir / f"{date_str}.json"
    md_path = output_dir / f"{date_str}.md"

    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")

    print(f"[recommend] generated {len(result['recommendations'])} recommendations")
    print(f"[recommend] JSON: {json_path}")
    print(f"[recommend] MD:   {md_path}")


if __name__ == "__main__":
    main()
