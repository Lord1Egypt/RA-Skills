#!/usr/bin/env python3
"""
卡路里计算脚本
根据步数和运动时长计算消耗热量

使用方法:
    python calorie_calc.py --steps 10698 --weight 70.9 --age 34

依赖:
    无（纯Python标准库）
"""

import argparse
from datetime import datetime


def calc_step_calories(steps, weight=70):
    """计算步数消耗的卡路里"""
    # 每步约消耗0.04-0.06卡路里，根据体重调整
    cal_per_step = 0.04 + (weight / 100) * 0.02
    return steps * cal_per_step


def calc_walking_calories(distance_km, weight=70, duration_min=60):
    """计算步行消耗的卡路里"""
    # MET值计算：快走约4.5 MET
    # 卡路里 = MET × 体重(kg) × 时间(小时)
    met = 4.5
    hours = duration_min / 60
    return met * weight * hours


def calc_running_calories(distance_km, weight=70):
    """计算跑步消耗的卡路里"""
    # 慢跑约7 MET
    met = 7
    hours = distance_km / 10  # 假设10km/h配速
    return met * weight * hours


def calc_swimming_calories(duration_min=45, weight=70):
    """计算游泳消耗的卡路里"""
    # 游泳约6 MET
    met = 6
    hours = duration_min / 60
    return met * weight * hours


def estimate_distance(steps, stride_length=0.75):
    """估算行走距离"""
    return steps * stride_length / 1000  # km


def estimate_duration(steps, pace='moderate'):
    """估算运动时长（分钟）"""
    # 慢速 80步/分钟，中速 100步/分钟，快速 120步/分钟
    paces = {'slow': 80, 'moderate': 100, 'fast': 120}
    steps_per_min = paces.get(pace, 100)
    return steps / steps_per_min


def main():
    parser = argparse.ArgumentParser(description='计算运动卡路里消耗')
    parser.add_argument('--steps', '-s', type=int, default=0, help='步数')
    parser.add_argument('--weight', '-w', type=float, default=70, help='体重(kg)')
    parser.add_argument('--age', '-a', type=int, default=30, help='年龄')
    parser.add_argument('--duration', '-d', type=int, default=0, help='运动时长(分钟)')
    parser.add_argument('--distance', type=float, default=0, help='运动距离(km)')

    args = parser.parse_args()

    print("=" * 40)
    print("🔥 卡路里消耗计算")
    print("=" * 40)
    print(f"日期：{datetime.now().strftime('%Y-%m-%d')}")

    if args.steps > 0:
        distance = args.distance if args.distance > 0 else estimate_distance(args.steps)
        duration = args.duration if args.duration > 0 else estimate_duration(args.steps)

        step_cal = calc_step_calories(args.steps, args.weight)
        walking_cal = calc_walking_calories(distance, args.weight, duration)
        total_cal = step_cal + walking_cal

        print(f"\n📊 运动数据：")
        print(f"   步数：{args.steps:,}步")
        print(f"   距离：约{distance:.1f}km")
        print(f"   时长：约{duration:.0f}分钟")
        print(f"   体重：{args.weight}kg")

        print(f"\n🔥 卡路里消耗：")
        print(f"   步数消耗：约 {step_cal:.0f} 卡")
        print(f"   快走消耗：约 {walking_cal:.0f} 卡")
        print(f"   ─────────────────")
        print(f"   总计：约 {total_cal:.0f} 卡")

        # 有效减脂心率
        min_hr = int((220 - args.age) * 0.6)
        max_hr = int((220 - args.age) * 0.7)
        print(f"\n❤️ 有效减脂心率：{min_hr}-{max_hr} 次/分")

        print(f"\n💡 消耗参考：")
        print(f"   🍔 汉堡 ≈ 250-300 卡 ({total_cal/275:.1f}个)")
        print(f"   🥤 奶茶 ≈ 150-200 卡 ({total_cal/175:.1f}杯)")
        print(f"   🍎 苹果 ≈ 50-80 卡 ({total_cal/65:.1f}个)")

    elif args.duration > 0:
        # 仅根据时长计算（游泳等）
        swimming_cal = calc_swimming_calories(args.duration, args.weight)
        print(f"\n🏊 运动数据：")
        print(f"   时长：{args.duration}分钟")
        print(f"   体重：{args.weight}kg")
        print(f"\n🔥 游泳消耗：约 {swimming_cal:.0f} 卡")

    else:
        print("\n⚠️ 请输入步数或运动时长")
        print("示例：python calorie_calc.py --steps 10000 --weight 70")

    print("=" * 40)


if __name__ == "__main__":
    main()
