#!/usr/bin/env python3
"""
Market Data Hub - 使用示例

演示如何使用market-data-hub获取股票行情数据并计算技术指标。
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace/skills/market-data-hub/src')

from market_data_hub import MarketDataHub
import pandas as pd


def demo_realtime_quote():
    """演示：获取实时行情"""
    print("=" * 60)
    print("示例1: 获取实时行情")
    print("=" * 60)
    
    hub = MarketDataHub()
    
    # 股票代码：300502 新易盛
    symbol = '300502'
    
    try:
        # 自动选择数据源
        quote = hub.get_realtime_quote(symbol)
        
        print(f"\n股票代码: {quote['symbol']}")
        print(f"股票名称: {quote.get('name', 'N/A')}")
        print(f"当前价格: {quote['price']:.2f}")
        print(f"涨跌额: {quote.get('change', 0):+.2f}")
        print(f"涨跌幅: {quote.get('change_pct', 0):+.2f}%")
        print(f"成交量: {quote.get('volume', 0):,.0f}")
        print(f"成交额: {quote.get('amount', 0):,.0f}")
        print(f"开盘价: {quote.get('open', 0):.2f}")
        print(f"最高价: {quote.get('high', 0):.2f}")
        print(f"最低价: {quote.get('low', 0):.2f}")
        print(f"昨收价: {quote.get('pre_close', 0):.2f}")
        print(f"数据来源: {quote.get('source', 'unknown')}")
        print(f"时间戳: {quote.get('timestamp', 'N/A')}")
        
    except Exception as e:
        print(f"获取行情失败: {e}")


def demo_kline_data():
    """演示：获取K线数据"""
    print("\n" + "=" * 60)
    print("示例2: 获取K线数据")
    print("=" * 60)
    
    hub = MarketDataHub()
    
    try:
        # 获取日线数据
        df = hub.get_kline(
            symbol='300502',
            period='day',
            start_date='2024-01-01',
            end_date='2024-03-01',
            source='tencent'
        )
        
        print(f"\n获取到 {len(df)} 条K线数据")
        print("\n前5条数据:")
        print(df.head().to_string())
        print("\n后5条数据:")
        print(df.tail().to_string())
        
        # 保存到CSV
        df.to_csv('kline_data.csv', index=False)
        print("\n数据已保存到 kline_data.csv")
        
    except Exception as e:
        print(f"获取K线失败: {e}")


def demo_technical_indicators():
    """演示：计算技术指标"""
    print("\n" + "=" * 60)
    print("示例3: 计算技术指标")
    print("=" * 60)
    
    hub = MarketDataHub()
    
    try:
        # 获取K线数据
        df = hub.get_kline('300502', period='day', 
                          start_date='2024-01-01', 
                          end_date='2024-03-01')
        
        if len(df) < 30:
            print("数据量不足，无法计算指标")
            return
        
        # 为KDJ计算添加high/low列
        if 'high' not in df.columns:
            df['high'] = df['close']
            df['low'] = df['close']
        
        print("\n计算移动平均线...")
        df = hub.calculate_ma(df, periods=[5, 10, 20, 60])
        
        print("计算MACD...")
        df = hub.calculate_macd(df)
        
        print("计算RSI...")
        df = hub.calculate_rsi(df, period=14)
        
        print("计算布林带...")
        df = hub.calculate_bollinger_bands(df)
        
        print("计算KDJ...")
        df = hub.calculate_kdj(df)
        
        # 显示最新数据和指标
        print("\n最新数据及指标:")
        latest = df.iloc[-1]
        
        print(f"\n基础数据:")
        print(f"  日期: {latest.get('date', 'N/A')}")
        print(f"  收盘: {latest['close']:.2f}")
        print(f"  成交量: {latest.get('volume', 0):,.0f}")
        
        print(f"\n均线指标:")
        print(f"  MA5: {latest.get('MA5', 0):.2f}")
        print(f"  MA10: {latest.get('MA10', 0):.2f}")
        print(f"  MA20: {latest.get('MA20', 0):.2f}")
        print(f"  MA60: {latest.get('MA60', 0):.2f}")
        
        print(f"\nMACD指标:")
        print(f"  DIF: {latest.get('MACD_DIF', 0):.4f}")
        print(f"  DEA: {latest.get('MACD_DEA', 0):.4f}")
        print(f"  MACD柱: {latest.get('MACD_HIST', 0):.4f}")
        
        print(f"\nRSI指标:")
        print(f"  RSI(14): {latest.get('RSI', 0):.2f}")
        
        print(f"\n布林带:")
        print(f"  上轨: {latest.get('BB_UPPER', 0):.2f}")
        print(f"  中轨: {latest.get('BB_MIDDLE', 0):.2f}")
        print(f"  下轨: {latest.get('BB_LOWER', 0):.2f}")
        
        print(f"\nKDJ指标:")
        print(f"  K值: {latest.get('KDJ_K', 0):.2f}")
        print(f"  D值: {latest.get('KDJ_D', 0):.2f}")
        print(f"  J值: {latest.get('KDJ_J', 0):.2f}")
        
        # 交易信号分析
        print("\n信号分析:")
        
        # MACD金叉死叉
        if latest.get('MACD_golden_cross', False):
            print("  [信号] MACD金叉 - 买入信号")
        elif latest.get('MACD_death_cross', False):
            print("  [信号] MACD死叉 - 卖出信号")
        
        # RSI超买超卖
        if latest.get('RSI_overbought', False):
            print("  [信号] RSI超买 - 注意回调风险")
        elif latest.get('RSI_oversold', False):
            print("  [信号] RSI超卖 - 可能存在反弹机会")
        
        # 价格与均线关系
        if latest['close'] > latest.get('MA20', 0):
            print("  [趋势] 价格在MA20之上，中期趋势向上")
        else:
            print("  [趋势] 价格在MA20之下，中期趋势向下")
        
        # 保存带指标的数据
        df.to_csv('kline_with_indicators.csv', index=False)
        print("\n带指标的数据已保存到 kline_with_indicators.csv")
        
    except Exception as e:
        print(f"计算指标失败: {e}")
        import traceback
        traceback.print_exc()


def demo_batch_quotes():
    """演示：批量获取行情"""
    print("\n" + "=" * 60)
    print("示例4: 批量获取行情")
    print("=" * 60)
    
    hub = MarketDataHub()
    
    # 多只股票
    symbols = ['300502', '600519', '000858', '002594']
    
    try:
        quotes = hub.get_batch_quotes(symbols, source='tencent')
        
        print(f"\n成功获取 {len(quotes)} 只股票行情:")
        print("\n代码\t\t名称\t\t价格\t\t涨跌幅")
        print("-" * 60)
        
        for quote in quotes:
            print(f"{quote['symbol']}\t\t{quote.get('name', 'N/A')[:6]:<8}\t"
                  f"{quote['price']:>8.2f}\t{quote.get('change_pct', 0):>+7.2f}%")
        
    except Exception as e:
        print(f"批量获取失败: {e}")


def demo_usage_stats():
    """演示：使用统计"""
    print("\n" + "=" * 60)
    print("示例5: 使用统计")
    print("=" * 60)
    
    hub = MarketDataHub()
    
    # 执行一些操作
    try:
        hub.get_realtime_quote('300502')
        hub.get_realtime_quote('600519')
    except:
        pass
    
    # 获取统计
    stats = hub.get_usage_stats()
    
    print("\n数据源使用统计:")
    print(f"{'数据源':<12} {'请求次数':>10} {'失败次数':>10}")
    print("-" * 40)
    
    for source in ['tencent', 'akshare', 'baostock']:
        requests = stats['requests'].get(source, 0)
        failures = stats['failures'].get(source, 0)
        print(f"{source:<12} {requests:>10} {failures:>10}")


def demo_custom_config():
    """演示：自定义配置"""
    print("\n" + "=" * 60)
    print("示例6: 自定义配置")
    print("=" * 60)
    
    # 自定义限流配置
    rate_limits = {
        'tencent': {'rate': 5.0, 'capacity': 50},   # 更宽松的限制
        'akshare': {'rate': 1.0, 'capacity': 20}
    }
    
    # 自定义数据源优先级
    source_priority = ['akshare', 'tencent', 'baostock']
    
    hub = MarketDataHub(
        rate_limits=rate_limits,
        source_priority=source_priority,
        enable_rate_limit=True,
        enable_retry=True,
        enable_circuit_breaker=True
    )
    
    print("\n自定义配置已启用:")
    print(f"  数据源优先级: {source_priority}")
    print(f"  腾讯限流: 5次/秒, 容量50")
    print(f"  AKShare限流: 1次/秒, 容量20")
    
    # 获取可用数据源
    available = hub.get_available_sources()
    print(f"\n可用数据源: {available}")


def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Market Data Hub - 使用示例")
    print("=" * 60)
    
    # 运行所有示例
    demo_realtime_quote()
    demo_kline_data()
    demo_technical_indicators()
    demo_batch_quotes()
    demo_usage_stats()
    demo_custom_config()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
