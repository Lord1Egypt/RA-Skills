#!/usr/bin/env python3
from ipo_calendar import fetch_from_dongfangcai

ipos = fetch_from_dongfangcai()

if not ipos:
    print('获取数据失败')
else:
    print(f'✅ 总共获取到 {len(ipos)} 只新股\n')
    print('按申购日期排序：\n')
    for ipo in sorted(ipos, key=lambda x: x['apply_date']):
        date_str = ipo['apply_date'].split(' ')[0] if ' ' in ipo['apply_date'] else ipo['apply_date']
        price = f"{ipo['issue_price']}元" if ipo['issue_price'] > 0 else '待公布'
        print(f"{date_str}: {ipo['name']} ({ipo['code']}) - 发行价{price} - {ipo['market']}")
