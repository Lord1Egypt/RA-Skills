#!/usr/bin/env python3
"""
生肖配对分析器
分析十二生肖之间的相合相冲关系
"""

import sys
import json

# 十二生肖
ZODIAC = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

# 六合（最佳配对）
LIUHE = {
    "鼠": "牛", "牛": "鼠",
    "虎": "猪", "猪": "虎",
    "兔": "狗", "狗": "兔",
    "龙": "鸡", "鸡": "龙",
    "蛇": "猴", "猴": "蛇",
    "马": "羊", "羊": "马"
}

# 三合（良好配对）
SANHE = [
    ["猴", "鼠", "龙"],  # 水局
    ["虎", "马", "狗"],  # 火局
    ["蛇", "鸡", "牛"],  # 金局
    ["猪", "兔", "羊"]   # 木局
]

# 六冲（避免配对）
LIUCHONG = {
    "鼠": "马", "马": "鼠",
    "牛": "羊", "羊": "牛",
    "虎": "猴", "猴": "虎",
    "兔": "鸡", "鸡": "兔",
    "龙": "狗", "狗": "龙",
    "蛇": "猪", "猪": "蛇"
}

# 六害（不太理想）
LIUHAI = {
    "鼠": "羊", "羊": "鼠",
    "牛": "马", "马": "牛",
    "虎": "蛇", "蛇": "虎",
    "兔": "龙", "龙": "兔",
    "猴": "猪", "猪": "猴",
    "鸡": "狗", "狗": "鸡"
}

# 五行属性
ZODIAC_WUXING = {
    "鼠": "水", "牛": "土", "虎": "木", "兔": "木",
    "龙": "土", "蛇": "火", "马": "火", "羊": "土",
    "猴": "金", "鸡": "金", "狗": "土", "猪": "水"
}

# 配对评价
MATCH_COMMENTS = {
    "六合": {
        "score": 95,
        "desc": "天作之合，最佳配对",
        "detail": "六合是十二生肖中最完美的配对，两人性格互补，能够互相理解和支持。"
    },
    "三合": {
        "score": 85,
        "desc": "情投意合，良好配对",
        "detail": "三合配对非常和谐，有共同的价值观和目标，容易建立稳定的关系。"
    },
    "相生": {
        "score": 75,
        "desc": "五行相生，相互扶持",
        "detail": "五行相生关系，能够互相促进和成长，关系较为和谐。"
    },
    "普通": {
        "score": 60,
        "desc": "关系一般，需要经营",
        "detail": "没有明显的吉凶关系，需要双方共同努力经营感情。"
    },
    "相害": {
        "score": 40,
        "desc": "略有摩擦，需要包容",
        "detail": "六害关系，可能会有一些小摩擦和误解，需要多沟通和理解。"
    },
    "相冲": {
        "score": 25,
        "desc": "性格冲突，需要磨合",
        "detail": "六冲关系，性格和观念可能有较大差异，需要更多的包容和妥协。"
    }
}


def check_sanhe(z1, z2):
    """检查是否为三合"""
    for group in SANHE:
        if z1 in group and z2 in group:
            return True
    return False


def check_wuxing_relation(z1, z2):
    """检查五行关系"""
    w1 = ZODIAC_WUXING.get(z1)
    w2 = ZODIAC_WUXING.get(z2)
    
    if not w1 or not w2:
        return None
    
    # 五行相生
    sheng_relation = {
        "木": "火", "火": "土", "土": "金", "金": "水", "水": "木"
    }
    
    if sheng_relation.get(w1) == w2:
        return "z1生z2"
    elif sheng_relation.get(w2) == w1:
        return "z2生z1"
    elif w1 == w2:
        return "相同"
    else:
        return "相克"


def analyze_match(z1, z2):
    """
    分析两个生肖的配对
    
    Args:
        z1: 第一个生肖
        z2: 第二个生肖
    
    Returns:
        dict: 配对分析结果
    """
    if z1 not in ZODIAC or z2 not in ZODIAC:
        return {"错误": "无效的生肖"}
    
    # 检查各种关系
    if LIUHE.get(z1) == z2:
        match_type = "六合"
    elif LIUCHONG.get(z1) == z2:
        match_type = "相冲"
    elif LIUHAI.get(z1) == z2:
        match_type = "相害"
    elif check_sanhe(z1, z2):
        match_type = "三合"
    elif check_wuxing_relation(z1, z2) in ["z1生z2", "z2生z1"]:
        match_type = "相生"
    else:
        match_type = "普通"
    
    result = MATCH_COMMENTS.get(match_type, MATCH_COMMENTS["普通"]).copy()
    result["配对类型"] = match_type
    result["生肖1"] = z1
    result["生肖2"] = z2
    result["五行1"] = ZODIAC_WUXING.get(z1)
    result["五行2"] = ZODIAC_WUXING.get(z2)
    
    # 添加五行关系说明
    wx_relation = check_wuxing_relation(z1, z2)
    if wx_relation == "z1生z2":
        result["五行关系"] = f"{z1}({ZODIAC_WUXING[z1]})生{z2}({ZODIAC_WUXING[z2]})"
    elif wx_relation == "z2生z1":
        result["五行关系"] = f"{z2}({ZODIAC_WUXING[z2]})生{z1}({ZODIAC_WUXING[z1]})"
    elif wx_relation == "相同":
        result["五行关系"] = f"同属{ZODIAC_WUXING[z1]}"
    else:
        result["五行关系"] = f"{ZODIAC_WUXING[z1]}克{ZODIAC_WUXING[z2]}"
    
    return result


def get_best_matches(zodiac):
    """获取最佳配对"""
    if zodiac not in ZODIAC:
        return []
    
    # 六合
    liuhe = LIUHE.get(zodiac)
    
    # 三合
    sanhe = []
    for group in SANHE:
        if zodiac in group:
            sanhe = [z for z in group if z != zodiac]
            break
    
    return {
        "六合": liuhe,
        "三合": sanhe,
        "避免": LIUCHONG.get(zodiac),
        "谨慎": LIUHAI.get(zodiac)
    }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  配对分析: python zodiac_match.py <生肖1> <生肖2>")
        print("  最佳配对: python zodiac_match.py <生肖>")
        print("示例:")
        print("  python zodiac_match.py 龙 鸡")
        print("  python zodiac_match.py 龙")
        sys.exit(1)
    
    try:
        if len(sys.argv) == 2:
            # 查询最佳配对
            zodiac = sys.argv[1]
            result = get_best_matches(zodiac)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # 配对分析
            z1 = sys.argv[1]
            z2 = sys.argv[2]
            result = analyze_match(z1, z2)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
