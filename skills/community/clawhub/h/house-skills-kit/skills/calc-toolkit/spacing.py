#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具27 · 日照楼间距测算器（冬至正午 · 物理口径）

用法:
  # 前栋18层，昆明（默认纬度25），实际间距50m
  python3 spacing.py --floors 18 --actual 50

  # 前栋26层×3.0米层高，北京，看第5层采光
  python3 spacing.py --floors 26 --floor-h 3.0 --latitude 39.9 --actual 70 --floor 5

  # 只算理论最低间距
  python3 spacing.py --floors 18

公式（北半球冬至正午，全年影子最长时刻）:
  太阳高度角 h = 90° − 纬度 − 23.45°（冬至赤纬）
  日照间距系数 = 1 / tan(h)        ← 昆明1.13 / 广州1.06 / 上海1.22 / 北京1.99 / 哈尔滨2.63
  最低楼间距 D_min = 前栋总高 × 系数
  遮挡分析: 受挡面阴影高 = 前栋高 − 实距/系数；被挡层数 = 阴影高 ÷ 层高

标准依据: GB50180《城市居住区规划设计标准》——住宅日照需满足
  大寒日≥2小时 或 冬至日≥1小时（按气候区划），此处按最不利冬至正午简化。
  注: 地方规划口径常用"有效日照带(8/9时~15/16时)"而非正午，实际验收以地方细则为准。
"""
import argparse
import math

W = 58


def get_rules(city=None):
    try:
        from ruleengine import get_rules as _gr
        rules, _ = _gr("sunshine", city=city)
        return rules
    except Exception:
        return {}


def main():
    ap = argparse.ArgumentParser(description="日照楼间距测算（冬至正午物理口径）")
    ap.add_argument("--floors", type=int, help="前栋（南侧遮挡建筑）层数")
    ap.add_argument("--floor-h", type=float, default=None, help="层高（默认取规则库2.9）")
    ap.add_argument("--latitude", type=float, default=None, help="纬度（默认取规则库/城市档）")
    ap.add_argument("--actual", type=float, default=0, help="实际楼间距（m，给则做达标判定）")
    ap.add_argument("--floor", type=int, default=0, help="关注的楼层（给则判该层正午采光）")
    ap.add_argument("--city", default=None)
    args = ap.parse_args()

    if not args.floors:
        ap.print_help()
        return

    R = get_rules(city=args.city)
    floor_h = args.floor_h if args.floor_h else float(R.get("floor_h", 2.9))
    lat = args.latitude if args.latitude else float(R.get("latitude", 25.0))

    h_sun = 90 - lat - 23.45                       # 冬至正午太阳高度角
    coef = 1 / math.tan(math.radians(h_sun))
    H = args.floors * floor_h
    d_min = H * coef

    print("=" * W)
    print("日照楼间距测算（冬至正午 · 全年影子最长）")
    print("=" * W)
    print(f"前栋 {args.floors} 层 × {floor_h:g}m = {H:.1f}m ｜ 纬度 {lat:g}°"
          + (f"（{args.city}）" if args.city else ""))
    print(f"  冬至正午太阳高度角: {h_sun:.1f}° ｜ 日照间距系数: {coef:.2f}")
    print("-" * W)
    print(f"★ 最低楼间距 D_min = {H:.1f} × {coef:.2f} = {d_min:.1f} m")
    if args.actual > 0:
        gap = args.actual - d_min
        ok = gap >= 0
        print(f"  实际间距 {args.actual:g}m → {'✓ 达标' if ok else '✗ 低于理论最低'}"
              f"（{'富余' if ok else '差'} {abs(gap):.1f}m）")
        shadow_h = H - args.actual / coef
        shaded = max(0.0, shadow_h / floor_h)
        if shaded < 0.05:
            print("  正午被挡楼层: 无（首层即采光）")
        else:
            top = int(shaded)
            extra = ""
            if shaded != int(shaded):
                top = int(shaded) + 1
                extra = f"（第{int(shaded)+1}层半挡，窗台高度影响）"
            print(f"  正午被挡楼层: 1~{top} 层受影响{extra}")
            if args.floor:
                blocked = args.floor <= shaded
                print(f"  ★ 关注的第 {args.floor} 层: {'正午被前栋遮挡' if blocked else '正午可采光 ✓'}")
    elif args.floor:
        need_d = (args.floor - 1) * floor_h
        need_d = H - need_d
        print(f"  第 {args.floor} 层正午采光要求间距 ≥ {need_d:.1f}m")
    print("-" * W)
    print("提示:")
    print("  · 本工具为冬至正午最不利简化；国标GB50180按气候区执行大寒日≥2h或冬至日≥1h")
    print("  · 地方验收多用有效日照带（8/9~15/16时）+满窗日照，规划间距常另有地方系数表")
    print("  · 常见系数参考: 昆明≈1.1 / 上海≈1.2 / 济南≈1.5 / 北京≈1.7-2.0 / 哈尔滨≈2.6")
    print("  · 坡地/错位排布/檐口装饰层都会影响实际遮挡，以日照分析软件结论为准")


if __name__ == "__main__":
    main()
