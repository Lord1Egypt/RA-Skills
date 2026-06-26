#!/usr/bin/env python3
"""
运动计划生成器
根据用户异常指标，自动生成个性化运动方案
"""

import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
PLANS_DIR = BASE_DIR / "data" / "plans"
PLANS_DIR.mkdir(parents=True, exist_ok=True)


# 异常指标 → 运动方案映射
EXERCISE_MAPPING = {
    "ALT偏高": {
        "推荐运动": ["八段锦", "太极拳", "慢走", "游泳"],
        "目的": "养肝调理，促进代谢",
        "注意事项": "避免剧烈运动，以温和有氧为主"
    },
    "GGT偏高": {
        "推荐运动": ["八段锦", "太极", "散步"],
        "目的": "护肝降酶",
        "注意事项": "戒酒，规律作息"
    },
    "总胆固醇高": {
        "推荐运动": ["快走", "骑行", "游泳", "跳绳"],
        "目的": "降血脂",
        "注意事项": "每周至少3次，每次30分钟以上"
    },
    "甘油三酯高": {
        "推荐运动": ["有氧运动", "跑步", "游泳"],
        "目的": "降低甘油三酯",
        "注意事项": "配合饮食控制"
    },
    "LDL高": {
        "推荐运动": ["快走", "骑行", "登山"],
        "目的": "降低低密度脂蛋白",
        "注意事项": "坚持规律运动"
    },
    "HDL低": {
        "推荐运动": ["游泳", "骑行", "快走"],
        "目的": "升高高密度脂蛋白",
        "注意事项": "运动强度适中"
    },
    "血糖高": {
        "推荐运动": ["餐后散步", "力量训练", "太极"],
        "目的": "控制血糖",
        "注意事项": "餐后30分钟开始运动"
    },
    "血压高": {
        "推荐运动": ["太极拳", "散步", "瑜伽", "冥想"],
        "目的": "降血压",
        "注意事项": "避免剧烈运动"
    },
    "尿酸高": {
        "推荐运动": ["游泳", "骑行", "散步"],
        "目的": "促进尿酸排泄",
        "注意事项": "避免剧烈运动，多喝水"
    },
    "肩颈问题": {
        "推荐运动": ["肩颈拉伸", "瑜伽", "游泳"],
        "目的": "舒缓肩颈",
        "注意事项": "每工作1小时活动5分钟"
    },
    "腰椎问题": {
        "推荐运动": ["腰椎养护操", "游泳", "小燕飞"],
        "目的": "保护腰椎",
        "注意事项": "避免久坐和弯腰"
    },
    "肥胖": {
        "推荐运动": ["有氧+力量", "跑步", "骑行", "跳绳"],
        "目的": "减脂",
        "注意事项": "循序渐进，控制饮食"
    },
    "失眠": {
        "推荐运动": ["太极", "睡前拉伸", "散步"],
        "目的": "改善睡眠",
        "注意事项": "睡前2小时完成运动"
    }
}


# 约束条件
USER_CONSTRAINTS = {
    "不能长时间剧烈运动": {
        "运动时长": "每次30分钟左右",
        "运动强度": "温和为主"
    },
    "腰和肩颈不太好": {
        "避免": "跑跳、剧烈拉伸",
        "推荐": "太极、八段锦、游泳"
    }
}


def analyze_health_issues(abnormal_list):
    """分析用户的健康问题"""
    issues = []
    for item in abnormal_list:
        indicator = item["indicator"]
        if indicator in ["ALT", "AST", "GGT"]:
            issues.append(f"{indicator}偏高")
        elif indicator == "总胆固醇" and item["status"] == "偏高":
            issues.append("总胆固醇高")
        elif indicator == "甘油三酯" and item["status"] == "偏高":
            issues.append("甘油三酯高")
        elif indicator == "LDL" and item["status"] == "偏高":
            issues.append("LDL高")
        elif indicator == "HDL" and item["status"] == "偏低":
            issues.append("HDL低")
        elif indicator == "空腹血糖" and item["status"] == "偏高":
            issues.append("血糖高")
        elif indicator in ["收缩压", "舒张压"] and item["status"] == "偏高":
            issues.append("血压高")
        elif indicator == "尿酸" and item["status"] == "偏高":
            issues.append("尿酸高")
    return issues


def generate_weekly_plan(health_issues, constraints=None):
    """生成周一到周日的运动计划"""
    
    # 收集所有推荐运动
    all_recommended = []
    for issue in health_issues:
        if issue in EXERCISE_MAPPING:
            all_recommended.extend(EXERCISE_MAPPING[issue]["推荐运动"])
    
    # 去重
    all_recommended = list(set(all_recommended))
    
    # 默认运动（适合所有人的温和运动）
    default_morning = ["八段锦", "太极", "全身拉伸"]
    default_afternoon = ["散步", "慢走", "骑行"]
    
    # 合并
    morning_exercises = list(set(all_recommended + default_morning))
    afternoon_exercises = default_afternoon
    
    # 生成周计划（周一到周五为主，周六周日灵活）
    # 工作日：固定计划 | 周末：灵活安排
    weekly_plan = {}
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for i, day in enumerate(days):
        # 早上：选一个主要运动
        if i % 3 == 0:  # 每3天轮换一次
            morning = "八段锦"
        elif i % 3 == 1:
            morning = "太极"
        else:
            morning = "全身拉伸"
        
        # 下午/晚上
        if i == 2 or i == 6:  # 周三、周日休息
            afternoon = "休息"
            afternoon_duration = "0"
        elif i == 5:  # 周六可以多运动
            afternoon = "徒步/爬山"
            afternoon_duration = "60"
        else:
            afternoon = "散步"
            afternoon_duration = "30"
        
        weekly_plan[day] = {
            "早上": {
                "运动": morning,
                "时长": "30分钟",
                "目的": get_exercise_purpose(morning, health_issues)
            },
            "下午": {
                "运动": afternoon,
                "时长": f"{afternoon_duration}分钟",
                "目的": "有氧锻炼" if afternoon != "休息" else "身体恢复"
            }
        }
    
    return weekly_plan


def get_exercise_purpose(exercise, health_issues):
    """获取运动目的"""
    purposes = {
        "八段锦": "养肝调理，舒筋活络",
        "太极": "调和气血，舒缓身心",
        "全身拉伸": "放松肌肉，缓解疲劳",
        "肩颈拉伸": "舒缓肩颈",
        "腰椎养护操": "保护腰椎",
        "散步": "温和有氧",
        "慢走": "活血放松",
        "骑行": "有氧锻炼",
        "游泳": "全身运动，保护关节"
    }
    return purposes.get(exercise, "身体健康")


def generate_exercise_plan(user_id, abnormal_list, constraints=None):
    """为用户生成完整的运动计划"""
    
    # 分析健康问题
    health_issues = analyze_health_issues(abnormal_list)
    
    # 添加默认的身体限制
    if not health_issues:
        health_issues = ["身体健康维持"]  # 默认
    
    # 生成周计划
    weekly_plan = generate_weekly_plan(health_issues, constraints)
    
    # 构建完整计划
    plan = {
        "user_id": user_id,
        "health_issues": health_issues,
        "constraints": constraints or ["不能长时间剧烈运动", "腰和肩颈不太好"],
        "weekly_plan": weekly_plan,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 保存
    plan_file = PLANS_DIR / f"{user_id}_plan.json"
    with open(plan_file, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    return plan


def load_user_plan(user_id):
    """加载用户的运动计划"""
    plan_file = PLANS_DIR / f"{user_id}_plan.json"
    if plan_file.exists():
        with open(plan_file, encoding="utf-8") as f:
            return json.load(f)
    return None


def get_today_plan(user_id):
    """获取今天的运动计划"""
    import datetime
    plan = load_user_plan(user_id)
    if not plan:
        return None
    
    # 获取今天周几
    weekday = datetime.datetime.now().weekday()
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    today = days[weekday]
    
    return {
        "day": today,
        "plan": plan["weekly_plan"].get(today)
    }


if __name__ == "__main__":
    # 测试
    test_abnormal = [
        {"indicator": "ALT", "value": 58, "status": "偏高"},
        {"indicator": "GGT", "value": 65, "status": "偏高"}
    ]
    
    plan = generate_exercise_plan("test_user", test_abnormal)
    print(json.dumps(plan, ensure_ascii=False, indent=2))