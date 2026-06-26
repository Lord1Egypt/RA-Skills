#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""查询下周新股"""

from ipo_data_sources import get_all_ipos
from datetime import datetime, timedelta

# 获取所有新股
ipos = get_all_ipos(refresh=False)

if not ipos:
    print('获取数据失败')
else:
    # 计算下周日期范围（下周一到周日）
    today = datetime.now()
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7
    next_monday = today + timedelta(days=days_until_monday)
    next_sunday = next_monday + timedelta(days=6)
    
    next_monday_str = next_monday.strftime('%Y-%m-%d')
    next_sunday_str = next_sunday.strftime('%Y-%m-%d')
    
    print(f'📅 下周新股申购日历 ({next_monday_str} 至 {next_sunday_str})\n')
    
    # 筛选下周新股
    next_week_ipos = [ipo for ipo in ipos if next_monday_str <= ipo['apply_date'] <= next_sunday_str]
    
    if not next_week_ipos:
        print('📭 下周暂无可申购新股')
    else:
        for ipo in sorted(next_week_ipos, key=lambda x: x['apply_date']):
            date_str = ipo['apply_date'].split(' ')[0] if ' ' in ipo['apply_date'] else ipo['apply_date']
            price_str = f"{ipo['issue_price']}元" if ipo['issue_price'] > 0 else '待公布'
            print(f"{date_str}: {ipo['name']} ({ipo['code']})")
            print(f"  - 发行价：{price_str}")
            print(f"  - 市场：{ipo['market'] or '未知'}")
            if ipo['industry_pe'] > 0:
                print(f"  - 行业市盈率：{ipo['industry_pe']}倍")
            print()
