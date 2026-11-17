#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具26 · 楼面价与货值测算器（拿地视角 · 地货比）

用法:
  # 土地4.2亿 亩价换算+容积率2.5 → 楼面价
  python3 floor_price.py --land 420000000 --area-mu 63 --far 2.5

  # 已知计容面积：直接算楼面价+货值
  python3 floor_price.py --land 420000000 --gfa 105000 --price 15000

  # 只算货值结构
  python3 floor_price.py --gfa 105000 --price 15000

公式:
  楼面价 = 土地总价 ÷ 计容建筑面积（GFA = 占地面积 × 容积率）
  亩 → ㎡: ×666.67
  总货值 = 可售面积 × 销售均价（简化: 可售=计容，实际要扣配套/自持，--sellable可调）
  地货比 = 土地总价 ÷ 总货值（拿地安全线经验: >0.6偏危险, <0.4较安全；演示档）
"""
import argparse

W = 58


def fmt_money(x):
    if x >= 1e8:
        return f"{x/1e8:.2f}亿"
    if x >= 1e4:
        return f"{x/1e4:,.10g}万"     # 1.5万不吞成2万
    return f"{x:,.0f}"


def main():
    ap = argparse.ArgumentParser(description="楼面价与货值测算（拿地视角）")
    ap.add_argument("--land", type=float, default=0, help="土地总价（元）")
    ap.add_argument("--area-mu", type=float, default=0, help="占地面积（亩）")
    ap.add_argument("--area-sqm", type=float, default=0, help="占地面积（㎡，与--area-mu二选一）")
    ap.add_argument("--far", type=float, default=0, help="容积率")
    ap.add_argument("--gfa", type=float, default=0, help="计容建筑面积（㎡，可直接给）")
    ap.add_argument("--price", type=float, default=0, help="销售均价（元/㎡，给则算货值）")
    ap.add_argument("--sellable", type=float, default=1.0, help="可售面积比例（默认1.0=计容全可售）")
    args = ap.parse_args()

    if not args.gfa and not ((args.land or args.price) and (args.area_mu or args.area_sqm) and args.far):
        ap.print_help()
        return

    area_sqm = args.area_sqm if args.area_sqm else args.area_mu * 2000 / 3   # 1亩=2000/3㎡
    gfa = args.gfa if args.gfa else area_sqm * args.far
    sellable = gfa * args.sellable

    print("=" * W)
    print("楼面价与货值测算（拿地视角 · 演示档）")
    print("=" * W)
    if args.area_mu or args.area_sqm:
        src = f"{args.area_mu:g}亩" if args.area_mu else f"{area_sqm:,.0f}㎡"
        print(f"占地 {src} = {area_sqm:,.0f}㎡ ｜ 容积率 {args.far:g} → 计容 {gfa:,.0f}㎡")
    else:
        print(f"计容建筑面积 {gfa:,.0f}㎡")
    if args.land:
        fp = args.land / gfa
        print(f"土地总价 {fmt_money(args.land)}")
        print(f"  ★ 楼面价:  {fp:,.0f} 元/㎡" + (f"  ｜ 亩均 {args.land/max(args.area_mu,1e-9)/1e4:,.0f} 万/亩" if args.area_mu else ""))
    if args.price:
        value = sellable * args.price
        print(f"销售均价 {args.price:,.0f} 元/㎡ × 可售 {sellable:,.0f}㎡（{args.sellable*100:g}%）")
        print(f"  ★ 总货值: {fmt_money(value)}")
        if args.land:
            fp = args.land / gfa
            ratio = args.land / value
            print(f"  ★ 楼面价/售价 = {fp:,.0f} / {args.price:,.0f} = {fp/args.price*100:.1f}%")
            print(f"  ★ 地货比 = {ratio:.2f}  （经验: <0.4较安全 / 0.4-0.6常规 / >0.6拿地偏险）")
            print(f"  毛剩余空间(不含建安费用): ≈{fmt_money(value - args.land)}（未扣建安/税费/营销/财务）")
    print("-" * W)
    print("提示:")
    print("  · 计容面积≠可售面积: 配套/物业/自持要扣（--sellable 0.85等）")
    print("  · 实际货值结构常分业态（住宅/商业/车位），此处为单一均价简化")
    print("  · 地货比为行业经验参考线，非监管指标；投资测算须含全成本（建安通常4000-6000元/㎡起）")


if __name__ == "__main__":
    main()
