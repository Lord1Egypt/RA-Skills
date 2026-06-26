#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股日内交易 - 自动复盘判断脚本
根据当天行情自动判断交易结果，无需手动输入
"""
import os
import json
import sys
import requests
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, Optional, List

# 配置
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_ROOT, "data")
OUTPUT_DIR = os.path.join(SKILL_ROOT, "output")
PICKS_DIR = os.path.join(OUTPUT_DIR, "picks")


def get_realtime_data_tengxun(stock_code: str) -> Optional[Dict]:
    """获取实时行情数据（腾讯财经API）"""
    # 转换股票代码格式: 09988 -> hk09988
    code = stock_code.strip().upper()
    for suffix in [".HK", "-SW", "-W", "-R", "-P"]:
        if suffix in code:
            code = code.replace(suffix, "")
    
    hk_code = f"hk{code}"
    url = f"https://qt.gtimg.cn/q={hk_code}"
    
    try:
        resp = requests.get(url, timeout=10)
        text = resp.text.strip()
        
        # 解析返回数据
        # 格式: v_hk00700="100~腾讯控股~00700~547.500~..."
        if not text or "v_hk" not in text:
            return None
        
        # 解析字段
        parts = text.split("=")
        if len(parts) < 2:
            return None
        
        # 去掉引号，按~分割
        data_str = parts[1].strip().strip('"')
        fields = data_str.split("~")
        
        if len(fields) < 50:
            return None
        
        # 腾讯财经字段说明：
        # 3: 当前价, 4: 开盘价, 5: 收盘价(昨收), 
        # 33: 最高价, 34: 最低价
        # 38: 成交量, 31: 涨跌幅
        
        price = float(fields[3]) if fields[3] else 0
        high = float(fields[33]) if fields[33] else 0
        low = float(fields[34]) if fields[34] else 0
        volume = float(fields[38]) if fields[38] else 0
        change_pct = float(fields[31]) if fields[31] else 0
        
        # 振幅需要计算
        prev_close = float(fields[5]) if fields[5] else price
        amplitude = ((high - low) / prev_close * 100) if prev_close > 0 else 0
        
        return {
            "price": price,
            "high": high,
            "low": low,
            "volume": volume,
            "change_pct": change_pct,
            "amplitude": round(amplitude, 2),
            "prev_close": prev_close,
        }
        
    except Exception as e:
        print(f"获取行情失败 ({stock_code}): {e}")
    return None


def get_realtime_data(secid: str) -> Optional[Dict]:
    """获取实时行情数据（东方财富API - 备用）"""
    url = "https://push2.eastmoney.com/api/qt/stock/get"
    params = {
        "secid": secid,  # 116.00700 港股
        "fields": "f43,f44,f45,f46,f47,f60,f169,f170,f171,f177"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("data"):
            d = data["data"]
            return {
                "price": d.get("f43", 0) / 1000,      # 当前价
                "high": d.get("f44", 0) / 1000,       # 最高价
                "low": d.get("f45", 0) / 1000,        # 最低价
                "volume": d.get("f47", 0),            # 成交量
                "change_pct": d.get("f170", 0) / 100, # 涨跌幅
                "amplitude": d.get("f177", 0) / 100,  # 振幅
            }
    except Exception as e:
        print(f"东方财富API失败: {e}")
    return None


def convert_stock_code(code: str) -> str:
    """转换股票代码为东方财富格式"""
    # 移除空格和HK后缀
    code = code.strip().upper().replace("HK", "").replace(".HK", "")
    
    # 腾讯控股 -> 00700
    # 阿里巴巴-SW -> 09988
    # 美团-W -> 03690
    # 小米集团-W -> 01810
    
    # 映射表
    mapping = {
        "00700": "116.00700",   # 腾讯控股
        "09988": "116.09988",   # 阿里巴巴-SW
        "03690": "116.03690",   # 美团-W
        "01810": "116.01810",   # 小米集团-W
        "02318": "116.02318",   # 中国平安
        "00939": "116.00939",   # 建设银行
        "00981": "116.00981",   # 中芯国际
        "02018": "116.02018",   # 阿里健康
        "06690": "116.06690",   # 海尔智家
        "03888": "116.03888",   # 金山软件
        "00267": "116.00267",   # 信达生物
        "02269": "116.02269",   # 药明生物
        "00175": "116.00175",   # 吉利汽车
        "01171": "116.01171",   # 矿业资源
        "02628": "116.02628",   # 中国人寿
        "01299": "116.01299",   # 友邦保险
        "01398": "116.01398",   # 工商银行
        "03988": "116.03988",   # 中国银行
        "01880": "116.01880",   # 中国中免
        "00190": "116.00190",   # 中国圣牧
    }
    
    # 处理带后缀的股票代码
    # 例如 09988.HK -> 09988
    for suffix in [".HK", "-SW", "-W", "-R", "-P"]:
        if suffix in code:
            code = code.replace(suffix, "")
    
    secid = mapping.get(code, f"116.{code}")
    return secid


def load_picks(date: str) -> List[Dict]:
    """加载指定日期的选股结果"""
    picks_file = os.path.join(PICKS_DIR, f"picks_{date}.json")
    
    if not os.path.exists(picks_file):
        print(f"选股文件不存在: {picks_file}")
        return []
    
    with open(picks_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get("suggestions", [])


def auto_judge_result(stock_code: str, trade_prices: Dict) -> Dict:
    """
    自动判断交易结果
    
    逻辑：
    1. 如果最低价 > 买入价 -> 没有成交 (no_buy)
    2. 如果最低价 <= 买入价（触发了买入）：
       - 如果最高价 >= 卖出价 -> 止盈卖出 (sell_achieved)
       - 如果最低价 <= 止损价 -> 止损卖出 (stop_loss)
       - 否则 -> 持有到收盘 (hold_to_close)
    """
    # 获取实时行情（优先用腾讯API）
    market_data = get_realtime_data_tengxun(stock_code)
    
    # 备用：东方财富API
    if not market_data:
        secid = convert_stock_code(stock_code)
        market_data = get_realtime_data(secid)
    
    if not market_data:
        return {"error": "无法获取行情数据", "result": "unknown"}
    
    high = market_data["high"]
    low = market_data["low"]
    close = market_data["price"]
    
    # 获取交易价格（兼容 stop_loss 和 stop_loss_price 两种字段名）
    buy_price = trade_prices.get("buy_price")
    sell_target = trade_prices.get("sell_target")
    stop_loss_price = trade_prices.get("stop_loss_price") or trade_prices.get("stop_loss")
    
    if not all([buy_price, sell_target, stop_loss_price]):
        return {"error": "交易价格不完整", "result": "unknown"}
    
    # 判断逻辑
    result = {
        "stock_code": stock_code,
        "market_data": market_data,
        "trade_prices": {
            "buy_price": buy_price,
            "sell_target": sell_target,
            "stop_loss_price": stop_loss_price,
        },
        "result": "unknown",
        "pnl_pct": 0,
        "reason": "",
    }
    
    # 判断结果
    if low > buy_price:
        # 没有触发买入价
        result["result"] = "no_buy"
        result["reason"] = f"最低价{low:.3f} > 买入价{buy_price:.3f}，未触发买入"
        result["pnl_pct"] = 0
    else:
        # 触发了买入
        if high >= sell_target:
            # 达到卖出目标
            result["result"] = "sell_achieved"
            result["pnl_pct"] = round((sell_target - buy_price) / buy_price * 100, 2)
            result["reason"] = f"最高价{high:.3f} >= 卖出目标{sell_target:.3f}，触发止盈"
        elif low <= stop_loss_price:
            # 触发止损
            result["result"] = "stop_loss"
            result["pnl_pct"] = round((stop_loss_price - buy_price) / buy_price * 100, 2)
            result["reason"] = f"最低价{low:.3f} <= 止损价{stop_loss_price:.3f}，触发止损"
        else:
            # 持有到收盘（既没止盈也没止损）
            result["result"] = "hold_to_close"
            result["pnl_pct"] = round((close - buy_price) / buy_price * 100, 2)
            result["reason"] = f"持有到收盘，收盘价{close:.3f}"
    
    return result


def load_performance_data() -> Dict:
    """加载性能追踪数据"""
    perf_file = os.path.join(DATA_DIR, "performance_tracking.json")
    if os.path.exists(perf_file):
        with open(perf_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"version": "1.0", "daily_stats": [], "stock_performance": {}, "summary": {}}


def save_performance_data(data: Dict):
    """保存性能追踪数据"""
    perf_file = os.path.join(DATA_DIR, "performance_tracking.json")
    with open(perf_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_performance_tracking(date: str, result: Dict):
    """更新性能追踪数据"""
    data = load_performance_data()
    
    # 更新 daily_stats
    stat = {
        "date": date,
        "stock": result.get("stock_code", ""),
        "stock_name": result.get("stock_name", ""),
        "result": result["result"],
        "score": result.get("score", 0),
        "pnl_pct": result.get("pnl_pct", 0),
        "reason": result.get("reason", ""),
    }
    
    # 检查是否已存在今天的记录
    existing = [i for i, s in enumerate(data.get("daily_stats", [])) if s.get("date") == date]
    if existing:
        data["daily_stats"][existing[0]] = stat
    else:
        data["daily_stats"].append(stat)
    
    # 更新 summary
    stats = data.get("daily_stats", [])
    total = len(stats)
    no_buy = sum(1 for s in stats if s.get("result") == "no_buy")
    stop_loss = sum(1 for s in stats if s.get("result") == "stop_loss")
    sell_achieved = sum(1 for s in stats if s.get("result") in ["sell_achieved", "hold_to_close"])
    total_buys = stop_loss + sell_achieved
    
    data["summary"] = {
        "total_trading_days": total,
        "total_selections": total,
        "total_buys": total_buys,
        "total_sells_achieved": sell_achieved,
        "total_stop_loss": stop_loss,
        "buy_success_rate_pct": round(sell_achieved / total_buys * 100, 1) if total_buys > 0 else 0,
    }
    
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    
    save_performance_data(data)
    print(f"✅ 已更新性能追踪数据")


def run_auto_review(date: str = None):
    """运行自动复盘"""
    if date is None:
        # 默认昨天
        yesterday = datetime.now() - timedelta(days=1)
        # 跳过周末
        if yesterday.weekday() == 5:  # 周六
            yesterday -= timedelta(days=1)
        elif yesterday.weekday() == 6:  # 周日
            yesterday -= timedelta(days=2)
        date = yesterday.strftime("%Y-%m-%d")
    
    print(f"\n📊 自动复盘 - {date}")
    print("=" * 50)
    
    # 加载选股结果
    picks = load_picks(date)
    
    if not picks:
        print(f"⚠️ {date} 没有选股记录")
        return
    
    print(f"📋 找到 {len(picks)} 只选股记录")
    
    results = []
    for pick in picks:
        stock_code = pick.get("stock_code", "")
        stock_name = pick.get("stock_name", "")
        trade_prices = pick.get("trade_prices", {})
        
        if not trade_prices:
            print(f"⚠️ {stock_code} 没有交易价格信息，跳过")
            continue
        
        print(f"\n🔍 分析: {stock_code} {stock_name}")
        
        # 自动判断结果
        result = auto_judge_result(stock_code, trade_prices)
        result["stock_name"] = stock_name
        result["score"] = pick.get("score", 0)
        
        # 打印结果
        result_emoji = {
            "no_buy": "⏳",
            "sell_achieved": "✅",
            "stop_loss": "🛑",
            "hold_to_close": "📊",
        }
        
        emoji = result_emoji.get(result["result"], "❓")
        print(f"  {emoji} 结果: {result['result']}")
        print(f"  📝 原因: {result['reason']}")
        
        if result["result"] != "no_buy":
            print(f"  💰 盈亏: {result['pnl_pct']}%")
        
        # 更新性能追踪
        update_performance_tracking(date, result)
        results.append(result)
    
    # 汇总
    print("\n" + "=" * 50)
    print("📈 复盘汇总")
    
    result_counts = {}
    for r in results:
        result_counts[r["result"]] = result_counts.get(r["result"], 0) + 1
    
    for result_type, count in result_counts.items():
        emoji = result_emoji.get(result_type, "❓")
        print(f"  {emoji} {result_type}: {count}")
    
    # 生成报告
    generate_review_report(date, results)


def generate_review_report(date: str, results: List[Dict]):
    """生成复盘报告"""
    report_file = os.path.join(OUTPUT_DIR, f"复盘报告_自动_{date}.md")
    
    result_emoji = {
        "no_buy": "⏳",
        "sell_achieved": "✅",
        "stop_loss": "🛑",
        "hold_to_close": "📊",
    }
    
    report = f"""# 📊 港股日内交易复盘报告（自动判断）
📅 日期: {date}
⏰ 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 📈 交易统计

"""
    
    # 统计
    total = len(results)
    no_buy = sum(1 for r in results if r["result"] == "no_buy")
    stop_loss = sum(1 for r in results if r["result"] == "stop_loss")
    sell_achieved = sum(1 for r in results if r["result"] in ["sell_achieved", "hold_to_close"])
    
    if total > 0:
        buy_achieved = total - no_buy
        buy_rate = round(buy_achieved / total * 100, 1) if total > 0 else 0
        sell_rate = round(sell_achieved / buy_achieved * 100, 1) if buy_achieved > 0 else 0
        stop_rate = round(stop_loss / buy_achieved * 100, 1) if buy_achieved > 0 else 0
        
        report += f"| 指标 | 数值 |\n"
        report += f"|------|------|\n"
        report += f"| 选股次数 | {total} |\n"
        report += f"| 买入达成 | {buy_achieved} ({buy_rate}%) |\n"
        report += f"| 卖出达成 | {sell_achieved} ({sell_rate}%) |\n"
        report += f"| 止损触发 | {stop_loss} ({stop_rate}%) |\n"
        
        # 收益率
        total_pnl = sum(r.get("pnl_pct", 0) for r in results)
        avg_pnl = round(total_pnl / total, 2) if total > 0 else 0
        
        report += f"| 总盈亏 | {total_pnl}% |\n"
        report += f"| 平均每笔 | {avg_pnl}% |\n"
    
    report += "\n---\n\n## 📋 详细记录\n\n"
    
    for r in results:
        emoji = result_emoji.get(r["result"], "❓")
        report += f"""### {emoji} {r.get('stock_name', r.get('stock_code', ''))}

- **股票代码**: {r.get('stock_code', '')}
- **交易价格**:
  - 买入价: {r.get('trade_prices', {}).get('buy_price', 'N/A')}
  - 卖出目标: {r.get('trade_prices', {}).get('sell_target', 'N/A')}
  - 止损价: {r.get('trade_prices', {}).get('stop_loss_price', 'N/A')}
- **当日行情**:
  - 最高价: {r.get('market_data', {}).get('high', 'N/A')}
  - 最低价: {r.get('market_data', {}).get('low', 'N/A')}
  - 收盘价: {r.get('market_data', {}).get('price', 'N/A')}
- **判断结果**: {r['result']}
- **盈亏**: {r.get('pnl_pct', 0)}%
- **原因**: {r.get('reason', '')}

---
"""
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 报告已保存到: {report_file}")


if __name__ == "__main__":
    # 获取日期参数
    date = sys.argv[1] if len(sys.argv) > 1 else None
    run_auto_review(date)