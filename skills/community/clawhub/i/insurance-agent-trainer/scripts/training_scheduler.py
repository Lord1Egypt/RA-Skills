# Insurance Training Scheduler / 保险训练日程调度器

"""
根据代理人等级 + 当日行程 + 产品优先度，生成个性化每日训练计划
"""

import json
from datetime import datetime, time


# ============ 训练模块定义 ============

TRAINING_MODULES = {
    "quick_qa": {
        "name": "快问快答",
        "alias": "晨间快练",
        "duration_range": (10, 20),
        "best_time": [time(8, 0), time(12, 30), time(18, 0)],
        "mode": "问答",
        "best_for": "激活产品知识，热身用",
        "question_count_range": (5, 10)
    },
    "role_play": {
        "name": "情景对练",
        "alias": "实战演练",
        "duration_range": (20, 40),
        "best_time": [time(12, 30), time(17, 30)],
        "mode": "对话",
        "best_for": "异议处理、促成技巧实战",
        "question_count_range": (3, 5)
    },
    "case_study": {
        "name": "案例研讨",
        "alias": "深度分析",
        "duration_range": (30, 60),
        "best_time": [time(17, 30), time(19, 0)],
        "mode": "分析+讨论",
        "best_for": "高净值客户、复杂方案设计",
        "question_count_range": (1, 3)
    },
    "objection_focus": {
        "name": "异议攻关",
        "alias": "短板特训",
        "duration_range": (10, 20),
        "best_time": [time(12, 30)],
        "mode": "针对性练习",
        "best_for": "强化弱项",
        "question_count_range": (3, 5)
    },
    "assessment": {
        "name": "综合考核",
        "alias": "能力评估",
        "duration_range": (30, 60),
        "best_time": [time(14, 0)],
        "mode": "考试",
        "best_for": "晋升评估、阶段测试",
        "question_count_range": (20, 50)
    }
}

WEEKLY_THEMES = {
    "L1": ["产品基础知识", "销售开场", "需求挖掘基础", "异议处理入门", "促成技巧基础", "综合演练", "复盘总结"],
    "L2": ["产品知识巩固", "需求挖掘进阶", "异议处理强化", "竞品对比训练", "高净值客户", "综合实战", "数据分析能力"],
    "L3": ["高净值客户专题", "资产隔离与传承", "税务筹划联动", "竞品深度对比", "团队管理培训", "战略规划", "创新销售模式"]
}


# ============ 行程分析 ============

def analyze_daily_schedule(schedule: list[dict]) -> dict:
    """
    分析当日行程，识别产品训练需求
    schedule: [{"time": "09:00-10:00", "activity": "晨会", "location": "营业部"},
               {"time": "10:30-12:00", "activity": "拜访客户A（国企中层，有养老需求）", "location": "客户公司"}]
    """
    result = {
        "total_visits": 0,
        "products_needed": [],
        "client_needs": [],
        "travel_time_minutes": 0,
        "available_training_minutes": 0,
        "training_slots": []
    }

    known_keywords = {
        "养老": ["年金险", "终身寿险", "养老险"],
        "健康": ["医疗险", "重疾险", "防癌险"],
        "教育": ["教育金", "年金险"],
        "传承": ["终身寿险", "定额终身寿险", "保险金信托"],
        "医疗": ["医疗险", "重疾险"],
        "财富": ["万能险", "分红险", "投连险"],
        "企业": ["团体险", "财产险", "责任险"]
    }

    for item in schedule:
        activity = item.get("activity", "")
        # 识别拜访（排除晨会/夕会/培训等非客户拜访）
        if any(kw in activity for kw in ["拜访", "约见", "客户", "面谈"]):
            result["total_visits"] += 1
            # 识别产品需求关键词
            for kw, products in known_keywords.items():
                if kw in activity:
                    for p in products:
                        if p not in result["products_needed"]:
                            result["products_needed"].append(p)

    # 估算空闲训练时间
    # 假设：晨会1小时，午饭1小时，每个拜访平均1.5小时（含路程），其余为自由时间
    visit_hours = result["total_visits"] * 1.5
    fixed_hours = 2  # 晨会 + 午饭
    total_work_hours = 9  # 标准工作日9小时
    free_minutes = int((total_work_hours - visit_hours - fixed_hours) * 60)
    result["available_training_minutes"] = max(0, free_minutes)

    # 生成训练时间槽（优先匹配最佳时间）
    if result["available_training_minutes"] >= 20:
        result["training_slots"] = [
            {"time": "08:00-08:20", "minutes": 20, "recommended": "quick_qa"},
            {"time": "12:30-13:00", "minutes": 30, "recommended": "role_play"},
        ]
        if result["available_training_minutes"] >= 90:
            result["training_slots"].append(
                {"time": "17:30-18:30", "minutes": 60, "recommended": "case_study"}
            )

    return result


# ============ 训练计划生成 ============

def generate_daily_training_plan(
    agent_profile: dict,
    daily_schedule: list[dict],
    products: list[str],
    priority: str = "balanced"
) -> dict:
    """
    生成个性化每日训练计划

    Args:
        agent_profile: 代理人画像字典
        daily_schedule: 当日行程列表
        products: 当日拜访涉及的产品列表
        priority: "weakness" | "product" | "balanced"
    """
    level = agent_profile.get("skill_level", {}).get("current", "L2")
    weak_points = agent_profile.get("personalized_weak_points", [])
    name = agent_profile.get("basic_info", {}).get("name", "代理人")

    schedule_analysis = analyze_daily_schedule(daily_schedule)
    today_products = products if products else schedule_analysis["products_needed"]

    # 确定每周训练主题（简化版）
    weekday = datetime.now().weekday()
    weekly_themes = WEEKLY_THEMES.get(level, WEEKLY_THEMES["L2"])
    today_theme = weekly_themes[weekday] if weekday < len(weekly_themes) else "综合训练"

    sessions = []
    slots = schedule_analysis.get("training_slots", [])

    if priority == "weakness" and weak_points:
        # 以弱项为中心的训练安排
        for slot in slots:
            sessions.append({
                "time": slot["time"],
                "duration": slot["minutes"],
                "type": "objection_focus",
                "name": "异议攻关",
                "focus": weak_points[0] if weak_points else "产品知识",
                "product": today_products[0] if today_products else "通用",
                "mode": "针对性练习",
                "objective": f"强化弱项：{weak_points[0] if weak_points else '综合能力'}",
                "question_count": 5,
                "level": level
            })
    elif slots:
        # 综合训练安排（推荐）
        session_configs = [
            {"slot_idx": 0, "type": "quick_qa", "product": today_products[0] if today_products else "通用",
             "focus": "产品知识快问快答", "duration": 20},
            {"slot_idx": 1, "type": "role_play", "product": today_products[0] if today_products else "健康险",
             "focus": "情景对练", "duration": 30},
        ]
        if len(slots) >= 3:
            session_configs.append(
                {"slot_idx": 2, "type": "case_study", "product": today_products[-1] if today_products else "通用",
                 "focus": "案例分析", "duration": 40}
            )

        for cfg in session_configs:
            if cfg["slot_idx"] < len(slots):
                slot = slots[cfg["slot_idx"]]
                sessions.append({
                    "time": slot["time"],
                    "duration": cfg["duration"],
                    "type": cfg["type"],
                    "name": TRAINING_MODULES[cfg["type"]]["name"],
                    "product": cfg["product"],
                    "focus": cfg["focus"],
                    "mode": TRAINING_MODULES[cfg["type"]]["mode"],
                    "objective": f"今日训练主题：{today_theme}",
                    "level": level,
                    "coaching_tips": get_coaching_tips(cfg["type"], level)
                })

    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "agent": name,
        "level": level,
        "total_minutes": sum(s.get("duration", 0) for s in sessions),
        "weekly_theme": today_theme,
        "schedule_summary": {
            "total_visits": schedule_analysis["total_visits"],
            "products": today_products,
            "available_training_minutes": schedule_analysis["available_training_minutes"]
        },
        "sessions": sessions,
        "key_metrics_to_track": get_key_metrics(level)
    }


def get_coaching_tips(session_type: str, level: str) -> str:
    tips = {
        "quick_qa": "计时快答，结束后立即公布答案，错题自动进入错题本",
        "role_play": "AI扮演客户，代理人全程演练，AI实时点评",
        "case_study": "提供完整客户档案，代理人设计方案后AI给出优化建议",
        "objection_focus": "针对特定异议进行高强度重复练习，直到熟练",
        "assessment": "全真模拟考试，结束后生成详细能力报告"
    }
    return tips.get(session_type, "")


def get_key_metrics(level: str) -> list[dict]:
    base = [
        {"metric": "知识点正确率", "target": {"L1": "≥70%", "L2": "≥80%", "L3": "≥90%"}[level]},
        {"metric": "异议处理时效", "target": "<30秒"},
        {"metric": "话术合规率", "target": "100%"}
    ]
    if level in ["L2", "L3"]:
        base.append({"metric": "方案组合完整性", "target": "≥3单产品"})
    if level == "L3":
        base.append({"metric": "IRR计算准确率", "target": "100%"})
    return base


# ============ 输出格式化 ============

def format_training_plan_markdown(plan: dict) -> str:
    md = f"""# 📋 每日训练计划 — {plan['date']}

**代理人**: {plan['agent']}  |  **等级**: {plan['level']}  |  **本周主题**: {plan['weekly_theme']}
**总训练时长**: {plan['total_minutes']}分钟  |  **今日拜访**: {plan['schedule_summary']['total_visits']}个客户

## 今日产品重点
> {' / '.join(plan['schedule_summary']['products']) if plan['schedule_summary']['products'] else '通用训练'}

---

## 训练安排
"""
    for i, s in enumerate(plan["sessions"], 1):
        md += f"""
### Session {i} — {s['time']}（{s['duration']}分钟）

| 项目 | 内容 |
|------|------|
| **类型** | {s['name']} |
| **模式** | {s['mode']} |
| **产品** | {s['product']} |
| **重点** | {s['focus']} |
| **目标** | {s['objective']} |

**教练提示**: {s.get('coaching_tips', '')}
"""
    md += "\n## 📊 关键指标追踪\n\n| 指标 | 今日目标 |
|------|---------|\n"
    for m in plan["key_metrics_to_track"]:
        md += f"| {m['metric']} | {m['target']} |\n"
    return md


if __name__ == "__main__":
    sample_agent = {
        "basic_info": {"name": "张明"},
        "skill_level": {"current": "L2"},
        "personalized_weak_points": ["健康险异议处理（社保不够用算账）", "IRR计算"]
    }
    sample_schedule = [
        {"time": "09:00-09:30", "activity": "晨会", "location": "营业部"},
        {"time": "10:30-12:00", "activity": "拜访客户A（国企中层，有养老需求）", "location": "客户公司"},
        {"time": "14:00-15:30", "activity": "拜访客户B（私企业主，健康险需求）", "location": "客户公司"},
        {"time": "16:00-17:30", "activity": "缘故客户C（教育金规划）", "location": "咖啡厅"}
    ]

    plan = generate_daily_training_plan(sample_agent, sample_schedule, ["健康险", "年金险"])
    print(format_training_plan_markdown(plan))
