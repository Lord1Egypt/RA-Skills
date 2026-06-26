#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股统计分析模块
历史中签率、涨幅统计、新股对比等
"""

from datetime import datetime, timedelta
import json
import os

# ============ 历史新股数据（模拟） ============
# 实际应从数据源获取

HISTORY_IPOS = [
    {
        'code': '301234',
        'name': '科技先锋',
        'apply_date': '2026-02-15',
        'list_date': '2026-02-28',
        'issue_price': 25.50,
        'first_day_close': 42.80,
        'first_day_gain': 67.8,  # 首日涨幅%
        'win_rate': 0.028,  # 中签率%
        'industry': '电子设备',
        'board': '创业板',
    },
    {
        'code': '688123',
        'name': '创新医疗',
        'apply_date': '2026-02-10',
        'list_date': '2026-02-25',
        'issue_price': 38.00,
        'first_day_close': 68.50,
        'first_day_gain': 80.3,
        'win_rate': 0.022,
        'industry': '生物医药',
        'board': '科创板',
    },
    {
        'code': '001567',
        'name': '消费龙头',
        'apply_date': '2026-02-05',
        'list_date': '2026-02-20',
        'issue_price': 18.60,
        'first_day_close': 26.80,
        'first_day_gain': 44.1,
        'win_rate': 0.035,
        'industry': '食品饮料',
        'board': '深市主板',
    },
    {
        'code': '601890',
        'name': '机械重工',
        'apply_date': '2026-01-20',
        'list_date': '2026-02-10',
        'issue_price': 12.50,
        'first_day_close': 16.20,
        'first_day_gain': 29.6,
        'win_rate': 0.045,
        'industry': '机械设备',
        'board': '沪市主板',
    },
    {
        'code': '301456',
        'name': '新能源材料',
        'apply_date': '2026-01-15',
        'list_date': '2026-01-30',
        'issue_price': 32.00,
        'first_day_close': 58.50,
        'first_day_gain': 82.8,
        'win_rate': 0.025,
        'industry': '电力设备',
        'board': '创业板',
    },
]


def get_history_stats(days=90):
    """
    获取历史新股统计
    
    Args:
        days: 统计天数（默认 90 天）
        
    Returns:
        dict: 统计数据
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # 筛选范围内的新股
    recent_ipos = [
        ipo for ipo in HISTORY_IPOS
        if datetime.strptime(ipo['list_date'], '%Y-%m-%d') >= cutoff_date
    ]
    
    if not recent_ipos:
        return None
    
    # 计算统计数据
    total = len(recent_ipos)
    avg_gain = sum(ipo['first_day_gain'] for ipo in recent_ipos) / total
    avg_win_rate = sum(ipo['win_rate'] for ipo in recent_ipos) / total
    
    # 最高涨幅
    max_gain_ipo = max(recent_ipos, key=lambda x: x['first_day_gain'])
    
    # 最低涨幅
    min_gain_ipo = min(recent_ipos, key=lambda x: x['first_day_gain'])
    
    # 行业统计
    by_industry = {}
    for ipo in recent_ipos:
        industry = ipo['industry']
        if industry not in by_industry:
            by_industry[industry] = []
        by_industry[industry].append(ipo)
    
    industry_stats = {}
    for industry, ipos in by_industry.items():
        industry_stats[industry] = {
            'count': len(ipos),
            'avg_gain': round(sum(i['first_day_gain'] for i in ipos) / len(ipos), 1),
            'avg_win_rate': round(sum(i['win_rate'] for i in ipos) / len(ipos), 4),
        }
    
    return {
        'total': total,
        'avg_gain': round(avg_gain, 1),
        'avg_win_rate': round(avg_win_rate * 100, 3),  # 转为百分比
        'max_gain': {
            'name': max_gain_ipo['name'],
            'code': max_gain_ipo['code'],
            'gain': max_gain_ipo['first_day_gain'],
        },
        'min_gain': {
            'name': min_gain_ipo['name'],
            'code': min_gain_ipo['code'],
            'gain': min_gain_ipo['first_day_gain'],
        },
        'by_industry': industry_stats,
    }


def get_industry_ranking():
    """
    获取行业涨幅排行
    
    Returns:
        list: 行业排行列表
    """
    stats = get_history_stats()
    if not stats:
        return []
    
    industry_list = [
        {
            'industry': name,
            'count': data['count'],
            'avg_gain': data['avg_gain'],
            'avg_win_rate': data['avg_win_rate'],
        }
        for name, data in stats['by_industry'].items()
    ]
    
    # 按平均涨幅排序
    industry_list.sort(key=lambda x: x['avg_gain'], reverse=True)
    
    return industry_list


def compare_ipos(codes):
    """
    对比多只新股
    
    Args:
        codes: 股票代码列表
        
    Returns:
        list: 新股对比数据
    """
    result = []
    
    for code in codes:
        # 在历史数据中查找
        ipo = next((i for i in HISTORY_IPOS if i['code'] == code), None)
        
        if ipo:
            result.append({
                'code': ipo['code'],
                'name': ipo['name'],
                'issue_price': ipo['issue_price'],
                'first_day_close': ipo['first_day_close'],
                'first_day_gain': ipo['first_day_gain'],
                'win_rate': ipo['win_rate'],
                'industry': ipo['industry'],
                'board': ipo['board'],
            })
        else:
            # 在当前新股中查找
            from ipo_data_sources import get_all_ipos
            all_ipos = get_all_ipos()
            ipo = next((i for i in all_ipos if i['code'] == code), None)
            
            if ipo:
                result.append({
                    'code': ipo['code'],
                    'name': ipo['name'],
                    'issue_price': ipo['issue_price'],
                    'first_day_close': None,
                    'first_day_gain': None,
                    'win_rate': None,
                    'industry': ipo.get('industry', '未知'),
                    'board': ipo.get('board', '未知'),
                    'status': '未上市',
                })
    
    return result


def export_to_csv(filename='ipo_history.csv'):
    """
    导出历史数据到 CSV
    
    Args:
        filename: 输出文件名
    """
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_IPOS[0].keys())
        writer.writeheader()
        writer.writerows(HISTORY_IPOS)
    
    print(f"已导出到 {filename}")


# ============ 测试入口 ============

if __name__ == "__main__":
    print("=" * 60)
    print("新股统计分析")
    print("=" * 60)
    
    # 历史统计
    stats = get_history_stats(90)
    if stats:
        print(f"\n📊 近 90 天新股统计")
        print(f"  新股数量：{stats['total']}只")
        print(f"  平均涨幅：{stats['avg_gain']}%")
        print(f"  平均中签率：{stats['avg_win_rate']}%")
        print(f"  最高涨幅：{stats['max_gain']['name']} ({stats['max_gain']['gain']}%)")
        print(f"  最低涨幅：{stats['min_gain']['name']} ({stats['min_gain']['gain']}%)")
        
        print(f"\n📈 行业涨幅排行:")
        ranking = get_industry_ranking()
        for i, item in enumerate(ranking, 1):
            print(f"  {i}. {item['industry']}: {item['avg_gain']}% ({item['count']}只)")
    
    # 新股对比
    print(f"\n🔄 新股对比:")
    comparison = compare_ipos(['301234', '688123', '001567'])
    for ipo in comparison:
        print(f"  {ipo['name']} ({ipo['code']}): 发行{ipo['issue_price']}元, "
              f"首日{ipo['first_day_gain']}%, 中签率{ipo['win_rate']*1000:.2f}‰")
