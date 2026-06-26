#!/usr/bin/env python3
"""
今日菜单生成器 - 根据用户食材自动匹配菜谱并生成菜单方案。

用法:
    python scripts/generate_menu.py --ingredients "鸡翅,土豆,西红柿,鸡蛋"
    python scripts/generate_menu.py --ingredients "五花肉,冬瓜" --people 4 --style 家常
    python scripts/generate_menu.py --ingredients "鸡胸肉,黄瓜,西兰花" --style 清淡减脂
    python scripts/generate_menu.py --ingredients "里脊肉,豆腐" --style 川湘重口 --count 3
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional


# ── 菜谱数据 ──────────────────────────────────────────────────────────

RECIPES = [
    {
        "id": 1,
        "name": "红烧肉",
        "main_ingredients": ["五花肉"],
        "styles": ["家常"],
        "difficulty": 2,
        "time_minutes": 50,
        "serves": "2~3人",
    },
    {
        "id": 2,
        "name": "可乐鸡翅",
        "main_ingredients": ["鸡翅"],
        "styles": ["家常"],
        "difficulty": 1,
        "time_minutes": 25,
        "serves": "2人",
    },
    {
        "id": 3,
        "name": "番茄炒蛋",
        "main_ingredients": ["西红柿", "鸡蛋"],
        "styles": ["家常", "快手10分钟"],
        "difficulty": 1,
        "time_minutes": 10,
        "serves": "2人",
    },
    {
        "id": 4,
        "name": "酸辣土豆丝",
        "main_ingredients": ["土豆"],
        "styles": ["家常", "快手10分钟", "川湘重口"],
        "difficulty": 1,
        "time_minutes": 10,
        "serves": "2人",
    },
    {
        "id": 5,
        "name": "蒜蓉西兰花",
        "main_ingredients": ["西兰花"],
        "styles": ["家常", "快手10分钟", "清淡减脂"],
        "difficulty": 1,
        "time_minutes": 8,
        "serves": "2人",
    },
    {
        "id": 6,
        "name": "红烧排骨",
        "main_ingredients": ["排骨"],
        "styles": ["家常"],
        "difficulty": 2,
        "time_minutes": 60,
        "serves": "2~3人",
    },
    {
        "id": 7,
        "name": "麻婆豆腐",
        "main_ingredients": ["豆腐", "猪肉"],
        "styles": ["家常", "川湘重口"],
        "difficulty": 2,
        "time_minutes": 15,
        "serves": "2人",
    },
    {
        "id": 8,
        "name": "清炒空心菜",
        "main_ingredients": ["空心菜"],
        "styles": ["家常", "快手10分钟"],
        "difficulty": 1,
        "time_minutes": 5,
        "serves": "2人",
    },
    {
        "id": 9,
        "name": "清蒸鲈鱼",
        "main_ingredients": ["鲈鱼"],
        "styles": ["家常"],
        "difficulty": 2,
        "time_minutes": 20,
        "serves": "2~3人",
    },
    {
        "id": 10,
        "name": "冬瓜丸子汤",
        "main_ingredients": ["冬瓜", "猪肉"],
        "styles": ["家常"],
        "difficulty": 1,
        "time_minutes": 25,
        "serves": "2~3人",
    },
    {
        "id": 11,
        "name": "蒜蓉炒虾仁",
        "main_ingredients": ["虾"],
        "styles": ["快手10分钟"],
        "difficulty": 1,
        "time_minutes": 8,
        "serves": "2人",
    },
    {
        "id": 12,
        "name": "凉拌黄瓜",
        "main_ingredients": ["黄瓜"],
        "styles": ["快手10分钟"],
        "difficulty": 1,
        "time_minutes": 5,
        "serves": "2人",
    },
    {
        "id": 13,
        "name": "肥牛金针菇卷",
        "main_ingredients": ["肥牛", "金针菇"],
        "styles": ["快手10分钟"],
        "difficulty": 1,
        "time_minutes": 10,
        "serves": "2人",
    },
    {
        "id": 14,
        "name": "西红柿蛋花汤",
        "main_ingredients": ["西红柿", "鸡蛋"],
        "styles": ["快手10分钟", "清淡减脂"],
        "difficulty": 1,
        "time_minutes": 8,
        "serves": "2人",
    },
    {
        "id": 15,
        "name": "白灼虾",
        "main_ingredients": ["虾"],
        "styles": ["清淡减脂"],
        "difficulty": 1,
        "time_minutes": 10,
        "serves": "2人",
        "calories": "~200kcal",
    },
    {
        "id": 16,
        "name": "水煮鸡胸肉沙拉",
        "main_ingredients": ["鸡胸肉"],
        "styles": ["清淡减脂"],
        "difficulty": 1,
        "time_minutes": 15,
        "serves": "1人",
        "calories": "~300kcal",
    },
    {
        "id": 17,
        "name": "清蒸鳕鱼",
        "main_ingredients": ["鳕鱼"],
        "styles": ["清淡减脂"],
        "difficulty": 1,
        "time_minutes": 15,
        "serves": "1人",
        "calories": "~180kcal",
    },
    {
        "id": 18,
        "name": "辣子鸡",
        "main_ingredients": ["鸡腿", "鸡翅", "鸡肉"],
        "styles": ["川湘重口"],
        "difficulty": 2,
        "time_minutes": 25,
        "serves": "2~3人",
    },
    {
        "id": 19,
        "name": "水煮肉片",
        "main_ingredients": ["里脊肉", "猪肉"],
        "styles": ["川湘重口"],
        "difficulty": 2,
        "time_minutes": 20,
        "serves": "2~3人",
    },
    {
        "id": 20,
        "name": "剁椒鱼头",
        "main_ingredients": ["鳙鱼"],
        "styles": ["川湘重口"],
        "difficulty": 2,
        "time_minutes": 25,
        "serves": "2~3人",
    },
]

# 食材别名映射 → 标准名
ALIASES = {
    "番茄": "西红柿",
    "蕃茄": "西红柿",
    "洋柿子": "西红柿",
    "瘦肉": "猪肉",
    "前腿肉": "猪肉",
    "肉末": "猪肉",
    "肉馅": "猪肉",
    "猪里脊": "里脊肉",
    "小里脊": "里脊肉",
    "肥肠": "猪大肠",
    "猪手": "猪蹄",
    "猪脚": "猪蹄",
    "牛腱": "牛腱子",
    "肥牛卷": "肥牛",
    "肥牛片": "肥牛",
    "琵琶腿": "鸡腿",
    "大鸡腿": "鸡腿",
    "鸡翅中": "鸡翅",
    "翅中": "鸡翅",
    "凤爪": "鸡爪",
    "鸡胸": "鸡胸肉",
    "海鲈鱼": "鲈鱼",
    "基围虾": "虾",
    "大虾": "虾",
    "明虾": "虾",
    "虾仁": "虾",
    "龙虾": "小龙虾",
    "蛤蜊": "花甲",
    "蚬子": "花甲",
    "牡蛎": "生蚝",
    "海蛎子": "生蚝",
    "乌贼": "墨鱼",
    "章鱼": "八爪鱼",
    "小章鱼": "八爪鱼",
    "黄鱼": "黄花鱼",
    "鲑鱼": "三文鱼",
    "胖头鱼": "鳙鱼",
    "花鲢": "鳙鱼",
    "蛋": "鸡蛋",
    "老豆腐": "豆腐",
    "北豆腐": "豆腐",
    "内酯豆腐": "嫩豆腐",
    "南豆腐": "嫩豆腐",
    "豆腐干": "豆干",
    "香干": "豆干",
    "豆皮": "千张",
    "百叶": "千张",
    "大白菜": "白菜",
    "小白菜": "娃娃菜",
    "通菜": "空心菜",
    "蕹菜": "空心菜",
    "西芹": "芹菜",
    "芫荽": "香菜",
    "绿花菜": "西兰花",
    "花菜": "菜花",
    "白花菜": "菜花",
    "青瓜": "黄瓜",
    "凉瓜": "苦瓜",
    "马铃薯": "土豆",
    "淮山": "山药",
    "地瓜": "红薯",
    "番薯": "红薯",
    "红萝卜": "胡萝卜",
    "蒜头": "大蒜",
    "蒜": "大蒜",
    "姜": "生姜",
    "柿子椒": "青椒",
    "彩椒": "红椒",
    "藕": "莲藕",
    "冬菇": "香菇",
    "黑木耳": "木耳",
    "白木耳": "银耳",
    "昆布": "海带",
    "龙口粉丝": "粉丝",
    "红薯粉条": "粉条",
    "金针菜": "黄花菜",
    "白米": "大米",
    "黄小米": "小米",
    "江米": "糯米",
    "挂面": "面条",
    "手擀面": "面条",
    "中筋粉": "面粉",
    "赤小豆": "红豆",
}


def normalize_ingredient(name: str) -> str:
    """将用户输入的食材名标准化。"""
    name = name.strip()
    return ALIASES.get(name, name)


def match_recipes(user_ingredients: list[str], style: str | None = None) -> list[dict]:
    """根据用户食材和风格偏好匹配菜谱。

    返回按匹配度排序的菜谱列表，每个菜谱附带 match_score。
    """
    normalized = [normalize_ingredient(i) for i in user_ingredients]
    results = []

    for recipe in RECIPES:
        # 风格过滤
        if style and style not in recipe["styles"]:
            continue

        # 计算主料匹配度
        required = recipe["main_ingredients"]
        matched = sum(1 for r in required if r in normalized)

        if matched == 0:
            continue

        score = matched / len(required)  # 1.0 = 完全匹配
        missing = [r for r in required if r not in normalized]

        results.append({
            **recipe,
            "match_score": score,
            "missing_ingredients": missing,
        })

    # 按匹配度降序、难度升序排列
    results.sort(key=lambda x: (-x["match_score"], x["difficulty"]))
    return results


def categorize_ingredient(name: str) -> str:
    """判断食材类别。"""
    meat = {"猪肉", "五花肉", "排骨", "猪蹄", "里脊肉", "猪肝", "猪大肠",
            "牛肉", "牛腩", "牛腱子", "肥牛", "羊肉", "羊排",
            "鸡肉", "鸡腿", "鸡翅", "鸡爪", "鸡胸肉", "鸭肉", "鸭翅"}
    seafood = {"草鱼", "鲫鱼", "鲈鱼", "黑鱼", "黄骨鱼", "鲢鱼", "鳙鱼",
               "虾", "小龙虾", "螃蟹", "花甲", "扇贝", "生蚝",
               "鱿鱼", "墨鱼", "八爪鱼", "带鱼", "黄花鱼", "鳕鱼", "三文鱼"}
    egg_tofu = {"鸡蛋", "鸭蛋", "鹅蛋", "鹌鹑蛋",
                "豆腐", "嫩豆腐", "冻豆腐", "豆干", "千张", "腐竹"}
    vegs = {"白菜", "娃娃菜", "菠菜", "生菜", "油麦菜", "空心菜", "韭菜",
            "芹菜", "香菜", "茼蒿", "西兰花", "菜花", "黄瓜", "冬瓜",
            "南瓜", "丝瓜", "苦瓜", "茄子", "西红柿", "土豆", "山药",
            "红薯", "胡萝卜", "白萝卜", "洋葱", "大蒜", "生姜",
            "青椒", "红椒", "莲藕", "金针菇"}
    dried = {"香菇", "木耳", "银耳", "海带", "紫菜", "粉丝", "粉条", "黄花菜", "茶树菇"}
    staple = {"大米", "小米", "糯米", "玉米", "面条", "馒头", "面粉", "绿豆", "红豆", "花生"}

    n = normalize_ingredient(name)
    if n in meat:
        return "肉类"
    if n in seafood:
        return "水产海鲜"
    if n in egg_tofu:
        return "蛋类/豆制品"
    if n in vegs:
        return "蔬菜"
    if n in dried:
        return "干货/菌菇"
    if n in staple:
        return "主食杂粮"
    return "其他"


def generate_menu(
    user_ingredients: list[str],
    people: int = 2,
    style: str | None = None,
    count: int | None = None,
    time_limit: int | None = None,
) -> dict:
    """生成完整菜单方案。

    Args:
        user_ingredients: 用户手头的食材列表
        people: 就餐人数
        style: 口味偏好（家常/清淡减脂/快手10分钟/川湘重口）
        count: 期望菜品数量
        time_limit: 可用烹饪时间（分钟）

    Returns:
        包含推荐菜品、备菜清单、时间线的字典
    """
    if count is None:
        count = min(max(2, people), 4)  # 2~4 道菜

    # 匹配菜谱
    matched = match_recipes(user_ingredients, style)

    if not matched:
        return {
            "success": False,
            "message": "抱歉，根据你提供的食材暂时没有匹配的菜谱。",
            "user_ingredients": user_ingredients,
            "suggestions": "试试提供更多食材，或者换个口味风格？",
        }

    # 选菜策略：荤素搭配
    selected = []
    has_meat = False
    has_veg = False

    for recipe in matched:
        if len(selected) >= count:
            break

        # 时间限制
        if time_limit and recipe["time_minutes"] > time_limit:
            continue

        # 判断荤素
        is_meat = any(
            categorize_ingredient(i) in ("肉类", "水产海鲜")
            for i in recipe["main_ingredients"]
        )

        selected.append({**recipe, "is_meat": is_meat})
        if is_meat:
            has_meat = True
        else:
            has_veg = True

    # 如果只有荤或只有素，且还有余量，补充
    if len(selected) < count and selected:
        for recipe in matched:
            if recipe["id"] in [s["id"] for s in selected]:
                continue
            if len(selected) >= count:
                break

            is_meat = any(
                categorize_ingredient(i) in ("肉类", "水产海鲜")
                for i in recipe["main_ingredients"]
            )

            if (not has_veg and not is_meat) or (not has_meat and is_meat):
                selected.append({**recipe, "is_meat": is_meat})
                if is_meat:
                    has_meat = True
                else:
                    has_veg = True

    # 按耗时从长到短排列（烹饪时间线用）
    selected.sort(key=lambda x: -x["time_minutes"])

    total_time = max(r["time_minutes"] for r in selected) if selected else 0

    # 汇总食材清单
    all_ingredients = {}
    for recipe in selected:
        for ing in recipe["main_ingredients"]:
            cat = categorize_ingredient(ing)
            if cat not in all_ingredients:
                all_ingredients[cat] = []
            if ing not in all_ingredients[cat]:
                all_ingredients[cat].append(ing)

    return {
        "success": True,
        "people": people,
        "style": style or "家常",
        "estimated_time": total_time,
        "dishes": [
            {
                "id": r["id"],
                "name": r["name"],
                "difficulty": r["difficulty"],
                "time_minutes": r["time_minutes"],
                "serves": r["serves"],
                "match_score": r["match_score"],
                "missing_ingredients": r.get("missing_ingredients", []),
                "calories": r.get("calories"),
            }
            for r in selected
        ],
        "ingredient_summary": all_ingredients,
        "cooking_timeline": [
            {
                "order": i + 1,
                "dish": r["name"],
                "time_minutes": r["time_minutes"],
                "tip": "先开始（耗时最长）" if i == 0 else (
                    "可与上一道并行准备" if r["time_minutes"] <= 15 else "等前面的炖上后开始"
                ),
            }
            for i, r in enumerate(selected)
        ],
    }


def main():
    parser = argparse.ArgumentParser(
        description="今日菜单生成器 - 根据食材推荐菜谱"
    )
    parser.add_argument(
        "--ingredients", "-i",
        required=True,
        help="用户手头的食材，逗号分隔，如 '鸡翅,土豆,西红柿,鸡蛋'",
    )
    parser.add_argument(
        "--people", "-p",
        type=int,
        default=2,
        help="就餐人数 (默认 2)",
    )
    parser.add_argument(
        "--style", "-s",
        choices=["家常", "清淡减脂", "快手10分钟", "川湘重口"],
        default=None,
        help="口味风格偏好",
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=None,
        help="期望菜品数量 (默认根据人数自动)",
    )
    parser.add_argument(
        "--time", "-t",
        type=int,
        default=None,
        help="可用烹饪时间（分钟）",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="输出 JSON 文件路径（默认输出到 stdout）",
    )

    args = parser.parse_args()

    ingredients = [i.strip() for i in args.ingredients.split(",") if i.strip()]

    result = generate_menu(
        user_ingredients=ingredients,
        people=args.people,
        style=args.style,
        count=args.count,
        time_limit=args.time,
    )

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"菜单已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
