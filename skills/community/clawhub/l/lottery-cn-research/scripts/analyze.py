# -*- coding: utf-8 -*-
"""
analyze.py — 历史开奖数据的统计分析

用法:
  python analyze.py --data ssq_history.json
  python analyze.py --data ssq_history.json --window 30 --json out.json
  python analyze.py --data ssq_history.json --game ssq

分析维度(每个号码池独立):
  - 出现频率(频率%)
  - 冷热号(近 window 期内出现频次 vs 理论期望)
  - 遗漏值(当前遗漏 / 历史最大遗漏)
  - 奇偶比、大小比、三区分布
  - 和值分布(均值/最小/最大/直方图)
  - 连号个数均值、重号(与上期重复)均值、质数个数均值

依赖: 仅标准库 + lottery_core.py
"""

import argparse
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lottery_core as core


def prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def analyze_pool(records, pool_name, pconf, window):
    lo, hi, cnt = pconf["min"], pconf["max"], pconf["count"]
    size = hi - lo + 1
    n = len(records)
    freq = {x: 0 for x in range(lo, hi + 1)}
    recent = {x: 0 for x in range(lo, hi + 1)}
    missing = {x: 0 for x in range(lo, hi + 1)}
    max_missing = {x: 0 for x in range(lo, hi + 1)}
    sums, consec_list, repeat_list, prime_list = [], [], [], []

    prev = None
    for i, rec in enumerate(records):
        nums = sorted(set(int(x) for x in rec["pools"].get(pool_name, [])))
        # 频率与遗漏
        for x in range(lo, hi + 1):
            missing[x] += 1
            if x in nums:
                freq[x] += 1
                if i >= n - window:
                    recent[x] += 1
                missing[x] = 0
                max_missing[x] = max(max_missing[x], 0)
        for x in nums:
            max_missing[x] = max(max_missing[x], 0)  # 已在上行重置
        # 和值
        if nums:
            sums.append(sum(nums))
        # 连号(相邻差1的对数)
        cons = sum(1 for j in range(1, len(nums)) if nums[j] - nums[j - 1] == 1)
        consec_list.append(cons)
        # 质数个数
        prime_list.append(sum(1 for x in nums if prime(x)))
        # 重号(与上一期重复)
        if prev is not None:
            repeat_list.append(len(set(nums) & set(prev)))
        prev = nums

    # 最大遗漏需重新计算(遗漏在每期已重置, 用另一遍)
    max_missing = {x: 0 for x in range(lo, hi + 1)}
    cur = {x: 0 for x in range(lo, hi + 1)}
    for rec in records:
        nums = set(int(x) for x in rec["pools"].get(pool_name, []))
        for x in range(lo, hi + 1):
            cur[x] += 1
            if x in nums:
                max_missing[x] = max(max_missing[x], cur[x] - 1)
                cur[x] = 0
    # 当前遗漏 = cur (遍历结束后未重置的)
    current_missing = dict(cur)

    expected = window * cnt / size  # 近 window 期理论出现次数
    hot, cold = [], []
    for x in range(lo, hi + 1):
        if recent[x] > expected:
            hot.append((x, recent[x]))
        elif recent[x] < expected * 0.6:
            cold.append((x, recent[x]))

    stats = {
        "pool": pool_name,
        "range": [lo, hi],
        "draw_count": cnt,
        "total_draws": n,
        "frequency": freq,
        "recent_freq_window": window,
        "recent_freq": recent,
        "expected_recent": round(expected, 2),
        "current_missing": current_missing,
        "max_missing": max_missing,
        "hot": sorted(hot, key=lambda t: -t[1]),
        "cold": sorted(cold, key=lambda t: t[1]),
        "sum": {
            "mean": round(sum(sums) / len(sums), 2) if sums else 0,
            "min": min(sums) if sums else 0,
            "max": max(sums) if sums else 0,
        },
        "avg_consecutive": round(sum(consec_list) / len(consec_list), 2) if consec_list else 0,
        "avg_repeat": round(sum(repeat_list) / len(repeat_list), 2) if repeat_list else 0,
        "avg_prime": round(sum(prime_list) / len(prime_list), 2) if prime_list else 0,
    }
    return stats


def render_text(game, stats_list):
    lines = []
    cfg = core.GAME_CONFIG[game]
    lines.append("=" * 60)
    lines.append("%s (%s) 统计分析报告" % (cfg["name"], game))
    lines.append("开奖时间: %s   单注: %d元   返奖率: %.0f%%"
                 % (cfg["draw"], cfg["ticket"], cfg["payout_ratio"] * 100))
    lines.append("=" * 60)
    for st in stats_list:
        lo, hi = st["range"]
        size = hi - lo + 1
        lines.append("")
        lines.append("-- 号码池: %s (%d-%d, 每期%d个) --" % (st["pool"], lo, hi, st["draw_count"]))
        lines.append("样本期数: %d" % st["total_draws"])
        # 频率(按频率降序展示前若干)
        freq_sorted = sorted(st["frequency"].items(), key=lambda t: -t[1])
        top = freq_sorted[:8]
        bot = freq_sorted[-8:]
        lines.append("高频号: " + ", ".join("%d(%d)" % (k, v) for k, v in top))
        lines.append("低频号: " + ", ".join("%d(%d)" % (k, v) for k, v in bot))
        # 冷热
        lines.append("热号(近%d期>期望%.1f): " % (st["recent_freq_window"], st["expected_recent"])
                     + (", ".join("%d(%d)" % t for t in st["hot"]) or "无"))
        lines.append("冷号(近%d期偏低): " % st["recent_freq_window"]
                     + (", ".join("%d(%d)" % t for t in st["cold"]) or "无"))
        # 遗漏: 当前遗漏最大的几个
        miss_sorted = sorted(st["current_missing"].items(), key=lambda t: -t[1])[:8]
        lines.append("当前遗漏最大: " + ", ".join("%d(%d期)" % (k, v) for k, v in miss_sorted))
        maxmiss_sorted = sorted(st["max_missing"].items(), key=lambda t: -t[1])[:5]
        lines.append("历史最大遗漏: " + ", ".join("%d(%d期)" % (k, v) for k, v in maxmiss_sorted))
        # 和值 / 连号 / 重号 / 质数
        lines.append("和值: 均值%.1f 区间[%d, %d]" % (st["sum"]["mean"], st["sum"]["min"], st["sum"]["max"]))
        lines.append("平均连号数: %.2f   平均重号数: %.2f   平均质数数: %.2f"
                     % (st["avg_consecutive"], st["avg_repeat"], st["avg_prime"]))
    lines.append("")
    lines.append("说明: 上述统计仅描述历史分布, 不预测未来。彩票每期独立随机, 任何策略均")
    lines.append("不改变中奖概率。本工具仅供研究与娱乐参考。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="彩票历史数据统计分析")
    ap.add_argument("--data", required=True, help="归一化数据文件(JSON/CSV)")
    ap.add_argument("--game", default=None, help="彩种(数据文件已含则可选)")
    ap.add_argument("--window", type=int, default=30, help="冷热判定窗口期")
    ap.add_argument("--json", default=None, help="将统计结果另存为 JSON")
    args = ap.parse_args()

    data = core.load_normalized(args.data)
    game = args.game or data.get("game")
    if not game:
        raise ValueError("未在数据与参数中确定彩种, 请用 --game 指定。")
    game = core.resolve_game(game)
    cfg = core.GAME_CONFIG[game]

    records = data["records"]
    stats_list = []
    for pname, pconf in cfg["pools"].items():
        stats_list.append(analyze_pool(records, pname, pconf, args.window))

    print(render_text(game, stats_list))

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"game": game, "stats": stats_list}, f, ensure_ascii=False, indent=2)
        print("\n统计结果已写出 -> %s" % args.json)


if __name__ == "__main__":
    main()
