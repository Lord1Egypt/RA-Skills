#!/usr/bin/env python3
"""
健康管理系统主程序 v1.0
通用版本 - 支持多用户 - 完整闭环 - 动态更新
"""

import sys
import json
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from indicator_extractor import process_text_input, load_user_health_data
from exercise_generator import generate_exercise_plan, load_user_plan, get_today_plan
from video_matcher import get_video_link
from checkin_manager import record_checkin, get_checkin_stats, get_monthly_summary
from data_comparator import save_health_record, compare_health_data, should_update_plan
from feishu_doc_writer import save_checkin, load_checkins, generate_weekly_report, generate_monthly_report


def handle_user_input(user_id, input_data, input_type="text"):
    """处理用户输入（多模态）"""
    result = {"success": False, "user_id": user_id, "step": "unknown"}
    
    if input_type == "text":
        indicators = process_text_input(user_id, input_data)
        save_health_record(user_id, indicators["indicators"], "文字输入")
        
        result["step"] = "extract"
        result["indicators"] = indicators["indicators"]
        result["abnormal"] = indicators["abnormal"]
        
        update_check = should_update_plan(user_id)
        result["needs_plan_update"] = update_check.get("need_update", False)
        
        if indicators["abnormal"]:
            plan = generate_exercise_plan(user_id, indicators["abnormal"])
            result["step"] = "plan_generated"
            result["health_issues"] = plan["health_issues"]
            result["weekly_plan"] = plan["weekly_plan"]
            
            if update_check.get("need_update"):
                result["message"] = "检测到体检数据变化，运动计划已自动更新！"
                result["changes"] = update_check.get("changes", [])
            else:
                result["message"] = "运动计划已生成"
        
        result["success"] = True
    
    return result


def get_daily_push_content(user_id):
    """获取每日推送内容（运动计划 + 视频链接）"""
    today = get_today_plan(user_id)
    if not today:
        return "暂无运动计划，请先上传体检报告"
    
    day = today["day"]
    plan = today["plan"]
    
    message = f"🏃 **{day}运动计划**\n\n"
    
    for time_slot, details in plan.items():
        exercise = details.get("运动", "")
        duration = details.get("时长", "")
        purpose = details.get("目的", "")
        
        message += f"⏰ {time_slot}：{exercise} ({duration}) - {purpose}\n"
        
        video = get_video_link(exercise)
        if video:
            message += f"   📹 动作教程：{video}\n"
        
        message += "\n"
    
    message += "💪 跟练视频更有效！"
    
    return message


def handle_checkin(user_id, date=None, **data):
    """处理打卡（自动保存到本地/飞书）"""
    if date is None:
        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 保存打卡（自动选择飞书或本地）
    save_result = save_checkin(user_id, date, data)
    
    # 获取统计
    stats = get_checkin_stats(user_id, 7)
    
    response = {
        "success": True,
        "message": f"✅ 打卡成功！已连续打卡 {stats['连续打卡天数']} 天",
        "stats": stats
    }
    
    # 如果飞书失败，提示用户
    if save_result.get("warning"):
        response["warning"] = save_result["warning"]
        response["local_path"] = save_result.get("local_path", "")
    
    return response


def handle_weekly_review(user_id):
    """处理周复盘"""
    from datetime import datetime, timedelta
    
    # 获取本周数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    
    week_data = {}
    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        month_str = current.strftime("%Y-%m")
        month_data = load_checkins(user_id, month_str)
        if date_str in month_data:
            week_data[date_str] = month_data[date_str]
        current += timedelta(days=1)
    
    return generate_weekly_report(user_id, week_data)


def handle_monthly_review(user_id, year_month=None):
    """处理月度复盘"""
    if year_month is None:
        from datetime import datetime
        year_month = datetime.now().strftime("%Y-%m")
    
    month_data = load_checkins(user_id, year_month)
    return generate_monthly_report(user_id, month_data)


def get_system_status(user_id):
    """获取系统状态"""
    health_data = load_user_health_data(user_id)
    plan = load_user_plan(user_id)
    stats = get_checkin_stats(user_id, 7)
    comparison = compare_health_data(user_id)
    
    return {
        "user_id": user_id,
        "has_health_data": health_data is not None,
        "has_exercise_plan": plan is not None,
        "has_history": comparison.get("has_history", False),
        "checkin_stats": stats,
        "health_issues": plan.get("health_issues", []) if plan else [],
        "latest_indicators": health_data.get("indicators", {}) if health_data else {}
    }


if __name__ == "__main__":
    # 测试
    user_id = "test_user"
    
    print("=== 测试打卡功能 ===")
    result = handle_checkin(user_id, 运动项目="八段锦", 运动时长=30, 步数=5000)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n=== 测试周报 ===")
    print(handle_weekly_review(user_id))
    
    print("\n=== 测试月报 ===")
    print(handle_monthly_review(user_id))
    
    print("\n=== 测试每日推送 ===")
    print(get_daily_push_content(user_id))
