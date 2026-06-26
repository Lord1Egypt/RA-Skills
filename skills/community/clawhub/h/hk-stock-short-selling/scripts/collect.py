#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""采集并保存历史卖空数据"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hk_short_selling import HKShortSeller
from datetime import datetime

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始采集港股卖空数据...")
    
    seller = HKShortSeller()
    
    # 获取当天数据
    df = seller.get_today_data()
    
    if df.empty:
        print("未获取到数据")
        return
    
    print(f"获取到 {len(df)} 条记录")
    
    # 保存
    if seller.save_today():
        print("历史数据已保存")
    else:
        print("保存失败")

if __name__ == '__main__':
    main()
