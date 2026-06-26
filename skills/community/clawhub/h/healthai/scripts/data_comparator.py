#!/usr/bin/env python3
"""
数据变化检测器
对比多次体检数据，检测指标变化趋势
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
USERS_DIR = BASE_DIR / "data" / "users"


def save_health_record(user_id, indicators, record_type="体检"):
    """保存健康记录（每次体检/数据都独立存）"""
    user_dir = USERS_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建记录文件
    records_file = user_dir / "health_records.json"
    
    # 加载现有记录
    if records_file.exists():
        with open(records_file, encoding="utf-8") as f:
            records = json.load(f)
    else:
        records = []
    
    # 添加新记录
    record = {
        "record_id": f"{len(records) + 1}",
        "record_type": record_type,
        "timestamp": datetime.now().isoformat(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "indicators": indicators
    }
    
    records.append(record)
    
    # 保存
    with open(records_file, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    
    return record


def compare_health_data(user_id):
    """对比用户的健康数据变化"""
    user_dir = USERS_DIR / user_id
    records_file = user_dir / "health_records.json"
    
    if not records_file.exists():
        return {"has_history": False, "message": "暂无历史记录"}
    
    with open(records_file, encoding="utf-8") as f:
        records = json.load(f)
    
    if len(records) < 2:
        return {"has_history": False, "message": "历史记录不足，无法对比"}
    
    # 取最近两次记录对比
    latest = records[-1]
    previous = records[-2]
    
    # 对比指标
    changes = []
    for indicator, value in latest.get("indicators", {}).items():
        if indicator in previous.get("indicators", {}):
            old_value = previous["indicators"][indicator]
            if isinstance(value, (int, float)) and isinstance(old_value, (int, float)):
                diff = value - old_value
                percent_change = (diff / old_value * 100) if old_value != 0 else 0
                
                # 判断变化方向
                if abs(percent_change) > 5:  # 超过5%认为有变化
                    if diff < 0:
                        trend = "↓ 下降"
                        status = "改善" if indicator in ["ALT", "GGT", "总胆固醇", "甘油三酯", "血糖", "血压"] else "降低"
                    else:
                        trend = "↑ 上升"
                        status = "恶化" if indicator in ["ALT", "GGT", "总胆固醇", "甘油三酯", "血糖", "血压"] else "升高"
                    
                    changes.append({
                        "indicator": indicator,
                        "old_value": old_value,
                        "new_value": value,
                        "diff": round(diff, 2),
                        "percent": round(percent_change, 1),
                        "trend": trend,
                        "status": status
                    })
    
    # 构建对比报告
    report = {
        "has_history": True,
        "latest_record": {
            "date": latest["date"],
            "indicators": latest["indicators"]
        },
        "previous_record": {
            "date": previous["date"],
            "indicators": previous["indicators"]
        },
        "changes": changes,
        "summary": f"对比 {previous['date']} → {latest['date']}，共检测到 {len(changes)} 项变化"
    }
    
    return report


def should_update_plan(user_id):
    """判断是否需要更新运动计划"""
    comparison = compare_health_data(user_id)
    
    if not comparison.get("has_history"):
        return {"need_update": False, "reason": "暂无历史数据"}
    
    changes = comparison.get("changes", [])
    
    # 检查是否有重大变化
    significant_changes = []
    for change in changes:
        indicator = change["indicator"]
        percent = abs(change["percent"])
        
        # 关键指标变化超过10%需要关注
        key_indicators = ["ALT", "AST", "GGT", "总胆固醇", "甘油三酯", "空腹血糖", "血压"]
        
        if indicator in key_indicators and percent > 10:
            significant_changes.append(change)
    
    if significant_changes:
        return {
            "need_update": True,
            "reason": f"检测到 {len(significant_changes)} 项关键指标显著变化",
            "changes": significant_changes
        }
    
    return {"need_update": False, "reason": "指标变化在正常范围内"}


def auto_update_plan(user_id):
    """自动更新运动计划（当检测到显著变化时）"""
    from exercise_generator import generate_exercise_plan, load_user_health_data
    
    # 检查是否需要更新
    check_result = should_update_plan(user_id)
    
    if not check_result.get("need_update"):
        return {
            "success": True,
            "updated": False,
            "message": check_result.get("reason", "无需更新")
        }
    
    # 加载最新健康数据
    health_data = load_user_health_data(user_id)
    
    if not health_data or not health_data.get("abnormal"):
        return {"success": False, "message": "无健康数据，无法更新计划"}
    
    # 重新生成计划
    new_plan = generate_exercise_plan(user_id, health_data["abnormal"])
    
    return {
        "success": True,
        "updated": True,
        "message": "运动计划已根据最新体检数据自动更新",
        "changes": check_result.get("changes", []),
        "new_health_issues": new_plan["health_issues"],
        "new_plan": new_plan["weekly_plan"]
    }


if __name__ == "__main__":
    # 测试
    user_id = "test_user"
    
    # 模拟两次体检数据
    save_health_record(user_id, {
        "ALT": 58,
        "GGT": 65,
        "总胆固醇": 6.5,
        "体重": 70
    }, "体检1")
    
    save_health_record(user_id, {
        "ALT": 45,
        "GGT": 50,
        "总胆固醇": 5.8,
        "体重": 68
    }, "体检2")
    
    # 对比
    result = compare_health_data(user_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n" + "="*50)
    
    # 检查是否需要更新
    print(json.dumps(should_update_plan(user_id), ensure_ascii=False, indent=2))