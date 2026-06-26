#!/usr/bin/env python3
"""
数据校验脚本

验证多源数据一致性，检测异常值

用法：
    python3 workflows/scripts/verify-data.py
"""

import sys
import os

# 添加投资框架目录到路径
framework_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, framework_dir)
os.chdir(framework_dir)

from data_fetcher import DataFetcher, DataFetchError
from datetime import datetime


def verify_multi_source(fetcher, symbol):
    """
    多源数据校验
    
    从三个数据源获取数据，对比一致性
    """
    print(f"\n🔍 校验 {symbol} 数据一致性")
    print("=" * 50)
    
    results = {}
    
    # 从三个数据源获取
    sources = ['tencent', 'sina', 'eastmoney']
    for source in sources:
        try:
            # 临时修改配置，使用单一数据源
            from data_fetcher.config import load_config, save_config
            config = load_config()
            original = config['data_sources']['priority'].copy()
            config['data_sources']['priority'] = [source]
            save_config(config)
            
            quote = fetcher.get_quote(symbol, use_cache=False)
            results[source] = quote
            
            # 恢复配置
            config['data_sources']['priority'] = original
            save_config(config)
            
            print(f"✅ {source}: ¥{quote.price} ({quote.change_percent}%)")
        except DataFetchError as e:
            print(f"❌ {source}: {e}")
            results[source] = None
    
    # 恢复配置
    from data_fetcher.config import load_config, save_config
    config = load_config()
    config['data_sources']['priority'] = ['eastmoney', 'sina', 'tencent']
    save_config(config)
    
    # 计算中位数
    prices = [q.price for q in results.values() if q is not None]
    if len(prices) >= 2:
        median_price = sorted(prices)[len(prices) // 2]
        print(f"\n📊 中位数价格：¥{median_price}")
        
        # 检查偏差
        for source, quote in results.items():
            if quote and abs(quote.price - median_price) / median_price > 0.02:
                print(f"⚠️  {source} 偏差超过 2%：¥{quote.price} vs ¥{median_price}")
    
    return results


def verify_index_data(fetcher):
    """
    验证大盘指数数据
    """
    print("\n📊 验证大盘指数数据")
    print("=" * 50)
    
    indices = {
        '000001.SH': '上证指数',
        '399001.SZ': '深证成指',
        '399006.SZ': '创业板指',
    }
    
    for symbol, name in indices.items():
        try:
            quote = fetcher.get_quote(symbol, use_cache=False)
            print(f"✅ {name} ({symbol}): {quote.price} ({quote.change_percent}%)")
        except DataFetchError as e:
            print(f"❌ {name} ({symbol}): {e}")


def verify_cache(fetcher):
    """
    验证缓存功能
    """
    print("\n💾 验证缓存功能")
    print("=" * 50)
    
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
    
    if elapsed2 > 0 and elapsed1 > 0:
        print(f"   加速比：{elapsed1/elapsed2:.1f}x")
    
    # 缓存统计
    stats = fetcher.get_cache_stats()
    print(f"\n📊 缓存统计：{stats}")


def main():
    """主函数"""
    print("🔍 投资框架数据校验")
    print(f"⏰ 校验时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    fetcher = DataFetcher()
    
    try:
        # 1. 验证大盘指数
        verify_index_data(fetcher)
        
        # 2. 验证个股数据（多源对比）
        verify_multi_source(fetcher, '600519.SH')
        
        # 3. 验证缓存功能
        verify_cache(fetcher)
        
        print("\n" + "=" * 50)
        print("✅ 数据校验完成！")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  校验中断")
    except Exception as e:
        print(f"\n❌ 校验失败：{e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
