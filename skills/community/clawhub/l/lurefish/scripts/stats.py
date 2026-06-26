#!/usr/bin/env python3
"""
渔获统计脚本 - 分析钓鱼数据

用法:
  python stats.py              # 完整统计
  python stats.py --month 3    # 指定月份
  python stats.py --top 5      # TOP 5 钓点/饵
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import Counter

DATA_DIR = Path.home() / "lurefish"
CATCHES_FILE = DATA_DIR / "catches.json"


def load_catches():
    """加载渔获记录"""
    if not CATCHES_FILE.exists():
        return []
    return json.loads(CATCHES_FILE.read_text(encoding="utf-8"))


def stats_summary(catches, top_n=5):
    """生成统计摘要"""
    if not catches:
        print("📭 暂无渔获记录")
        return

    total = len(catches)
    total_weight = sum(c.get("weight", 0) or 0 for c in catches)
    total_length = sum(c.get("length", 0) or 0 for c in catches)

    # 鱼种统计
    species_count = Counter(c["species"] for c in catches if c.get("species"))

    # 用饵统计
    lure_count = Counter(c.get("lure") for c in catches if c.get("lure"))

    # 钓点统计
    location_count = Counter(c.get("location") for c in catches if c.get("location"))

    # 时段统计
    hour_count = Counter()
    for c in catches:
        if c.get("time"):
            try:
                hour = int(c["time"].split(":")[0])
                hour_count[hour] += 1
            except:
                pass

    # 日期统计
    date_count = Counter(c["date"] for c in catches if c.get("date"))

    print("🎣 渔获统计")
    print("=" * 40)
    print(f"📊 总渔获: {total} 条")
    print(f"⚖️  总重量: {total_weight:.2f} kg")
    print(f"📏 总长度: {total_length:.0f} cm")
    print(f"📅 出钓天数: {len(date_count)} 天")
    print()

    print(f"🐟 鱼种 TOP {top_n}:")
    for species, count in species_count.most_common(top_n):
        pct = count / total * 100
        print(f"   {species}: {count} 条 ({pct:.1f}%)")

    print()
    print(f"🎣 用饵 TOP {top_n}:")
    for lure, count in lure_count.most_common(top_n):
        pct = count / total * 100
        print(f"   {lure}: {count} 条 ({pct:.1f}%)")

    print()
    print(f"📍 钓点 TOP {top_n}:")
    for loc, count in location_count.most_common(top_n):
        pct = count / total * 100
        print(f"   {loc}: {count} 条 ({pct:.1f}%)")

    if hour_count:
        print()
        print("⏰ 高产时段:")
        for hour, count in hour_count.most_common(5):
            print(f"   {hour:02d}:00-{hour+1:02d}:00: {count} 条")


def stats_by_month(catches, month):
    """按月份统计"""
    month_str = f"-{month:02d}-"
    month_catches = [c for c in catches if month_str in c.get("date", "")]
    print(f"📅 {month} 月统计\n")
    stats_summary(month_catches)


def main():
    parser = argparse.ArgumentParser(description="渔获统计")
    parser.add_argument("--month", "-m", type=int, help="指定月份 (1-12)")
    parser.add_argument("--top", "-t", type=int, default=5, help="TOP N")
    parser.add_argument("--year", "-y", type=int, help="指定年份")
    parser.add_argument("--export", "-e", help="导出报告到文件")

    args = parser.parse_args()

    catches = load_catches()

    if args.year:
        year_str = str(args.year)
        catches = [c for c in catches if c.get("date", "").startswith(year_str)]

    if args.month:
        stats_by_month(catches, args.month)
    else:
        stats_summary(catches, args.top)


if __name__ == "__main__":
    main()
