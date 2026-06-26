# -*- coding: utf-8 -*-
"""
12星座符号常量定义
Created: 2026-04-14
"""

# 星座符号字典
CONSTELLATION_SYMBOLS = {
    "白羊座": "♈",
    "金牛座": "♉",
    "双子座": "♊",
    "巨蟹座": "♋",
    "狮子座": "♌",
    "处女座": "♍",
    "天秤座": "♎",
    "天蝎座": "♏",
    "射手座": "♐",
    "摩羯座": "♑",
    "水瓶座": "♒",
    "双鱼座": "♓",
}

# Unicode编码
CONSTELLATION_UNICODE = {
    "白羊座": "U+2648",
    "金牛座": "U+2649",
    "双子座": "U+264A",
    "巨蟹座": "U+264B",
    "狮子座": "U+264C",
    "处女座": "U+264D",
    "天秤座": "U+264E",
    "天蝎座": "U+264F",
    "射手座": "U+2650",
    "摩羯座": "U+2651",
    "水瓶座": "U+2652",
    "双鱼座": "U+2653",
}

# 英文名称
CONSTELLATION_ENGLISH = {
    "白羊座": "Aries",
    "金牛座": "Taurus",
    "双子座": "Gemini",
    "巨蟹座": "Cancer",
    "狮子座": "Leo",
    "处女座": "Virgo",
    "天秤座": "Libra",
    "天蝎座": "Scorpio",
    "射手座": "Sagittarius",
    "摩羯座": "Capricorn",
    "水瓶座": "Aquarius",
    "双鱼座": "Pisces",
}

# 星座顺序列表
CONSTELLATION_ORDER = [
    "白羊座", "金牛座", "双子座", "巨蟹座",
    "狮子座", "处女座", "天秤座", "天蝎座",
    "射手座", "摩羯座", "水瓶座", "双鱼座"
]

# 符号列表
SYMBOL_LIST = ["♈", "♉", "♊", "♋", "♌", "♍", "♎", "♏", "♐", "♑", "♒", "♓"]


def get_symbol(constellation_name):
    """根据星座名称获取符号"""
    return CONSTELLATION_SYMBOLS.get(constellation_name, "")


def get_constellation_by_symbol(symbol):
    """根据符号获取星座名称"""
    for name, sym in CONSTELLATION_SYMBOLS.items():
        if sym == symbol:
            return name
    return ""


if __name__ == "__main__":
    # 测试
    print("12星座符号：")
    for name, symbol in CONSTELLATION_SYMBOLS.items():
        print(f"{name}: {symbol}")