#!/usr/bin/env python3
"""
AI陪伴减肥 - 核心计算引擎 v2.0
功能: 热量计算、BMR计算、脂肪增量、目标步数、膳食评价、蹲起消耗、围餐计算、食物估算
输出: JSON格式供智能体解析
"""
import argparse
import json
import math
import re
from typing import Dict, List, Any, Optional, Tuple


# ============================================================
# 食物热量数据库（100g标准单位）
# ============================================================
FOOD_DATABASE = {
    # 主食类
    '米饭': {'cal': 116, 'carb': 25.9, 'unit': '小碗(150g)', 'small': 174, 'medium': 232, 'large': 348},
    '面条': {'cal': 284, 'carb': 59.5, 'unit': '小碗(200g)', 'small': 340, 'medium': 568, 'large': 852},
    '馒头': {'cal': 223, 'carb': 47.0, 'unit': '个(100g)', 'small': 167, 'medium': 223, 'large': 335},
    '包子': {'cal': 218, 'carb': 25.0, 'unit': '个(80g)', 'small': 174, 'medium': 218, 'large': 327},
    '饺子': {'cal': 242, 'carb': 26.0, 'unit': '10个(120g)', 'small': 145, 'medium': 242, 'large': 363},
    '煎饼': {'cal': 298, 'carb': 50.0, 'unit': '个(100g)', 'small': 224, 'medium': 298, 'large': 447},
    '油条': {'cal': 386, 'carb': 51.0, 'unit': '根(50g)', 'small': 193, 'medium': 386, 'large': 579},
    '面包': {'cal': 246, 'carb': 41.0, 'unit': '片(50g)', 'small': 123, 'medium': 246, 'large': 369},
    '蛋糕': {'cal': 350, 'carb': 45.0, 'unit': '块(100g)', 'small': 175, 'medium': 350, 'large': 525},
    
    # 蛋白质类
    '鸡胸肉': {'cal': 133, 'protein': 31.0, 'unit': '块(150g)', 'small': 100, 'medium': 200, 'large': 300},
    '鸡腿': {'cal': 181, 'protein': 26.0, 'unit': '个(120g)', 'small': 109, 'medium': 217, 'large': 325},
    '牛肉': {'cal': 106, 'protein': 20.0, 'unit': '份(100g)', 'small': 80, 'medium': 160, 'large': 240},
    '猪肉': {'cal': 143, 'protein': 21.0, 'unit': '份(100g)', 'small': 107, 'medium': 214, 'large': 321},
    '三文鱼': {'cal': 183, 'protein': 22.0, 'unit': '份(100g)', 'small': 138, 'medium': 275, 'large': 412},
    '虾': {'cal': 85, 'protein': 18.0, 'unit': '份(100g)', 'small': 64, 'medium': 128, 'large': 192},
    '鸡蛋': {'cal': 144, 'protein': 13.0, 'unit': '个(60g)', 'small': 72, 'medium': 144, 'large': 216},
    '豆腐': {'cal': 81, 'protein': 8.0, 'unit': '块(150g)', 'small': 91, 'medium': 122, 'large': 182},
    
    # 蔬菜类
    '西兰花': {'cal': 34, 'carb': 4.3, 'unit': '份(100g)', 'small': 25, 'medium': 51, 'large': 76},
    '菠菜': {'cal': 24, 'carb': 3.6, 'unit': '份(100g)', 'small': 18, 'medium': 36, 'large': 54},
    '青菜': {'cal': 14, 'carb': 1.5, 'unit': '份(100g)', 'small': 11, 'medium': 21, 'large': 32},
    '黄瓜': {'cal': 15, 'carb': 2.9, 'unit': '根(200g)', 'small': 18, 'medium': 30, 'large': 45},
    '番茄': {'cal': 18, 'carb': 3.5, 'unit': '个(150g)', 'small': 14, 'medium': 27, 'large': 40},
    '土豆': {'cal': 76, 'carb': 17.0, 'unit': '个(150g)', 'small': 86, 'medium': 114, 'large': 171},
    '红薯': {'cal': 99, 'carb': 20.0, 'unit': '个(150g)', 'single': 149},
    '玉米': {'cal': 112, 'carb': 23.0, 'unit': '根(150g)', 'single': 168},
    
    # 炒菜类
    '番茄炒蛋': {'cal': 120, 'carb': 5.0, 'unit': '份(200g)', 'small': 120, 'medium': 180, 'large': 240},
    '青椒肉丝': {'cal': 180, 'carb': 6.0, 'unit': '份(200g)', 'small': 135, 'medium': 270, 'large': 405},
    '宫保鸡丁': {'cal': 210, 'carb': 8.0, 'unit': '份(200g)', 'small': 158, 'medium': 315, 'large': 473},
    '红烧肉': {'cal': 280, 'carb': 5.0, 'unit': '3块(100g)', 'small': 93, 'medium': 280, 'large': 420},
    '清炒时蔬': {'cal': 60, 'carb': 4.0, 'unit': '份(200g)', 'small': 45, 'medium': 90, 'large': 135},
    '地三鲜': {'cal': 150, 'carb': 15.0, 'unit': '份(200g)', 'small': 113, 'medium': 225, 'large': 338},
    
    # 水果类
    '苹果': {'cal': 52, 'carb': 13.8, 'unit': '个(200g)', 'small': 52, 'medium': 104, 'large': 156},
    '香蕉': {'cal': 93, 'carb': 22.8, 'unit': '根(100g)', 'small': 70, 'medium': 93, 'large': 140},
    '橙子': {'cal': 47, 'carb': 11.8, 'unit': '个(150g)', 'small': 35, 'medium': 71, 'large': 106},
    '西瓜': {'cal': 30, 'carb': 7.5, 'unit': '块(500g)', 'small': 150, 'medium': 300, 'large': 600, 'basketball': 750},
    '葡萄': {'cal': 67, 'carb': 17.3, 'unit': '10颗(50g)', 'small': 34, 'medium': 67, 'large': 101},
    '草莓': {'cal': 32, 'carb': 7.7, 'unit': '10颗(150g)', 'small': 24, 'medium': 48, 'large': 72},
    
    # 饮品类
    '牛奶': {'cal': 54, 'carb': 3.4, 'unit': '盒(250ml)', 'small': 54, 'medium': 108, 'large': 162},
    '酸奶': {'cal': 72, 'carb': 10.0, 'unit': '杯(200ml)', 'small': 72, 'medium': 144, 'large': 216},
    '奶茶': {'cal': 80, 'carb': 12.0, 'unit': '杯(500ml)', 'small': 60, 'medium': 120, 'large': 180},
    '可乐': {'cal': 42, 'carb': 10.6, 'unit': '罐(330ml)', 'single': 139},
    
    # 火锅类（按人头估算）
    '火锅': {'cal': 600, 'carb': 20.0, 'unit': '人', 'small': 450, 'medium': 600, 'large': 800},
    '麻辣烫': {'cal': 400, 'carb': 30.0, 'unit': '份(500g)', 'small': 300, 'medium': 400, 'large': 600},
    
    # 零食类
    '薯片': {'cal': 548, 'carb': 50.0, 'unit': '小包(30g)', 'single': 165},
    '饼干': {'cal': 435, 'carb': 70.0, 'unit': '片(10g)', 'single': 44},
    '瓜子': {'cal': 597, 'carb': 17.0, 'unit': '把(20g)', 'single': 119},
    '花生': {'cal': 589, 'carb': 20.0, 'unit': '把(15g)', 'single': 88},
    '巧克力': {'cal': 550, 'carb': 60.0, 'unit': '块(30g)', 'single': 165},
    
    # 快餐类
    '披萨': {'cal': 266, 'carb': 33.0, 'unit': '片(100g)', 'small': 200, 'medium': 266, 'large': 400, 'quarter': 66},
    '炸鸡': {'cal': 298, 'carb': 10.0, 'protein': 26.0, 'unit': '块(100g)', 'small': 150, 'medium': 298, 'large': 450},
    '汉堡': {'cal': 295, 'carb': 24.0, 'protein': 17.0, 'unit': '个(100g)', 'small': 220, 'medium': 295, 'large': 400},
    '薯条': {'cal': 312, 'carb': 41.0, 'unit': '份(100g)', 'small': 200, 'medium': 312, 'large': 450},
    '炸薯条': {'cal': 312, 'carb': 41.0, 'unit': '份(100g)', 'small': 200, 'medium': 312, 'large': 450},
    
    # 甜品类
    '冰淇淋': {'cal': 207, 'carb': 24.0, 'unit': '份(100g)', 'small': 100, 'medium': 207, 'large': 310},
    '布丁': {'cal': 130, 'carb': 22.0, 'unit': '杯(100g)', 'single': 130},
    '蛋挞': {'cal': 277, 'carb': 30.0, 'unit': '个(50g)', 'single': 139},
}

# 份量关键词映射
PORTION_KEYWORDS = {
    # 小份
    '小': 'small', '小份': 'small', '小碗': 'small', '小个': 'small', '小把': 'small',
    # 中份
    '中': 'medium', '中份': 'medium', '中碗': 'medium', '中个': 'medium',
    # 大份 - 包含篮球等特殊描述
    '大': 'large', '大份': 'large', '大碗': 'large', '大个': 'large', '一大': 'large',
    '篮球': 'large', '篮球大小': 'large', '篮球大的': 'large', '一个': 'medium',
    # 分数描述
    '四分之一': 'quarter', '四分之': 'quarter', '1/4': 'quarter', '¼': 'quarter',
}

# 饱腹感系数
SATIETY_FACTORS = {
    6: 0.6, '六分饱': 0.6, '六成饱': 0.6,
    7: 0.7, '七分饱': 0.7, '七成饱': 0.7,
    8: 0.8, '八分饱': 0.8, '八成饱': 0.8, '八成': 0.8,
    9: 0.9, '九分饱': 0.9, '九成饱': 0.9,
    10: 1.0, '十分饱': 1.0, '十成饱': 1.0, '吃撑': 1.1,
}

# 数量词处理
NUMBER_MAP = {
    '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '半': 0.5, '个': 1, '份': 1, '碗': 1, '杯': 1, '根': 1, '块': 1,
}


def parse_number(text: str) -> float:
    """解析中文数字"""
    for cn, num in NUMBER_MAP.items():
        text = text.replace(cn, str(num))
    try:
        return float(text)
    except ValueError:
        return 1.0


# ============================================================
# 运动消耗数据库（单位：kcal/小时，基于60kg体重）
# ============================================================
EXERCISE_DATABASE = {
    '走路': {
        '慢走': {'cal_per_hour': 200, 'speed': '4km/h', 'emoji': '🚶'},
        '快走': {'cal_per_hour': 350, 'speed': '6km/h', 'emoji': '🚶‍♂️'},
        '暴走': {'cal_per_hour': 450, 'speed': '8km/h', 'emoji': '💨'},
    },
    '跑步': {
        '慢跑': {'cal_per_hour': 450, 'speed': '8km/h', 'emoji': '🏃'},
        '快跑': {'cal_per_hour': 600, 'speed': '12km/h', 'emoji': '🏃‍♂️'},
    },
    '骑行': {
        '骑行': {'cal_per_hour': 400, 'speed': '15km/h', 'emoji': '🚴'},
        '动感单车': {'cal_per_hour': 500, 'emoji': '🚴‍♂️'},
    },
    '游泳': {
        '蛙泳': {'cal_per_hour': 450, 'emoji': '🏊'},
        '自由泳': {'cal_per_hour': 550, 'emoji': '🏊‍♀️'},
        '慢游': {'cal_per_hour': 350, 'emoji': '🏊‍♂️'},
    },
    '球类': {
        '羽毛球': {'cal_per_hour': 350, 'emoji': '🏸'},
        '乒乓球': {'cal_per_hour': 280, 'emoji': '🏓'},
        '篮球': {'cal_per_hour': 450, 'emoji': '🏀'},
        '足球': {'cal_per_hour': 500, 'emoji': '⚽'},
        '网球': {'cal_per_hour': 400, 'emoji': '🎾'},
    },
    '健身': {
        '跳绳': {'cal_per_hour': 600, 'emoji': '🪢'},
        '瑜伽': {'cal_per_hour': 150, 'emoji': '🧘'},
        '普拉提': {'cal_per_hour': 250, 'emoji': '🧘‍♀️'},
        ' HIIT': {'cal_per_hour': 550, 'emoji': '💪'},
        '健身操': {'cal_per_hour': 400, 'emoji': '💃'},
    },
    '力量': {
        '蹲起': {'cal_per_hour': 300, 'emoji': '🏋️'},
        '俯卧撑': {'cal_per_hour': 250, 'emoji': '💪'},
        '平板支撑': {'cal_per_hour': 200, 'emoji': '🤸'},
        '引体向上': {'cal_per_hour': 350, 'emoji': '🏋️‍♂️'},
    },
    '日常': {
        '爬楼梯': {'cal_per_hour': 500, 'emoji': '🪜'},
        '家务': {'cal_per_hour': 200, 'emoji': '🧹'},
        '逛街': {'cal_per_hour': 250, 'emoji': '🛍️'},
    },
}


def calculate_exercise_calories(exercise_type: str, duration_min: int, weight_kg: float = 60) -> Dict:
    """
    计算运动消耗热量
    返回: 消耗热量(kcal)、等效步数
    """
    # 查找运动类型
    exercise_data = None
    for category, exercises in EXERCISE_DATABASE.items():
        if exercise_type in exercises:
            exercise_data = exercises[exercise_type]
            break
    
    if not exercise_data:
        return {'found': False, 'calories': 0, 'equivalent_steps': 0}
    
    # 按体重调整
    weight_factor = weight_kg / 60
    base_cal_per_hour = exercise_data['cal_per_hour']
    actual_cal = base_cal_per_hour * weight_factor * duration_min / 60
    
    # 计算等效步数（以快走为基准，约每步0.04kcal）
    steps_per_hour = 6000  # 快走速度
    calories_per_step = 0.04 * (weight_kg / 60)
    equivalent_steps = int(actual_cal / calories_per_step)
    
    return {
        'found': True,
        'name': exercise_type,
        'emoji': exercise_data.get('emoji', '🏃'),
        'duration_min': duration_min,
        'calories': round(actual_cal, 1),
        'equivalent_steps': equivalent_steps,
        'weight_factor': round(weight_factor, 2)
    }


def get_exercise_equivalents(target_calories: float, weight_kg: float = 60) -> List[Dict]:
    """
    获取等效运动方案
    消耗指定热量需要做哪些运动
    """
    equivalents = []
    weight_factor = weight_kg / 60
    
    for category, exercises in EXERCISE_DATABASE.items():
        for name, data in exercises.items():
            cal_per_hour = data['cal_per_hour'] * weight_factor
            duration_needed = target_calories / cal_per_hour * 60  # 分钟
            
            if duration_needed <= 120:  # 最多2小时
                equivalents.append({
                    'name': name,
                    'category': category,
                    'emoji': data.get('emoji', '🏃'),
                    'duration_min': int(duration_needed),
                    'calories': target_calories
                })
    
    # 按耗时排序
    equivalents.sort(key=lambda x: x['duration_min'])
    return equivalents[:10]  # 返回前10个最优方案


def steps_to_exercise(steps: int, weight_kg: float = 60) -> Dict[str, str]:
    """
    将步数转换为等效运动
    """
    # 步数消耗的热量
    cal_per_step = 0.04 * (weight_kg / 60)
    total_cal = steps * cal_per_step
    
    # 推荐的等效运动
    recommendations = []
    for category, exercises in EXERCISE_DATABASE.items():
        for name, data in exercises.items():
            cal_per_hour = data['cal_per_hour'] * weight_kg / 60
            duration = total_cal / cal_per_hour * 60
            
            if 10 <= duration <= 90:  # 10分钟到1.5小时
                recommendations.append({
                    'name': name,
                    'emoji': data.get('emoji', '🏃'),
                    'duration': int(duration)
                })
    
    return {
        'steps': steps,
        'calories': round(total_cal, 1),
        'recommendations': recommendations[:5]
    }


def estimate_food(food_text: str) -> Tuple[float, float, float, List[str]]:
    """
    估算食物热量
    返回: (热量kcal, 碳水g, 蛋白质g, 匹配信息)
    """
    total_cal = 0
    total_carb = 0
    total_protein = 0
    matched = []
    
    text = food_text.lower()
    
    # 尝试匹配火锅/围餐
    if '火锅' in text:
        matched.append('火锅')
        portions = {'small': 450, 'medium': 600, 'large': 800}
        portion = 'medium'
        for kw, size in PORTION_KEYWORDS.items():
            if kw in text:
                portion = size
                break
        total_cal = portions.get(portion, 600)
        total_carb = 20
    
    # 尝试匹配数据库食物
    for name, data in FOOD_DATABASE.items():
        if name in text:
            cal = data.get('cal', 0)
            
            # 判断份量
            portion_key = 'medium'  # 默认中份
            for kw, size in PORTION_KEYWORDS.items():
                if kw in text:
                    portion_key = size
                    break
            
            # 特殊处理：西瓜+篮球描述 → 使用basketball份量
            if 'basketball' in data and ('篮球' in text or '西瓜' in text and '大' in text):
                portion_key = 'basketball'
            
            # 处理数量
            num_match = re.search(r'([零一二两三四五六七八九十半]+|[0-9.]+)\s*[个碗份杯根块把]?', text)
            quantity = 1
            if num_match:
                quantity = parse_number(num_match.group(1))
            
            # 处理分数描述（如四分之一披萨）
            if portion_key == 'quarter' and 'quarter' in data:
                food_cal = data['quarter']
            elif 'single' in data:
                food_cal = data['single'] * quantity
            else:
                food_cal = data.get(portion_key, data.get('cal', 0)) * quantity
            
            total_cal += food_cal
            total_carb += data.get('carb', 0) * quantity / 10
            total_protein += data.get('protein', 0) * quantity / 10
            matched.append(f"{name}({portion_key}×{quantity})")
    
    # 如果没有匹配到，返回默认估算
    if total_cal == 0:
        # 通用估算：每餐约500-800kcal
        matched.append('通用估算')
        total_cal = 600
    
    return total_cal, total_carb, total_protein, matched


def calculate_step_length(height_cm: float) -> float:
    """计算步长(cm) - 优化公式"""
    return height_cm / 4 + 30


def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """计算基础代谢率(BMR)"""
    if gender.lower() in ['female', 'f', '女']:
        return 655 + 9.6 * weight_kg + 1.8 * height_cm - 4.7 * age
    else:
        return 66 + 13.7 * weight_kg + 5 * height_cm - 6.8 * age


def calculate_tdee(bmr: float, activity_level: str = 'sedentary') -> float:
    """计算每日总消耗(TDEE)
    
    活动系数:
    - 久坐(sedentary): 1.2
    - 轻度活动(light): 1.375
    - 中度活动(moderate): 1.55
    - 高强度(active): 1.725
    """
    activity_coefficients = {
        'sedentary': 1.2,   # 久坐少动
        'light': 1.375,      # 轻度活动
        'moderate': 1.55,    # 中度活动
        'active': 1.725      # 高强度
    }
    coeff = activity_coefficients.get(activity_level, 1.2)
    return bmr * coeff


def calculate_calorie_diff(total_calories: float, tdee: float) -> float:
    """计算净热量差: 净热量差 = 摄入总热量 × 0.9 - TDEE
    考虑食物热效应(TEF约10%)后的净热量
    """
    net_calories = total_calories * 0.9  # 扣除食物热效应
    return net_calories - tdee


def calculate_fat_change(calorie_diff: float) -> float:
    """计算脂肪增量(克)，负数表示减脂
    公式: F = 净热量差 / 7700 × 1000
    依据: 1kg脂肪 ≈ 7700kcal
    """
    return calorie_diff / 7700 * 1000


def calculate_calories_per_1000_steps(weight_kg: float) -> float:
    """计算每千步消耗热量
    公式: 体重kg × 0.42
    """
    return weight_kg * 0.42


def calculate_target_steps(calorie_diff: float, weight_kg: float, max_steps: int = 12000) -> Dict[str, Any]:
    """计算目标步数（热量差→步数闭环核心）
    
    【核心逻辑】昨日热量差 = 今日目标步数
    
    热量差的来源：
    - 热量差 = 昨日摄入热量 × 0.9（TEF） - TDEE
    
    热量差 → 步数转换：
    - 每千步消耗 = 体重 × 0.42 kcal
    - 热量差 > 0（超标）：需要额外走路消耗
    - 热量差 ≤ 0（缺口/平衡）：只需基础保障步数
    
    公式：
    - 热量差 < 0（减脂模式）: 目标 = 基础步数(6000)
    - 热量差 = 0（平衡模式）: 目标 = 基础步数(6000)
    - 热量差 > 0（补偿模式）: 目标 = 基础步数 + 额外步数
    
    参数:
        calorie_diff: 净热量差（C0 = 摄入×0.9 - TDEE）
        weight_kg: 体重(kg)
        max_steps: 最大步数上限（默认12000步≈8公里）
    
    返回:
        字典包含：
        - target_steps: 目标步数
        - base_steps: 基础保障步数
        - extra_steps: 额外需要的步数
        - mode: 模式（reduce/balance/compensate）
        - calories_per_1000_steps: 每千步消耗热量
        - calories_to_burn: 需要消耗的热量（正数）
    """
    base_steps = 6000  # 基础保障步数
    calories_per_1000_steps = weight_kg * 0.42  # 每千步消耗
    
    if calorie_diff <= 0:
        # 热量缺口或平衡：只需基础步数
        return {
            'target_steps': base_steps,
            'base_steps': base_steps,
            'extra_steps': 0,
            'mode': 'reduce' if calorie_diff < 0 else 'balance',
            'calories_per_1000_steps': round(calories_per_1000_steps, 1),
            'calories_to_burn': 0,
            'mode_label': '减脂中' if calorie_diff < 0 else '平衡态',
            'mode_emoji': '📉' if calorie_diff < 0 else '⚖️',
            'reason': '热量缺口良好，基础走路即可' if calorie_diff < 0 else '吃动平衡，保持现状'
        }
    else:
        # 热量超标：基础步数 + 额外步数
        extra_1000_steps = calorie_diff / calories_per_1000_steps
        extra_steps = int(extra_1000_steps * 1000)
        calculated_steps = base_steps + extra_steps
        target_steps = min(calculated_steps, max_steps)
        
        # 如果超过上限，重新计算实际能消耗的热量
        actual_extra_steps = target_steps - base_steps
        calories_burned = actual_extra_steps * calories_per_1000_steps / 1000
        
        return {
            'target_steps': target_steps,
            'base_steps': base_steps,
            'extra_steps': actual_extra_steps,
            'mode': 'compensate',
            'calories_per_1000_steps': round(calories_per_1000_steps, 1),
            'calories_to_burn': round(calories_burned, 1),
            'mode_label': '需补偿',
            'mode_emoji': '⚠️',
            'reason': f'超标{calorie_diff:.0f}kcal，需走{actual_extra_steps}步消耗',
            'calorie_diff': calorie_diff,
            'max_reached': calculated_steps > max_steps  # 是否触发上限
        }


def calculate_squat_calories(weight_kg: float, height_m: float) -> float:
    """计算每次蹲起消耗热量(kcal)"""
    return 0.00239 * weight_kg * height_m


def calculate_squats_needed(calorie_diff: float, squat_calories: float) -> int:
    """计算达到热量差需要的蹲起次数"""
    if squat_calories <= 0:
        return 0
    return max(int(abs(calorie_diff) / squat_calories), 0)


# ============================================================
# 激励机制函数
# ============================================================
STREAK_BADGES = {
    3: {'name': '铜牌战士', 'emoji': '🥉', 'color': '#CD7F32'},
    7: {'name': '银牌达人', 'emoji': '🥈', 'color': '#C0C0C0'},
    14: {'name': '金牌冠军', 'emoji': '🥇', 'color': '#FFD700'},
    30: {'name': '钻石会员', 'emoji': '💎', 'color': '#B9F2FF'},
    60: {'name': '王者段位', 'emoji': '👑', 'color': '#FF69B4'},
    100: {'name': '传奇大师', 'emoji': '🌟', 'color': '#9400D3'},
}


def calculate_streak_badge(streak_days: int) -> Dict[str, Any]:
    """计算连续达标徽章"""
    current_badge = None
    next_badge = None
    progress = 0
    
    # 找到当前和下一个徽章
    sorted_milestones = sorted(STREAK_BADGES.keys())
    for milestone in sorted_milestones:
        if streak_days >= milestone:
            current_badge = STREAK_BADGES[milestone]
        else:
            if not next_badge:
                next_badge = {'days': milestone, **STREAK_BADGES[milestone]}
            break
    
    # 计算进度
    if next_badge:
        # 找到上一个里程碑
        prev_milestone = 0
        for m in sorted_milestones:
            if m < next_badge['days']:
                prev_milestone = m
        progress = (streak_days - prev_milestone) / (next_badge['days'] - prev_milestone)
    
    return {
        'current_badge': current_badge,
        'next_badge': next_badge,
        'progress': round(progress * 100, 1),
        'streak_days': streak_days
    }


def generate_weekly_report(daily_records: List[Dict]) -> Dict[str, Any]:
    """生成周报"""
    if not daily_records:
        return {'error': '暂无数据'}
    
    total_days = len(daily_records)
    achieved_days = sum(1 for r in daily_records if r.get('steps_achieved', False))
    total_cal_diff = sum(r.get('calorie_diff', 0) for r in daily_records)
    total_steps = sum(r.get('actual_steps', 0) for r in daily_records)
    avg_score = sum(r.get('score', 0) for r in daily_records) / total_days if total_days > 0 else 0
    
    # 体重变化
    weights = [r.get('weight_morning') for r in daily_records if r.get('weight_morning')]
    weight_change = 0
    if len(weights) >= 2:
        weight_change = weights[-1] - weights[0]
    
    # 最佳/最差日
    sorted_by_score = sorted(daily_records, key=lambda x: x.get('score', 0), reverse=True)
    best_day = sorted_by_score[0] if sorted_by_score else None
    worst_day = sorted_by_score[-1] if sorted_by_score else None
    
    return {
        'period': f"{daily_records[0].get('date', '?')} 至 {daily_records[-1].get('date', '?')}",
        'total_days': total_days,
        'achieved_days': achieved_days,
        'achieved_rate': round(achieved_days / total_days * 100, 1) if total_days > 0 else 0,
        'total_cal_diff': round(total_cal_diff, 1),
        'avg_cal_diff': round(total_cal_diff / total_days, 1) if total_days > 0 else 0,
        'total_steps': total_steps,
        'avg_steps': int(total_steps / total_days) if total_days > 0 else 0,
        'avg_score': round(avg_score, 1),
        'weight_change': round(weight_change, 2),
        'best_day': best_day,
        'worst_day': worst_day,
        'streak_days': daily_records[-1].get('streak_days', 0) if daily_records else 0
    }


def generate_monthly_report(weekly_reports: List[Dict]) -> Dict[str, Any]:
    """生成月报"""
    if not weekly_reports:
        return {'error': '暂无数据'}
    
    total_achieved = sum(w.get('achieved_days', 0) for w in weekly_reports)
    total_days = sum(w.get('total_days', 0) for w in weekly_reports)
    total_cal_diff = sum(w.get('total_cal_diff', 0) for w in weekly_reports)
    total_steps = sum(w.get('total_steps', 0) for w in weekly_reports)
    avg_score = sum(w.get('avg_score', 0) for w in weekly_reports) / len(weekly_reports) if weekly_reports else 0
    
    return {
        'total_weeks': len(weekly_reports),
        'total_days': total_days,
        'total_achieved': total_achieved,
        'achieved_rate': round(total_achieved / total_days * 100, 1) if total_days > 0 else 0,
        'total_cal_diff': round(total_cal_diff, 1),
        'total_steps': total_steps,
        'avg_score': round(avg_score, 1),
        'weight_change': sum(w.get('weight_change', 0) for w in weekly_reports),
        'best_week': max(weekly_reports, key=lambda x: x.get('avg_score', 0)) if weekly_reports else None,
        'worst_week': min(weekly_reports, key=lambda x: x.get('avg_score', 0)) if weekly_reports else None
    }


# ============================================================
# 营养补剂数据库
# ============================================================
SUPPLEMENT_DATABASE = {
    # 基础代谢类
    '基础代谢支持': {
        'desc': '提升基础代谢，加速燃脂',
        'supplements': [
            {'name': '左旋肉碱', 'dosage': '2-5g/天', 'timing': '运动前30分钟', 
             'effect': '促进脂肪燃烧，提升运动表现', 'evidence': '⭐⭐⭐⭐'},
            {'name': '咖啡因', 'dosage': '100-200mg/天', 'timing': '早晨或运动前',
             'effect': '提升代谢3-11%，抑制食欲', 'evidence': '⭐⭐⭐⭐'},
            {'name': '绿茶提取物(EGCG)', 'dosage': '500mg/天', 'timing': '分2次随餐',
             'effect': '促进脂肪氧化，增强能量消耗', 'evidence': '⭐⭐⭐'},
        ]
    },
    
    # 食欲控制类
    '食欲控制': {
        'desc': '减少饥饿感，稳定血糖',
        'supplements': [
            {'name': '白芸豆提取物', 'dosage': '500-1000mg/餐前', 'timing': '餐前10分钟',
             'effect': '阻断淀粉吸收，减少碳水摄入', 'evidence': '⭐⭐⭐'},
            {'name': '葡甘露聚糖', 'dosage': '1-3g/餐前', 'timing': '餐前30分钟配大杯水',
             'effect': '增加饱腹感，延缓胃排空', 'evidence': '⭐⭐⭐'},
            {'name': '5-HTP', 'dosage': '50-100mg/天', 'timing': '睡前或餐前',
             'effect': '提升血清素，减少情绪性进食', 'evidence': '⭐⭐'},
        ]
    },
    
    # 肌肉保护类
    '肌肉保护': {
        'desc': '防止肌肉流失，保护基础代谢',
        'supplements': [
            {'name': '支链氨基酸(BCAA)', 'dosage': '5-10g/天', 'timing': '运动前后',
             'effect': '减少肌肉分解，促进恢复', 'evidence': '⭐⭐⭐⭐'},
            {'name': '谷氨酰胺', 'dosage': '5-10g/天', 'timing': '睡前或运动后',
             'effect': '维护肠道健康，提升免疫力', 'evidence': '⭐⭐⭐'},
            {'name': 'HMB', 'dosage': '3g/天', 'timing': '分3次',
             'effect': '抑制肌肉蛋白分解', 'evidence': '⭐⭐⭐'},
        ]
    },
    
    # 营养补充类
    '营养补充': {
        'desc': '补充减肥期间容易缺乏的营养素',
        'supplements': [
            {'name': '复合维生素B', 'dosage': '1片/天', 'timing': '早餐后',
             'effect': '支持能量代谢，预防疲劳', 'evidence': '⭐⭐⭐⭐⭐'},
            {'name': '维生素D3', 'dosage': '2000-4000IU/天', 'timing': '随含脂肪的餐',
             'effect': '促进钙吸收，支持肌肉功能', 'evidence': '⭐⭐⭐'},
            {'name': 'omega-3鱼油', 'dosage': '1-2g/天', 'timing': '随餐',
             'effect': '抗炎、支持心血管健康', 'evidence': '⭐⭐⭐'},
            {'name': '镁', 'dosage': '400mg/天', 'timing': '睡前',
             'effect': '改善睡眠质量，减少肌肉痉挛', 'evidence': '⭐⭐⭐'},
            {'name': '锌', 'dosage': '15-30mg/天', 'timing': '随餐',
             'effect': '支持代谢酶功能，维持免疫', 'evidence': '⭐⭐⭐'},
        ]
    },
    
    # 水分代谢类
    '水分代谢': {
        'desc': '促进体内水分平衡，加速代谢废物排出',
        'supplements': [
            {'name': '钾', 'dosage': '1000-3500mg/天', 'timing': '分次随餐',
             'effect': '调节水分平衡，支持肌肉功能', 'evidence': '⭐⭐⭐'},
            {'name': '电解质粉', 'dosage': '按产品说明', 'timing': '大量出汗后',
             'effect': '补充钠、钾、镁等电解质', 'evidence': '⭐⭐⭐'},
        ]
    },
    
    # 皮肤紧致类
    '皮肤紧致': {
        'desc': '减少皮肤松弛，保持弹性',
        'supplements': [
            {'name': '胶原蛋白肽', 'dosage': '5-10g/天', 'timing': '睡前或运动后',
             'effect': '改善皮肤弹性，减少松弛', 'evidence': '⭐⭐⭐'},
            {'name': '维生素C', 'dosage': '500-1000mg/天', 'timing': '分2次随餐',
             'effect': '促进胶原蛋白合成，抗氧化', 'evidence': '⭐⭐⭐⭐'},
            {'name': '透明质酸', 'dosage': '100-200mg/天', 'timing': '随餐',
             'effect': '保持皮肤水分，提升弹性', 'evidence': '⭐⭐'},
        ]
    },
    
    # 情绪支持类
    '情绪支持': {
        'desc': '缓解减肥期间的情绪波动',
        'supplements': [
            {'name': '南非醉茄', 'dosage': '300-600mg/天', 'timing': '早晨或睡前',
             'effect': '降低皮质醇，减少压力性暴食', 'evidence': '⭐⭐⭐'},
            {'name': 'L-茶氨酸', 'dosage': '200mg/天', 'timing': '早晨或需要放松时',
             'effect': '减轻焦虑，提升专注力', 'evidence': '⭐⭐⭐'},
            {'name': '褪黑素', 'dosage': '0.5-3mg/天', 'timing': '睡前30分钟',
             'effect': '改善睡眠质量，促进恢复', 'evidence': '⭐⭐⭐'},
        ]
    },
    
    # 运动表现类
    '运动表现': {
        'desc': '提升运动能力，增加消耗',
        'supplements': [
            {'name': 'β-丙氨酸', 'dosage': '3-6g/天', 'timing': '分次服用',
             'effect': '提升耐力，减少疲劳', 'evidence': '⭐⭐⭐⭐'},
            {'name': '肌酸', 'dosage': '5g/天', 'timing': '训练日运动后',
             'effect': '增加力量，提升运动表现', 'evidence': '⭐⭐⭐⭐'},
            {'name': '牛磺酸', 'dosage': '1-3g/天', 'timing': '运动前',
             'effect': '提升运动耐力，促进脂肪燃烧', 'evidence': '⭐⭐⭐'},
        ]
    }
}


def get_supplement_recommendation(weight_kg: float, bmr: float, score: float, 
                                   streak_days: int, target_steps: int, 
                                   actual_steps: int, calorie_diff: float,
                                   nutrition_score: float, days_count: int = 0) -> Dict[str, Any]:
    """
    根据用户状态推荐营养补剂方案
    
    参数:
        weight_kg: 体重(kg)
        bmr: 基础代谢率
        score: 当日评分
        streak_days: 连续达标天数
        target_steps: 目标步数
        actual_steps: 实际步数
        calorie_diff: 热量差
        nutrition_score: 营养评分(0-4)
        days_count: 减肥总天数
    
    返回:
        补剂推荐方案
    """
    recommendations = {
        'must_have': [],    # 必备
        'recommended': [],   # 推荐
        'optional': [],     # 可选
        'tips': []          # 小贴士
    }
    

# ============================================================
# 科学优化函数（7项）
# ============================================================

# -------------------- 1. BMR公式优化 - Katch-McArdle --------------------
def calculate_bmr_advanced(weight_kg: float, height_cm: float, age: int, gender: str, body_fat_percent: float = None) -> float:
    """计算基础代谢率（高级版，支持体脂率修正）
    
    参数:
        weight_kg: 体重(kg)
        height_cm: 身高(cm)
        age: 年龄
        gender: 性别 'male'/'female'
        body_fat_percent: 体脂率%(可选)，如果不提供则使用简化公式
    
    返回:
        BMR(kcal/天)
    """
    if body_fat_percent is not None and 5 <= body_fat_percent <= 50:
        # Katch-McArdle公式（更精确，需要体脂率）
        lean_mass = weight_kg * (1 - body_fat_percent / 100)
        bmr = 370 + (21.6 * lean_mass)
    else:
        # Mifflin-St Jeor公式（简化版，无体脂率）
        if gender == 'female':
            bmr = 655 + (9.6 * weight_kg) + (1.8 * height_cm) - (4.7 * age)
        else:
            bmr = 66 + (13.7 * weight_kg) + (5 * height_cm) - (6.8 * age)
    
    return round(bmr, 1)


def estimate_body_fat_from_bmi(bmi: float, age: int, gender: str) -> float:
    """根据BMI估算体脂率（间接法）
    
    参数:
        bmi: 体质指数
        age: 年龄
        gender: 性别
    
    返回:
        估算体脂率%
    """
    # Deurenberg公式
    if gender == 'female':
        bf = (1.20 * bmi) + (0.23 * age) - 5.4
    else:
        bf = (1.20 * bmi) + (0.23 * age) - 16.2
    
    # 限制合理范围
    return max(5.0, min(50.0, round(bf, 1)))


# -------------------- 2. TDEE用步数反推 --------------------
def calculate_tdee_from_steps(weight_kg: float, actual_steps: int, bmr: float) -> float:
    """根据实际步数反推TDEE
    
    原理：步数反映了日常活动水平
    
    参数:
        weight_kg: 体重(kg)
        actual_steps: 实际步数
        bmr: 基础代谢率
    
    返回:
        TDEE(kcal/天)
    """
    # 每日静坐消耗 = BMR × 0.2 (约占20%)
    sedentary_burn = bmr * 0.2
    
    # 步数消耗（每千步约消耗体重×0.42kcal）
    steps_burn = actual_steps * (weight_kg * 0.42) / 1000
    
    # TDEE = BMR + 静坐消耗 + 步数消耗
    tdee = bmr + sedentary_burn + steps_burn
    
    return round(tdee, 1)


def estimate_activity_level_from_steps(actual_steps: int) -> float:
    """根据步数估算活动系数（用于参考）
    
    参数:
        actual_steps: 日均步数
    
    返回:
        活动系数
    """
    if actual_steps < 3000:
        return 1.2   # 久坐
    elif actual_steps < 6000:
        return 1.375  # 轻度
    elif actual_steps < 10000:
        return 1.55   # 中度
    else:
        return 1.725  # 高强度


# -------------------- 3. 个性化基础步数 --------------------
def calculate_personalized_base_steps(weight_kg: float, age: int, gender: str) -> int:
    """计算个性化基础步数
    
    考虑因素：
    - 年龄：年龄越大，基础步数适当减少
    - 体重：体重越大，关节负担越重，适当减少
    - 性别：男女有差异
    
    参数:
        weight_kg: 体重(kg)
        age: 年龄
        gender: 性别
    
    返回:
        个性化基础步数
    """
    base = 6000
    
    # 年龄修正：30岁为基准
    if age < 30:
        age_factor = 1.0
    elif age < 45:
        age_factor = 0.95
    elif age < 60:
        age_factor = 0.85
    else:
        age_factor = 0.75
    
    # 体重修正：60kg为基准
    if weight_kg < 50:
        weight_factor = 1.0
    elif weight_kg < 80:
        weight_factor = 0.95
    elif weight_kg < 100:
        weight_factor = 0.85
    else:
        weight_factor = 0.75
    
    # 性别修正
    gender_factor = 1.0 if gender == 'male' else 0.95
    
    # 计算最终值
    final_steps = int(base * age_factor * weight_factor * gender_factor)
    
    # 限制合理范围 3000-8000
    return max(3000, min(8000, final_steps))


# -------------------- 4. 体重预测 - Logistic模型 --------------------
def predict_weight_logistic(weights: List[float], days: List[int], target_weight: float = None) -> Dict[str, Any]:
    """使用Logistic模型预测体重变化趋势
    
    Logistic模型特点：
    - 初期快速下降
    - 逐渐趋于平稳
    - 不会无限下降
    
    参数:
        weights: 历史体重列表(kg)
        days: 对应天数(从第1天开始)
        target_weight: 目标体重(可选)
    
    返回:
        预测结果字典
    """
    if len(weights) < 3:
        return {'error': '需要至少3天数据', 'predictions': []}
    
    current_weight = weights[-1]
    
    # 简单Logistic拟合（使用初始体重和当前体重估算参数）
    initial_weight = weights[0]
    
    # 估算饱和值（使用目标体重或当前体重-10kg）
    if target_weight:
        saturation = target_weight
    else:
        saturation = max(current_weight, initial_weight - 10)
    
    # 简单线性估算斜率
    if len(weights) >= 2:
        daily_change = (weights[-1] - weights[0]) / len(weights)
    else:
        daily_change = -0.1
    
    # 生成预测
    predictions = []
    for i in range(1, 29):  # 预测未来4周
        t = len(weights) + i
        # 简化的S型曲线
        if daily_change < 0:
            # 减脂趋势
            remaining = current_weight - saturation
            if remaining > 0.1:
                k = 0.1  # 衰减率
                predicted = saturation + remaining * math.exp(-k * i)
            else:
                predicted = current_weight
        else:
            predicted = current_weight
        
        predictions.append({
            'day': i,
            'date': f'+{i}天',
            'weight': round(predicted, 1)
        })
    
    # 估算达成目标时间
    goal_date = None
    if target_weight and daily_change < 0:
        remaining = current_weight - target_weight
        if remaining > 0:
            days_needed = int(remaining / abs(daily_change)) if daily_change != 0 else 999
            goal_date = f'约{days_needed}天'
    
    return {
        'current_weight': round(current_weight, 1),
        'saturation_weight': round(saturation, 1),
        'daily_change': round(daily_change, 3),
        'goal_date': goal_date,
        'predictions': predictions
    }


# -------------------- 5. 热量估算校准 --------------------
class CalorieCalibrator:
    """热量估算校准器"""
    
    def __init__(self):
        self.food_calibrations = {}  # 食物ID -> 校准因子
        self.user_feedback_log = []  # 用户反馈记录
    
    def calibrate(self, food_name: str, reported_calories: float, actual_weight_change: float, days: int) -> float:
        """根据用户反馈校准热量估算
        
        参数:
            food_name: 食物名称
            reported_calories: 报告的热量
            actual_weight_change: 实际体重变化(kg)
            days: 天数
        
        返回:
            校准后的估算因子
        """
        # 计算每日热量偏差
        expected_cal_diff = actual_weight_change * 7700 / days
        calorie_deviation = expected_cal_diff
        
        # 简单校准：调整报告热量
        if food_name not in self.food_calibrations:
            self.food_calibrations[food_name] = 1.0
        
        # 更新校准因子
        adjustment = 1.0 - (calorie_deviation / reported_calories) if reported_calories > 0 else 1.0
        self.food_calibrations[food_name] = (
            0.7 * self.food_calibrations[food_name] + 0.3 * adjustment
        )
        
        return self.food_calibrations[food_name]
    
    def get_calibrated_calorie(self, food_name: str, base_calorie: float) -> float:
        """获取校准后的热量"""
        factor = self.food_calibrations.get(food_name, 1.0)
        return round(base_calorie * factor, 1)


# -------------------- 6. 碳水量精确计算 --------------------
def calculate_carb_from_foods(foods: List[str]) -> Dict[str, float]:
    """从食物成分表精确计算碳水化合物
    
    参数:
        foods: 食物名称列表
    
    返回:
        {'total_carb_g': 总碳水(g), 'carb_ratio': 碳水比例%, 'details': {...}}
    """
    # 常见食物碳水含量(g/100g)
    CARB_DB = {
        '米饭': 28.0, '面条': 25.0, '馒头': 22.0, '面包': 40.0,
        '土豆': 17.0, '红薯': 20.0, '玉米': 19.0,
        '苹果': 13.0, '香蕉': 22.0, '橙子': 11.0,
        '鸡胸肉': 0.0, '牛肉': 0.0, '猪肉': 0.0, '鱼': 0.0, '蛋': 0.7,
        '菠菜': 3.6, '白菜': 2.0, '西兰花': 4.3, '西红柿': 3.5,
        '牛奶': 5.0, '酸奶': 9.0, '豆浆': 1.8,
        '油': 0.0, '肥肉': 0.0,
    }
    
    # 份量估算(g)
    PORTION_EST = {
        '米饭': 150, '面条': 200, '馒头': 100, '面包': 50,
        '土豆': 150, '红薯': 150, '玉米': 150,
        '苹果': 200, '香蕉': 100, '橙子': 150,
        '鸡胸肉': 150, '牛肉': 150, '猪肉': 150, '鱼': 150, '蛋': 60,
        '菠菜': 150, '白菜': 200, '西兰花': 150, '西红柿': 150,
        '牛奶': 250, '酸奶': 200, '豆浆': 300,
        '油': 10, '肥肉': 50,
    }
    
    total_carb = 0.0
    details = {}
    
    for food in foods:
        # 模糊匹配
        food_lower = food.lower()
        matched = None
        for name in CARB_DB.keys():
            if name in food_lower or food_lower in name:
                matched = name
                break
        
        if matched:
            portion = PORTION_EST.get(matched, 100)
            carb_g = CARB_DB[matched] * portion / 100
            total_carb += carb_g
            details[food] = {'carb_g': round(carb_g, 1), 'portion_g': portion}
        else:
            details[food] = {'carb_g': 0, 'portion_g': 0, 'note': '未识别'}
    
    return {
        'total_carb_g': round(total_carb, 1),
        'details': details
    }


def calculate_carb_ratio_from_calories(total_calories: float, carb_g: float) -> float:
    """计算碳水比例%
    
    参数:
        total_calories: 总热量(kcal)
        carb_g: 碳水(g)
    
    返回:
        碳水比例%
    """
    if total_calories <= 0:
        return 0.0
    # 碳水每克4kcal
    carb_calories = carb_g * 4
    return round(carb_calories / total_calories * 100, 1)


# -------------------- 7. 平台期自动识别 --------------------
def detect_plateau(weights: List[float], days: List[int], threshold: float = 0.1, window: int = 14) -> Dict[str, Any]:
    """自动识别体重平台期
    
    平台期定义：连续N天体重变化小于阈值
    
    参数:
        weights: 体重列表(kg)
        days: 天数列表
        threshold: 变化阈值(kg)，默认0.1kg
        window: 窗口天数，默认14天
    
    返回:
        平台期分析结果
    """
    if len(weights) < window:
        return {
            'is_plateau': False,
            'reason': '数据不足',
            'message': '需要至少14天数据才能判断平台期'
        }
    
    # 取最近window天的数据
    recent_weights = weights[-window:]
    recent_days = days[-window:]
    
    # 计算变化
    total_change = recent_weights[-1] - recent_weights[0]
    daily_avg_change = total_change / (len(recent_weights) - 1) if len(recent_weights) > 1 else 0
    
    # 判断是否平台期
    is_plateau = abs(total_change) < threshold
    
    # 生成建议
    suggestions = []
    if is_plateau:
        suggestions = [
            '试试变换运动方式，如从走路换成游泳',
            '调整饮食结构，增加蛋白质比例',
            '保证充足睡眠，7-8小时',
            '多喝水，促进代谢',
            '耐心坚持，平台期是正常的'
        ]
    
    return {
        'is_plateau': is_plateau,
        'period_days': window if is_plateau else 0,
        'total_change_kg': round(total_change, 2),
        'daily_avg_change_kg': round(daily_avg_change, 3),
        'start_weight': round(recent_weights[0], 1),
        'end_weight': round(recent_weights[-1], 1),
        'suggestions': suggestions,
        'message': '已进入平台期' if is_plateau else '体重仍在变化中，继续加油！'
    }


# -------------------- 科学计算主函数 --------------------
def calculate_scientific(user_info: Dict, intake_calories: float, actual_steps: int, 
                         weight_history: List[float] = None, carb_g: float = None,
                         target_weight: float = None) -> Dict[str, Any]:
    """综合科学计算主函数
    
    整合7项科学优化
    
    参数:
        user_info: 用户信息 {'weight', 'height', 'age', 'gender', 'body_fat_percent'}
        intake_calories: 摄入热量(kcal)
        actual_steps: 实际步数
        weight_history: 体重历史(可选)
        carb_g: 碳水克数(可选)
        target_weight: 目标体重(可选)
    
    返回:
        综合计算结果
    """
    weight = user_info.get('weight', 60)
    height = user_info.get('height', 165)
    age = user_info.get('age', 30)
    gender = user_info.get('gender', 'female')
    body_fat = user_info.get('body_fat_percent')
    
    # 1. BMR（高级版）
    bmr = calculate_bmr_advanced(weight, height, age, gender, body_fat)
    
    # 2. TDEE（用步数反推）
    tdee = calculate_tdee_from_steps(weight, actual_steps, bmr)
    
    # 3. 个性化基础步数
    base_steps = calculate_personalized_base_steps(weight, age, gender)
    
    # 4. 热量计算
    net_calorie = intake_calories * 0.9  # 扣除TEF
    calorie_diff = net_calorie - tdee
    
    # 5. 脂肪变化
    fat_change_g = calorie_diff / 7.7
    
    # 6. 目标步数（热量差→步数闭环核心）
    # 使用统一的calculate_target_steps函数，保持一致性
    steps_result = calculate_target_steps(calorie_diff, weight)
    target_steps = steps_result['target_steps']
    
    # 7. 碳水比例
    if carb_g:
        carb_ratio = calculate_carb_ratio_from_calories(intake_calories, carb_g)
    else:
        carb_ratio = 50.0  # 默认值
    
    # 8. 体重预测（如果有历史数据）
    weight_prediction = None
    if weight_history and len(weight_history) >= 3:
        days = list(range(1, len(weight_history) + 1))
        weight_prediction = predict_weight_logistic(weight_history, days, target_weight)
    
    # 9. 平台期检测（如果有历史数据）
    plateau_status = None
    if weight_history and len(weight_history) >= 14:
        days = list(range(1, len(weight_history) + 1))
        plateau_status = detect_plateau(weight_history, days)
    
    return {
        'bmr': bmr,
        'tdee': tdee,
        'net_calorie': round(net_calorie, 1),
        'calorie_diff': round(calorie_diff, 1),
        'fat_change_g': round(fat_change_g, 1),
        'base_steps': steps_result['base_steps'],
        'target_steps': target_steps,
        'extra_steps': steps_result['extra_steps'],
        'steps_mode': steps_result['mode'],
        'mode_label': steps_result['mode_label'],
        'mode_emoji': steps_result['mode_emoji'],
        'calories_per_1000_steps': steps_result['calories_per_1000_steps'],
        'calories_to_burn': steps_result.get('calories_to_burn', 0),
        'carb_ratio': carb_ratio,
        'weight_prediction': weight_prediction,
        'plateau_status': plateau_status,
        # 热量差→步数闭环核心公式
        'step_loop': {
            'formula': '昨日热量差 = 今日目标步数',
            'calorie_diff': round(calorie_diff, 1),
            'target_steps': target_steps,
            'description': steps_result['reason']
        },
        'formulas_used': {
            'bmr': 'Katch-McArdle' if body_fat else 'Mifflin-St Jeor',
            'tdee': '步数反推',
            'tef': '×0.9',
            'fat': '/7700×1000',
            'step_loop': '热量差→步数闭环'
        }
    }


# -------------------- 导出接口 --------------------
def scientific_analysis(user_info: Dict, intake_calories: float, actual_steps: int,
                       weight_history: List[float] = None, carb_g: float = None,
                       target_weight: float = None) -> str:
    """科学分析输出接口（供智能体调用）
    
    返回格式化的分析报告
    """
    result = calculate_scientific(user_info, intake_calories, actual_steps, 
                                   weight_history, carb_g, target_weight)
    
    output = f"""🔬 科学分析报告
━━━━━━━━━━━━━━━

【基础数据】
• BMR: {result['bmr']} kcal (公式: {result['formulas_used']['bmr']})
• TDEE: {result['tdee']} kcal (基于步数反推)
• 净热量: {result['net_calorie']} kcal (已扣除TEF)

【热量分析】
• 热量差: {result['calorie_diff']} kcal
• 脂肪变化: {result['fat_change_g']}g

【步数目标】
• 个性化基础: {result['base_steps']} 步
• 今日目标: {result['target_steps']} 步

【碳水摄入】
• 碳水比例: {result['carb_ratio']}%
"""
    
    if result['weight_prediction']:
        wp = result['weight_prediction']
        output += f"""
【体重预测】
• 当前体重: {wp['current_weight']} kg
• 变化趋势: {wp['daily_change']:.3f} kg/天
• {wp.get('goal_date', '继续坚持！')}
"""
    
    if result['plateau_status']:
        ps = result['plateau_status']
        output += f"""
【平台期检测】
• 状态: {'⚠️ 已进入平台期' if ps['is_plateau'] else '✅ 正常减脂中'}
• 近14天变化: {ps['total_change_kg']} kg
• 建议: {'/'.join(ps['suggestions'][:2]) if ps['is_plateau'] else '继续保持！'}
"""
    
    return output

    # 计算热量缺口百分比
    cal_deficit_pct = abs(calorie_diff) / bmr * 100 if bmr > 0 else 0
    
    # 1. 热量缺口大(>20%) → 肌肉保护类必备
    if cal_deficit_pct > 20:
        recommendations['must_have'].extend([
            {'category': '肌肉保护', 'priority': 'high',
             'reason': f'热量缺口{cal_deficit_pct:.0f}%较大，需保护肌肉',
             'supplements': SUPPLEMENT_DATABASE['肌肉保护']['supplements'][:2]}
        ])
        recommendations['must_have'].extend([
            {'category': '营养补充', 'priority': 'high',
             'reason': '减肥期间营养需求增加，需全面补充',
             'supplements': SUPPLEMENT_DATABASE['营养补充']['supplements'][:3]}
        ])
    
    # 2. 营养评分低 → 营养补充必备
    if nutrition_score < 2:
        recommendations['must_have'].extend([
            {'category': '营养补充', 'priority': 'high',
             'reason': '饮食结构不均衡，需要补充关键营养素',
             'supplements': SUPPLEMENT_DATABASE['营养补充']['supplements']}
        ])
    
    # 3. 连续达标里程碑 → 对应补剂
    milestone_supplements = {
        3: ('基础代谢支持', '连续3天达标，基础代谢正在适应，可以适当提升'),
        7: ('肌肉保护', '连续7天达标！开始需要保护肌肉，建议添加BCAA'),
        14: ('皮肤紧致', '连续14天！减肥效果显现，需要开始关注皮肤弹性'),
        30: ('综合强化', '一个月！进入关键期，建议全面补充')
    }
    
    for milestone, (category, reason) in milestone_supplements.items():
        if streak_days >= milestone:
            recommendations['recommended'].append({
                'category': category,
                'priority': 'milestone',
                'milestone': f'连续{milestone}天达标',
                'reason': reason,
                'supplements': SUPPLEMENT_DATABASE.get(category, SUPPLEMENT_DATABASE['营养补充'])['supplements']
            })
    
    # 4. 步数完成率低 → 运动表现类
    step_completion = actual_steps / target_steps if target_steps > 0 else 1
    if step_completion < 0.5 and streak_days >= 3:
        recommendations['recommended'].append({
            'category': '运动表现', 
            'priority': 'medium',
            'reason': f'步数完成率{step_completion*100:.0f}%，需要提升运动动力',
            'supplements': SUPPLEMENT_DATABASE['运动表现']['supplements'][:2]
        })
    
    # 5. 食欲控制困难 → 食欲控制类
    if score < 6:
        recommendations['recommended'].append({
            'category': '食欲控制',
            'priority': 'medium',
            'reason': '饱腹感受到挑战，需要帮助控制食欲',
            'supplements': SUPPLEMENT_DATABASE['食欲控制']['supplements'][:2]
        })
    
    # 6. 基础必备（适用于所有减肥人群）
    recommendations['optional'].append({
        'category': '基础必备',
        'priority': 'basic',
        'reason': '减肥基础支持',
        'supplements': [
            {'name': '复合维生素B', 'dosage': '1片/天', 'timing': '早餐后',
             'effect': '支持能量代谢', 'evidence': '⭐⭐⭐⭐⭐'},
            {'name': '维生素D3', 'dosage': '2000IU/天', 'timing': '随含脂肪的餐',
             'effect': '促进钙吸收', 'evidence': '⭐⭐⭐'},
            {'name': 'omega-3鱼油', 'dosage': '1g/天', 'timing': '随餐',
             'effect': '抗炎支持', 'evidence': '⭐⭐⭐'}
        ]
    })
    
    # 7. 生成小贴士
    tips = []
    if cal_deficit_pct > 25:
        tips.append('⚠️ 热量缺口较大，建议适当增加100-200kcal摄入，避免代谢适应性下降')
    if nutrition_score < 1:
        tips.append('🥗 饮食结构需改善，增加蛋白质和蔬菜比例')
    if step_completion < 0.7:
        tips.append('🚶 尝试分解步数目标，如上下班各走20分钟')
    if days_count > 14 and days_count % 7 == 0:
        tips.append('📊 本周结束前可以做一次饮食回顾，调整下周的方案')
    
    recommendations['tips'] = tips
    
    return recommendations


def format_supplement_card(recommendations: Dict[str, Any], streak_days: int, milestone_reached: bool = False) -> str:
    """格式化补剂推荐卡片"""
    card_lines = []
    
    card_lines.append("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
    card_lines.append("┃   💊 营养补剂推荐方案            ┃")
    card_lines.append("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
    
    # 里程碑提示
    if milestone_reached:
        card_lines.append(f"\n🏆 恭喜达成连续{streak_days}天目标！")
        card_lines.append("   根据你的里程碑状态，推荐以下补剂：\n")
    
    # 必备补剂
    if recommendations['must_have']:
        card_lines.append("【🔴 必备推荐】")
        for rec in recommendations['must_have']:
            card_lines.append(f"  📌 {rec['reason']}")
            for supp in rec['supplements'][:2]:
                card_lines.append(f"     • {supp['name']}: {supp['dosage']}")
                card_lines.append(f"       效果: {supp['effect']}")
            card_lines.append("")
    
    # 推荐补剂
    if recommendations['recommended']:
        card_lines.append("【🟡 推荐考虑】")
        for rec in recommendations['recommended']:
            milestone = rec.get('milestone', '')
            if milestone:
                card_lines.append(f"  🏅 {milestone} - {rec['reason']}")
            else:
                card_lines.append(f"  📌 {rec['reason']}")
            for supp in rec['supplements'][:2]:
                card_lines.append(f"     • {supp['name']}: {supp['dosage']}")
                card_lines.append(f"       效果: {supp['effect']} ({supp.get('evidence', '⭐⭐')})")
            card_lines.append("")
    
    # 可选补剂
    if recommendations['optional']:
        card_lines.append("【⚪ 可选基础包】")
        for rec in recommendations['optional']:
            card_lines.append(f"  📌 {rec['reason']}")
            for supp in rec['supplements'][:3]:
                card_lines.append(f"     • {supp['name']}: {supp['dosage']}")
            card_lines.append("")
    
    # 小贴士
    if recommendations['tips']:
        card_lines.append("【💡 使用建议】")
        for tip in recommendations['tips']:
            card_lines.append(f"  {tip}")
    
    card_lines.append("\n📝 注：补剂不能替代均衡饮食，")
    card_lines.append("   如有特殊情况请咨询医生。")
    
    return "\n".join(card_lines)


def generate_encouragement_message(score: float, streak_days: int, calorie_diff: float) -> str:
    """生成鼓励消息"""
    messages = []
    
    # 根据评分
    if score >= 9:
        messages.append("🎊 完美！今天的饮食堪称教科书级别！")
    elif score >= 7:
        messages.append("🌟 很棒！继续保持这个节奏！")
    elif score >= 5:
        messages.append("😊 还不错，明天可以做得更好！")
    elif score >= 3:
        messages.append("🤔 有进步空间，一起加油！")
    else:
        messages.append("💪 没关系！每天都是新的开始！")
    
    # 根据连续达标
    if streak_days >= 7:
        messages.append(f"🏆 连续达标{streak_days}天！太厉害了！")
    elif streak_days >= 3:
        messages.append(f"🔥 连续{streak_days}天，继续保持！")
    
    # 根据热量
    if calorie_diff < -300:
        messages.append("📉 热量缺口不错，瘦得稳稳的~")
    elif calorie_diff > 300:
        messages.append("⚠️ 今天超标了，明天注意控制哦~")
    
    return " ".join(messages)


# ============================================================
# 零食热量数据库（常见零食100g标准单位）
# ============================================================
SNACK_DATABASE = {
    # 甜点类
    '蛋糕': {'cal': 350, 'category': '甜点', 'emoji': '🍰'},
    '奶油蛋糕': {'cal': 350, 'category': '甜点', 'emoji': '🍰'},
    '慕斯': {'cal': 280, 'category': '甜点', 'emoji': '🍮'},
    '布丁': {'cal': 180, 'category': '甜点', 'emoji': '🍮'},
    '饼干': {'cal': 450, 'category': '甜点', 'emoji': '🍪'},
    '曲奇': {'cal': 500, 'category': '甜点', 'emoji': '🍪'},
    '月饼': {'cal': 400, 'category': '甜点', 'emoji': '🥮'},
    '蛋黄酥': {'cal': 380, 'category': '甜点', 'emoji': '🥮'},
    '泡芙': {'cal': 320, 'category': '甜点', 'emoji': '🥐'},
    '甜甜圈': {'cal': 400, 'category': '甜点', 'emoji': '🍩'},
    '马卡龙': {'cal': 420, 'category': '甜点', 'emoji': '🧁'},
    '冰淇淋': {'cal': 200, 'category': '甜点', 'emoji': '🍦'},
    '雪糕': {'cal': 180, 'category': '甜点', 'emoji': '🍦'},

    # 零食类
    '薯片': {'cal': 548, 'category': '零食', 'emoji': '🍟'},
    '薯条': {'cal': 312, 'category': '零食', 'emoji': '🍟'},
    '爆米花': {'cal': 387, 'category': '零食', 'emoji': '🍿'},
    '瓜子': {'cal': 600, 'category': '零食', 'emoji': '🌻'},
    '花生': {'cal': 560, 'category': '零食', 'emoji': '🥜'},
    '坚果': {'cal': 600, 'category': '零食', 'emoji': '🥜'},
    '开心果': {'cal': 560, 'category': '零食', 'emoji': '🌰'},
    '杏仁': {'cal': 580, 'category': '零食', 'emoji': '🌰'},
    '腰果': {'cal': 553, 'category': '零食', 'emoji': '🥜'},
    '巧克力': {'cal': 550, 'category': '零食', 'emoji': '🍫'},
    '士力架': {'cal': 490, 'category': '零食', 'emoji': '🍫'},
    '威化饼干': {'cal': 380, 'category': '零食', 'emoji': '🍪'},
    '肉干': {'cal': 310, 'category': '零食', 'emoji': '🥩'},
    '牛肉干': {'cal': 310, 'category': '零食', 'emoji': '🥩'},
    '猪肉铺': {'cal': 290, 'category': '零食', 'emoji': '🥩'},
    '鱿鱼丝': {'cal': 310, 'category': '零食', 'emoji': '🦑'},
    '海苔': {'cal': 350, 'category': '零食', 'emoji': '🥬'},

    # 饮品类
    '奶茶': {'cal': 250, 'category': '饮品', 'emoji': '🧋'},
    '珍珠奶茶': {'cal': 300, 'category': '饮品', 'emoji': '🧋'},
    '奶盖': {'cal': 280, 'category': '饮品', 'emoji': '🥤'},
    '拿铁': {'cal': 150, 'category': '饮品', 'emoji': '☕'},
    '卡布奇诺': {'cal': 180, 'category': '饮品', 'emoji': '☕'},
    '可乐': {'cal': 42, 'category': '饮品', 'emoji': '🥤'},
    '雪碧': {'cal': 45, 'category': '饮品', 'emoji': '🥤'},
    '橙汁': {'cal': 45, 'category': '饮品', 'emoji': '🍊'},
    '果汁': {'cal': 50, 'category': '饮品', 'emoji': '🍹'},
    '酸奶': {'cal': 72, 'category': '饮品', 'emoji': '🥛'},
    '养乐多': {'cal': 70, 'category': '饮品', 'emoji': '🥛'},
    '啤酒': {'cal': 43, 'category': '饮品', 'emoji': '🍺'},
    '白酒': {'cal': 280, 'category': '饮品', 'emoji': '🥃'},
    '红酒': {'cal': 75, 'category': '饮品', 'emoji': '🍷'},

    # 快餐类
    '炸鸡': {'cal': 300, 'category': '快餐', 'emoji': '🍗'},
    '炸鸡腿': {'cal': 280, 'category': '快餐', 'emoji': '🍗'},
    '炸鸡翅': {'cal': 260, 'category': '快餐', 'emoji': '🍗'},
    '汉堡': {'cal': 450, 'category': '快餐', 'emoji': '🍔'},
    '薯条': {'cal': 312, 'category': '快餐', 'emoji': '🍟'},
    '披萨': {'cal': 266, 'category': '快餐', 'emoji': '🍕'},
    '热狗': {'cal': 290, 'category': '快餐', 'emoji': '🌭'},
    '炸鱼': {'cal': 280, 'category': '快餐', 'emoji': '🐟'},
    '炸虾': {'cal': 290, 'category': '快餐', 'emoji': '🦐'},

    # 甜品饮品
    '珍珠': {'cal': 100, 'category': '配料', 'emoji': '🟤'},
    '芋圆': {'cal': 120, 'category': '配料', 'emoji': '🟤'},
    '波霸': {'cal': 110, 'category': '配料', 'emoji': '🟤'},
    '椰果': {'cal': 50, 'category': '配料', 'emoji': '🥥'},

    # 水果类（高糖）
    '榴莲': {'cal': 147, 'category': '水果', 'emoji': '🥭'},
    '芒果': {'cal': 65, 'category': '水果', 'emoji': '🥭'},
    '荔枝': {'cal': 71, 'category': '水果', 'emoji': '🍒'},
    '龙眼': {'cal': 60, 'category': '水果', 'emoji': '🍒'},
    '葡萄': {'cal': 67, 'category': '水果', 'emoji': '🍇'},
    '西瓜': {'cal': 30, 'category': '水果', 'emoji': '🍉'},
    '香蕉': {'cal': 93, 'category': '水果', 'emoji': '🍌'},

    # 夜宵类
    '烧烤': {'cal': 350, 'category': '夜宵', 'emoji': '🍖'},
    '烤肉': {'cal': 320, 'category': '夜宵', 'emoji': '🥓'},
    '火锅': {'cal': 300, 'category': '夜宵', 'emoji': '🍲'},
    '串串': {'cal': 280, 'category': '夜宵', 'emoji': '🍢'},
    '麻辣烫': {'cal': 200, 'category': '夜宵', 'emoji': '🍲'},
    '泡面': {'cal': 400, 'category': '夜宵', 'emoji': '🍜'},
    '关东煮': {'cal': 150, 'category': '夜宵', 'emoji': '🍢'},
    '小龙虾': {'cal': 85, 'category': '夜宵', 'emoji': '🦞'},
}


def calculate_snack_exchange(snack_name: str, quantity: float = 1.0, weight_kg: float = 60) -> Dict[str, Any]:
    """
    计算零食兑换步数
    参数:
        snack_name: 零食名称
        quantity: 数量（个/份，零食默认按1份约50g估算）
        weight_kg: 体重kg
    返回: 热量、等效步数、多种运动方案
    """
    # 查找零食
    snack_data = None
    for name, data in SNACK_DATABASE.items():
        if name in snack_name or snack_name in name:
            snack_data = data
            matched_name = name
            break
    
    if not snack_data:
        return {'found': False}
    
    # 估算一份的热量（默认50g）
    portion_grams = 50
    cal_per_gram = snack_data['cal'] / 100
    total_cal = cal_per_gram * portion_grams * quantity
    
    # 体重调整因子
    weight_factor = weight_kg / 60
    
    # 计算等效步数（以快走为基准）
    cal_per_step = 0.04 * weight_factor
    equivalent_steps = int(total_cal / cal_per_step)
    
    # 计算等效运动时间
    walk_speed = 6  # km/h，快走
    steps_per_minute = 100
    walk_minutes = equivalent_steps / steps_per_minute
    
    # 其他运动等效
    exercises = {
        '快走': int(walk_minutes),
        '慢跑': int(walk_minutes * 0.6),
        '跳绳': int(walk_minutes * 0.5),
        '游泳': int(walk_minutes * 0.7),
        '骑行': int(walk_minutes * 0.8),
        '蹲起': int(total_cal / (0.14 * weight_factor)),
    }
    
    return {
        'found': True,
        'snack_name': matched_name,
        'emoji': snack_data['emoji'],
        'category': snack_data['category'],
        'portion_grams': portion_grams * quantity,
        'calories': round(total_cal, 0),
        'equivalent_steps': equivalent_steps,
        'exercises': {k: round(v, 0) for k, v in exercises.items()},
        'weight_factor': round(weight_factor, 2)
    }


def format_snack_exchange_card(result: Dict) -> str:
    """格式化零食兑换卡片（估算，非真实记录）"""
    if not result['found']:
        return "这个零食我不太熟悉呢... 🤔 你能告诉我大概吃了多少吗？"
    
    card_lines = []
    card_lines.append(f"\n📌 【估算】根据常识估算，非真实记录")
    card_lines.append(f"{result['emoji']} {result['snack_name']} ({result['portion_grams']:.0f}g)")
    card_lines.append(f"热量约：{result['calories']:.0f} kcal 🔥")
    card_lines.append(f"\n🚶 要消耗这些热量，你需要：")
    card_lines.append(f"━━━━━━━━━━━━━━━")
    
    for exercise, minutes in result['exercises'].items():
        if exercise == '蹲起':
            card_lines.append(f"  🏋️ {exercise}：约 {minutes:.0f} 次")
        else:
            card_lines.append(f"  {exercise}：约 {minutes:.0f} 分钟")
    
    card_lines.append(f"━━━━━━━━━━━━━━━")
    
    # 判断是否值得吃
    if result['calories'] < 100:
        card_lines.append("💚 热量较低，偶尔吃吃问题不大~")
    elif result['calories'] < 200:
        card_lines.append("💛 热量中等，今天多走几步就能消耗啦！")
    elif result['calories'] < 300:
        card_lines.append("🧡 热量有点高哦，确定要吃吗？")
    else:
        card_lines.append("❤️ 高热量零食！吃之前再想想？")
    
    card_lines.append(f"\n⚠️ 注意：此为估算，如需记录请告诉我\"我吃了xxx\"")
    
    return "\n".join(card_lines)


def calculate_party_mode(meal_type: str, people_count: int = 4, weight_kg: float = 60) -> Dict[str, Any]:
    """
    计算聚餐模式热量
    参数:
        meal_type: 聚餐类型(火锅/烧烤/自助餐/炒菜)
        people_count: 用餐人数
        weight_kg: 体重
    返回: 估算热量和建议
    """
    party_calories = {
        '火锅': {'base': 600, 'emoji': '🍲', 'tips': '多点蔬菜少吃肉，蘸料少放麻酱~'},
        '烧烤': {'base': 650, 'emoji': '🍖', 'tips': '优先选瘦肉，海鲜更佳，少喝啤酒~'},
        '自助餐': {'base': 800, 'emoji': '🍽️', 'tips': '先喝汤再吃菜，细嚼慢咽~'},
        '炒菜': {'base': 500, 'emoji': '🥘', 'tips': '荤素搭配，主食减半~'},
        '日料': {'base': 400, 'emoji': '🍣', 'tips': '刺身最健康，寿司别蘸太多酱油~'},
        '韩料': {'base': 450, 'emoji': '🥘', 'tips': '烤肉适量，石锅拌饭不错~'},
        '西餐': {'base': 550, 'emoji': '🥩', 'tips': '牛排选菲力，主食换沙拉~'},
        '火锅串串': {'base': 500, 'emoji': '🍢', 'tips': '数签子算热量，蔬菜串多吃~'},
    }
    
    # 查找匹配
    data = None
    matched_type = None
    for ptype, pdata in party_calories.items():
        if ptype in meal_type or meal_type in ptype:
            data = pdata
            matched_type = ptype
            break
    
    if not data:
        data = {'base': 500, 'emoji': '🍽️', 'tips': '注意控制份量哦~'}
        matched_type = '普通聚餐'
    
    # 体重调整
    weight_factor = weight_kg / 60
    per_person_cal = data['base'] * weight_factor
    
    return {
        'meal_type': matched_type,
        'emoji': data['emoji'],
        'per_person_cal': round(per_person_cal, 0),
        'total_cal': round(per_person_cal * people_count, 0),
        'people_count': people_count,
        'tips': data['tips']
    }


def format_party_mode_card(result: Dict) -> str:
    """格式化聚餐模式卡片（估算，非真实记录）"""
    card_lines = []
    card_lines.append(f"\n📌 【估算】根据常识估算，非真实记录")
    card_lines.append(f"{result['emoji']} {result['meal_type']} 热量估算")
    card_lines.append(f"━━━━━━━━━━━━━━━")
    card_lines.append(f"👥 {result['people_count']}人用餐")
    card_lines.append(f"🍽️ 人均热量：约 {result['per_person_cal']:.0f} kcal")
    card_lines.append(f"📊 总热量：约 {result['total_cal']:.0f} kcal")
    card_lines.append(f"━━━━━━━━━━━━━━━")
    card_lines.append(f"💡 建议：{result['tips']}")
    card_lines.append(f"\n⚠️ 注意：聚餐后请告诉我\"我吃了xxx\"来记录真实数据")
    return "\n".join(card_lines)


def calculate_dynamic_adjustment(weight_change_per_week: float, current_target_steps: int, 
                                  current_bmr: float) -> Dict[str, Any]:
    """
    计算动态目标调整
    参数:
        weight_change_per_week: 每周体重变化(kg)，负数表示减重
        current_target_steps: 当前目标步数
        current_bmr: 当前基础代谢
    返回: 调整后的目标和说明
    """
    # 每周减重0.5-1kg是健康范围
    healthy_range = (-1.0, -0.5)  # 健康减重范围
    
    adjustments = {
        'too_fast': {
            'reason': '减重太快，建议调整',
            'action': '适当增加热量摄入100-200kcal',
            'step_change': -1000,
            'message': '⚠️ 减重速度过快，可能影响基础代谢，建议适当增加营养摄入~'
        },
        'too_slow': {
            'reason': '减重太慢或体重稳定',
            'action': '适当增加运动量或减少热量摄入',
            'step_change': 1000,
            'message': '💪 减重进入平台期，适当增加运动量效果更好~'
        },
        'weight_gain': {
            'reason': '体重上升',
            'action': '减少热量摄入或增加运动',
            'step_change': 1500,
            'message': '📈 体重有所上升，注意控制饮食和增加运动哦~'
        },
        'healthy': {
            'reason': '减重节奏良好',
            'action': '保持当前方案',
            'step_change': 0,
            'message': '✅ 减重节奏良好，继续保持！'
        },
        'no_data': {
            'reason': '数据不足',
            'action': '继续记录一周后再评估',
            'step_change': 0,
            'message': '📊 数据还不够，持续记录一周后再做调整评估~'
        }
    }
    
    # 判断减重状态
    if weight_change_per_week is None or weight_change_per_week == 0:
        status = 'no_data'
    elif weight_change_per_week < healthy_range[0]:
        status = 'too_fast'
    elif weight_change_per_week > healthy_range[1] and weight_change_per_week < 0:
        status = 'too_slow'
    elif weight_change_per_week >= 0:
        status = 'weight_gain'
    else:
        status = 'healthy'
    
    adjustment = adjustments[status]
    new_target = max(4000, min(20000, current_target_steps + adjustment['step_change']))
    
    return {
        'status': status,
        'current_target': current_target_steps,
        'new_target': new_target,
        'step_change': adjustment['step_change'],
        'reason': adjustment['reason'],
        'action': adjustment['action'],
        'message': adjustment['message'],
        'bmr': current_bmr,
        'weekly_cal_adjustment': -adjustment['step_change'] * 0.04 if adjustment['step_change'] != 0 else 0
    }


def format_dynamic_adjustment_card(result: Dict) -> str:
    """格式化动态调整卡片"""
    card_lines = []
    card_lines.append(f"\n📊 周目标评估")
    card_lines.append(f"━━━━━━━━━━━━━━━")
    card_lines.append(f"当前基础代谢：{result['bmr']:.0f} kcal/天")
    
    if result['step_change'] != 0:
        direction = "↑" if result['step_change'] > 0 else "↓"
        card_lines.append(f"目标步数调整：{abs(result['step_change']):,} 步 {direction}")
        card_lines.append(f"新目标：{result['new_target']:,} 步")
    else:
        card_lines.append(f"目标步数：保持 {result['current_target']:,} 步")
    
    card_lines.append(f"━━━━━━━━━━━━━━━")
    card_lines.append(result['message'])
    card_lines.append(f"📌 {result['action']}")
    
    return "\n".join(card_lines)


def format_makeup_checkin_guide() -> str:
    """生成补打卡对话引导"""
    return """
📝 补打卡流程引导

想补录之前的饮食记录吗？很简单！

请按以下格式告诉我：
━━━━━━━━━━━━━━━━━
【日期】+【早/午/晚吃了什么】

例如：
• "补录昨天：早餐粥和包子，午餐米饭和鱼，晚餐没吃"
• "上周三的记录：早上面条，中午炸鸡"
• "昨天三餐都没记，帮我补上"

━━━━━━━━━━━━━━━━━
我会帮你：
1. 估算补录的热量
2. 计算当时的脂肪变化
3. 更新你的历史数据

随时可以补打卡，别担心遗漏~ 😊
"""


def format_progress_report(daily_records: List[Dict], days: int = 7) -> str:
    """生成周报/阶段进步亮点"""
    if not daily_records:
        return "📊 数据不足，需要至少记录几天才能生成报告哦~"
    
    recent = daily_records[-days:] if len(daily_records) >= days else daily_records
    
    # 统计
    total_days = len(recent)
    achieved_days = sum(1 for r in recent if r.get('target_achieved', False))
    avg_steps = sum(r.get('actual_steps', 0) for r in recent) / total_days if total_days > 0 else 0
    
    # 体重变化
    weights = [r.get('weight_morning') for r in recent if r.get('weight_morning')]
    weight_change = weights[-1] - weights[0] if len(weights) > 1 else None
    
    # 热量统计
    avg_cal = sum(r.get('total_calories', 0) for r in recent) / total_days if total_days > 0 else 0
    
    # 评分
    scores = [r.get('score', 0) for r in recent]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # 亮点分析
    highlights = []
    if weight_change and weight_change < -0.5:
        highlights.append("🏆 体重下降明显，继续保持！")
    if avg_score >= 7:
        highlights.append("⭐ 饮食控制越来越好了！")
    if achieved_days >= total_days * 0.8:
        highlights.append("🎯 运动目标达成率高！")
    if avg_cal < 1400:
        highlights.append("⚠️ 注意热量摄入可能偏低哦~")
    
    card_lines = []
    card_lines.append(f"\n📊 {'本周' if days == 7 else f'最近{days}天'}数据回顾")
    card_lines.append(f"━━━━━━━━━━━━━━━")
    card_lines.append(f"📅 记录天数：{total_days}天")
    card_lines.append(f"✅ 达标天数：{achieved_days}天 ({achieved_days/total_days*100:.0f}%)")
    card_lines.append(f"🚶 日均步数：{avg_steps:,.0f}步")
    card_lines.append(f"🍽️ 日均热量：{avg_cal:,.0f} kcal")
    card_lines.append(f"⭐ 平均评分：{avg_score:.1f}/10")
    
    if weight_change is not None:
        arrow = "↓" if weight_change < 0 else "↑"
        card_lines.append(f"⚖️ 体重变化：{arrow}{abs(weight_change):.1f}kg")
    
    card_lines.append(f"━━━━━━━━━━━━━━━")
    
    if highlights:
        card_lines.append("🌟 本周亮点：")
        for h in highlights:
            card_lines.append(f"  {h}")
    
    # 下周建议
    if avg_score < 6:
        card_lines.append(f"💡 下周建议：注意增加蛋白质和蔬菜摄入~")
    elif achieved_days < total_days * 0.5:
        card_lines.append(f"💡 下周建议：尝试分解步数目标，分散完成~")
    else:
        card_lines.append(f"💡 下周建议：保持当前节奏，你已经很棒了！")
    
    return "\n".join(card_lines)


# ============================================================
# 历史分析函数
# ============================================================
def analyze_weight_trend(daily_records: List[Dict], days: int = 7) -> Dict[str, Any]:
    """分析体重趋势"""
    recent = daily_records[-days:] if len(daily_records) >= days else daily_records
    weights = [(r.get('date'), r.get('weight_morning')) for r in recent if r.get('weight_morning')]
    
    if len(weights) < 2:
        return {'trend': 'insufficient_data', 'change': 0, 'data': weights}
    
    changes = []
    for i in range(1, len(weights)):
        if weights[i][1] and weights[i-1][1]:
            changes.append(weights[i][1] - weights[i-1][1])
    
    avg_change = sum(changes) / len(changes) if changes else 0
    total_change = weights[-1][1] - weights[0][1] if weights[-1][1] and weights[0][1] else 0
    
    # 判断趋势
    if avg_change < -0.1:
        trend = '下降 📉'
    elif avg_change > 0.1:
        trend = '上升 📈'
    else:
        trend = '平稳 ➡️'
    
    return {
        'trend': trend,
        'avg_change_per_day': round(avg_change, 2),
        'total_change': round(total_change, 2),
        'data': weights
    }


def analyze_calorie_trend(daily_records: List[Dict], days: int = 7) -> Dict[str, Any]:
    """分析热量趋势"""
    recent = daily_records[-days:] if len(daily_records) >= days else daily_records
    data = [(r.get('date'), r.get('total_calories', 0), r.get('target_steps', 0), 
             r.get('actual_steps', 0)) for r in recent]
    
    if not data:
        return {'trend': 'insufficient_data'}
    
    avg_cal = sum(d[1] for d in data) / len(data)
    avg_target = sum(d[2] for d in data) / len(data)
    avg_actual = sum(d[3] for d in data) / len(data)
    completion_rate = avg_actual / avg_target * 100 if avg_target > 0 else 0
    
    return {
        'avg_daily_calories': round(avg_cal, 1),
        'avg_target_steps': int(avg_target),
        'avg_actual_steps': int(avg_actual),
        'completion_rate': round(completion_rate, 1),
        'data': data
    }


def evaluate_diet(total_calories: float, bmr: float, carb_ratio: float,
                  food_items: List[Dict[str, Any]], food_count: int) -> Dict[str, Any]:
    """膳食评价（10分制）+ 具体建议"""
    scores = {'nutrition': 0.0, 'calorie_control': 0.0, 'carb_ratio': 0.0, 'diversity': 0.0}
    suggestions = []
    
    # 营养均衡度（4分）
    protein_keywords = ['鸡', '肉', '鱼', '蛋', '豆', '奶', '蛋白', '三文', '虾', '牛', '猪']
    carb_keywords = ['米', '面', '馒', '包', '面', '土', '玉', '薯', '红']
    veg_keywords = ['菜', '蔬', '青', '西兰', '菠菜', '番', '黄', '茄']
    
    has_protein = any(any(k in item.get('name', '') for k in protein_keywords) for item in food_items if food_items)
    has_carb = any(any(k in item.get('name', '') for k in carb_keywords) for item in food_items if food_items)
    has_veg = any(any(k in item.get('name', '') for k in veg_keywords) for item in food_items if food_items)
    
    if has_protein and has_veg:
        scores['nutrition'] = 4.0
    elif has_protein:
        scores['nutrition'] = 2.5
        suggestions.append("加点蔬菜更营养均衡~")
    elif has_veg:
        scores['nutrition'] = 2.0
        suggestions.append("记得补充蛋白质哦，鸡胸肉、鱼虾都是好选择~")
    else:
        scores['nutrition'] = 1.0
        suggestions.append("蔬菜和蛋白质都要有才更健康！")
    
    # 总热量控制（3分）
    calorie_ratio = total_calories / bmr
    if 0.85 <= calorie_ratio <= 1.15:
        scores['calorie_control'] = 3.0
    elif 0.7 <= calorie_ratio < 0.85:
        scores['calorie_control'] = 2.5
        suggestions.append("吃得有点少哦，长期会掉基础代谢~")
    elif 1.15 < calorie_ratio <= 1.3:
        scores['calorie_control'] = 2.0
        suggestions.append("热量稍微超标，动一动就平衡啦~")
    elif calorie_ratio > 1.3:
        scores['calorie_control'] = 1.0
        suggestions.append("今天吃多了！晚上多走8000步弥补一下~")
    else:
        scores['calorie_control'] = 1.5
        suggestions.append("摄入严重不足，小心基础代谢下降！")
    
    # 碳水比例（2分）
    if 45 <= carb_ratio <= 55:
        scores['carb_ratio'] = 2.0
    elif 40 <= carb_ratio < 45 or 55 < carb_ratio <= 60:
        scores['carb_ratio'] = 1.5
        suggestions.append("碳水比例可以再优化一下~")
    elif 30 <= carb_ratio < 40 or 60 < carb_ratio <= 70:
        scores['carb_ratio'] = 1.0
        suggestions.append("碳水比例偏差有点大，需要调整！")
    else:
        scores['carb_ratio'] = 0.5
        suggestions.append("碳水要么太多要么太少，明天注意调整主食量！")
    
    # 食物多样性（1分）
    scores['diversity'] = min(1.0, food_count / 5.0)
    if food_count < 3:
        suggestions.append("食物种类太单一了，建议每天吃够5种以上~")
    
    total_score = sum(scores.values())
    
    return {
        'total_score': round(total_score, 1),
        'nutrition': f"{scores['nutrition']}/4",
        'calorie_control': f"{scores['calorie_control']}/3",
        'carb_ratio': f"{scores['carb_ratio']}/2",
        'diversity': f"{scores['diversity']}/1",
        'suggestions': suggestions[:3]  # 最多3条建议
    }


def generate_summary_card(user_info: Dict, calc_results: Dict,
                          exercise: Dict, evaluation: Dict, foods: List[str]) -> str:
    """生成总结卡片 - 优化阅读体验"""
    gender_display = "女" if str(user_info.get('gender', '')).lower() in ['female', 'f', '女'] else "男"
    fat_change_g = calc_results['fat_change_g']  # 单位已经是克
    
    # 根据热量差显示不同状态
    if calc_results['calorie_diff'] > 0:
        diff_emoji = "📈"
        diff_text = f"超标 +{calc_results['calorie_diff']:.0f} kcal"
        diff_status = "need_exercise"
    else:
        diff_emoji = "📉"
        diff_text = f"缺口 {abs(calc_results['calorie_diff']):.0f} kcal"
        diff_status = "good"
    
    # 根据脂肪变化显示
    if fat_change_g > 0:
        fat_emoji = "🥺"
        fat_text = f"+{fat_change_g:.0f}g (会长胖哦~)"
    else:
        fat_emoji = "🎉"
        fat_text = f"{fat_change_g:.0f}g (在减脂呢~)"
    
    # 根据评分显示星级
    total = evaluation['total_score']
    stars = "⭐" * int(total // 2) + ("🌙" if total % 2 else "")
    
    # 评分详情emoji
    nutrition_full = int(float(evaluation['nutrition'].split('/')[0]))
    calorie_full = int(float(evaluation['calorie_control'].split('/')[0]))
    carb_full = int(float(evaluation['carb_ratio'].split('/')[0]))
    diversity_full = int(float(evaluation['diversity'].split('/')[0]))
    
    nutrition_bar = "▓" * nutrition_full + "░" * (4 - nutrition_full)
    calorie_bar = "▓" * calorie_full + "░" * (3 - calorie_full)
    carb_bar = "▓" * carb_full + "░" * (2 - carb_full)
    diversity_bar = "▓" * diversity_full + "░" * (1 - diversity_full)
    
    card = f"""
╭─────────────────────────────────────────╮
│  🌟  🌟  AI陪伴减肥报告  🌟  🌟          │
╰─────────────────────────────────────────╯

👤 【基本档案】
   身高: {user_info['height']}cm  体重: {user_info['weight']}kg
   年龄: {user_info['age']}岁  性别: {gender_display}

🍽️ 【今日饮食】
   食物: {', '.join(foods[:4])}{'...' if len(foods) > 4 else ''}
   热量: {calc_results['total_calories']:.0f} kcal 💫
   碳水: {calc_results['carb_ratio']:.0f}% 📊

╭─────────────────────────────────────────╮
│  {diff_emoji} 热量状态: {diff_text}             │
│  {fat_emoji} 脂肪变化: {fat_text}              │
╰─────────────────────────────────────────╯

🔥 【代谢数据】
   🫀 基础代谢(BMR): {calc_results['bmr']:.0f} kcal/天
   ⚡ 总消耗(TDEE): {calc_results['tdee']:.0f} kcal/天 (活动系数: {calc_results.get('activity_level', 'sedentary')})
   📐 步长: {calc_results['step_length_cm']:.1f} cm
   🦶 每千步消耗: {calc_results['cal_per_1000_steps']:.1f} kcal

👟 【今日目标】
   🚶 建议步数: {calc_results['target_steps']:,} 步
   🏋️ 蹲起消耗: {exercise['squats_needed']:,} 次
      (每次 {exercise['squat_calories']:.3f} kcal)

╭─────────────────────────────────────────╮
│  {stars} 综合评分: {total}/10                    │
├─────────────────────────────────────────┤
│  🥗 营养均衡  [{nutrition_bar}] {evaluation['nutrition']}   │
│  🔥 热量控制  [{calorie_bar}] {evaluation['calorie_control']}   │
│  🍞 碳水比例  [{carb_bar}] {evaluation['carb_ratio']}   │
│  🌈 食物多样  [{diversity_bar}] {evaluation['diversity']}   │
╰─────────────────────────────────────────╯
"""
    return card


def generate_daily_summary(user_info: Dict, calc_results: Dict,
                           exercise: Dict, evaluation: Dict, 
                           foods: List[str], streak_days: int = 0,
                           weight_change: float = 0,
                           target_steps: int = 6000) -> str:
    """生成日终总结卡片 - 优化版模板"""
    from datetime import datetime
    
    gender_display = "女" if str(user_info.get('gender', '')).lower() in ['female', 'f', '女'] else "男"
    fat_change_g = calc_results['fat_change_g']  # 单位已经是克
    today = datetime.now().strftime('%Y年%m月%d日')
    
    # 热量差状态
    if calc_results['calorie_diff'] > 0:
        diff_emoji = "📈"
        diff_text = f"超标 +{calc_results['calorie_diff']:.0f} kcal"
    elif calc_results['calorie_diff'] < -200:
        diff_emoji = "📉"
        diff_text = f"缺口 {abs(calc_results['calorie_diff']):.0f} kcal"
    else:
        diff_emoji = "📊"
        diff_text = f"吃动平衡"
    
    # 脂肪变化状态
    if fat_change_g > 0:
        fat_emoji = "🥺"
        fat_text = f"+{fat_change_g:.0f}g"
    else:
        fat_emoji = "🎉"
        fat_text = f"{fat_change_g:.0f}g"
    
    # 步数
    actual_steps = exercise.get('actual_steps', 0)
    
    # 热量
    intake = calc_results['total_calories']
    bmr = calc_results['bmr']
    
    total = evaluation['total_score']
    
    card = f"""
╭─────────────────────────────────────────╮
│  🌟 今日营养处方 🌟                     │
│  📅 {today}                      │
╰─────────────────────────────────────────╯

【🍽️ 今日饮食】
• 食物: {', '.join(foods[:5])}{'...' if len(foods) > 5 else ''}
• 今日总热量: {intake:.0f} kcal
• 碳水比例: {calc_results['carb_ratio']:.0f}%

【🔥 今日运动】
• 步数: {actual_steps:,} 步
• 运动消耗: 约 {exercise.get('exercise_calories', 0):.0f} kcal

【📊 热量分析】
• 摄入热量: {intake:.0f} kcal
• 热量状态: {diff_emoji} {diff_text}
• 脂肪变化: {fat_emoji} 约 {fat_text}

【⚖️ 体重追踪】
• 当前体重: {user_info['weight']:.1f} kg
• 累计减重: ↓ {abs(weight_change):.2f} kg

【⭐ 今日评分】{total:.1f}/10
┌─────────────┬──────────┬─────┐
│  营养均衡   │ {evaluation['nutrition']}  │ 满 │
│  热量控制   │ {evaluation['calorie_control']}  │ 满 │
│  碳水比例   │ {evaluation['carb_ratio']}  │ 满 │
│  食物多样   │ {evaluation['diversity']}  │ 满 │
└─────────────┴──────────┴─────┘

【🎯 明日目标】
• 步数目标: {target_steps:,} 步
• 体重打卡: 明早空腹
• 继续保持健康饮食

---

💡 Kite小结：{'今天表现很棒！' if total >= 8 else '今天还不错，明天继续加油！'}
继续坚持，向目标冲刺！💪

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*本建议仅供日常参考，效果因人而异*
"""
    return card


def generate_html_prescription(user_info: Dict, calc_results: Dict,
                                exercise: Dict, evaluation: Dict,
                                foods: List[str], streak_days: int = 0,
                                weight_change: float = 0,
                                target_steps: int = 6000,
                                supplement_recommendations: List[Dict] = None) -> str:
    """生成HTML格式的【营养处方】"""
    from datetime import datetime
    
    fat_change_g = calc_results.get('fat_change_g', 0)
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][today.weekday()]
    
    intake = calc_results.get('total_calories', 0)
    actual_steps = exercise.get('actual_steps', 0)
    total = evaluation.get('total_score', 0)
    stars = "⭐" * int(total) + "🌙" * (10 - int(total))
    
    # 营养建议生成
    advice_items = []
    
    # 基于评分生成建议
    nutrition_score = float(evaluation.get('nutrition', '0/4').split('/')[0])
    diversity_score = float(evaluation.get('diversity', '0/1').split('/')[0])
    
    if nutrition_score < 2:
        advice_items.append({'icon': '🥗', 'text': '蛋白质摄入不足，建议增加肉类、蛋类或豆制品'})
    if diversity_score < 0.5:
        advice_items.append({'icon': '🌈', 'text': '食物种类单一，建议增加蔬菜和水果'})
    if calc_results.get('carb_ratio', 50) < 40:
        advice_items.append({'icon': '🍞', 'text': '碳水比例偏低，可适当增加主食摄入'})
    elif calc_results.get('carb_ratio', 50) > 60:
        advice_items.append({'icon': '🍞', 'text': '碳水比例偏高，建议减少精制碳水'})
    
    if not advice_items:
        advice_items.append({'icon': '✅', 'text': '饮食结构良好，继续保持！'})
    
    # 基于连续达标天数生成补剂推荐
    if streak_days >= 30:
        supplement_items = supplement_recommendations or [
            {'name': '复合维生素B族', 'dose': '1片/天', 'reason': '长期热量控制需补充'},
            {'name': '维生素D3', 'dose': '2000IU/天', 'reason': '支持代谢和骨骼健康'},
            {'name': 'Omega-3鱼油', 'dose': '1000mg/天', 'reason': '抗炎和心血管保护'},
            {'name': '镁元素', 'dose': '400mg/天', 'reason': '改善睡眠和肌肉恢复'},
            {'name': '左旋肉碱', 'dose': '2g/天', 'reason': '加速脂肪燃烧'}
        ]
    elif streak_days >= 14:
        supplement_items = supplement_recommendations or [
            {'name': '支链氨基酸(BCAA)', 'dose': '5g/天', 'reason': '保护肌肉不流失'},
            {'name': '复合维生素', 'dose': '1片/天', 'reason': '弥补饮食限制造成的营养缺口'},
            {'name': '左旋肉碱', 'dose': '2g/天', 'reason': '辅助脂肪代谢'}
        ]
    elif streak_days >= 7:
        supplement_items = supplement_recommendations or [
            {'name': '乳清蛋白', 'dose': '20g/天', 'reason': '补充优质蛋白'},
            {'name': '复合维生素B', 'dose': '1片/天', 'reason': '支持能量代谢'}
        ]
    elif streak_days >= 3:
        supplement_items = supplement_recommendations or [
            {'name': '电解质粉', 'dose': '适量', 'reason': '运动后补充流失矿物质'}
        ]
    else:
        supplement_items = supplement_recommendations or [
            {'name': '暂无推荐', 'dose': '-', 'reason': '先建立健康的饮食习惯'}
        ]
    
    advice_html = ''.join([f'<li><span>{a["icon"]}</span> {a["text"]}</li>' for a in advice_items])
    supplement_html = ''.join([
        f'<div class="supplement-item"><div class="supplement-name">* {s["name"]}</div><div class="supplement-dose">{s["dose"]}</div><div class="supplement-reason">{s["reason"]}</div></div>'
        for s in supplement_items
    ])
    
    kite_tip = '今天表现很棒！继续保持~' if total >= 8 else '今天还不错，明天继续加油！' if total >= 6 else '需要调整一下饮食和运动计划哦~'
    calorie_diff_ok = calc_results.get('calorie_diff', 0) <= 0
    steps_ok = actual_steps >= target_steps * 0.8
    fat_text = '克 (减脂中~)' if fat_change_g < 0 else '克'
    calorie_diff_green = '#00b894' if calorie_diff_ok else '#ff7675'
    steps_ok_green = '#00b894' if steps_ok else '#ff7675'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>营养处方 - {date_str}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 15px; }}
.container {{ max-width: 440px; margin: 0 auto; }}
.header {{ background: rgba(255,255,255,0.98); border-radius: 20px 20px 0 0; padding: 25px; text-align: center; box-shadow: 0 -5px 20px rgba(0,0,0,0.1); }}
.header h1 {{ color: #667eea; font-size: 26px; font-weight: 700; margin-bottom: 8px; }}
.header .date {{ color: #888; font-size: 14px; }}
.content {{ background: rgba(255,255,255,0.98); padding: 15px; }}
.calorie-card {{ background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 16px; padding: 20px; color: white; text-align: center; margin-bottom: 15px; }}
.calorie-card .title {{ font-size: 12px; opacity: 0.8; margin-bottom: 5px; }}
.calorie-card .number {{ font-size: 48px; font-weight: 700; }}
.calorie-card .unit {{ font-size: 16px; opacity: 0.8; }}
.calorie-card .carb {{ font-size: 14px; margin-top: 10px; opacity: 0.9; }}
.data-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }}
.data-card {{ background: linear-gradient(135deg, #f8f9fa, #fff); border-radius: 12px; padding: 15px; text-align: center; border: 1px solid #eee; }}
.data-card.highlight {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
.data-card .label {{ font-size: 11px; color: #888; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 5px; }}
.data-card.highlight .label {{ color: rgba(255,255,255,0.8); }}
.data-card .value {{ font-size: 24px; font-weight: 700; color: #333; }}
.data-card.highlight .value {{ color: white; }}
.data-card .unit {{ font-size: 12px; color: #666; }}
.data-card.highlight .unit {{ color: rgba(255,255,255,0.8); }}
.score-card {{ background: #fff; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 15px; border: 1px solid #eee; }}
.score-card .label {{ font-size: 12px; color: #888; margin-bottom: 10px; }}
.score-card .number {{ font-size: 56px; font-weight: 700; background: linear-gradient(135deg, #f6d365, #fda085); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.score-card .max {{ font-size: 20px; color: #888; }}
.score-card .stars {{ font-size: 20px; margin-top: 5px; }}
.progress-section {{ background: #f8f9fa; border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
.section-title {{ font-size: 13px; font-weight: 600; color: #667eea; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
.progress-list {{ list-style: none; }}
.progress-list li {{ padding: 8px 0; font-size: 14px; color: #555; border-bottom: 1px solid #eee; display: flex; align-items: center; gap: 8px; }}
.progress-list li:last-child {{ border-bottom: none; }}
.advice-card {{ background: linear-gradient(135deg, #fff9e6, #fff); border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #f39c12; }}
.advice-list {{ list-style: none; }}
.advice-list li {{ padding: 8px 0; font-size: 14px; color: #555; display: flex; align-items: flex-start; gap: 8px; }}
.supplement-card {{ background: linear-gradient(135deg, #e8f5e9, #fff); border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 4px solid #00b894; }}
.supplement-item {{ background: white; border-radius: 8px; padding: 10px; margin-bottom: 8px; }}
.supplement-item:last-child {{ margin-bottom: 0; }}
.supplement-name {{ font-weight: 600; color: #333; font-size: 14px; }}
.supplement-dose {{ font-size: 12px; color: #667eea; margin: 3px 0; }}
.supplement-reason {{ font-size: 12px; color: #888; }}
.target-card {{ background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 16px; padding: 25px; color: white; text-align: center; margin-bottom: 15px; }}
.target-card .label {{ font-size: 14px; opacity: 0.9; }}
.target-card .number {{ font-size: 48px; font-weight: 700; margin: 5px 0; }}
.target-card .unit {{ font-size: 16px; opacity: 0.8; }}
.kite-card {{ background: #fef9e7; border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
.kite-card .title {{ font-size: 13px; font-weight: 600; color: #f39c12; margin-bottom: 5px; }}
.kite-card .text {{ font-size: 14px; color: #555; line-height: 1.5; }}
.footer {{ background: rgba(255,255,255,0.95); border-radius: 0 0 20px 20px; padding: 15px; text-align: center; font-size: 11px; color: #999; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>营养处方</h1>
    <div class="date">{date_str} {weekday}</div>
  </div>
  
  <div class="content">
    <div class="calorie-card">
      <div class="title">【总 热 量】</div>
      <div class="number">{intake:.0f}</div>
      <div class="unit">千卡</div>
      <div class="carb">碳水比例约 {calc_results.get('carb_ratio', 0):.0f}%</div>
    </div>
    
    <div class="data-grid">
      <div class="data-card">
        <div class="label">【最新体重】</div>
        <div class="value">{user_info.get('weight', 0):.1f}</div>
        <div class="unit">公斤</div>
      </div>
      <div class="data-card">
        <div class="label">【目标步数】</div>
        <div class="value">{target_steps:,}</div>
        <div class="unit">步</div>
      </div>
      <div class="data-card highlight">
        <div class="label">【脂肪增量】</div>
        <div class="value">{fat_change_g:.0f}</div>
        <div class="unit">{fat_text}</div>
      </div>
      <div class="data-card highlight">
        <div class="label">【今日得分】</div>
        <div class="value">{total:.1f}</div>
        <div class="unit">分</div>
      </div>
    </div>
    
    <div class="score-card">
      <div class="label">综合评分</div>
      <div class="number">{total:.1f}<span class="max">/10</span></div>
      <div class="stars">{stars}</div>
    </div>
    
    <div class="progress-section">
      <div class="section-title">📈 进步亮点</div>
      <ul class="progress-list">
        <li><span style="color:{calorie_diff_green}">{'V' if calorie_diff_ok else '!'}</span> 热量控制{'良好' if calorie_diff_ok else '需注意'}</li>
        <li><span style="color:{steps_ok_green}">{'V' if steps_ok else '!'}</span> 步数{'达标' if steps_ok else '可提高'}</li>
        <li><span style="color: #00b894;">V</span> 连续达标 {streak_days} 天</li>
      </ul>
    </div>
    
    <div class="advice-card">
      <div class="section-title">💡 营养建议</div>
      <ul class="advice-list">
        {advice_html}
      </ul>
    </div>
    
    <div class="supplement-card">
      <div class="section-title">💊 营养补剂推荐</div>
      {supplement_html}
    </div>
    
    <div class="target-card">
      <div class="label">🎯 明日目标步数</div>
      <div class="number">{target_steps:,}</div>
      <div class="unit">步</div>
    </div>
    
    <div class="kite-card">
      <div class="title">💡 Kite小结</div>
      <div class="text">{kite_tip}</div>
    </div>
  </div>
  
  <div class="footer">
    本建议仅供日常参考，效果因人而异，实施前请咨询专业人士<br>
    免责声明：本报告基于估算数据，不构成医疗建议
  </div>
</div>
</body>
</html>
"""
    return html


def get_kite_commentary(calc_results: Dict, evaluation: Dict) -> str:
    """生成AI风格的评价和鼓励 - 增强版"""
    total_score = evaluation['total_score']
    suggestions = evaluation.get('suggestions', [])
    calorie_diff = calc_results['calorie_diff']
    
    # 根据评分和热量差生成不同风格回复
    if total_score >= 9.0:
        if calorie_diff <= 0:
            comment = "🎊 完美！今天的饮食堪称教科书级别！\n🌈 热量控制得刚刚好，脂肪正在悄悄减少~"
        else:
            comment = "🥳 哇哦！今天吃得很满足呀！\n🚶 但别忘了多走走路消耗多余热量哦~"
    elif total_score >= 8.0:
        comment = "🌟 很不错！继续保持这个节奏~\n💪 小蛮腰已经在向你招手啦！"
    elif total_score >= 7.0:
        comment = "😊 还不错，有进步空间哦！\n📝 明天注意一下建议的小问题就好啦~"
    elif total_score >= 6.0:
        comment = "🤔 中等水平，还能更好~"
        if calorie_diff > 200:
            comment += "\n🚶 今天超标比较多，记得多走点路哦！"
    elif total_score >= 5.0:
        if calorie_diff > 0:
            comment = "😅 热量超标啦！不过别慌~\n🏃 今天多走 8000-10000 步就能平衡回来！"
        else:
            comment = "🍽️ 吃得有点少哦~\n⚠️ 长期这样会掉基础代谢的，要适当增加营养！"
    elif total_score >= 3.0:
        comment = "😣 今天吃多了呀...\n💝 但没关系！明天重新开始就好，我们一起加油！"
    else:
        comment = "🫣 今天是放纵日吗？火锅烧烤炸鸡全套齐了？\n🏃 没事没事！接下来3天清淡点 + 每天走10000步~"

    # 添加建议
    if suggestions:
        comment += f"\n\n💡 小贴士: {suggestions[0]}"
    if len(suggestions) > 1:
        comment += f"\n📌 {suggestions[1]}"

    return comment


def generate_weekly_comparison(weekly_data: Dict) -> str:
    """生成周对比报告"""
    current_week = weekly_data.get('current_week', [])
    previous_week = weekly_data.get('previous_week', [])
    
    # 计算本周平均
    if not current_week:
        return "📊 本周数据不足，无法生成对比报告"
    
    current_avg_calories = sum(d.get('calories', 0) for d in current_week) / len(current_week)
    current_avg_steps = sum(d.get('steps', 0) for d in current_week) / len(current_week)
    current_total_score = sum(d.get('score', 0) for d in current_week) / len(current_week)
    
    # 计算上周平均（如果有）
    prev_avg_calories = 0
    prev_avg_steps = 0
    prev_total_score = 0
    has_previous = False
    if previous_week:
        has_previous = True
        prev_avg_calories = sum(d.get('calories', 0) for d in previous_week) / len(previous_week)
        prev_avg_steps = sum(d.get('steps', 0) for d in previous_week) / len(previous_week)
        prev_total_score = sum(d.get('score', 0) for d in previous_week) / len(previous_week)
    
    # 计算变化
    calorie_change = current_avg_calories - prev_avg_calories if has_previous else 0
    steps_change = current_avg_steps - prev_avg_steps if has_previous else 0
    score_change = current_total_score - prev_total_score if has_previous else 0
    
    # 计算本周亮点
    best_day = max(current_week, key=lambda x: x.get('score', 0))
    worst_day = min(current_week, key=lambda x: x.get('score', 0))
    
    card = f"""
╭─────────────────────────────────────────╮
│  📊 本周数据对比报告 📊                 │
╰─────────────────────────────────────────╯

【📈 本周概况】 ({len(current_week)}天数据)
┌────────────┬────────────┬────────────┐
│  日均热量  │  日均步数  │  平均评分  │
│  {current_avg_calories:,.0f}kcal  │  {current_avg_steps:,.0f}步  │  {current_total_score:.1f}分  │
└────────────┴────────────┴────────────┘
"""
    
    if has_previous:
        # 热量变化
        if calorie_change < -100:
            calorie_trend = "📉 热量下降 ↑"
        elif calorie_change > 100:
            calorie_trend = "📈 热量上升 ↓"
        else:
            calorie_trend = "➡️ 热量稳定"
        
        # 步数变化
        if steps_change > 500:
            steps_trend = "📈 步数增加 ↑"
        elif steps_change < -500:
            steps_trend = "📉 步数下降 ↓"
        else:
            steps_trend = "➡️ 步数稳定"
        
        # 评分变化
        score_arrow = "↑" if score_change > 0 else ("↓" if score_change < 0 else "→")
        
        card += f"""
【📊 vs 上周变化】
┌────────────┬────────────┬────────────┐
│  热量变化  │  步数变化  │  评分变化  │
│  {calorie_trend}  │  {steps_trend}  │  {score_arrow} {abs(score_change):.1f}分  │
└────────────┴────────────┴────────────┘
"""
    
    # 本周亮点
    card += f"""
【🌟 本周亮点】
• 最佳日：{best_day.get('date', 'N/A')} (评分{best_day.get('score', 0):.1f})
• 待改进：{worst_day.get('date', 'N/A')} (评分{worst_day.get('score', 0):.1f})
"""
    
    # 进步亮点（如果有上周数据）
    if has_previous:
        highlights = []
        if score_change > 0.5:
            highlights.append("⭐ 评分提升明显，继续保持！")
        if steps_change > 1000:
            highlights.append("🚶 步数增加明显，运动积极性提高！")
        if calorie_change < -100:
            highlights.append("🍽️ 热量摄入优化，饮食更健康！")
        if score_change < -0.5:
            highlights.append("💪 这周稍微松懈，下周加油！")
        
        if highlights:
            card += f"\n【🎯 进步亮点】\n" + "\n".join(f"• {h}" for h in highlights)
    
    card += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
*数据仅供参考，坚持才是胜利！*
"""
    
    return card


def get_steps_from_coze(coze_variables: Dict = None) -> Dict:
    """
    从Coze变量获取用户步数
    
    【优先级】
    1. Coze变量有步数 → 直接使用
    2. Coze变量无步数 → 返回需要询问用户
    
    Args:
        coze_variables: Coze变量字典，包含 daily_steps 等字段
    
    Returns:
        {
            'source': 'coze' / 'user_input' / 'required',
            'steps': int or None,
            'message': str,
            'action': 'use' / 'ask_user' / 'wait'
        }
    """
    result = {
        'source': 'required',
        'steps': None,
        'message': '',
        'action': 'wait'
    }
    
    # 方案1：从Coze变量获取
    if coze_variables:
        # 尝试多个可能的变量名
        for key in ['daily_steps', 'steps', 'step_count', 'today_steps']:
            if key in coze_variables and coze_variables[key]:
                steps = coze_variables[key]
                if isinstance(steps, (int, float)) and steps > 0:
                    result = {
                        'source': 'coze',
                        'steps': int(steps),
                        'message': f'已从智能设备同步步数：{int(steps)}步',
                        'action': 'use'
                    }
                    break
    
    # 方案2：返回需要询问用户
    if result['action'] == 'wait':
        result['message'] = '需要用户手动输入步数'
    
    return result


def sync_steps_to_coze(steps: int, coze_variables: Dict = None) -> Dict:
    """
    将用户步数同步到Coze变量
    
    Args:
        steps: 步数
        coze_variables: 现有Coze变量
    
    Returns:
        更新后的Coze变量
    """
    if coze_variables is None:
        coze_variables = {}
    
    coze_variables['daily_steps'] = steps
    coze_variables['steps_last_updated'] = 'TODAY'
    
    return coze_variables


def generate_steps_auto_guide() -> str:
    """生成步数自动获取引导话术"""
    return """📱 步数自动获取设置

要自动同步你的步数吗？

【推荐方式】绑定智能设备
• 智能手环（小米/华为/Apple Watch）
• 手机自带计步（需授权）
• 微信运动

【设置方法】
1. 打开微信运动 → 关注并绑定
2. 或在设置中授权健康App
3. 每日步数会自动同步到这里~

【手动输入】
• 随时告诉我"今天走了xxx步"
• 我会帮你记录和同步

【当前状态】
• 已绑定：✅ 自动同步中
• 未绑定：❌ 请告诉我今日步数
"""


def generate_steps_prompt_message(is_auto: bool = False) -> str:
    """生成询问步数的话术"""
    if is_auto:
        return "今日步数已自动同步：{steps}步 ✅\n\n需要手动补充吗？"
    else:
        return "📱 今日步数是多少呀？\n\n可以这样告诉我：\n• \"走了8000步\"\n• \"今天运动了5000步\"\n• 直接告诉我数字也可以~"


def generate_interaction_template() -> Dict[str, str]:
    """生成AI选项式问答话术模板 - 监督增强版"""
    return {
        # ===== 基础话术 =====
        'greeting': "嗨~ 我是你的AI减肥小助手！🌟\n要帮你算得准准的，先了解你一点点信息呀~ 😊",
        'info_request': "📝 请告诉我：\n• 身高(cm)\n• 体重(kg)\n• 年龄(岁)\n• 性别(男/女)\n\n也可以直接说：\"我身高165，体重55，25岁女生\"",
        'food_input': "🍽️ 今天吃了什么呀？\n\n尽量描述得详细点哦~\n📌 例如：\n• 两小碗米饭 🍚\n• 一份宫保鸡丁 🍗\n• 半份西兰花 🥦\n• 一杯酸奶 🥛",
        'portion_options': "📏 份量大小可以这样描述：\n\n🍚 主食类：\n   小碗(半碗) / 中碗(正常) / 大碗(满满一碗)\n\n🍗 荤菜类：\n   小份(3-4块) / 中份(5-6块) / 大份(7-8块)\n\n🥗 素菜类：\n   小碟(几口) / 中碟(半盘) / 大碟(满满一盘)",
        'satiety_check': "🤔 吃了大概几成饱呀？\n\n🍽️ 可选：\n六分饱(有点饿) / 七分饱(刚刚好) / 八分饱(很满足)\n九分饱(有点撑) / 十分饱(吃撑了)",
        'group_meal': "🍲 火锅、聚餐这种多人一起吃的话~\n\n告诉我一共几个人就行啦！\n📌 例如：\"昨天4个人一起吃了火锅\"\n我来帮你平均分摊热量~",
        'uncertainty': "🤗 没关系，说个大概的样子就行！\n\n📌 比如：\n• \"一碗面\" → 我来估算份量\n• \"一些炒菜\" → 大概一盘左右\n• \"吃了点东西\" → 按普通一餐算~\n\n放心交给我！😉",
        
        # ===== 监督时间表话术 =====
        'morning_greeting': "早安呀~ ☀️ 新的一天开始啦！\n\n🌟 今日目标步数：{today_steps} 步！\n记得今天努力完成哦~ 🚶\n\n现在起床第一件事：空腹称体重~ 📝\n站上去吧，我来帮你记录今天的起点！\n\n早餐别忘了打卡哦~ 🍳",
        'morning_weight_record': "记录完成！📝\n今日空腹体重：{weight}kg\n对比昨日：{diff}kg\n\n今天的步数目标是 {steps} 步，加油！🚶",
        
        'breakfast_reminder': "🍳 早餐时间到！\n\n今天早餐吃了什么呀？\n记得告诉我，我来帮你记录~\n\n📌 如果你正在执行8+16断食法：\n   • 10点前进食 → 回复「不吃」即可\n   • 10点后第一餐 → 告诉我吃的什么",
        'breakfast_recorded': "早餐记录完成！🍳\n估算热量：约 {calories} kcal\n\n记得午餐也要告诉我哦~ 中午见！😊",
        'breakfast_missed': "还没吃吗？先记下来，待会儿补上也行哦~ ⏰\n记得待会儿回来告诉我吃了啥呀！",
        'breakfast_skipped': "🥄 早餐跳过（8+16断食法）\n\n记录：不吃早餐 ✅\n热量：0 kcal\n\n📌 提醒：10点前不要吃任何东西，10点后可以开始进食窗口啦~",
        
        'lunch_reminder': "午餐时间到！🍽️\n\n今天中午吃了啥？\n另外，昨天说好的步数目标完成了吗？🚶",
        'lunch_with_check': "午餐记录：约 {calories} kcal\n\n昨日步数：{completed} / {target}\n{check_result}\n\n今日目标步数是 {today_steps} 步！🚶",
        'yesterday_incomplete': "昨天的步数目标还有 {remaining} 步没完成~",
        'yesterday_incomplete_action': "今天的步数目标会加上这个缺口！\n或者做 {squats} 个蹲起也能抵消~ 🏋️",
        
        'evening_reminder': "晚上好~ 🌙\n\n🍽️ 今天的晚餐吃了什么呀？记得告诉我打卡哦~\n\n📌 如果你正在执行8+16断食法：\n   • 18点前进食 → 正常记录\n   • 18点后不吃了 → 回复「不吃」即可\n\n🚶 步数目标完成了吗？📱\n\n完成了：太棒了！🎉\n没完成：还有 {remaining} 步，现在出门走走还来得及！",
        'evening_complete': "🎉 太棒了！今天的步数目标完成了！\n离小蛮腰又近一步~ 💪\n\n今天的晚餐记得告诉我哦~",
        'evening_incomplete': "今日步数：{completed} / {target}\n还差 {remaining} 步！\n\n🏃 现在出门还来得及哦~\n或者做 {squats} 个蹲起也能抵消~ 🏋️",
        'evening_skipped': "🥄 晚餐跳过（8+16断食法）\n\n记录：不吃晚餐 ✅\n热量：0 kcal\n\n📌 提醒：18点后不要再吃东西了，明天早餐记得吃哦~",
        
        'meal_miss_check': "📋 今天的记录检查：\n\n• 早餐：{breakfast_status}\n• 午餐：{lunch_status}\n• 晚餐：{dinner_status}\n\n有遗漏的话，现在回忆一下告诉我，我来帮你补上~",
        'meal_missing': "今天的 {meal} 还没记录呢...\n现在回忆一下告诉我，我来帮你补上！\n这样明天才能准确计算目标步数呀~ 📊",
        
        'daily_summary': "📊 今日总结\n\n━━━━━━━━━━━━━━━\n🍽️ 饮食：\n   早餐 {breakfast_cal} + 午餐 {lunch_cal} + 晚餐 {dinner_cal}\n   = {total_cal} kcal\n\n🚶 运动：\n   {completed_steps} / {target_steps} 步\n\n⚖️ 热量平衡：\n   {balance_status} {balance_cal} kcal\n\n⭐ 今日评分：{score}/10\n━━━━━━━━━━━━━━━\n\n💡 明日目标步数：{tomorrow_steps} 步\n{adjustment_note}\n\n早点休息，明天继续加油！🌙",
        
        'tomorrow_preview': "📋 明日预告\n\n基于今日饮食数据：\n• 今日总热量：{today_cal} kcal\n• 热量差：{diff_cal} kcal\n• 明日目标步数：{tomorrow_steps} 步\n\n{encouragement}\n\n记得明天早上空腹称体重哦~ 🌅",
        
        # ===== 鼓励话术 =====
        'weight_loss': "比昨天轻了 {diff}kg，继续保持！🎉",
        'weight_gain': "比昨天重了 {diff}kg，没关系，可能是水分波动~ 💧\n继续加油！",
        'target_achieved': "🎊 目标达成！\n你太棒了！继续保持这个节奏~ 💪",
        'target_incomplete': "今天没完全达成目标没关系~ 🌱\n明天继续努力，我们一起加油！",
        
        # ===== 运动督促 =====
        'steps_encouragement': "🚶 走路小贴士：\n\n• 快步走效果更好哦~\n• 上下班提前两站下车~\n• 饭后散步半小时~\n\n每次多走1000步，脂肪远离你！💪",
        'squat_intro': "🏋️ 蹲起替代方案：\n\n每次蹲起消耗约 {cal_per_squat} kcal\n想消耗 {need_cal} kcal 的话，需要蹲 {squats} 次\n\n可以分组做：20个一组，间隔休息~\n加油！💪",
        
        # ===== 加餐记录话术 =====
        'snack_reminder': "🍪 今天有加餐吗？\n\n想吃零食？先告诉我，我来帮你算算需要多少步才能消耗~",
        'snack_recorded': "加餐记录完成！🍪\n热量：约 {calories} kcal\n\n消耗这些需要：\n• 快走 {walk_min} 分钟\n• 蹲起 {squats} 次\n\n明天记得少吃一点哦~ 或者多走几步！💪",
        'snack_no_need': "不加餐很棒！继续保持这个习惯~ 🍎\n减少了不必要的热量摄入，离目标更近了！",
        
        # ===== 8+16断食法支持话术 =====
        'fasting_intro': "🍽️ 8+16断食法说明：\n\n⏰ 进食窗口：每天 10:00-18:00（8小时）\n🚫 禁食窗口：18:00-次日10:00（16小时）\n\n执行要点：\n• 早餐跳过（10点前进食算破坏断食）\n• 午餐正常吃\n• 晚餐在18:00前吃完\n• 禁食期间只能喝水或黑咖啡",
        'fasting_skip_breakfast': "🥄 早餐跳过（8+16断食法）\n\n记录：不吃早餐 ✅\n热量：0 kcal\n\n📌 提醒：\n• 10点前不要吃任何东西哦~\n• 10点开始可以吃第一餐啦！\n• 18点后也不要吃任何东西~",
        'fasting_skip_dinner': "🍽️ 晚餐跳过（8+16断食法）\n\n记录：不吃晚餐 ✅\n热量：0 kcal\n\n📌 提醒：\n• 明天早餐记得吃哦~\n• 10点前吃完最后一口~",
        'fasting_reminder': "⏰ {time} 啦！\n\n{fasting_type}时间到~\n{fasting_message}",
        'fasting_breakfast_time': "🍳 断食结束！可以吃早餐啦~\n\n记得：\n• 吃完早餐后不要再吃东西了\n• 等到10点再吃第一餐",
        'fasting_dinner_time': "🚫 禁食时间开始！\n\n18:00后不要再吃东西了哦~\n可以喝：白开水、纯黑咖啡、茶\n\n坚持16小时，明天10点就能吃早餐啦！💪",
        
        # ===== 平台期解释话术 =====
        'plateau_intro': "📊 关于体重平台期\n\n【什么是平台期？】\n身体适应了当前的消耗模式，进入'节能模式'，体重暂时停滞。\n\n【为什么会发生？】\n• 基础代谢适应性下降\n• 热量消耗自我调节\n• 肌肉量变化\n\n【这说明什么？】\n说明你之前的减脂方法是有效的！\n身体正在为下一阶段减脂做准备~",
        'plateau_encouragement': "💪 平台期不是终点，是加油站！\n\n你的身体正在适应新体重，这是正常现象~ \n\n继续坚持：\n• 饮食不要太严格\n• 适当增加力量训练\n• 保证睡眠7-8小时\n• 给身体2-4周适应期\n\n平台期过后，你会进入新一轮快速减脂期！🎉",
        'plateau_tips': "📋 突破平台期小建议：\n\n1. 变换运动方式 🚶\n   尝试快走、跑步、游泳、力量训练交替\n\n2. 轻断食1-2天 🍽️\n   每周选1-2天只吃500kcal，让身体'重启'\n\n3. 增加蛋白质 🥩\n   多吃鸡蛋、鸡胸肉、鱼虾，提高基础代谢\n\n4. 保证睡眠 😴\n   每天7-8小时，睡眠不足会阻碍减脂\n\n5. 多喝水 💧\n   每天2-3L，帮助代谢废物\n\n记住：平台期坚持住，就离成功更近一步！🌟",
        'plateau_progress': "📈 当前进度\n\n• 已坚持：{days} 天\n• 已减重：{lost} kg\n• 目标：{target} kg\n\n进度：{progress}%\n\n不要放弃，你正在正确的路上！💪"
    }


def validate_user_data(weight, height, age, gender):
    """验证用户数据完整性"""
    errors = []
    if not weight or weight <= 0:
        errors.append("体重")
    if not height or height <= 0:
        errors.append("身高")
    if not age or age <= 0:
        errors.append("年龄")
    if not gender:
        errors.append("性别")
    
    if errors:
        return False, f"缺少必要数据：{', '.join(errors)}。请先补充完整信息。"
    return True, None

def main():
    parser = argparse.ArgumentParser(description='AI陪伴减肥计算器 v2.0')

    # 用户信息
    parser.add_argument('--weight', type=float, required=True, help='体重(kg)')
    parser.add_argument('--height', type=float, required=True, help='身高(cm)')
    parser.add_argument('--age', type=int, required=True, help='年龄')
    parser.add_argument('--gender', choices=['male', 'female', '男', '女'], required=True)

    # 食物信息
    parser.add_argument('--calories', type=float, help='总热量(kcal)')
    parser.add_argument('--foods', type=str, default='', help='食物描述文本，供自动估算')
    parser.add_argument('--carb_ratio', type=float, default=50.0, help='碳水比例(%%)')
    parser.add_argument('--food_count', type=int, default=3, help='食物种类数')
    parser.add_argument('--food_items', type=str, default='[]', help='食物列表JSON')

    # 围餐
    parser.add_argument('--diner_count', type=int, default=1, help='就餐人数(围餐时)')

    # 活动系数
    parser.add_argument('--activity', default='sedentary',
                        choices=['physical_labor', 'moderate', 'sedentary'])

    # 零食兑换模式
    parser.add_argument('--snack', type=str, default='', help='零食名称，查询等效步数')
    parser.add_argument('--snack_quantity', type=float, default=1.0, help='零食数量')

    # 聚餐模式
    parser.add_argument('--party_type', type=str, default='', help='聚餐类型(火锅/烧烤/自助餐/炒菜等)')
    parser.add_argument('--party_people', type=int, default=4, help='聚餐人数')

    # 动态调整模式
    parser.add_argument('--dynamic_adjust', action='store_true', help='启用动态目标调整')
    parser.add_argument('--weekly_weight_change', type=float, default=0, help='每周体重变化(kg)')

    # 周报生成模式
    parser.add_argument('--weekly_report', action='store_true', help='生成周报')
    parser.add_argument('--report_days', type=int, default=7, help='报告天数')

    # 补打卡引导
    parser.add_argument('--makeup_guide', action='store_true', help='显示补打卡引导')

    # 交互话术模板
    parser.add_argument('--interaction_guide', action='store_true', help='显示所有交互话术模板')

    args = parser.parse_args()

    # 【强制规则1】验证用户数据完整性
    is_valid, error_msg = validate_user_data(args.weight, args.height, args.age, args.gender)
    if not is_valid:
        print(json.dumps({
            'status': 'error',
            'code': 'MISSING_USER_DATA',
            'message': error_msg,
            'action': '请先通过Coze变量获取用户完整数据：身高、体重、年龄、性别'
        }, ensure_ascii=False, indent=2))
        return

    # 解析食物列表
    try:
        food_items = json.loads(args.food_items) if args.food_items else []
    except json.JSONDecodeError:
        food_items = []

    # 计算热量
    total_calories = 0
    matched_foods = []

    if args.foods:
        # 自动估算食物热量
        total_calories, carb_total, protein_total, matched = estimate_food(args.foods)
        matched_foods = matched

    if args.calories:
        total_calories = args.calories

    # 围餐分摊
    if args.diner_count > 1:
        total_calories = total_calories / args.diner_count
        matched_foods.append(f'(围餐,共{args.diner_count}人)')

    # 如果有食物列表，合并计算
    if food_items:
        for item in food_items:
            matched_foods.append(item.get('name', '未知食物'))

    food_count = len(matched_foods) if matched_foods else args.food_count

    # 计算
    step_length = calculate_step_length(args.height)
    bmr = calculate_bmr(args.weight, args.height, args.age, args.gender)
    tdee = calculate_tdee(bmr, args.activity)
    calorie_diff = calculate_calorie_diff(total_calories, tdee)
    fat_change_g = calculate_fat_change(calorie_diff)
    # 热量差→步数闭环核心计算
    steps_result = calculate_target_steps(calorie_diff, args.weight)
    target_steps = steps_result['target_steps']
    cal_per_1000_steps = steps_result['calories_per_1000_steps']

    # 蹲起计算
    height_m = args.height / 100
    squat_calories = calculate_squat_calories(args.weight, height_m)
    squats_needed = calculate_squats_needed(calorie_diff, squat_calories)

    # 膳食评价
    evaluation = evaluate_diet(total_calories, bmr, args.carb_ratio, food_items, food_count)

    # 生成结果
    calc_results = {
        'step_length_cm': round(step_length, 1),
        'bmr': round(bmr, 1),
        'tdee': round(tdee, 1),
        'activity_level': args.activity,
        'total_calories': round(total_calories, 1),
        'carb_ratio': args.carb_ratio,
        'calorie_diff': round(calorie_diff, 1),
        'fat_change_g': round(fat_change_g, 1),
        'target_steps': target_steps,
        'cal_per_1000_steps': round(cal_per_1000_steps, 2),
        'diner_count': args.diner_count
    }

    # 蹲起计算
    squat_calories = calculate_squat_calories(args.weight, height_m)
    squats_needed = calculate_squats_needed(calorie_diff, squat_calories)
    
    # 等效运动方案
    exercise_equivalents = get_exercise_equivalents(abs(calorie_diff), args.weight)
    
    exercise = {
        'squat_calories': round(squat_calories, 4),
        'squats_needed': squats_needed,
        'equivalents': exercise_equivalents,
        'steps_to_exercise': steps_to_exercise(target_steps, args.weight)
    }

    summary_card = generate_summary_card(
        {'weight': args.weight, 'height': args.height, 'age': args.age, 'gender': args.gender},
        calc_results, exercise, evaluation, matched_foods
    )

    ai_comment = get_kite_commentary(calc_results, evaluation)
    interaction_templates = generate_interaction_template()
    
    # 激励机制（默认数据）
    streak_badge = calculate_streak_badge(0)  # 默认0天

    # ===== 新增模式处理 =====
    # 零食兑换模式
    snack_result = None
    if args.snack:
        snack_result = calculate_snack_exchange(args.snack, args.snack_quantity, args.weight)

    # 聚餐模式
    party_result = None
    if args.party_type:
        party_result = calculate_party_mode(args.party_type, args.party_people, args.weight)

    # 动态调整模式
    adjustment_result = None
    if args.dynamic_adjust:
        adjustment_result = calculate_dynamic_adjustment(
            args.weekly_weight_change, target_steps, bmr
        )

    # 补打卡引导
    makeup_guide = None
    if args.makeup_guide:
        makeup_guide = format_makeup_checkin_guide()

    # 交互话术模板
    if args.interaction_guide:
        templates = generate_interaction_template()
        print(json.dumps({'status': 'success', 'interaction_templates': templates}, ensure_ascii=False, indent=2))
        return

    # 最终输出
    result = {
        'status': 'success',
        'calculation': calc_results,
        'exercise': exercise,
        'evaluation': evaluation,
        'matched_foods': matched_foods,
        'summary_card': summary_card,
        'ai_comment': ai_comment,
        'interaction_templates': interaction_templates,
        'motivation': {
            'streak_badge': streak_badge,
            'encouragement': generate_encouragement_message(evaluation['total_score'], 0, calorie_diff)
        },
        'supplement': {
            'recommendations': get_supplement_recommendation(
                weight_kg=args.weight,
                bmr=bmr,
                score=evaluation['total_score'],
                streak_days=0,  # 默认0天，实际应从数据管理器获取
                target_steps=target_steps,
                actual_steps=0,  # 默认未记录，实际应从数据管理器获取
                calorie_diff=calorie_diff,
                nutrition_score=int(float(evaluation['nutrition'].split('/')[0]))
            ),
            'card': format_supplement_card(
                get_supplement_recommendation(
                    weight_kg=args.weight,
                    bmr=bmr,
                    score=evaluation['total_score'],
                    streak_days=0,
                    target_steps=target_steps,
                    actual_steps=0,
                    calorie_diff=calorie_diff,
                    nutrition_score=int(float(evaluation['nutrition'].split('/')[0]))
                ),
                streak_days=0
            )
        },
        # ===== 新增功能字段 =====
        'snack_exchange': snack_result,
        'snack_card': format_snack_exchange_card(snack_result) if snack_result and snack_result.get('found') else None,
        'party_mode': party_result,
        'party_card': format_party_mode_card(party_result) if party_result else None,
        'dynamic_adjustment': adjustment_result,
        'adjustment_card': format_dynamic_adjustment_card(adjustment_result) if adjustment_result else None,
        'makeup_guide': makeup_guide,
        'interaction_templates': interaction_templates,
        'disclaimer': '本建议仅供日常参考，具体效果因人而异，实施前请咨询专业人士，责任自负。'
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()


# ==================== Coze快捷命令解析 ====================

def parse_command(command: str) -> Dict:
    """
    解析用户输入的快捷命令
    返回格式：{"type": "命令类型", "action": "具体动作", "params": {...}}
    """
    command = command.strip()
    
    # 打卡命令
    if command.startswith('#打卡') or command.startswith('#打卡 '):
        parts = command.replace('#打卡', '').strip().split(' ', 1)
        target = parts[0] if parts else ''
        content = parts[1] if len(parts) > 1 else ''
        
        # 识别打卡类型
        if '体重' in target or '称' in target:
            try:
                weight = float(''.join(filter(lambda x: x.isdigit() or x == '.', target)))
                return {'type': 'command', 'action': 'weight_checkin', 'params': {'weight': weight}}
            except:
                return {'type': 'command', 'action': 'weight_checkin', 'params': {'await_weight': True}}
        elif '早餐' in target or '早' in target:
            return {'type': 'command', 'action': 'breakfast_checkin', 'params': {'foods': content or None}}
        elif '午餐' in target or '中' in target:
            return {'type': 'command', 'action': 'lunch_checkin', 'params': {'foods': content or None}}
        elif '晚餐' in target or '晚' in target:
            return {'type': 'command', 'action': 'dinner_checkin', 'params': {'foods': content or None}}
        else:
            return {'type': 'command', 'action': 'meal_checkin', 'params': {'content': target, 'foods': content}}
    
    # 查询命令
    elif command.startswith('#查') or command.startswith('#查询') or command.startswith('#看'):
        target = command.replace('#查', '').replace('#查询', '').replace('#看', '').strip()
        
        if '周' in target or '周报' in target:
            return {'type': 'command', 'action': 'weekly_report', 'params': {}}
        elif '月' in target or '月报' in target:
            return {'type': 'command', 'action': 'monthly_report', 'params': {}}
        elif '体重' in target or '重' in target:
            return {'type': 'command', 'action': 'weight_trend', 'params': {}}
        elif '步' in target or '走路' in target:
            return {'type': 'command', 'action': 'steps_trend', 'params': {}}
        elif '热量' in target or '卡' in target:
            return {'type': 'command', 'action': 'calorie_trend', 'params': {}}
        elif '成就' in target or '徽章' in target or 'badge' in target.lower():
            return {'type': 'command', 'action': 'achievements', 'params': {}}
        else:
            return {'type': 'command', 'action': 'status', 'params': {}}
    
    # 计算命令
    elif command.startswith('#算') or command.startswith('#计算'):
        content = command.replace('#算', '').replace('#计算', '').strip()
        
        # 火锅/聚餐
        people_match = re.search(r'(\d+)[人个]', content)
        people = int(people_match.group(1)) if people_match else None
        
        if '火锅' in content:
            return {'type': 'command', 'action': 'party_hotpot', 'params': {'people': people or 2}}
        elif '烧烤' in content:
            return {'type': 'command', 'action': 'party_bbq', 'params': {'people': people or 2}}
        elif '自助' in content:
            return {'type': 'command', 'action': 'party_buffet', 'params': {'people': people or 2}}
        elif people:
            return {'type': 'command', 'action': 'party_generic', 'params': {'people': people}}
        else:
            # 零食热量
            return {'type': 'command', 'action': 'snack_calorie', 'params': {'snack': content}}
    
    # 设置命令
    elif command.startswith('#设') or command.startswith('#设置') or command.startswith('#调'):
        content = command.replace('#设', '').replace('#设置', '').replace('#调', '').strip()
        
        if '提醒' in content or '时间' in content:
            time_match = re.search(r'(\d{1,2})[点:]?(\d{0,2})?', content)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or '0')
                return {'type': 'command', 'action': 'set_reminder', 'params': {'hour': hour, 'minute': minute, 'target': content}}
        
        if '开' in content or '启用' in content or '开启' in content:
            return {'type': 'command', 'action': 'enable_reminder', 'params': {}}
        elif '关' in content or '关闭' in content or '停' in content:
            return {'type': 'command', 'action': 'disable_reminder', 'params': {}}
        
        return {'type': 'command', 'action': 'settings', 'params': {'content': content}}
    
    # 补打卡命令
    elif command.startswith('#补') or command.startswith('#补录') or command.startswith('#补打卡'):
        content = command.replace('#补', '').replace('#补录', '').replace('#补打卡', '').strip()
        
        date_match = re.search(r'(昨|前|今)?天?(早|午|晚)?餐?', content)
        if date_match:
            day = date_match.group(1) or '昨'
            meal = date_match.group(2) or ''
            return {'type': 'command', 'action': 'makeup_checkin', 'params': {'day': day, 'meal': meal, 'content': content}}
        
        return {'type': 'command', 'action': 'makeup_checkin', 'params': {'await_detail': True}}
    
    # 帮助命令
    elif command.startswith('#帮') or command.startswith('#帮助') or command.startswith('#?'):
        return {'type': 'command', 'action': 'help', 'params': {}}
    
    # 成就命令
    elif command.startswith('#成就') or command.startswith('#徽章'):
        return {'type': 'command', 'action': 'achievements', 'params': {}}
    
    # 开始命令
    elif command.startswith('#开始') or command.startswith('#重置') or command.startswith('#新'):
        return {'type': 'command', 'action': 'init', 'params': {}}
    
    else:
        return {'type': 'unknown', 'action': 'chat', 'params': {'content': command}}


def format_command_help() -> str:
    """生成快捷命令帮助文本"""
    return """
📖 快捷命令帮助

━━━━━━━━━━━━━━━
#打卡 - 快速打卡
  #打卡体重 58.5    → 记录体重
  #打卡早餐 粥包子   → 记录早餐
  #打卡午餐 米饭鱼   → 记录午餐
  #打卡晚餐 面条     → 记录晚餐

#查 - 查询数据
  #查周报          → 查看本周数据
  #查月报          → 查看本月数据
  #查体重          → 查看体重趋势
  #查步数          → 查看步数统计
  #查成就          → 查看已获徽章

#算 - 快速计算
  #算蛋糕          → 计算零食热量
  #算火锅4人       → 计算聚餐热量

#设 - 设置调整
  #设提醒8点       → 设置提醒时间
  #关闭提醒        → 关闭提醒

#补 - 补打卡
  #补昨天午餐      → 补录遗漏记录

#帮 - 获取帮助
━━━━━━━━━━━━━━━
💡 也可以直接说话，比如：
  "我吃了蛋糕"
  "体重58.5"
  "昨天4个人吃火锅"
"""


def format_command_response(parsed: Dict, context: Dict = None) -> str:
    """
    根据解析的命令生成AI回复模板
    context: 包含用户档案、当前进度等上下文
    """
    action = parsed['action']
    params = parsed['params']
    
    responses = {
        'weight_checkin': """📝 体重打卡记录
━━━━━━━━━━━━━━━
体重：{weight} kg
━━━━━━━━━━━━━━━
{encouragement}
""",
        'breakfast_checkin': """🍳 早餐打卡记录
━━━━━━━━━━━━━━━
内容：{foods}
热量：约 {calories} kcal
━━━━━━━━━━━━━━━
记得午餐也要打卡哦~ 😊""",
        'lunch_checkin': """🍽️ 午餐打卡记录
━━━━━━━━━━━━━━━
内容：{foods}
热量：约 {calories} kcal
━━━━━━━━━━━━━━━
晚餐别忘了~ 🌙""",
        'dinner_checkin': """🌙 晚餐打卡记录
━━━━━━━━━━━━━━━
内容：{foods}
热量：约 {calories} kcal
━━━━━━━━━━━━━━━
今日饮食已记录完毕！""",
        'weekly_report': """📊 本周减肥周报
━━━━━━━━━━━━━━━
✅ 达标天数：{achieved}/{total}
📉 体重变化：{weight_change} kg
🚶 总步数：{total_steps} 步
⭐ 平均评分：{avg_score} 分
━━━━━━━━━━━━━━━
{highlights}
━━━━━━━━━━━━━━━
💪 下周目标：{next_goal}""",
        'monthly_report': """📊 本月减肥月报
━━━━━━━━━━━━━━━
✅ 达标天数：{achieved}/{total}
📉 体重变化：{weight_change} kg
🔥 当前连续：{streak} 天
━━━━━━━━━━━━━━━
🏆 里程碑：{milestones}
━━━━━━━━━━━━━━━
{congrats}""",
        'snack_calorie': """🍰 {snack} 热量估算
━━━━━━━━━━━━━━━
热量：约 {calories} kcal
━━━━━━━━━━━━━━━
🚶 要消耗这些热量：
  快走：约 {walk_min} 分钟
  慢跑：约 {jog_min} 分钟
  🏋️ 蹲起：约 {squat} 次
━━━━━━━━━━━━━━━
💡 {suggestion}""",
        'party_hotpot': """🍲 火锅热量估算
━━━━━━━━━━━━━━━
👥 {people}人用餐
🍽️ 人均热量：约 {per_person} kcal
📊 总热量：约 {total} kcal
━━━━━━━━━━━━━━━
💡 建议：多点蔬菜少吃肉，蘸料少放麻酱~""",
        'set_reminder': """⏰ 提醒时间已设置
━━━━━━━━━━━━━━━
提醒时间：{hour}:{minute:02d}
━━━━━━━━━━━━━━━
设置成功！到时候我会提醒你~ 🌟""",
        'enable_reminder': """✅ 提醒已开启
━━━━━━━━━━━━━━━
早安提醒：{morning_time}
午安提醒：{lunch_time}
晚安提醒：{evening_time}
━━━━━━━━━━━━━━━
有需要随时调整哦~ 😊""",
        'disable_reminder': """⏰ 提醒已关闭
━━━━━━━━━━━━━━━
已暂停提醒服务
━━━━━━━━━━━━━━━
需要开启时告诉我~ 🌙""",
        'makeup_checkin': """📝 补打卡引导
━━━━━━━━━━━━━━━
请告诉我：
日期 + 早/午/晚 + 吃了什么

例如：
"昨天早餐吃了粥和包子"
"前天午餐吃了米饭和鱼"
━━━━━━━━━━━━━━━
我来帮你补上！😊""",
        'help': format_command_help(),
        'achievements': """🏆 成就徽章墙
━━━━━━━━━━━━━━━
{current_badges}

已解锁：{unlocked_count} 个
━━━━━━━━━━━━━━━
{next_badge}
""",
        'init': """🌟 开始新的减肥之旅！
━━━━━━━━━━━━━━━
要帮你量身定制方案，先了解你~

① 身高体重是多少？
② 年龄和性别？
③ 做什么工作？

直接告诉我，我来帮你算！😊""",
        'status': """📊 当前状态
━━━━━━━━━━━━━━━
📅 今日日期：{date}
🚶 今日步数：{steps}/{target}
🍽️ 今日热量：{calories}/{bmr}
⭐ 连续达标：{streak} 天
━━━━━━━━━━━━━━━
{next_action}""",
    }
    
    return responses.get(action, responses['help']).format(**params)


# ============ 新增功能：生理期模式、暴食急救、作息个性化 ============

class MenstrualMode:
    """生理期模式"""
    
    # 生理期四个阶段
    PHASES = {
        'menstruation': {'name': '经期', 'days': (1, 7), 'calorie_adjust': 1.15, 'description': '需要更多热量和营养支持'},
        'follicular': {'name': '卵泡期', 'days': (8, 14), 'calorie_adjust': 1.0, 'description': '代谢较快，适合控制饮食'},
        'ovulation': {'name': '排卵期', 'days': (15, 20), 'calorie_adjust': 1.05, 'description': '能量水平较高'},
        'luteal': {'name': '黄体期', 'days': (21, 28), 'calorie_adjust': 1.1, 'description': '食欲可能增加，适当放宽'}
    }
    
    # 生理期推荐食物
    RECOMMENDED_FOODS = {
        'menstruation': [
            {'food': '红枣桂圆茶', 'reason': '补气血'},
            {'food': '红豆汤', 'reason': '补铁消肿'},
            {'food': '菠菜猪肝', 'reason': '高铁食物'},
            {'food': '黑巧克力', 'reason': '缓解痛经(适量)'}
        ],
        'follicular': [
            {'food': '高蛋白食物', 'reason': '修复身体组织'},
            {'food': '绿叶蔬菜', 'reason': '富含叶酸'},
            {'food': '全谷物', 'reason': '稳定血糖'}
        ],
        'luteal': [
            {'food': '坚果', 'reason': '补充镁元素'},
            {'food': '深色蔬菜', 'reason': '缓解腹胀'},
            {'food': ' Complex carbs', 'reason': '稳定情绪'}
        ]
    }
    
    @staticmethod
    def get_phase(day_of_cycle: int) -> str:
        """根据生理期第几天判断当前阶段"""
        for phase, info in MenstrualMode.PHASES.items():
            start, end = info['days']
            if start <= day_of_cycle <= end:
                return phase
        return 'follicular'  # 默认返回卵泡期
    
    @staticmethod
    def get_calorie_adjustment(day_of_cycle: int) -> float:
        """获取热量调整系数"""
        phase = MenstrualMode.get_phase(day_of_cycle)
        return MenstrualMode.PHASES[phase]['calorie_adjust']
    
    @staticmethod
    def get_recommendations(day_of_cycle: int) -> List[Dict]:
        """获取阶段推荐食物"""
        phase = MenstrualMode.get_phase(day_of_cycle)
        return MenstrualMode.RECOMMENDED_FOODS.get(phase, [])
    
    @staticmethod
    def adjust_target_steps(target_steps: int, day_of_cycle: int) -> int:
        """根据生理期调整目标步数"""
        phase = MenstrualMode.get_phase(day_of_cycle)
        if phase == 'menstruation':
            # 经期减少步数要求
            return int(target_steps * 0.8)  # 降低20%
        return target_steps


class BingeRecovery:
    """暴食急救模块"""
    
    # 暴食程度定义
    SEVERITY_LEVELS = {
        'mild': {'threshold': 1.5, 'label': '轻微超标', 'calorie_limit': 2000},
        'moderate': {'threshold': 2.0, 'label': '中度超标', 'calorie_limit': 3000},
        'severe': {'threshold': 2.5, 'label': '严重超标', 'calorie_limit': 4000},
        'extreme': {'threshold': float('inf'), 'label': '极度超标', 'calorie_limit': 5000}
    }
    
    @staticmethod
    def assess_binge(intake: float, tdee: float) -> Dict:
        """评估暴食程度"""
        ratio = intake / tdee if tdee > 0 else 0
        
        for level, info in BingeRecovery.SEVERITY_LEVELS.items():
            if ratio < info['threshold']:
                return {
                    'level': level,
                    'label': info['label'],
                    'ratio': ratio,
                    'excess_calories': max(0, intake - tdee)
                }
        
        return {
            'level': 'extreme',
            'label': '极度超标',
            'ratio': ratio,
            'excess_calories': intake - tdee
        }
    
    @staticmethod
    def get_recovery_plan(assessment: Dict, weight: float) -> Dict:
        """生成急救恢复计划"""
        excess = assessment['excess_calories']
        level = assessment['level']
        
        # 计算需要多少步数消耗多余热量
        steps_per_cal = weight * 0.42  # 每千步消耗
        
        # 急救措施
        measures = []
        
        if level in ['severe', 'extreme']:
            measures.extend([
                {'action': '停止自责', 'reason': '情绪崩溃只会让情况更糟'},
                {'action': '喝温水', 'reason': '帮助消化，缓解不适'},
                {'action': '轻度活动', 'reason': '散步30分钟促进消化'},
                {'action': '第二天轻断食', 'reason': '让身体有时间处理多余热量'}
            ])
        else:
            measures.extend([
                {'action': '多喝水', 'reason': '促进代谢'},
                {'action': '散步30分钟', 'reason': '消耗部分多余热量'},
                {'action': '正常作息', 'reason': '保证睡眠利于恢复'}
            ])
        
        # 建议的补偿步数
        compensation_steps = min(int(excess / steps_per_cal * 1000), 15000)
        
        return {
            'excess_calories': excess,
            'compensation_steps': compensation_steps,
            'recovery_days': 2 if level in ['severe', 'extreme'] else 1,
            'measures': measures,
            'message': BingeRecovery._get_encouragement(level)
        }
    
    @staticmethod
    def _get_encouragement(level: str) -> str:
        """获取鼓励话语"""
        messages = {
            'mild': "偶尔超标是正常的，重要的是不要放弃，明天继续加油！",
            'moderate': "今天吃得多了点没关系的，身体需要能量。下次注意就好~",
            'severe': "我知道你可能有点自责，但没关系！我们可以一起制定恢复计划。",
            'extreme': "不管发生了什么，你都是最棒的！暴食不代表失败，我们一起重新开始。"
        }
        return messages.get(level, "")


class SleepSchedule:
    """作息个性化模块"""
    
    SCHEDULE_TYPES = {
        'early_bird': {
            'name': '早起型',
            'wake_time': '06:00',
            'sleep_time': '22:00',
            'meal_times': {
                'breakfast': '07:00',
                'lunch': '12:00',
                'dinner': '18:30'
            },
            'fasting_window': {'start': '18:30', 'end': '07:00'}
        },
        'normal': {
            'name': '标准型',
            'wake_time': '07:30',
            'sleep_time': '23:00',
            'meal_times': {
                'breakfast': '08:00',
                'lunch': '12:30',
                'dinner': '19:30'
            },
            'fasting_window': {'start': '19:30', 'end': '08:00'}
        },
        'night_owl': {
            'name': '晚睡型',
            'wake_time': '09:00',
            'sleep_time': '01:00',
            'meal_times': {
                'breakfast': '10:00',
                'lunch': '14:00',
                'dinner': '21:00'
            },
            'fasting_window': {'start': '21:00', 'end': '10:00'}
        }
    }
    
    @staticmethod
    def get_schedule_type(wake_time: str, sleep_time: str) -> str:
        """根据作息时间判断作息类型"""
        # 解析时间
        wake_hour = int(wake_time.split(':')[0])
        sleep_hour = int(sleep_time.split(':')[0])
        
        if wake_hour <= 6:
            return 'early_bird'
        elif sleep_hour >= 24 or sleep_hour <= 2:
            return 'night_owl'
        else:
            return 'normal'
    
    @staticmethod
    def get_adjusted_reminders(schedule_type: str) -> List[Dict]:
        """获取调整后的提醒时间"""
        schedule = SleepSchedule.SCHEDULE_TYPES.get(schedule_type, SleepSchedule.SCHEDULE_TYPES['normal'])
        
        # 计算相对于标准作息的时间偏移
        standard_wake = 7
        standard_sleep = 23
        
        wake_hour = int(schedule['wake_time'].split(':')[0])
        offset = wake_hour - standard_wake
        
        # 基础提醒时间（按标准作息）
        base_reminders = [
            {'name': '空腹称重', 'base_time': '07:00'},
            {'name': '早餐提醒', 'base_time': '08:30'},
            {'name': '午餐提醒', 'base_time': '12:00'},
            {'name': '步数督促', 'base_time': '20:00'},
            {'name': '晚间总结', 'base_time': '22:00'}
        ]
        
        # 应用偏移
        adjusted = []
        for reminder in base_reminders:
            base_hour = int(reminder['base_time'].split(':')[0])
            new_hour = base_hour + offset
            if new_hour < 0:
                new_hour += 24
            elif new_hour >= 24:
                new_hour -= 24
            adjusted.append({
                'name': reminder['name'],
                'time': f'{new_hour:02d}:00'
            })
        
        return adjusted
    
    @staticmethod
    def get_fasting_plan(schedule_type: str) -> Dict:
        """获取调整后的断食计划"""
        schedule = SleepSchedule.SCHEDULE_TYPES.get(schedule_type, SleepSchedule.SCHEDULE_TYPES['normal'])
        return {
            'eating_window': f"每天 {schedule['meal_times']['breakfast']} - {schedule['meal_times']['dinner']}",
            'fasting_start': schedule['fasting_window']['start'],
            'fasting_end': schedule['fasting_window']['end'],
            'fasting_hours': SleepSchedule._calculate_fasting_hours(
                schedule['meal_times']['dinner'],
                schedule['meal_times']['breakfast']
            )
        }
    
    @staticmethod
    def _calculate_fasting_hours(dinner_time: str, breakfast_time: str) -> int:
        """计算断食时长"""
        dinner_hour = int(dinner_time.split(':')[0])
        breakfast_hour = int(breakfast_time.split(':')[0])
        
        fasting = (24 - dinner_hour) + breakfast_hour
        return fasting


def apply_personalization(user_info: Dict, calc_results: Dict, 
                          exercise: Dict) -> Dict:
    """应用个性化调整
    
    综合考虑生理期、断食、作息等因素调整计算结果
    """
    result = calc_results.copy()
    
    # 1. 生理期调整
    menstrual_day = user_info.get('menstrual_day', 0)
    if menstrual_day > 0:
        phase = MenstrualMode.get_phase(menstrual_day)
        adjust = MenstrualMode.get_calorie_adjustment(menstrual_day)
        result['menstrual_phase'] = phase
        result['menstrual_adjust'] = adjust
        # 调整热量差计算
        if 'calorie_diff' in result:
            result['adjusted_calorie_diff'] = result['calorie_diff'] / adjust
        # 调整目标步数
        if 'target_steps' in result:
            result['target_steps'] = MenstrualMode.adjust_target_steps(
                result['target_steps'], menstrual_day
            )
    
    # 2. 暴食检测与急救
    intake = result.get('total_calories', 0)
    tdee = result.get('tdee', user_info.get('tdee', 1500))
    binge_assessment = BingeRecovery.assess_binge(intake, tdee)
    result['binge_assessment'] = binge_assessment
    
    if binge_assessment['level'] in ['severe', 'extreme']:
        result['recovery_plan'] = BingeRecovery.get_recovery_plan(
            binge_assessment, user_info.get('weight', 60)
        )
    
    # 3. 作息个性化调整
    schedule_type = user_info.get('schedule_type', 'normal')
    if schedule_type != 'normal':
        adjusted_reminders = SleepSchedule.get_adjusted_reminders(schedule_type)
        fasting_plan = SleepSchedule.get_fasting_plan(schedule_type)
        result['personalized_reminders'] = adjusted_reminders
        result['fasting_plan'] = fasting_plan
    
    return result


def generate_enhanced_prescription(user_info: Dict, calc_results: Dict,
                                   exercise: Dict, evaluation: Dict,
                                   foods: List[str], streak_days: int = 0,
                                   weight_change: float = 0,
                                   target_steps: int = 6000,
                                   supplement_recommendations: List[Dict] = None) -> str:
    """生成增强版HTML营养处方 - 完整版（热量差→步数闭环核心）
    
    核心逻辑：昨日热量差 = 今日目标步数
    
    热量差来源：
    - 热量差 = 昨日摄入 × 0.9（TEF） - TDEE
    
    热量差 → 步数转换：
    - 热量差 < 0（减脂）：目标步数 = 基础步数6000
    - 热量差 = 0（平衡）：目标步数 = 基础步数6000
    - 热量差 > 0（超标）：目标步数 = 基础步数 + 额外步数
    """
    from datetime import datetime
    
    fat_change_g = calc_results.get('fat_change_g', 0)
    carb_ratio = calc_results.get('carb_ratio', 50)
    intake = calc_results.get('total_calories', 0)
    calorie_diff = calc_results.get('calorie_diff', 0)
    tdee = calc_results.get('tdee', 1800)
    net_calorie = calc_results.get('net_calorie', intake * 0.9)
    actual_steps = exercise.get('actual_steps', 0)
    weight = user_info.get('weight', 0)
    
    today = datetime.now()
    date_str = today.strftime('%Y年%m月%d日')
    weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][today.weekday()]
    
    # ===== 热量差→步数闭环核心计算 =====
    steps_mode = calc_results.get('steps_mode', 'balance')
    mode_label = calc_results.get('mode_label', '平衡态')
    mode_emoji = calc_results.get('mode_emoji', '⚖️')
    extra_steps = calc_results.get('extra_steps', 0)
    base_steps = calc_results.get('base_steps', 6000)
    calories_per_1000_steps = calc_results.get('calories_per_1000_steps', weight * 0.42)
    
    # 热量差状态显示
    if calorie_diff > 0:
        diff_status = "需补偿"
        diff_color = "#ff7675"
        diff_arrow = "↑"
    elif calorie_diff < 0:
        diff_status = "减脂中"
        diff_color = "#00b894"
        diff_arrow = "↓"
    else:
        diff_status = "平衡"
        diff_color = "#74b9ff"
        diff_arrow = "="
    
    # ===== 步数主线 =====
    steps_completion = (actual_steps / target_steps * 100) if target_steps > 0 else 0
    steps_score = min(5.0, steps_completion / 20)
    steps_stars = "⭐" * int(steps_score) + "🌙" * (5 - int(steps_score))
    
    if steps_completion >= 100:
        steps_status = "complete"
        steps_status_text = "任务完成"
    elif steps_completion >= 80:
        steps_status = "good"
        steps_status_text = "接近完成"
    else:
        steps_status = "pending"
        steps_status_text = "进行中"
    
    # ===== 饮食主线 =====
    total_score = evaluation.get('total_score', 0)
    diet_score = max(0, min(5.0, total_score - steps_score + 2.5))
    diet_stars = "⭐" * int(diet_score) + "🌙" * (5 - int(diet_score))
    
    # ===== 综合评分 =====
    total_final_score = steps_score + diet_score
    final_stars = "⭐" * int(total_final_score) + "🌙" * (10 - int(total_final_score))
    
    # ===== 热量差→步数闭环话术 =====
    if steps_mode == 'compensate':
        loop_reason = "因为昨天超标" + str(int(abs(calorie_diff))) + "kcal，需要多走" + str(extra_steps) + "步"
    elif steps_mode == 'reduce':
        loop_reason = "昨天热量缺口良好，只需基础走路"
    else:
        loop_reason = "昨天吃动平衡，保持基础运动即可"
    
    # ===== 营养建议（基于热量差模式）=====
    advice_items = []
    nutrition_score = float(evaluation.get('nutrition', '0/4').split('/')[0])
    diversity_score = float(evaluation.get('diversity', '0/1').split('/')[0])
    
    # 基于热量差模式的建议
    if steps_mode == 'compensate':
        advice_items.append({'icon': '⚠️', 'text': '昨天热量超标，建议增加蔬菜比例，减少精制碳水'})
        advice_items.append({'icon': '🚶', 'text': '今天需要多走路' + str(extra_steps) + '步来补偿'})
    elif steps_mode == 'reduce':
        advice_items.append({'icon': '🎉', 'text': '昨天热量控制良好，减脂中！'})
        advice_items.append({'icon': '💪', 'text': '保持当前饮食节奏，适当增加蛋白质'})
    else:
        advice_items.append({'icon': '⚖️', 'text': '吃动平衡，维持现状即可'})
    
    if nutrition_score < 2:
        advice_items.append({'icon': '🥗', 'text': '蛋白质摄入不足，建议增加肉类、蛋类'})
    if diversity_score < 0.5:
        advice_items.append({'icon': '🌈', 'text': '食物种类单一，建议增加蔬菜水果'})
    if carb_ratio > 60:
        advice_items.append({'icon': '🍞', 'text': '碳水比例偏高，减少精制碳水'})
    
    if len(advice_items) > 4:
        advice_items = advice_items[:4]
    
    # ===== 补剂推荐（基于达标天数）=====
    if streak_days >= 30:
        supplement_items = supplement_recommendations or [
            {'name': '左旋肉碱', 'dose': '500mg/天', 'reason': '提高脂肪代谢效率'},
            {'name': '复合维生素B族', 'dose': '1片/天', 'reason': '长期热量控制需补充'},
            {'name': '维生素D3', 'dose': '2000IU/天', 'reason': '支持代谢和骨骼健康'},
            {'name': 'Omega-3鱼油', 'dose': '1000mg/天', 'reason': '抗炎和心血管保护'},
        ]
    elif streak_days >= 14:
        supplement_items = supplement_recommendations or [
            {'name': '左旋肉碱', 'dose': '500mg/天', 'reason': '提高脂肪代谢效率'},
            {'name': '复合维生素', 'dose': '1片/天', 'reason': '弥补饮食限制造成的营养缺口'},
            {'name': '镁元素', 'dose': '400mg/天', 'reason': '改善睡眠和肌肉恢复'},
        ]
    elif streak_days >= 7:
        supplement_items = supplement_recommendations or [
            {'name': '乳清蛋白', 'dose': '20g/天', 'reason': '补充优质蛋白'},
            {'name': '复合维生素B', 'dose': '1片/天', 'reason': '支持能量代谢'},
        ]
    elif streak_days >= 3:
        supplement_items = supplement_recommendations or [
            {'name': '电解质粉', 'dose': '适量', 'reason': '运动后补充流失矿物质'},
        ]
    else:
        supplement_items = supplement_recommendations or [
            {'name': '暂无推荐', 'dose': '-', 'reason': '先建立健康的饮食习惯'},
        ]
    
    advice_html = ''.join(['<li><span>' + a['icon'] + '</span> ' + a['text'] + '</li>' for a in advice_items])
    supplement_html = ''.join([
        '<div class="supp-item"><div class="supp-name">' + s['name'] + '</div><div class="supp-dose">' + s['dose'] + '</div><div class="supp-reason">' + s['reason'] + '</div></div>'
        for s in supplement_items
    ])
    
    # ===== 特殊模式 =====
    menstrual_mode_html = ''
    menstrual_day = user_info.get('menstrual_day', 0)
    if menstrual_day > 0:
        phase = MenstrualMode.get_phase(menstrual_day)
        phase_name = MenstrualMode.PHASES.get(phase, {}).get('name', '')
        phase_desc = MenstrualMode.PHASES.get(phase, {}).get('description', '')
        menstrual_mode_html = '<div class="mode-card menstrual"><div class="mode-title">🌸 生理期 · ' + phase_name + '（第' + str(menstrual_day) + '天）</div><div class="mode-desc">' + phase_desc + '</div></div>'
    
    binge_mode_html = ''
    binge_assessment = calc_results.get('binge_assessment')
    if binge_assessment and binge_assessment['level'] in ['severe', 'extreme']:
        recovery_plan = calc_results.get('recovery_plan', {})
        measures_html = ''.join(['<div class="binge-measure">• ' + m['action'] + '：' + m['reason'] + '</div>' for m in recovery_plan.get('measures', [])])
        binge_mode_html = '<div class="mode-card binge"><div class="mode-title">⚠️ 暴食急救 · ' + binge_assessment['label'] + '</div><div class="mode-desc">超出TDEE ' + str(int(binge_assessment['excess_calories'])) + ' kcal</div><div class="binge-measures">' + measures_html + '</div></div>'
    
    # ===== 热量计算 =====
    steps_calories = actual_steps * weight * 0.00042
    remaining_steps = max(0, target_steps - actual_steps)
    fat_color = '#00b894' if fat_change_g < 0 else '#ff7675'
    
    # ===== Kite小结（基于热量差模式）=====
    if steps_mode == 'compensate':
        if steps_completion >= 100:
            kite_tip = "太棒了！虽然昨天超标，但你今天全部补偿回来了！"
        elif steps_completion >= 80:
            kite_tip = "做得不错！差一点就完全补偿回来了，明天继续加油！"
        else:
            kite_tip = "昨天超标了，今天多走走，把多余的热量消耗掉~"
    elif steps_mode == 'reduce':
        if steps_completion >= 100:
            kite_tip = "太棒了！减脂状态保持得很好，继续保持这个节奏！"
        else:
            kite_tip = "昨天热量控制不错，今天走路保持基础消耗就好~"
    else:
        if steps_completion >= 100:
            kite_tip = "完美！吃动平衡，你做得很好！"
        else:
            kite_tip = "今天继续保持平衡就好，走完基础步数~"
    
    # ===== 热量差→步数闭环展示 =====
    loop_display = '''
    <div class="loop-section">
        <div class="loop-title">🔗 热量差→步数闭环</div>
        <div class="loop-flow">
            <div class="loop-item intake">
                <div class="loop-label">昨日摄入</div>
                <div class="loop-value">''' + f'{net_calorie:.0f}' + ''' kcal</div>
            </div>
            <div class="loop-arrow">→</div>
            <div class="loop-item diff">
                <div class="loop-label">热量差</div>
                <div class="loop-value" style="color:''' + diff_color + '''">''' + diff_arrow + f'{abs(calorie_diff):.0f}' + ''' kcal</div>
                <div class="loop-status">''' + diff_status + '''</div>
            </div>
            <div class="loop-arrow">→</div>
            <div class="loop-item steps">
                <div class="loop-label">今日步数</div>
                <div class="loop-value">''' + f'{target_steps:,}' + ''' 步</div>
            </div>
        </div>
        <div class="loop-reason">''' + loop_reason + '''</div>
    </div>
    '''
    
    # ===== 热量差CSS样式 =====
    loop_css = '''
        .loop-section{background:#f8f9fa;border-radius:12px;padding:12px;margin-bottom:12px}
        .loop-title{font-size:11px;color:#667eea;font-weight:600;margin-bottom:10px;text-align:center}
        .loop-flow{display:flex;justify-content:space-between;align-items:center;gap:6px}
        .loop-item{text-align:center;flex:1;background:#fff;border-radius:8px;padding:10px 6px}
        .loop-item.intake{border-top:3px solid #74b9ff}
        .loop-item.diff{border-top:3px solid ''' + diff_color + '''}
        .loop-item.steps{border-top:3px solid #667eea}
        .loop-label{font-size:9px;color:#888;margin-bottom:3px}
        .loop-value{font-size:14px;font-weight:700;color:#333}
        .loop-status{font-size:9px;color:''' + diff_color + ''';margin-top:2px}
        .loop-arrow{font-size:16px;color:#ccc;flex-shrink:0}
        .loop-reason{font-size:10px;color:#888;text-align:center;margin-top:8px;padding-top:8px;border-top:1px dashed #eee}
    '''
    
    
    # ===== 拼装HTML =====
    css_base = '''*{margin:0;padding:0;box-sizing:border-box}body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:linear-gradient(135deg,#667eea,#764ba2);min-height:100vh;padding:15px}.container{max-width:440px;margin:0 auto}.header{background:rgba(255,255,255,0.98);border-radius:20px 20px 0 0;padding:18px;text-align:center}.header h1{color:#667eea;font-size:22px;font-weight:700;margin-bottom:4px}.header .date{color:#888;font-size:12px}.content{background:rgba(255,255,255,0.98);padding:12px}.mode-card{background:#fff;border-radius:10px;padding:10px;margin-bottom:10px;text-align:center}.mode-card.menstrual{border-left:3px solid #f472b6;background:#fdf2f8}.mode-card.binge{border-left:3px solid #ef4444;background:#fef2f2}.mode-title{font-size:13px;font-weight:600;color:#333}.mode-desc{font-size:11px;color:#666}.binge-measures{text-align:left}.binge-measure{font-size:10px;color:#888}.data-section{background:linear-gradient(135deg,#667eea,#764ba2);border-radius:16px;padding:20px;color:#fff;margin-bottom:12px}.data-title{font-size:11px;opacity:0.8;text-align:center;margin-bottom:12px}.data-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,0.2)}.data-row:last-child{border-bottom:none}.data-label{font-size:13px;opacity:0.9}.data-value{font-size:16px;font-weight:700}.loop-section{background:#f8f9fa;border-radius:12px;padding:12px;margin-bottom:12px}.loop-title{font-size:11px;color:#667eea;font-weight:600;margin-bottom:10px;text-align:center}.loop-flow{display:flex;justify-content:space-between;align-items:center;gap:6px}.loop-item{text-align:center;flex:1;background:#fff;border-radius:8px;padding:10px 6px}.loop-item.intake{border-top:3px solid #74b9ff}.loop-item.diff{border-top:3px solid }''' + diff_color + '''}.loop-item.steps{border-top:3px solid #667eea}.loop-label{font-size:9px;color:#888;margin-bottom:3px}.loop-value{font-size:14px;font-weight:700;color:#333}.loop-status{font-size:9px;color:''' + diff_color + ''';margin-top:2px}.loop-arrow{font-size:16px;color:#ccc;flex-shrink:0}.loop-reason{font-size:10px;color:#888;text-align:center;margin-top:8px;padding-top:8px;border-top:1px dashed #eee}.dual-header{display:flex;gap:10px;margin-bottom:12px}.mission-card{flex:1;background:linear-gradient(135deg,#667eea,#764ba2);border-radius:12px;padding:12px;color:#fff;text-align:center}.mission-label{font-size:9px;opacity:0.8;margin-bottom:4px}.mission-target{font-size:28px;font-weight:700}.mission-unit{font-size:11px;opacity:0.8}.mission-progress{background:rgba(255,255,255,0.3);border-radius:6px;height:8px;margin:8px 0}.mission-progress-bar{background:#fff;height:100%;border-radius:6px}.mission-status{font-size:11px}.mission-status.complete{color:#4ade80}.mission-status.good{color:#facc15}.diet-card{flex:1;background:linear-gradient(135deg,#f6d365,#fda085);border-radius:12px;padding:12px;color:#fff;text-align:center}.detail-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:12px}.detail-card{background:#f8f9fa;border-radius:8px;padding:10px;text-align:center}.detail-card .label{font-size:9px;color:#888;margin-bottom:3px}.detail-card .value{font-size:16px;font-weight:700;color:#333}.detail-card .unit{font-size:9px;color:#666}.score-section{background:#fff;border-radius:12px;padding:15px;margin-bottom:12px;border:1px solid #eee}.score-title{font-size:11px;color:#888;text-align:center;margin-bottom:10px}.score-main{display:flex;justify-content:center;align-items:baseline;gap:3px}.score-number{font-size:42px;font-weight:700;color:#f6d365}.score-max{font-size:16px;color:#ccc}.score-stars{text-align:center;font-size:18px;margin-top:5px}.score-breakdown{display:flex;justify-content:center;gap:15px;margin-top:8px;font-size:10px;color:#888}.dual-breakdown{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px}.breakdown-card{background:#f8f9fa;border-radius:10px;padding:12px;text-align:center}.breakdown-title{font-size:10px;color:#888;margin-bottom:6px}.breakdown-stars{font-size:16px;margin-bottom:4px}.breakdown-score{font-size:20px;font-weight:700;color:#333}.breakdown-max{font-size:12px;color:#888}.advice-card{background:#fff;border-radius:10px;padding:12px;margin-bottom:10px;border:1px solid #f0f0f0}.advice-title{font-size:12px;font-weight:600;color:#333;margin-bottom:8px;display:flex;align-items:center;gap:6px}.advice-list{list-style:none}.advice-list li{padding:6px 0;font-size:12px;color:#555;border-bottom:1px solid #f5f5f5}.advice-list li:last-child{border-bottom:none}.supplement-card{background:#fff;border-radius:10px;padding:12px;margin-bottom:10px;border:1px solid #f0f0f0}.supp-title{font-size:12px;font-weight:600;color:#333;margin-bottom:8px;display:flex;align-items:center;gap:6px}.supp-item{background:#f8f9fa;border-radius:8px;padding:10px;margin-bottom:8px}.supp-item:last-child{margin-bottom:0}.supp-name{font-weight:600;color:#333;font-size:12px}.supp-dose{color:#667eea;font-size:11px;margin:3px 0}.supp-reason{color:#888;font-size:10px}.kite-card{background:#fef9e7;border-radius:10px;padding:12px;margin-bottom:10px}.kite-title{font-size:12px;font-weight:600;color:#f39c12;margin-bottom:4px}.kite-text{font-size:12px;color:#555;line-height:1.4}.footer{background:rgba(255,255,255,0.95);border-radius:0 0 20px 20px;padding:10px;text-align:center;font-size:9px;color:#999}'''
    
    html = '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>营养处方 - ' + date_str + '</title><style>' + css_base + '</style></head><body><div class="container"><div class="header"><h1>🍎 营养处方</h1><div class="date">' + date_str + ' ' + weekday + '</div></div><div class="content">' + menstrual_mode_html + binge_mode_html + '<div class="data-section"><div class="data-title">📊 核心数据</div><div class="data-row"><span class="data-label">【总  热  量】</span><span class="data-value">' + str(int(intake)) + ' 千卡，碳水 ' + str(int(carb_ratio)) + '%</span></div><div class="data-row"><span class="data-label">【最新体重】</span><span class="data-value">' + str(weight) + ' 公斤</span></div><div class="data-row"><span class="data-label">【脂肪增量】</span><span class="data-value" style="color:' + fat_color + '">' + str(int(fat_change_g)) + ' 克</span></div><div class="data-row"><span class="data-label">【目标步数】</span><span class="data-value">' + f'{target_steps:,}' + ' 步</span></div><div class="data-row"><span class="data-label">【今日得分】</span><span class="data-value">' + f'{total_final_score:.1f}' + ' 分</span></div></div>' + loop_display + '<div class="dual-header"><div class="mission-card"><div class="mission-label">🚶 步数监督</div><div class="mission-target">' + f'{target_steps:,}' + '</div><div class="mission-unit">步目标</div><div class="mission-progress"><div class="mission-progress-bar"></div></div><div class="mission-status ' + steps_status + '">' + steps_status_text + ' ' + f'{actual_steps:,}' + '/' + f'{target_steps:,}' + '</div></div><div class="diet-card"><div class="mission-label">🍽️ 饮食记录</div><div class="mission-target">' + str(int(intake)) + '</div><div class="mission-unit">千卡摄入</div><div class="mission-progress" style="background:rgba(0,0,0,0.2)"><div class="mission-progress-bar" style="width:' + f'{min(100, intake/30)}' + '%"></div></div><div class="mission-status">' + str(int(carb_ratio)) + '%碳水</div></div></div><div class="detail-grid"><div class="detail-card"><div class="label">已完成</div><div class="value">' + f'{actual_steps:,}' + '</div><div class="unit">步</div></div><div class="detail-card"><div class="label">消耗热量</div><div class="value">' + f'{steps_calories:.0f}' + '</div><div class="unit">千卡</div></div><div class="detail-card"><div class="label">还需步数</div><div class="value">' + f'{remaining_steps:,}' + '</div><div class="unit">步</div></div><div class="detail-card"><div class="label">连续达标</div><div class="value">' + str(streak_days) + '</div><div class="unit">天</div></div></div><div class="score-section"><div class="score-title">综合评分</div><div class="score-main"><div class="score-number">' + f'{total_final_score:.1f}' + '</div><div class="score-max">/10</div></div><div class="score-stars">' + final_stars + '</div><div class="score-breakdown"><span>步数 ' + f'{steps_score:.1f}' + '/5</span><span>·</span><span>饮食 ' + f'{diet_score:.1f}' + '/5</span></div></div><div class="dual-breakdown"><div class="breakdown-card"><div class="breakdown-title">🚶 步数评分</div><div class="breakdown-stars">' + steps_stars + '</div><div class="breakdown-score">' + f'{steps_score:.1f}' + '<span class="breakdown-max">/5</span></div></div><div class="breakdown-card"><div class="breakdown-title">🍽️ 饮食评分</div><div class="breakdown-stars">' + diet_stars + '</div><div class="breakdown-score">' + f'{diet_score:.1f}' + '<span class="breakdown-max">/5</span></div></div></div><div class="advice-card"><div class="advice-title">💡 营养建议</div><ul class="advice-list">' + advice_html + '</ul></div><div class="supplement-card"><div class="supp-title">💊 营养补剂推荐</div>' + supplement_html + '</div><div class="kite-card"><div class="kite-title">💡 Kite小结</div><div class="kite-text">' + kite_tip + '</div></div></div><div class="footer">本建议仅供日常参考，效果因人而异，实施前请咨询专业人士<br>免责声明：本报告基于估算数据，不构成医疗建议</div></div></body></html>'
    return html

