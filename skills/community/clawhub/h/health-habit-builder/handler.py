"""
Health Habit Builder - Main Handler
健康习惯养成师 - 主逻辑入口
"""

import json
import uuid
from datetime import datetime, timedelta

from engine.types import HabitRequest, HabitResponse, HabitPhase
from engine.assessor import assess_habit_difficulty
from engine.microhabit import generate_microhabits
from engine.tracker import check_in, get_progress
from engine.motivator import analyze_motivation

# 模拟数据存储
_habits_db = {}
_checkins_db = {}


def handle_habit_request(request: dict) -> dict:
    try:
        intent = request.get("intent")
        
        if intent == "create":
            return _handle_create(request)
        elif intent == "evaluate":
            return _handle_evaluate(request)
        elif intent == "checkIn":
            return _handle_checkin(request)
        elif intent == "progress":
            return _handle_progress(request)
        elif intent == "adjust":
            return _handle_adjust(request)
        elif intent == "motivate":
            return _handle_motivate(request)
        else:
            return {
                "success": False,
                "error": {
                    "code": "INVALID_INTENT",
                    "message": f"未知的意图: {intent}"
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e)
            }
        }


def _handle_create(request: dict) -> dict:
    habit_info = request.get("habit", {})
    user_context = request.get("userContext", {})
    
    habit_id = f"habit_{uuid.uuid4().hex[:8]}"
    habit_name = habit_info.get("name", "未命名习惯")
    
    difficulty_result = assess_habit_difficulty(habit_name, user_context)
    microhabits = generate_microhabits(habit_name, difficulty_result.get("overall", 5))
    
    habit_plan = {
        "id": habit_id,
        "name": habit_name,
        "description": habit_info.get("description", f"养成{habit_name}的健康习惯"),
        "scientificBasis": {
            "model": "Fogg行为模型 + 习惯循环理论",
            "principles": [
                "从小开始 - 微习惯不超过2分钟",
                "锚点触发 - 关联现有习惯",
                "即时奖励 - 完成后立即给予正向反馈",
                "渐进式增加难度"
            ],
            "evidence": "研究表明，66天的持续练习可使行为自动化的概率达到80%以上"
        },
        "difficultyAssessment": difficulty_result,
        "microHabitProgression": microhabits,
        "personalization": {
            "recommendedTime": _recommend_time(habit_name),
            "environmentSetup": _get_environment_setup(habit_name),
            "reminderStrategy": {
                "primary": "早晨7:00推送提醒",
                "backup": "关联到现有习惯（如刷牙后）",
                "content": "积极的启动语 + 进度提醒"
            }
        },
        "motivationSystem": {
            "intrinsicRewards": [
                f"即时感受：完成{habit_name}后的成就感",
                f"短期收益：当天的精神状态改善",
                "长期价值：形成自动化行为，减轻意志力负担"
            ],
            "extrinsicRewards": [
                "完成7天：解锁新徽章",
                "完成21天：获得习惯养成者称号",
                "完成66天：习惯完全形成"
            ],
            "accountability": {
                "selfTracking": "每日打卡+简短反思",
                "progressVisualization": "连续天数日历+完成率图表"
            }
        },
        "troubleshootingGuide": {
            "commonChallenges": [
                {
                    "scenario": "忘记执行",
                    "solution": "设置双重提醒，关联到现有习惯",
                    "prevention": "选择固定的执行时间和地点"
                },
                {
                    "scenario": "动力不足",
                    "solution": "降低难度，重新从微习惯开始",
                    "prevention": "关注内在奖励而非外在奖励"
                },
                {
                    "scenario": "中断一天",
                    "solution": "不要自责，第二天继续即可",
                    "prevention": "设置预防机制，如提前准备"
                }
            ]
        }
    }
    
    _habits_db[habit_id] = {
        "id": habit_id,
        "name": habit_name,
        "startDate": datetime.now().strftime("%Y-%m-%d"),
        "currentPhase": "initiation",
        "streak": {"current": 0, "longest": 0, "totalDays": 0},
        "completionRate": 0,
        "history": []
    }
    
    return {
        "success": True,
        "habitPlan": habit_plan
    }


def _handle_evaluate(request: dict) -> dict:
    habit_info = request.get("habit", {})
    habit_name = habit_info.get("name", "")
    user_context = request.get("userContext", {})
    
    difficulty_result = assess_habit_difficulty(habit_name, user_context)
    
    return {
        "success": True,
        "evaluation": {
            "overallDifficulty": difficulty_result.get("overall", 5),
            "successProbability": difficulty_result.get("successProbability", 0.5),
            "barriers": _analyze_barriers(habit_name, user_context),
            "recommendations": _generate_recommendations(habit_name, difficulty_result),
            "estimatedTime": difficulty_result.get("estimatedFormationTime", 66)
        }
    }


def _handle_checkin(request: dict) -> dict:
    habit_id = request.get("habitId", "")
    feedback = request.get("feedback", {})
    
    if habit_id not in _habits_db:
        _habits_db[habit_id] = {
            "id": habit_id,
            "name": "模拟习惯",
            "startDate": datetime.now().strftime("%Y-%m-%d"),
            "currentPhase": "learning",
            "streak": {"current": 5, "longest": 10, "totalDays": 15},
            "completionRate": 85,
            "history": []
        }
    
    habit = _habits_db[habit_id]
    status = feedback.get("status", "completed")
    
    if status == "completed":
        habit["streak"]["current"] += 1
        habit["streak"]["totalDays"] += 1
        habit["streak"]["longest"] = max(habit["streak"]["longest"], habit["streak"]["current"])
        message = f"太棒了！已连续完成 {habit['streak']['current']} 天"
    elif status == "skipped":
        habit["streak"]["current"] = 0
        message = "今天跳过了，没关系，明天继续加油"
    else:
        habit["streak"]["current"] = 0
        message = "部分完成，继续努力"
    
    habit["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": status,
        "quality": feedback.get("quality"),
        "notes": feedback.get("notes", "")
    })
    
    return {
        "success": True,
        "checkInResult": {
            "habitId": habit_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": status,
            "currentStreak": habit["streak"]["current"],
            "longestStreak": habit["streak"]["longest"],
            "totalCompleted": habit["streak"]["totalDays"],
            "message": message
        }
    }


def _handle_progress(request: dict) -> dict:
    habit_id = request.get("habitId", "")
    
    if habit_id not in _habits_db:
        _habits_db[habit_id] = {
            "id": habit_id,
            "name": "每日冥想",
            "startDate": (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d"),
            "currentPhase": "learning",
            "streak": {"current": 7, "longest": 14, "totalDays": 21},
            "completionRate": 85,
            "history": [
                {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), "status": "completed"}
                for i in range(min(7, 21))
            ]
        }
    
    habit = _habits_db[habit_id]
    
    recent_history = habit.get("history", [])
    if not recent_history:
        recent_history = [
            {"date": (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d"), "status": "completed"}
            for i in range(7)
        ]
    
    return {
        "success": True,
        "progressReport": {
            "habitId": habit_id,
            "habitName": habit.get("name", "未知习惯"),
            "currentPhase": _get_phase_name(habit.get("currentPhase", "initiation")),
            "streak": habit["streak"],
            "completionRate": habit.get("completionRate", 0),
            "consistencyScore": int(habit["streak"]["longest"] / max(habit["streak"]["totalDays"], 1) * 100),
            "recentHistory": recent_history[-10:],
            "motivationLevel": {
                "current": 75,
                "trend": "stable"
            },
            "nextMilestone": {
                "daysRemaining": max(0, 21 - habit["streak"]["totalDays"]),
                "reward": "21天徽章"
            }
        }
    }


def _handle_adjust(request: dict) -> dict:
    habit_id = request.get("habitId", "")
    adjustment = request.get("adjustment", {})
    adjustment_type = adjustment.get("type", "difficulty")
    description = adjustment.get("description", "")
    
    suggestions = {
        "goal": {
            "type": "goal",
            "changes": {
                "frequency": "调整为每周4-5次而非每天",
                "duration": "缩短单次时间至10分钟"
            },
            "reasoning": "降低门槛可以提高坚持概率",
            "expectedOutcome": "完成率提升，动力增强"
        },
        "schedule": {
            "type": "schedule",
            "changes": {
                "time": "从晚上改到早晨",
                "trigger": "关联到起床后第一件事"
            },
            "reasoning": "早晨精力充沛，干扰更少",
            "expectedOutcome": "完成质量提升"
        },
        "difficulty": {
            "type": "difficulty",
            "changes": {
                "action": "拆分为更小的微习惯",
                "simplicity": "从1分钟开始"
            },
            "reasoning": "降低阻力是维持习惯的关键",
            "expectedOutcome": "更容易启动和坚持"
        }
    }
    
    return {
        "success": True,
        "adjustmentSuggestion": suggestions.get(adjustment_type, suggestions["difficulty"])
    }


def _handle_motivate(request: dict) -> dict:
    habit_id = request.get("habitId", "")
    
    return {
        "success": True,
        "motivationAnalysis": {
            "levels": {
                "intrinsic": 72,
                "extrinsic": 45,
                "overall": 65
            },
            "trend": "stable",
            "positiveFactors": [
                "已完成连续7天，信心增强",
                "感受到睡眠质量改善",
                "形成了一定的仪式感"
            ],
            "negativeFactors": [
                "偶尔感到枯燥",
                "时间安排不够稳定"
            ],
            "recommendations": [
                {
                    "type": "boost",
                    "action": "尝试不同的时间或地点增加新鲜感",
                    "priority": "high"
                },
                {
                    "type": "sustain",
                    "action": "继续关注内在感受而非外在奖励",
                    "priority": "medium"
                }
            ]
        }
    }


def _recommend_time(habit_name: str) -> str:
    time_map = {
        "冥想": "早晨起床后或晚上睡前",
        "运动": "早晨7-8点或晚上6-7点",
        "阅读": "睡前30分钟",
        "写作": "早晨精力最充沛的时段",
        "喝水": "全天分散，多设置提醒"
    }
    
    for key, time in time_map.items():
        if key in habit_name:
            return time
    return "根据个人日程选择固定时间，建议早晨或晚上"


def _get_environment_setup(habit_name: str) -> list:
    return [
        "准备一个固定的位置/角落",
        "移除干扰物（如手机静音）",
        "准备好所需物品/装备",
        "营造舒适的氛围（灯光、音乐等）"
    ]


def _analyze_barriers(habit_name: str, user_context: dict) -> list:
    barriers = []
    past_failures = user_context.get("pastFailures", "")
    
    if "时间" in past_failures or "忙" in past_failures:
        barriers.append({
            "barrier": "时间不足",
            "severity": "high",
            "mitigation": "将习惯拆分为更小的微习惯，选择不被打扰的时段"
        })
    
    if "坚持" in past_failures or "懒" in past_failures:
        barriers.append({
            "barrier": "意志力不足",
            "severity": "high",
            "mitigation": "降低难度，关联到已有习惯，利用环境设计减少阻力"
        })
    
    if "忘记" in past_failures:
        barriers.append({
            "barrier": "容易忘记",
            "severity": "medium",
            "mitigation": "设置多重提醒，绑定到现有习惯作为触发器"
        })
    
    if not barriers:
        barriers = [
            {
                "barrier": "启动阻力",
                "severity": "medium",
                "mitigation": "从极小的微习惯开始，如1分钟版本"
            },
            {
                "barrier": "单调乏味",
                "severity": "low",
                "mitigation": "加入变化和奖励，保持新鲜感"
            }
        ]
    
    return barriers


def _generate_recommendations(habit_name: str, difficulty_result: dict) -> list:
    difficulty = difficulty_result.get("overall", 5)
    recommendations = []
    
    if difficulty >= 7:
        recommendations.append("建议从极简版本开始，如每天1分钟")
        recommendations.append("先将这个习惯和已有习惯绑定")
    
    if difficulty >= 5:
        recommendations.append("设置提醒和奖励系统")
        recommendations.append("找一个 accountability partner 互相监督")
    
    recommendations.append("记录进度，保持可视化")
    recommendations.append("允许偶尔跳过，但不要连续中断超过2天")
    
    return recommendations


def _get_phase_name(phase: str) -> str:
    phase_names = {
        "initiation": "启动期",
        "learning": "学习期",
        "integration": "整合期",
        "maintenance": "维持期",
        "mastery": "精通期"
    }
    return phase_names.get(phase, "启动期")


if __name__ == "__main__":
    print("=== Health Habit Builder 自测 ===")
    print()
    print("1. 测试创建习惯...")
    create_request = {
        "intent": "create",
        "habit": {
            "name": "每日冥想",
            "description": "通过每日冥想培养正念，减少压力",
            "frequency": "每天"
        },
        "userContext": {
            "pastFailures": "之前尝试过但坚持不到一周",
            "motivationType": "内在驱动"
        }
    }
    result = handle_habit_request(create_request)
    print(f"成功: {result.get('success')}")
    if result.get("success"):
        habit_plan = result.get("habitPlan", {})
        print(f"习惯ID: {habit_plan.get('id')}")
        print(f"难度评分: {habit_plan.get('difficultyAssessment', {}).get('overall')}")
        print(f"成功概率: {habit_plan.get('difficultyAssessment', {}).get('successProbability')}")
        print(f"预计形成时间: {habit_plan.get('difficultyAssessment', {}).get('estimatedFormationTime')}天")
    
    print()
    print("2. 测试评估习惯...")
    eval_request = {
        "intent": "evaluate",
        "habit": {"name": "早起锻炼"},
        "userContext": {"pastFailures": "太累了起不来"}
    }
    eval_result = handle_habit_request(eval_request)
    print(f"成功: {eval_result.get('success')}")
    if eval_result.get("success"):
        eval_data = eval_result.get("evaluation", {})
        print(f"难度: {eval_data.get('overallDifficulty')}")
        print(f"建议: {eval_data.get('recommendations', [])[:2]}")
    
    print()
    print("3. 测试打卡...")
    habit_id = result.get("habitPlan", {}).get("id", "test_habit_001") if result.get("success") else "test_habit_001"
    checkin_request = {
        "intent": "checkIn",
        "habitId": habit_id,
        "feedback": {
            "status": "completed",
            "quality": 8,
            "notes": "感觉很好"
        }
    }
    checkin_result = handle_habit_request(checkin_request)
    print(f"成功: {checkin_result.get('success')}")
    if checkin_result.get("success"):
        print(f"连续天数: {checkin_result.get('checkInResult', {}).get('currentStreak')}")
        print(f"消息: {checkin_result.get('checkInResult', {}).get('message')}")
    
    print()
    print("4. 测试进度查询...")
    progress_request = {
        "intent": "progress",
        "habitId": habit_id
    }
    progress_result = handle_habit_request(progress_request)
    print(f"成功: {progress_result.get('success')}")
    if progress_result.get("success"):
        report = progress_result.get("progressReport", {})
        print(f"习惯名: {report.get('habitName')}")
        print(f"当前阶段: {report.get('currentPhase')}")
        print(f"连续: {report.get('streak', {}).get('current')}天")
        print(f"完成率: {report.get('completionRate')}%")
    
    print()
    print("5. 测试动机分析...")
    motivate_request = {
        "intent": "motivate",
        "habitId": habit_id
    }
    motivate_result = handle_habit_request(motivate_request)
    print(f"成功: {motivate_result.get('success')}")
    if motivate_result.get("success"):
        analysis = motivate_result.get("motivationAnalysis", {})
        print(f"总体动机: {analysis.get('levels', {}).get('overall')}")
        print(f"趋势: {analysis.get('trend')}")
        print(f"建议数量: {len(analysis.get('recommendations', []))}")
    
    print()
    print("=== 自测完成 ===")
