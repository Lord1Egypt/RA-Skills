"""
Health Habit Builder - Difficulty Assessor
健康习惯养成师 - 难度评估引擎
"""

import random
from typing import Dict, Any


def assess_habit_difficulty(habit_name: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估习惯难度
    
    Args:
        habit_name: 习惯名称
        user_context: 用户上下文
        
    Returns:
        难度评估结果
    """
    # 基于关键词估算基础难度
    base_difficulty = _estimate_base_difficulty(habit_name)
    
    # 根据用户历史调整
    past_failures = user_context.get("pastFailures", "")
    if past_failures:
        if "时间" in past_failures or "忙" in past_failures:
            base_difficulty += 1
        if "坚持" in past_failures:
            base_difficulty += 1
        if "懒" in past_failures:
            base_difficulty += 1
    
    # 限制在1-10范围
    overall = max(1, min(10, base_difficulty))
    
    # 计算成功概率
    success_probability = _calculate_success_probability(overall, user_context)
    
    # 估算形成时间
    estimated_time = _estimate_formation_time(overall)
    
    # 难度因素分析
    factors = _analyze_difficulty_factors(habit_name, overall)
    
    return {
        "overall": overall,
        "factors": factors,
        "successProbability": success_probability,
        "estimatedFormationTime": estimated_time
    }


def _estimate_base_difficulty(habit_name: str) -> int:
    """估算基础难度"""
    difficulty_map = {
        "冥想": 4,
        "运动": 5,
        "跑步": 5,
        "健身": 6,
        "瑜伽": 4,
        "阅读": 3,
        "写作": 5,
        "早起": 6,
        "早睡": 5,
        "喝水": 2,
        "刷牙": 1,
        "冥想": 4,
        "学习": 5,
        "英语": 5,
        "跑步": 5,
        "走路": 2,
        "散步": 2,
        "休息": 3,
        "午睡": 3,
    }
    
    for key, diff in difficulty_map.items():
        if key in habit_name:
            return diff
    
    # 默认中等难度
    return 5


def _calculate_success_probability(overall: int, user_context: Dict[str, Any]) -> float:
    """计算成功概率"""
    # 基础概率
    base_prob = 1 - (overall - 1) / 9 * 0.5
    
    # 调整因素
    motivation_type = user_context.get("motivationType", "")
    if "内在" in motivation_type:
        base_prob += 0.1
    
    past_failures = user_context.get("pastFailures", "")
    if past_failures:
        base_prob -= 0.1
    
    return max(0.1, min(0.95, base_prob))


def _estimate_formation_time(overall: int) -> int:
    """估算习惯形成时间"""
    # 基于研究：平均66天，范围18-254天
    base_time = 66
    adjustment = (overall - 5) * 5
    return max(18, min(254, base_time + adjustment))


def _analyze_difficulty_factors(habit_name: str, overall: int) -> list:
    """分析难度因素"""
    factors = []
    
    if overall >= 5:
        factors.append({
            "factor": "时间安排",
            "impact": overall - 3,
            "mitigation": "选择固定时间段，关联到已有习惯"
        })
    
    if overall >= 6:
        factors.append({
            "factor": "意志力消耗",
            "impact": overall - 4,
            "mitigation": "降低初始难度，建立仪式感"
        })
    
    factors.append({
        "factor": "环境干扰",
        "impact": max(1, overall - 5),
        "mitigation": "创造有利的环境，减少干扰源"
    })
    
    if overall >= 7:
        factors.append({
            "factor": "动力衰减",
            "impact": overall - 4,
            "mitigation": "设置阶段性奖励，关注内在满足感"
        })
    
    return factors
