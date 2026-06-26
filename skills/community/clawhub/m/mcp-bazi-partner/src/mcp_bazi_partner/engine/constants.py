"""All constant tables for BaZi analysis."""

# Heavenly Stems attributes
TIANGAN_WUXING = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火",
    "戊": "土", "己": "土", "庚": "金", "辛": "金",
    "壬": "水", "癸": "水",
}

TIANGAN_YINYANG = {
    "甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴",
    "戊": "阳", "己": "阴", "庚": "阳", "辛": "阴",
    "壬": "阳", "癸": "阴",
}

# Earthly Branches hidden stems (ordered: benqi > zhongqi > yuqi)
DIZHI_CANGGAN = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

# Hidden stem weight (benqi > zhongqi > yuqi)
CANGGAN_WEIGHT = [0.6, 0.3, 0.1]

# Wuxing relationships
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

# ShiShen (Ten Gods) to pattern name mapping
SHISHEN_TO_PATTERN = {
    "正官": "正官格",
    "七杀": "七杀格",
    "正财": "财格",
    "偏财": "财格",
    "正印": "印格",
    "偏印": "印格",
    "食神": "食神格",
    "伤官": "伤官格",
}

# JianLu table: day stem -> linguan position (earthly branch)
JIANLU_TABLE = {
    "甲": "寅", "乙": "卯", "丙": "巳", "丁": "午",
    "戊": "巳", "己": "午", "庚": "申", "辛": "酉",
    "壬": "亥", "癸": "子",
}

# YangRen table: yang day stems only
YANGREN_TABLE = {
    "甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子",
}

# Zaqi (mixed-qi) months
ZAQI_ZHI = {"辰", "戌", "丑", "未"}

# Hour to shichen mapping: hour (0-23) -> (mapped_hour, mapped_minute)
HOUR_TO_SHICHEN_MID = {
    23: (23, 30), 0: (0, 30),
    1: (2, 0), 2: (2, 0),
    3: (4, 0), 4: (4, 0),
    5: (6, 0), 6: (6, 0),
    7: (8, 0), 8: (8, 0),
    9: (10, 0), 10: (10, 0),
    11: (12, 0), 12: (12, 0),
    13: (14, 0), 14: (14, 0),
    15: (16, 0), 16: (16, 0),
    17: (18, 0), 18: (18, 0),
    19: (20, 0), 20: (20, 0),
    21: (22, 0), 22: (22, 0),
}

# Shichen names
SHICHEN_NAMES = [
    "子时", "丑时", "寅时", "卯时", "辰时", "巳时",
    "午时", "未时", "申时", "酉时", "戌时", "亥时",
]


def hour_to_shichen_name(hour: int) -> str:
    idx = ((hour + 1) % 24) // 2
    return SHICHEN_NAMES[idx]


def get_shishen(day_gan: str, other_gan: str) -> str:
    """Calculate the ShiShen (Ten God) relationship between day stem and another stem."""
    day_wx = TIANGAN_WUXING[day_gan]
    day_yy = TIANGAN_YINYANG[day_gan]
    other_wx = TIANGAN_WUXING[other_gan]
    other_yy = TIANGAN_YINYANG[other_gan]
    same_yy = (day_yy == other_yy)

    if day_wx == other_wx:
        return "比肩" if same_yy else "劫财"
    elif WUXING_SHENG[day_wx] == other_wx:
        return "食神" if same_yy else "伤官"
    elif WUXING_KE[day_wx] == other_wx:
        return "偏财" if same_yy else "正财"
    elif WUXING_SHENG[other_wx] == day_wx:
        return "偏印" if same_yy else "正印"
    elif WUXING_KE[other_wx] == day_wx:
        return "七杀" if same_yy else "正官"
    return "未知"


# Status display mapping (poetic labels with colors)
STATUS_DISPLAY = {
    "成格": ("天成", "#d4a853"),
    "败格有救": ("柳暗花明", "#c9a84c"),
    "败格无救": ("蓄势待发", "#4a7a9b"),
}
