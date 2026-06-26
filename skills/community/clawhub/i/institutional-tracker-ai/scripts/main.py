#!/usr/bin/env python3
"""
机构操盘行为识别算法 v2.0 - 全面使用 Tushare 结构化数据
"""
import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import WEIGHTS, POOL_SIZE, SCORES_DIR, REPORTS_DIR
from data_fetcher import NeoDataFetcher, TushareFetcher
from signal_engine import (
    score_fund_flow, score_volume_price, score_position,
    score_north_margin, score_limit_event,
    compute_total_score, determine_state,
    analyze_intraday_pattern
)
from market_regime import judge_market_regime
from sentiment_aggregator import aggregate_external_sentiment


def get_last_trade_date(ts: TushareFetcher) -> str:
    """获取最近交易日（用来兜底今天盘中数据缺失）"""
    today = datetime.now().strftime("%Y%m%d")
    # 用北向资金接口获取最近有数据的日期
    north = ts.get_north_money(
        (datetime.now() - timedelta(days=5)).strftime("%Y%m%d"), today
    )
    if north:
        return north[0].get("trade_date", today)
    return today


def build_stock_pool(ts: TushareFetcher, neodata: NeoDataFetcher) -> list:
    """构建动态监控池"""
    print("\n📊 Step 1: 构建动态监控池")
    print("=" * 50)

    pool = []
    seen = set()

    # AI链条完整标的池（覆盖算力→芯片→模型→应用全链条）
    core_stocks = [
        # === AI算力/光互联 ===
        ("中际旭创", "300308.SZ", "光模块龙头"),
        ("新易盛", "300502.SZ", "光模块"),
        ("天孚通信", "300394.SZ", "光器件"),
        ("太辰光", "300570.SZ", "光纤连接器"),
        ("华工科技", "000988.SZ", "光模块/激光"),
        # === AI服务器/算力基建 ===
        ("工业富联", "601138.SH", "AI服务器龙头"),
        ("立讯精密", "002475.SZ", "连接器/服务器"),
        ("沪电股份", "002463.SZ", "AI用PCB"),
        ("中国长城", "000066.SZ", "国产服务器"),
        # === AI芯片 ===
        ("寒武纪", "688256.SH", "AI芯片龙头"),
        ("海光信息", "688041.SH", "GPU/DCU龙头"),
        ("中芯国际", "688981.SH", "芯片代工龙头"),
        ("北方华创", "002371.SZ", "半导体设备龙头"),
        ("紫光国微", "002049.SZ", "芯片设计"),
        ("景嘉微", "300474.SZ", "国产GPU"),
        # === AI大模型/平台 ===
        ("科大讯飞", "002230.SZ", "AI语音/大模型"),
        ("金山办公", "688111.SH", "AI办公"),
        # === AI应用/软件 ===
        ("中科创达", "300496.SZ", "AI操作系统"),
        ("虹软科技", "688088.SH", "AI视觉"),
        # === AI+存储 ===
        ("源杰科技", "688498.SH", "光芯片"),
        ("江波龙", "301308.SZ", "存储芯片"),
        # === AI+智能制造 ===
        ("宁德时代", "300750.SZ", "锂电+AI智造"),
        ("比亚迪", "002594.SZ", "智能汽车"),
        ("阳光电源", "300274.SZ", "智能逆变器"),
        # === AI+医疗 ===
        ("迈瑞医疗", "300760.SZ", "医疗器械/AI"),
    ]

    for name, code, sector in core_stocks:
        if code not in seen:
            pool.append({"name": name, "code": code, "sector": sector})
            seen.add(code)

    # 从北向十大成交中补充
    print("  → 获取北向十大成交股...")
    last_td = get_last_trade_date(ts)
    for mtype in ["1", "3"]:  # 沪股通 + 深股通
        top10 = ts.get_hsgt_top10(last_td, mtype)
        for item in top10:
            code = item.get("ts_code", "")
            name = item.get("name", "?")
            if code and code not in seen:
                pool.append({"name": name, "code": code, "sector": "北向热门"})
                seen.add(code)

    print(f"  📋 最终监控池: {len(pool)} 只标的")
    return pool


def analyze_stock(stock: dict, ts: TushareFetcher,
                  north_top10: list, north_global: list,
                  limit_data: list, last_td: str,
                  regime_adjust: float = 0,
                  regime_label: str = "NEUTRAL") -> dict:
    """用 Tushare 结构化数据分析单只股票"""
    name = stock["name"]
    code = stock["code"]

    # 日期范围：最近60个交易日（用于位置分析）
    end_date = last_td
    start_60d = (datetime.strptime(last_td, "%Y%m%d") - timedelta(days=90)).strftime("%Y%m%d")
    start_5d = (datetime.strptime(last_td, "%Y%m%d") - timedelta(days=10)).strftime("%Y%m%d")

    # 1. 获取日线行情（60天）
    daily = ts.get_daily(code, start_60d, end_date)

    # 2. 获取每日指标（量比、换手率、PE）
    daily_basic = ts.get_daily_basic(code, start_5d, end_date)

    # 3. 获取个股资金流向（5天）
    moneyflow = ts.get_moneyflow(code, start_5d, end_date)

    # 4. 获取融资融券
    margin = ts.get_margin(code, start_5d, end_date)

    # 5. 获取日内分钟线（v11新增）
    mins_data = []
    try:
        mins_data = ts.get_mins(code, freq="5min", trade_date=last_td)
    except Exception:
        pass

    # 6. 计算各维度分数
    scores = {}
    scores["fund_flow"] = score_fund_flow(moneyflow, float(daily_basic[0].get("total_mv", 0) or 0) if daily_basic else 0)
    scores["volume_price"] = score_volume_price(daily, daily_basic)
    scores["chip_dist"] = score_position(daily, daily_basic)
    scores["north_margin"] = score_north_margin(north_top10, margin, code, north_global)
    scores["event"] = score_limit_event(limit_data, code, daily, daily_basic, margin)

    # 7. 计算总分
    total_score, details = compute_total_score(scores, WEIGHTS)

    # 8. 日内分钟线加成（v11）
    intraday_score, intraday_reason = analyze_intraday_pattern(mins_data)
    if intraday_score != 0:
        total_score += intraday_score * 0.15  # 日内模式权重15%
        details["intraday"] = {
            "raw_score": intraday_score, "weight": 0.15,
            "weighted_score": round(intraday_score * 0.15, 1),
            "reason": intraday_reason
        }

    # 9. 判定状态（含市场环境调整 + regime过滤）
    state_code, state_name, advice = determine_state(
        total_score, regime_adjust, regime_label,
        daily=daily, moneyflow=moneyflow,
        daily_basic=daily_basic, margin_data=margin)

    # 额外信息
    latest_close = float(daily[0].get("close", 0)) if daily else 0
    latest_chg = float(daily[0].get("pct_chg", 0)) if daily else 0

    return {
        "name": name,
        "code": code,
        "sector": stock["sector"],
        "price": latest_close,
        "change_pct": latest_chg,
        "total_score": total_score,
        "state_code": state_code,
        "state_name": state_name,
        "advice": advice,
        "details": details,
    }


def generate_html_report(results: list, north_data: list, run_date: str, version: str = "v2.0") -> str:
    """生成 HTML 分析报告"""
    results.sort(key=lambda x: x["total_score"], reverse=True)

    buy_signals = [r for r in results if r["state_code"] == "ACCUMULATION"]
    sell_signals = [r for r in results if r["state_code"] == "DISTRIBUTION"]
    markup = [r for r in results if r["state_code"] == "MARKUP"]
    washout = [r for r in results if r["state_code"] == "WASHOUT"]
    caution = [r for r in results if r["state_code"] == "CAUTION"]
    neutral = [r for r in results if r["state_code"] == "NEUTRAL"]

    def score_color(s):
        if s >= 50: return "#B71C1C"
        if s >= 30: return "#C62828"
        if s >= 10: return "#E65100"
        if s >= -20: return "#666"
        return "#1B5E20"

    def chg_color(c):
        return "#C62828" if c > 0 else "#1B5E20" if c < 0 else "#666"

    def render_card(r):
        color = score_color(r["total_score"])
        cc = chg_color(r["change_pct"])
        details_html = ""
        for dim, info in r["details"].items():
            dim_name = {"fund_flow": "资金结构", "volume_price": "量价形态",
                       "chip_dist": "位置分析", "north_margin": "北向+两融",
                       "event": "涨跌停/事件"}.get(dim, dim)
            bw = max(0, min(100, (info["raw_score"] + 100) / 2))
            bc = "#4caf50" if info["raw_score"] > 0 else "#f44336" if info["raw_score"] < 0 else "#999"
            details_html += f'''
            <div style="margin:5px 0;font-size:12px;">
              <div style="display:flex;align-items:center;">
                <span style="width:72px;color:#666;flex-shrink:0;">{dim_name}</span>
                <div style="flex:1;height:7px;background:#f0f0f0;border-radius:4px;margin:0 8px;">
                  <div style="width:{bw}%;height:100%;background:{bc};border-radius:4px;"></div>
                </div>
                <span style="width:40px;text-align:right;font-weight:500;color:{bc};">{info["raw_score"]:+.0f}</span>
              </div>
              <div style="font-size:11px;color:#999;margin-left:80px;line-height:1.4;">{info["reason"]}</div>
            </div>'''

        return f'''
        <div style="border:1px solid #e0e0e0;border-radius:10px;padding:16px;margin-bottom:12px;border-left:4px solid {color};">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div>
              <span style="font-size:16px;font-weight:600;">{r["name"]}</span>
              <span style="font-size:12px;color:#999;margin-left:6px;">{r["code"]}</span>
              <span style="font-size:11px;background:#f0f0f0;padding:2px 8px;border-radius:10px;margin-left:6px;">{r["sector"]}</span>
              <span style="font-size:13px;margin-left:10px;color:{cc};">{r["price"]:.2f} ({r["change_pct"]:+.2f}%)</span>
            </div>
            <div style="text-align:right;">
              <div style="font-size:22px;font-weight:700;color:{color};">{r["total_score"]:+.0f}</div>
              <div style="font-size:12px;">{r["state_name"]}</div>
            </div>
          </div>
          <div style="background:#f8f9fa;padding:8px 12px;border-radius:6px;margin-bottom:10px;font-size:13px;font-weight:500;">
            {r["advice"]}
          </div>
          <details>
            <summary style="cursor:pointer;font-size:12px;color:#666;">查看详细信号 ▾</summary>
            <div style="margin-top:8px;">{details_html}</div>
          </details>
        </div>'''

    sections = ""
    for title, icon, items, color in [
        ("买入信号（机构吸筹·建议持有10日）", "⭐", buy_signals, "#C62828"),
        ("拉升期（持有观望）", "🚀", markup, "#E65100"),
        ("洗盘期（持有/加仓）", "💎", washout, "#F57C00"),
        ("观望区", "⚪", neutral, "#666"),
        ("风险警示（非卖出信号）", "⚠️", caution, "#E65100"),
    ]:
        if items:
            sections += f'<h3 style="color:{color};margin:24px 0 12px;">{icon} {title}</h3>'
            for r in items:
                sections += render_card(r)

    north_html = ""
    if north_data:
        nv = float(north_data[0].get("north_money", 0) or 0)
        nc = "#C62828" if nv > 0 else "#1B5E20"
        ci = sum(1 for d in north_data if float(d.get("north_money", 0) or 0) > 0)
        north_html = f'''
        <div style="background:#f3e5f5;border-radius:8px;padding:12px 16px;margin-bottom:16px;">
          <span style="font-size:13px;font-weight:500;">北向资金：</span>
          <span style="font-size:18px;font-weight:700;color:{nc};">{nv/10000:.2f}亿</span>
          <span style="font-size:12px;color:#666;margin-left:8px;">连续{ci}日净流入</span>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>机构操盘行为识别报告 - {run_date}</title>
<style>
body {{ font-family: -apple-system, "PingFang SC", sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; background: #fff; color: #1a1a1a; }}
h1 {{ font-size: 22px; text-align: center; }}
.sub {{ text-align: center; color: #666; font-size: 13px; margin-bottom: 24px; }}
.grid {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-bottom: 20px; }}
.gi {{ background: #f5f5f5; border-radius: 8px; padding: 12px; text-align: center; }}
.gi .n {{ font-size: 20px; font-weight: 700; }}
.gi .l {{ font-size: 11px; color: #666; }}
.disc {{ background: #fff8e1; border: 1px solid #ffe082; border-radius: 8px; padding: 12px; font-size: 12px; color: #e65100; margin-top: 24px; }}
</style>
</head>
<body>
<h1>🦉 AI链条机构建仓探测报告</h1>
<div class="sub">运行时间: {run_date} | 监控池: {len(results)} 只AI链条龙头 | 建议持有期: 10个交易日 | 止损线: -15% | 算法 v11</div>
<div class="grid">
  <div class="gi"><div class="n" style="color:#C62828;">{len(buy_signals)}</div><div class="l">⭐ 吸筹(买入)</div></div>
  <div class="gi"><div class="n" style="color:#E65100;">{len(markup)}</div><div class="l">🚀 拉升(持有)</div></div>
  <div class="gi"><div class="n" style="color:#F57C00;">{len(washout)}</div><div class="l">💎 洗盘(加仓)</div></div>
  <div class="gi"><div class="n">{len(neutral)}</div><div class="l">⚪ 观望</div></div>
  <div class="gi"><div class="n" style="color:#E65100;">{len(caution)}</div><div class="l">⚠️ 风险警示</div></div>
</div>
{north_html}
{sections}
<div class="disc">
  <strong>重要声明：</strong>本报告由算法自动生成，基于 Tushare 结构化交易数据。
  "机构行为"基于超大单(>100万)/大单(20-100万)分类的统计推断，不代表真实资金身份。
  所有结论仅供参考，不构成任何投资建议。投资有风险，决策需谨慎。
</div>
</body>
</html>'''


def main():
    print("🦉 机构操盘行为识别算法 v5.0 (3轮迭代最终版)")
    print("=" * 55)
    run_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"运行时间: {run_date}")

    ts = TushareFetcher()
    neodata = NeoDataFetcher()

    # 1. 确定最近交易日
    last_td = get_last_trade_date(ts)
    print(f"最近交易日: {last_td}")

    # 2. 全局数据（所有股票共享）
    print("\n📊 获取全局数据...")
    end_d = last_td
    start_d = (datetime.strptime(last_td, "%Y%m%d") - timedelta(days=10)).strftime("%Y%m%d")

    north_global = ts.get_north_money(start_d, end_d)
    if north_global:
        nv = float(north_global[0].get("north_money", 0) or 0)
        print(f"  ✅ 北向资金: {nv/10000:.2f}亿, {len(north_global)}天数据")

    # 北向十大（沪+深合并）
    north_top10 = ts.get_hsgt_top10(last_td, "1") + ts.get_hsgt_top10(last_td, "3")
    print(f"  ✅ 北向十大: {len(north_top10)} 只")

    # 涨跌停
    limit_data = ts.get_limit_list(last_td)
    if limit_data:
        up = sum(1 for x in limit_data if x.get("limit") == "U")
        down = sum(1 for x in limit_data if x.get("limit") == "D")
        print(f"  ✅ 涨跌停: 涨停{up}只, 跌停{down}只")

    # 上证指数（用于市场环境判断）
    print("  → 获取上证指数...")
    start_120d = (datetime.strptime(last_td, "%Y%m%d") - timedelta(days=180)).strftime("%Y%m%d")
    index_daily = ts.get_index_daily("000001.SH", start_120d, end_d)
    if index_daily:
        print(f"  ✅ 上证指数 {len(index_daily)} 天")

    # 获取外部情绪数据 (v3新增)
    print("  → 获取外部情绪数据...")
    external_sentiment = aggregate_external_sentiment(
        include_youtube=True,
        include_eastmoney=True,
        include_news=True,
        include_hot_stocks=True
    )
    sent_score = external_sentiment.get("sentiment_score", 0)
    sent_label = external_sentiment.get("sentiment_label", "?")
    print(f"  ✅ 外部情绪: {sent_label} ({sent_score:+.1f}), 置信度{external_sentiment.get('confidence', 0):.0f}%")
    for src, data in external_sentiment.get("sources", {}).items():
        print(f"     {src}: {data.get('score', 0):+.1f} - {data.get('reason', '')[:40]}")

    # 判断市场环境 (含外部情绪)
    regime = judge_market_regime(index_daily, north_global, limit_data,
                                 external_sentiment=external_sentiment)
    regime_adjust = regime["distribution_threshold_adjust"]
    print(f"\n  🌡️ 市场环境: {regime['regime_label']} (得分:{regime['regime_score']:+d})")
    for k, v in regime["details"].items():
        print(f"     {k}: {v['score']:+.0f} {v['reason']}")

    # 3. 构建监控池
    pool = build_stock_pool(ts, neodata)

    # 4. 逐只分析
    print(f"\n📊 Step 2: 逐只分析 ({len(pool)} 只)")
    print("=" * 55)
    results = []
    for i, stock in enumerate(pool):
        print(f"  [{i+1}/{len(pool)}] {stock['name']:<8} ({stock['code']})...", end="", flush=True)
        try:
            result = analyze_stock(stock, ts, north_top10, north_global, limit_data, last_td, regime_adjust, regime["regime"])
            results.append(result)
            print(f" {result['price']:.2f} {result['change_pct']:+.1f}% → {result['state_name']} ({result['total_score']:+.0f})")
        except Exception as e:
            print(f" ❌ {e}")

    # 5. 生成报告
    print(f"\n📊 Step 3: 生成报告")
    print("=" * 55)
    html = generate_html_report(results, north_global, run_date)

    report_file = REPORTS_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    report_file.write_text(html, encoding="utf-8")
    print(f"  ✅ HTML报告: {report_file}")

    score_file = SCORES_DIR / f"scores_{datetime.now().strftime('%Y%m%d')}.json"
    score_data = [{"name": r["name"], "code": r["code"], "sector": r["sector"],
                   "price": r["price"], "change_pct": r["change_pct"],
                   "total_score": r["total_score"], "state_code": r["state_code"],
                   "details": r["details"]} for r in results]
    score_file.write_text(json.dumps(score_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 摘要
    results.sort(key=lambda x: x["total_score"], reverse=True)
    print(f"\n{'='*55}\n📋 分析摘要\n{'='*55}")
    for r in results:
        icon = {"ACCUMULATION":"⭐","MARKUP":"🚀","WASHOUT":"💎","NEUTRAL":"⚪","DISTRIBUTION":"🔴"}.get(r["state_code"],"?")
        print(f"  {icon} {r['name']:<8} {r['code']:<12} {r['price']:>8.2f} {r['change_pct']:>+6.2f}%  评分:{r['total_score']:>+6.1f}")

    return report_file


if __name__ == "__main__":
    rp = main()
    print(f"\n✅ 完成! 报告: {rp}")
