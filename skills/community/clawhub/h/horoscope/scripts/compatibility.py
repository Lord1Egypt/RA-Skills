#!/usr/bin/env python3
"""星座配对查询 - 查询两个星座的配对分析"""

import json
from pathlib import Path

# 加载星座数据
DATA_DIR = Path(__file__).parent.parent / "data"


def load_data():
    """加载星座数据和配对数据"""
    with open(DATA_DIR / "zodiac_info.json", "r", encoding="utf-8") as f:
        zodiac_info = json.load(f)
    with open(DATA_DIR / "compatibility.json", "r", encoding="utf-8") as f:
        compatibility = json.load(f)
    return zodiac_info, compatibility


def normalize_sign(sign: str, zodiac_info: dict) -> str | None:
    """将各种格式的星座名转换为英文
    
    Args:
        sign: 星座名（中文、英文、别名均可）
        zodiac_info: 星座信息字典
    
    Returns:
        英文星座名，如果无法识别则返回 None
    """
    sign_lower = sign.lower().strip()
    
    # 直接匹配英文
    if sign_lower in zodiac_info:
        return sign_lower
    
    # 匹配中文名或别名
    for en, info in zodiac_info.items():
        if sign_lower == info["name_zh"].lower():
            return en
        if sign_lower in [a.lower() for a in info.get("aliases", [])]:
            return en
    
    return None


def get_compatibility(sign1: str, sign2: str) -> dict:
    """查询两个星座的配对
    
    Args:
        sign1: 第一个星座名
        sign2: 第二个星座名
    
    Returns:
        {"success": True, "data": {...}} 或 {"success": False, "error": "..."}
    """
    zodiac_info, compatibility = load_data()
    
    s1 = normalize_sign(sign1, zodiac_info)
    s2 = normalize_sign(sign2, zodiac_info)
    
    if not s1:
        return {"success": False, "error": f"未知的星座: {sign1}"}
    if not s2:
        return {"success": False, "error": f"未知的星座: {sign2}"}
    
    # 元素中英文映射
    element_map = {
        "火象": "fire",
        "土象": "earth",
        "风象": "air",
        "水象": "water",
    }
    
    # 获取元素并转换为英文
    element1 = element_map.get(zodiac_info[s1]["element"], zodiac_info[s1]["element"])
    element2 = element_map.get(zodiac_info[s2]["element"], zodiac_info[s2]["element"])
    
    # 构建 key（排序以匹配 fire-earth 和 earth-fire）
    elements = sorted([element1, element2])
    key = f"{elements[0]}-{elements[1]}"
    
    if key not in compatibility:
        return {"success": False, "error": f"未找到配对数据: {key}"}
    
    result = compatibility[key].copy()
    result["sign1"] = zodiac_info[s1]
    result["sign2"] = zodiac_info[s2]
    result["success"] = True
    
    return result


def format_compatibility_output(sign1: str, sign2: str, result: dict) -> str:
    """格式化配对输出
    
    Args:
        sign1: 第一个星座名（原始输入）
        sign2: 第二个星座名（原始输入）
        result: get_compatibility 返回的结果
    
    Returns:
        格式化的配对文本
    """
    if not result["success"]:
        return f"❌ 获取配对失败: {result['error']}"
    
    s1_info = result["sign1"]
    s2_info = result["sign2"]
    
    symbol1 = s1_info.get("symbol", "")
    symbol2 = s2_info.get("symbol", "")
    name1_zh = s1_info.get("name_zh", "")
    name2_zh = s2_info.get("name_zh", "")
    
    score = result.get("score", 0)
    summary = result.get("summary", "")
    strengths = result.get("strengths", [])
    conflicts = result.get("conflicts", [])
    advice = result.get("advice", "")
    
    # 生成星级评分
    stars = "⭐" * score + "☆" * (10 - score)
    
    return f"""{symbol1} × {symbol2} {name1_zh} × {name2_zh}

契合度：{stars} ({score}/10)

{summary}

✅ 优势：
{chr(10).join(f'  • {s}' for s in strengths)}

⚠️ 冲突：
{chr(10).join(f'  • {c}' for c in conflicts)}

💡 建议：
{advice}
"""


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("aries", "leo"),
        ("白羊座", "狮子座"),
        ("白羊", "狮子"),
        ("aries", "taurus"),
        ("unknown", "leo"),
    ]
    
    print("=== 测试星座配对 ===\n")
    
    for s1, s2 in test_cases:
        result = get_compatibility(s1, s2)
        if result["success"]:
            print(f"✅ {s1} × {s2}:")
            print(format_compatibility_output(s1, s2, result))
            print("-" * 50)
        else:
            print(f"❌ {s1} × {s2}: {result['error']}\n")
