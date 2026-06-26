#!/usr/bin/env python3
"""
ASIN Five-Dimension Health Analyzer
Calculates compliance, advertising, review, visual, and content scores
based on user-provided ASIN data and industry benchmarks.

Usage:
    python asin-analyze.py --asin B09VCTKXJM --category "camping tent" \
        --acos 28 --review-count 35 --negative-rate 8 --image-count 6 --video-count 1 \
        --has-prohibited-words false --scene-word-coverage 60

    python asin-analyze.py --input '{"asin":"B09VCTKXJM","category":"bluetooth earbuds","acos":32,"review_count":15,"negative_rate":12,"image_count":5,"video_count":0,"has_prohibited_words":false,"scene_word_coverage":40}'
"""

import argparse
import json
import sys
from datetime import datetime


# ── Industry Benchmarks ──────────────────────────────────────────

ACoS_THRESHOLDS = {
    "green": (0, 20),     # Excellent
    "yellow": (20, 30),   # Needs attention
    "red": (30, 100),     # Critical
}

NEGATIVE_RATE_THRESHOLDS = {
    "green": (0, 5),
    "yellow": (5, 15),
    "red": (15, 100),
}

IMAGE_THRESHOLDS = {
    "green": 7,     # 7+ images with scene shots
    "yellow": 5,    # 5-6 images
    "red": 0,       # <5 images
}

VIDEO_THRESHOLDS = {
    "green": 3,     # 3+ videos
    "yellow": 1,    # 1-2 videos
    "red": 0,       # 0 videos
}

# Product lifecycle stage thresholds by review count
LIFECYCLE_STAGES = {
    "new_launch": (0, 10),       # 0-30 days
    "growth": (10, 50),          # 30-90 days
    "mature": (50, 200),         # 90-180 days
    "decline": (200, 999999),    # 180+ days
}

# Dimension weights by lifecycle stage
LIFECYCLE_WEIGHTS = {
    "new_launch":  {"compliance": 5, "advertising": 4, "review": 2, "visual": 5, "content": 3},
    "growth":      {"compliance": 3, "advertising": 5, "review": 4, "visual": 3, "content": 4},
    "mature":      {"compliance": 2, "advertising": 4, "review": 5, "visual": 2, "content": 5},
    "decline":     {"compliance": 3, "advertising": 2, "review": 5, "visual": 2, "content": 3},
}

# Recommended fix order by lifecycle stage
LIFECYCLE_FIX_ORDER = {
    "new_launch":  ["compliance", "visual", "advertising", "content", "review"],
    "growth":      ["advertising", "review", "content", "compliance", "visual"],
    "mature":      ["review", "content", "advertising", "compliance", "visual"],
    "decline":     ["review", "compliance", "content", "advertising", "visual"],
}

# Related skills per dimension
DIMENSION_SKILLS = {
    "compliance": "miaoji-compliance-copy",
    "advertising": "miaoji-bid-guard",
    "review": "amazon-review-advisor",
    "visual": "miaoji-scene-studio",
    "content": "miaoji-video-script",
}


# ── Scoring Functions ────────────────────────────────────────────

def score_compliance(has_prohibited_words: bool, scene_word_coverage: float) -> dict:
    """Score compliance dimension (0-100)."""
    if has_prohibited_words:
        base = 15
    else:
        base = 60

    # Scene word coverage bonus (0-40 points)
    coverage_bonus = min(scene_word_coverage * 0.4, 40)

    score = base + coverage_bonus
    score = max(0, min(100, score))

    level = "red" if score < 50 else ("yellow" if score < 80 else "green")
    issues = []
    if has_prohibited_words:
        issues.append("Contains prohibited/marketing words — immediate removal required")
    if scene_word_coverage < 30:
        issues.append("Low scene-word coverage — Rufus search visibility may be weak")
    elif scene_word_coverage < 60:
        issues.append("Moderate scene-word coverage — add more usage scenario keywords")

    return {"score": round(score), "level": level, "issues": issues}


def score_advertising(acos: float) -> dict:
    """Score advertising dimension (0-100)."""
    if acos <= ACoS_THRESHOLDS["green"][1]:
        # 0-20% ACoS: 80-100 score
        score = 100 - (acos / 20) * 20
    elif acos <= ACoS_THRESHOLDS["yellow"][1]:
        # 20-30% ACoS: 50-79 score
        score = 80 - ((acos - 20) / 10) * 30
    else:
        # >30% ACoS: 0-49 score
        score = 50 - min(((acos - 30) / 20) * 50, 50)

    score = max(0, min(100, round(score)))
    level = "red" if score < 50 else ("yellow" if score < 80 else "green")

    issues = []
    if acos > 30:
        issues.append(f"ACoS {acos}% is critically high — set bid guardrails immediately")
    elif acos > 20:
        issues.append(f"ACoS {acos}% above target — optimize keyword bidding strategy")

    return {"score": score, "level": level, "issues": issues}


def score_review(negative_rate: float, review_count: int) -> dict:
    """Score review dimension (0-100)."""
    # Base score from negative rate
    if negative_rate <= NEGATIVE_RATE_THRESHOLDS["green"][1]:
        base = 90 - (negative_rate / 5) * 10
    elif negative_rate <= NEGATIVE_RATE_THRESHOLDS["yellow"][1]:
        base = 80 - ((negative_rate - 5) / 10) * 30
    else:
        base = 50 - min(((negative_rate - 15) / 20) * 50, 50)

    # Volume penalty: few reviews means higher risk
    if review_count < 10:
        volume_adj = -5
    elif review_count < 50:
        volume_adj = 0
    else:
        volume_adj = 5

    score = max(0, min(100, round(base + volume_adj)))
    level = "red" if score < 50 else ("yellow" if score < 80 else "green")

    issues = []
    if negative_rate > 15:
        issues.append(f"Negative review rate {negative_rate}% is critical — prioritize review management")
    elif negative_rate > 5:
        issues.append(f"Negative rate {negative_rate}% above benchmark — monitor review sentiment")
    if review_count < 10:
        issues.append("Very few reviews — accelerate review generation program")

    return {"score": score, "level": level, "issues": issues}


def score_visual(image_count: int, has_scene_shots: bool = None) -> dict:
    """Score visual dimension (0-100)."""
    # Image count base
    if image_count >= IMAGE_THRESHOLDS["green"]:
        base = 70
    elif image_count >= IMAGE_THRESHOLDS["yellow"]:
        base = 50
    else:
        base = 25

    # Scene shot bonus
    scene_bonus = 0
    if has_scene_shots is True:
        scene_bonus = 25
    elif has_scene_shots is None and image_count >= 6:
        scene_bonus = 15  # Assume some scene shots if 6+ images
    elif has_scene_shots is None and image_count >= 4:
        scene_bonus = 5

    # Image quality estimation
    completeness_bonus = min(image_count, 9) * 2  # Up to 18 points for 9 images

    score = base + scene_bonus + completeness_bonus
    score = max(0, min(100, round(score)))
    level = "red" if score < 50 else ("yellow" if score < 80 else "green")

    issues = []
    if image_count < 5:
        issues.append("Too few images — add more product and scene shots")
    if not has_scene_shots and image_count < 7:
        issues.append("No lifestyle/scene shots detected — add contextual imagery")

    return {"score": score, "level": level, "issues": issues}


def score_content(video_count: int) -> dict:
    """Score content dimension (0-100)."""
    if video_count >= VIDEO_THRESHOLDS["green"]:
        score = 90 + min(video_count - 3, 5) * 2  # 90-100
    elif video_count >= VIDEO_THRESHOLDS["yellow"]:
        score = 55 + (video_count * 15)  # 55-85
    else:
        score = 20

    score = max(0, min(100, round(score)))
    level = "red" if score < 50 else ("yellow" if score < 80 else "green")

    issues = []
    if video_count == 0:
        issues.append("No video content — generates video scripts to add coverage")
    elif video_count < 3:
        issues.append("Below recommended video count — add product demo and unboxing videos")

    return {"score": score, "level": level, "issues": issues}


def determine_lifecycle(review_count: int) -> str:
    """Determine product lifecycle stage from review count."""
    for stage, (low, high) in LIFECYCLE_STAGES.items():
        if low <= review_count < high:
            return stage
    return "decline"


def calculate_weighted_total(scores: dict, lifecycle: str) -> float:
    """Calculate weighted overall health score."""
    weights = LIFECYCLE_WEIGHTS[lifecycle]
    total_weight = sum(weights.values())
    weighted_sum = sum(scores[dim]["score"] * weights[dim] for dim in scores)
    return round(weighted_sum / total_weight, 1)


def generate_fix_plan(scores: dict, lifecycle: str) -> list:
    """Generate prioritized fix plan based on lifecycle stage and scores."""
    order = LIFECYCLE_FIX_ORDER[lifecycle]
    plan = []
    for dim in order:
        s = scores[dim]
        if s["level"] != "green":
            plan.append({
                "dimension": dim,
                "priority": len(plan) + 1,
                "level": s["level"],
                "score": s["score"],
                "skill": DIMENSION_SKILLS[dim],
                "issues": s["issues"],
            })
    # Add green items at the end as "maintain"
    for dim in order:
        if scores[dim]["level"] == "green":
            plan.append({
                "dimension": dim,
                "priority": len(plan) + 1,
                "level": "green",
                "score": scores[dim]["score"],
                "skill": DIMENSION_SKILLS[dim],
                "issues": [],
                "maintain": True,
            })
    return plan


def analyze(params: dict) -> dict:
    """Run full five-dimension analysis."""
    # Extract params with defaults
    asin = params.get("asin", "UNKNOWN")
    category = params.get("category", "unknown")
    acos = float(params.get("acos", 25))
    review_count = int(params.get("review_count", 0))
    negative_rate = float(params.get("negative_rate", 10))
    image_count = int(params.get("image_count", 5))
    video_count = int(params.get("video_count", 0))
    has_prohibited_words = params.get("has_prohibited_words", False)
    scene_word_coverage = float(params.get("scene_word_coverage", 50))
    has_scene_shots = params.get("has_scene_shots")  # None = unknown

    # Calculate scores
    scores = {
        "compliance": score_compliance(has_prohibited_words, scene_word_coverage),
        "advertising": score_advertising(acos),
        "review": score_review(negative_rate, review_count),
        "visual": score_visual(image_count, has_scene_shots),
        "content": score_content(video_count),
    }

    # Determine lifecycle
    lifecycle = determine_lifecycle(review_count)

    # Weighted total
    overall = calculate_weighted_total(scores, lifecycle)

    # Fix plan
    fix_plan = generate_fix_plan(scores, lifecycle)

    return {
        "asin": asin,
        "category": category,
        "lifecycle": lifecycle,
        "overall_score": overall,
        "scores": scores,
        "fix_plan": fix_plan,
        "timestamp": datetime.now().isoformat(),
    }


def format_report(result: dict) -> str:
    """Format analysis result as readable report."""
    level_emoji = {"green": "🟢", "yellow": "🟡", "red": "🔴"}
    lifecycle_cn = {
        "new_launch": "新品期(0-30天)",
        "growth": "成长期(30-90天)",
        "mature": "成熟期(90-180天)",
        "decline": "衰退期(180天+)",
    }

    lines = []
    lines.append("🏥 ASIN体检报告")
    lines.append("━" * 35)
    lines.append(f"产品：{result['asin']} / {result['category']}")
    lines.append(f"阶段：{lifecycle_cn.get(result['lifecycle'], result['lifecycle'])}")
    lines.append(f"综合健康指数：{result['overall_score']}/100")
    lines.append("")

    lines.append("📊 五维健康指数：")
    dim_cn = {
        "compliance": "合规度",
        "advertising": "广告度",
        "review": "评论度",
        "visual": "视觉度",
        "content": "内容度",
    }
    for dim, data in result["scores"].items():
        emoji = level_emoji.get(data["level"], "⚪")
        name = dim_cn.get(dim, dim)
        score_str = f"{emoji} {data['score']:3d}/100"
        issue_hint = f" — {data['issues'][0]}" if data["issues"] else ""
        lines.append(f"  {name}：{score_str}{issue_hint}")

    lines.append("")
    lines.append("🎯 修复优先级：")
    for item in result["fix_plan"]:
        if item.get("maintain"):
            lines.append(f"  ✅ {dim_cn[item['dimension']]}({item['score']}/100) — 维持")
        else:
            emoji = level_emoji.get(item["level"], "⚪")
            lines.append(f"  {item['priority']}️⃣ {dim_cn[item['dimension']]}{emoji} → {item['skill']}")

    lines.append("")
    lines.append("💊 紧急修复详情：")
    for item in result["fix_plan"][:2]:
        if item.get("maintain"):
            continue
        lines.append(f"")
        lines.append(f"【{item['priority']}】{dim_cn[item['dimension']]} {level_emoji.get(item['level'], '')}")
        lines.append(f"  → 推荐技能：{item['skill']}")
        for issue in item["issues"]:
            lines.append(f"  → 问题：{issue}")

    lines.append("")
    lines.append("━" * 35)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="ASIN Five-Dimension Health Analyzer")
    parser.add_argument("--asin", required=True, help="Product ASIN")
    parser.add_argument("--category", default="unknown", help="Product category")
    parser.add_argument("--acos", type=float, default=25, help="Current ACoS percentage")
    parser.add_argument("--review-count", type=int, default=0, help="Total review count")
    parser.add_argument("--negative-rate", type=float, default=10, help="Negative review percentage")
    parser.add_argument("--image-count", type=int, default=5, help="Number of listing images")
    parser.add_argument("--video-count", type=int, default=0, help="Number of listing videos")
    parser.add_argument("--has-prohibited-words", type=str, default="false", help="Contains prohibited words (true/false)")
    parser.add_argument("--scene-word-coverage", type=float, default=50, help="Scene word coverage 0-100")
    parser.add_argument("--has-scene-shots", type=str, default=None, help="Has scene/lifestyle shots (true/false/empty=unknown)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--input", type=str, help="JSON string with all parameters")

    args = parser.parse_args()

    # Parse input
    if args.input:
        params = json.loads(args.input)
    else:
        has_prohibited = args.has_prohibited_words.lower() == "true"
        has_scene = None
        if args.has_scene_shots is not None:
            has_scene = args.has_scene_shots.lower() == "true"

        params = {
            "asin": args.asin,
            "category": args.category,
            "acos": args.acos,
            "review_count": args.review_count,
            "negative_rate": args.negative_rate,
            "image_count": args.image_count,
            "video_count": args.video_count,
            "has_prohibited_words": has_prohibited,
            "scene_word_coverage": args.scene_word_coverage,
            "has_scene_shots": has_scene,
        }

    result = analyze(params)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_report(result))


if __name__ == "__main__":
    main()
