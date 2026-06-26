#!/usr/bin/env python3
"""
机构操盘行为识别算法 - 大规模回测验证 v3
v3改进:
1. 标的池从10只扩展到30只（覆盖全行业）
2. 多窗口收益测试（3/5/10/20日）
3. 追踪止损模拟
4. Regime条件信号过滤
5. 统计检验 + 样本外验证
"""
import sys
import json
import math
import time
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))

from config import WEIGHTS, REPORTS_DIR
from data_fetcher import TushareFetcher
from signal_engine import (
    score_fund_flow, score_volume_price, score_position,
    score_north_margin, score_limit_event,
    compute_total_score, determine_state
)
from market_regime import judge_market_regime

# AI链条龙头标的池（10只纯龙头，市值>500亿，行业地位第一）
BACKTEST_STOCKS = [
    # AI算力/光模块
    ("300308.SZ", "中际旭创", "光模块龙头"),
    ("300502.SZ", "新易盛", "光模块"),
    ("601138.SH", "工业富联", "AI服务器龙头"),
    # AI芯片
    ("688256.SH", "寒武纪", "AI芯片龙头"),
    ("688041.SH", "海光信息", "GPU/DCU龙头"),
    ("688981.SH", "中芯国际", "芯片代工龙头"),
    ("002371.SZ", "北方华创", "半导体设备龙头"),
    # AI应用
    ("002230.SZ", "科大讯飞", "AI应用龙头"),
    # 智能制造
    ("300750.SZ", "宁德时代", "智能制造龙头"),
    ("002594.SZ", "比亚迪", "智能汽车龙头"),
]

LOOKBACK_DAYS = 60
FORWARD_WINDOWS = [3, 5, 10, 20]
TRAILING_STOP_PCT = 15.0  # v11: 止损线调至15%（A股波动大，8%太紧）


def fetch_period_data(ts, code, start, end):
    """获取单只股票一段时间的全部数据"""
    daily = ts.get_daily(code, start, end); time.sleep(0.6)
    basic = ts.get_daily_basic(code, start, end); time.sleep(0.6)
    mf = ts.get_moneyflow(code, start, end); time.sleep(0.6)
    margin = ts.get_margin(code, start, end); time.sleep(0.6)
    return daily, basic, mf, margin


def compute_signal_for_day(daily_slice, basic_slice, mf_slice, margin_slice,
                            north_slice, limit_data, idx_slice, code,
                            spx_slice=None, hsi_slice=None):
    """计算某一天的信号评分和状态"""
    regime = judge_market_regime(idx_slice, north_slice, limit_data, spx_slice, hsi_slice)
    regime_adjust = regime["distribution_threshold_adjust"]

    scores = {}
    scores["fund_flow"] = score_fund_flow(mf_slice, float(basic_slice[0].get("total_mv", 0) or 0) if basic_slice else 0)
    scores["volume_price"] = score_volume_price(daily_slice, basic_slice)
    scores["chip_dist"] = score_position(daily_slice, basic_slice)
    scores["north_margin"] = score_north_margin([], margin_slice, code, north_slice)
    scores["event"] = score_limit_event(limit_data, code, daily_slice, basic_slice, margin_slice)

    total_score, details = compute_total_score(scores, WEIGHTS)
    state_code, _, _ = determine_state(total_score, regime_adjust, regime["regime"],
                                        daily=daily_slice, moneyflow=mf_slice,
                                        daily_basic=basic_slice, margin_data=margin_slice)

    return total_score, state_code, regime["regime"], regime["regime_score"], details


def binomial_p_value(n, k, p0=0.5):
    """计算二项分布单侧P值: P(X >= k | n, p0)
    用于检验"胜率是否显著高于随机"
    """
    if n == 0:
        return 1.0
    # 用正态近似
    mean = n * p0
    std = math.sqrt(n * p0 * (1 - p0))
    if std == 0:
        return 0.0 if k > mean else 1.0
    z = (k - 0.5 - mean) / std  # 连续性修正
    # 标准正态CDF的互补
    return 0.5 * math.erfc(z / math.sqrt(2))


def wilson_ci(n, k, z=1.96):
    """Wilson置信区间（适合小样本比例估计）"""
    if n == 0:
        return (0, 1)
    p_hat = k / n
    denom = 1 + z * z / n
    center = (p_hat + z * z / (2 * n)) / denom
    spread = z * math.sqrt((p_hat * (1 - p_hat) + z * z / (4 * n)) / n) / denom
    return (max(0, center - spread), min(1, center + spread))


def run_backtest_period(ts, period_name, start_date, end_date, stocks):
    """对指定时间段执行回测"""
    print(f"\n{'='*65}")
    print(f"🧪 回测: {period_name} ({start_date} → {end_date})")
    print(f"{'='*65}")

    # 需要更早的数据用于lookback
    actual_start = (datetime.strptime(start_date, "%Y%m%d") - timedelta(days=200)).strftime("%Y%m%d")

    # === 全局数据 ===
    print("  获取全局数据...")
    index_daily = ts.get_index_daily("000001.SH", actual_start, end_date)
    print(f"    上证: {len(index_daily)}天")
    time.sleep(0.6)

    north_global = ts.get_north_money(actual_start, end_date)
    print(f"    北向: {len(north_global)}天")
    time.sleep(0.6)

    spx_data = ts.get_global_index("SPX")
    print(f"    标普: {len(spx_data)}天")
    time.sleep(0.6)

    hsi_data = ts.get_global_index("HSI")
    print(f"    恒生: {len(hsi_data)}天")
    time.sleep(0.6)

    # 涨跌停: 取有交易日数据的日期
    trade_dates = sorted(set(d.get("trade_date", "") for d in index_daily
                             if d.get("trade_date", "") >= start_date), reverse=True)
    # 采样获取涨跌停（API限制，不能每天都取）
    limit_by_date = {}
    sample_dates = trade_dates[::5][:30]  # 每5天取一个，最多30个
    for td in sample_dates:
        try:
            limit_by_date[td] = ts.get_limit_list(td)
            time.sleep(0.6)
        except Exception:
            pass
    print(f"    涨跌停: {len(limit_by_date)}天(采样)")

    # === 个股数据 ===
    print("  获取个股数据...")
    all_data = {}
    for code, name, sector in stocks:
        print(f"    → {name}({code})...", end="", flush=True)
        try:
            daily, basic, mf, margin = fetch_period_data(ts, code, actual_start, end_date)
            all_data[code] = {
                "name": name, "sector": sector,
                "daily": daily, "daily_basic": basic,
                "moneyflow": mf, "margin": margin
            }
            print(f" {len(daily)}天")
        except Exception as e:
            print(f" ERROR: {e}")

    # === 逐日回测 ===
    print(f"  逐日计算信号...")
    all_signals = []
    skipped = 0

    for code, name, sector in stocks:
        if code not in all_data:
            continue
        sd = all_data[code]
        daily_all = sd["daily"]
        mf_all = sd["moneyflow"]
        basic_all = sd["daily_basic"]
        margin_all = sd["margin"]

        if not daily_all or len(daily_all) < LOOKBACK_DAYS + max(FORWARD_WINDOWS) + 5:
            skipped += 1
            continue

        dates = [d["trade_date"] for d in daily_all]

        for i in range(max(FORWARD_WINDOWS), len(daily_all) - LOOKBACK_DAYS):
            signal_date = dates[i]
            if signal_date < start_date or signal_date > end_date:
                continue

            # 数据切片
            daily_slice = daily_all[i:i + LOOKBACK_DAYS]
            basic_slice = [b for b in basic_all if b.get("trade_date", "") <= signal_date][:5]
            mf_slice = [m for m in mf_all if m.get("trade_date", "") <= signal_date][:5]
            margin_slice = [m for m in margin_all if m.get("trade_date", "") <= signal_date][:5]
            north_slice = [n for n in north_global if n.get("trade_date", "") <= signal_date][:20]
            limit = limit_by_date.get(signal_date, [])
            idx_slice = [d for d in index_daily if d.get("trade_date", "") <= signal_date][:120]
            spx_slice = [d for d in spx_data if d.get("trade_date", "") <= signal_date][:5]
            hsi_slice = [d for d in hsi_data if d.get("trade_date", "") <= signal_date][:5]

            try:
                total_score, state_code, regime, regime_score, details = compute_signal_for_day(
                    daily_slice, basic_slice, mf_slice, margin_slice,
                    north_slice, limit, idx_slice, code,
                    spx_slice, hsi_slice
                )
            except Exception:
                continue

            # 多窗口未来收益
            sc = float(daily_all[i].get("close", 0) or 0)
            if sc <= 0:
                continue

            future_returns = {}
            for fw in FORWARD_WINDOWS:
                if i - fw >= 0:
                    fc = float(daily_all[i - fw].get("close", 0) or 0)
                    future_returns[fw] = (fc - sc) / sc * 100 if fc > 0 else 0
                else:
                    future_returns[fw] = 0

            # 追踪止损模拟（买入后追踪最高价，跌破8%止损）
            trailing_return = 0
            if state_code == "ACCUMULATION" and i > 0:
                peak = sc
                for j in range(i - 1, max(i - 21, -1), -1):  # 最多看20日
                    cj = float(daily_all[j].get("close", 0) or 0)
                    if cj > peak:
                        peak = cj
                    drawdown = (cj - peak) / peak * 100
                    if drawdown <= -TRAILING_STOP_PCT:
                        trailing_return = (cj - sc) / sc * 100
                        break
                else:
                    # 未触发止损，用20日收益
                    trailing_return = future_returns.get(20, 0)

            all_signals.append({
                "code": code, "name": name, "date": signal_date,
                "state": state_code, "score": total_score,
                "future_return": future_returns.get(5, 0),
                "future_returns": future_returns,
                "trailing_return": trailing_return,
                "regime": regime, "regime_score": regime_score,
            })

    if skipped:
        print(f"  (跳过{skipped}只数据不足)")
    print(f"  总信号: {len(all_signals)}")

    return all_signals


def analyze_signals(signals, label=""):
    """分析信号统计并输出"""
    if not signals:
        print(f"  {label}: 无信号")
        return {}

    # 市场环境分布
    regime_counts = defaultdict(int)
    for s in signals:
        regime_counts[s["regime"]] += 1

    print(f"\n  市场环境: ", end="")
    for r in ["BULL", "NEUTRAL", "BEAR"]:
        c = regime_counts.get(r, 0)
        print(f"{r}={c}({c / len(signals) * 100:.0f}%) ", end="")
    print()

    # 分状态统计
    state_stats = defaultdict(lambda: {"count": 0, "returns": [], "win": 0})
    for sig in signals:
        st = sig["state"]
        state_stats[st]["count"] += 1
        state_stats[st]["returns"].append(sig["future_return"])
        if (st in ["ACCUMULATION", "MARKUP", "WASHOUT"] and sig["future_return"] > 0) or \
                (st == "DISTRIBUTION" and sig["future_return"] < 0):
            state_stats[st]["win"] += 1

    labels_map = {
        "ACCUMULATION": "⭐ 吸筹(买)", "MARKUP": "🚀 拉升", "WASHOUT": "💎 洗盘",
        "NEUTRAL": "⚪ 观望", "CAUTION": "⚠️ 风险警示", "DISTRIBUTION": "🔴 出货(卖)"
    }

    print(f"\n  {'状态':<14} {'次数':>5} {'平均5日':>8} {'中位':>7} {'胜率':>7}")
    print(f"  {'-' * 50}")
    for st in ["ACCUMULATION", "MARKUP", "WASHOUT", "NEUTRAL", "CAUTION", "DISTRIBUTION"]:
        info = state_stats[st]
        if info["count"] == 0:
            continue
        rets = sorted(info["returns"])
        avg = sum(rets) / len(rets)
        med = rets[len(rets) // 2]
        wr = info["win"] / info["count"] * 100
        print(f"  {labels_map.get(st, st):<14} {info['count']:>5} {avg:>+7.2f}% {med:>+6.2f}% {wr:>6.1f}%")

    # 核心指标 + 统计检验
    buy = [s for s in signals if s["state"] == "ACCUMULATION"]
    sell = [s for s in signals if s["state"] == "DISTRIBUTION"]
    base = sum(s["future_return"] for s in signals) / len(signals)

    result = {
        "total": len(signals),
        "regime_dist": dict(regime_counts),
        "baseline": base,
    }

    print(f"\n  📏 基准(全样本): {base:+.2f}%")

    if buy:
        ba = sum(s["future_return"] for s in buy) / len(buy)
        bw = sum(1 for s in buy if s["future_return"] > 0)
        wr = bw / len(buy) * 100
        alpha = ba - base

        # 统计检验
        # 1. 胜率P值: 胜率是否显著>50%
        p_winrate = binomial_p_value(len(buy), bw, 0.5)
        # 2. 胜率是否显著>基准胜率
        base_wr = sum(1 for s in signals if s["future_return"] > 0) / len(signals)
        p_vs_base = binomial_p_value(len(buy), bw, base_wr)
        # 3. Wilson置信区间
        ci_low, ci_high = wilson_ci(len(buy), bw)

        print(f"\n  ⭐ 买入信号:")
        print(f"    次数: {len(buy)}  |  平均收益: {ba:+.2f}%  |  胜率: {wr:.1f}%  |  Alpha: {alpha:+.2f}%")
        print(f"    P值(>50%): {p_winrate:.4f}  |  P值(>基准{base_wr * 100:.0f}%): {p_vs_base:.4f}")
        print(f"    95%置信区间: [{ci_low * 100:.1f}%, {ci_high * 100:.1f}%]")
        if p_winrate < 0.05:
            print(f"    ✅ 统计显著(p<0.05): 胜率显著高于随机")
        elif p_winrate < 0.10:
            print(f"    ⚠️ 边缘显著(p<0.10): 有迹象但不够确定")
        else:
            print(f"    ❌ 不显著(p={p_winrate:.3f}): 可能是随机波动")

        result["buy"] = {
            "n": len(buy), "avg": ba, "win_rate": wr, "alpha": alpha,
            "p_value_50": p_winrate, "p_value_base": p_vs_base,
            "ci_95": [ci_low, ci_high],
        }

        # 多窗口收益分析
        print(f"\n    📊 多窗口收益(买入后):")
        window_results = {}
        for fw in FORWARD_WINDOWS:
            fw_rets = [s["future_returns"].get(fw, 0) for s in buy if "future_returns" in s]
            if fw_rets:
                fw_avg = sum(fw_rets) / len(fw_rets)
                fw_win = sum(1 for r in fw_rets if r > 0) / len(fw_rets) * 100
                fw_p = binomial_p_value(len(fw_rets), sum(1 for r in fw_rets if r > 0), 0.5)
                marker = "✅" if fw_p < 0.05 else "⚠️" if fw_p < 0.10 else "  "
                print(f"    {marker} {fw:>2}日: {fw_avg:+.2f}% 胜率{fw_win:.1f}% P={fw_p:.3f}")
                window_results[fw] = {"avg": fw_avg, "win_rate": fw_win, "p_value": fw_p}
        result["buy_windows"] = window_results

        # 追踪止损分析
        trailing_rets = [s.get("trailing_return", 0) for s in buy if s.get("trailing_return", 0) != 0]
        if trailing_rets:
            t_avg = sum(trailing_rets) / len(trailing_rets)
            t_win = sum(1 for r in trailing_rets if r > 0) / len(trailing_rets) * 100
            print(f"\n    🛡️ 追踪止损({TRAILING_STOP_PCT}%回撤止损):")
            print(f"    平均收益: {t_avg:+.2f}% | 胜率: {t_win:.1f}% | 有效信号: {len(trailing_rets)}次")
            result["trailing_stop"] = {"avg": t_avg, "win_rate": t_win, "n": len(trailing_rets)}

        # BULL-only买入分析
        bull_buy = [s for s in buy if s["regime"] == "BULL"]
        if bull_buy:
            bb_avg = sum(s["future_return"] for s in bull_buy) / len(bull_buy)
            bb_win = sum(1 for s in bull_buy if s["future_return"] > 0) / len(bull_buy) * 100
            bb_p = binomial_p_value(len(bull_buy), sum(1 for s in bull_buy if s["future_return"] > 0), 0.5)
            print(f"\n    🐂 BULL-only买入: {len(bull_buy)}次 {bb_avg:+.2f}% 胜率{bb_win:.1f}% P={bb_p:.4f}")
            result["buy_bull_only"] = {"n": len(bull_buy), "avg": bb_avg, "win_rate": bb_win, "p_value": bb_p}

    if sell:
        sa = sum(s["future_return"] for s in sell) / len(sell)
        sc = sum(1 for s in sell if s["future_return"] < 0)
        cr = sc / len(sell) * 100
        p_sell = binomial_p_value(len(sell), sc, 0.5)
        ci_low, ci_high = wilson_ci(len(sell), sc)

        print(f"\n  🔴 卖出信号:")
        print(f"    次数: {len(sell)}  |  平均收益: {sa:+.2f}%  |  正确率: {cr:.1f}%")
        print(f"    P值(>50%): {p_sell:.4f}  |  95%CI: [{ci_low * 100:.1f}%, {ci_high * 100:.1f}%]")

        # 分市场环境
        for regime in ["BULL", "NEUTRAL", "BEAR"]:
            rs = [s for s in sell if s["regime"] == regime]
            if rs:
                ra = sum(s["future_return"] for s in rs) / len(rs)
                rc = sum(1 for s in rs if s["future_return"] < 0) / len(rs) * 100
                print(f"    └ {regime}: {len(rs)}次, {ra:+.2f}%, 正确{rc:.0f}%")

        result["sell"] = {
            "n": len(sell), "avg": sa, "correct_rate": cr,
            "p_value": p_sell, "ci_95": [ci_low, ci_high],
        }

    return result


def main():
    ts = TushareFetcher()

    print("🔬 机构操盘行为识别算法 — 大规模回测 v2")
    print("=" * 65)
    print("目标: 扩大样本量 + 样本外验证 + 统计检验")
    print()

    # ============================================================
    # Phase 1: 多时期回测（扩大样本量）
    # ============================================================
    periods = [
        ("2022 熊市(上证3400→2800)", "20220101", "20221031"),
        ("2023 震荡反弹(上证3000→3100)", "20230101", "20231231"),
        ("2024 结构牛(上证2800→3400)", "20240101", "20241231"),
        ("2025 科技牛(上证3100→3600)", "20250101", "20251231"),
        ("2026 YTD", "20260101", "20260429"),
    ]

    all_period_results = {}
    combined_signals = []

    for name, start, end in periods:
        signals = run_backtest_period(ts, name, start, end, BACKTEST_STOCKS)
        result = analyze_signals(signals, name)
        all_period_results[name] = result
        combined_signals.extend(signals)

    # ============================================================
    # Phase 2: 全周期汇总
    # ============================================================
    print(f"\n{'='*65}")
    print(f"📊 全周期汇总 (2022-2026, {len(combined_signals)}条信号)")
    print(f"{'='*65}")
    combined_result = analyze_signals(combined_signals, "全周期")

    # ============================================================
    # Phase 3: 样本外验证 (训练=2022-2024, 测试=2025-2026)
    # ============================================================
    train_signals = [s for s in combined_signals if s["date"] < "20250101"]
    test_signals = [s for s in combined_signals if s["date"] >= "20250101"]

    print(f"\n{'='*65}")
    print(f"🔍 样本外验证")
    print(f"{'='*65}")
    print(f"  训练集(2022-2024): {len(train_signals)}条")
    print(f"  测试集(2025-2026): {len(test_signals)}条 ← 算法从未见过这些数据")

    print(f"\n  --- 训练集(2022-2024)表现 ---")
    train_result = analyze_signals(train_signals, "训练集")

    print(f"\n  --- 测试集(2025-2026)表现 [样本外] ---")
    test_result = analyze_signals(test_signals, "测试集")

    # 对比
    print(f"\n  --- 过拟合检测 ---")
    if "buy" in train_result and "buy" in test_result:
        tr_wr = train_result["buy"]["win_rate"]
        te_wr = test_result["buy"]["win_rate"]
        degradation = tr_wr - te_wr
        print(f"  买入胜率: 训练{tr_wr:.1f}% → 测试{te_wr:.1f}% (衰减{degradation:+.1f}%)")
        if degradation > 15:
            print(f"  ⚠️ 严重过拟合: 样本外衰减>{degradation:.0f}%")
        elif degradation > 5:
            print(f"  ⚠️ 轻度过拟合: 样本外衰减{degradation:.0f}%")
        else:
            print(f"  ✅ 无明显过拟合: 样本外表现稳定")

        tr_alpha = train_result["buy"]["alpha"]
        te_alpha = test_result["buy"]["alpha"]
        print(f"  Alpha: 训练{tr_alpha:+.2f}% → 测试{te_alpha:+.2f}%")

    # ============================================================
    # Phase 4: 综合可信度评分
    # ============================================================
    print(f"\n{'='*65}")
    print(f"📋 综合可信度评估")
    print(f"{'='*65}")

    scores = {}

    # 1. 数据质量 (固定)
    scores["data_quality"] = 75

    # 2. 买入信号可信度
    if "buy" in combined_result:
        buy_p = combined_result["buy"].get("p_value_50", 1)
        buy_n = combined_result["buy"]["n"]
        buy_wr = combined_result["buy"]["win_rate"]
        buy_score = 0
        if buy_p < 0.01:
            buy_score = 90
        elif buy_p < 0.05:
            buy_score = 75
        elif buy_p < 0.10:
            buy_score = 55
        else:
            buy_score = 30
        # 样本量加成
        if buy_n >= 50:
            buy_score += 10
        elif buy_n < 20:
            buy_score -= 15
        scores["buy_signal"] = min(100, max(0, buy_score))
    else:
        scores["buy_signal"] = 0

    # 3. 卖出信号可信度
    if "sell" in combined_result:
        sell_p = combined_result["sell"].get("p_value", 1)
        sell_cr = combined_result["sell"]["correct_rate"]
        sell_score = 0
        if sell_p < 0.05 and sell_cr > 55:
            sell_score = 70
        elif sell_p < 0.10:
            sell_score = 45
        elif sell_cr > 50:
            sell_score = 35
        else:
            sell_score = 15
        scores["sell_signal"] = sell_score
    else:
        scores["sell_signal"] = 0

    # 4. 样本外验证
    if "buy" in test_result and "buy" in train_result:
        te_wr = test_result["buy"]["win_rate"]
        degradation = train_result["buy"]["win_rate"] - te_wr
        if degradation < 5 and te_wr > 60:
            scores["out_of_sample"] = 85
        elif degradation < 10 and te_wr > 55:
            scores["out_of_sample"] = 65
        elif degradation < 15:
            scores["out_of_sample"] = 45
        else:
            scores["out_of_sample"] = 20
    else:
        scores["out_of_sample"] = 30

    # 5. 样本量
    total_buy = combined_result.get("buy", {}).get("n", 0)
    if total_buy >= 100:
        scores["sample_size"] = 90
    elif total_buy >= 50:
        scores["sample_size"] = 70
    elif total_buy >= 30:
        scores["sample_size"] = 50
    elif total_buy >= 15:
        scores["sample_size"] = 35
    else:
        scores["sample_size"] = 15

    # 加权综合
    weights = {"data_quality": 0.15, "buy_signal": 0.30, "sell_signal": 0.15,
               "out_of_sample": 0.25, "sample_size": 0.15}
    overall = sum(scores[k] * weights[k] for k in weights)

    for k, v in scores.items():
        bar = "█" * (v // 5) + "░" * (20 - v // 5)
        print(f"  {k:<18} {bar} {v:>3}/100")
    print(f"\n  {'OVERALL':<18} {'━' * 20} {overall:>5.1f}/100")

    if overall >= 70:
        verdict = "✅ 可信度较高 — 可作为重要参考"
    elif overall >= 50:
        verdict = "⚠️ 可信度中等 — 作为辅助参考使用"
    elif overall >= 30:
        verdict = "⚠️ 可信度偏低 — 仅供观察，不建议依赖"
    else:
        verdict = "❌ 可信度不足 — 需要继续改进"
    print(f"  {verdict}")

    # 保存完整结果
    final = {
        "run_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_signals": len(combined_signals),
        "period_results": {k: v for k, v in all_period_results.items() if v},
        "combined": combined_result,
        "train_set": train_result,
        "test_set": test_result,
        "reliability_scores": scores,
        "overall_score": overall,
    }
    out = REPORTS_DIR / "backtest_fullcycle_v2.json"
    out.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  ✅ 完整结果: {out}")
    return final


if __name__ == "__main__":
    main()
