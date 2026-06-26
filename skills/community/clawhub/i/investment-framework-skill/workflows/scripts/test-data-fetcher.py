#!/usr/bin/env python3
"""
数据获取层测试脚本

测试各数据源是否正常工作

用法：
    cd investment-framework-skill
    python3 workflows/scripts/test-data-fetcher.py
"""

import sys
import os

# 添加投资框架目录到路径
framework_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, framework_dir)
os.chdir(framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def test_tencent():
    """测试腾讯财经"""
    print("\n" + "="*50)
    print("📊 测试腾讯财经 API")
    print("="*50)
    
    fetcher = DataFetcher()
    
    # 测试个股
    test_symbols = ['600519.SH', '000001.SZ', '300750.SZ']
    
    for symbol in test_symbols:
        try:
            quote = fetcher.get_quote(symbol, use_cache=False)
            print(f"✅ {symbol}: ¥{quote.price} ({quote.change_percent}%) [来源：{quote.source}]")
        except DataFetchError as e:
            print(f"❌ {symbol}: {e}")
    
    # 测试指数
    print("\n测试大盘指数：")
    indices = ['000001.SH', '399001.SZ', '399006.SZ']
    quotes = fetcher.get_indices(indices, use_cache=False)
    
    for quote in quotes:
        print(f"✅ {quote.symbol}: {quote.price} ({quote.change_percent}%)")


def test_sina():
    """测试新浪财经"""
    print("\n" + "="*50)
    print("📊 测试新浪财经 API")
    print("="*50)
    
    # 临时修改配置，优先使用新浪
    from data_fetcher.config import load_config, save_config
    
    config = load_config()
    original_priority = config['data_sources']['priority'].copy()
    config['data_sources']['priority'] = ['sina', 'tencent', 'eastmoney']
    save_config(config)
    
    fetcher = DataFetcher()
    
    test_symbols = ['600519.SH', '000001.SZ']
    
    for symbol in test_symbols:
        try:
            quote = fetcher.get_quote(symbol, use_cache=False)
            print(f"✅ {symbol}: ¥{quote.price} ({quote.change_percent}%) [来源：{quote.source}]")
        except DataFetchError as e:
            print(f"❌ {symbol}: {e}")
    
    # 恢复配置
    config['data_sources']['priority'] = original_priority
    save_config(config)


def test_eastmoney():
    """测试东方财富"""
    print("\n" + "="*50)
    print("📊 测试东方财富 API")
    print("="*50)
    
    fetcher = DataFetcher()
    
    # 测试股价
    symbol = '600519.SH'
    try:
        quote = fetcher.get_quote(symbol, use_cache=False)
        print(f"✅ 股价：¥{quote.price} ({quote.change_percent}%)")
        print(f"   市盈率：{quote.pe}")
        print(f"   市净率：{quote.pb}")
        print(f"   市值：{quote.market_cap / 100000000:.2f}亿")
    except DataFetchError as e:
        print(f"❌ 股价获取失败：{e}")
    
    # 测试财报
    try:
        financials = fetcher.get_financials(symbol, use_cache=False)
        print(f"\n✅ 财报数据（{financials.report_date}）：")
        print(f"   每股收益：{financials.eps}元")
        print(f"   ROE: {financials.roe}%")
        print(f"   资产负债率：{financials.debt_ratio}%")
        print(f"   毛利率：{financials.gross_margin}%")
    except DataFetchError as e:
        print(f"❌ 财报获取失败：{e}")


def test_cache():
    """测试缓存"""
    print("\n" + "="*50)
    print("📊 测试缓存功能")
    print("="*50)
    
    fetcher = DataFetcher()
    
    symbol = '600519.SH'
    
    # 第一次获取（不缓存）
    print("第一次获取（不缓存）...")
    start = datetime.now()
    quote1 = fetcher.get_quote(symbol, use_cache=False)
    elapsed1 = (datetime.now() - start).total_seconds()
    print(f"✅ 耗时：{elapsed1*1000:.0f}ms")
    
    # 第二次获取（使用缓存）
    print("第二次获取（使用缓存）...")
    start = datetime.now()
    quote2 = fetcher.get_quote(symbol, use_cache=True)
    elapsed2 = (datetime.now() - start).total_seconds()
    print(f"✅ 耗时：{elapsed2*1000:.0f}ms")
    if elapsed2 > 0:
        print(f"   加速比：{elapsed1/elapsed2:.1f}x")
    
    # 缓存统计
    stats = fetcher.get_cache_stats()
    print(f"\n📊 缓存统计：")
    print(f"   内存缓存：{stats['memory']['valid']} 条有效")


def main():
    """主函数"""
    print("🚀 投资框架数据获取层测试")
    print(f"⏰ 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_tencent()
        test_sina()
        test_eastmoney()
        test_cache()
        
        print("\n" + "="*50)
        print("✅ 测试完成！")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  测试中断")
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
