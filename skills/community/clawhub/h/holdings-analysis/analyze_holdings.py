#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""持仓卖出信号分析
分析持仓股票的卖出时机
"""
import sys
import json
from pathlib import Path

# 添加路径
sys.path.insert(0, 'C:/Users/Administrator/.qclaw/workspace-ag01/skills/trend-launch-scanner')

from trend_scanner import fetch_kline_tencent, add_indicators, calc_score_v2
from sell_signal import calc_sell_score


def analyze_holdings():
    """分析持仓股的卖出信号"""
    holdings_file = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/holdings.json")
    
    if not holdings_file.exists():
        return None
    
    with open(holdings_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        positions = data.get("positions", [])
    
    if not positions:
        return None
    
    results = []
    
    for pos in positions:
        code = pos.get("code")
        name = pos.get("name", code)
        buy_price = pos.get("buy_price")
        buy_date = pos.get("buy_date")
        
        # 获取K线数据
        df = fetch_kline_tencent(code)
        
        result = {
            "code": code,
            "name": name,
            "buy_price": buy_price,
            "buy_date": buy_date,
        }
        
        if df is None or len(df) == 0:
            result["error"] = "获取数据失败"
            results.append(result)
            continue
        
        # 添加指标
        df = add_indicators(df)
        
        # 趋势评分
        trend_score = calc_score_v2(df)
        result["trend_score"] = trend_score["total"]
        
        # 卖出信号
        sell_result = calc_sell_score(df, buy_price, buy_date)
        if sell_result:
            result["sell_score"] = sell_result.get("sell_score", 0)
            result["action"] = sell_result.get("action", "[HOLD]")
            result["close"] = sell_result.get("close", 0)
            result["rsi"] = sell_result.get("rsi", 0)
            result["profit_pct"] = sell_result.get("profit_pct", 0)
            result["hold_days"] = sell_result.get("hold_days", 0)
            result["sell_signals"] = sell_result.get("sell_signals", [])
            result["warning_signals"] = sell_result.get("warning_signals", [])
        
        # 判断操作建议
        sell_score = result.get("sell_score", 0)
        if sell_score >= 40:
            result["suggestion"] = "SELL"  # 建议卖出
        elif sell_score >= 25:
            result["suggestion"] = "WARN"   # 警惕
        else:
            result["suggestion"] = "HOLD"   # 持有
        
        results.append(result)
    
    # 按卖出评分排序
    results.sort(key=lambda x: x.get("sell_score", 0), reverse=True)
    
    return results


def format_holdings_report(results):
    """格式化持仓报告"""
    if not results:
        return None
    
    lines = []
    lines.append("")
    lines.append("━━━━━━━━━━━━━━")
    lines.append("📋 持仓股卖出分析")
    lines.append("")
    
    sell_count = 0
    warn_count = 0
    
    for r in results:
        code = r.get("code", "")
        name = r.get("name", code)
        trend_score = r.get("trend_score", 0)
        sell_score = r.get("sell_score", 0)
        suggestion = r.get("suggestion", "HOLD")
        
        # 图标
        if suggestion == "SELL":
            icon = "🔴"
            sell_count += 1
        elif suggestion == "WARN":
            icon = "🟡"
            warn_count += 1
        else:
            icon = "🟢"
        
        lines.append(f"{icon} {code} {name}")
        
        # 趋势评分和卖出评分
        lines.append(f"   趋势:{trend_score}分 | 卖出信号:{sell_score}分")
        
        # 收益
        profit_pct = r.get("profit_pct")
        if profit_pct is not None:
            profit_str = f"+{profit_pct:.1f}%" if profit_pct > 0 else f"{profit_pct:.1f}%"
            lines.append(f"   收益:{profit_str} | 现价:{r.get('close', 0):.2f}元")
        
        # 信号
        sell_signals = r.get("sell_signals", [])
        warning_signals = r.get("warning_signals", [])
        
        if sell_signals:
            sig_names = [s[0] for s in sell_signals]
            lines.append(f"   [卖出] {', '.join(sig_names)}")
        
        if warning_signals:
            sig_names = [s[0] for s in warning_signals]
            lines.append(f"   [警告] {', '.join(sig_names)}")
        
        lines.append("")
    
    # 汇总
    if sell_count > 0:
        lines.append(f"⚠️ {sell_count}只股票触发卖出信号")
    if warn_count > 0:
        lines.append(f"⚡ {warn_count}只股票需要关注")
    if sell_count == 0 and warn_count == 0:
        lines.append("✅ 持仓趋势良好，继续持有")
    
    return "\n".join(lines)


def save_holdings_report(results):
    """保存持仓报告到文件"""
    if not results:
        return None
    
    report = format_holdings_report(results)
    if report:
        output_file = Path("C:/Users/Administrator/.qclaw/workspace-ag01/data/holdings_analysis.txt")
        output_file.write_text(report, encoding="utf-8")
        return str(output_file)
    return None


def main():
    print("分析持仓股卖出信号...")
    
    results = analyze_holdings()
    
    if results is None:
        print("无持仓数据或文件不存在")
        sys.exit(0)
    
    # 保存报告
    output_file = save_holdings_report(results)
    if output_file:
        print(f"报告已保存: {output_file}")
    
    # 打印报告（只保留ASCII和基本中文）
    report = format_holdings_report(results)
    if report:
        # 只保留ASCII和中文
        import re
        report_clean = re.sub(r'[^\u4e00-\u9fff\u0000-\u007F]', '', report)
        print("\n" + report_clean)
    
    print("完成")
    sys.exit(0)


if __name__ == "__main__":
    main()
