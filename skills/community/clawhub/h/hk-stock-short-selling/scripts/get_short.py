#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""获取港股卖空数据"""

import sys
import os

# 添加路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hk_short_selling import HKShortSeller

def main():
    seller = HKShortSeller()
    
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print("""
港股卖空数据获取

用法:
    python get_short.py [股票代码...] [选项]

示例:
    python get_short.py 2513              # 智谱
    python get_short.py 100 700 9988      # 多只
    python get_short.py --all              # 全部
    python get_short.py --top 20           # 前20
        """)
        return
    
    # 排行榜
    if '--top' in args:
        n = 20
        idx = args.index('--top')
        if idx + 1 < len(args):
            try:
                n = int(args[idx + 1])
            except:
                pass
        df = seller.get_top(n=n)
        if not df.empty:
            print(f"\n卖空金额前{n}名:")
            print(df[['stock_code', 'stock_name', 'short_volume', 'short_amount']].to_string(index=False))
        return
    
    # 全部数据
    if '--all' in args:
        df = seller.get_today_data()
        print(f"\n总共 {len(df)} 只股票有卖空数据")
        print(df[['stock_code', 'stock_name', 'short_volume', 'short_amount']].head(20).to_string(index=False))
        return
    
    # 指定股票
    codes = [a for a in args if not a.startswith('-')]
    if codes:
        df = seller.get_today_data(stock_codes=codes)
        if not df.empty:
            print(f"\n找到 {len(df)} 只股票:")
            print(df[['stock_code', 'stock_name', 'short_volume', 'short_amount', 'date']].to_string(index=False))
        else:
            print("未找到这些股票的卖空数据")
            print(f"注意: 港股代码应为5位数字，如 2513")
    else:
        print("请指定股票代码，或使用 --all 查看全部")

if __name__ == '__main__':
    main()
