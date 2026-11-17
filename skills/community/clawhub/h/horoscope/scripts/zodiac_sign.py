#!/usr/bin/env python3
"""生日查星座 - 根据出生日期查询星座信息"""

import json
from datetime import datetime
from pathlib import Path

# 加载星座数据
DATA_DIR = Path(__file__).parent.parent / "data"


def load_zodiac_info():
    """加载星座基础信息"""
    with open(DATA_DIR / "zodiac_info.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_personalities():
    """加载星座性格详解"""
    with open(DATA_DIR / "personalities.json", "r", encoding="utf-8") as f:
        return json.load(f)


def get_zodiac_sign(month: int, day: int) -> tuple[str, dict] | None:
    """根据月日返回星座信息
    
    Args:
        month: 月份 (1-12)
        day: 日期 (1-31)
    
    Returns:
        (星座英文名, 星座信息字典) 元组，如果日期无效则返回 None
    """
    if not (1 <= month <= 12) or not (1 <= day <= 31):
        return None
    
    zodiac_info = load_zodiac_info()
    
    # 星座日期范围（月份, 日期, 星座英文名）
    # 注意：这里的日期是每个星座的结束日期
    ranges = [
        (1, 20, "capricorn"),    # 摩羯座结束于 1/20
        (2, 19, "aquarius"),     # 水瓶座结束于 2/19
        (3, 21, "pisces"),       # 双鱼座结束于 3/21
        (4, 20, "aries"),        # 白羊座结束于 4/20
        (5, 21, "taurus"),       # 金牛座结束于 5/21
        (6, 21, "gemini"),       # 双子座结束于 6/21
        (7, 23, "cancer"),       # 巨蟹座结束于 7/23
        (8, 23, "leo"),          # 狮子座结束于 8/23
        (9, 23, "virgo"),        # 处女座结束于 9/23
        (10, 23, "libra"),       # 天秤座结束于 10/23
        (11, 22, "scorpio"),     # 天蝎座结束于 11/22
        (12, 22, "sagittarius"), # 射手座结束于 12/22
        (12, 31, "capricorn"),   # 摩羯座结束于 12/31（跨年）
    ]
    
    for end_month, end_day, sign in ranges:
        if (month, day) <= (end_month, end_day):
            return sign, zodiac_info[sign]
    
    return None


def parse_date(date_str: str) -> tuple[int | None, int | None]:
    """解析多种日期格式
    
    支持的格式：
    - MM-DD (如 3-15)
    - MM/DD (如 7/29)
    - YYYY-MM-DD (如 1990-05-15)
    - YYYY/MM/DD (如 1990/05/15)
    - M月D日 (如 12月25日)
    
    Args:
        date_str: 日期字符串
    
    Returns:
        (month, day) 元组，如果无法解析则返回 (None, None)
    """
    formats = [
        "%m-%d",
        "%m/%d",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m月%d日",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.month, dt.day
        except ValueError:
            continue
    
    return None, None


def format_zodiac_output(month: int, day: int, sign_en: str, zodiac_info: dict) -> str:
    """格式化星座输出（包含性格详解）
    
    Args:
        month: 月份
        day: 日期
        sign_en: 星座英文名
        zodiac_info: 星座基础信息字典
    
    Returns:
        格式化的星座文本
    """
    symbol = zodiac_info.get("symbol", "")
    emoji = zodiac_info.get("emoji", "")
    name_zh = zodiac_info.get("name_zh", "")
    date_range = zodiac_info.get("date_range", "")
    element = zodiac_info.get("element", "")
    quality = zodiac_info.get("quality", "")
    ruling_planet = zodiac_info.get("ruling_planet", "")
    lucky_numbers = zodiac_info.get("lucky_number", [])
    lucky_colors = zodiac_info.get("lucky_color", [])
    lucky_gem = zodiac_info.get("lucky_gem", "")
    lucky_day = zodiac_info.get("lucky_day", "")
    
    # 加载性格详解
    personalities = load_personalities()
    personality = personalities.get(sign_en, {})
    
    core_traits = personality.get("core_traits", "")
    strengths = personality.get("strengths", [])
    weaknesses = personality.get("weaknesses", [])
    career_suitable = personality.get("career_fit", {}).get("suitable", [])
    career_avoid = personality.get("career_fit", {}).get("avoid", [])
    love_style = personality.get("love_style", "")
    communication = personality.get("communication", "")
    growth_advice = personality.get("growth_advice", "")
    
    output = f"""{symbol} {emoji} {name_zh}

📅 日期范围：{date_range}
🔥 元素：{element} | 性质：{quality}
🪐 守护星：{ruling_planet}

🔢 幸运数字：{', '.join(map(str, lucky_numbers))}
🎨 幸运颜色：{', '.join(lucky_colors)}
💎 幸运宝石：{lucky_gem}
📅 幸运日：{lucky_day}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💫 性格详解

🎯 核心特质：{core_traits}

✅ 优点：
{chr(10).join(f'  • {s}' for s in strengths)}

❌ 缺点：
{chr(10).join(f'  • {w}' for w in weaknesses)}

💼 适合职业：{', '.join(career_suitable)}
🚫 避免职业：{', '.join(career_avoid)}

💕 恋爱风格：{love_style}

🗣️ 沟通方式：{communication}

💡 成长建议：{growth_advice}
"""
    return output


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        "3-15",
        "7/29",
        "1990-05-15",
        "12月25日",
        "invalid",
    ]
    
    print("=== 测试生日查星座 ===\n")
    
    for date_str in test_cases:
        month, day = parse_date(date_str)
        if month and day:
            result = get_zodiac_sign(month, day)
            if result:
                sign_en, zodiac = result
                print(f"✅ {date_str} ({month}月{day}日):")
                print(format_zodiac_output(month, day, sign_en, zodiac))
                print("-" * 50)
            else:
                print(f"❌ {date_str}: 未找到星座\n")
        else:
            print(f"❌ {date_str}: 无法解析日期\n")
