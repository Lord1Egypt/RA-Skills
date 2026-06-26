#!/usr/bin/env python3
"""项目管理计算引擎 — 根据飞书表格数据自动计算"""

import json
import sys
import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

# 里程碑推算规则
MILESTONE_RULES = {
    "M1": {"name": "需求确认", "offset": None},        # 由 PM 提供
    "M2": {"name": "试运行完成", "offset": relativedelta(months=3)},  # M1 + 3个月
    "M3": {"name": "验收通过", "offset": timedelta(days=15)},        # M2 + 半个月
    "M4": {"name": "质保完成", "offset": relativedelta(years=1)},    # M3 + 1年
}


def calc_milestone_dates(m1_date_str):
    """
    根据需求确认日期自动推算所有里程碑日期

    Args:
        m1_date_str: 需求确认日期（格式: YYYY-MM-DD 或 YYYY年M月D日）

    Returns:
        dict: 各里程碑的计划完成日期
    """
    # 解析日期
    for fmt in ["%Y-%m-%d", "%Y年%m月%d日", "%Y.%m.%d", "%Y/%m/%d"]:
        try:
            m1_date = datetime.strptime(m1_date_str.strip(), fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError(f"无法解析日期: {m1_date_str}")

    dates = {}
    prev_date = m1_date

    for key, rule in MILESTONE_RULES.items():
        if rule["offset"] is None:
            dates[key] = {"name": rule["name"], "date": m1_date}
        else:
            calc_date = prev_date + rule["offset"]
            dates[key] = {"name": rule["name"], "date": calc_date}
            prev_date = calc_date

    return dates


def calc_payment_amounts(contract_amount, ratios):
    """
    根据合同金额和回款比例自动计算回款金额

    Args:
        contract_amount: 合同金额（万元）
        ratios: 各里程碑回款比例列表 [M1比例, M2比例, M3比例, M4比例]

    Returns:
        list: 各里程碑回款金额（万元）
    """
    amounts = []
    for r in ratios:
        amount = round(contract_amount * r / 100, 4)
        amounts.append(amount)
    return amounts


def calc_payment_status(planned, actual):
    """
    根据计划金额和实际金额判断回款/付款状态

    Args:
        planned: 计划金额
        actual: 实际金额

    Returns:
        str: 状态文本
    """
    if actual <= 0:
        return "未回款"
    elif actual < planned:
        return "部分回款"
    else:
        return "已回款"


def calc_payment_warning(planned_date_str, actual_amount, planned_amount):
    """
    根据计划回款日期和实际金额判断预警级别

    Args:
        planned_date_str: 计划回款日期
        actual_amount: 实际回款金额
        planned_amount: 计划回款金额

    Returns:
        str: 预警标记
    """
    if actual_amount >= planned_amount:
        return "✅"

    now = datetime.now()

    for fmt in ["%Y-%m-%d", "%Y年%m月%d日", "%Y.%m.%d", "%Y/%m/%d"]:
        try:
            planned_date = datetime.strptime(planned_date_str.strip(), fmt)
            break
        except ValueError:
            continue
    else:
        return "—"

    days_diff = (planned_date - now).days

    if days_diff < 0:
        return "🔴 已逾期"
    elif days_diff <= 7:
        return "🟡 即将到期"
    else:
        return "—"


def calc_milestone_status(planned_date_str, actual_date_str=None):
    """
    根据计划完成日期和实际完成日期判断里程碑状态

    Args:
        planned_date_str: 计划完成日期
        actual_date_str: 实际完成日期（可选）

    Returns:
        str: 状态标记
    """
    if actual_date_str and actual_date_str.strip():
        return "✅ 已完成"

    now = datetime.now()

    for fmt in ["%Y-%m-%d", "%Y年%m月%d日", "%Y.%m.%d", "%Y/%m/%d"]:
        try:
            planned_date = datetime.strptime(planned_date_str.strip(), fmt)
            break
        except ValueError:
            continue
    else:
        return "⬜ 未开始"

    days_diff = (planned_date - now).days

    if days_diff < 0:
        return "🔴 已延期"
    elif days_diff <= 7:
        return "🟦 即将到期"
    else:
        return "🟦 进行中"


def calc_risks(milestones, changes_count_by_milestone, budget_used, budget_total):
    """
    自动识别风险

    Args:
        milestones: 里程碑数据列表
        changes_count_by_milestone: 各里程碑变更数
        budget_used: 已用预算
        budget_total: 总预算

    Returns:
        list: 识别到的风险列表
    """
    risks = []

    for m in milestones:
        # R001: 里程碑延期
        if m.get("status") in ["🔴 已延期"]:
            risks.append({
                "rule": "R001",
                "desc": f"{m['name']}已延期",
                "level": "🔴高",
                "milestone": m["name"]
            })

        # R002: 里程碑即将到期
        if m.get("status") in ["🟦 即将到期"]:
            risks.append({
                "rule": "R002",
                "desc": f"{m['name']}即将到期",
                "level": "🟡中",
                "milestone": m["name"]
            })

        # R003: 需求变更频发
        m_name = m.get("name", "")
        change_count = changes_count_by_milestone.get(m_name, 0)
        if change_count >= 3:
            risks.append({
                "rule": "R003",
                "desc": f"{m_name}变更频发（{change_count}次）",
                "level": "🟡中",
                "milestone": m_name
            })

    # R004: 预算超支风险
    if budget_total > 0 and budget_used > budget_total * 0.8:
        risks.append({
            "rule": "R004",
            "desc": f"预算超支风险（已用{budget_used}/{budget_total}，超过80%）",
            "level": "🔴高",
            "milestone": "全局"
        })

    return risks


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法:")
        print("  python calc_engine.py milestones <M1日期>")
        print("  python calc_engine.py payments <合同金额> <比例1> <比例2> <比例3> <比例4>")
        print("  python calc_engine.py status <计划日期> [实际日期]")
        print("  python calc_engine.py warning <计划日期> <实际金额> <计划金额>")
        sys.exit(1)

    action = sys.argv[1]

    if action == "milestones":
        result = calc_milestone_dates(sys.argv[2])
        for k, v in result.items():
            print(f"{k} {v['name']}: {v['date'].strftime('%Y-%m-%d')}")

    elif action == "payments":
        amount = float(sys.argv[2])
        ratios = [float(x) for x in sys.argv[3:7]]
        amounts = calc_payment_amounts(amount, ratios)
        for i, a in enumerate(amounts):
            print(f"M{i+1}: {ratios[i]}% → {a} 万元")

    elif action == "status":
        planned = sys.argv[2]
        actual = sys.argv[3] if len(sys.argv) > 3 else None
        print(calc_milestone_status(planned, actual))

    elif action == "warning":
        planned = sys.argv[2]
        actual = float(sys.argv[3])
        planned_amt = float(sys.argv[4])
        print(calc_payment_warning(planned, actual, planned_amt))

    else:
        print(f"未知动作: {action}", file=sys.stderr)
        sys.exit(1)