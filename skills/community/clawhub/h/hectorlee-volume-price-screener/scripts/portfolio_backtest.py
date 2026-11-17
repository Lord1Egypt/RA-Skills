#!/usr/bin/env python3
"""
每日 Top-千分之一 组合回测
============================
思路：不是所有命中都算，而是**每个交易日只选排名最前的千分之一**
（全市场 4591 只 → 前 ~5 只），模拟真实"每天挑精华"的操作。

排序指标（--sort）:
  score   : 100分制量价评分
  ml      : ML 上涨概率（加载 models/ml_model_v2.pkl）
  random  : 随机（对照基线）

回测规则:
  - 每个交易日 t: 当日命中池按指标降序，取前 top_k 只
  - 冷却期: 同一只股票 20 个交易日内不重复入选（避免重叠持仓）
  - 组合收益: 当日所选股票等权平均的 fwd5/10/20 收益
  - 统计: 平均收益、胜率、盈亏比、vs 沪深300 超额α、跑赢率

用法:
  python portfolio_backtest.py --sort score --top-k 5
  python portfolio_backtest.py --sort ml --top-k 5 --model models/ml_model_v2.pkl
  python portfolio_backtest.py --sort random --top-k 5          # 随机对照
  python portfolio_backtest.py --ratio 0.001                    # 按千分位自动算 k
  python portfolio_backtest.py --all-sorts                       # 三种排序对比
  python portfolio_backtest.py --walk-forward --top-k 5          # 前推验证（无泄漏，推荐）
"""

import argparse
import json
import os
import pickle
import random
import sys
import time
from collections import defaultdict
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_model import extract_feature_vector
from backtest import build_index_return_map

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
CACHE_FILE = os.path.join(DATA_DIR, "kline_cache.pkl")
SAMPLES_FILE = os.path.join(DATA_DIR, "ml_samples.jsonl")
MODEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models", "ml_model_v2.pkl")
TOTAL_MARKET = 4591   # 全市场A股数量（腾讯备用源实测）


def load_samples(path: str = SAMPLES_FILE) -> List[dict]:
    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            s = json.loads(line)
            if "fwd20" in s:
                samples.append(s)
    return samples


def load_index_map() -> Dict[str, dict]:
    """从K线缓存构建沪深300 各周期收益映射"""
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
    idx_kl = cache.get("sh000300")
    if not idx_kl:
        return {}
    return build_index_return_map(idx_kl, [5, 10, 20])


def add_ml_probs(samples: List[dict], model_path: str = MODEL_FILE) -> List[dict]:
    """批量计算 ML 上涨概率"""
    with open(model_path, "rb") as f:
        bundle = pickle.load(f)
    model = bundle["model"]
    X = [extract_feature_vector(s) for s in samples]
    probs = model.predict_proba(X)[:, 1]
    for s, p in zip(samples, probs):
        s["ml_prob"] = float(p)
    return samples


def daily_portfolio(samples: List[dict], sort_key: str, top_k: int,
                    cooldown: int = 20, seed: int = 42) -> Dict[str, List[dict]]:
    """按日分组 + 排序 + 取前 k + 冷却去重

    返回: {date: [选中样本, ...]}
    """
    # 按日期分组
    by_date = defaultdict(list)
    for s in samples:
        by_date[s["date"]].append(s)

    rng = random.Random(seed)
    selected: Dict[str, List[dict]] = {}
    last_pick: Dict[str, int] = {}      # code -> 最后入选的日期序号
    date_order = sorted(by_date.keys())

    for di, d in enumerate(date_order):
        pool = by_date[d]
        if sort_key == "score":
            pool.sort(key=lambda s: s.get("score", 0), reverse=True)
        elif sort_key == "ml":
            pool.sort(key=lambda s: s.get("ml_prob", 0), reverse=True)
        else:  # random
            rng.shuffle(pool)

        picks = []
        for s in pool:
            if len(picks) >= top_k:
                break
            code = s["code"]
            if code in last_pick and di - last_pick[code] < cooldown:
                continue   # 冷却期内跳过
            last_pick[code] = di
            picks.append(s)
        selected[d] = picks
    return selected


def compute_portfolio_stats(selected: Dict[str, List[dict]], idx_map: Dict[str, dict],
                            horizons: List[int] = (5, 10, 20)) -> dict:
    """组合收益统计（每日等权 → 交易日序列 → 汇总）"""
    stats = {"n_days": len(selected), "total_picks": sum(len(v) for v in selected.values()), "by_horizon": {}}
    for fd in horizons:
        daily_rets = []
        for d, picks in selected.items():
            rets = [p.get(f"fwd{fd}") for p in picks if f"fwd{fd}" in p]
            if not rets:
                continue
            daily_rets.append((d, sum(rets) / len(rets)))
        if not daily_rets:
            continue
        rets = [r for _, r in daily_rets]
        bench = [idx_map.get(d, {}).get(fd) for d, _ in daily_rets]
        bench_valid = [b for b in bench if b is not None]
        avg_ret = sum(rets) / len(rets)
        wins = [r for r in rets if r > 0]
        losses = [r for r in rets if r <= 0]
        win_rate = len(wins) / len(rets) * 100
        avg_win = sum(wins) / len(wins) if wins else 0
        avg_loss = abs(sum(losses) / len(losses)) if losses else 0
        pl = avg_win / avg_loss if avg_loss > 0 else float("inf")
        avg_bench = sum(bench_valid) / len(bench_valid) if bench_valid else 0
        alpha = avg_ret - avg_bench
        alpha_wins = sum(1 for i, r in enumerate(rets) if bench[i] is not None and r > bench[i]) / len(rets) * 100
        stats["by_horizon"][fd] = {
            "n_days": len(daily_rets), "avg_ret": round(avg_ret, 3),
            "win_rate": round(win_rate, 1), "profit_loss": round(pl, 2) if pl != float("inf") else None,
            "avg_win": round(avg_win, 3), "avg_loss": round(avg_loss, 3),
            "bench_avg": round(avg_bench, 3), "alpha": round(alpha, 3),
            "alpha_win_rate": round(alpha_wins, 1),
        }
    return stats


def print_portfolio_stats(stats: dict, tag: str = ""):
    print(f"\n── {tag} ──" if tag else "")
    print(f"交易日 {stats['n_days']} 天，累计入选 {stats['total_picks']} 只次（日均 {stats['total_picks']/max(1,stats['n_days']):.1f} 只）")
    hdr = f"{'周期':<6}{'天数':>6}{'日均收益':>10}{'基准':>9}{'超额α':>9}{'胜率':>8}{'盈亏比':>8}{'跑赢率':>8}"
    print(hdr)
    print("-" * 70)
    for fd, s in stats["by_horizon"].items():
        pl = f"{s['profit_loss']:.2f}" if s["profit_loss"] else "-"
        print(f"  {fd}日{'':<3}{s['n_days']:>6}{s['avg_ret']:>+9.2f}%{s['bench_avg']:>+8.2f}%"
              f"{s['alpha']:>+8.2f}%{s['win_rate']:>7.1f}%{pl:>8}{s['alpha_win_rate']:>7.1f}%")
    print("-" * 70)


def run_walk_forward(samples: List[dict], idx_map: Dict[str, dict], top_k: int,
                     cooldown: int = 20, seed: int = 42, split_ratio: float = 0.7,
                     ml_params: Optional[dict] = None) -> dict:
    """前推验证（无泄漏）：前 70% 时间训练 ML，后 30% 时间回测

    这是唯一可信的收益评估——避免样本内过拟合。
    """
    from sklearn.ensemble import GradientBoostingClassifier
    dates = sorted(set(s["date"] for s in samples))
    split_date = dates[int(len(dates) * split_ratio)]
    train = [s for s in samples if s["date"] <= split_date]
    test = [s for s in samples if s["date"] > split_date]
    print(f"[前推验证] 切分点 {split_date} | 训练 {len(train)}条({len(set(s['date'] for s in train))}天) "
          f"→ 验证 {len(test)}条({len(set(s['date'] for s in test))}天)")

    # 训练集上训练 ML（强正则化抗过拟合）
    mp = ml_params or dict(n_estimators=50, max_depth=2, learning_rate=0.02,
                           subsample=0.6, min_samples_leaf=200, random_state=seed)
    X_tr = [extract_feature_vector(s) for s in train]
    y_tr = [1.0 if s.get("fwd20", 0) > 0 else 0.0 for s in train]
    model = GradientBoostingClassifier(**mp)
    model.fit(X_tr, y_tr)

    # 验证集计算 ML 概率（无泄漏）
    probs = model.predict_proba([extract_feature_vector(s) for s in test])[:, 1]
    for s, p in zip(test, probs):
        s["ml_prob"] = float(p)

    # 三种排序在验证期回测
    results = {}
    for sk, tag in [("score", "评分排序(验证期)"), ("ml", "ML概率(验证期-无泄漏)"),
                    ("random", "随机(验证期)")]:
        selected = daily_portfolio(test, sk, top_k, cooldown=cooldown, seed=seed)
        stats = compute_portfolio_stats(selected, idx_map)
        results[sk] = (stats, selected)
        print_portfolio_stats(stats, tag)

    print("\n═══ 前推验证 20日 α 对比 ═══")
    print(f"{'排序':<10}{'日均收益':>10}{'胜率':>8}{'盈亏比':>8}{'超额α':>9}")
    for sk in ["score", "ml", "random"]:
        s = results[sk][0]["by_horizon"].get(20, {})
        pl = f"{s.get('profit_loss', 0):.2f}" if s.get("profit_loss") else "-"
        print(f"{sk:<10}{s.get('avg_ret', 0):>+9.2f}%{s.get('win_rate', 0):>7.1f}%{pl:>8}"
              f"{s.get('alpha', 0):>+8.2f}%")
    return results


def rolling_nav(selected: Dict[str, List[dict]], hold_days: int = 20,
                cost_pct: float = 0.0) -> List[tuple]:
    """滚动持有净值模拟（基于真实K线收盘价，每日等权再平衡）

    规则:
      - 每个交易日 t 收盘价买入当日选中股，持有 hold_days 个交易日后卖出
      - 每日等权: 当日活跃持仓每笔权重相同，组合日收益 = 平均单日收益
      - 买入日不计收益（收盘买入），从次日起计
      - 成本: cost_pct=单边费率(%)，按成交金额买卖各收一次

    返回: [(date, nav), ...]
    """
    with open(CACHE_FILE, "rb") as f:
        cache = pickle.load(f)
    prices = {code: {k["date"]: k["close"] for k in kl} for code, kl in cache.items() if kl}

    sel_dates = sorted(selected.keys())
    di_map = {d: i for i, d in enumerate(sel_dates)}

    # 持仓登记: (buy_di, code, buy_price)
    holdings = []
    for di, d in enumerate(sel_dates):
        for p in selected[d]:
            code = p["code"]
            pmap = prices.get(code, {})
            if d in pmap and pmap[d] > 0:
                holdings.append((di, code, pmap[d]))

    nav = 1.0
    curve = []
    for di, d in enumerate(sel_dates):
        active = [h for h in holdings if h[0] <= di < h[0] + hold_days]
        if not active:
            curve.append((d, nav))
            continue
        # 当日收益（从买入次日起）
        day_rets = []
        for (bdi, code, buy_price) in active:
            pmap = prices.get(code, {})
            if di == bdi:
                continue
            prev_d = sel_dates[di - 1]
            prev_price = buy_price if di == bdi + 1 else pmap.get(prev_d)
            cur = pmap.get(d)
            if prev_price and cur and prev_price > 0:
                day_rets.append(cur / prev_price - 1)
        if day_rets:
            nav *= (1 + sum(day_rets) / len(day_rets))
        # 成本（按成交金额比例，近似当日每笔等权）
        if cost_pct > 0:
            n_active = max(1, len(active))
            n_new = sum(1 for h in active if h[0] == di)
            n_out = sum(1 for h in holdings if h[0] + hold_days == di)
            fee = (n_new + n_out) * (nav / n_active) * (cost_pct / 100.0)
            nav -= fee
        curve.append((d, nav))
    return curve


def print_nav_report(curve: List[tuple], idx_map: Dict[str, dict], tag: str = ""):
    """净值曲线报告（累计收益 + 同期基准 + 超额 + 回撤）"""
    if len(curve) < 2:
        print("  净值曲线数据不足")
        return
    dates = [d for d, _ in curve]
    navs = [n for _, n in curve]
    total_ret = (navs[-1] / navs[0] - 1) * 100
    # 同期基准（从K线缓存读沪深300）
    bench_ret = None
    try:
        with open(CACHE_FILE, "rb") as f:
            cache = pickle.load(f)
        idx_kl = cache.get("sh000300") or []
        idx_dates = [k["date"] for k in idx_kl]
        idx_closes = [k["close"] for k in idx_kl]
        d0, d1 = dates[0], dates[-1]
        i0 = next((i for i, d in enumerate(idx_dates) if d >= d0), None)
        i1 = next((i for i, d in enumerate(idx_dates) if d >= d1), None)
        if i0 is not None and i1 is not None and i0 < i1 and idx_closes[i0] > 0:
            bench_ret = (idx_closes[i1] / idx_closes[i0] - 1) * 100
    except Exception:
        pass
    # 最大回撤
    peak = navs[0]
    max_dd = 0.0
    for n in navs:
        if n > peak:
            peak = n
        dd = (peak - n) / peak * 100
        if dd > max_dd:
            max_dd = dd
    # 年化（按 244 交易日）
    years = len(navs) / 244.0
    annual = ((navs[-1] / navs[0]) ** (1 / years) - 1) * 100 if years > 0 else 0
    print(f"\n── {tag} 净值报告 ──" if tag else "")
    print(f"  区间: {dates[0]} → {dates[-1]}（{len(navs)} 交易日，约 {years:.1f} 年）")
    print(f"  累计收益: {total_ret:+.2f}%   年化: {annual:+.2f}%   最大回撤: {max_dd:.2f}%")
    print(f"  期末净值: {navs[-1]:.4f}")
    if bench_ret is not None:
        print(f"  沪深300同期: {bench_ret:+.2f}%   超额: {total_ret - bench_ret:+.2f}%")


def main():
    ap = argparse.ArgumentParser(description="每日Top千分之一组合回测")
    ap.add_argument("--sort", default="score", choices=["score", "ml", "random"])
    ap.add_argument("--top-k", type=int, default=None, help="每日选取数量（默认按千分位自动算）")
    ap.add_argument("--ratio", type=float, default=0.001, help="选取比例（千分之一=0.001）")
    ap.add_argument("--model", default=MODEL_FILE, help="ML模型路径")
    ap.add_argument("--cooldown", type=int, default=20, help="同股冷却期（交易日）")
    ap.add_argument("--all-sorts", action="store_true", help="对比三种排序")
    ap.add_argument("--walk-forward", action="store_true", help="前推验证（无泄漏，推荐）")
    ap.add_argument("--nav", action="store_true", help="额外输出滚动持有净值曲线报告")
    ap.add_argument("--cost", type=float, default=0.0, help="单边交易成本%%，净值模拟扣费（如 0.1）")
    args = ap.parse_args()

    top_k = args.top_k or max(1, round(TOTAL_MARKET * args.ratio))
    print(f"[组合回测] 全市场 {TOTAL_MARKET} 只 × {args.ratio*100:.1f}% → 每日选 {top_k} 只")

    t0 = time.time()
    print("[组合回测] 加载样本...")
    samples = load_samples()
    print(f"[组合回测] 样本 {len(samples)} 条，加载索引基准...")
    idx_map = load_index_map()
    print(f"[组合回测] 数据加载完成 {time.time()-t0:.1f}s")

    if args.walk_forward:
        results = run_walk_forward(samples, idx_map, top_k, cooldown=args.cooldown)
        if args.nav:
            for sk, (stats, selected) in results.items():
                curve = rolling_nav(selected, hold_days=20, cost_pct=args.cost)
                tag = {"score": "评分排序", "ml": "ML概率", "random": "随机"}[sk]
                print_nav_report(curve, idx_map, tag)
        return

    sorts = ["score", "ml", "random"] if args.all_sorts else [args.sort]
    if "ml" in sorts:
        print("[组合回测] 计算 ML 概率...")
        samples = add_ml_probs(samples)

    results = {}
    for sk in sorts:
        selected = daily_portfolio(samples, sk, top_k, cooldown=args.cooldown)
        stats = compute_portfolio_stats(selected, idx_map)
        results[sk] = (stats, selected)
        tag = {"score": "评分排序", "ml": "ML概率排序", "random": "随机对照"}[sk]
        print_portfolio_stats(stats, tag)

    # 对比汇总
    if len(sorts) > 1:
        print("\n═══ 三种排序 20日收益对比 ═══")
        print(f"{'排序':<10}{'日均收益':>10}{'胜率':>8}{'盈亏比':>8}{'超额α':>9}")
        for sk in sorts:
            s = results[sk][0]["by_horizon"].get(20, {})
            pl = f"{s.get('profit_loss', 0):.2f}" if s.get("profit_loss") else "-"
            print(f"{sk:<10}{s.get('avg_ret', 0):>+9.2f}%{s.get('win_rate', 0):>7.1f}%{pl:>8}"
                  f"{s.get('alpha', 0):>+8.2f}%")

    # 最近一天选出的股票（示例）
    selected = results[sorts[0]][1]
    last_date = max(selected.keys())
    print(f"\n[示例] 最近一个交易日 {last_date} 选出 {len(selected[last_date])} 只：")
    for p in sorted(selected[last_date], key=lambda x: -(x.get("score", 0) or 0)):
        ml = f" ML={p.get('ml_prob', 0)*100:.0f}%" if "ml_prob" in p else ""
        print(f"  {p['code']} {p.get('name','')} 评分{p.get('score',0):.0f}{ml}")


if __name__ == "__main__":
    main()
