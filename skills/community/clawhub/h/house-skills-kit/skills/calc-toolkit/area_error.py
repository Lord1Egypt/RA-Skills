#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具23 · 面积误差补退计算器（3%红线 · 法定兜底口径）

用法:
  # 合同100㎡收房103.5㎡ 单价1万
  python3 area_error.py --contract 100 --final 103.5 --price 10000

  # 缩水：合同100㎡收房95.8㎡
  python3 area_error.py --contract 100 --final 95.8 --price 10000

  # 已知误差比直接算
  python3 area_error.py --contract 100 --ratio 4.2 --price 10000

法条依据（全国统一，合同未另有约定时适用）:
  · 《商品房销售管理办法》第20条（建设部令第88号）
  · 最高人民法院《关于审理商品房买卖合同纠纷案件的司法解释》第14条
  规则:
    面积误差比 = (产权登记面积 − 合同约定面积) / 合同约定面积 × 100%
    ① |误差比| ≤ 3%（含）: 据实结算，多退少补（按合同单价）；买受人不得据此解约
    ② |误差比| > 3%: 买受人有权退房（返还已付购房款+利息）
       不退房继续履行:
         面积大了 → ≤3%部分买受人按合同价补足；>3%部分开发商承担、产权归买受人（白送）
         面积小了 → ≤3%部分开发商返还并支付利息；>3%部分开发商双倍返还
  ⚠ 合同另有约定的从约定（实践中常见开发商以补充协议改为"多退少补"，该类条款
    涉嫌排除消费者主要权利，可主张无效——郑州中院等已有多起认定显失公平判例）
"""
import argparse
import sys

W = 58


def fmt_money(x):
    return f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description="面积误差补退计算器（3%红线法定口径）")
    ap.add_argument("--contract", type=float, help="合同约定面积（㎡）")
    ap.add_argument("--final", type=float, default=None, help="产权登记面积（㎡，与--ratio二选一）")
    ap.add_argument("--ratio", type=float, default=None, help="面积误差比%%（直接给比率，与--final二选一）")
    ap.add_argument("--price", type=float, help="合同单价（元/㎡）")
    args = ap.parse_args()

    if not args.contract or not args.price or (args.final is None) == (args.ratio is None):
        ap.print_help()
        sys.exit(1)

    contract = args.contract
    unit = args.price
    if args.final is not None:
        final = args.final
        ratio = (final - contract) / contract * 100
    else:
        ratio = args.ratio
        final = contract * (1 + ratio / 100)

    diff_area = final - contract
    unit_area_value = abs(diff_area) * unit          # 全部误差对应的价款（据实结算口径）
    ratio_abs = abs(ratio)

    print("=" * W)
    print("面积误差补退测算（3%红线 · 法定兜底口径）")
    print("=" * W)
    print(f"合同面积 {contract:g}㎡ → 产权登记 {final:.2f}㎡ ｜ 单价 {fmt_money(unit)} 元/㎡")
    sign = "+" if diff_area >= 0 else "−"
    print(f"误差 {sign}{abs(diff_area):.2f}㎡ ｜ 面积误差比 = {ratio:+.2f}%")
    print("-" * W)

    if ratio_abs <= 3:
        # ① 据实结算
        print(f"【判定】|{ratio:.2f}%| ≤ 3%（含）→ 据实结算，多退少补")
        print("  法律依据: 销售管理办法第20条① / 司法解释第14条①")
        print("  （此区间买受人请求解约的，法院不予支持）")
        if diff_area >= 0:
            print(f"  ★ 买受人补足房款: {fmt_money(unit_area_value)} 元"
                  f"（{diff_area:.2f}㎡ × {fmt_money(unit)}）")
        else:
            print(f"  ★ 开发商返还房款: {fmt_money(unit_area_value)} 元"
                  f"（{abs(diff_area):.2f}㎡ × {fmt_money(unit)}）")
    else:
        over_area = abs(diff_area) - contract * 0.03   # 超3%部分的面积
        within_value = contract * 0.03 * unit          # 3%以内部分价款
        over_value = over_area * unit                  # 超3%部分价款（一倍）
        print(f"【判定】|{ratio:.2f}%| > 3% → 触发法定保护条款")
        print("  法律依据: 销售管理办法第20条② / 司法解释第14条②")
        print(f"  买受人享有【退房权】：返还已付购房款+利息（30日内退还）")
        print("-" * W)
        print("若不退房、继续履行：")
        if diff_area > 0:
            # 面积大了
            print(f"  ≤3%部分（{contract*0.03:g}㎡）买受人按合同价补足: {fmt_money(within_value)} 元")
            print(f"  >3%部分（{over_area:.2f}㎡ × {fmt_money(unit)} = {fmt_money(over_value)} 元）")
            print(f"  ★ 该超出部分房款由开发商承担，产权归买受人 —— 等于【白送 {over_area:.2f}㎡】")
            print(f"  实际只需补: {fmt_money(within_value)} 元（而非据实结算的 {fmt_money(unit_area_value)} 元）")
        else:
            # 面积小了
            print(f"  ≤3%部分（{contract*0.03:g}㎡）开发商返还: {fmt_money(within_value)} 元 + 利息")
            print(f"  >3%部分（{over_area:.2f}㎡ × {fmt_money(unit)} = {fmt_money(over_value)} 元）开发商【双倍】返还")
            dbl = over_value * 2
            print(f"  ★ 双倍返还金额: {fmt_money(dbl)} 元")
            print(f"  合计应返还: {fmt_money(within_value + dbl)} 元"
                  f"（约为据实结算 {fmt_money(unit_area_value)} 元的 {(within_value+dbl)/unit_area_value:.1f} 倍）")
    print("-" * W)
    print("提示:")
    print("  · 合同对误差处理另有约定的，从约定；但'只多退少补/免除双倍返还/勾掉退房权'")
    print("    类条款涉嫌显失公平，可依民法典第497条主张无效（参考郑州中院普法案例）")
    print("  · 退房利息计付标准以法院判决/合同约定为准（常用LPR或同期存款利率）")
    print("  · 因规划设计变更造成面积差异的，还应签署补充协议（办法第24条）")


if __name__ == "__main__":
    main()
