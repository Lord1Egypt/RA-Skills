#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具24 · 违约金/定金测算器（定金罚则 + 延期交房）

用法:
  # 房价100万 定金30万 买方违约（验20%红线+算损失）
  python3 deposit.py --mode penalty --price 1000000 --deposit 300000 --breach buyer

  # 卖方违约（双倍返还）+ 合同另有违约金10万（择一比较）
  python3 deposit.py --mode penalty --price 1000000 --deposit 300000 --breach seller --penalty 100000

  # 延期交房：日万分之一，逾期90天
  python3 deposit.py --mode late --price 1500000 --days 90 --rate-wan 1

法条依据（全国统一）:
  · 民法典第586条: 定金不得超过主合同标的额20%，超过部分不产生定金效力
    （违约时超出部分按普通预付款处理——返还，不适用罚则）
  · 民法典第587条: 定金罚则——给付方违约无权请求返还；收受方违约双倍返还
  · 民法典第588条: 定金与违约金【择一】适用；定金不足弥补损失可另行索赔
    （买卖合同解释第28条: 定金+赔偿总和不超过实际损失）
  · 民法典第585条: 违约金"过分高于损失"可请求酌减，司法实践参考线=超过损失30%
  · 延期交房违约金为合同约定惯例（日万分之一~万分之三/日），非法定标准
"""
import argparse
import sys

W = 58


def fmt_money(x):
    return f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description="违约金/定金测算器（民法典定金罚则口径）")
    ap.add_argument("--mode", choices=["penalty", "late"], default="penalty", help="penalty=定金/违约金 late=延期交房")
    ap.add_argument("--price", type=float, help="合同总价（元）")
    ap.add_argument("--deposit", type=float, default=0, help="实付定金（元）")
    ap.add_argument("--breach", choices=["buyer", "seller"], default="buyer", help="违约方")
    ap.add_argument("--penalty", type=float, default=0, help="合同另约定的违约金（元，与定金并存时择一）")
    ap.add_argument("--days", type=int, default=0, help="逾期天数（late模式）")
    ap.add_argument("--rate-wan", type=float, default=1.0, help="日违约金 万分之N/日（late模式，默认1）")
    args = ap.parse_args()

    if not args.price:
        ap.print_help()
        sys.exit(1)

    print("=" * W)
    if args.mode == "late":
        daily = args.price * args.rate_wan / 10000
        total = daily * args.days
        print("延期交房违约金测算（合同约定口径）")
        print("=" * W)
        print(f"房价 {fmt_money(args.price)} ｜ 约定 日万分之{args.rate_wan:g} ｜ 逾期 {args.days} 天")
        print("-" * W)
        print(f"  日违约金:  {fmt_money(daily)} 元")
        print(f"  ★ 合计:    {fmt_money(total)} 元（占房价 {total/args.price*100:.2f}%）")
        print("-" * W)
        print("  · 常见约定档位: 日万分之0.5~3（万分之一=年化3.65%量级）")
        print("  · 司法实践: 违约金超过实际损失30%可请求酌减（民法典585条）")
        print("  · 逾期交付损失参照: 同地段同类房屋租金标准（司法解释）")
        sys.exit(0)

    # ── penalty 模式 ──
    cap = args.price * 0.20
    valid = min(args.deposit, cap)          # 有效定金（适用罚则）
    excess = args.deposit - valid           # 超出部分（不产生定金效力，违约时原额处理）
    ratio = args.deposit / args.price * 100 if args.price else 0

    print("定金罚则测算（民法典586/587/588）")
    print("=" * W)
    print(f"合同总价 {fmt_money(args.price)} ｜ 实付定金 {fmt_money(args.deposit)}（{ratio:.1f}%）")
    if excess > 0:
        print(f"  ⚠ 超过20%红线（上限 {fmt_money(cap)}）：超出的 {fmt_money(excess)} 元")
        print("    【不产生定金效力】——违约时按普通预付款原额返还，不适用罚则")
    print("-" * W)
    print(f"有效定金（适用罚则）: {fmt_money(valid)} 元")
    loss = gain = 0.0
    if args.breach == "buyer":
        loss = valid
        print(f"【买方违约】无权请求返还定金")
        print(f"  ★ 买方损失: {fmt_money(loss)} 元（有效定金被没收）")
        if excess > 0:
            print(f"  超出部分 {fmt_money(excess)} 元【应予返还】—— 开发商只能没收 {fmt_money(valid)}")
    else:
        gain = valid * 2
        print(f"【卖方违约】双倍返还定金（587条）")
        net = gain + excess - args.deposit
        print(f"  ★ 应返还: {fmt_money(gain)} 元（有效定金双倍）" + (f" + 超出部分原额 {fmt_money(excess)} 元 = 共 {fmt_money(gain+excess)} 元" if excess > 0 else ""))
        print(f"  买方净赚: {fmt_money(net)} 元（实缴 {fmt_money(args.deposit)}，收回 {fmt_money(gain+excess)}）")
    if args.penalty > 0:
        print("-" * W)
        print(f"合同另有违约金 {fmt_money(args.penalty)} 元 → 【择一适用】（588条，不可叠加）")
        base_d = gain if args.breach == "seller" else loss
        best = max(base_d, args.penalty)
        pick = "定金罚则" if base_d >= args.penalty else "违约金条款"
        print(f"  定金路径 {fmt_money(base_d)} vs 违约金路径 {fmt_money(args.penalty)} → 守约方应选【{pick}】（{fmt_money(best)}）")
        print("  · 若定金不足弥补损失，还可另行索赔超过部分（总和≤实际损失）")
    print("-" * W)
    print("提示:")
    print("  · 定金须实际交付且写明'定金'字样（订金/意向金/认筹金不适用罚则）")
    print("  · 违约金过分高于损失（>损失30%）可请求法院酌减；过低于损失可请求增加")


if __name__ == "__main__":
    main()
