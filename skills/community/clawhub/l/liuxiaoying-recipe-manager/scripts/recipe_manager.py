#!/usr/bin/env python3
"""
Recipe Manager - 配方库与成本计算
数据存储：~/.openclaw_recipes.json
"""

import json
import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

DATA_FILE = Path.home() / ".openclaw_recipes.json"

def load_data():
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"next_id": 1, "recipes": []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def parse_price(price_str):
    """解析单价，支持“5元/斤” -> 0.01元/克"""
    price_str = price_str.strip().lower()
    if '元/斤' in price_str or '元每斤' in price_str:
        num = float(price_str.split('元')[0])
        return num / 500
    elif '元/克' in price_str:
        return float(price_str.split('元')[0])
    else:
        return float(price_str)

def add_recipe(name, version, ingredients_json, steps, serving_size=None):
    data = load_data()
    ingredients = json.loads(ingredients_json)
    total_cost = sum(i["grams"] * i["price_per_gram"] for i in ingredients)
    recipe = {
        "id": data["next_id"],
        "name": name,
        "version": version,
        "ingredients": ingredients,
        "steps": steps,
        "serving_size": serving_size,
        "cost_total": total_cost,
        "cost_per_gram": total_cost / sum(i["grams"] for i in ingredients) if ingredients else 0,
        "created_at": datetime.now().isoformat()
    }
    data["recipes"].append(recipe)
    data["next_id"] += 1
    save_data(data)
    return {"success": True, "recipe": recipe}

def list_recipes(name=None):
    data = load_data()
    recipes = data["recipes"]
    if name:
        recipes = [r for r in recipes if r["name"].lower() == name.lower()]
    return {"recipes": recipes}

def get_recipe(name, version=None):
    data = load_data()
    matched = [r for r in data["recipes"] if r["name"].lower() == name.lower()]
    if not matched:
        return None
    if version:
        matched = [r for r in matched if r["version"] == version]
    if not matched:
        return None
    matched.sort(key=lambda x: x["id"], reverse=True)
    return matched[0]

def delete_recipe(recipe_id):
    data = load_data()
    before = len(data["recipes"])
    data["recipes"] = [r for r in data["recipes"] if r["id"] != recipe_id]
    if len(data["recipes"]) < before:
        save_data(data)
        return {"success": True}
    return {"success": False, "error": "Recipe not found"}

def export_csv(output_path=None):
    import csv
    data = load_data()
    if not output_path:
        output_path = Path.home() / "recipes_export.csv"
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["配方名", "版本", "原料列表(克数,单价)", "做法步骤", "总成本(元)", "每克成本(元)", "每份克数", "创建时间"])
        for r in data["recipes"]:
            ingredients_str = "; ".join([f"{i['name']}:{i['grams']}g @{i['price_per_gram']:.3f}元/g" for i in r["ingredients"]])
            writer.writerow([
                r["name"], r["version"], ingredients_str, r["steps"],
                f"{r['cost_total']:.2f}", f"{r['cost_per_gram']:.4f}",
                r.get("serving_size", ""), r["created_at"]
            ])
    return {"success": True, "file_path": str(output_path)}

def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--version", default="v1")
    add_parser.add_argument("--ingredients", required=True)
    add_parser.add_argument("--steps", required=True)
    add_parser.add_argument("--serving-size", type=float, default=None)

    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--name", default=None)

    get_parser = subparsers.add_parser("get")
    get_parser.add_argument("--name", required=True)
    get_parser.add_argument("--version", default=None)

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", type=int, required=True)

    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--output", default=None)

    args = parser.parse_args()

    if args.command == "add":
        result = add_recipe(args.name, args.version, args.ingredients, args.steps, args.serving_size)
    elif args.command == "list":
        result = list_recipes(args.name)
    elif args.command == "get":
        recipe = get_recipe(args.name, args.version)
        result = {"success": recipe is not None, "recipe": recipe}
    elif args.command == "delete":
        result = delete_recipe(args.id)
    elif args.command == "export":
        result = export_csv(args.output)
    else:
        result = {"success": False, "error": "Unknown command"}

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
