#!/usr/bin/env python3
"""
不良资产竞价快速报价计算器

用途：在银登中心/阿里司法拍卖竞价前，快速计算出价区间
依赖：Python 3.6+（只需标准库）

用法：
  # 个贷包快速出价（交互模式）
  python bid-quick-calc.py

  # 指定参数出价（适合批量）
  python bid-quick-calc.py --amount 120000000 --recovery 0.15 --discount 0.12 --term 2 --cost 0.05

  # 对公抵押包（更高回收率、更长周期）
  python bid-quick-calc.py --amount 50000000 --recovery 0.40 --discount 0.10 --term 3 --cost 0.08

数据来源：银登中心历史成交数据 + 行业经验值（2026H1）
"""

import sys
import argparse
import math


def bid_quote(base_amount, recovery_rate, discount_rate, term_year, cost_rate):
    """
    核心报价计算函数

    Parameters:
    - base_amount: 本金总额（元）
    - recovery_rate: 预期回收率（如0.15表示15%）
    - discount_rate: 折现率（如0.12表示12%）
    - term_year: 回收周期（年）
    - cost_rate: 处置费率（如0.05表示5%）

    Returns:
    - dict with bidding ladder
    """
    # 预期回收现值
    pv = base_amount * recovery_rate / ((1 + discount_rate) ** term_year)

    # 处置费用折减
    total_cost = base_amount * cost_rate

    # 扣除费用后净回收
    net_pv = pv - total_cost

    # 底线价格（低于此线不参与）
    reservation = net_pv * 0.5

    # 多轮竞价阶梯
    round1_bid = net_pv * 0.60   # 首轮试探（底价+少量溢价）
    round2_bid = net_pv * 0.75   # 二轮加码
    round3_bid = net_pv * 0.88   # 末轮决断（接近上限）
    max_bid = net_pv * 0.95      # 最高限价（超过此线必亏）

    # 隐含折扣率
    implied_discount = round(target := net_pv * 0.80 / base_amount, 4)

    # IRR 估算（反推）
    irr_estimate = (pv / max_bid) ** (1 / term_year) - 1

    return {
        "本金总额": round(base_amount, 2),
        "预期回收现值": round(pv, 2),
        "处置费用": round(total_cost, 2),
        "净回收现值": round(net_pv, 2),
        "底线价格(不参与)": round(reservation, 2),
        "首轮出价(试探)": round(round1_bid, 2),
        "二轮出价(加码)": round(round2_bid, 2),
        "末轮出价(决断)": round(round3_bid, 2),
        "最高限价(不超)": round(max_bid, 2),
        "隐含折扣率": implied_discount,
        "隐含IRR(上限反推)": round(irr_estimate, 4),
    }


# ─── 资产类型预设参数 ────────────────────────────────────────────

PRESETS = {
    "个贷包": {
        "description": "信用卡/消费贷不良包，小额分散，AI催收为主",
        "recovery": 0.12,
        "discount": 0.14,
        "term": 2.0,
        "cost": 0.05,
    },
    "对公抵押": {
        "description": "企业贷款抵押包，单笔大额，法律处置周期长",
        "recovery": 0.45,
        "discount": 0.10,
        "term": 3.0,
        "cost": 0.08,
    },
    "一线住宅抵押": {
        "description": "一线城市住宅抵押不良，流动性强，回收确定性高",
        "recovery": 0.75,
        "discount": 0.08,
        "term": 1.5,
        "cost": 0.05,
    },
    "二线住宅抵押": {
        "description": "二线城市住宅抵押，回收率略低于一线",
        "recovery": 0.60,
        "discount": 0.10,
        "term": 2.0,
        "cost": 0.06,
    },
    "信用大额对公": {
        "description": "纯信用大额对公贷款，无抵押，回收依赖企业自身",
        "recovery": 0.20,
        "discount": 0.16,
        "term": 3.0,
        "cost": 0.10,
    },
    "产业资本(战略)": {
        "description": "有战略协同价值的资产，产业资本出价逻辑不同",
        "recovery": 0.55,
        "discount": 0.08,
        "term": 3.0,
        "cost": 0.06,
    },
}


def get_preset(preset_name, base_amount):
    """根据预设类型获取参数"""
    preset = PRESETS.get(preset_name)
    if not preset:
        return None

    result = {"类型": preset_name, "说明": preset["description"]}
    result.update(bid_quote(
        base_amount,
        preset["recovery"],
        preset["discount"],
        preset["term"],
        preset["cost"],
    ))
    result["预设_回收率"] = preset["recovery"]
    result["预设_折现率"] = preset["discount"]
    result["预设_周期(年)"] = preset["term"]
    result["预设_处置费率"] = preset["cost"]
    return result


def format_output(data):
    """格式化输出为可读表格"""
    lines = []
    lines.append("=" * 60)
    if "类型" in data:
        lines.append(f"  {data['类型']} — {data['说明']}")
        lines.append("-" * 60)
    lines.append(f"  本金总额:          {data['本金总额']:>15,.2f}")
    lines.append(f"  预期回收现值:      {data['预期回收现值']:>15,.2f}")
    lines.append(f"  处置费用:          {data['处置费用']:>15,.2f}")
    lines.append(f"  净回收现值:        {data['净回收现值']:>15,.2f}")
    lines.append("-" * 60)
    lines.append(f"  底线价格(不参与):  {data['底线价格(不参与)']:>15,.2f}")
    lines.append(f"  首轮出价(试探):    {data['首轮出价(试探)']:>15,.2f}")
    lines.append(f"  二轮出价(加码):    {data['二轮出价(加码)']:>15,.2f}")
    lines.append(f"  末轮出价(决断):    {data['末轮出价(决断)']:>15,.2f}")
    lines.append(f"  最高限价(不超):    {data['最高限价(不超)']:>15,.2f}")
    lines.append("-" * 60)
    lines.append(f"  隐含折扣率:        {data['隐含折扣率']:>15.4f}")
    lines.append(f"  隐含IRR(上限反推): {data['隐含IRR(上限反推)']:>15.2%}")
    lines.append("=" * 60)
    return "\n".join(lines)


def interactive_mode():
    """交互模式：引导用户输入"""
    print("=" * 60)
    print("  不良资产竞价快速报价计算器 v1.0")
    print("  🐎 助手 · NPL估值工具")
    print("=" * 60)
    print()

    # 选择预设或手动输入
    print("可用预设类型：")
    for i, name in enumerate(PRESETS, 1):
        print(f"  [{i}] {name} — {PRESETS[name]['description']}")
    print("  [0] 手动输入参数")
    print()

    try:
        choice = input("请选择 [0-6]: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n退出")
        return

    try:
        choice_int = int(choice) if choice else -1
    except ValueError:
        choice_int = -1

    if choice_int == 0:
        # 手动输入
        try:
            amount = float(input("本金总额（万元）: ")) * 10_000
            recovery = float(input("预期回收率（如0.15表示15%）: "))
            discount = float(input("折现率（如0.12表示12%）: "))
            term = float(input("回收周期（年，如2）: "))
            cost = float(input("处置费率（如0.05表示5%）: "))
        except (EOFError, KeyboardInterrupt, ValueError):
            print("\n输入无效，退出")
            return

        result = bid_quote(amount, recovery, discount, term, cost)
        print()
        print(format_output(result))

    elif 1 <= choice_int <= len(PRESETS):
        preset_name = list(PRESETS.keys())[choice_int - 1]
        try:
            amount = float(input(f"请输入{preset_name}本金总额（万元）: ")) * 10_000
        except (EOFError, KeyboardInterrupt, ValueError):
            print("\n输入无效，退出")
            return

        result = get_preset(preset_name, amount)
        print()
        print(format_output(result))
    else:
        print("无效选择")
        return


def cli_mode(args):
    """CLI参数模式"""
    result = bid_quote(
        base_amount=args.amount,
        recovery_rate=args.recovery,
        discount_rate=args.discount,
        term_year=args.term,
        cost_rate=args.cost,
    )
    print(format_output(result))

    # 如有预设类型，额外输出预设对比
    if args.preset:
        preset_result = get_preset(args.preset, args.amount)
        if preset_result:
            print()
            print("📊 预设类型参考：")
            print(format_output(preset_result))


def main():
    parser = argparse.ArgumentParser(
        description="不良资产竞价快速报价计算器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 个贷包 (1.2亿本金，15%回收率，12%折现，2年周期，5%处置费)
  bid-quick-calc.py --amount 120000000 --recovery 0.15 --discount 0.12 --term 2 --cost 0.05

  # 对公抵押包 (5000万本金，用预设类型)
  bid-quick-calc.py --amount 50000000 --preset "对公抵押"

  # 交互模式（默认）
  bid-quick-calc.py
        """,
    )
    parser.add_argument("--amount", type=float, help="本金总额（元）")
    parser.add_argument("--recovery", type=float, help="预期回收率（如0.15）")
    parser.add_argument("--discount", type=float, help="折现率（如0.12）")
    parser.add_argument("--term", type=float, help="回收周期（年）")
    parser.add_argument("--cost", type=float, help="处置费率（如0.05）")
    parser.add_argument("--preset", type=str, help=f"预设类型: {', '.join(PRESETS.keys())}")

    args = parser.parse_args()

    # 检测是否提供了完整参数
    has_core_params = all([
        args.amount is not None,
        args.recovery is not None,
        args.discount is not None,
        args.term is not None,
        args.cost is not None,
    ])

    if has_core_params:
        cli_mode(args)
    elif args.amount is not None and args.preset:
        # 使用预设参数
        result = get_preset(args.preset, args.amount)
        if result:
            print(format_output(result))
        else:
            print(f"错误：未知预设类型 '{args.preset}'")
            print(f"可用预设: {', '.join(PRESETS.keys())}")
            sys.exit(1)
    else:
        # 不完整或无参数 → 交互模式
        interactive_mode()


if __name__ == "__main__":
    main()
