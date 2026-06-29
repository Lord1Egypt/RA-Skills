#!/usr/bin/env python3
"""
Grocery Price Comparer — compare prices across Hema, Dingdong, Meituan Maicai & Pupu.

Usage:
  python compare.py --list "猪肉500g, 西红柿3个, 鸡蛋一盒, 牛奶1L"
  python compare.py --list "牛腩800g, 西兰花2颗, 豆腐1盒" --platforms hema,dingdong
  python compare.py --help

MIT-0 License
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")
REF_DIR = os.path.join(os.path.dirname(__file__), "..", "references")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_schema(name):
    return load_json(os.path.join(SCHEMA_DIR, name))


def load_reference(name):
    return load_json(os.path.join(REF_DIR, name))


# ── Step 1: Parse Shopping List ────────────────────────────────────────────

UNIT_ALIASES = {
    "斤": 500, "jin": 500, "g": 1, "克": 1, "公斤": 1000, "kg": 1000,
    "个": None, "只": None, "盒": None, "袋": None, "包": None,
    "瓶": None, "箱": None, "把": None, "份": None, "杯": None, "条": None,
    "棵": None, "颗": None, "根": None, "升": None, "l": None, "ml": None,
    "件": None, "对": None,
}

PIECE_UNITS = {"个", "只", "盒", "袋", "包", "瓶", "箱", "把", "份",
               "杯", "条", "棵", "颗", "根", "件", "对", "枚", "罐", "桶"}


def infer_category(name):
    name_lower = name.lower()
    meat = ["肉", "猪", "牛", "羊", "鸡", "鸭", "鹅", "排", "腿", "翅", "骨", "肚", "肠", "肝", "meat", "beef", "pork", "chicken"]
    seafood = ["鱼", "虾", "蟹", "贝", "海鲜", "三文鱼", "基围虾", "fish", "shrimp"]
    veg = ["菜", "蔬", "叶", "番茄", "西红柿", "黄瓜", "萝卜", "土豆", "葱", "姜", "蒜", "椒", "豆", "菌", "菇", "笋", "vegetable", "veggie"]
    fruit = ["果", "apple", "banana", "orange", "grape", "水果", "莓", "蕉", "芒", "桃", "李", "杏", "瓜", "berry", "fruit"]
    dairy = ["牛奶", "奶", "酸奶", "奶酪", "蛋", "milk", "egg", "cheese", "yogurt", "dairy"]
    grain = ["米", "面", "粉", "粮", "面包", "rice", "noodle", "flour", "grain"]
    condiment = ["酱", "油", "醋", "盐", "糖", "料", "调味", "spice", "sauce"]
    beverage = ["水", "饮料", "酒", "茶", "咖啡", "drink", "water", "juice", "cola"]
    for kw in beverage:
        if kw in name_lower:
            return "Beverage"
    for kw in meat:
        if kw in name_lower:
            return "Meat"
    for kw in seafood:
        if kw in name_lower:
            return "Seafood"
    for kw in dairy:
        if kw in name_lower:
            return "Dairy & Eggs"
    for kw in fruit:
        if kw in name_lower:
            return "Fruit"
    for kw in veg:
        if kw in name_lower:
            return "Vegetable"
    for kw in grain:
        if kw in name_lower:
            return "Grains & Staples"
    for kw in condiment:
        if kw in name_lower:
            return "Condiment"
    return "Other"


def parse_shopping_list(raw_text):
    """Parse free-text shopping list into structured items.

    AI Prompt Template (used when LLM parsing is available):
      Extract structured items from the shopping list text.
      For each item, return: name (str), spec (str), quantity (int|float),
      preferred_unit (str), category (str).
    """
    items = []
    parts = [p.strip() for p in raw_text.replace("，", ",").split(",") if p.strip()]
    for part in parts:
        name = part
        spec = ""
        preferred_unit = ""
        quantity = 1
        # Pattern: leading number+unit, e.g. "500g猪肉"
        m = re.match(r"^([\d.]+)([^\d]+)", part)
        if m:
            q_val = float(m.group(1))
            unit_raw = m.group(2)
            remaining = part[len(m.group(0)):]
            name = remaining if remaining else name
            spec = m.group(0)
            preferred_unit = m.group(2).strip()
            quantity = q_val
        else:
            # Pattern: trailing number+unit, e.g. "猪肉500g"
            m2 = re.match(r"(.+?)([\d.]+)(g|斤|公斤|kg|ml|l|升|枚|个|只|盒|袋|包|瓶|箱|把|份|杯|条|棵|颗|根)", part)
            if m2:
                name = m2.group(1)
                q_val = float(m2.group(2))
                unit = m2.group(3)
                spec = f"{m2.group(2)}{unit}"
                preferred_unit = unit
                quantity = q_val

        if preferred_unit and preferred_unit.lower() in PIECE_UNITS:
            quantity = int(quantity) if quantity == int(quantity) else quantity
        elif preferred_unit in ("g", "克"):
            quantity = int(quantity)
        elif preferred_unit in ("kg", "公斤"):
            quantity = float(quantity)

        category = infer_category(name)
        items.append({
            "name": name,
            "spec": spec or "1份",
            "quantity": quantity,
            "preferred_unit": preferred_unit or "份",
            "category": category,
        })
    return items


# ── Step 2: Query Platforms (mock data) ─────────────────────────────────────

MOCK_PRICES = {
    "hema": {
        "猪肉": {"price": 29.9, "unit": "500g", "spec": "五花肉500g", "delivery": 6},
        "鸡蛋": {"price": 19.9, "unit": "30枚", "spec": "鲜鸡蛋30枚装", "delivery": 0},
        "牛奶": {"price": 13.8, "unit": "1L", "spec": "鲜牛奶1L", "delivery": 0},
        "西红柿": {"price": 5.9, "unit": "500g", "spec": "西红柿500g", "delivery": 0},
        "牛腩": {"price": 49.9, "unit": "500g", "spec": "牛腩500g", "delivery": 0},
        "豆腐": {"price": 3.5, "unit": "1盒", "spec": "嫩豆腐350g", "delivery": 0},
        "西兰花": {"price": 6.9, "unit": "1颗", "spec": "西兰花约300g", "delivery": 0},
        "青菜": {"price": 3.9, "unit": "250g", "spec": "上海青250g", "delivery": 0},
        "苹果": {"price": 9.9, "unit": "1kg", "spec": "红富士苹果1kg", "delivery": 0},
        "大米": {"price": 35.9, "unit": "5kg", "spec": "东北大米5kg", "delivery": 0},
        "五花肉": {"price": 29.9, "unit": "500g", "spec": "五花肉500g", "delivery": 0},
        "鸡胸肉": {"price": 15.8, "unit": "500g", "spec": "鸡胸肉500g", "delivery": 0},
        "黄瓜": {"price": 4.5, "unit": "500g", "spec": "黄瓜500g", "delivery": 0},
        "白菜": {"price": 2.9, "unit": "1颗", "spec": "大白菜约1.5kg", "delivery": 0},
        "香蕉": {"price": 6.9, "unit": "500g", "spec": "香蕉500g", "delivery": 0},
        "肥牛": {"price": 39.9, "unit": "500g", "spec": "澳洲肥牛卷500g", "delivery": 0},
        "肥羊": {"price": 42.9, "unit": "500g", "spec": "羊肉卷500g", "delivery": 0},
        "虾滑": {"price": 22.9, "unit": "200g", "spec": "虾滑200g", "delivery": 0},
        "丸子": {"price": 19.9, "unit": "500g", "spec": "火锅丸子500g", "delivery": 0},
        "三文鱼": {"price": 89.0, "unit": "500g", "spec": "三文鱼刺身", "delivery": 0},
        "基围虾": {"price": 39.9, "unit": "500g", "spec": "基围虾500g", "delivery": 0},
    },
    "dingdong": {
        "猪肉": {"price": 27.8, "unit": "500g", "spec": "猪五花500g", "delivery": 5},
        "鸡蛋": {"price": 18.9, "unit": "30枚", "spec": "鲜鸡蛋30枚", "delivery": 0},
        "牛奶": {"price": 12.9, "unit": "1L", "spec": "鲜牛奶1L", "delivery": 0},
        "西红柿": {"price": 5.5, "unit": "500g", "spec": "西红柿500g", "delivery": 0},
        "牛腩": {"price": 45.8, "unit": "500g", "spec": "牛腩块500g", "delivery": 0},
        "豆腐": {"price": 2.9, "unit": "1盒", "spec": "内酯豆腐350g", "delivery": 0},
        "西兰花": {"price": 5.9, "unit": "1颗", "spec": "西兰花1颗", "delivery": 0},
        "青菜": {"price": 3.5, "unit": "250g", "spec": "小青菜250g", "delivery": 0},
        "苹果": {"price": 8.9, "unit": "1kg", "spec": "苹果1kg", "delivery": 0},
        "大米": {"price": 32.9, "unit": "5kg", "spec": "东北珍珠米5kg", "delivery": 0},
        "五花肉": {"price": 27.8, "unit": "500g", "spec": "五花肉500g", "delivery": 0},
        "鸡胸肉": {"price": 14.5, "unit": "500g", "spec": "鸡大胸500g", "delivery": 0},
        "黄瓜": {"price": 3.9, "unit": "500g", "spec": "黄瓜500g", "delivery": 0},
        "白菜": {"price": 2.5, "unit": "1颗", "spec": "大白菜约1.5kg", "delivery": 0},
        "香蕉": {"price": 5.9, "unit": "500g", "spec": "香蕉500g", "delivery": 0},
        "肥牛": {"price": 36.8, "unit": "500g", "spec": "肥牛卷500g", "delivery": 0},
        "肥羊": {"price": 39.9, "unit": "500g", "spec": "羊肉卷500g", "delivery": 0},
        "虾滑": {"price": 21.8, "unit": "200g", "spec": "虾滑200g", "delivery": 0},
        "丸子": {"price": 18.5, "unit": "500g", "spec": "火锅丸子拼盘500g", "delivery": 0},
        "三文鱼": {"price": 85.0, "unit": "500g", "spec": "三文鱼刺身", "delivery": 0},
        "基围虾": {"price": 37.8, "unit": "500g", "spec": "基围虾500g", "delivery": 0},
    },
    "meituan": {
        "猪肉": {"price": 31.5, "unit": "500g", "spec": "猪五花500g", "delivery": 3},
        "鸡蛋": {"price": 20.5, "unit": "30枚", "spec": "谷物蛋30枚", "delivery": 0},
        "牛奶": {"price": 14.5, "unit": "1L", "spec": "鲜牛奶1L", "delivery": 0},
        "西红柿": {"price": 6.5, "unit": "500g", "spec": "西红柿500g", "delivery": 0},
        "牛腩": {"price": 48.0, "unit": "500g", "spec": "牛腩500g", "delivery": 0},
        "豆腐": {"price": 3.8, "unit": "1盒", "spec": "嫩豆腐350g", "delivery": 0},
        "西兰花": {"price": 7.5, "unit": "1颗", "spec": "西兰花300g", "delivery": 0},
        "青菜": {"price": 4.5, "unit": "250g", "spec": "青菜250g", "delivery": 0},
        "苹果": {"price": 10.9, "unit": "1kg", "spec": "冰糖心苹果1kg", "delivery": 0},
        "大米": {"price": 38.9, "unit": "5kg", "spec": "五常大米5kg", "delivery": 0},
        "肥牛": {"price": 42.0, "unit": "500g", "spec": "肥牛卷500g", "delivery": 0},
        "基围虾": {"price": 41.5, "unit": "500g", "spec": "基围虾500g", "delivery": 0},
    },
    "pupu": {
        "猪肉": {"price": 28.0, "unit": "500g", "spec": "猪五花500g", "delivery": 0},
        "鸡蛋": {"price": 18.5, "unit": "30枚", "spec": "鲜鸡蛋30枚", "delivery": 0},
        "牛奶": {"price": 12.5, "unit": "1L", "spec": "纯牛奶1L", "delivery": 0},
        "西红柿": {"price": 5.2, "unit": "500g", "spec": "西红柿500g", "delivery": 0},
        "牛腩": {"price": 46.5, "unit": "500g", "spec": "牛腩500g", "delivery": 0},
        "豆腐": {"price": 2.8, "unit": "1盒", "spec": "嫩豆腐350g", "delivery": 0},
        "西兰花": {"price": 5.5, "unit": "1颗", "spec": "西兰花", "delivery": 0},
        "青菜": {"price": 3.2, "unit": "250g", "spec": "上海青250g", "delivery": 0},
        "苹果": {"price": 8.5, "unit": "1kg", "spec": "苹果1kg", "delivery": 0},
        "大米": {"price": 33.9, "unit": "5kg", "spec": "东北大米5kg", "delivery": 0},
        "肥牛": {"price": 38.0, "unit": "500g", "spec": "肥牛卷500g", "delivery": 0},
    },
}

PLATFORM_NAMES = {
    "hema": "盒马 (Hema)",
    "dingdong": "叮咚买菜 (Dingdong)",
    "meituan": "美团买菜 (Meituan Maicai)",
    "pupu": "朴朴超市 (Pupu)",
}


def query_platform(item_name, platform, platforms_data):
    """Search for item on a platform.

    AI Prompt Template (for LLM-based semantic matching):
      Given item name: {item_name}, search product catalog on {platform}.
      Return best matching product with price, unit, spec, delivery fee.
    """
    name_lower = item_name.strip().lower()
    for key, data in platforms_data[platform].items():
        if key.lower() in name_lower or name_lower in key.lower():
            return {
                "platform": platform,
                "platform_name": PLATFORM_NAMES[platform],
                "item_name": key,
                **data,
            }
    return None


# ── Step 3: Unit Normalization ──────────────────────────────────────────────

UNIT_TO_GRAM = {
    "g": 1, "克": 1, "斤": 500, "jin": 500, "公斤": 1000, "kg": 1000,
    "毫升": 1, "ml": 1, "升": 1000, "l": 1000, "L": 1000,
}


def extract_unit_from_spec(spec):
    """Extract unit type from spec like '500g', '30枚', '1L'."""
    m = re.search(r"([\d.]+)\s*(g|克|斤|公斤|kg|KG|ml|升|L|l|个|只|盒|袋|包|瓶|箱|把|份|杯|条|棵|颗|根|枚|罐|桶)$", spec)
    if m:
        return m.group(2)
    m2 = re.search(r"([\d.]+)(g|克|斤|jin|公斤|kg|KG|ml|升|L|l|个|只|盒|袋|包|瓶|箱|把|份|杯|条|棵|颗|根|枚)", spec)
    if m2:
        return m2.group(2)
    for unit in PIECE_UNITS:
        if unit in spec:
            return unit
    return "份"


def extract_qty_from_spec(spec):
    """Extract numeric quantity from spec."""
    m = re.search(r"([\d.]+)", spec)
    return float(m.group(1)) if m else 1


def normalize_price(price, unit, spec):
    """Convert price to CNY/500g.

    AI Prompt Template:
      Normalize price: item costs {price} CNY per {unit} ({spec}).
      Convert to CNY/500g. Use: 1 jin = 500g, 1 kg = 1000g.
      For piece-count units, estimate grams from product description.
    """
    unit_type = extract_unit_from_spec(spec) if unit == "份" else unit
    if unit_type in UNIT_TO_GRAM:
        grams = extract_qty_from_spec(spec) * UNIT_TO_GRAM[unit_type]
        if grams == 0:
            grams = 500
        return round(price * 500 / grams, 2)
    elif unit_type in PIECE_UNITS:
        qty = extract_qty_from_spec(spec)
        return {
            "value": round(price / qty if qty > 0 else price, 2),
            "unit": f"per {unit_type}",
            "note": "piece-count, weight estimated",
        }
    return {"value": price, "unit": unit, "note": "could not normalize"}


# ── Step 4: Build Price Matrix ──────────────────────────────────────────────

def build_price_matrix(items, platforms, platforms_data):
    matrix = []
    for item in items:
        row = {"item": item["name"], "spec": item["spec"], "quantity": item["quantity"]}
        best_price = float("inf")
        best_platform = ""
        platform_prices = {}
        for p in platforms:
            result = query_platform(item["name"], p, platforms_data)
            if result:
                norm = normalize_price(result["price"], result["unit"], result["spec"])
                if isinstance(norm, dict):
                    display_price = '¥{:.2f} ({})'.format(norm["value"], norm["unit"])
                    price_val = norm["value"]
                else:
                    display_price = f"¥{norm}"
                    price_val = norm
                delivery = result.get("delivery", 0)
                platform_prices[p] = {
                    "price": price_val,
                    "display": display_price,
                    "spec": result["spec"],
                    "delivery": delivery,
                }
                if price_val < best_price:
                    best_price = price_val
                    best_platform = PLATFORM_NAMES.get(p, p)
            else:
                platform_prices[p] = None
        row["prices"] = platform_prices
        row["best"] = "{} (¥{:.2f})".format(best_platform, best_price) if best_price < float("inf") else "N/A"
        matrix.append(row)
    return matrix


# ── Step 5: Total Cost Calculation ──────────────────────────────────────────

def calculate_totals(matrix, platforms):
    totals = {}
    for p in platforms:
        total = 0.0
        delivery = 0
        for row in matrix:
            prices = row["prices"].get(p)
            if prices:
                total += prices["price"] * row["quantity"]
                delivery = max(delivery, prices.get("delivery", 0))
        if total > 0:
            totals[p] = {
                "subtotal": round(total, 2),
                "delivery": delivery,
                "total": round(total + delivery, 2),
            }
    return totals


# ── Steps 6-7: Analysis & Plan ──────────────────────────────────────────────

def analyze_tradeoffs(totals, matrix, platforms, platforms_data):
    if not totals:
        return {"error": "No valid totals to compare"}
    cheapest = min(totals, key=lambda p: totals[p]["total"])
    cheapest_total = totals[cheapest]["total"]

    split_total = 0.0
    split_plan = {}
    for row in matrix:
        best_p = min(
            [p for p in row["prices"] if row["prices"][p] is not None],
            key=lambda p: row["prices"][p]["price"],
            default=None,
        )
        if best_p:
            cost = row["prices"][best_p]["price"] * row["quantity"]
            if best_p not in split_plan:
                split_plan[best_p] = {"items": [], "cost": 0}
            split_plan[best_p]["items"].append(row["item"])
            split_plan[best_p]["cost"] += cost
            split_total += cost

    for p in split_plan:
        deliv = 0
        for row in matrix:
            prices = row["prices"].get(p)
            if prices:
                deliv = max(deliv, prices.get("delivery", 0))
                break
        split_plan[p]["cost"] = round(split_plan[p]["cost"], 2)
        split_plan[p]["delivery"] = deliv
        split_plan[p]["total"] = round(split_plan[p]["cost"] + deliv, 2)

    split_total_with_delivery = sum(v["total"] for v in split_plan.values())
    savings = round(cheapest_total - split_total_with_delivery, 2)

    recommendation = {
        "cheapest_single": {"platform": cheapest, "platform_name": PLATFORM_NAMES.get(cheapest, cheapest), "total": cheapest_total},
        "split_plan": None,
        "recommendation_label": "",
    }
    if savings > cheapest_total * 0.05:
        recommendation["split_plan"] = split_plan
        recommendation["split_total"] = round(split_total_with_delivery, 2)
        recommendation["savings_vs_single"] = savings
        recommendation["recommendation_label"] = "🔀 Split optimal"
    else:
        recommendation["recommendation_label"] = "🏷 Cheapest overall: " + PLATFORM_NAMES.get(cheapest, cheapest)
    return recommendation


def generate_procurement_plan(items, matrix, strategy, platforms):
    plan = {}
    if strategy.get("split_plan"):
        plan_data = strategy["split_plan"]
    else:
        single = strategy["cheapest_single"]["platform"]
        plan_data = {}
        plan_data[single] = {"items": [], "cost": 0, "delivery": 0}
        for row in matrix:
            p_row = row["prices"].get(single)
            if p_row:
                cost = p_row["price"] * row["quantity"]
                plan_data[single]["items"].append(row["item"])
                plan_data[single]["cost"] += cost
                plan_data[single]["delivery"] = max(plan_data[single]["delivery"], p_row.get("delivery", 0))
        for p in plan_data:
            plan_data[p]["cost"] = round(plan_data[p]["cost"], 2)
            plan_data[p]["total"] = round(plan_data[p]["cost"] + plan_data[p]["delivery"], 2)
    for p, data in plan_data.items():
        pname = PLATFORM_NAMES.get(p, p)
        plan[pname] = data
    return plan


# ── Display ─────────────────────────────────────────────────────────────────

def print_matrix(matrix):
    headers = ["Item", "Spec", "Qty"]
    pnames = ["hema", "dingdong", "meituan", "pupu"]
    for p in pnames:
        headers.append(PLATFORM_NAMES[p].split()[0])
    headers.append("Best")
    sep = "-" * (24 + 24 + 8 + 24 * 4 + 30)
    print("\n" + "=" * (24 + 24 + 8 + 24 * 4 + 30))
    print("  PRICE COMPARISON MATRIX".center(24 + 24 + 8 + 24 * 4 + 30))
    print("=" * (24 + 24 + 8 + 24 * 4 + 30))
    hdr = f"{'Item':<18} {'Spec':<18} {'Qty':<6}"
    for p in pnames:
        hdr += f" {PLATFORM_NAMES[p].split()[0]:<20}"
    hdr += f" {'Best':<25}"
    print(hdr)
    print("-" * (24 + 24 + 8 + 24 * 4 + 30))
    for row in matrix:
        line = f"{row['item']:<18} {row['spec']:<18} {row['quantity']:<6}"
        for p in pnames:
            pdata = row["prices"].get(p)
            line += f" {pdata['display']:<20}" if pdata else f" {'N/A':<20}"
        line += f" {row['best']:<25}"
        print(line)
    print("=" * (24 + 24 + 8 + 24 * 4 + 30))


def print_totals(totals):
    print(f"\n{'Platform':<30} {'Subtotal':<12} {'Delivery':<12} {'Total':<12}")
    print("-" * 66)
    for p, t in totals.items():
        pn = PLATFORM_NAMES.get(p, p)
        print(f"{pn:<30} ¥{t['subtotal']:<10.2f} ¥{t['delivery']:<10.2f} ¥{t['total']:<10.2f}")


def print_recommendation(strat):
    print(f"\n  Recommendation: {strat['recommendation_label']}")
    print(f"  Cheapest single platform: {strat['cheapest_single']['platform_name']} -> ¥{strat['cheapest_single']['total']:.2f}")
    if strat.get("split_plan"):
        print(f"  Split-order total: ¥{strat['split_total']:.2f} (saves ¥{strat['savings_vs_single']:.2f})")


def print_plan(plan):
    print("\n" + "=" * 60)
    print("  PROCUREMENT PLAN".center(60))
    print("=" * 60)
    for pname, data in plan.items():
        print(f"\n=== {pname} ===")
        if isinstance(data, dict) and "items" in data:
            for item in data["items"]:
                print(f"  - {item}")
            print(f"  Subtotal: ¥{data.get('cost', 0):.2f}")
            print(f"  Delivery: ¥{data.get('delivery', 0):.2f}")
            print(f"  Total:    ¥{data.get('total', 0):.2f}")
    print("=" * 60)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Grocery Price Comparer — compare prices across Hema, Dingdong, Meituan Maicai & Pupu",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list "猪肉500g, 西红柿3个, 鸡蛋一盒, 牛奶1L"
  %(prog)s --list "牛腩800g, 西兰花2颗, 豆腐1盒" --platforms hema,dingdong
  %(prog)s --list "苹果1kg, 大米5kg" --output json
  %(prog)s --validate-schemas
        """,
    )
    parser.add_argument("--list", "-l", default="", help="Shopping list (comma-separated)")
    parser.add_argument("--platforms", "-p", default="hema,dingdong,meituan,pupu", help="Platforms: hema,dingdong,meituan,pupu")
    parser.add_argument("--output", "-o", choices=["table", "json"], default="table", help="Output format")
    parser.add_argument("--validate-schemas", action="store_true", help="Validate schemas (dev mode)")

    args = parser.parse_args()

    if args.validate_schemas:
        try:
            load_schema("input.schema.json")
            load_schema("output.schema.json")
            print("  Schemas validated successfully")
            return 0
        except Exception as e:
            print(f"  Schema validation failed: {e}")
            return 1

    if not args.list and not args.validate_schemas:
        print("Error: --list is required for comparison. Use --validate-schemas for schema-only check.")
        print('Example: compare.py --list "猪肉500g, 西红柿3个"')
        return 1

    platforms = [p.strip() for p in args.platforms.split(",") if p.strip()]
    invalid = [p for p in platforms if p not in PLATFORM_NAMES]
    if invalid:
        print(f"  Unknown platforms: {invalid}. Valid: {', '.join(PLATFORM_NAMES.keys())}")
        return 1

    try:
        load_reference("categories.json")
        load_reference("platforms.json")
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    print(f"Grocery Price Comparer v1.0.0")
    print(f"Input: {args.list}")
    print(f"Platforms: {', '.join(PLATFORM_NAMES[p] for p in platforms)}")

    # Step 1
    print("\n[Step 1/8] Parsing shopping list...")
    items = parse_shopping_list(args.list)
    print(f"  -> {len(items)} items parsed:")
    for it in items:
        print(f"    - {it['name']} ({it['spec']}) x{it['quantity']} [{it['category']}]")

    # Steps 2-3
    print("\n[Step 2-3/8] Querying platforms & normalizing units...")
    platforms_data = {p: MOCK_PRICES.get(p, {}) for p in platforms}

    # Step 4
    print("\n[Step 4/8] Building price matrix...")
    matrix = build_price_matrix(items, platforms, platforms_data)
    if args.output == "table":
        print_matrix(matrix)
    else:
        print(json.dumps(matrix, ensure_ascii=False, indent=2))

    # Step 5
    print("\n[Step 5/8] Calculating total cost...")
    totals = calculate_totals(matrix, platforms)
    if args.output == "table":
        print_totals(totals)
    else:
        print(json.dumps(totals, ensure_ascii=False, indent=2))

    # Step 6
    print("\n[Step 6/8] Running trade-off analysis...")
    strategy = analyze_tradeoffs(totals, matrix, platforms, platforms_data)
    if args.output == "table":
        print_recommendation(strategy)
    else:
        print(json.dumps(strategy, ensure_ascii=False, indent=2))

    # Step 7
    print("\n[Step 7/8] Generating procurement plan...")
    plan = generate_procurement_plan(items, matrix, strategy, platforms)
    if args.output == "table":
        print_plan(plan)

    # Step 8
    print("\n[Step 8/8] Price alerts available (use --alert for setup)")

    if args.output == "json":
        output = {
            "version": "1.0.0",
            "input": {"shopping_list": args.list, "platforms": platforms},
            "parsed_items": items,
            "matrix": matrix,
            "totals": totals,
            "strategy": strategy,
            "procurement_plan": plan,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    print("\nComparison complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
