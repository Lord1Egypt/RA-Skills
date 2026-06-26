#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎯 Goal Manager v2.0 - 目标管理助手
功能：目标设定、SMART/OKR 框架、进度跟踪、复盘总结、目标分解
代码量：~13KB
"""

import json
import re
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(__file__).parent
GOALS_FILE = DATA_DIR / "goals.json"
REVIEWS_FILE = DATA_DIR / "reviews.json"

# ============================================================================
# 📋 目标模板库（SMART/OKR）
# ============================================================================
GOAL_TEMPLATES = {
    # 职业发展
    "职业晋升": {
        "category": "职业",
        "framework": "OKR",
        "objective": "晋升到高级工程师",
        "key_results": [
            {"desc": "完成 3 个重要项目", "target": 3, "unit": "个"},
            {"desc": "主导 1 个跨部门项目", "target": 1, "unit": "个"},
            {"desc": "获得 2 项专业认证", "target": 2, "unit": "项"},
            {"desc": "团队满意度达到 90%", "target": 90, "unit": "%"}
        ],
        "duration": "yearly",
        "tips": ["定期和上级沟通", "记录工作成果", "主动承担责任"]
    },
    "技能提升": {
        "category": "职业",
        "framework": "SMART",
        "goal": "学习 2 项新技能",
        "specific": "掌握 Python 数据分析和机器学习",
        "measurable": "完成 2 个实战项目，通过相关认证",
        "achievable": "每周学习 10 小时",
        "relevant": "提升职业竞争力",
        "time_bound": "2026 年 12 月前完成",
        "duration": "yearly",
        "tips": ["制定学习计划", "做项目实践", "找导师指导"]
    },
    "副业收入": {
        "category": "财务",
        "framework": "SMART",
        "goal": "建立月入 1 万的副业",
        "specific": "开发在线课程或咨询服务",
        "measurable": "月收入达到 10000 元",
        "achievable": "每周投入 15 小时",
        "relevant": "增加收入来源",
        "time_bound": "2026 年 6 月前实现",
        "duration": "half_year",
        "tips": ["找到擅长领域", "从小规模开始", "持续优化"]
    },
    
    # 健康生活
    "减肥塑形": {
        "category": "健康",
        "framework": "SMART",
        "goal": "减重 10 公斤",
        "specific": "从 75kg 减到 65kg",
        "measurable": "每周称重，每月测量体脂",
        "achievable": "每周运动 4 次，控制饮食",
        "relevant": "改善健康状况",
        "time_bound": "6 个月内完成",
        "duration": "half_year",
        "tips": ["记录饮食", "找运动伙伴", "保证睡眠"]
    },
    "健身增肌": {
        "category": "健康",
        "framework": "OKR",
        "objective": "塑造健康体态",
        "key_results": [
            {"desc": "体脂率降到 15%", "target": 15, "unit": "%"},
            {"desc": "卧推达到 80kg", "target": 80, "unit": "kg"},
            {"desc": "每周健身 4 次", "target": 4, "unit": "次/周"},
            {"desc": "蛋白质摄入 150g/天", "target": 150, "unit": "g/天"}
        ],
        "duration": "yearly",
        "tips": ["请私教指导", "记录训练日志", "合理饮食"]
    },
    "健康作息": {
        "category": "健康",
        "framework": "SMART",
        "goal": "建立健康作息",
        "specific": "23 点前睡觉，7 点起床，每天睡眠 8 小时",
        "measurable": "使用睡眠 APP 追踪",
        "achievable": "逐步调整，每周提前 15 分钟",
        "relevant": "改善精神状态",
        "time_bound": "3 个月内养成习惯",
        "duration": "quarter",
        "tips": ["睡前不玩手机", "固定起床时间", "午休 20 分钟"]
    },
    
    # 学习成长
    "阅读计划": {
        "category": "学习",
        "framework": "SMART",
        "goal": "阅读 24 本书",
        "specific": "每月阅读 2 本书（1 本专业 +1 本兴趣）",
        "measurable": "写读书笔记，每月复盘",
        "achievable": "每天阅读 30 分钟",
        "relevant": "拓展知识面",
        "time_bound": "2026 年全年",
        "duration": "yearly",
        "tips": ["随身带书", "参加读书会", "写书评"]
    },
    "英语学习": {
        "category": "学习",
        "framework": "OKR",
        "objective": "英语达到流利交流水平",
        "key_results": [
            {"desc": "托福/雅思达到 7 分", "target": 7, "unit": "分"},
            {"desc": "词汇量达到 8000", "target": 8000, "unit": "词"},
            {"desc": "每周口语练习 3 次", "target": 3, "unit": "次/周"},
            {"desc": "看 12 部英文电影", "target": 12, "unit": "部"}
        ],
        "duration": "yearly",
        "tips": ["沉浸式学习", "找语伴练习", "每天背单词"]
    },
    "写作输出": {
        "category": "学习",
        "framework": "SMART",
        "goal": "建立个人品牌",
        "specific": "在公众号/知乎等平台持续输出",
        "measurable": "每周发布 2 篇文章，粉丝达到 5000",
        "achievable": "每天写作 1 小时",
        "relevant": "提升影响力",
        "time_bound": "2026 年 12 月前",
        "duration": "yearly",
        "tips": ["找到定位", "保持更新", "与读者互动"]
    },
    
    # 财务管理
    "储蓄目标": {
        "category": "财务",
        "framework": "SMART",
        "goal": "存款达到 20 万",
        "specific": "每月储蓄 1 万元",
        "measurable": "每月检查账户余额",
        "achievable": "控制开支，增加收入",
        "relevant": "为未来做准备",
        "time_bound": "2026 年 12 月前",
        "duration": "yearly",
        "tips": ["自动转账", "记账复盘", "学习理财"]
    },
    "投资理财": {
        "category": "财务",
        "framework": "OKR",
        "objective": "建立稳健投资组合",
        "key_results": [
            {"desc": "年化收益率达到 8%", "target": 8, "unit": "%"},
            {"desc": "学习 3 种投资方式", "target": 3, "unit": "种"},
            {"desc": "建立应急基金 6 个月", "target": 6, "unit": "月"},
            {"desc": "每月定投 5000 元", "target": 5000, "unit": "元"}
        ],
        "duration": "yearly",
        "tips": ["学习基础知识", "分散投资", "长期持有"]
    },
    
    # 人际关系
    "拓展人脉": {
        "category": "社交",
        "framework": "SMART",
        "goal": "拓展高质量人脉",
        "specific": "参加行业活动，认识同行精英",
        "measurable": "每月参加 2 次活动，添加 50 个有效联系人",
        "achievable": "主动交流，提供价值",
        "relevant": "职业发展需要",
        "time_bound": "2026 年全年",
        "duration": "yearly",
        "tips": ["准备自我介绍", "主动跟进", "维护关系"]
    },
    "陪伴家人": {
        "category": "生活",
        "framework": "SMART",
        "goal": "增加陪伴家人时间",
        "specific": "每周至少 1 天完全陪家人",
        "measurable": "记录陪伴时间，每月至少 4 天",
        "achievable": "提前安排工作，放下手机",
        "relevant": "家庭幸福重要",
        "time_bound": "2026 年全年",
        "duration": "yearly",
        "tips": ["质量重于数量", "创造仪式感", "用心倾听"]
    },
    
    # 旅行体验
    "旅行计划": {
        "category": "生活",
        "framework": "SMART",
        "goal": "旅行 3 个城市",
        "specific": "国内 2 个 + 国外 1 个",
        "measurable": "完成旅行并写游记",
        "achievable": "利用假期，提前规划",
        "relevant": "开阔眼界",
        "time_bound": "2026 年 12 月前",
        "duration": "yearly",
        "tips": ["提前订票", "做攻略", "记录美好"]
    }
}

# ============================================================================
# 📝 复盘模板库
# ============================================================================
REVIEW_TEMPLATES = {
    "daily": {
        "title": "每日复盘",
        "questions": [
            "今天完成了哪 3 件最重要的事？",
            "今天有什么收获或进步？",
            "今天遇到了什么困难？如何解决的？",
            "今天有什么可以改进的地方？",
            "明天的 3 个重点是什么？"
        ]
    },
    "weekly": {
        "title": "周复盘",
        "questions": [
            "本周完成了哪些目标？",
            "本周最大的收获是什么？",
            "本周有什么遗憾或未完成的事？",
            "本周时间分配合理吗？",
            "下周的 3 个重点目标是什么？"
        ]
    },
    "monthly": {
        "title": "月度复盘",
        "sections": [
            "✅ 完成的目标",
            "⏳ 进行中的目标",
            "❌ 未完成的目标及原因",
            "💡 经验教训",
            "🎯 下月目标"
        ]
    },
    "quarterly": {
        "title": "季度复盘",
        "sections": [
            "📊 季度目标完成度",
            "🏆 最大成就",
            "⚠️ 主要挑战",
            "📈 成长与进步",
            "🎯 下季度规划"
        ]
    },
    "yearly": {
        "title": "年度复盘",
        "sections": [
            "🎯 年度目标回顾",
            "🏆 年度高光时刻",
            "📚 学到的最重要的一课",
            "💰 财务状况总结",
            "❤️ 健康与关系",
            "🚀 新年愿景"
        ]
    }
}

# ============================================================================
# 📊 进度追踪
# ============================================================================
def load_data():
    """加载数据"""
    if GOALS_FILE.exists():
        with open(GOALS_FILE, "r", encoding="utf-8") as f:
            goals_data = json.load(f)
    else:
        goals_data = {"yearly_goals": [], "monthly_goals": [], "quarterly_goals": []}
    
    if REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, "r", encoding="utf-8") as f:
            reviews_data = json.load(f)
    else:
        reviews_data = {"reviews": []}
    
    return goals_data, reviews_data


def save_goals(data):
    """保存目标数据"""
    with open(GOALS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_reviews(data):
    """保存复盘数据"""
    with open(REVIEWS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_goal(template_name, custom_krs=None):
    """从模板创建目标"""
    goals_data, reviews_data = load_data()
    
    if template_name not in GOAL_TEMPLATES:
        return {"error": "未找到该模板"}
    
    template = GOAL_TEMPLATES[template_name]
    now = datetime.now()
    
    # 计算截止日期
    duration = template.get("duration", "yearly")
    if duration == "yearly":
        end_date = now.replace(year=now.year + 1)
    elif duration == "half_year":
        end_date = now + timedelta(days=180)
    elif duration == "quarter":
        end_date = now + timedelta(days=90)
    else:
        end_date = now + timedelta(days=365)
    
    goal = {
        "id": f"goal_{now.strftime('%Y%m%d%H%M%S')}",
        "name": template_name,
        "category": template["category"],
        "framework": template["framework"],
        "created_date": now.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "status": "active",
        "progress": 0,
        "template": template,
        "checkpoints": [],
        "notes": []
    }
    
    # OKR 框架
    if template["framework"] == "OKR":
        goal["objective"] = template["objective"]
        goal["key_results"] = []
        for kr in template.get("key_results", []):
            goal["key_results"].append({
                "desc": kr["desc"],
                "target": kr["target"],
                "current": 0,
                "unit": kr["unit"],
                "progress": 0
            })
    
    # SMART 框架
    elif template["framework"] == "SMART":
        goal["goal"] = template["goal"]
        goal["smart"] = {
            "specific": template.get("specific", ""),
            "measurable": template.get("measurable", ""),
            "achievable": template.get("achievable", ""),
            "relevant": template.get("relevant", ""),
            "time_bound": template.get("time_bound", "")
        }
    
    # 确定存储位置
    if duration == "yearly":
        goals_data["yearly_goals"].append(goal)
    elif duration == "quarter":
        goals_data["quarterly_goals"].append(goal)
    else:
        goals_data["monthly_goals"].append(goal)
    
    save_goals(goals_data)
    
    return goal


def update_progress(goal_name, kr_index=None, value=None):
    """更新进度"""
    goals_data, _ = load_data()
    
    for goal_list in ["yearly_goals", "quarterly_goals", "monthly_goals"]:
        for goal in goals_data.get(goal_list, []):
            if goal_name in goal.get("name", "") or goal_name in goal.get("objective", ""):
                if goal["framework"] == "OKR" and kr_index is not None and value is not None:
                    # 更新 KR 进度
                    if kr_index < len(goal["key_results"]):
                        kr = goal["key_results"][kr_index]
                        kr["current"] = value
                        kr["progress"] = min(100, round(value / kr["target"] * 100, 1))
                
                # 计算总体进度
                if goal["framework"] == "OKR":
                    total_progress = sum(kr["progress"] for kr in goal["key_results"])
                    goal["progress"] = round(total_progress / len(goal["key_results"]), 1) if goal["key_results"] else 0
                
                # 添加检查点
                goal["checkpoints"].append({
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "progress": goal["progress"],
                    "note": f"更新进度：{goal['progress']}%"
                })
                
                save_goals(goals_data)
                return goal
    
    return {"error": "未找到该目标"}


def format_goal(goal):
    """格式化目标输出"""
    response = f"🎯 **{goal['name']}**\n\n"
    response += f"📂 分类：{goal['category']}\n"
    response += f"📐 框架：{goal['framework']}\n"
    response += f"📅 创建：{goal['created_date']}\n"
    response += f"🎯 截止：{goal['end_date']}\n"
    response += f"📊 进度：{goal['progress']}%\n\n"
    
    if goal["framework"] == "OKR":
        response += f"**O: {goal.get('objective', '')}**\n\n"
        for i, kr in enumerate(goal.get("key_results", []), 1):
            bar_len = int(kr["progress"] / 10)
            bar = "█" * bar_len + "░" * (10 - bar_len)
            response += f"**KR{i}**: {kr['desc']}\n"
            response += f"  进度：[{bar}] {kr['current']}/{kr['target']} {kr['unit']} ({kr['progress']}%)\n\n"
    
    elif goal["framework"] == "SMART":
        smart = goal.get("smart", {})
        response += f"**目标**: {goal.get('goal', '')}\n\n"
        response += f"- **S** (具体): {smart.get('specific', '')}\n"
        response += f"- **M** (可衡量): {smart.get('measurable', '')}\n"
        response += f"- **A** (可实现): {smart.get('achievable', '')}\n"
        response += f"- **R** (相关): {smart.get('relevant', '')}\n"
        response += f"- **T** (时限): {smart.get('time_bound', '')}\n"
    
    tips = goal.get("template", {}).get("tips", [])
    if tips:
        response += f"\n💡 **建议**: {', '.join(tips[:3])}"
    
    return response


def generate_review(period="monthly"):
    """生成复盘报告"""
    template = REVIEW_TEMPLATES.get(period, REVIEW_TEMPLATES["monthly"])
    now = datetime.now()
    
    response = f"📋 **{template['title']}**\n"
    response += f"日期：{now.strftime('%Y-%m-%d')}\n\n"
    response += "---\n\n"
    
    if "questions" in template:
        for i, q in enumerate(template["questions"], 1):
            response += f"{i}. {q}\n   \n"
    elif "sections" in template:
        for section in template["sections"]:
            response += f"{section}\n\n"
    
    response += "\n---\n\n"
    response += "💭 **自由记录**:\n\n\n\n"
    response += "🎯 **下次复盘日期**: "
    
    if period == "daily":
        next_date = now + timedelta(days=1)
    elif period == "weekly":
        next_date = now + timedelta(days=7)
    elif period == "monthly":
        next_date = now.replace(day=1) + timedelta(days=32)
        next_date = next_date.replace(day=1)
    else:
        next_date = now + timedelta(days=90)
    
    response += next_date.strftime("%Y-%m-%d")
    
    return response


def get_goal_templates():
    """获取目标模板列表"""
    response = "📋 **目标模板库**\n\n"
    
    categories = {}
    for name, tmpl in GOAL_TEMPLATES.items():
        cat = tmpl["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((name, tmpl))
    
    for cat, templates in sorted(categories.items()):
        response += f"**{cat}**\n"
        for name, tmpl in templates:
            fw = tmpl["framework"]
            if fw == "OKR":
                desc = tmpl.get("objective", "")
            else:
                desc = tmpl.get("goal", "")
            response += f"- {name} ({fw}): {desc}\n"
        response += "\n"
    
    return response


def get_all_goals():
    """获取所有目标"""
    goals_data, _ = load_data()
    
    response = "🎯 **我的目标**\n\n"
    
    for goal_list, title in [
        ("yearly_goals", "年度目标"),
        ("quarterly_goals", "季度目标"),
        ("monthly_goals", "月度目标")
    ]:
        goals = goals_data.get(goal_list, [])
        if goals:
            response += f"**{title}**\n"
            for goal in goals:
                status_icon = "✅" if goal["progress"] >= 100 else "🔄" if goal["progress"] > 0 else "⏳"
                response += f"{status_icon} **{goal['name']}**: {goal['progress']}%\n"
            response += "\n"
    
    if not any(goals_data.get(gl, []) for gl in ["yearly_goals", "quarterly_goals", "monthly_goals"]):
        response += "暂无目标，创建一个吧！\n"
    
    return response


# ============================================================================
# 🎯 主函数
# ============================================================================
def main(query):
    """主函数"""
    query_lower = query.lower()
    
    # 显示模板
    if "模板" in query_lower or "有哪些目标" in query_lower:
        return get_goal_templates()
    
    # 创建目标
    if "创建" in query_lower or "设定" in query_lower or "目标" in query_lower:
        for template_name in GOAL_TEMPLATES.keys():
            if template_name in query_lower:
                goal = create_goal(template_name)
                if goal.get("error"):
                    return f"❌ {goal['error']}"
                return f"✅ 目标已创建！\n\n" + format_goal(goal)
        
        return "📋 请选择一个目标模板：\n\n" + get_goal_templates()
    
    # 查看目标
    if "查看" in query_lower or "我的目标" in query_lower:
        return get_all_goals()
    
    # 更新进度
    if "更新" in query_lower or "进度" in query_lower:
        # 解析：更新减肥目标 KR1 为 5
        match = re.search(r'更新 (.+?) (?:KR|kr)?(\d+)? 为 (\d+)', query_lower)
        if match:
            goal_name = match.group(1)
            kr_index = int(match.group(2)) - 1 if match.group(2) else 0
            value = int(match.group(3))
            
            goal = update_progress(goal_name, kr_index, value)
            if goal.get("error"):
                return f"❌ {goal['error']}"
            return f"✅ 进度已更新！\n\n" + format_goal(goal)
        
        return "💡 用法：更新 [目标名] KR[编号] 为 [数值]\n例如：更新减肥塑形 KR1 为 5"
    
    # 复盘
    if "复盘" in query_lower or "总结" in query_lower or "反思" in query_lower:
        period = "monthly"
        if "日" in query_lower: period = "daily"
        elif "周" in query_lower: period = "weekly"
        elif "季" in query_lower: period = "quarterly"
        elif "年" in query_lower: period = "yearly"
        
        return generate_review(period)
    
    # 删除目标
    if "删除" in query_lower or "取消" in query_lower:
        goals_data, _ = load_data()
        deleted = False
        
        for goal_list in ["yearly_goals", "quarterly_goals", "monthly_goals"]:
            goals_data[goal_list] = [
                g for g in goals_data.get(goal_list, [])
                if not any(name in g.get("name", "") for name in GOAL_TEMPLATES.keys() if name in query_lower)
            ]
        
        save_goals(goals_data)
        return "✅ 目标已删除（如有）"
    
    # 默认回复
    return """🎯 目标管理助手 v2.0

**功能**：
1. 创建目标 - "创建阅读计划目标"、"设定减肥塑形目标"
2. 查看目标 - "查看我的目标"
3. 更新进度 - "更新减肥塑形 KR1 为 5"
4. 复盘总结 - "做月度复盘"、"写周复盘"
5. 模板库 - "有哪些目标模板"

**目标框架**：
- **OKR**: 目标 + 关键结果（适合量化目标）
- **SMART**: 具体、可衡量、可实现、相关、时限

**目标分类**：
- 职业：职业晋升、技能提升、副业收入
- 健康：减肥塑形、健身增肌、健康作息
- 学习：阅读计划、英语学习、写作输出
- 财务：储蓄目标、投资理财
- 社交：拓展人脉
- 生活：陪伴家人、旅行计划

**复盘模板**：日报、周报、月报、季报、年报

告诉我你想设定什么目标？👻"""


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print(main("创建阅读计划目标"))
