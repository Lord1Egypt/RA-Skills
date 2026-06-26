#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大单与资金流监控系统
功能：异常成交量监控、主力资金流向、大单追踪
"""

from longport.openapi import QuoteContext, Config, SubType, PushQuote
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import json

# ============ 配置 ============
config = Config.from_env()
qctx = QuoteContext(config)

# 监控股票池
WATCHLIST = [
    "700.HK",      # 腾讯
    "9988.HK",     # 阿里
    "3690.HK",     # 美团
    "AAPL.US",     # 苹果
    "NVDA.US",     # 英伟达
    "QQQ.US",      # 纳指 ETF
]

# 大单阈值（股数）
BLOCK_TRADE_THRESHOLD = {
    "HK": 10000,    # 港股 1 万股以上
    "US": 5000,     # 美股 5000 股以上
    "CN": 10000     # A 股 1 万股以上
}

# 异常成交量倍数（相对于平均成交量）
ABNORMAL_VOLUME_MULTIPLIER = 3.0

# ============ 数据结构 ============

class VolumeTracker:
    """成交量追踪器"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.baseline_volume = 0  # 基准成交量
        self.current_volume = 0   # 当前成交量
        self.big_orders = []      # 大单记录
        self.volume_spike = False # 成交量异常
        
    def update_volume(self, volume: int):
        """更新成交量"""
        self.current_volume = volume
        
        # 检测成交量异常
        if self.baseline_volume > 0:
            ratio = self.current_volume / self.baseline_volume
            if ratio > ABNORMAL_VOLUME_MULTIPLIER:
                self.volume_spike = True
    
    def add_big_order(self, order: Dict):
        """记录大单"""
        self.big_orders.append({
            "timestamp": datetime.now().isoformat(),
            **order
        })

# ============ 大单检测 ============

def detect_block_trade(quote: PushQuote, prev_quote: Optional[PushQuote] = None) -> Optional[Dict]:
    """检测大单交易"""
    if not prev_quote:
        return None
    
    # 计算成交量变化
    volume_change = quote.volume - prev_quote.volume
    if volume_change <= 0:
        return None
    
    # 判断市场
    region = "US" if ".US" in quote.symbol else "HK" if ".HK" in quote.symbol else "CN"
    threshold = BLOCK_TRADE_THRESHOLD.get(region, 10000)
    
    # 检测大单
    if volume_change >= threshold:
        # 判断买卖方向
        if quote.last_done > prev_quote.last_done:
            side = "Buy"
        elif quote.last_done < prev_quote.last_done:
            side = "Sell"
        else:
            side = "Unknown"
        
        return {
            "symbol": quote.symbol,
            "side": side,
            "volume": volume_change,
            "price": quote.last_done,
            "amount": quote.last_done * volume_change,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
    
    return None

# ============ 资金流计算 ============

def calculate_money_flow(quotes: List[Dict]) -> Dict:
    """计算资金流向"""
    if not quotes:
        return {"inflow": 0, "outflow": 0, "net_flow": 0}
    
    inflow = 0
    outflow = 0
    
    for i in range(1, len(quotes)):
        prev = quotes[i-1]
        curr = quotes[i]
        
        volume_change = curr.get('volume', 0) - prev.get('volume', 0)
        if volume_change <= 0:
            continue
        
        trade_value = curr['last_done'] * volume_change
        
        # 价格上涨 = 资金流入，价格下跌 = 资金流出
        if curr['last_done'] > prev['last_done']:
            inflow += trade_value
        elif curr['last_done'] < prev['last_done']:
            outflow += trade_value
    
    return {
        "inflow": inflow,
        "outflow": outflow,
        "net_flow": inflow - outflow,
        "flow_ratio": (inflow - outflow) / (inflow + outflow) if (inflow + outflow) > 0 else 0
    }

# ============ 异常检测 ============

def detect_abnormal_activity(symbol: str, current_data: Dict, historical_avg: Dict) -> List[Dict]:
    """检测异常交易活动"""
    alerts = []
    
    # 1. 成交量异常
    if historical_avg.get('volume', 0) > 0:
        volume_ratio = current_data.get('volume', 0) / historical_avg['volume']
        if volume_ratio > ABNORMAL_VOLUME_MULTIPLIER:
            alerts.append({
                "type": "volume_spike",
                "symbol": symbol,
                "message": f"成交量异常：当前{current_data.get('volume', 0):,}股，是均值的{volume_ratio:.1f}倍",
                "severity": "high" if volume_ratio > 5 else "medium"
            })
    
    # 2. 价格波动异常
    if historical_avg.get('volatility', 0) > 0:
        current_volatility = current_data.get('volatility', 0)
        if current_volatility > historical_avg['volatility'] * 2:
            alerts.append({
                "type": "volatility_spike",
                "symbol": symbol,
                "message": f"波动率异常：当前{current_volatility:.2%}，是均值的{current_volatility/historical_avg['volatility']:.1f}倍",
                "severity": "high"
            })
    
    # 3. 大单集中
    if current_data.get('big_order_count', 0) > 10:
        alerts.append({
            "type": "block_trade_cluster",
            "symbol": symbol,
            "message": f"大单集中：1 分钟内{current_data['big_order_count']}笔大单",
            "severity": "high"
        })
    
    return alerts

# ============ 实时监控 ============

class RealTimeMonitor:
    """实时监控器"""
    
    def __init__(self, symbols: List[str]):
        self.symbols = symbols
        self.trackers = {s: VolumeTracker(s) for s in symbols}
        self.prev_quotes = {}
        self.alerts = []
        
    def on_quote(self, symbol: str, quote: PushQuote):
        """行情推送回调"""
        tracker = self.trackers.get(symbol)
        if not tracker:
            return
        
        # 检测大单
        prev_quote = self.prev_quotes.get(symbol)
        block_trade = detect_block_trade(quote, prev_quote)
        
        if block_trade:
            tracker.add_big_order(block_trade)
            self.alerts.append({
                "type": "block_trade",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                **block_trade
            })
            print(f"🚨 大单提醒：{block_trade['side']} {symbol} {block_trade['volume']:,}股 @ {block_trade['price']:.2f}")
        
        # 更新成交量
        tracker.update_volume(quote.volume)
        
        # 检测成交量异常
        if tracker.volume_spike:
            self.alerts.append({
                "type": "volume_spike",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "symbol": symbol,
                "message": f"成交量异常放大"
            })
            print(f"🚨 成交量异常：{symbol}")
            tracker.volume_spike = False  # 重置
        
        self.prev_quotes[symbol] = quote
    
    def get_summary(self) -> Dict:
        """获取监控摘要"""
        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbols": {},
            "total_alerts": len(self.alerts)
        }
        
        for symbol, tracker in self.trackers.items():
            summary["symbols"][symbol] = {
                "current_volume": tracker.current_volume,
                "big_orders": len(tracker.big_orders),
                "total_big_order_volume": sum(o['volume'] for o in tracker.big_orders)
            }
        
        return summary

# ============ 主力动向分析 ============

def analyze_smart_money(symbols: List[str]) -> Dict:
    """分析主力动向"""
    result = {}
    
    for symbol in symbols:
        try:
            # 获取实时行情
            quotes = qctx.quote([symbol])
            if not quotes:
                continue
            
            quote = quotes[0]
            
            # 简化分析：基于价格和成交量变化
            result[symbol] = {
                "price": quote.last_done,
                "volume": quote.volume,
                "change_rate": (quote.last_done - quote.prev_close) / quote.prev_close if quote.prev_close > 0 else 0,
                "smart_money_signal": "unknown",  # 需要更多数据
                "confidence": 0
            }
        
        except Exception as e:
            print(f"❌ 分析 {symbol} 失败：{e}")
    
    return result

# ============ 主函数 ============

if __name__ == "__main__":
    print("💰 大单与资金流监控系统")
    print("=" * 60)
    print(f"监控标的：{', '.join(WATCHLIST)}")
    print(f"大单阈值：港股{BLOCK_TRADE_THRESHOLD['HK']:,}股，美股{BLOCK_TRADE_THRESHOLD['US']:,}股")
    print("=" * 60)
    print()
    
    # 创建监控器
    monitor = RealTimeMonitor(WATCHLIST)
    
    # 设置回调
    def on_quote_callback(symbol: str, quote: PushQuote):
        monitor.on_quote(symbol, quote)
    
    qctx.set_on_quote(on_quote_callback)
    
    # 订阅行情
    print("📡 订阅行情...")
    qctx.subscribe(WATCHLIST, [SubType.Quote], True)
    print("✅ 订阅成功，开始监控...")
    print()
    
    # 运行 60 秒
    try:
        start_time = time.time()
        while time.time() - start_time < 60:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    
    # 显示摘要
    print()
    print("=" * 60)
    print("📊 监控摘要:")
    summary = monitor.get_summary()
    print(f"时间：{summary['timestamp']}")
    print(f"总提醒数：{summary['total_alerts']}")
    print()
    
    for symbol, data in summary['symbols'].items():
        print(f"{symbol}:")
        print(f"  当前成交量：{data['current_volume']:,}股")
        print(f"  大单数：{data['big_orders']}笔")
        print(f"  大单总量：{data['total_big_order_volume']:,}股")
    
    print()
    if monitor.alerts:
        print("🚨 最新提醒:")
        for alert in monitor.alerts[-5:]:
            print(f"  [{alert['timestamp']}] {alert['type']}: {alert.get('symbol', '')} {alert.get('message', '')}")
