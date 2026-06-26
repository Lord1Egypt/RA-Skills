#!/usr/bin/env python3
from ipo_data_sources import get_all_ipos
from datetime import datetime, timedelta

# 获取所有新股
all_ipos = get_all_ipos(refresh=False)

if not all_ipos:
    print('获取数据失败')
else:
    today = datetime.now()
    next_30_days = today + timedelta(days=30)
    
    today_str = today.strftime('%Y-%m-%d')
    next_30_str = next_30_days.strftime('%Y-%m-%d')
    
    print(f'📅 未来 30 天新股申购日历 ({today_str} 至 {next_30_str})\n')
    print(f'数据源：{len(all_ipos)} 只新股\n')
    
    # 筛选未来新股
    upcoming = [ipo for ipo in all_ipos if today_str <= ipo['apply_date'] <= next_30_str]
    
    if not upcoming:
        print('📭 未来 30 天暂无已公布的新股')
        print('\n💡 说明：新股发行信息通常提前 1-2 周公布，请届时查询')
    else:
        print(f'✅ 已公布 {len(upcoming)} 只新股\n')
        
        # 按日期分组
        from collections import defaultdict
        by_date = defaultdict(list)
        for ipo in sorted(upcoming, key=lambda x: x['apply_date']):
            by_date[ipo['apply_date']].append(ipo)
        
        for date in sorted(by_date.keys()):
            ipos = by_date[date]
            print(f"\n{date} ({len(ipos)}只):")
            for ipo in ipos:
                price = f"{ipo['issue_price']}元" if ipo['issue_price'] > 0 else '待公布'
                market = ipo.get('market', '未知')
                print(f"  • {ipo['name']} ({ipo['code']}) - {price} - {market}")
