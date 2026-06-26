#!/usr/bin/env python3
"""
calculate_promotion.py — Compute final price after applying retail promotions

Usage:
    python3 calculate_promotion.py \
      --kb knowledge_base.json \
      --items '[{"sku":"SKU001","price":399,"qty":1},{"sku":"SKU002","price":259,"qty":1}]' \
      [--member-tier vip]

Output: JSON with itemized calculation and final total
"""

import json
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path


def get_active_promos(promos: list) -> list:
    today = datetime.now(timezone.utc).date().isoformat()
    active = []
    for p in promos:
        end = p.get("end_date")
        start = p.get("start_date", "2000-01-01")
        if start > today:
            continue
        if end and end < today:
            continue
        active.append(p)
    return active


def is_applicable(promo: dict, item_sku: str, item_category: str = "") -> bool:
    applicable_to = promo.get("applicable_to", [])
    excluded = promo.get("excluded", [])

    # Check exclusions first
    for ex in excluded:
        if ex in (item_sku, item_category, "全场"):
            return False

    # Check inclusions
    if not applicable_to or "全场" in applicable_to:
        return True
    return item_sku in applicable_to or item_category in applicable_to


def apply_threshold(promo: dict, subtotal: float) -> tuple[float, str]:
    """Apply 满X减Y or 满X打Y折 rule. Returns (discount_amount, description)."""
    rules_str = promo.get("rules", "")
    # Parse "满300减50" pattern
    import re
    m = re.search(r"满(\d+(?:\.\d+)?)减(\d+(?:\.\d+)?)", rules_str)
    if m:
        threshold = float(m.group(1))
        reduction = float(m.group(2))
        if subtotal >= threshold:
            return reduction, f"满{threshold:.0f}减{reduction:.0f}"
    # Parse "满X打Y折" pattern
    m = re.search(r"满(\d+(?:\.\d+)?)打(\d+(?:\.\d+)?)折", rules_str)
    if m:
        threshold = float(m.group(1))
        discount_rate = float(m.group(2)) / 10  # 8折 = 0.8
        if subtotal >= threshold:
            discount = round(subtotal * (1 - discount_rate), 2)
            return discount, f"满{threshold:.0f}打{m.group(2)}折"
    return 0.0, ""


def apply_discount(promo: dict, item_price: float) -> tuple[float, str]:
    """Apply percentage/rate discount to a single item."""
    import re
    rules_str = promo.get("rules", "")
    # "8折" pattern
    m = re.search(r"(\d+(?:\.\d+)?)折", rules_str)
    if m:
        rate = float(m.group(1)) / 10
        discount = round(item_price * (1 - rate), 2)
        return discount, f"{m.group(1)}折"
    # "X% off" pattern
    m = re.search(r"(\d+(?:\.\d+)?)%\s*(?:off|优惠)", rules_str, re.IGNORECASE)
    if m:
        rate = float(m.group(1)) / 100
        discount = round(item_price * rate, 2)
        return discount, f"{m.group(1)}% off"
    return 0.0, ""


def apply_member_discount(member_tier: str, subtotal: float, membership_config: dict) -> tuple[float, str]:
    """Apply membership tier discount."""
    if not member_tier or not membership_config:
        return 0.0, ""
    levels = membership_config.get("levels", [])
    for level in levels:
        if level.get("name", "").lower() == member_tier.lower():
            discount_rate = level.get("discount_rate", 1.0)
            if discount_rate < 1.0:
                discount = round(subtotal * (1 - discount_rate), 2)
                return discount, f"{level['name']}专属{round(discount_rate*10, 1)}折"
    return 0.0, ""


def calculate(items: list, promos: list, member_tier: str = "", membership_config: dict = None) -> dict:
    """
    items: [{"sku": str, "name": str, "price": float, "qty": int, "category": str}]
    Returns full calculation breakdown.
    """
    active_promos = get_active_promos(promos)
    line_items = []
    subtotal = 0.0

    for item in items:
        price = float(item.get("price", 0))
        qty = int(item.get("qty", 1))
        line_total = round(price * qty, 2)
        subtotal += line_total
        line_items.append({
            "sku": item.get("sku", ""),
            "name": item.get("name", item.get("sku", "")),
            "unit_price": price,
            "qty": qty,
            "line_total": line_total,
        })

    applied_promos = []
    total_discount = 0.0

    # Separate stackable and non-stackable promos
    stackable_promos = [p for p in active_promos if p.get("stackable", False)]
    nonstackable_promos = [p for p in active_promos if not p.get("stackable", False)]

    # Apply stackable promos first
    for promo in stackable_promos:
        ptype = promo.get("type", "")
        if ptype == "threshold":
            discount, desc = apply_threshold(promo, subtotal)
        elif ptype == "discount":
            discount, desc = apply_discount(promo, subtotal)
        else:
            continue
        if discount > 0:
            applied_promos.append({"promo": promo.get("title"), "rule": desc, "discount": discount})
            total_discount += discount

    # For non-stackable promos, pick the best one
    best_nonstackable = None
    best_discount = 0.0
    best_desc = ""
    for promo in nonstackable_promos:
        ptype = promo.get("type", "")
        if ptype == "threshold":
            discount, desc = apply_threshold(promo, subtotal)
        elif ptype == "discount":
            discount, desc = apply_discount(promo, subtotal)
        else:
            continue
        if discount > best_discount:
            best_discount = discount
            best_nonstackable = promo
            best_desc = desc

    if best_nonstackable and best_discount > 0:
        applied_promos.append({
            "promo": best_nonstackable.get("title"),
            "rule": best_desc,
            "discount": best_discount,
        })
        total_discount += best_discount

    # Apply member discount on post-promo subtotal
    # Only apply if not already applied via an explicit promo entry (avoid double-dip)
    member_promo_already_applied = any(
        "会员" in p.get("promo", "") or "member" in p.get("promo", "").lower()
        for p in applied_promos
    )
    post_promo = round(subtotal - total_discount, 2)
    member_discount, member_desc = (0.0, "") if member_promo_already_applied else apply_member_discount(
        member_tier, post_promo, membership_config or {}
    )
    if member_discount > 0:
        applied_promos.append({
            "promo": "会员专属折扣",
            "rule": member_desc,
            "discount": member_discount,
        })
        total_discount += member_discount

    final_total = max(0.0, round(subtotal - total_discount, 2))
    total_savings = round(subtotal - final_total, 2)

    return {
        "line_items": line_items,
        "subtotal": subtotal,
        "applied_promos": applied_promos,
        "total_discount": total_discount,
        "final_total": final_total,
        "total_savings": total_savings,
        "member_tier": member_tier or None,
        "currency": "CNY",
    }


def format_result(result: dict) -> str:
    """Human-readable Chinese summary."""
    lines = []
    for item in result["line_items"]:
        lines.append(f"  {item['name']} ×{item['qty']}   ¥{item['line_total']:.2f}")
    lines.append(f"  小计：¥{result['subtotal']:.2f}")
    lines.append("")
    if result["applied_promos"]:
        for p in result["applied_promos"]:
            lines.append(f"  ✨ {p['promo']}（{p['rule']}）  -¥{p['discount']:.2f}")
    else:
        lines.append("  暂无可用优惠")
    lines.append("")
    lines.append(f"  最终合计：¥{result['final_total']:.2f}")
    if result["total_savings"] > 0:
        lines.append(f"  节省：¥{result['total_savings']:.2f} 🎉")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Calculate retail promotion pricing")
    parser.add_argument("--kb", required=True, help="knowledge_base.json path")
    parser.add_argument("--items", required=True, help='JSON array of items')
    parser.add_argument("--member-tier", default="", help="Customer membership tier")
    parser.add_argument("--human", action="store_true", help="Print human-readable summary")
    args = parser.parse_args()

    kb = json.loads(Path(args.kb).read_text(encoding="utf-8"))
    items = json.loads(args.items)
    promos = kb.get("promotions", [])
    membership = kb.get("membership", {})

    result = calculate(items, promos, args.member_tier, membership)

    if args.human:
        print(format_result(result))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
