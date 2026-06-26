#!/usr/bin/env python3
"""
宠物大全查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询宠物基本信息和详情

用法:
    python pet_query.py 哈士奇
    python pet_query.py --category dog
    python pet_query.py --detail 哈士奇

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python pet_query.py --key your_api_key ...
    2. 环境变量：export JUHE_PET_QUERY_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_PET_QUERY_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/755
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

SEARCH_API_URL = "https://apis.juhe.cn/fapigx/pet/search"
DETAIL_API_URL = "https://apis.juhe.cn/fapigx/pet/detail"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/755"

# 类别映射
CATEGORY_NAMES = {
    "dog": "狗狗",
    "cat": "猫咪",
    "shuizi": "水族",
    "xiaochong": "小宠",
    "pachong": "爬虫",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_PET_QUERY_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_PET_QUERY_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def search_pets(query: str = None, category: str = None, page: int = 1, page_size: int = 10, api_key: str = None) -> dict:
    """搜索宠物"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "page": page,
        "page_size": page_size,
    }
    if query:
        params["q"] = query
    if category:
        params["category"] = category

    data = urllib.parse.urlencode(params).encode("utf-8")
    url = f"{SEARCH_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "data": res.get("data", []),
            "total_count": res.get("total_count", 0),
            "page": res.get("page", 1),
            "page_size": res.get("page_size", page_size),
            "total_page": res.get("total_page", 1),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"
    elif error_code == 275500:
        hint = "（网络异常）"
    elif error_code == 275501:
        hint = "（参数为空）"
    elif error_code == 275502:
        hint = "（参数错误）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def get_pet_detail(hash_id: str, api_key: str = None) -> dict:
    """获取宠物详情"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    params = {
        "key": api_key,
        "hash_id": hash_id,
    }
    url = f"{DETAIL_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "data": res,
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_pet_brief(pet: dict, index: int = 0) -> str:
    """格式化宠物简要信息"""
    lines = []
    name = pet.get("name", "未知")
    category = pet.get("category", "")
    category_name = CATEGORY_NAMES.get(category, category)

    lines.append(f"#{index + 1} {name}")
    if category_name:
        lines.append(f"   类别：{category_name}")

    alias = pet.get("alias", "")
    if alias:
        lines.append(f"   别名：{alias}")

    origin = pet.get("origin", "")
    if origin:
        lines.append(f"   产地：{origin}")

    weight = pet.get("weight", "")
    if weight:
        lines.append(f"   体重：{weight}")

    height = pet.get("height", "")
    if height:
        lines.append(f"   身高：{height}")

    life_span = pet.get("life_span", "")
    if life_span:
        lines.append(f"   寿命：{life_span}")

    tags = pet.get("tags", "")
    if tags:
        lines.append(f"   特征：{tags}")

    return "\n".join(lines)


def format_pet_detail(pet: dict) -> str:
    """格式化宠物详情"""
    lines = []
    name = pet.get("name", "未知")
    category = pet.get("category", "")
    category_name = CATEGORY_NAMES.get(category, category)

    lines.append(f"🐾 {name} 详情")
    lines.append("")
    lines.append(f"类别：{category_name}")

    alias = pet.get("alias", "")
    if alias:
        lines.append(f"别名：{alias}")

    origin = pet.get("origin", "")
    if origin:
        lines.append(f"产地：{origin}")

    weight = pet.get("weight", "")
    if weight:
        lines.append(f"体重：{weight}")

    height = pet.get("height", "")
    if height:
        lines.append(f"身高：{height}")

    life_span = pet.get("life_span", "")
    if life_span:
        lines.append(f"寿命：{life_span}")

    fur_color = pet.get("fur_color", "")
    if fur_color:
        lines.append(f"毛色：{fur_color}")

    functions = pet.get("functions", "")
    if functions:
        lines.append(f"用途：{functions}")

    body_shape = pet.get("body_shape", "")
    if body_shape:
        lines.append(f"体型：{body_shape}")

    ear_features = pet.get("ear_features", "")
    if ear_features:
        lines.append(f"耳朵特征：{ear_features}")

    eye_features = pet.get("eye_features", "")
    if eye_features:
        lines.append(f"眼睛特征：{eye_features}")

    tail_features = pet.get("tail_features", "")
    if tail_features:
        lines.append(f"尾巴特征：{tail_features}")

    # 详细介绍
    introduction = pet.get("introduction", "")
    if introduction:
        lines.append("")
        lines.append("📖 介绍")
        lines.append(introduction[:500] + "..." if len(introduction) > 500 else introduction)

    # 历史
    history = pet.get("history", "")
    if history:
        lines.append("")
        lines.append("📜 历史")
        lines.append(history[:300] + "..." if len(history) > 300 else history)

    # 饲养知识
    care_knowledge = pet.get("care_knowledge", "")
    if care_knowledge:
        lines.append("")
        lines.append("💡 饲养知识")
        lines.append(care_knowledge[:300] + "..." if len(care_knowledge) > 300 else care_knowledge)

    # 常见疾病
    common_diseases = pet.get("common_diseases", "")
    if common_diseases:
        lines.append("")
        lines.append("⚠️ 常见疾病")
        lines.append(common_diseases[:300] + "..." if len(common_diseases) > 300 else common_diseases)

    # 毛发护理
    fur_care = pet.get("fur_care", "")
    if fur_care:
        lines.append("")
        lines.append("🧹 毛发护理")
        lines.append(fur_care[:300] + "..." if len(fur_care) > 300 else fur_care)

    # 评分数据
    rating_data = pet.get("rating_data", [])
    if rating_data:
        lines.append("")
        lines.append("📊 评分")
        for item in rating_data:
            lines.append(f"   {item.get('name', '')}: {item.get('value', '')}")

    return "\n".join(lines)


def format_search_result(result: dict) -> str:
    """格式化搜索结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    data = result.get("data", [])
    total_count = result.get("total_count", 0)

    if not data:
        return "🐾 未找到相关宠物"

    lines = []
    lines.append(f"🐾 宠物搜索结果（共 {total_count} 条）")
    lines.append("")

    for i, pet in enumerate(data):
        lines.append(format_pet_brief(pet, i))
        lines.append("")

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    query = None
    category = None
    detail_mode = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--detail" and i + 1 < len(args):
            detail_mode = True
            query = args[i + 1]
            i += 2
        elif args[i] in ("--help", "-h"):
            print("用法：python pet_query.py [选项] [搜索词]")
            print("")
            print("选项:")
            print("  --category CAT   按类别搜索：dog/cat/shuizi/xiaochong/pachong")
            print("  --detail NAME    查看宠物详情")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python pet_query.py 哈士奇")
            print("  python pet_query.py --category dog")
            print("  python pet_query.py --detail 哈士奇")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        elif not args[i].startswith("--"):
            query = args[i]
            print(f"搜索词：{query}")
            i += 1
        else:
            i += 1

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_PET_QUERY_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_PET_QUERY_KEY=your_api_key")
        print("   3. 命令行参数：python pet_query.py --key your_api_key 哈士奇")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    if detail_mode:
        # 详情模式：先搜索获取 hash_id，再查详情
        if not query:
            print("错误：--detail 后需要提供宠物名称")
            sys.exit(1)

        # 先搜索
        search_result = search_pets(query=query, api_key=api_key, page_size=1)
        if not search_result["success"]:
            print(format_search_result(search_result))
            sys.exit(1)

        data = search_result.get("data", [])
        if not data:
            print(f"🐾 未找到宠物：{query}")
            sys.exit(1)

        hash_id = data[0].get("hash_id", "")
        if not hash_id:
            print("❌ 无法获取宠物 ID")
            sys.exit(1)

        # 查详情
        detail_result = get_pet_detail(hash_id, api_key)
        if not detail_result["success"]:
            print(f"❌ 查询失败：{detail_result.get('error', '未知错误')}")
            sys.exit(1)

        pet_data = detail_result.get("data", {})
        print(format_pet_detail(pet_data))

    elif category:
        # 按类别搜索
        result = search_pets(category=category, api_key=api_key, page_size=10)
        print(format_search_result(result))

    elif query:
        # 按名称搜索
        result = search_pets(query=query, api_key=api_key, page_size=10)
        print(format_search_result(result))

    else:
        print("用法：python pet_query.py [选项] [搜索词]")
        print("")
        print("示例:")
        print("  python pet_query.py 哈士奇")
        print("  python pet_query.py --category dog")
        print("  python pet_query.py --detail 哈士奇")
        print("")
        print(f"免费申请 API Key: {REGISTER_URL}")
        sys.exit(1)

    # 输出 JSON 数据
    print("")
    print("JSON 数据:")


if __name__ == "__main__":
    main()
