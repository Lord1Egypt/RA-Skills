#!/usr/bin/env python3
"""
八字排盘计算器
根据出生年月日时计算八字四柱
"""

import sys
import json
from datetime import datetime

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行对应
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 生肖对应
SHENGXIAO = {
    "子": "鼠", "丑": "牛", "寅": "虎", "卯": "兔",
    "辰": "龙", "巳": "蛇", "午": "马", "未": "羊",
    "申": "猴", "酉": "鸡", "戌": "狗", "亥": "猪"
}

# 时辰对应
SHICHEN = {
    0: "子", 1: "丑", 2: "丑", 3: "寅", 4: "寅", 5: "卯",
    6: "卯", 7: "辰", 8: "辰", 9: "巳", 10: "巳", 11: "午",
    12: "午", 13: "未", 14: "未", 15: "申", 16: "申", 17: "酉",
    18: "酉", 19: "戌", 20: "戌", 21: "亥", 22: "亥", 23: "子"
}


def get_year_ganzhi(year):
    """计算年柱"""
    # 以1984年（甲子年）为基准
    base_year = 1984
    offset = (year - base_year) % 60
    gan_index = offset % 10
    zhi_index = offset % 12
    return TIANGAN[gan_index] + DIZHI[zhi_index]


def get_month_ganzhi(year, month):
    """计算月柱
    年干决定月干起始
    甲己之年丙作首，乙庚之岁戊为头
    丙辛之岁寻庚上，丁壬壬位顺行流
    若言戊癸何方发，甲寅之上好追求
    """
    year_gan = get_year_ganzhi(year)[0]
    
    # 确定月干起始
    start_gan_map = {
        "甲": 2, "己": 2,  # 丙
        "乙": 4, "庚": 4,  # 戊
        "丙": 6, "辛": 6,  # 庚
        "丁": 8, "壬": 8,  # 壬
        "戊": 0, "癸": 0   # 甲
    }
    
    start_gan = start_gan_map.get(year_gan, 0)
    
    # 正月（寅月）开始
    month_zhi_index = (month + 1) % 12  # 正月寅
    gan_index = (start_gan + month - 1) % 10
    
    return TIANGAN[gan_index] + DIZHI[month_zhi_index]


def get_day_ganzhi(year, month, day):
    """计算日柱
    使用简化算法，以1900-01-31为基准（甲子日）
    """
    base_date = datetime(1900, 1, 31)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    offset = days_diff % 60
    gan_index = offset % 10
    zhi_index = offset % 12
    
    return TIANGAN[gan_index] + DIZHI[zhi_index]


def get_hour_ganzhi(day_gan, hour):
    """计算时柱
    日干决定时干起始
    甲己还加甲，乙庚丙作初
    丙辛从戊起，丁壬庚子居
    戊癸何方发，壬子是真途
    """
    start_gan_map = {
        "甲": 0, "己": 0,   # 甲
        "乙": 2, "庚": 2,  # 丙
        "丙": 4, "辛": 4,  # 戊
        "丁": 6, "壬": 6,  # 庚
        "戊": 8, "癸": 8   # 壬
    }
    
    start_gan = start_gan_map.get(day_gan, 0)
    
    # 计算时辰（每2小时一个时辰）
    shichen_index = (hour + 1) // 2 % 12
    gan_index = (start_gan + shichen_index) % 10
    
    return TIANGAN[gan_index] + DIZHI[shichen_index]


def calculate_bazi(year, month, day, hour, minute=0):
    """
    计算八字
    
    Args:
        year: 年份
        month: 月份（1-12）
        day: 日期
        hour: 小时（0-23）
        minute: 分钟（可选）
    
    Returns:
        dict: 八字信息
    """
    # 计算四柱
    year_pillar = get_year_ganzhi(year)
    month_pillar = get_month_ganzhi(year, month)
    day_pillar = get_day_ganzhi(year, month, day)
    hour_pillar = get_hour_ganzhi(day_pillar[0], hour)
    
    # 提取天干地支
    pillars = {
        "年柱": year_pillar,
        "月柱": month_pillar,
        "日柱": day_pillar,
        "时柱": hour_pillar
    }
    
    # 计算五行分布
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for pillar in pillars.values():
        gan = pillar[0]
        zhi = pillar[1]
        wuxing_count[TIANGAN_WUXING[gan]] += 1
        wuxing_count[DIZHI_WUXING[zhi]] += 1
    
    # 日主（日干）
    day_master = day_pillar[0]
    day_master_wuxing = TIANGAN_WUXING[day_master]
    
    # 生肖
    zodiac = SHENGXIAO[year_pillar[1]]
    
    # 时辰名称
    shichen_name = SHICHEN.get(hour, "子")
    
    return {
        "八字": pillars,
        "日主": day_master,
        "日主五行": day_master_wuxing,
        "生肖": zodiac,
        "五行分布": wuxing_count,
        "出生时间": f"{year}年{month}月{day}日 {hour:02d}:{minute:02d}",
        "时辰": shichen_name
    }


def analyze_wuxing(bazi_result):
    """分析五行强弱和喜用神"""
    wuxing = bazi_result["五行分布"]
    day_master_wuxing = bazi_result["日主五行"]
    
    # 计算五行强度（简化版）
    total = sum(wuxing.values())
    if total == 0:
        return {}
    
    strength = {k: round(v / total * 100, 1) for k, v in wuxing.items()}
    
    # 判断日主强弱（简化逻辑）
    day_master_count = wuxing.get(day_master_wuxing, 0)
    
    # 生助日主的五行
    shengzhu_map = {
        "金": ["土", "金"],
        "木": ["水", "木"],
        "水": ["金", "水"],
        "火": ["木", "火"],
        "土": ["火", "土"]
    }
    
    # 克制日主的五行
    kezhi_map = {
        "金": ["火", "木"],
        "木": ["金", "土"],
        "水": ["土", "火"],
        "火": ["水", "金"],
        "土": ["木", "水"]
    }
    
    shengzhu = shengzhu_map.get(day_master_wuxing, [])
    kezhi = kezhi_map.get(day_master_wuxing, [])
    
    # 计算生助和克制的力量
    shengzhu_power = sum(wuxing.get(w, 0) for w in shengzhu)
    kezhi_power = sum(wuxing.get(w, 0) for w in kezhi)
    
    if shengzhu_power > kezhi_power + 2:
        strength_level = "身强"
        xiyongshen = kezhi if kezhi else ["需要具体分析"]
    elif shengzhu_power < kezhi_power - 2:
        strength_level = "身弱"
        xiyongshen = shengzhu if shengzhu else ["需要具体分析"]
    else:
        strength_level = "中和"
        xiyongshen = ["根据大运流年而定"]
    
    return {
        "五行强度": strength,
        "日主强弱": strength_level,
        "喜用神": xiyongshen,
        "忌神": kezhi if strength_level == "身强" else shengzhu
    }


def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("用法: python bazi_calculator.py <年> <月> <日> <时> [分]")
        print("示例: python bazi_calculator.py 1990 3 15 15")
        sys.exit(1)
    
    try:
        year = int(sys.argv[1])
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = int(sys.argv[4])
        minute = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        
        result = calculate_bazi(year, month, day, hour, minute)
        analysis = analyze_wuxing(result)
        
        output = {
            "八字排盘": result,
            "五行分析": analysis
        }
        
        print(json.dumps(output, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
