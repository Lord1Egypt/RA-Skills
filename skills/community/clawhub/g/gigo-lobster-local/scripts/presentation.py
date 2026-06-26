from __future__ import annotations

import hashlib
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


def _resolve_public_url(template: str, ref_code: str, extras: dict[str, str] | None = None) -> str:
    value = str(template)
    if "{ref_code}" in value:
        return value.replace("{ref_code}", ref_code)

    parsed = urlparse(value)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    query.setdefault("ref_code", ref_code)
    for key, extra_value in (extras or {}).items():
        query.setdefault(key, extra_value)
    return urlunparse(parsed._replace(query=urlencode(query)))


DIMENSION_PROFILE = {
    "meat": {
        "icon": "🦞",
        "color": "#FF7A59",
        "tag": {"zh": "需求满足", "en": "Requirement fit"},
        "title": {"zh": "有效性", "en": "Execution"},
        "desc": {
            "zh": "你的龙虾能不能把事情做成，交付物靠不靠谱。",
            "en": "Whether the lobster can actually get the work done and deliver something reliable.",
        },
        "strong": {
            "zh": ["需求满足强", "指令遵循强", "成品感在线"],
            "en": ["Strong requirement fit", "Follows instructions", "Feels finished"],
        },
        "weak": {
            "zh": ["交付还不够稳", "需求命中率偏低", "需要更强的收尾"],
            "en": ["Delivery still wobbles", "Hits requirements less often", "Needs stronger finishing"],
        },
    },
    "brain": {
        "icon": "🧠",
        "color": "#FFD05A",
        "tag": {"zh": "调试能手", "en": "Debug sharp"},
        "title": {"zh": "脑力", "en": "Reasoning"},
        "desc": {
            "zh": "理解问题、拆解任务、定位 bug 和做判断的能力。",
            "en": "How well the lobster breaks down problems, diagnoses issues, and makes decisions.",
        },
        "strong": {
            "zh": ["拆题清楚", "定位准确", "判断稳"],
            "en": ["Breaks tasks down", "Diagnoses accurately", "Makes solid calls"],
        },
        "weak": {
            "zh": ["拆题不够稳", "容易漏边界", "判断还需加强"],
            "en": ["Breakdown can wobble", "Misses edge cases", "Judgment needs tightening"],
        },
    },
    "claw": {
        "icon": "🦀",
        "color": "#53D5FF",
        "tag": {"zh": "执行快手", "en": "Moves fast"},
        "title": {"zh": "动手", "en": "Hands-on"},
        "desc": {
            "zh": "真正写、改、串起多步骤流程时的执行表现。",
            "en": "How it performs when it actually has to write, edit, and complete multi-step work.",
        },
        "strong": {
            "zh": ["上手快", "多步任务稳", "执行链顺"],
            "en": ["Acts quickly", "Handles multi-step work", "Execution chain feels smooth"],
        },
        "weak": {
            "zh": ["动手偏慢", "复杂任务容易散", "执行链不够顺"],
            "en": ["Hands-on speed is slow", "Can scatter on complex work", "Execution chain feels uneven"],
        },
    },
    "shell": {
        "icon": "🛡️",
        "color": "#51E5A5",
        "tag": {"zh": "安全意识", "en": "Safety aware"},
        "title": {"zh": "安全性", "en": "Safety"},
        "desc": {
            "zh": "边界感、风险意识、守底线和兜底处理的能力。",
            "en": "Its sense of boundaries, risk awareness, and ability to handle edge cases safely.",
        },
        "strong": {
            "zh": ["权限边界强", "风险提示到位", "兜底处理稳"],
            "en": ["Strong guardrails", "Flags risk early", "Fallback handling is steady"],
        },
        "weak": {
            "zh": ["风险拒绝偏弱", "边界意识不足", "需要更稳的防护"],
            "en": ["Weak refusal behavior", "Boundaries are light", "Needs stronger protection"],
        },
    },
    "soul": {
        "icon": "👀",
        "color": "#FF8AF3",
        "tag": {"zh": "会聊天", "en": "Human-feel"},
        "title": {"zh": "拟人化", "en": "Warmth"},
        "desc": {
            "zh": "是不是像在和一个真人搭子交流，有没有温度和节奏感。",
            "en": "Whether it feels like talking to a real collaborator with warmth and rhythm.",
        },
        "strong": {
            "zh": ["沟通自然", "语气讨喜", "像个搭子"],
            "en": ["Conversational", "Pleasant tone", "Feels like a teammate"],
        },
        "weak": {
            "zh": ["有点生硬", "温度偏少", "互动感还不够"],
            "en": ["Feels stiff", "Low warmth", "Needs more human feel"],
        },
    },
    "cost": {
        "icon": "💸",
        "color": "#FFB83D",
        "tag": {"zh": "资源效率", "en": "Resource smart"},
        "title": {"zh": "性价比", "en": "Cost"},
        "desc": {
            "zh": "在完成目标的同时，会不会乱花 token、步骤和计算资源。",
            "en": "How efficiently it reaches the goal without overspending tokens, steps, or resources.",
        },
        "strong": {
            "zh": ["资源效率高", "步骤克制", "不会乱花 token"],
            "en": ["Resource efficient", "Lean steps", "Token-aware"],
        },
        "weak": {
            "zh": ["资源开销偏高", "步骤偏多", "还可以更省"],
            "en": ["Resource heavy", "Too many steps", "Can be leaner"],
        },
    },
    "speed": {
        "icon": "⏱️",
        "color": "#66D0FF",
        "tag": {"zh": "反应迅速", "en": "Fast finisher"},
        "title": {"zh": "效率", "en": "Speed"},
        "desc": {
            "zh": "从响应到收尾的整体速度，是否拖沓。",
            "en": "How quickly the lobster responds and reaches a usable finish.",
        },
        "strong": {
            "zh": ["反应利索", "推进够快", "不拖沓"],
            "en": ["Responsive", "Moves quickly", "No drag"],
        },
        "weak": {
            "zh": ["推进偏慢", "完成时间偏长", "节奏需要提速"],
            "en": ["Moves slowly", "Takes longer to finish", "Needs more pace"],
        },
    },
}

SKILL_RECOMMENDATIONS = {
    "meat": {
        "icon": "🍖",
        "name": {"zh": "交付加速包", "en": "Delivery Booster"},
        "desc": {
            "zh": "补足成品感和需求命中率，让龙虾交付更稳。",
            "en": "Tightens requirement fit and makes deliveries feel more finished.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
    "brain": {
        "icon": "🧠",
        "name": {"zh": "调试直觉", "en": "Debug Instinct"},
        "desc": {
            "zh": "强化拆题、诊断和判断，让大任务更不容易跑偏。",
            "en": "Strengthens diagnosis and judgment so bigger tasks drift less often.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
    "claw": {
        "icon": "🦀",
        "name": {"zh": "执行快手", "en": "Execution Sprint"},
        "desc": {
            "zh": "优化多步动作链路，让复杂任务推进更丝滑。",
            "en": "Improves multi-step execution so complex tasks flow more smoothly.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
    "shell": {
        "icon": "🛡️",
        "name": {"zh": "安全护甲 Pro", "en": "Safety Shield Pro"},
        "desc": {
            "zh": "补强边界感、危险拒绝和隐私处理，让龙虾出门更安心。",
            "en": "Reinforces guardrails, refusal behavior, and privacy handling.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
    "soul": {
        "icon": "👀",
        "name": {"zh": "人格魅力", "en": "Human Touch"},
        "desc": {
            "zh": "让表达更自然、更有温度、更像真人搭子。",
            "en": "Makes the lobster feel warmer, more natural, and more human.",
        },
        "badge": {"zh": "免费", "en": "Free"},
        "badge_type": "free",
    },
    "cost": {
        "icon": "💸",
        "name": {"zh": "资源节流术", "en": "Lean Mode"},
        "desc": {
            "zh": "减少 token 和步骤浪费，把资源花在更有价值的地方。",
            "en": "Cuts token waste and trims steps so resources go to what matters.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
    "speed": {
        "icon": "⏱️",
        "name": {"zh": "极速响应", "en": "Rapid Finish"},
        "desc": {
            "zh": "优化响应与收尾节奏，让端到端体感更利索。",
            "en": "Speeds up the full flow so the lobster feels snappier end to end.",
        },
        "badge": {"zh": "灰度测试中", "en": "Early access"},
        "badge_type": "gray",
    },
}

TIER_SEQUENCE = [
    {"key": "street_stall", "zh": "路边摊", "en": "Street Stall"},
    {"key": "night_market", "zh": "大排档", "en": "Night Market"},
    {"key": "restaurant", "zh": "青铜", "en": "Bronze"},
    {"key": "star_grade", "zh": "白银", "en": "Silver"},
    {"key": "michelin", "zh": "黄金", "en": "Gold"},
    {"key": "royal", "zh": "铂金", "en": "Platinum"},
    {"key": "legendary", "zh": "大师", "en": "Master"},
    {"key": "god_tier", "zh": "宗师", "en": "Grandmaster"},
]

TIER_THRESHOLDS = {
    "street_stall": 31,
    "night_market": 46,
    "restaurant": 56,
    "star_grade": 66,
    "michelin": 76,
    "royal": 85,
    "legendary": 92,
    "god_tier": 100,
}


def _sort_dimensions(dimensions: dict[str, int]) -> list[tuple[str, int]]:
    return sorted((dimensions or {}).items(), key=lambda item: item[1], reverse=True)


def derive_profile_tags(dimensions: dict[str, int], lang: str = "zh") -> list[str]:
    return [
        DIMENSION_PROFILE[key]["tag"][lang]
        for key, _score in _sort_dimensions(dimensions)[:4]
        if key in DIMENSION_PROFILE
    ]


def build_portrait_copy(dimensions: dict[str, int], lang: str = "zh") -> str:
    ordered = _sort_dimensions(dimensions)
    top = ordered[0] if ordered else ("meat", 0)
    second = ordered[1] if len(ordered) > 1 else ("brain", 0)
    lowest = ordered[-1] if ordered else ("speed", 0)

    top_label = DIMENSION_PROFILE.get(top[0], {}).get("title", {}).get(lang, top[0])
    second_label = DIMENSION_PROFILE.get(second[0], {}).get("title", {}).get(lang, second[0])
    weak_label = DIMENSION_PROFILE.get(lowest[0], {}).get("title", {}).get(lang, lowest[0])

    if lang == "en":
        return (
            f"A lobster that shines in {top_label.lower()} and {second_label.lower()}, "
            f"while still having room to tighten up its {weak_label.lower()}."
        )

    return f"一只在{top_label}和{second_label}上尤其亮眼的龙虾，不过{weak_label}还有继续补强的空间。"


def get_dimension_panels(dimensions: dict[str, int], lang: str = "zh") -> list[dict[str, object]]:
    ordered = []
    for key, score in _sort_dimensions(dimensions):
        profile = DIMENSION_PROFILE.get(key, {})
        if score >= 85:
            level = "强" if lang == "zh" else "Strong"
            level_key = "strong"
        elif score >= 65:
            level = "稳" if lang == "zh" else "Stable"
            level_key = "medium"
        elif score >= 45:
            level = "中" if lang == "zh" else "Mid"
            level_key = "medium"
        else:
            level = "弱" if lang == "zh" else "Needs work"
            level_key = "weak"

        ordered.append(
            {
                "key": key,
                "score": score,
                "icon": profile.get("icon", ""),
                "color": profile.get("color", "#FF7A59"),
                "title": profile.get("title", {}).get(lang, key),
                "description": profile.get("desc", {}).get(lang, ""),
                "badges": profile.get("strong" if score >= 70 else "weak", {}).get(lang, []),
                "level": level,
                "level_key": level_key,
            }
        )
    return ordered


def build_focus_items(dimensions: dict[str, int], lang: str = "zh") -> list[dict[str, object]]:
    weakest = list(reversed(_sort_dimensions(dimensions)))[:3]
    items: list[dict[str, object]] = []
    for index, (key, score) in enumerate(weakest, start=1):
        profile = DIMENSION_PROFILE.get(key, {})
        items.append(
            {
                "rank": index,
                "key": key,
                "score": score,
                "title": profile.get("title", {}).get(lang, key),
                "detail": profile.get("weak", {}).get(lang, [""])[0],
                "color": profile.get("color", "#FF7A59"),
                "icon": profile.get("icon", ""),
            }
        )
    return items


def build_skill_recommendations(dimensions: dict[str, int], lang: str = "zh") -> list[dict[str, object]]:
    weakest = list(reversed(_sort_dimensions(dimensions)))[:3]
    cards: list[dict[str, object]] = []
    for key, _score in weakest:
        skill = SKILL_RECOMMENDATIONS.get(key, {})
        profile = DIMENSION_PROFILE.get(key, {})
        cards.append(
            {
                "key": key,
                "icon": skill.get("icon", profile.get("icon", "")),
                "name": skill.get("name", {}).get(lang, key),
                "desc": skill.get("desc", {}).get(lang, ""),
                "badge": skill.get("badge", {}).get(lang, ""),
                "badge_type": skill.get("badge_type", "free"),
                "color": profile.get("color", "#FF7A59"),
            }
        )
    return cards


def get_tier_progress(score: int, tier_key: str, lang: str = "zh") -> dict[str, object]:
    current_index = max(0, next((i for i, item in enumerate(TIER_SEQUENCE) if item["key"] == tier_key), 0))
    current = TIER_SEQUENCE[current_index]
    next_step = TIER_SEQUENCE[min(len(TIER_SEQUENCE) - 1, current_index + 1)]
    gap = max(0, TIER_THRESHOLDS.get(tier_key, 100) - score)

    return {
        "current_label": current[lang],
        "next_label": next_step[lang],
        "gap": gap,
        "steps": [
            {
                "key": item["key"],
                "label": item[lang],
                "active": item["key"] == tier_key,
                "passed": index < current_index,
            }
            for index, item in enumerate(TIER_SEQUENCE)
        ],
    }


def build_public_metrics(upload_result: dict | None, ref_code: str, config: dict) -> dict[str, object]:
    site_home_url = str(config.get("site_home_url", "https://eval.agent-gigo.com/"))
    landing_home_url = str(config.get("landing_url", "https://eval.agent-gigo.com/r/?ref_code={ref_code}&source=cert"))
    rank = None
    total_entries = None
    surpassed_percent = None
    tracking_enabled = bool(upload_result and upload_result.get("success"))
    share_url = (
        _resolve_public_url(
            str(config.get("share_url_base", "https://eval.agent-gigo.com/r/?ref_code={ref_code}")),
            ref_code,
        )
        if tracking_enabled
        else site_home_url
    )

    if upload_result and upload_result.get("success"):
        rank = upload_result.get("rank")
        total_entries = upload_result.get("total_entries")
        if isinstance(rank, int) and isinstance(total_entries, int) and total_entries > 0:
            surpassed_percent = round(max(0.0, ((total_entries - rank) / total_entries) * 100), 1)

    landing_url = _resolve_public_url(landing_home_url, ref_code, {"source": "cert"}) if tracking_enabled else site_home_url

    return {
        "share_enabled": tracking_enabled,
        "share_url": share_url,
        "landing_url": landing_url,
        "landing_home_url": landing_home_url,
        "site_home_url": site_home_url,
        "rank": rank,
        "total_entries": total_entries,
        "surpassed_percent": surpassed_percent,
    }


def certificate_serial(ref_code: str) -> str:
    digest = hashlib.sha1(ref_code.encode("utf-8")).hexdigest()
    return f"{int(digest[:8], 16) % 1_000_000:06d}"
