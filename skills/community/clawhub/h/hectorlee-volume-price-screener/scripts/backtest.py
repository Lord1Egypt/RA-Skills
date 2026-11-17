#!/usr/bin/env python3
"""
V2 历史回测引擎 - 验证形态超额收益
=====================================
逐日滚动扫描：对每只股票，把每个历史交易日当作"当前日"，
用截至该日的 K 线运行形态识别，命中后记录 5/10/20 日收益率。

输出:
  1. 命中统计: 命中数、日均命中率
  2. 收益统计: 命中后 5/10/20 日平均收益、胜率、盈亏比
  3. 超额收益: 命中股收益 - 沪深300 同期收益（alpha）
  4. 随机对照: 同数量随机"伪命中"收益 → 显著性对比
  5. 训练样本导出: 每命中样本的特征 + 未来收益（供 ML 模型使用）

用法:
  python backtest.py --sample 500            # 抽样500只快速回测
  python backtest.py --all                    # 全市场回测
  python backtest.py --days 250               # 回测最近1年（默认3年）
  python backtest.py --export data/ml_samples.jsonl   # 导出ML训练样本
  python backtest.py --sample 500 --horizons 5,10,20
"""

import argparse
import json
import math
import os
import random
import sys
import time
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pattern_detect import detect_from_klines, DEFAULT_PARAMS
from scoring import score_pattern
from risk_filter import comprehensive_filter
from data_provider import get_all_stocks, fetch_klines_batch

INDEX_CODE = "sh000300"   # 沪深300
INDEX_NAME = "沪深300"
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "kline_cache.pkl")


# ============================================================
# 数据
# ============================================================

def load_kline_history(codes: List[str], days: int = 750, workers: int = 14,
                       use_cache: bool = True) -> Dict[str, Optional[List[dict]]]:
    """拉取历史K线（近 days 个交易日），支持本地缓存"""
    cache_path = os.path.abspath(CACHE_FILE)
    cache: Dict[str, Optional[List[dict]]] = {}
    if use_cache and os.path.exists(cache_path):
        try:
            import pickle
            with open(cache_path, "rb") as f:
                cache = pickle.load(f)
            print(f"[回测] 命中K线缓存（{len(cache)}只），跳过网络拉取")
        except Exception:
            cache = {}

    missing = [c for c in codes if c not in cache or not cache.get(c)]
    if missing:
        print(f"[回测] 拉取 {len(missing)} 只股票K线（{days}根）...")
        t0 = time.time()
        fetched = fetch_klines_batch(missing, count=days, workers=workers)
        cache.update(fetched)
        print(f"[回测] 数据拉取完成 {time.time()-t0:.1f}s"
              f"（成功 {sum(1 for v in fetched.values() if v)}/{len(fetched)}）")
        # 保存缓存
        try:
            import pickle
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "wb") as f:
                pickle.dump(cache, f)
            print(f"[回测] K线缓存已保存: {cache_path}")
        except Exception as e:
            print(f"[回测] 缓存保存失败: {e}")
    return {c: cache.get(c) for c in codes}


# ============================================================
# 滚动扫描
# ============================================================

def scan_stock(code: str, name: str, klines: List[dict], params: dict,
               min_hist: int = 90, forward_days: List[int] = (5, 10, 20),
               max_records: Optional[int] = None) -> List[dict]:
    """对单只股票做逐日滚动扫描

    把每个 t 当作"当前日"，用 klines[:t+1] 检测形态（t 即窗口末）。
    命中后计算 forward_days 的收益率（使用全量序列后续K线）。

    性能优化：一次性构建 Bar 列表，每次只传最近 ~90 根，避免重复转换。
    """
    from pattern_detect import detect_pattern, Bar
    bars = [_bar(k) for k in klines]
    n = len(bars)
    records = []
    for t in range(min_hist, n - max(forward_days)):
        # 只传最近 min(90, t+1) 根，检测窗口固定为最后20日
        window = bars[max(0, t + 1 - 90): t + 1]
        result = detect_pattern(window, code=code, params=params)
        if result is None:
            continue
        # 风险过滤（锚点索引相对于 window）
        excluded, reason, _ = comprehensive_filter(
            code, name, window, result.anchor_idx, params=params)
        if excluded:
            continue

        rec = {
            "code": code, "name": name,
            "date": klines[t]["date"],
            "anchor_date": result.anchor_date,
            "surge_pct": round(result.surge_pct, 3),
            "volume_ratio": round(result.volume_ratio, 3),
            "shrink_days": result.shrink_days,
            "shrink_depth": round(result.shrink_depth, 3),
            "amplitude": round(result.amplitude, 3),
            "range_position": result.range_position,
            "pullback_ratio": round(result.pullback_ratio, 3),
            "low_point_rise": result.low_point_rise,
            "breakout_60d": result.breakout_60d,
            "ma_support": result.ma_support,
            "vol_ma_bull": result.vol_ma_bull,
            "conc_rise_3d": result.conc_rise_3d,
            "conc_fall_3d": result.conc_fall_3d,
            "divergence_warning": result.divergence_warning,
            "score": score_pattern(result, params).total,
        }
        # 未来收益
        base_close = klines[t]["close"]
        if base_close <= 0:
            continue
        for fd in forward_days:
            if t + fd < n and klines[t + fd]["close"] > 0:
                rec[f"fwd{fd}"] = round((klines[t + fd]["close"] / base_close - 1) * 100, 3)
        records.append(rec)
        if max_records and len(records) >= max_records:
            break
    return records


def _bar(k: dict):
    from pattern_detect import Bar
    return Bar(date=k["date"], open=float(k["open"]), high=float(k["high"]),
               low=float(k["low"]), close=float(k["close"]), volume=float(k["volume"]))


# ============================================================
# 基准收益（沪深300 同期）
# ============================================================

def build_index_return_map(index_klines: List[dict], forward_days: List[int]) -> Dict[str, dict]:
    """构建日期 → 各 forward 收益 的映射"""
    dates = [k["date"] for k in index_klines]
    closes = [k["close"] for k in index_klines]
    idx_map = {}
    for i, d in enumerate(dates):
        entry = {}
        for fd in forward_days:
            if i + fd < len(dates) and closes[i] > 0:
                entry[fd] = round((closes[i + fd] / closes[i] - 1) * 100, 3)
        if entry:
            idx_map[d] = entry
    return idx_map


# ============================================================
# 统计
# ============================================================

def compute_stats(records: List[dict], idx_map: Dict[str, dict],
                  forward_days: List[int]) -> dict:
    """计算命中统计 + 超额收益"""
    stats = {"n_hits": len(records), "by_horizon": {}}
    if not records:
        return stats

    for fd in forward_days:
        hits = [r for r in records if f"fwd{fd}" in r]
        if not hits:
            continue
        rets = [r[f"fwd{fd}"] for r in hits]
        bench = []
        for r in hits:
            b = idx_map.get(r["date"], {}).get(fd)
            if b is not None:
                bench.append(b)
        avg_ret = sum(rets) / len(rets)
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        win_rate = len(wins) / len(rets) * 100
        avg_win = sum(wins) / len(wins) if wins else 0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0
        profit_loss = avg_win / avg_loss if avg_loss > 0 else float("inf")
        avg_bench = sum(bench) / len(bench) if bench else 0
        alpha = avg_ret - avg_bench
        # 超额胜率（跑赢基准的比例）
        alpha_wins = 0.0
        if bench and len(bench) == len(rets):
            alpha_wins = sum(1 for i, r in enumerate(rets) if r > bench[i]) / len(rets) * 100
        stats["by_horizon"][fd] = {
            "n": len(rets),
            "avg_ret": round(avg_ret, 3),
            "win_rate": round(win_rate, 1),
            "profit_loss": round(profit_loss, 2) if profit_loss != float("inf") else None,
            "avg_win": round(avg_win, 3),
            "avg_loss": round(avg_loss, 3),
            "bench_avg": round(avg_bench, 3),
            "alpha": round(alpha, 3),
            "alpha_win_rate": round(alpha_wins, 1),
        }
    return stats


def random_control(codes: List[str], klines_map: Dict[str, Optional[List[dict]]],
                   n_samples: int, seed: int = 42) -> List[float]:
    """随机对照：随机选 n_samples 只股票随机日期的 20 日收益分布

    用于显著性对比（形态命中 vs 全市场随机）。
    """
    rng = random.Random(seed)
    rets = []
    attempts = 0
    while len(rets) < n_samples and attempts < n_samples * 20:
        attempts += 1
        code = rng.choice(codes)
        kl = klines_map.get(code)
        if not kl or len(kl) < 111:   # 需要至少 90+21 根
            continue
        t = rng.randint(90, len(kl) - 21)
        if kl[t]["close"] <= 0 or kl[t + 20]["close"] <= 0:
            continue
        ret = (kl[t + 20]["close"] / kl[t]["close"] - 1) * 100
        rets.append(ret)
    return rets


# ============================================================
# 主流程
# ============================================================

def run_backtest(codes_names: List[tuple], params: dict, days: int = 750,
                 sample: Optional[int] = None, seed: int = 42,
                 export: Optional[str] = None,
                 horizons: List[int] = (5, 10, 20)):
    """执行回测"""
    if sample:
        rng = random.Random(seed)
        codes_names = rng.sample(codes_names, min(sample, len(codes_names)))
        print(f"[回测] 随机抽样 {len(codes_names)} 只")

    codes = [c for c, _ in codes_names]
    name_map = dict(codes_names)

    # 数据
    kl_map = load_kline_history(codes, days=days)
    idx_kl = kl_map.pop(INDEX_CODE, None)
    if idx_kl is None:
        from data_provider import get_kline
        idx_kl = get_kline(INDEX_CODE, days)
    if not idx_kl:
        print("[回测] 警告: 沪深300基准数据获取失败，超额收益无法计算")
        idx_map = {}
    else:
        idx_map = build_index_return_map(idx_kl, horizons)
        print(f"[回测] 基准{INDEX_NAME} {len(idx_kl)}根K线")

    # 滚动扫描
    t0 = time.time()
    all_records = []
    for code, kl in kl_map.items():
        if kl is None or len(kl) < 120:
            continue
        name = name_map.get(code, "")
        try:
            recs = scan_stock(code, name, kl, params, forward_days=horizons)
            all_records.extend(recs)
        except Exception as e:
            print(f"[回测] {code} 扫描异常: {e}")
    print(f"[回测] 滚动扫描完成 {time.time()-t0:.1f}s，命中 {len(all_records)} 条")

    # 统计
    stats = compute_stats(all_records, idx_map, horizons)
    print_stats(stats)

    # 随机对照
    print("\n── 随机对照（20日收益显著性） ──")
    control_rets = random_control(codes, kl_map, n_samples=max(500, len(all_records) // 3))
    hit_rets = [r.get("fwd20") for r in all_records if "fwd20" in r]
    if hit_rets and control_rets:
        avg_hit = sum(hit_rets) / len(hit_rets)
        avg_ctrl = sum(control_rets) / len(control_rets)
        diff = avg_hit - avg_ctrl
        # 简易显著性：命中收益为正的比例 vs 随机为正比例
        hit_pos = sum(1 for r in hit_rets if r > 0) / len(hit_rets) * 100
        ctrl_pos = sum(1 for r in control_rets if r > 0) / len(control_rets) * 100
        print(f"  命中20日均收益 {avg_hit:+.2f}% vs 随机 {avg_ctrl:+.2f}% → 超额 {diff:+.2f}%")
        print(f"  命中正收益占比 {hit_pos:.1f}% vs 随机 {ctrl_pos:.1f}%")
        if diff > 0 and hit_pos > ctrl_pos:
            print(f"  ✅ 形态存在正向超额收益（有待更大样本验证）")
        else:
            print(f"  ⚠️ 形态未呈现明显超额收益，需检查参数或样本量")

    # 导出训练样本
    if export and all_records:
        os.makedirs(os.path.dirname(export) or ".", exist_ok=True)
        with open(export, "w", encoding="utf-8") as f:
            for r in all_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\n[回测] ML训练样本已导出: {export}（{len(all_records)}条）")

    return all_records, stats


def print_stats(stats: dict):
    print("\n" + "=" * 78)
    print(f"形态历史回测统计（命中 {stats['n_hits']} 条）")
    print("=" * 78)
    if not stats["by_horizon"]:
        print("  无有效命中记录")
        return
    hdr = f"{'周期':<6}{'样本':>6}{'平均收益':>10}{'基准':>9}{'超额α':>9}{'胜率':>8}{'盈亏比':>8}{'跑赢率':>8}"
    print(hdr)
    print("-" * 78)
    for fd, s in stats["by_horizon"].items():
        pl = f"{s['profit_loss']:.2f}" if s["profit_loss"] else "-"
        print(f"  {fd}日{'':<3}{s['n']:>6}{s['avg_ret']:>+9.2f}%{s['bench_avg']:>+8.2f}%"
              f"{s['alpha']:>+8.2f}%{s['win_rate']:>7.1f}%{pl:>8}{s['alpha_win_rate']:>7.1f}%")
    print("=" * 78)


def main():
    ap = argparse.ArgumentParser(description="V2 历史回测：验证放量缩量横盘形态超额收益")
    ap.add_argument("--all", action="store_true", help="全市场回测")
    ap.add_argument("--sample", type=int, default=None, help="随机抽样N只（快速验证）")
    ap.add_argument("--days", type=int, default=750, help="回测K线根数（默认750≈3年）")
    ap.add_argument("--horizons", default="5,10,20", help="收益周期逗号分隔")
    ap.add_argument("--export", default=None, help="导出ML训练样本路径(.jsonl)")
    ap.add_argument("--params", default=None, help="覆盖参数JSON")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    params = dict(DEFAULT_PARAMS)
    if args.params:
        params.update(json.loads(args.params))
    horizons = [int(x) for x in args.horizons.split(",")]

    stocks = get_all_stocks()
    print(f"[回测] 全市场股票池 {len(stocks)} 只")
    codes_names = [(s["code"], s["name"]) for s in stocks]
    # 加基准
    codes_names.append((INDEX_CODE, INDEX_NAME))

    run_backtest(codes_names, params, days=args.days, sample=args.sample,
                 seed=args.seed, export=args.export, horizons=horizons)


if __name__ == "__main__":
    main()
