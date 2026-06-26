#!/usr/bin/env python3
"""
推进建议生成脚本
根据客户状态生成下一步行动建议
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# 阶段定义
STAGES = {
    1: "需求识别（首次接触，了解需求）",
    2: "房源匹配（提供方案，带看房源）",
    3: "方案对比（客户对比竞品，TCO分析）",
    4: "谈判（讨论条款，谈判租金/租期）",
    5: "决策（内部决策，审批流程）",
    6: "签约（签约成交，入驻准备）",
}

# 决策人类型话术库
DECISION_MAKER_TALK = {
    "CEO": {
        "focus": ["战略发展", "产业生态", "品牌形象", "长期规划"],
        "talk_points": ["园区产业集聚效应", "未来发展规划", "高端商务配套", "企业形象提升"],
        "suggested_actions": ["邀请参加园区高管活动", "安排与园区领导会面", "提供定制化产业服务方案"],
    },
    "COO": {
        "focus": ["成本控制", "运营效率", "配套服务", "员工满意度"],
        "talk_points": ["TCO成本优势", "一站式企业服务", "人才公寓配套", "员工餐饮配套"],
        "suggested_actions": ["安排运营团队参观", "提供详细成本对比表", "安排与已入驻企业COO交流"],
    },
    "CFO": {
        "focus": ["财务风险", "税务筹划", "现金流", "政策补贴"],
        "talk_points": ["租金含税票", "税收返还政策", "人才补贴申报", "财务成本优化"],
        "suggested_actions": ["提供税务筹划方案", "安排与财务部门对接", "详细解读政策申报流程"],
    },
    "CTO": {
        "focus": ["技术设施", "网络环境", "电力负荷", "研发配套"],
        "talk_points": ["双路供电系统", "万兆光纤入户", "层高承重参数", "共享实验室"],
        "suggested_actions": ["安排技术团队实地考察", "提供详细技术参数", "安排与园区技术团队对接"],
    },
}

# 风险提示库
RISK_SIGNALS = {
    "response_slow": "回复周期变长（>3天）",
    "no_question": "不再提问细节",
    "compare_only": "只谈竞品，不谈自身需求",
    "price_only": "只谈价格，不谈其他",
    "internal_silent": "不再提及内部决策进展",
}

def generate_progress_advice(customer_name, stage, duration_days, decision_maker, interaction_history=None):
    """生成推进建议"""
    # 1. 评估紧急程度
    urgency = evaluate_urgency(stage, duration_days)
    
    # 2. 生成下一步行动建议
    next_actions = generate_next_actions(stage, duration_days, decision_maker)
    
    # 3. 生成话术建议
    talk_suggestions = generate_talk_suggestions(decision_maker)
    
    # 4. 标识关键时间节点
    key_dates = identify_key_dates(stage, datetime.now())
    
    # 5. 风险提示
    risk_warnings = generate_risk_warnings(interaction_history)
    
    return {
        "customer_name": customer_name,
        "urgency": urgency,
        "next_actions": next_actions,
        "talk_suggestions": talk_suggestions,
        "key_dates": key_dates,
        "risk_warnings": risk_warnings,
        "stage": stage,
        "duration_days": duration_days,
    }

def evaluate_urgency(stage, duration_days):
    """评估紧急程度"""
    # 各阶段建议停留时间
    suggested_days = {
        1: 7,   # 需求识别：7天内应进入房源匹配
        2: 7,   # 房源匹配：7天内应带看
        3: 7,   # 方案对比：7天内应进入谈判
        4: 14,  # 谈判：14天内应进入决策
        5: 14,  # 决策：14天内应签约
        6: 7,   # 签约：7天内应完成
    }
    
    suggested = suggested_days.get(stage, 7)
    
    if duration_days <= suggested:
        return "🔵 正常"
    elif duration_days <= suggested * 2:
        return "🟡 重要"
    else:
        return "🔴 紧急"

def generate_next_actions(stage, duration_days, decision_maker):
    """生成下一步行动建议"""
    actions = {"today": [], "tomorrow": [], "this_week": []}
    
    if stage == 1:  # 需求识别
        actions["today"] = ["发送园区详细介绍资料", "预约电话沟通（确认需求细节）"]
        actions["tomorrow"] = ["电话沟通（30分钟）", "记录需求清单"]
        actions["this_week"] = ["安排第一次带看", "准备3套房源方案"]
    
    elif stage == 2:  # 房源匹配
        if duration_days > 7:
            actions["today"] = ["🟡 紧急：电话跟进（了解决策进展）", "发送客户见证视频"]
            actions["tomorrow"] = ["🟡 安排第二次带看（不同户型）", "准备TCO成本分析"]
            actions["this_week"] = ["🟡 邀请参加园区活动", "提供限时优惠（迫使其决策）"]
        else:
            actions["today"] = ["确认带看时间", "准备带看材料"]
            actions["tomorrow"] = ["执行带看", "当晚发送带看总结"]
            actions["this_week"] = ["发送正式报价方案", "跟进反馈"]
    
    elif stage == 3:  # 方案对比
        if duration_days > 7:
            actions["today"] = ["🔴 紧急：发送TCO全成本对比报告", "强调我方优势（产业生态+政策支持）"]
            actions["tomorrow"] = ["🔴 预约第二次带看（看高区景观房源）", "准备竞品对比分析"]
            actions["this_week"] = ["🔴 邀请决策人午餐会", "提供限时优惠（免租期延长）"]
        else:
            actions["today"] = ["发送TCO成本对比报告", "回答客户对比疑问"]
            actions["tomorrow"] = ["预约第二次带看", "准备谈判要点"]
            actions["this_week"] = ["跟进决策进展", "提供补充材料"]
    
    elif stage == 4:  # 谈判
        actions["today"] = ["准备谈判要点（租金底线/租期/免租期）", "预约谈判会议"]
        actions["tomorrow"] = ["执行谈判", "记录谈判结果和分歧点"]
        actions["this_week"] = ["根据谈判结果调整方案", "准备签约文件"]
    
    elif stage == 5:  # 决策
        actions["today"] = ["跟进内部决策进展", "提供补充材料（如需）"]
        actions["tomorrow"] = ["了解决策时间表", "准备签约文件"]
        actions["this_week"] = ["确认签约时间", "安排入驻前准备"]
    
    elif stage == 6:  # 签约
        actions["today"] = ["准备签约文件", "确认入驻时间"]
        actions["tomorrow"] = ["执行签约", "安排入驻事宜"]
        actions["this_week"] = ["完成入驻手续", "后续服务跟进"]
    
    # 根据决策人类型调整行动建议
    if decision_maker in DECISION_MAKER_TALK:
        actions["this_week"].extend(DECISION_MAKER_TALK[decision_maker]["suggested_actions"][:1])
    
    return actions

def generate_talk_suggestions(decision_maker):
    """生成话术建议"""
    if decision_maker not in DECISION_MAKER_TALK:
        return {
            "focus": ["成本", "位置", "配套", "服务"],
            "talk_points": ["TCO成本优势", "区位交通便利", "园区配套齐全", "一站式服务"],
            "tips": ["多用数据说话", "提供成功案例", "强调稀缺性"],
        }
    
    return DECISION_MAKER_TALK[decision_maker]

def identify_key_dates(stage, from_date):
    """标识关键时间节点"""
    key_dates = []
    
    if stage <= 2:
        # 需求识别和房源匹配阶段
        key_dates.append(("带看后24小时", from_date + timedelta(days=1), "发送带看总结+跟进邮件"))
        key_dates.append(("带看后3天", from_date + timedelta(days=3), "电话跟进（了解决策进展）"))
        key_dates.append(("带看后7天", from_date + timedelta(days=7), "第二次跟进（提供补充材料）"))
    
    elif stage == 3:
        # 方案对比阶段
        key_dates.append(("方案发送后24小时", from_date + timedelta(days=1), "电话沟通（解答疑问）"))
        key_dates.append(("方案发送后3天", from_date + timedelta(days=3), "发送TCO对比报告"))
        key_dates.append(("方案发送后7天", from_date + timedelta(days=7), "邀请再次带看或谈判"))
    
    elif stage >= 4:
        # 谈判及以后阶段
        key_dates.append(("谈判后24小时", from_date + timedelta(days=1), "发送谈判总结+调整后的方案"))
        key_dates.append(("谈判后3天", from_date + timedelta(days=3), "电话跟进（了解决策进展）"))
        key_dates.append(("谈判后7天", from_date + timedelta(days=7), "最后通牒（限时优惠到期）"))
    
    return key_dates

def generate_risk_warnings(interaction_history):
    """生成风险提示"""
    warnings = []
    
    if not interaction_history:
        warnings.append("⚠️ 无互动记录，无法评估风险")
        return warnings
    
    # 模拟风险识别逻辑
    recent_interactions = interaction_history[-3:] if len(interaction_history) >= 3 else interaction_history
    
    # 检查回复周期
    # 这里应该实际分析互动记录，现在只是模拟
    warnings.append("⚠️ 风险提示：需要实际互动记录来分析")
    warnings.append("💡 建议：每次沟通后记录关键信息（客户反馈/顾虑/决策进展）")
    
    return warnings

def format_progress_advice(advice):
    """格式化推进建议"""
    output = f"# 📈 客户推进建议 - {advice['customer_name']}\n\n"
    
    output += f"## 🚨 紧急程度评估\n"
    output += f"**当前状态**：{advice['urgency']}\n\n"
    
    output += f"## 📋 下一步行动建议\n\n"
    output += f"### 今日行动（{datetime.now().strftime('%Y-%m-%d')}）\n"
    for action in advice['next_actions']['today']:
        output += f"- {action}\n"
    output += "\n"
    
    output += f"### 明日行动（{(datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')}）\n"
    for action in advice['next_actions']['tomorrow']:
        output += f"- {action}\n"
    output += "\n"
    
    output += f"### 本周行动（未来7天）\n"
    for action in advice['next_actions']['this_week']:
        output += f"- {action}\n"
    output += "\n"
    
    output += f"## 💬 话术建议（针对{advice['talk_suggestions']['focus'][0]}）\n"
    output += f"**关注重点**：{', '.join(advice['talk_suggestions']['focus'])}\n\n"
    output += f"**谈话要点**：\n"
    for point in advice['talk_suggestions']['talk_points']:
        output += f"- {point}\n"
    output += "\n"
    output += f"**沟通技巧**：\n"
    output += f"- 多用数据说话（成本对比/政策收益）\n"
    output += f"- 提供成功案例（同行业企业）\n"
    output += f"- 强调稀缺性（好房源不等人）\n\n"
    
    output += f"## 📅 关键时间节点\n"
    for date_name, date_value, action in advice['key_dates']:
        output += f"- **{date_name}**（{date_value.strftime('%Y-%m-%d')}）：{action}\n"
    output += "\n"
    
    output += f"## ⚠️ 风险提示\n"
    for warning in advice['risk_warnings']:
        output += f"- {warning}\n"
    output += "\n"
    
    output += f"---\n"
    output += f"*本推进建议由招商助手自动生成 @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    
    return output

def save_to_file(content, customer_name, output_dir=None):
    """保存推进建议到文件"""
    if output_dir is None:
        output_dir = os.path.expanduser("~/.workbuddy/workspace/investment-assistant")
    
    os.makedirs(output_dir, exist_ok=True)
    
    date_str = datetime.now().strftime("%Y%m%d")
    output_file = os.path.join(output_dir, f"推进建议_{customer_name}_{date_str}.md")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_file

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python3 progress_advisor.py <客户名称> [决策人类型]")
        print("示例: python3 progress_advisor.py \"测试科技公司\" CEO")
        print("决策人类型：CEO/COO/CFO/CTO")
        sys.exit(1)
    
    customer_name = sys.argv[1]
    decision_maker = sys.argv[2] if len(sys.argv) > 2 else "CEO"
    
    print(f"📈 开始生成推进建议: {customer_name}")
    print(f"🧑‍💼 决策人类型: {decision_maker}")
    
    # 模拟数据（实际应从客户档案读取）
    stage = 3  # 方案对比阶段
    duration_days = 12  # 已停留12天
    interaction_history = []  # 实际应从跟进记录读取
    
    # 生成推进建议
    advice = generate_progress_advice(customer_name, stage, duration_days, decision_maker, interaction_history)
    
    # 格式化输出
    content = format_progress_advice(advice)
    print(content)
    
    # 保存文件
    output_file = save_to_file(content, customer_name)
    print(f"\n✅ 推进建议已保存: {output_file}")
    
    return output_file

if __name__ == "__main__":
    main()
