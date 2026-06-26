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


OBJECTIVE_RULES = {
    "Stockout prevention": ["stockout", "out of stock", "缺货", "断货", "replenish", "补货", "hero sku", "hot seller", "fast seller"],
    "Aging cleanup": ["aged", "aging", "滞销", "dead stock", "clearance", "slow mover", "slow-moving", "overstock"],
    "Promo readiness": ["promo", "campaign", "活动", "大促", "618", "11.11", "launch", "peak season", "seasonal push"],
    "Cash discipline": ["cash", "working capital", "资金", "inventory amount", "holding cost", "capital"],
}

SIGNAL_RULES = {
    "Inventory on hand": ["inventory", "stock", "库存", "on hand", "units", "qty"],
    "Sales velocity": ["sales", "销量", "velocity", "sell-through", "sell through", "gmv", "orders"],
    "Lead time / replenishment": ["lead time", "supplier", "arrival", "purchase order", "procurement", "补货", "采购", "到货"],
    "Campaign plan": ["promo", "campaign", "活动", "大促", "618", "11.11", "launch", "peak"],
    "Seasonality / category": ["season", "seasonal", "类目", "category", "tag", "collection", "季节"],
}

RISK_KEYWORDS = {
    "Stockout risk": ["stockout", "out of stock", "缺货", "断货", "lead time", "hot seller", "hero sku"],
    "Aging / overstock risk": ["aged", "aging", "滞销", "overstock", "slow mover", "dead stock", "clearance"],
    "Capital lock-up": ["cash", "capital", "holding cost", "inventory amount", "资金", "occupy cash"],
    "Structural imbalance": ["mix", "structure", "结构", "long tail", "long-tail", "category balance", "assortment"],
    "Promo readiness gap": ["promo", "campaign", "活动", "大促", "618", "11.11", "launch"],
}

PRIORITY_ORDERS = {
    "Stockout prevention": ["Stockout risk", "Promo readiness gap", "Structural imbalance", "Aging / overstock risk"],
    "Aging cleanup": ["Aging / overstock risk", "Capital lock-up", "Structural imbalance", "Stockout risk"],
    "Promo readiness": ["Promo readiness gap", "Stockout risk", "Structural imbalance", "Aging / overstock risk"],
    "Cash discipline": ["Capital lock-up", "Aging / overstock risk", "Structural imbalance", "Stockout risk"],
}

RISK_LIBRARY = {
    "Stockout risk": {
        "inspect": "Days of cover, top-SKU velocity, supplier lead time, and whether hero demand already outpaces inbound supply.",
        "action": "Expedite replenishment, protect stock exposure, or shift demand into substitutes before the gap becomes customer-visible.",
    },
    "Aging / overstock risk": {
        "inspect": "Slow sell-through, aging buckets, markdown history, and whether inventory is stacking inside low-demand variants.",
        "action": "Freeze rebuys, build a clearance or bundle lane, and reduce low-conviction stock before it drags the next cycle.",
    },
    "Capital lock-up": {
        "inspect": "Inventory amount tied in slow or low-margin SKUs versus how much cash is protected by hero and core lines.",
        "action": "Pause discretionary purchasing and redirect working capital toward faster, cleaner inventory turns.",
    },
    "Structural imbalance": {
        "inspect": "The balance between hero, core, seasonal, and long-tail SKUs, plus whether category mix reflects current demand.",
        "action": "Rebalance future buys, simplify weak tails, and stop letting low-value assortment complexity crowd out priority stock.",
    },
    "Promo readiness gap": {
        "inspect": "Promo SKU demand, inbound timing, warehouse readiness, and whether featured products have enough protected stock.",
        "action": "Lock a promo stock plan, narrow the hero SKU list, and align campaign promises to credible available inventory.",
    },
}


class InventoryHealthAuditor:
    def __init__(self, user_input: Any):
        self.raw = user_input
        self.text = _normalize_inputs(user_input)
        self.lower = self.text.lower()
        self.objective = _detect_one(self.text, OBJECTIVE_RULES, "Stockout prevention")
        self.signals = _detect_many(
            self.text,
            SIGNAL_RULES,
            ["Inventory on hand", "Sales velocity", "Lead time / replenishment"],
            limit=5,
        )
        self.risks = self._priority_risks()

    def _priority_risks(self) -> List[str]:
        defaults = PRIORITY_ORDERS[self.objective]
        return _detect_many(self.text, RISK_KEYWORDS, defaults, limit=4)

    def _action_plan(self) -> List[str]:
        plan_map = {
            "Stockout prevention": [
                "Week 1: isolate the hero SKUs with the thinnest days of cover and confirm inbound reality instead of planned inbound only.",
                "Week 2: protect demand by limiting exposure, swapping substitutes, or prioritizing the cleanest replenishment path.",
                "Weeks 3-4: rebalance future purchasing so the next cycle does not repeat the same shortage pattern.",
            ],
            "Aging cleanup": [
                "Week 1: rank aged and slow-moving SKUs by cash tied up, not just by unit count.",
                "Week 2: launch the simplest recovery move first, such as bundle, markdown lane, or purchase freeze.",
                "Weeks 3-4: remove repeat causes by tightening assortment and reducing weak replenishment habits.",
            ],
            "Promo readiness": [
                "Week 1: confirm the promo hero list, inbound timing, and which SKUs should be protected versus deprioritized.",
                "Week 2: align campaign promises, warehouse capacity, and stock allocation before traffic ramps.",
                "Weeks 3-4: monitor the featured assortment separately so promo demand does not hide broader imbalance.",
            ],
            "Cash discipline": [
                "Week 1: map where cash is trapped across slow, low-margin, or structurally weak SKUs.",
                "Week 2: stop low-conviction purchases and prioritize actions that convert trapped stock into usable working capital.",
                "Weeks 3-4: reset the buy logic so cash goes first to cleaner turns and higher-confidence inventory positions.",
            ],
        }
        return plan_map[self.objective]

    def _assumptions(self) -> List[str]:
        notes = [
            "This report is heuristic and should be treated as an operator-facing decision brief, not a live planning system.",
            "Final replenishment volume, purchase orders, and markdown decisions should remain human-approved.",
        ]
        missing = [
            signal
            for signal in ["Sales velocity", "Lead time / replenishment", "Campaign plan"]
            if signal not in self.signals
        ]
        if missing:
            notes.append(f"Signals that appear missing or only lightly referenced: {_join(missing)}.")
        if "Seasonality / category" not in self.signals:
            notes.append("If seasonality is material, re-check the output before treating slow movement as true structural weakness.")
        return notes

    def render(self) -> str:
        meta = _load_skill_meta()
        lines: List[str] = []
        lines.append("# Inventory Health Audit Report")
        lines.append("")
        lines.append(f"**Skill description:** {meta['description']}")
        lines.append(f"**Primary objective:** {self.objective}")
        lines.append(f"**Signals referenced:** {_join(self.signals)}")
        lines.append(f"**Priority lenses:** {_join(self.risks)}")
        lines.append(f"**Input snapshot:** {self.text or 'No structured inventory notes were provided, so this report uses default weekly inventory-review assumptions.'}")
        lines.append("")
        lines.append("## Overview")
        lines.append("- Treat inventory health as a balance among service level, cash discipline, and demand readiness, not as a pure stock-quantity question.")
        lines.append(f"- Because the main objective is **{self.objective.lower()}**, the first action should target the smallest number of SKUs that create the largest operational or cash consequence.")
        lines.append("- Separate hero, core, seasonal, and long-tail logic before making any broad purchase or clearance decision.")
        lines.append("")
        lines.append("## Priority Queue")
        lines.append("| Priority | Risk type | What to inspect now | Recommended action |")
        lines.append("|---|---|---|---|")
        for idx, risk in enumerate(self.risks, 1):
            details = RISK_LIBRARY[risk]
            lines.append(f"| {idx} | {risk} | {details['inspect']} | {details['action']} |")
        lines.append("")
        lines.append("## 30-Day Action Plan")
        for idx, step in enumerate(self._action_plan(), 1):
            lines.append(f"{idx}. {step}")
        lines.append("")
        lines.append("## Assumptions and Limits")
        for note in self._assumptions():
            lines.append(f"- {note}")
        return "\n".join(lines)


def handle(user_input: Any) -> str:
    return InventoryHealthAuditor(user_input).render()


if __name__ == "__main__":
    payload = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()
    print(handle(payload))
