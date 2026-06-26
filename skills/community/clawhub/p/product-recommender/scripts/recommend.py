#!/usr/bin/env python3
"""
recommend.py — Score and filter products for recommendations

Usage:
    python3 recommend.py --kb knowledge_base.json \
                          --intent '{"budget_max":500,"recipient":"mother","occasion":"birthday","preferences":["素色","轻便"]}' \
                          [--top 3] [--include-scores]

Output: JSON array of top recommended products with scores and reasons
"""

import json
import argparse
import re
from pathlib import Path

# ─── Tag mappings ──────────────────────────────────────────────────────────────

RECIPIENT_TAGS = {
    "mother":         ["妈妈", "母亲", "长辈", "女性", "40+"],
    "father":         ["爸爸", "父亲", "长辈", "男性", "40+"],
    "partner_female": ["女朋友", "老婆", "女性", "时尚"],
    "partner_male":   ["男朋友", "老公", "男性"],
    "elderly":        ["老人", "长辈", "60+", "简单易用"],
    "child":          ["小孩", "儿童", "安全", "可爱"],
    "friend":         ["朋友", "礼物", "通用"],
    "self":           [],
    "colleague":      ["实用", "大方", "通用"],
}

OCCASION_TAGS = {
    "birthday":    ["生日", "礼物", "送礼"],
    "wedding":     ["婚礼", "结婚", "喜庆"],
    "graduation":  ["毕业", "升学", "纪念"],
    "holiday":     ["节日", "送礼", "通用"],
    "formal":      ["正式", "通勤", "职场", "面试"],
    "casual":      ["日常", "休闲", "百搭"],
    "travel":      ["旅行", "出行", "轻便"],
    "sports":      ["运动", "健身", "户外"],
    "beach":       ["海边", "夏天", "度假"],
}


# ─── Scoring functions ─────────────────────────────────────────────────────────

def tokenize(text: str) -> set:
    if not text:
        return set()
    chinese = set(re.findall(r"[\u4e00-\u9fff]", str(text)))
    latin = set(w.lower() for w in re.findall(r"[a-zA-Z]+", str(text)))
    text_cn = re.sub(r"[^\u4e00-\u9fff]", "", str(text))
    bigrams = {text_cn[i:i+2] for i in range(len(text_cn)-1)} if len(text_cn) >= 2 else set()
    return chinese | latin | bigrams


def score_recipient(product: dict, recipient: str) -> float:
    if not recipient or recipient == "self":
        return 0.5  # neutral
    lookup_tags = RECIPIENT_TAGS.get(recipient, [])
    if not lookup_tags:
        return 0.5
    suitable = product.get("suitable_for", [])
    tags = product.get("tags", [])
    combined_tokens = tokenize(" ".join(suitable + tags))
    lookup_tokens = tokenize(" ".join(lookup_tags))
    if not lookup_tokens:
        return 0.5
    overlap = len(combined_tokens & lookup_tokens)
    return min(1.0, overlap / len(lookup_tokens))


def score_occasion(product: dict, occasion: str) -> float:
    if not occasion:
        return 0.5
    lookup_tags = OCCASION_TAGS.get(occasion, [])
    if not lookup_tags:
        return 0.5
    tags = product.get("tags", [])
    desc = product.get("description", "")
    combined_tokens = tokenize(" ".join(tags) + " " + desc)
    lookup_tokens = tokenize(" ".join(lookup_tags))
    if not lookup_tokens:
        return 0.5
    overlap = len(combined_tokens & lookup_tokens)
    return min(1.0, overlap / len(lookup_tokens))


def score_preferences(product: dict, preferences: list) -> float:
    if not preferences:
        return 0.5
    product_text = " ".join([
        product.get("name", ""),
        product.get("description", ""),
        " ".join(product.get("tags", [])),
        " ".join(product.get("suitable_for", [])),
    ])
    product_tokens = tokenize(product_text)
    pref_tokens = tokenize(" ".join(preferences))
    if not pref_tokens:
        return 0.5
    overlap = len(product_tokens & pref_tokens)
    return min(1.0, overlap / len(pref_tokens))


def score_popularity(product: dict, all_products: list) -> float:
    """Normalize sales_rank or use index position as proxy."""
    sales_rank = product.get("sales_rank")
    if sales_rank is not None:
        max_rank = max((p.get("sales_rank", 0) or 0) for p in all_products)
        if max_rank > 0:
            return 1.0 - (sales_rank / max_rank)
    # Fallback: use position in list (earlier = more popular)
    try:
        idx = all_products.index(product)
        return max(0.0, 1.0 - idx / len(all_products))
    except ValueError:
        return 0.3


def compute_score(product: dict, intent: dict, all_products: list) -> float:
    r = score_recipient(product, intent.get("recipient", ""))
    o = score_occasion(product, intent.get("occasion", ""))
    p = score_preferences(product, intent.get("preferences", []))
    pop = score_popularity(product, all_products)
    return round(r * 30 + o * 25 + p * 25 + pop * 20, 2)


# ─── Budget filtering ─────────────────────────────────────────────────────────

def get_effective_price(product: dict) -> float:
    sale = product.get("sale_price")
    if sale is not None:
        return float(sale)
    price = product.get("price")
    return float(price) if price is not None else float("inf")


def passes_budget(product: dict, intent: dict) -> bool:
    budget_max = intent.get("budget_max")
    budget_min = intent.get("budget_min")
    price = get_effective_price(product)
    if budget_max is not None and price > float(budget_max):
        return False
    if budget_min is not None and price < float(budget_min):
        return False
    return True


def passes_constraints(product: dict, constraints: list) -> bool:
    if not constraints:
        return True
    product_text = " ".join([
        product.get("name", ""),
        product.get("description", ""),
        " ".join(product.get("tags", [])),
    ]).lower()
    for constraint in constraints:
        if constraint.lower() not in product_text:
            return False
    return True


def passes_stock(product: dict) -> bool:
    qty = product.get("stock_qty")
    status = product.get("stock_status", "unknown")
    if status == "live_api":
        return True  # Live; assume available unless explicitly 0
    if qty is not None and qty == 0:
        return False
    return True


# ─── Reason generation ────────────────────────────────────────────────────────

def generate_reason(product: dict, intent: dict) -> str:
    parts = []
    recipient = intent.get("recipient")
    occasion = intent.get("occasion")
    preferences = intent.get("preferences", [])

    if recipient and recipient != "self":
        recipient_labels = {
            "mother": "妈妈", "father": "爸爸", "partner_female": "女朋友",
            "partner_male": "男朋友", "elderly": "老人", "child": "小孩",
            "friend": "朋友", "colleague": "同事",
        }
        parts.append(f"适合送给{recipient_labels.get(recipient, '对方')}")

    if occasion:
        occasion_labels = {
            "birthday": "生日礼物", "wedding": "婚礼贺礼", "formal": "正式场合",
            "casual": "日常穿搭", "travel": "旅行使用",
        }
        parts.append(occasion_labels.get(occasion, ""))

    if preferences:
        parts.append(f"符合{'/'.join(preferences[:2])}的需求")

    suitable = product.get("suitable_for", [])
    if suitable:
        parts.append(f"适用人群：{'、'.join(suitable[:2])}")

    return "；".join(p for p in parts if p) or "综合性价比推荐"


# ─── Main recommend function ──────────────────────────────────────────────────

def recommend(kb: dict, intent: dict, top: int = 3, relax_budget: bool = True) -> dict:
    products = kb.get("products", [])
    if not products:
        return {"recommendations": [], "message": "暂无商品数据，请先完成知识库导入。"}

    constraints = intent.get("constraints", [])

    # Hard filtering
    filtered = [
        p for p in products
        if passes_budget(p, intent)
        and passes_constraints(p, constraints)
        and passes_stock(p)
    ]

    # Relax budget if no results
    relaxed = False
    if not filtered and relax_budget and intent.get("budget_max"):
        relaxed_intent = dict(intent)
        relaxed_intent["budget_max"] = float(intent["budget_max"]) * 1.2
        filtered = [
            p for p in products
            if passes_budget(p, relaxed_intent)
            and passes_constraints(p, constraints)
            and passes_stock(p)
        ]
        relaxed = bool(filtered)

    if not filtered:
        # Last resort: top products ignoring budget/constraints
        filtered = products[:10]

    # Score and rank
    scored = []
    for product in filtered:
        score = compute_score(product, intent, products)
        scored.append({
            "score": score,
            "product": product,
            "reason": generate_reason(product, intent),
            "effective_price": get_effective_price(product),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    top_items = scored[:top]

    # Upsell check
    upsell = None
    budget_max = intent.get("budget_max")
    if budget_max and top_items:
        max_shown_price = max(i["effective_price"] for i in top_items)
        if max_shown_price < float(budget_max) * 0.8:
            upsell_budget = float(budget_max) * 1.2
            upsell_candidates = [
                p for p in products
                if float(budget_max) < get_effective_price(p) <= upsell_budget
                and passes_stock(p)
            ]
            if upsell_candidates:
                best_upsell = max(upsell_candidates, key=lambda p: compute_score(p, intent, products))
                upsell = {
                    "product": best_upsell,
                    "effective_price": get_effective_price(best_upsell),
                    "reason": generate_reason(best_upsell, intent),
                }

    return {
        "recommendations": top_items,
        "upsell": upsell,
        "relaxed_budget": relaxed,
        "total_eligible": len(filtered),
        "intent_used": intent,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Recommend products from knowledge base")
    parser.add_argument("--kb", required=True, help="knowledge_base.json path")
    parser.add_argument("--intent", required=True, help="JSON intent object")
    parser.add_argument("--top", type=int, default=3)
    parser.add_argument("--include-scores", action="store_true")
    args = parser.parse_args()

    kb = json.loads(Path(args.kb).read_text(encoding="utf-8"))
    intent = json.loads(args.intent)
    result = recommend(kb, intent, args.top)

    if not args.include_scores:
        for item in result["recommendations"]:
            item.pop("score", None)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
