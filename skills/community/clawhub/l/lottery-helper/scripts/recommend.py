"""
lottery-helper/scripts/recommend.py
多因子蒙特卡洛彩票推荐算法
"""
import sys, os, random

# 让 query.py 可被 import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import query as q

# 强制 stdout 为 UTF-8，避免 Windows cp1252 控制台报错
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# 各彩种配置
THEORY = {
    "ssq":  {"balls": 33, "pick": 6, "bonus": 16, "pick_bonus": 1, "name": "双色球",    "size_ratio": 16},
    "dlt":  {"balls": 35, "pick": 5, "bonus": 12, "pick_bonus": 2, "name": "大乐透",    "size_ratio": 18},
    "pl3":  {"balls": 10, "pick": 3, "bonus": 0,  "pick_bonus": 0, "name": "排列三",    "size_ratio": 5},
    "pl5":  {"balls": 10, "pick": 5, "bonus": 0,  "pick_bonus": 0, "name": "排列五",    "size_ratio": 5},
    "3d": {"balls": 10, "pick": 3, "bonus": 0,  "pick_bonus": 0, "name": "福彩3D",    "size_ratio": 5},
    "kl8":  {"balls": 80, "pick": 20, "bonus": 0, "pick_bonus": 0, "name": "北京快乐8",  "size_ratio": 40},
    "qlc":  {"balls": 30, "pick": 7, "bonus": 0,  "pick_bonus": 0, "name": "七乐彩",    "size_ratio": 15},
    "qxc":  {"balls": 10, "pick": 7, "bonus": 0,  "pick_bonus": 0, "name": "七星彩",    "size_ratio": 5},
}


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def _main(code, parts):
    """提取主号码（不含附加号）。"""
    p = parts
    if code == "ssq":  return sorted([int(p[i]) for i in range(2, 8)])
    if code == "dlt":  return sorted([int(p[i]) for i in range(2, 7)])
    if code in ("pl3", "3d"): return [int(p[2]), int(p[3]), int(p[4])]
    if code == "pl5":  return [int(p[i]) for i in range(2, 7)]
    if code == "kl8":  return sorted([int(p[i]) for i in range(2, 22)])
    if code == "qlc":  return sorted([int(p[i]) for i in range(2, 9)])
    if code == "qxc":  return [int(p[i]) for i in range(2, 9)]
    return []


def _bonus(code, parts):
    """提取附加号码（蓝球/后区）。"""
    p = parts
    if code == "ssq":  return [int(p[8])]
    if code == "dlt":  return sorted([int(p[7]), int(p[8])])
    return []


def _stats(lines, code):
    """
    从历史数据计算各项统计。
    返回: (freq_main, freq_bonus, pos_ranges, prev_main)
    """
    cfg = THEORY[code]
    n_main, n_bonus = cfg["balls"], cfg.get("bonus", 0)

    freq_main = {i: 0 for i in range(1, n_main + 1)}
    freq_bonus = {i: 0 for i in range(1, n_bonus + 1)} if n_bonus > 0 else {}

    prev_main = []
    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) < 9:
            continue
        nums = _main(code, parts)
        for n in nums:
            if 1 <= n <= n_main:
                freq_main[n] += 1
        if idx == len(lines) - 1:
            prev_main = nums
        for n in _bonus(code, parts):
            if 1 <= n <= n_bonus:
                freq_bonus[n] += 1

    # 位置范围统计（仅 ssq/dlt）
    pos_ranges = {}
    if code in ("ssq", "dlt"):
        n_pos = cfg["pick"]
        for pos in range(n_pos):
            vals = []
            for line in lines:
                p = line.strip().split()
                if len(p) < 9:
                    continue
                nums = _main(code, p)
                if len(nums) > pos:
                    vals.append(nums[pos])
            if vals:
                s = sorted(vals)
                lo = s[max(0, int(len(s) * 0.05))]
                hi = s[min(len(s) - 1, int(len(s) * 0.95))]
                pos_ranges[pos] = (lo, hi)

    return freq_main, freq_bonus, pos_ranges, prev_main


def _hot_cold(freq):
    """将号码分为热/温/冷三类。返回 (hot_set, warm_set, cold_set)。"""
    total = sum(freq.values())
    if total == 0:
        return set(), set(), set()
    items = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    n = len(items)
    h = max(1, int(n * 0.35))
    w = max(1, int(n * 0.35))
    return ({i for i, _ in items[:h]},
            {i for i, _ in items[h:h + w]},
            {i for i, _ in items[h + w:]})


def _valid(combo, code, cfg, prev):
    """硬过滤：判断组合是否满足基本均衡约束。返回 True=通过。"""
    combo = sorted(combo)
    sz = cfg["size_ratio"]

    # 大小比过滤（仅 ssq/dlt）
    if code in ("ssq", "dlt"):
        big = sum(1 for x in combo if x > sz)
        if big == 0 or big == len(combo):
            return False

    # 和值过滤
    s = sum(combo)
    if code == "ssq" and not (60 <= s <= 110):
        return False
    if code == "dlt" and not (60 <= s <= 90):
        return False

    # 重复过滤：与上期重号过多则淘汰
    if prev:
        reps = len(set(combo) & set(prev))
        if reps > 4:
            return False

    return True


def _score(combo, freq, hot, warm, cold, pos_ranges, cfg, code, prev):
    """给一组号码打分（越高越好）。"""
    s = 0.0

    # 1. 频率得分（热号权重最高）
    mx = max(freq.values()) if freq else 1
    for num in combo:
        f = freq.get(num, 0) / mx
        s += (4.0 if num in hot else 2.5 if num in warm else 1.0) * f

    # 2. 位置合规得分（仅 ssq/dlt）
    for pos, (lo, hi) in pos_ranges.items():
        if pos < len(combo) and lo <= combo[pos] <= hi:
            s += 1.5

    # 3. 奇偶平衡得分
    odd = sum(1 for x in combo if x % 2 == 1)
    best = len(combo) // 2
    s += max(0, 1.0 - abs(odd - best) * 0.4)

    # 4. 和值得分
    if code in ("ssq", "dlt"):
        target = 85 if code == "ssq" else 75
        s += max(0, 2.0 - abs(sum(combo) - target) * 0.03)

    # 5. 号码分散得分
    ranges_count = len({1 if x <= cfg["balls"] // 3 else 2 if x <= 2 * cfg["balls"] // 3 else 3 for x in combo})
    s += ranges_count * 0.5

    return s


def _pick_mix(pool, n, hot, warm, cold, used):
    """按热/温/冷比例随机抽取 n 个不重复号码。"""
    by_type = {0: [x for x in pool if x in hot],
               1: [x for x in pool if x in warm],
               2: [x for x in pool if x in cold]}
    quotas = {0: int(n * 0.40), 1: int(n * 0.30), 2: n - int(n * 0.40) - int(n * 0.30)}
    result, used = list(used), set(used)
    for typ in [0, 1, 2]:
        avail = [x for x in by_type[typ] if x not in used]
        chosen = random.sample(avail, min(quotas[typ], len(avail)))
        result.extend(chosen)
        used.update(chosen)
        if len(result) >= n:
            break
    while len(result) < n:
        avail = [x for x in pool if x not in used]
        if not avail:
            break
        x = random.choice(avail)
        result.append(x)
        used.add(x)
    return sorted(result[:n])


# ---------------------------------------------------------------------------
# 对外接口
# ---------------------------------------------------------------------------

def recommend(code):
    """
    基于多因子蒙特卡洛策略生成推荐号码。
    返回: (主号列表, 分析dict(含"_bonus"/"_alternatives"/"_stats"), 错误信息)
    """
    cfg = THEORY.get(code)
    if not cfg:
        return [], {}, f"未知彩种: {code}"

    try:
        lines = q.fetch_raw(code, "asc")
    except Exception as e:
        return [], {}, f"获取数据失败: {e}"

    if len(lines) < 30:
        return [], {}, "历史数据不足30期，无法分析"

    freq_main, freq_bonus, pos_ranges, prev = _stats(lines, code)
    hot, warm, cold = _hot_cold(freq_main)
    n, n_bonus, pool_sz = cfg["pick"], cfg.get("pick_bonus", 0), cfg["balls"]
    all_nums = list(range(1, pool_sz + 1))

    # 蒙特卡洛采样（30000组候选）
    candidates = []
    for _ in range(30000):
        for combo in [
            _pick_mix(all_nums, n, hot, warm, cold, set()),
            sorted(random.sample(all_nums, n)),
        ]:
            if len(set(combo)) < n:
                continue
            if not _valid(combo, code, cfg, prev):
                continue
            sc = _score(combo, freq_main, hot, warm, cold, pos_ranges, cfg, code, prev)
            candidates.append((combo, sc))

    if not candidates:
        candidates = [(sorted(random.sample(all_nums, n)), 0) for _ in range(100)]

    candidates.sort(key=lambda x: x[1], reverse=True)
    top = [c[0] for c in candidates[:20]]
    final = top[0]

    # 构建分析数据
    total = sum(freq_main.values())
    recent_n = min(100, len(lines))
    analysis = {}
    for num in final:
        f = freq_main.get(num, 0)
        rate = f / total if total > 0 else 0
        category = "热号" if num in hot else ("温号" if num in warm else "冷号")
        analysis[num] = {
            "类型": category,
            "历史出现率": "{:.2%}".format(rate),
            "近100期": "{:.0f}次".format(f * recent_n / total if total > 0 else 0),
        }

    # 附加号（蓝球/后区）
    bonus_rec = []
    if n_bonus > 0:
        hb, wb, cb = _hot_cold(freq_bonus)
        bs = {}
        for num, cnt in freq_bonus.items():
            bs[num] = cnt * (3 if num in hb else 2 if num in wb else 1)
        bonus_rec = sorted(bs, key=bs.get, reverse=True)[:n_bonus]
        analysis["_bonus"] = bonus_rec
        for num in bonus_rec:
            f = freq_bonus.get(num, 0)
            r = f / sum(freq_bonus.values()) if freq_bonus else 0
            cat = "热号" if num in hb else ("温号" if num in wb else "冷号")
            analysis[num + 9000] = {"类型": cat, "历史出现率": "{:.2%}".format(r),
                                    "近100期": "{:.0f}次".format(f * recent_n / sum(freq_bonus.values()) if freq_bonus else 0)}

    # 备选方案
    alts = [c for c in top[1:] if c != final][:2]
    analysis["_alternatives"] = alts
    analysis["_stats"] = {
        "hot_count": len(hot), "warm_count": len(warm),
        "cold_count": len(cold), "total_draws": len(lines),
    }

    return final, analysis, None


def backtest(code, n_periods=200):
    """
    回测最近 n_periods 期的命中率。
    返回: {"avg_hits": float, "jackpot": int, "periods": int, "dist": dict}
    """
    cfg = THEORY.get(code)
    if not cfg:
        return {"avg_hits": 0, "jackpot": 0, "periods": 0, "dist": {}}

    try:
        lines = q.fetch_raw(code, "asc")
    except Exception:
        return {"avg_hits": 0, "jackpot": 0, "periods": 0, "dist": {}}

    max_test = min(n_periods, len(lines) - 5)
    if max_test < 10:
        return {"avg_hits": 0, "jackpot": 0, "periods": 0, "dist": {}}

    results = []
    for i in range(max_test):
        train = lines[:-(i + 1)]
        if len(train) < 30:
            continue
        freq, _, pos_rng, prev = _stats(train, code)
        h, w, c = _hot_cold(freq)
        pool = list(range(1, cfg["balls"] + 1))

        best_combo, best_sc = None, -999
        for _ in range(5000):
            combo = _pick_mix(pool, cfg["pick"], h, w, c, set())
            if len(set(combo)) < cfg["pick"] or not _valid(combo, code, cfg, prev):
                continue
            sc = _score(combo, freq, h, w, c, pos_rng, cfg, code, prev)
            if sc > best_sc:
                best_sc, best_combo = sc, combo

        if best_combo is None:
            best_combo = sorted(random.sample(pool, cfg["pick"]))

        actual = set(_main(code, lines[-(i + 1)].strip().split()))
        results.append(len(set(best_combo) & actual))

    dist = {h: results.count(h) for h in sorted(set(results))}
    return {
        "avg_hits": sum(results) / len(results) if results else 0,
        "jackpot": sum(1 for h in results if h == cfg["pick"]),
        "periods": len(results),
        "dist": dist,
    }


def format_recommendation(code, combo, analysis, bt_result=None):
    """将推荐结果格式化为友好文本（用于 CLI 输出）。"""
    cfg = THEORY[code]
    name, pick = cfg["name"], cfg["pick"]
    bonus = analysis.get("_bonus", [])
    alts = analysis.get("_alternatives", [])
    stats = analysis.get("_stats", {})

    labels = {"dlt": ("前区", "后区"), "ssq": ("红球", "蓝球")}
    main_lbl, bonus_lbl = labels.get(code, ("主号码", "附加号"))

    lines = []
    lines.append("")
    lines.append("=" * 52)
    lines.append(f"  [{name}] 多因子蒙特卡洛推荐")
    lines.append("=" * 52)
    lines.append(f"  {main_lbl}: " + " ".join(str(n).zfill(2) for n in combo))
    if bonus:
        lines.append(f"  {bonus_lbl}: " + " ".join(str(n).zfill(2) for n in bonus))
    lines.append("")
    lines.append("  号码分析（热/温/冷分类 + 位置区间 + 均衡约束）:")

    for num in combo:
        info = analysis.get(num, {})
        if info:
            cat = info.get("类型", "?")
            icon = {"热号": "HOT ", "温号": "WARM", "冷号": "COLD"}.get(cat, "    ")
            lines.append(f"    {icon} {str(num).zfill(2)}: 历史{info.get('历史出现率','?')} | 近100期{info.get('近100期','?')} | {cat}")

    if bonus:
        for num in bonus:
            info = analysis.get(num + 9000, {})
            if info:
                lines.append(f"    [{bonus_lbl}] {str(num).zfill(2)}: 历史{info.get('历史出现率','?')} | 近100期{info.get('近100期','?')} | {info.get('类型','?')}")

    if alts:
        lines.append("")
        lines.append("  其他备选组合:")
        for a in alts:
            lines.append("    " + " ".join(str(n).zfill(2) for n in a))

    if stats:
        lines.append("")
        lines.append(f"  热冷温: 热号{stats.get('hot_count',0)}个 / 温号{stats.get('warm_count',0)}个 / 冷号{stats.get('cold_count',0)}个（总样本{stats.get('total_draws',0)}期）")

    if bt_result:
        lbl = "前区" if code == "dlt" else main_lbl
        lines.append("")
        lines.append(f"  历史回测 (近{bt_result['periods']}期):")
        lines.append(f"    均命中{lbl}数: {bt_result['avg_hits']:.2f} / {pick}")
        lines.append(f"    理论均值: {pick * pick / cfg['balls']:.2f}")
        lines.append(f"    头奖(全中)次数: {bt_result['jackpot']}")
        lines.append(f"    命中分布: {bt_result['dist']}")

    lines.append("")
    lines.append("=" * 52)
    lines.append("  [免责声明]")
    lines.append("  彩票为物理独立随机事件，历史数据无法预测未来开奖。")
    lines.append("  本推荐仅供娱乐参考，不构成购彩建议。理性购彩，量力而行。")
    lines.append("=" * 52)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="彩票推荐 - 多因子蒙特卡洛策略")
    parser.add_argument("--codes", required=True, help="彩种代码，逗号分隔（必填）")
    parser.add_argument("--backtest", action="store_true",
                        help="是否运行历史回测（默认关闭，运行约需1~2分钟）")
    parser.add_argument("--recent", type=int, default=200,
                        help="回测期数，默认200（仅在 --backtest 时生效）")
    args = parser.parse_args()

    for code in args.codes.split(","):
        code = code.strip()
        if not code:
            continue
        combo, analysis, err = recommend(code)
        if err:
            print(f"[{code}] ERROR: {err}")
            continue
        bt = backtest(code, n_periods=args.recent) if args.backtest else None
        print(format_recommendation(code, combo, analysis, bt))
