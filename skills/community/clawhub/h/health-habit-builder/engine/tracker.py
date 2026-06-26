"""
Health Habit Builder - Tracker
健康习惯养成师 - 打卡跟踪器
"""

from datetime import datetime
from typing import Dict, Any, Optional


def check_in(habit_id: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理打卡
    
    Args:
        habit_id: 习惯ID
        feedback: 打卡反馈
        
    Returns:
        打卡结果
    """
    status = feedback.get("status", "completed")
    date = datetime.now().strftime("%Y-%m-%d")
    
    result = {
        "habitId": habit_id,
        "date": date,
        "status": status,
        "currentStreak": 1,
        "longestStreak": 1,
        "totalCompleted": 1,
        "message": ""
    }
    
    if status == "completed":
        result["currentStreak"] = feedback.get("streak", 1) + 1
        result["longestStreak"] = max(result["currentStreak"], feedback.get("longestStreak", 1))
        result["totalCompleted"] = feedback.get("totalCompleted", 0) + 1
        result["message"] = f"太棒了！已连续完成 {result['currentStreak']} 天"
    elif status == "skipped":
        result["currentStreak"] = 0
        result["message"] = "今天跳过了，没关系，明天继续加油"
    else:
        result["currentStreak"] = 0
        result["message"] = "部分完成，继续努力"
    
    return result


def get_progress(habit_id: str, habit_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    获取进度报告
    
    Args:
        habit_id: 习惯ID
        habit_data: 习惯数据
        
    Returns:
        进度报告
    """
    if habit_data is None:
        habit_data = {
            "name": "未知习惯",
            "currentPhase": "initiation",
            "streak": {"current": 0, "longest": 0, "totalDays": 0},
            "completionRate": 0,
            "history": []
        }
    
    return {
        "habitId": habit_id,
        "habitName": habit_data.get("name", "未知习惯"),
        "currentPhase": _get_phase_name(habit_data.get("currentPhase", "initiation")),
        "streak": habit_data.get("streak", {"current": 0, "longest": 0, "totalDays": 0}),
        "completionRate": habit_data.get("completionRate", 0),
        "consistencyScore": _calc_consistency(habit_data),
        "recentHistory": habit_data.get("history", [])[-10:],
        "motivationLevel": {
            "current": 75,
            "trend": "stable"
        },
        "nextMilestone": {
            "daysRemaining": max(0, 21 - habit_data.get("streak", {}).get("totalDays", 0)),
            "reward": "21天徽章"
        }
    }


def _calc_consistency(habit_data: Dict[str, Any]) -> int:
    """计算一致性评分"""
    streak = habit_data.get("streak", {})
    total = streak.get("totalDays", 0)
    longest = streak.get("longest", 0)
    
    if total == 0:
        return 0
    
    return int(longest / total * 100)


def _get_phase_name(phase: str) -> str:
    """获取阶段中文名称"""
    names = {
        "initiation": "启动期",
        "learning": "学习期",
        "integration": "整合期",
        "maintenance": "维持期",
        "mastery": "精通期"
    }
    return names.get(phase, "启动期")
