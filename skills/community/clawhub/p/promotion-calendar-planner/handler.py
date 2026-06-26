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


WINDOW_RULES = {
    "Annual plan": ["annual", "year plan", "full year", "全年"],
    "Q1": ["q1", "first quarter"],
    "Q2": ["q2", "second quarter"],
    "Q3": ["q3", "third quarter"],
    "Q4": ["q4", "fourth quarter", "holiday season"],
    "Quarterly plan": ["quarter", "quarterly"],
    "Monthly sprint": ["month", "monthly", "30-day", "30 day", "4 weeks"],
}

GOAL_RULES = {
    "Inventory digestion": ["clearance", "aged stock", "inventory", "sell-through", "去库存", "清库存"],
    "Profit discipline": ["profit", "margin", "gross margin", "毛利", "利润"],
    "New-customer acquisition": ["new customer", "acquisition", "new users", "拉新"],
    "Member / retention": ["member", "vip", "retention", "repeat", "会员", "复购"],
    "Revenue growth": ["revenue", "gmv", "sales", "top line", "增长", "销量"],
}

ANCHOR_RULES = {
    "618": ["618"],
    "Prime Day": ["prime day"],
    "11.11": ["11.11", "singles day", "双11"],
    "Black Friday": ["black friday", "bfcm"],
    "Lunar New Year": ["lunar new year", "spring festival", "春节"],
    "Back-to-school": ["back to school"],
    "Summer push": ["summer", "暑期"],
    "Brand day": ["brand day", "anniversary", "店庆"],
}

RESOURCE_RULES = {
    "Operations": ["ops", "运营", "operations"],
    "Design": ["design", "creative", "设计"],
    "Supply chain": ["supply chain", "inventory", "procurement", "供应链", "备货"],
    "Customer service": ["customer service", "support", "客服"],
    "CRM / lifecycle": ["crm", "member", "email", "私域", "会员"],
    "Media / traffic": ["ads", "media", "traffic", "投放"],
}

HERO_CATEGORY_MAP = {
    "Revenue growth": "Hero conversion SKUs and proven best sellers",
    "Profit discipline": "High-margin core assortment and protected bundles",
    "Inventory digestion": "Aged stock, bundle candidates, and low-risk clearance items",
    "New-customer acquisition": "Entry-price products, trial bundles, and first-order magnets",
    "Member / retention": "VIP favorites, replenishment products, and member-only sets",
}

PRICE_STRATEGY_MAP = {
    "Revenue growth": "Use the strongest commercially proven offer, but keep one margin guardrail visible.",
    "Profit discipline": "Prefer moderate discounts, bundles, thresholds, or gifts instead of blanket markdowns.",
    "Inventory digestion": "Use planned clearance lanes so aged stock does not contaminate the full assortment narrative.",
    "New-customer acquisition": "Use a clear first-order hook without training the whole customer base to wait for deep discounts.",
    "Member / retention": "Use exclusivity, early access, or loyalty value before defaulting to the deepest public promotion.",
}


def _default_anchors(window: str) -> List[str]:
    defaults = {
        "Annual plan": ["Lunar New Year", "618", "11.11", "Black Friday"],
        "Q1": ["Lunar New Year", "Brand day", "Spring refresh"],
        "Q2": ["618", "Summer push", "Brand day"],
        "Q3": ["Back-to-school", "Summer push", "Brand day"],
        "Q4": ["11.11", "Black Friday", "Holiday gifting"],
        "Quarterly plan": ["Primary sale node", "Support node", "Retention node"],
        "Monthly sprint": ["Teaser week", "Main push", "Recovery week"],
    }
    return defaults.get(window, ["Primary sale node", "Support node", "Retention node"])


def _resource_defaults(goal: str) -> List[str]:
    base = ["Operations", "Design", "Supply chain", "Customer service"]
    if goal in {"Member / retention", "New-customer acquisition"}:
        base.append("CRM / lifecycle")
    if goal in {"Revenue growth", "New-customer acquisition"}:
        base.append("Media / traffic")
    return base[:5]


class PromotionCalendarPlanner:
    def __init__(self, user_input: Any):
        self.raw = user_input
        self.text = _normalize_inputs(user_input)
        self.lower = self.text.lower()
        self.window = _detect_one(self.text, WINDOW_RULES, "Quarterly plan")
        self.goal = _detect_one(self.text, GOAL_RULES, "Revenue growth")
        self.anchors = _detect_many(self.text, ANCHOR_RULES, _default_anchors(self.window), limit=4)
        self.resources = _detect_many(self.text, RESOURCE_RULES, _resource_defaults(self.goal), limit=5)

    def _calendar_rows(self) -> List[str]:
        roles = [
            "Demand preheat / positioning",
            "Main conversion push",
            "Bridge or follow-up wave",
            "Retention or cleanup wave",
        ]
        rows: List[str] = []
        for idx, anchor in enumerate(self.anchors):
            role = roles[idx] if idx < len(roles) else "Support wave"
            risk_note = "Watch workload concentration and discount overlap." if idx < 2 else "Check whether the follow-up wave still serves a distinct purpose."
            rows.append(
                f"| {anchor} | {role} | {HERO_CATEGORY_MAP[self.goal]} | {PRICE_STRATEGY_MAP[self.goal]} | {_join(self.resources[:3])} | {risk_note} |"
            )
        return rows

    def _cadence_principles(self) -> List[str]:
        return [
            "Before the major node, align hero categories, offer logic, and stock confidence before creative production scales.",
            "During the peak, keep one clear job for each node so acquisition, conversion, clearance, and retention are not all competing in the same week.",
            "After the peak, plan a lighter recovery or retention beat so customer service, fulfillment, and CRM do not collapse into reactive firefighting.",
        ]

    def _team_checklist(self) -> List[str]:
        return [
            "Operations: confirm channel readiness, coupon rules, and the node-by-node approval owner.",
            "Design: prepare hero assets early and avoid stacking every revision into the last week before launch.",
            "Supply chain: verify hero SKU availability, aged-stock lanes, and whether promo promises match actual inventory reality.",
            "Customer service: prepare scripts for offer clarity, delay handling, and predictable FAQ spikes.",
            "CRM / lifecycle: pre-build reminder, follow-up, and retention touchpoints for the highest-priority nodes.",
        ]

    def _conflict_watchlist(self) -> List[str]:
        conflicts = [
            "Do not run two major promotions so close together that design, support, and inventory teams cannot reset cleanly.",
            "Do not let a clearance wave and a premium hero launch share the same story unless the assortment split is explicit.",
        ]
        if self.goal == "Profit discipline":
            conflicts.append("Avoid chasing GMV at the cost of margin by repeating deep discounts without a profitability review.")
        elif self.goal == "Inventory digestion":
            conflicts.append("Do not let aged-stock clearance consume the entire calendar if hero SKUs still need a healthier brand narrative.")
        else:
            conflicts.append("Make sure acquisition-heavy nodes still have a retention or follow-up path so value does not end with the first order.")
        return conflicts

    def _assumptions(self) -> List[str]:
        return [
            "Official platform sale dates, policy changes, and merchandising rules should be re-verified before execution.",
            "This plan is a baseline operating rhythm, not a live campaign pacing dashboard.",
            "Discount depth, traffic budget, and launch approvals should remain human-approved.",
        ]

    def render(self) -> str:
        meta = _load_skill_meta()
        lines: List[str] = []
        lines.append("# Promotion Calendar Plan")
        lines.append("")
        lines.append(f"**Skill description:** {meta['description']}")
        lines.append(f"**Planning window:** {self.window}")
        lines.append(f"**Primary commercial goal:** {self.goal}")
        lines.append(f"**Seasonal anchors:** {_join(self.anchors)}")
        lines.append(f"**Cross-functional focus:** {_join(self.resources)}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured planning brief was provided, so this plan uses default ecommerce promotion-planning assumptions.'}")
        lines.append("")
        lines.append("## Calendar Recommendations")
        lines.append("| Month / node | Activity role | Hero category | Price strategy | Resource need | Risk note |")
        lines.append("|---|---|---|---|---|---|")
        lines.extend(self._calendar_rows())
        lines.append("")
        lines.append("## Cadence Principles")
        for bullet in self._cadence_principles():
            lines.append(f"- {bullet}")
        lines.append("")
        lines.append("## Team Preparation Checklist")
        for item in self._team_checklist():
            lines.append(f"- {item}")
        lines.append("")
        lines.append("## Conflict Watchlist")
        for idx, item in enumerate(self._conflict_watchlist(), 1):
            lines.append(f"{idx}. {item}")
        lines.append("")
        lines.append("## Assumptions and Limits")
        for note in self._assumptions():
            lines.append(f"- {note}")
        return "\n".join(lines)


def handle(user_input: Any) -> str:
    return PromotionCalendarPlanner(user_input).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
