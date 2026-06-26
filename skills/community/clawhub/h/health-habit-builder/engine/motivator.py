"""
Health Habit Builder - Motivator
健康习惯养成师 - 动机分析引擎
"""

from typing import Dict, Any, List


def analyze_motivation(habit_id: str, habit_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    分析动机
    
    Args:
        habit_id: 习惯ID
        habit_data: 习惯数据
        
    Returns:
        动机分析结果
    """
    # 模拟动机分析
    streak = 7 if habit_data is None else habit_data.get("streak", {}).get("current", 0)
    
    # 根据连续天数调整动机评分
    if streak >= 21:
        intrinsic = 85
        extrinsic = 50
    elif streak >= 7:
        intrinsic = 72
        extrinsic = 45
    else:
        intrinsic = 60
        extrinsic = 40
    
    overall = int((intrinsic * 0.6 + extrinsic * 0.4))
    
    # 判断趋势
    if streak >= 14:
        trend = "improving"
    elif streak >= 3:
        trend = "stable"
    else:
        trend = "declining"
    
    return {
        "levels": {
            "intrinsic": intrinsic,
            "extrinsic": extrinsic,
            "overall": overall
        },
        "trend": trend,
        "positiveFactors": _get_positive_factors(streak),
        "negativeFactors": _get_negative_factors(streak),
        "recommendations": _get_recommendations(trend, intrinsic)
    }


def _get_positive_factors(streak: int) -> List[str]:
    """获取积极因素"""
    factors = []
    
    if streak >= 7:
        factors.append("已完成连续7天，信心增强")
    if streak >= 14:
        factors.append("进入第二周，习惯正在形成")
        factors.append("开始感受到正向变化")
    if streak >= 3:
        factors.append("已有一定基础，不易放弃")
    
    if not factors:
        factors.append("刚开始，动机最强")
    
    return factors


def _get_negative_factors(streak: int) -> List[str]:
    """获取消极因素"""
    factors = []
    
    if streak < 7:
        factors.append("习惯尚未稳定，需要坚持")
    
    if streak < 3:
        factors.append("放弃概率较高，需要注意")
    
    factors.append("可能遇到动力下降期")
    
    return factors


def _get_recommendations(trend: str, intrinsic: int) -> List[Dict[str, Any]]:
    """获取建议"""
    recommendations = []
    
    if trend == "declining":
        recommendations.append({
            "type": "boost",
            "action": "尝试不同的时间或地点增加新鲜感",
            "priority": "high"
        })
        recommendations.append({
            "type": "recover",
            "action": "回顾最初的动力，重新聚焦目标",
            "priority": "high"
        })
    elif trend == "stable":
        recommendations.append({
            "type": "sustain",
            "action": "继续关注内在感受而非外在奖励",
            "priority": "medium"
        })
        recommendations.append({
            "type": "boost",
            "action": "加入一点变化防止枯燥",
            "priority": "low"
        })
    else:  # improving
        recommendations.append({
            "type": "sustain",
            "action": "保持当前节奏，注意不要过度",
            "priority": "high"
        })
    
    return recommendations
