#!/usr/bin/env python3
"""
Health Habit Builder - Test Script
健康习惯养成师 - 自测脚本
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import handle_habit_request


def test_create():
    print("\n1. 测试创建习惯...")
    request = {
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
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        plan = result.get("habitPlan", {})
        print(f"  习惯ID: {plan.get('id')}")
        print(f"  难度评分: {plan.get('difficultyAssessment', {}).get('overall')}")
        print(f"  成功概率: {plan.get('difficultyAssessment', {}).get('successProbability')}")
        print(f"  预计形成时间: {plan.get('difficultyAssessment', {}).get('estimatedFormationTime')}天")
        return plan.get("id")
    return "test_habit_001"


def test_evaluate():
    print("\n2. 测试评估习惯...")
    request = {
        "intent": "evaluate",
        "habit": {"name": "早起锻炼"},
        "userContext": {"pastFailures": "太累了起不来"}
    }
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        eval_data = result.get("evaluation", {})
        print(f"  难度: {eval_data.get('overallDifficulty')}")
        print(f"  成功概率: {eval_data.get('successProbability')}")
        print(f"  建议: {eval_data.get('recommendations', [])[:2]}")


def test_checkin(habit_id):
    print("\n3. 测试打卡...")
    request = {
        "intent": "checkIn",
        "habitId": habit_id,
        "feedback": {
            "status": "completed",
            "quality": 8,
            "notes": "感觉很好"
        }
    }
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        checkin = result.get("checkInResult", {})
        print(f"  连续天数: {checkin.get('currentStreak')}")
        print(f"  消息: {checkin.get('message')}")


def test_progress(habit_id):
    print("\n4. 测试进度查询...")
    request = {
        "intent": "progress",
        "habitId": habit_id
    }
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        report = result.get("progressReport", {})
        print(f"  习惯名: {report.get('habitName')}")
        print(f"  当前阶段: {report.get('currentPhase')}")
        print(f"  连续: {report.get('streak', {}).get('current')}天")
        print(f"  完成率: {report.get('completionRate')}%")


def test_motivate(habit_id):
    print("\n5. 测试动机分析...")
    request = {
        "intent": "motivate",
        "habitId": habit_id
    }
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        analysis = result.get("motivationAnalysis", {})
        print(f"  总体动机: {analysis.get('levels', {}).get('overall')}")
        print(f"  趋势: {analysis.get('trend')}")
        print(f"  建议数量: {len(analysis.get('recommendations', []))}")


def test_adjust():
    print("\n6. 测试习惯调整...")
    request = {
        "intent": "adjust",
        "habitId": "test_habit_001",
        "adjustment": {
            "type": "difficulty",
            "description": "感觉太难了"
        }
    }
    result = handle_habit_request(request)
    print(f"  成功: {result.get('success')}")
    if result.get("success"):
        suggestion = result.get("adjustmentSuggestion", {})
        print(f"  调整类型: {suggestion.get('type')}")
        print(f"  原因: {suggestion.get('reasoning')}")


def main():
    print("=" * 50)
    print("Health Habit Builder 自测")
    print("=" * 50)
    
    habit_id = test_create()
    test_evaluate()
    test_checkin(habit_id)
    test_progress(habit_id)
    test_motivate(habit_id)
    test_adjust()
    
    print("\n" + "=" * 50)
    print("自测完成")
    print("=" * 50)


if __name__ == "__main__":
    main()
