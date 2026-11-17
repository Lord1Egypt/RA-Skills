#!/usr/bin/env python3
"""每日星座运势查询 - 调用 ohmanda API"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

# 加载星座数据
DATA_DIR = Path(__file__).parent.parent / "data"


def load_zodiac_info():
    """加载星座基础信息"""
    with open(DATA_DIR / "zodiac_info.json", "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_sign(sign: str) -> Optional[str]:
    """将各种格式的星座名转换为英文
    
    Args:
        sign: 星座名（中文、英文、别名均可）
    
    Returns:
        英文星座名，如果无法识别则返回 None
    """
    zodiac_info = load_zodiac_info()
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


def get_horoscope(sign: str) -> dict:
    """获取每日运势
    
    Args:
        sign: 星座名（中文、英文、别名均可）
    
    Returns:
        {"success": True, "data": {...}} 或 {"success": False, "error": "..."}
    """
    normalized = normalize_sign(sign)
    if not normalized:
        return {"success": False, "error": f"未知的星座: {sign}"}
    
    url = f"https://ohmanda.com/api/horoscope/{normalized}/"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {"success": True, "data": data}
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP 错误: {e.code}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"网络错误: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def format_horoscope_output(sign: str, result: dict) -> str:
    """格式化运势输出
    
    Args:
        sign: 原始星座名
        result: get_horoscope 返回的结果
    
    Returns:
        格式化的运势文本
    """
    if not result["success"]:
        return f"❌ 获取运势失败: {result['error']}"
    
    data = result["data"]
    zodiac_info = load_zodiac_info()
    normalized = normalize_sign(sign)
    
    if normalized and normalized in zodiac_info:
        info = zodiac_info[normalized]
        symbol = info.get("symbol", "")
        name_zh = info.get("name_zh", normalized)
    else:
        symbol = ""
        name_zh = normalized
    
    horoscope = data.get("horoscope", "暂无运势信息")
    date = data.get("date", "今日")
    
    return f"""{symbol} {name_zh}今日运势（{date}）

{horoscope}
"""


if __name__ == "__main__":
    # 测试用例
    test_cases = ["leo", "狮子座", "白羊", "aries", "unknown"]
    
    print("=== 测试每日运势查询 ===\n")
    
    for sign in test_cases:
        result = get_horoscope(sign)
        if result["success"]:
            print(f"✅ {sign}:")
            print(format_horoscope_output(sign, result))
            print("-" * 50)
        else:
            print(f"❌ {sign}: {result['error']}\n")
