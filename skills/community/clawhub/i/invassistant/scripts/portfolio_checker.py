# -*- coding: utf-8 -*-
"""
InvAssistant — 持仓组合检查主程序
读取配置文件，按策略类型分发检查逻辑，生成信号报告。

用法:
  python portfolio_checker.py                  # 检查全部持仓
  python portfolio_checker.py --detail TSLA    # 单标的详细分析
  python portfolio_checker.py --push           # 检查并推送结果
  python portfolio_checker.py --json           # 输出 JSON 格式

环境变量:
  INVASSISTANT_CONFIG — 配置文件路径 (默认: 项目根目录/invassistant-config.json)
"""
import sys
import io
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

# Windows 控制台编码修复
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 确保 scripts 目录在 path 中
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from data_fetcher import fetch_stock, fetch_all
from redline_engine import (
    check_emotion, check_tech, check_market,
    check_pullback, run_redline_check, run_trend_check,
    DEFAULT_REDLINE_PARAMS, DEFAULT_MARKET_PARAMS
)
from exit_engine import (
    run_exit_check, check_systemic_risk_exit,
    DEFAULT_EXIT_PARAMS, DEFAULT_SYSTEMIC_RISK_PARAMS
)


def load_config():
    """加载配置文件。"""
    config_path = os.environ.get("INVASSISTANT_CONFIG")
    if config_path:
        config_path = Path(config_path)
    else:
        config_path = PROJECT_DIR / "invassistant-config.json"

    if not config_path.exists():
        print(f"[警告] 配置文件不存在: {config_path}", file=sys.stderr)
        print(f"[提示] 运行 python scripts/init_config.py 生成默认配置", file=sys.stderr)
        # 返回内置默认配置
        from init_config import DEFAULT_CONFIG
        return DEFAULT_CONFIG

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_signal_report(results, market_detail, timestamp, systemic_risk=None):
    """
    将检查结果格式化为 Markdown 信号报告。

    Args:
        results: 各标的检查结果 dict
        market_detail: 市场环境描述
        timestamp: 检查时间
        systemic_risk: 系统性风险退出检查结果 (level, detail)

    Returns:
        str Markdown 格式的报告
    """
    lines = [
        f"# 持仓信号检查 | {timestamp}",
        "",
        f"**市场环境**: {market_detail}",
        ""
    ]

    # 系统性风险退出预警
    if systemic_risk and systemic_risk[0] != "none":
        level_label = {
            "warning": "⚠️ 预警",
            "panic": "🟠 恐慌",
            "extreme": "🔴 极端"
        }.get(systemic_risk[0], "")
        lines.extend([
            f"**系统性风险**: {level_label} — {systemic_risk[1]}",
            ""
        ])

    lines.extend(["---", ""])

    has_entry_signal = False
    has_exit_signal = False
    entry_items = []
    exit_items = []

    for sym, info in results.items():
        strategy = info.get("strategy", "unknown")
        price = info.get("price", 0)

        if strategy == "redline":
            rl = info.get("redline", {})
            rl1 = "✅" if rl.get("red_line_1", {}).get("passed") else "❌"
            rl2 = "✅" if rl.get("red_line_2", {}).get("passed") else "❌"
            rl3 = "✅" if rl.get("red_line_3", {}).get("passed") else "❌"
            passed = rl.get("all_passed", False)
            action = rl.get("action", "")
            lines.append(f"### {sym} ({info.get('name', '')}) — 三条红线")
            lines.append(f"- 价格: ${price:.2f}")
            lines.append(f"- 情绪释放: {rl1} {rl.get('red_line_1', {}).get('detail', '')}")
            lines.append(f"- 技术止跌: {rl2} {rl.get('red_line_2', {}).get('detail', '')}")
            lines.append(f"- 市场环境: {rl3}")
            lines.append(f"- **建仓: {'✅ ' + action if passed else '❌ ' + action}**")
            if passed:
                has_entry_signal = True
                entry_items.append(f"{sym} 三条红线全通过")

        elif strategy == "hold":
            lines.append(f"### {sym} ({info.get('name', '')}) — 永久HOLD")
            lines.append(f"- 价格: ${price:.2f}")
            lines.append(f"- 操作: 不加不减")

        elif strategy == "pullback":
            pb = info.get("pullback", {})
            signal = pb.get("signal", False)
            detail = pb.get("detail", "")
            lines.append(f"### {sym} ({info.get('name', '')}) — 回调监控")
            lines.append(f"- 价格: ${price:.2f}")
            lines.append(f"- {detail}")
            if signal:
                lines.append(f"- **⚠️ 达到回调阈值，可小加**")
                has_entry_signal = True
                entry_items.append(f"{sym} 回调达标")
            else:
                lines.append(f"- 未达回调阈值，继续HOLD")

        elif strategy == "satellite":
            lines.append(f"### {sym} ({info.get('name', '')}) — 卫星仓")
            lines.append(f"- 价格: ${price:.2f}")
            lines.append(f"- 操作: 不动")

        elif strategy == "trend":
            tl = info.get("trend_entry", {})
            t1 = "✅" if tl.get("trend_1_trend", {}).get("passed") else "❌"
            t2 = "✅" if tl.get("trend_2_breakout", {}).get("passed") else "❌"
            t3 = "✅" if tl.get("trend_3_fundamental", {}).get("passed") else "❌"
            t4 = "✅" if tl.get("trend_4_valuation", {}).get("passed") else "❌"
            passed = tl.get("all_passed", False)
            action = tl.get("action", "")
            lines.append(f"### {sym} ({info.get('name', '')}) — 趋势确认入场")
            lines.append(f"- 价格: ${price:.2f}")
            lines.append(f"- 趋势确立: {t1} {tl.get('trend_1_trend', {}).get('detail', '')}")
            lines.append(f"- 突破确认: {t2} {tl.get('trend_2_breakout', {}).get('detail', '')}")
            lines.append(f"- 基本面支持: {t3} {tl.get('trend_3_fundamental', {}).get('detail', '')}")
            lines.append(f"- 估值检查: {t4} {tl.get('trend_4_valuation', {}).get('detail', '')}")
            lines.append(f"- **建仓: {'✅ ' + action if passed else '❌ ' + action}**")
            if passed:
                has_entry_signal = True
                entry_items.append(f"{sym} 趋势确认全通过")

        # 退出信号
        exit_info = info.get("exit", {})
        if exit_info.get("has_exit_signal"):
            pa = exit_info.get("priority_action", {})
            urgency = pa.get("urgency", "")
            urgency_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(urgency, "")
            lines.append(f"- {urgency_icon} **退出信号: {pa.get('action', '')}**")
            lines.append(f"  - {pa.get('detail', '')}")
            has_exit_signal = True
            exit_items.append(f"{sym} → {pa.get('action', '')}")
        else:
            # 显示退出检查摘要
            checks = exit_info.get("checks", {})
            exit_summaries = []
            for check_name, check_result in checks.items():
                if check_result.get("detail"):
                    short = check_result["detail"]
                    if len(short) > 60:
                        short = short[:60] + "..."
                    exit_summaries.append(short)
            if exit_summaries:
                lines.append(f"- 退出检查: {'；'.join(exit_summaries[:2])}")

        lines.append("")

    # 全组合自检
    lines.extend([
        "---",
        "",
        "## 全组合自检",
        ""
    ])

    # 入场信号
    lines.append("### 📈 入场信号")
    if entry_items:
        for item in entry_items:
            lines.append(f"- 🔔 {item}")
    else:
        lines.append("- 无入场信号")

    # 退出信号
    lines.append("")
    lines.append("### 📉 退出信号")
    if exit_items:
        for item in exit_items:
            lines.append(f"- 🚨 {item}")
    else:
        lines.append("- 无退出信号")

    # 系统性风险
    lines.append("")
    lines.append("### 🛡️ 风险状态")
    if systemic_risk and systemic_risk[0] != "none":
        lines.append(f"- ⚠️ 系统性风险: {systemic_risk[0].upper()} — {systemic_risk[1]}")
    else:
        lines.append("- 系统性风险: 正常")

    has_signal = has_entry_signal or has_exit_signal
    conclusion_parts = []
    if has_entry_signal:
        conclusion_parts.append("存在入场信号")
    if has_exit_signal:
        conclusion_parts.append("存在退出信号")
    if not has_signal:
        conclusion_parts.append("今天不交易")

    lines.append(f"\n**👉 结论: {' + '.join(conclusion_parts)}**")

    return "\n".join(lines)


def run_full_check(config):
    """执行完整的组合检查（入场 + 退出信号）。"""
    portfolio = config.get("portfolio", {})
    watchlist = portfolio.get("watchlist", [])
    market_indicators = portfolio.get("market_indicators", ["QQQ", "^GSPC", "^VIX"])
    vix_threshold = portfolio.get("vix_threshold", 25)
    api_delay = portfolio.get("api_delay", 3)
    api_retries = portfolio.get("api_retries", 3)
    systemic_risk_config = portfolio.get("systemic_risk_exit", {})

    # 收集所有需要获取的标的
    all_symbols = [item["symbol"] for item in watchlist] + market_indicators
    # 去重
    all_symbols = list(dict.fromkeys(all_symbols))

    print(f"\n{'='*60}")
    print(f"持仓交易信号检查 | {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    # 获取数据
    data = fetch_all(all_symbols, delay=api_delay, retries=api_retries)

    # 市场环境检查（入场用）
    market_data = {k: data.get(k) for k in market_indicators}
    market_ok, market_detail = check_market(market_data, {"vix_threshold": vix_threshold})

    # 系统性风险退出检查（全组合层级）
    systemic_level, systemic_detail = check_systemic_risk_exit(
        market_data, systemic_risk_config
    )

    if systemic_level != "none":
        print(f"{'!'*60}")
        level_label = {
            "warning": "⚠️ 预警",
            "panic": "🟠 恐慌",
            "extreme": "🔴 极端"
        }.get(systemic_level, "")
        print(f"🛡️ 系统性风险: {level_label}")
        print(f"   {systemic_detail}")
        print(f"{'!'*60}\n")

    print(f"{'='*60}")
    print(f"📊 今日信号:\n")

    results = {}

    for item in watchlist:
        sym = item["symbol"]
        name = item.get("name", sym)
        strategy = item.get("strategy", "hold")
        params = item.get("params", {})
        exit_params = item.get("exit_params", {})
        df = data.get(sym)
        price = df["Close"].iloc[-1] if df is not None and len(df) > 0 else 0

        result_entry = {
            "symbol": sym,
            "name": name,
            "strategy": strategy,
            "price": float(price)
        }

        # ---- 入场信号检查 ----
        if strategy == "redline":
            rl_result = run_redline_check(df, market_data, params, {"vix_threshold": vix_threshold})
            result_entry["redline"] = rl_result
            rl1 = rl_result["red_line_1"]
            rl2 = rl_result["red_line_2"]
            action = rl_result["action"]
            print(f"{sym:5} | ${price:.2f} | 情绪:{rl1['detail']} 技术:{rl2['detail']} 市场:{market_detail}")
            prefix = "✅" if rl_result["all_passed"] else "❌"
            print(f"     | {rl_result['passed_count']}/3红线 | {prefix} {action}")

        elif strategy == "hold":
            print(f"{sym:5} | ${price:.2f} | 永久HOLD")

        elif strategy == "pullback":
            threshold = params.get("pullback_threshold", 0.06)
            signal, detail, pb_pct = check_pullback(df, threshold)
            result_entry["pullback"] = {"signal": signal, "detail": detail, "pullback_pct": pb_pct}
            action = f"⚠️可小加({pb_pct})" if signal else f"HOLD({pb_pct}未达标)"
            print(f"{sym:5} | ${price:.2f} | {detail} → {action}")

        elif strategy == "satellite":
            print(f"{sym:5} | ${price:.2f} | 卫星不动")

        elif strategy == "trend":
            # 模式B：趋势确认入场
            tl_result = run_trend_check(df, market_data, params, {"vix_threshold": vix_threshold})
            result_entry["trend_entry"] = tl_result
            t1 = tl_result.get("trend_1_trend", {})
            t2 = tl_result.get("trend_2_breakout", {})
            action = tl_result["action"]
            print(f"{sym:5} | ${price:.2f} | 趋势:{t1.get('detail','')} 突破:{t2.get('detail','')}")
            prefix = "✅" if tl_result["all_passed"] else "❌"
            print(f"     | 趋势确认 | {prefix} {action}")

        # ---- 退出信号检查 ----
        exit_result = run_exit_check(df, exit_params)
        result_entry["exit"] = exit_result

        if exit_result["has_exit_signal"]:
            pa = exit_result["priority_action"]
            urgency_icon = {
                "CRITICAL": "🔴",
                "HIGH": "🟠",
                "MEDIUM": "🟡"
            }.get(pa.get("urgency", ""), "")
            print(f"     | {urgency_icon} 退出信号: {pa['action']} | {pa['detail']}")
        else:
            # 简要显示退出状态
            checks = exit_result.get("checks", {})
            cost_basis = exit_params.get("cost_basis", 0)
            if cost_basis > 0:
                gain = (price - cost_basis) / cost_basis * 100
                print(f"     | 浮盈 {gain:+.1f}% (成本${cost_basis:.2f}) | 退出: 无信号")

        # 系统性风险覆盖（对HOLD标的也生效）
        if systemic_level in ("panic", "extreme"):
            if strategy == "hold" and systemic_level == "extreme":
                print(f"     | 🔴 系统性风险覆盖HOLD → 需减仓防守")
            elif strategy != "hold" and systemic_level == "panic":
                print(f"     | 🟠 系统性风险 → 非核心仓需减半")

        results[sym] = result_entry
        print()

    # 全组合自检
    print(f"{'='*60}")
    print("🧠 全组合自检:")

    # 入场信号汇总
    has_redline_signal = any(
        r.get("redline", {}).get("all_passed", False)
        for r in results.values()
        if r["strategy"] == "redline"
    )
    has_trend_signal = any(
        r.get("trend_entry", {}).get("all_passed", False)
        for r in results.values()
        if r["strategy"] == "trend"
    )
    has_pullback_signal = any(
        r.get("pullback", {}).get("signal", False)
        for r in results.values()
        if r["strategy"] == "pullback"
    )

    redline_names = [r["symbol"] for r in results.values() if r.get("redline", {}).get("all_passed")]
    trend_names = [r["symbol"] for r in results.values() if r.get("trend_entry", {}).get("all_passed")]
    pullback_names = [r["symbol"] for r in results.values() if r.get("pullback", {}).get("signal")]

    print(f"\n  📈 入场:")
    print(f"  1️⃣ 情绪错配(模式A): {', '.join(redline_names) if redline_names else '无'}")
    print(f"  2️⃣ 趋势确认(模式B): {', '.join(trend_names) if trend_names else '无'}")
    print(f"  3️⃣ 核心低估: {', '.join(pullback_names) if pullback_names else '无'}")

    # 退出信号汇总
    exit_signals = []
    for r in results.values():
        exit_info = r.get("exit", {})
        if exit_info.get("has_exit_signal"):
            pa = exit_info["priority_action"]
            exit_signals.append(f"{r['symbol']}→{pa['action']}")

    print(f"\n  📉 退出:")
    if exit_signals:
        for es in exit_signals:
            print(f"  🚨 {es}")
    else:
        print(f"  无退出信号")

    print(f"\n  🛡️ 风险:")
    print(f"  3️⃣ 系统风险: {'⚠️' + systemic_level.upper() if systemic_level != 'none' else '正常'}")

    has_entry = has_redline_signal or has_trend_signal or has_pullback_signal
    has_exit = len(exit_signals) > 0
    has_signal = has_entry or has_exit

    conclusion_parts = []
    if has_redline_signal or has_trend_signal:
        conclusion_parts.append("存在入场信号(模式A/B)")
    elif has_pullback_signal:
        conclusion_parts.append("存在回调加仓信号")
    if has_exit:
        conclusion_parts.append("存在退出信号")
    if systemic_level in ("panic", "extreme"):
        conclusion_parts.append("系统性风险防守")
    if not has_signal and systemic_level == "none":
        conclusion_parts.append("不交易")

    print(f"\n👉 结论: {' + '.join(conclusion_parts)}")
    print(f"{'='*60}\n")

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "market_ok": bool(market_ok),
        "market_detail": str(market_detail),
        "systemic_risk": {"level": systemic_level, "detail": systemic_detail},
        "results": results,
        "has_entry_signal": has_entry,
        "has_exit_signal": has_exit,
        "has_signal": has_signal
    }


def run_detail_check(config, symbol):
    """执行单标的详细分析。"""
    portfolio = config.get("portfolio", {})
    market_indicators = portfolio.get("market_indicators", ["QQQ", "^GSPC", "^VIX"])
    vix_threshold = portfolio.get("vix_threshold", 25)

    # 找到标的配置
    item = None
    for w in portfolio.get("watchlist", []):
        if w["symbol"].upper() == symbol.upper():
            item = w
            break

    if item is None:
        print(f"[错误] 标的 {symbol} 不在关注列表中")
        return None

    params = item.get("params", {})

    print(f"{'='*60}")
    print(f"{symbol} 详细信号分析")
    print(f"{'='*60}")

    # 获取数据
    from data_fetcher import fetch_stock
    import time, random

    df = fetch_stock(symbol, days=60)
    if df is None:
        print("[错误] 数据获取失败")
        return None

    price = df["Close"].iloc[-1]
    date = df.index[-1].strftime('%Y-%m-%d')
    print(f"\n📈 当前价格: ${price:.2f} ({date})")
    print(f"📊 近期数据: {len(df)} 个交易日\n")

    # 计算指标
    import pandas as pd
    df_copy = df.copy()
    df_copy['Return'] = df_copy['Close'].pct_change() * 100
    df_copy['MA20'] = df_copy['Close'].rolling(20).mean()
    df_copy['MA50'] = df_copy['Close'].rolling(50).mean()

    # ---- 红线1 详细分析 ----
    print(f"{'='*60}")
    print("🔴 红线1: 情绪释放型下跌")
    print(f"{'='*60}")

    latest_ret = df_copy['Return'].iloc[-1]
    print(f"今日涨跌幅: {latest_ret:.2f}%")

    consec = 0
    for i in range(len(df_copy)-1, 0, -1):
        if df_copy['Return'].iloc[i] < 0:
            consec += 1
        else:
            break
    print(f"连续下跌天数: {consec} 天")

    print(f"\n近5日涨跌幅:")
    for i in range(-5, 0):
        d = df_copy.index[i].strftime('%m-%d')
        r = df_copy['Return'].iloc[i]
        print(f"  {d}: {r:+.2f}%")

    threshold = params.get("emotion_drop_threshold", -4)
    consec_req = params.get("consecutive_days", 3)
    rl1_pass = latest_ret <= threshold or consec >= consec_req
    print(f"\n→ 红线1 {'✅ 通过' if rl1_pass else '❌ 未通过'}")
    print(f"  条件: 单日≥{abs(threshold)}% 或 连跌{consec_req}天")
    print(f"  实际: 今日{latest_ret:.2f}%, 连跌{consec}天")

    # ---- 红线2 详细分析 ----
    print(f"\n{'='*60}")
    print("🔴 红线2: 技术止跌信号")
    print(f"{'='*60}")

    latest = df_copy.iloc[-1]
    prev = df_copy.iloc[-2]
    ma20 = latest['MA20']
    ma50 = latest['MA50']
    close = latest['Close']

    print(f"收盘价: ${close:.2f}")
    if pd.notna(ma20):
        print(f"20日均线: ${ma20:.2f} (偏离 {(close-ma20)/ma20*100:+.2f}%)")
    if pd.notna(ma50):
        print(f"50日均线: ${ma50:.2f} (偏离 {(close-ma50)/ma50*100:+.2f}%)")

    vol = latest['Volume']
    prev_vol = prev['Volume']
    print(f"\n今日成交量: {vol:,.0f}")
    print(f"昨日成交量: {prev_vol:,.0f}")
    print(f"量能变化: {vol/prev_vol*100:.0f}%" if prev_vol > 0 else "量能变化: N/A")

    has_lower_shadow = (latest['Close'] - latest['Low']) > (latest['High'] - latest['Close']) * 1.5
    today_up = latest['Close'] > latest['Open']
    today_return = (latest['Close'] - latest['Open']) / latest['Open'] * 100 if latest['Open'] > 0 else 0
    vol_increase = vol > prev_vol * params.get("volume_ratio", 1.2)
    bounce_th = params.get("bounce_threshold", 1.5)
    strong_bounce = today_return >= bounce_th

    print(f"\n下影线: {'有' if has_lower_shadow else '无'} (止跌承接判据)")
    print(f"今日方向: {'收涨' if today_up else '收跌'} ({today_return:+.2f}%)")
    print(f"放量反弹: {'是' if vol_increase else '否'} (量比:{vol/prev_vol*100:.0f}%)" if prev_vol > 0 else "")
    print(f"强反弹(≥{bounce_th}%): {'是' if strong_bounce else '否'}")

    real_support = has_lower_shadow and today_up and (vol_increase or strong_bounce)
    print(f"→ 真实承接: {'是' if real_support else '否'}")
    if not real_support:
        reasons = []
        if not has_lower_shadow: reasons.append("无下影线")
        if not today_up: reasons.append("收跌")
        if not vol_increase and not strong_bounce: reasons.append(f"反弹力度不足(非放量且涨幅<{bounce_th}%)")
        print(f"  缺失: {', '.join(reasons)}")

    print(f"\n均线距离:")
    if pd.notna(ma20):
        print(f"  MA20偏离: {(close-ma20)/ma20*100:+.2f}% {'(接近)' if abs(close-ma20)/ma20<0.03 else ''}")
    if pd.notna(ma50):
        print(f"  MA50偏离: {(close-ma50)/ma50*100:+.2f}% {'(接近)' if abs(close-ma50)/ma50<0.03 else ''}")
    print(f"  ⚠️ 注意: 接近均线=趋势中性，不等于止跌确认")

    # Higher Low
    print("\n近期低点:")
    lows = []
    for i in range(-15, -1):
        if i > -15 and i < -1:
            try:
                if df_copy['Low'].iloc[i] < df_copy['Low'].iloc[i-1] and df_copy['Low'].iloc[i] < df_copy['Low'].iloc[i+1]:
                    lows.append((df_copy.index[i].strftime('%m-%d'), df_copy['Low'].iloc[i], len(df_copy)+i))
            except IndexError:
                pass
    for d, p_val, _ in lows[-4:]:
        print(f"  {d}: ${p_val:.2f}")

    rl2_pass, rl2_detail = check_tech(df, params)
    print(f"\n→ 红线2 {'✅ 通过' if rl2_pass else '❌ 未通过'}")
    print(f"  信号: {rl2_detail}")

    # ---- 红线3 ----
    print(f"\n{'='*60}")
    print("🔴 红线3: 市场环境")
    print(f"{'='*60}")

    # 获取市场数据
    market_data = {}
    for mi in market_indicators:
        time.sleep(1 + random.uniform(0, 1))
        market_data[mi] = fetch_stock(mi, days=10)

    vix_df = market_data.get("^VIX")
    if vix_df is not None:
        vix_val = vix_df["Close"].iloc[-1]
        print(f"VIX恐慌指数: {vix_val:.2f}")
        print(f"阈值: <{vix_threshold}")
    rl3_pass, rl3_detail = check_market(market_data, {"vix_threshold": vix_threshold})
    print(f"\n→ 红线3 {'✅ 通过' if rl3_pass else '❌ 未通过'}")
    print(f"  {rl3_detail}")

    # ---- 汇总 ----
    print(f"\n{'='*60}")
    print("📋 汇总")
    print(f"{'='*60}")
    passed = sum([rl1_pass, rl2_pass, rl3_pass])
    print(f"红线通过: {passed}/3")
    print(f"\n红线是过滤条件，必须全部通过：")
    all_passed = rl1_pass and rl2_pass and rl3_pass
    if all_passed:
        entry_size = params.get("entry_size", 0.3)
        print(f"✅ 三条红线全部通过 → 可建仓{int(entry_size*100)}%")
    else:
        failed = []
        if not rl1_pass: failed.append("情绪释放❌")
        if not rl2_pass: failed.append("技术止跌❌")
        if not rl3_pass: failed.append("市场环境❌")
        print(f"❌ 不建仓 | 未通过: {', '.join(failed)}")
        if not rl1_pass:
            print(f"\n💡 情绪释放是最关键的红线：")
            print(f"   没有情绪释放 → 没有情绪错配 → 没有入场理由")
            print(f"   当前状态：观察区(Watch)，等待情绪释放触发")

    # ---- 退出信号分析 ----
    exit_params = item.get("exit_params", {})
    if exit_params:
        print(f"\n{'='*60}")
        print("📉 退出信号分析")
        print(f"{'='*60}")

        exit_result = run_exit_check(df, exit_params)

        cost_basis = exit_params.get("cost_basis", 0)
        if cost_basis > 0:
            gain = (price - cost_basis) / cost_basis * 100
            print(f"\n持仓成本: ${cost_basis:.2f}")
            print(f"当前浮盈: {gain:+.1f}%")
        else:
            print(f"\n⚠️ 未配置持仓成本(cost_basis)，止盈/止损检查已跳过")

        checks = exit_result.get("checks", {})

        # 止损
        sl = checks.get("stop_loss", {})
        print(f"\n🔴 止损: {'触发' if sl.get('signal') else '未触发'}")
        print(f"   {sl.get('detail', 'N/A')}")

        # 止盈
        tp = checks.get("take_profit", {})
        print(f"\n🟢 止盈: {'触发' if tp.get('signal') else '未触发'}")
        print(f"   {tp.get('detail', 'N/A')}")

        # 趋势破位
        tb = checks.get("trend_break", {})
        print(f"\n📊 趋势破位: {'触发' if tb.get('signal') else '未触发'}")
        print(f"   {tb.get('detail', 'N/A')}")

        # 动量衰竭
        mf = checks.get("momentum_fade", {})
        print(f"\n📉 动量衰竭: {'触发' if mf.get('signal') else '未触发'}")
        print(f"   {mf.get('detail', 'N/A')}")

        if exit_result.get("has_exit_signal"):
            pa = exit_result["priority_action"]
            urgency_icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡"}.get(pa.get("urgency"), "")
            print(f"\n{urgency_icon} 最高优先级退出信号: {pa['action']}")
            print(f"   {pa['detail']}")
        else:
            print(f"\n✅ 无退出信号")

    return {
        "symbol": symbol,
        "date": date,
        "price": float(price),
        "red_line_1": {"passed": rl1_pass},
        "red_line_2": {"passed": rl2_pass, "detail": rl2_detail},
        "red_line_3": {"passed": rl3_pass, "detail": rl3_detail},
        "all_passed": all_passed,
        "passed_count": passed,
        "exit": exit_result if exit_params else None
    }


def do_push(config, report_text):
    """根据配置推送检查结果。"""
    adapters = config.get("adapters", {})
    pushed = False

    if adapters.get("wechatwork", {}).get("enabled"):
        try:
            from send_wecom import push_signal
            push_signal(report_text, adapters["wechatwork"].get("webhook_url", ""))
            pushed = True
        except Exception as e:
            print(f"[企微推送失败] {e}", file=sys.stderr)

    if adapters.get("dingtalk", {}).get("enabled"):
        try:
            from send_dingtalk import push_signal
            push_signal(report_text,
                       adapters["dingtalk"].get("webhook_url", ""),
                       adapters["dingtalk"].get("secret", ""))
            pushed = True
        except Exception as e:
            print(f"[钉钉推送失败] {e}", file=sys.stderr)

    if adapters.get("feishu", {}).get("enabled"):
        try:
            from send_feishu import push_signal
            push_signal(report_text,
                       adapters["feishu"].get("webhook_url", ""),
                       adapters["feishu"].get("secret", ""))
            pushed = True
        except Exception as e:
            print(f"[飞书推送失败] {e}", file=sys.stderr)

    if not pushed:
        print("[提示] 未配置任何推送渠道，请编辑 invassistant-config.json 中的 adapters 配置")


def main():
    parser = argparse.ArgumentParser(description="InvAssistant 持仓信号检查")
    parser.add_argument("--detail", metavar="SYMBOL", help="单标的详细分析 (如 TSLA)")
    parser.add_argument("--push", action="store_true", help="检查完成后推送结果")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--config", help="配置文件路径")
    args = parser.parse_args()

    if args.config:
        os.environ["INVASSISTANT_CONFIG"] = args.config

    config = load_config()

    if args.detail:
        result = run_detail_check(config, args.detail)
    else:
        check_result = run_full_check(config)

        # 保存 JSON
        output_cfg = config.get("output", {})
        if output_cfg.get("save_json", True):
            output_dir = PROJECT_DIR / output_cfg.get("json_dir", "output")
            output_dir.mkdir(parents=True, exist_ok=True)
            out_file = output_dir / f"portfolio_{datetime.now().strftime('%Y%m%d')}.json"
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(check_result, f, ensure_ascii=False, indent=2, default=str)
            print(f"📁 已保存: {out_file}")

        if args.json:
            print(json.dumps(check_result, ensure_ascii=False, indent=2, default=str))

        # 推送
        if args.push:
            systemic = check_result.get("systemic_risk", {})
            systemic_tuple = (systemic.get("level", "none"), systemic.get("detail", ""))
            report = format_signal_report(
                check_result["results"],
                check_result["market_detail"],
                check_result["timestamp"],
                systemic_risk=systemic_tuple
            )
            do_push(config, report)


if __name__ == "__main__":
    main()
