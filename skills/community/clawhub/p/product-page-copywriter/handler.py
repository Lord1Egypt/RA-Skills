#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Sequence


def _load_skill_meta() -> Dict[str, str]:
    skill_path = Path(__file__).with_name("SKILL.md")
    text = skill_path.read_text(encoding="utf-8")
    frontmatter = ""
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            frontmatter = parts[1]
            body = parts[2]

    data: Dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")

    title = data.get("name", Path(__file__).resolve().parent.name.replace("-", " ").title())
    for line in body.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return {
        "name": data.get("name", title),
        "title": title,
        "description": data.get("description", title),
    }


def _normalize_inputs(inputs: Any) -> str:
    if inputs is None:
        return ""
    if isinstance(inputs, str):
        return inputs.strip()
    if isinstance(inputs, dict):
        parts: List[str] = []
        for key, value in inputs.items():
            if value in (None, "", [], {}, ()):  # type: ignore[comparison-overlap]
                continue
            if isinstance(value, (list, tuple, set)):
                rendered = ", ".join(str(item) for item in value)
            else:
                rendered = str(value)
            parts.append(f"{key}: {rendered}")
        return " | ".join(parts)
    if isinstance(inputs, (list, tuple, set)):
        return " | ".join(str(item) for item in inputs)
    try:
        return json.dumps(inputs, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(inputs)


def _detect_many(text: str, rules: Dict[str, Sequence[str]], default: List[str], limit: int = 4) -> List[str]:
    lower = text.lower()
    found = [label for label, keywords in rules.items() if any(keyword in lower for keyword in keywords)]
    ordered: List[str] = []
    for item in found + default:
        if item not in ordered:
            ordered.append(item)
    return ordered[:limit]


def _detect_one(text: str, rules: Dict[str, Sequence[str]], default: str) -> str:
    lower = text.lower()
    for label, keywords in rules.items():
        if any(keyword in lower for keyword in keywords):
            return label
    return default


def _join(items: Sequence[str]) -> str:
    return ", ".join(items) if items else "Not specified"


PLATFORM_RULES = {
    "Tmall": ["tmall", "天猫"],
    "JD": ["jd", "jingdong", "京东"],
    "DTC / Shopify": ["shopify", "dtc", "independent site", "独立站"],
    "TikTok Shop": ["tiktok", "douyin", "抖音"],
    "Amazon": ["amazon"],
}

TONE_RULES = {
    "Compliant / cautious": ["compliance", "legal", "cautious", "conservative", "合规", "审核"],
    "Conversion-led": ["conversion", "sell", "performance", "转化", "成交"],
    "Brand-premium": ["premium", "brand", "high-end", "高端", "调性"],
    "Marketplace concise": ["concise", "marketplace", "简洁", "平台风格"],
}

AUDIENCE_RULES = {
    "Busy daily users": ["busy", "daily use", "everyday", "commute", "office", "通勤", "日常"],
    "Gift buyers": ["gift", "gifting", "送礼"],
    "Parents and families": ["parents", "family", "kids", "children", "家庭", "宝妈"],
    "Health-conscious shoppers": ["health", "fitness", "wellness", "健康"],
    "Value-driven shoppers": ["value", "budget", "save", "性价比", "省钱"],
}

ANGLE_RULES = {
    "Convenience / ease": ["easy", "portable", "simple", "convenient", "lightweight", "便捷", "轻便"],
    "Performance / outcome": ["performance", "effective", "powerful", "fast", "result", "效果", "高效"],
    "Safety / trust": ["safe", "certified", "tested", "trusted", "warranty", "安全", "认证"],
    "Style / premium feel": ["design", "premium", "sleek", "stylish", "质感", "高级"],
    "Value / bundle logic": ["bundle", "value", "save", "cost", "套装", "划算"],
    "Scenario fit": ["travel", "office", "home", "gym", "kitchen", "户外", "场景"],
}

RISK_RULES = {
    "Absolute or exaggerated claim risk": ["best", "guarantee", "100%", "perfect", "no.1", "顶级", "绝对"],
    "Efficacy or medical claim risk": ["medical", "therapy", "cure", "healing", "功效", "治疗", "改善"],
    "Children or sensitive-user risk": ["baby", "child", "pregnant", "儿童", "孕妇"],
    "Comparative substantiation risk": ["better than", "vs", "compare", "竞品", "领先"],
}

ANGLE_COPY = {
    "Convenience / ease": "easy everyday use",
    "Performance / outcome": "clear practical performance",
    "Safety / trust": "trust-building proof",
    "Style / premium feel": "premium product feel",
    "Value / bundle logic": "value that feels justified",
    "Scenario fit": "fit for real-life use moments",
}

AUDIENCE_COPY = {
    "Busy daily users": "busy everyday users",
    "Gift buyers": "gift-ready shoppers",
    "Parents and families": "families and parents",
    "Health-conscious shoppers": "health-conscious shoppers",
    "Value-driven shoppers": "value-focused shoppers",
}

PLATFORM_HINT = {
    "Tmall": "Tmall-ready merchandising language",
    "JD": "JD-friendly clarity and spec confidence",
    "DTC / Shopify": "DTC storytelling flow",
    "TikTok Shop": "TikTok Shop scannable hooks",
    "Amazon": "Amazon-style clarity and proof framing",
}


class ProductPageCopywriter:
    def __init__(self, user_input: Any):
        self.raw = user_input
        self.text = _normalize_inputs(user_input)
        self.lower = self.text.lower()
        self.platform = _detect_one(self.text, PLATFORM_RULES, "DTC / Shopify")
        self.tone = _detect_one(self.text, TONE_RULES, "Conversion-led")
        self.audiences = _detect_many(self.text, AUDIENCE_RULES, ["Busy daily users", "Value-driven shoppers"], limit=3)
        self.angles = _detect_many(
            self.text,
            ANGLE_RULES,
            ["Performance / outcome", "Convenience / ease", "Safety / trust"],
            limit=4,
        )
        self.risks = _detect_many(
            self.text,
            RISK_RULES,
            ["Absolute or exaggerated claim risk", "Comparative substantiation risk"],
            limit=3,
        )
        self.product_label = self._product_label()

    def _product_label(self) -> str:
        if isinstance(self.raw, dict):
            for key in ["product_name", "product", "name", "sku_name", "title"]:
                value = self.raw.get(key)
                if value:
                    return str(value)
            brand = self.raw.get("brand")
            category = self.raw.get("category") or self.raw.get("product_type")
            if brand and category:
                return f"{brand} {category}"
        return "[Brand/Product]"

    def _title_candidates(self) -> List[str]:
        audience = AUDIENCE_COPY.get(self.audiences[0], "everyday shoppers")
        angle_a = ANGLE_COPY[self.angles[0]]
        angle_b = ANGLE_COPY[self.angles[1]] if len(self.angles) > 1 else angle_a
        angle_c = ANGLE_COPY[self.angles[2]] if len(self.angles) > 2 else angle_b
        titles = [
            f"Version A: {self.product_label} | {angle_a} | {PLATFORM_HINT[self.platform]}",
            f"Version B: {self.product_label} for {audience} | {angle_b} without feature overload",
            f"Version C: {self.product_label} with {angle_c} and a {self.tone.lower()} finish",
        ]
        return titles

    def _hero_points(self) -> List[str]:
        points: List[str] = []
        for angle in self.angles[:3]:
            if angle == "Convenience / ease":
                points.append("Lead with the simplest daily-use benefit first, so the shopper understands the time or effort saved immediately.")
            elif angle == "Performance / outcome":
                points.append("Translate the strongest functional result into a clear user payoff instead of repeating technical specs without context.")
            elif angle == "Safety / trust":
                points.append("Show the proof source early, such as testing, certification, warranty, or support confidence, before making stronger claims.")
            elif angle == "Style / premium feel":
                points.append("Use premium cues carefully so the page feels elevated without sounding vague or inflated.")
            elif angle == "Value / bundle logic":
                points.append("Frame value as smart total-use value or bundle logic, not as cheapness alone.")
            else:
                points.append("Anchor the copy in a concrete use scenario so the shopper can picture where the product fits in real life.")
        return points

    def _page_structure(self) -> List[str]:
        return [
            "Module 1: Headline promise plus who the product helps and why it matters now.",
            "Module 2: Three proof-backed selling points ordered by user payoff, not internal spec priority.",
            "Module 3: Scenario or comparison block that helps the shopper understand fit, usage, and trust.",
            "Module 4: FAQ plus final close that removes the biggest hesitation before purchase.",
        ]

    def _faq_block(self) -> List[str]:
        return [
            "Common concern: Is the claimed benefit clearly supported by the facts we actually have?",
            "Proof to show: product specs, testing, warranty, user scenario clarity, or customer support reassurance.",
            f"Closing line: Invite purchase with confidence, but keep the promise inside a {self.tone.lower()} boundary.",
        ]

    def _compliance_notes(self) -> List[str]:
        notes = [
            "Replace absolute or category-leading language unless the team has documented proof.",
            "Flag any medical, efficacy, or highly sensitive claims for legal or platform review before publishing.",
        ]
        if self.platform in {"Tmall", "JD", "TikTok Shop"}:
            notes.append(f"Because the platform focus is {self.platform}, keep the first screen especially scannable and policy-safe.")
        for risk in self.risks:
            notes.append(f"Specific watchout: {risk}.")
        return notes[:5]

    def render(self) -> str:
        meta = _load_skill_meta()
        lines: List[str] = []
        lines.append("# Product Page Copy Pack")
        lines.append("")
        lines.append(f"**Skill description:** {meta['description']}")
        lines.append(f"**Product focus:** {self.product_label}")
        lines.append(f"**Platform focus:** {self.platform}")
        lines.append(f"**Copy tone:** {self.tone}")
        lines.append(f"**Audience cues:** {_join(self.audiences)}")
        lines.append(f"**Benefit angles:** {_join(self.angles)}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured product brief was provided, so this pack uses default ecommerce PDP assumptions.'}")
        lines.append("")
        lines.append("## Title Candidates")
        for title in self._title_candidates():
            lines.append(f"- {title}")
        lines.append("")
        lines.append("## Hero Selling Points")
        for idx, point in enumerate(self._hero_points(), 1):
            lines.append(f"{idx}. {point}")
        lines.append("")
        lines.append("## Page Structure")
        for item in self._page_structure():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## FAQ / Closing")
        for item in self._faq_block():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Compliance Watchouts")
        for note in self._compliance_notes():
            lines.append(f"- {note}")
        return "\n".join(lines)


def handle(user_input: Any) -> str:
    return ProductPageCopywriter(user_input).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
