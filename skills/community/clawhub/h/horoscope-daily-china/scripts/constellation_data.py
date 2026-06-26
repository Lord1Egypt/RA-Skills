# -*- coding: utf-8 -*-
"""
每日星座运势生成器 - 万维易源 API 版
核心数据模块：12 星座数据库、配对算法、健康/小人补充数据
"""

# ==================== 幸运方位映射表（基于星座元素） ====================
LUCKY_DIRECTIONS = {
    "白羊座": "东南方", "狮子座": "南方", "射手座": "西北方",  # 火象
    "金牛座": "西南方", "处女座": "西方", "摩羯座": "北方",  # 土象
    "双子座": "东方", "天秤座": "东南方", "水瓶座": "西南方",  # 风象
    "巨蟹座": "东北方", "天蝎座": "北方", "双鱼座": "东方",  # 水象
}

# ==================== 幸运时段映射表（基于星座特性） ====================
LUCKY_TIMES = {
    "白羊座": "06:00-08:00", "狮子座": "10:00-12:00", "射手座": "22:00-00:00",  # 火象
    "金牛座": "08:00-10:00", "处女座": "14:00-16:00", "摩羯座": "20:00-22:00",  # 土象
    "双子座": "12:00-14:00", "天秤座": "16:00-18:00", "水瓶座": "00:00-02:00",  # 风象
    "巨蟹座": "18:00-20:00", "天蝎座": "02:00-04:00", "双鱼座": "04:00-06:00",  # 水象
}

# ==================== 12 星座基本信息 ====================
CONSTELLATIONS = {
    "白羊座": {
        "date": "3.21-4.19",
        "element": "火",
        "symbol": "♈",
        "ruling_planet": "火星",
        "traits": ["热情", "直率", "勇敢", "冲动"],
        "lucky_numbers": [1, 8, 17],
        "lucky_colors": ["红色", "橙色"],
        "health_focus": "头部和眼睛",
        "enemy": "天秤座",  # 对冲星座
    },
    "金牛座": {
        "date": "4.20-5.20",
        "element": "土",
        "symbol": "♉",
        "ruling_planet": "金星",
        "traits": ["稳重", "务实", "耐心", "固执"],
        "lucky_numbers": [2, 6, 15],
        "lucky_colors": ["绿色", "粉色"],
        "health_focus": "肠胃和喉咙",
        "enemy": "天蝎座",
    },
    "双子座": {
        "date": "5.21-6.21",
        "element": "风",
        "symbol": "♊",
        "ruling_planet": "水星",
        "traits": ["聪明", "好奇", "善变", "机智"],
        "lucky_numbers": [3, 7, 14],
        "lucky_colors": ["黄色", "蓝色"],
        "health_focus": "呼吸系统和手臂",
        "enemy": "射手座",
    },
    "巨蟹座": {
        "date": "6.22-7.22",
        "element": "水",
        "symbol": "♋",
        "ruling_planet": "月亮",
        "traits": ["温柔", "敏感", "顾家", "情绪化"],
        "lucky_numbers": [2, 8, 16],
        "lucky_colors": ["白色", "银色"],
        "health_focus": "胃部和胸部",
        "enemy": "摩羯座",
    },
    "狮子座": {
        "date": "7.23-8.22",
        "element": "火",
        "symbol": "♌",
        "ruling_planet": "太阳",
        "traits": ["自信", "慷慨", "领导力", "骄傲"],
        "lucky_numbers": [1, 4, 19],
        "lucky_colors": ["金色", "橙色"],
        "health_focus": "心脏和背部",
        "enemy": "水瓶座",
    },
    "处女座": {
        "date": "8.23-9.22",
        "element": "土",
        "symbol": "♍",
        "ruling_planet": "水星",
        "traits": ["细致", "分析", "完美主义", "挑剔"],
        "lucky_numbers": [5, 6, 14],
        "lucky_colors": ["灰色", "米色"],
        "health_focus": "消化系统和神经系统",
        "enemy": "双鱼座",
    },
    "天秤座": {
        "date": "9.23-10.22",
        "element": "风",
        "symbol": "♎",
        "ruling_planet": "金星",
        "traits": ["优雅", "公正", "社交", "犹豫"],
        "lucky_numbers": [2, 7, 11],
        "lucky_colors": ["粉色", "蓝色"],
        "health_focus": "肾脏和腰部",
        "enemy": "白羊座",
    },
    "天蝎座": {
        "date": "10.23-11.22",
        "element": "水",
        "symbol": "♏",
        "ruling_planet": "冥王星",
        "traits": ["神秘", "洞察", "强烈", "多疑"],
        "lucky_numbers": [8, 9, 18],
        "lucky_colors": ["深红", "黑色"],
        "health_focus": "生殖系统和排泄系统",
        "enemy": "金牛座",
    },
    "射手座": {
        "date": "11.23-12.21",
        "element": "火",
        "symbol": "♐",
        "ruling_planet": "木星",
        "traits": ["乐观", "自由", "冒险", "粗心"],
        "lucky_numbers": [3, 9, 21],
        "lucky_colors": ["紫色", "蓝色"],
        "health_focus": "肝脏和臀部",
        "enemy": "双子座",
    },
    "摩羯座": {
        "date": "12.22-1.19",
        "element": "土",
        "symbol": "♑",
        "ruling_planet": "土星",
        "traits": ["务实", "自律", "野心", "保守"],
        "lucky_numbers": [4, 8, 16],
        "lucky_colors": ["棕色", "黑色"],
        "health_focus": "骨骼和牙齿",
        "enemy": "巨蟹座",
    },
    "水瓶座": {
        "date": "1.20-2.18",
        "element": "风",
        "symbol": "♒",
        "ruling_planet": "天王星",
        "traits": ["独立", "创新", "理性", "叛逆"],
        "lucky_numbers": [1, 7, 22],
        "lucky_colors": ["蓝色", "银色"],
        "health_focus": "小腿和脚踝",
        "enemy": "狮子座",
    },
    "双鱼座": {
        "date": "2.19-3.20",
        "element": "水",
        "symbol": "♓",
        "ruling_planet": "海王星",
        "traits": ["浪漫", "直觉", "善良", "逃避"],
        "lucky_numbers": [3, 9, 12],
        "lucky_colors": ["绿色", "紫色"],
        "health_focus": "脚部和免疫系统",
        "enemy": "处女座",
    },
}

# ==================== 星座拼音映射（万维易源 API） ====================
CONSTELLATION_PINYIN = {
    "白羊座": "baiyang",
    "金牛座": "jinniu",
    "双子座": "shuangzi",
    "巨蟹座": "juxie",
    "狮子座": "shizi",
    "处女座": "chunv",
    "天秤座": "tiancheng",
    "天蝎座": "tiexie",
    "射手座": "sheshou",
    "摩羯座": "mojie",
    "水瓶座": "shuiping",
    "双鱼座": "shuangyu",
}

# ==================== 元素兼容性（配对算法） ====================
ELEMENT_COMPATIBILITY = {
    "火": ["火", "风"],
    "土": ["土", "水"],
    "风": ["风", "火"],
    "水": ["水", "土"],
}

# ==================== 配对关键词标签 ====================
PAIR_TAGS = {
    "same_element": "同频型",
    "compatible": "互补型",
    "challenging": "挑战型",
}

# ==================== 配对结果模板 ====================
COMPATIBILITY_RESULTS = {
    "same_element": {
        "score": "88",
        "score_range": (85, 92),
        "title": "天生一对",
        "desc": "同元素星座，天生默契，相处融洽",
    },
    "compatible": {
        "score": "77",
        "score_range": (72, 82),
        "title": "和谐配对",
        "desc": "元素互补，相互吸引，需要理解",
    },
    "challenging": {
        "score": "63",
        "score_range": (58, 68),
        "title": "需要磨合",
        "desc": "差异较大，需要更多包容和沟通",
    },
}

# ==================== 元素组合个性化描述 ====================
ELEMENT_PAIR_DESCRIPTIONS = {
    ("火", "火"): {
        "tag": "同频型",
        "desc": "热情似火，活力四射，两人都是行动派。注意控制脾气，避免正面冲突。",
    },
    ("火", "风"): {
        "tag": "互补型",
        "desc": "风助火势，相互成就。沟通顺畅，思想碰撞，一起探索新鲜事物。",
    },
    ("火", "土"): {
        "tag": "挑战型",
        "desc": "火土相克，需要耐心磨合。一个冲动一个稳重，互补成长。",
    },
    ("火", "水"): {
        "tag": "挑战型",
        "desc": "水火不容，情感冲突。需学会理解对方的表达方式，找到平衡点。",
    },
    ("土", "土"): {
        "tag": "同频型",
        "desc": "稳重踏实，细水长流。价值观一致，建立稳固长久的关系。",
    },
    ("土", "水"): {
        "tag": "互补型",
        "desc": "土水相融，相互滋养。一个提供安全感，一个给予情感支持。",
    },
    ("风", "风"): {
        "tag": "同频型",
        "desc": "思想碰撞，自由独立。保持新鲜感，给彼此足够的空间。",
    },
    ("风", "水"): {
        "tag": "挑战型",
        "desc": "风水相生，灵感迸发。但需接地气，避免过于理想化。",
    },
    ("水", "水"): {
        "tag": "同频型",
        "desc": "情感共鸣，心灵相通。默契十足，但需注意不要过度情绪化。",
    },
}

# ==================== 函数定义 ====================

def get_constellation_info(name):
    """获取星座基本信息"""
    return CONSTELLATIONS.get(name, {})


def get_element(name):
    """获取星座元素"""
    info = CONSTELLATIONS.get(name, {})
    return info.get("element", "")


def calculate_compatibility(sign1, sign2):
    """
    计算两个星座的配对指数
    
    Args:
        sign1: 星座 1 名称
        sign2: 星座 2 名称
    
    Returns:
        dict: 包含分数范围、标题、描述、标签的配对结果
    """
    elem1 = get_element(sign1)
    elem2 = get_element(sign2)
    
    if not elem1 or not elem2:
        return {
            "score": "63",
            "score_range": (58, 68),
            "title": "需要磨合",
            "desc": "相互吸引，需要更多了解",
            "tag": "挑战型",
        }
    
    if elem1 == elem2:
        pair_type = "same_element"
    elif elem2 in ELEMENT_COMPATIBILITY.get(elem1, []):
        pair_type = "compatible"
    else:
        pair_type = "challenging"
    
    template = COMPATIBILITY_RESULTS[pair_type]
    
    elem_key = (elem1, elem2) if (elem1, elem2) in ELEMENT_PAIR_DESCRIPTIONS else (elem2, elem1)
    elem_desc = ELEMENT_PAIR_DESCRIPTIONS.get(elem_key, {})
    
    desc = elem_desc.get("desc", template["desc"])
    tag = elem_desc.get("tag", PAIR_TAGS.get(pair_type, "未知"))
    
    return {
        "score": template["score"],
        "score_range": template["score_range"],
        "title": template["title"],
        "desc": desc,
        "tag": tag,
    }


def get_fortune_level(score):
    """
    根据分数获取运势等级
    
    Args:
        score: 运势分数 (0-100)
    
    Returns:
        dict: 包含等级信息的字典
    """
    score = int(score)
    
    if score >= 85:
        return {"level": "excellent", "title": "运势极佳", "advice": "把握机会，大胆行动"}
    elif score >= 70:
        return {"level": "good", "title": "运势良好", "advice": "稳步推进，注意细节"}
    elif score >= 55:
        return {"level": "average", "title": "运势平稳", "advice": "保持耐心，积蓄力量"}
    else:
        return {"level": "caution", "title": "需谨慎", "advice": "低调行事，注意休息"}


def get_all_constellations():
    """获取所有 12 星座名称列表"""
    return list(CONSTELLATIONS.keys())


def get_health_advice(constellation):
    """获取健康建议（本地补充）"""
    info = CONSTELLATIONS.get(constellation, {})
    health_focus = info.get("health_focus", "身体")
    return f"注意{health_focus}的保养"


def get_enemy_constellation(constellation):
    """获取小人星座（本地补充 - 对冲星座）"""
    info = CONSTELLATIONS.get(constellation, {})
    return info.get("enemy", "")


def get_lucky_direction(constellation):
    """获取幸运方位（本地补充）"""
    return LUCKY_DIRECTIONS.get(constellation, "中央")


def get_lucky_time(constellation):
    """获取幸运时段（本地补充）"""
    return LUCKY_TIMES.get(constellation, "12:00-14:00")


# ==================== 测试代码 ====================
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("="*50)
    print("Constellation Data Module Test (万维易源版)")
    print("="*50)
    
    print("\n测试 1: 获取狮子座信息")
    info = get_constellation_info("狮子座")
    print(f"  元素：{info.get('element')}")
    print(f"  健康关注：{info.get('health_focus')}")
    print(f"  小人星座：{info.get('enemy')}")
    
    print("\n测试 2: 星座配对测试")
    pairs = [
        ("狮子座", "白羊座"),
        ("狮子座", "双子座"),
        ("巨蟹座", "天蝎座"),
    ]
    
    for sign1, sign2 in pairs:
        result = calculate_compatibility(sign1, sign2)
        print(f"  {sign1} ♡ {sign2}: {result['score']} - {result['title']}")
    
    print("\n测试 3: 健康建议")
    for sign in ["白羊座", "金牛座", "双子座"]:
        advice = get_health_advice(sign)
        print(f"  {sign}: {advice}")
    
    print("\n测试 4: 小人星座")
    for sign in ["白羊座", "金牛座", "双子座"]:
        enemy = get_enemy_constellation(sign)
        print(f"  {sign} 的小人星座：{enemy}")
    
    print("\n" + "="*50)
    print("测试完成！")
    print("="*50)
