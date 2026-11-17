# -*- coding: utf-8 -*-
"""
generate.py — 生成选号方案(机选 / 热号 / 冷号 / 均衡) + 可选过滤缩水

用法:
  python generate.py --game ssq --count 5                 # 5 注随机机选
  python generate.py --game ssq --count 5 --strategy hot  # 热号优先
  python generate.py --game ssq --count 5 --strategy cold # 冷号/遗漏回补
  python generate.py --game dlt --count 3 --strategy balanced --odd-range 2,3 --sum-range 80,130
  python generate.py --game ssq --data ssq_history.json   # 用历史数据驱动热/冷策略

策略说明:
  random    纯随机机选(等价于投注站机选)
  hot       近期高频号加权(热号策略)
  cold      当前遗漏大者加权(冷号/遗漏回补策略)
  balanced  均匀随机 + 默认均衡过滤(奇偶/大小尽量平衡)

过滤(缩水)参数(可选):
  --odd-range a,b        奇数个数范围
  --big-range a,b        大号个数范围(以号码池中点划分)
  --sum-range a,b        和值范围(多号池取主池)
  --consec-range a,b     连号个数范围
  --prime-range a,b      质数个数范围

重要: 任何策略与过滤都不改变中奖概率, 仅用于个人偏好与研究。理性购彩, 量力而行。
依赖: 仅标准库 + lottery_core.py
"""

import argparse
import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lottery_core as core
import analyze as analyze_mod


def midpoint(lo, hi):
    return (lo + hi) / 2.0


def sample_pool(pconf, strategy, weights, allow_repeat, rng):
    lo, hi, count = pconf["min"], pconf["max"], pconf["count"]
    nums = list(range(lo, hi + 1))
    if allow_repeat:
        # 数字型(3D/排列/七星): 允许重复, 加权有放回
        pool = nums
        w = [max(weights.get(x, 1), 0.0001) for x in pool]
        return [rng.choices(pool, weights=w, k=1)[0] for _ in range(count)]
    else:
        # 无放回加权抽样
        chosen = []
        avail = nums[:]
        w = {x: max(weights.get(x, 1), 0.0001) for x in avail}
        for _ in range(count):
            ws = [w[x] for x in avail]
            x = rng.choices(avail, weights=ws, k=1)[0]
            chosen.append(x)
            avail.remove(x)
            del w[x]
        return chosen


def make_weights(game, pool_name, pconf, strategy, records, rng):
    lo, hi = pconf["min"], pconf["max"]
    weights = {x: 1.0 for x in range(lo, hi + 1)}
    if strategy in ("hot", "cold") and records:
        st = analyze_mod.analyze_pool(records, pool_name, pconf, window=30)
        if strategy == "hot":
            for x in weights:
                weights[x] = st["recent_freq"].get(x, 0) + 1
        else:  # cold -> 遗漏回补
            for x in weights:
                weights[x] = st["current_missing"].get(x, 0) + 1
    return weights


def passes_filters(nums, pconf, filt):
    lo, hi = pconf["min"], pconf["max"]
    if not nums:
        return False
    odd = sum(1 for x in nums if x % 2 == 1)
    big = sum(1 for x in nums if x > midpoint(lo, hi))
    s = sum(nums)
    cons = sum(1 for j in range(1, len(nums)) if nums[j] - nums[j - 1] == 1)
    pr = sum(1 for x in nums if core_prime(x))
    if filt["odd"]:
        if not (filt["odd"][0] <= odd <= filt["odd"][1]):
            return False
    if filt["big"]:
        if not (filt["big"][0] <= big <= filt["big"][1]):
            return False
    if filt["sum"]:
        if not (filt["sum"][0] <= s <= filt["sum"][1]):
            return False
    if filt["consec"]:
        if not (filt["consec"][0] <= cons <= filt["consec"][1]):
            return False
    if filt["prime"]:
        if not (filt["prime"][0] <= pr <= filt["prime"][1]):
            return False
    return True


def core_prime(n):
    if n < 2:
        return False
    import math
    if n % 2 == 0:
        return n == 2
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def generate_sets(game, n_sets, strategy, records, filt, seed):
    rng = random.Random(seed)
    cfg = core.GAME_CONFIG[game]
    results = []
    max_tries = n_sets * 200 + 1000
    tries = 0
    while len(results) < n_sets and tries < max_tries:
        tries += 1
        combo = {}
        ok = True
        for pname, pconf in cfg["pools"].items():
            allow_repeat = (pconf["min"] == 0 and pconf["max"] <= 9)
            weights = make_weights(game, pname, pconf, strategy, records, rng)
            pick = sorted(sample_pool(pconf, strategy, weights, allow_repeat, rng))
            if not passes_filters(pick, pconf, filt):
                ok = False
                break
            combo[pname] = pick
        if ok:
            results.append(combo)
    return results


def fmt_combo(game, combo):
    cfg = core.GAME_CONFIG[game]
    parts = []
    for pname in cfg["pools"]:
        nums = combo[pname]
        if game == "ssq" and pname == "red":
            parts.append("红球 " + " ".join("%02d" % x for x in nums))
        elif game == "ssq" and pname == "blue":
            parts.append("蓝球 " + " ".join("%02d" % x for x in nums))
        elif game == "dlt" and pname == "front":
            parts.append("前区 " + " ".join("%02d" % x for x in nums))
        elif game == "dlt" and pname == "back":
            parts.append("后区 " + " ".join("%02d" % x for x in nums))
        else:
            parts.append(pname + " " + " ".join(str(x) for x in nums))
    return "  |  ".join(parts)


def main():
    ap = argparse.ArgumentParser(description="彩票选号生成")
    ap.add_argument("--game", default="ssq")
    ap.add_argument("--count", type=int, default=5, help="生成注数")
    ap.add_argument("--strategy", default="random", choices=["random", "hot", "cold", "balanced"])
    ap.add_argument("--data", default=None, help="历史数据(驱动 hot/cold 策略)")
    ap.add_argument("--odd-range", default=None, help="奇数个数范围, 如 2,4")
    ap.add_argument("--big-range", default=None, help="大号个数范围, 如 2,4")
    ap.add_argument("--sum-range", default=None, help="和值范围, 如 80,130")
    ap.add_argument("--consec-range", default=None, help="连号个数范围, 如 0,2")
    ap.add_argument("--prime-range", default=None, help="质数个数范围, 如 1,3")
    ap.add_argument("--seed", type=int, default=None, help="随机种子(可复现)")
    args = ap.parse_args()

    game = core.resolve_game(args.game)
    cfg = core.GAME_CONFIG[game]

    records = []
    if args.data:
        data = core.load_normalized(args.data)
        if data.get("game") and core.resolve_game(data["game"]) == game:
            records = data["records"]
        else:
            records = data["records"]

    filt = {"odd": None, "big": None, "sum": None, "consec": None, "prime": None}
    for key, val in (("odd", args.odd_range), ("big", args.big_range),
                     ("sum", args.sum_range), ("consec", args.consec_range),
                     ("prime", args.prime_range)):
        if val:
            a, b = val.split(",")
            filt[key] = (int(a), int(b))

    strategy = args.strategy
    if strategy == "balanced":
        # 均衡默认过滤: 奇偶、大小尽量居中
        for pname, pconf in cfg["pools"].items():
            c = pconf["count"]
            if filt["odd"] is None:
                filt["odd"] = (c // 2, (c + 1) // 2)
            if filt["big"] is None:
                filt["big"] = (c // 2, (c + 1) // 2)

    sets = generate_sets(game, args.count, strategy, records, filt, args.seed)

    print("=" * 60)
    print("%s (%s) 选号生成 — 策略: %s" % (cfg["name"], game, strategy))
    if any(filt.values()):
        print("过滤条件: " + ", ".join(
            "%s=%s" % (k, filt[k]) for k in filt if filt[k]))
    print("=" * 60)
    if not sets:
        print("未能在重试上限内生成满足过滤条件的组合, 请放宽过滤范围。")
    for i, combo in enumerate(sets, 1):
        print("第%02d注: %s" % (i, fmt_combo(game, combo)))
    print("")
    print("⚠️ 理性提醒: 所有选号均为随机/偏好生成, 不提升中奖概率。量力购彩, 仅供参考。")


if __name__ == "__main__":
    main()
