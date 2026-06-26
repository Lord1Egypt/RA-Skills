#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
长桥 OpenAPI 实时行情监控脚本
监控指定股票的价格变化，支持价格突破提醒
"""

from longport.openapi import QuoteContext, Config, SubType, PushQuote
from dotenv import load_dotenv
from datetime import datetime
import time
import os

# 加载环境变量
load_dotenv()

# ============ 配置区域 ============
# 监控的股票列表
WATCHLIST = [
    "QQQ.US",      # 纳斯达克 100 ETF
    "NVDA.US",     # 英伟达
    "AAPL.US",     # 苹果
    "TSLA.US",     # 特斯拉
    "AMD.US",      # AMD
    "MSFT.US",     # 微软
    "700.HK",      # 腾讯控股
]

# 关键价位（用于突破提醒）
KEY_LEVELS = {
    "QQQ.US": {"support": 605, "resistance": 610},
    "NVDA.US": {"support": 175, "resistance": 180},
}

# ============ 回调函数 ============
def on_quote(symbol: str, quote: PushQuote):
    """实时行情推送回调"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # 基础信息
    last_done = quote.last_done
    change = quote.change if hasattr(quote, 'change') else 0
    change_rate = quote.change_rate if hasattr(quote, 'change_rate') else 0
    volume = quote.volume if hasattr(quote, 'volume') else 0
    high = quote.high if hasattr(quote, 'high') else 0
    low = quote.low if hasattr(quote, 'low') else 0
    
    # 格式化输出
    change_str = f"+{change:.2f}" if change >= 0 else f"{change:.2f}"
    change_rate_str = f"+{change_rate:.2%}" if change_rate >= 0 else f"{change_rate:.2%}"
    
    print(f"[{timestamp}] {symbol:10} | 最新：{last_done:8.2f} | 涨跌：{change_str:8} ({change_rate_str:8}) | 高：{high:.2f} | 低：{low:.2f} | 量：{volume/1000000:.2f}M")
    
    # 检查关键价位突破
    if symbol in KEY_LEVELS:
        levels = KEY_LEVELS[symbol]
        
        if last_done >= levels["resistance"]:
            print(f"  ⚠️  【突破阻力位】{symbol} 突破 ${levels['resistance']}！")
        
        if last_done <= levels["support"]:
            print(f"  ⚠️  【跌破支撑位】{symbol} 跌破 ${levels['support']}！")

def main():
    """主函数"""
    print()
    print("📈 长桥 OpenAPI 实时行情监控")
    print("=" * 80)
    print(f"监控标的：{', '.join(WATCHLIST)}")
    print(f"开始时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    print()
    
    # 加载配置
    config = Config.from_env()
    
    # 创建行情上下文
    ctx = QuoteContext(config)
    
    # 设置回调函数
    ctx.set_on_quote(on_quote)
    
    # 订阅行情
    print("正在订阅行情...")
    ctx.subscribe(WATCHLIST, [SubType.Quote], True)
    print("✅ 订阅成功！开始接收实时行情推送...")
    print()
    print("-" * 80)
    
    # 保持运行，接收推送
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("-" * 80)
        print("停止监控，正在断开连接...")
        print("✅ 已断开连接")

if __name__ == "__main__":
    main()
