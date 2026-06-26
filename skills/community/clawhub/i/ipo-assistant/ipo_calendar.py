#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股申购日历模块 - 多数据源
获取可申购新股列表
数据来源：东方财富、akshare、Tushare
"""

from datetime import datetime, timedelta
from ipo_data_sources import get_all_ipos, load_from_cache, save_to_cache


def fetch_from_dongfangcai():
    """
    从东方财富获取新股申购数据
    
    API 端点：
    http://datacenter-web.eastmoney.com/api/data/v1/get
    ?reportName=RPTA_APP_IPOAPPLY
    &columns=ALL
    &pageNum=1&pageSize=50
    
    Returns:
        list: 新股数据列表
    """
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'reportName': 'RPTA_APP_IPOAPPLY',
        'columns': 'ALL',
        'pageNum': 1,
        'pageSize': 50,
        'sortColumns': 'APPLY_DATE',
        'sortTypes': '-1',
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'http://data.eastmoney.com/xg/xg/default.html',
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return parse_dongfangcai_data(data)
    except Exception as e:
        print(f"获取东方财富数据失败：{e}")
    
    return None


def parse_dongfangcai_data(data):
    """
    解析东方财富数据
    
    Args:
        data: API 返回的 JSON 数据
        
    Returns:
        list: 解析后的新股列表
    """
    result = []
    
    if 'result' in data and 'data' in data['result']:
        for item in data['result']['data']:
            # 只处理尚未上市的新股
            if item.get('LISTING_DATE') and item.get('LISTING_DATE') != '':
                continue
            
            # 处理日期格式（去除时间部分）
            apply_date = item.get('APPLY_DATE', '')
            if apply_date and ' ' in apply_date:
                apply_date = apply_date.split(' ')[0]
            
            ipo = {
                'code': item.get('SECURITY_CODE', ''),
                'name': item.get('SECURITY_NAME', ''),
                'apply_date': apply_date,  # 申购日期
                'issue_price': float(item.get('ISSUE_PRICE', 0) or 0),  # 发行价
                'issue_pe': float(item.get('ISSUE_PE', 0) or 0),  # 发行市盈率
                'industry_pe': float(item.get('INDUSTRY_PE', 0) or 0),  # 行业市盈率
                'online_max': int(item.get('ONLINE_ISSUE_MAX', 0) or 0),  # 网上申购上限
                'total_issue': float(item.get('TOTAL_ISSUE_AMOUNT', 0) or 0),  # 发行总量（万股）
                'raised_funds': float(item.get('RAISED_FUNDS', 0) or 0),  # 募集资金（亿元）
                'industry': item.get('INDUSTRY_NAME', '') or '未知',  # 行业
                'board': item.get('BOARD_NAME', '') or '未知',  # 板块
                'market': item.get('MARKET', ''),  # 市场（SH/SZ）
            }
            result.append(ipo)
    
    return result


# ============ 数据缓存 ============

CACHE_FILE = "data/ipo_cache.json"
CACHE_EXPIRE_HOURS = 12  # 缓存 12 小时


def load_from_cache():
    """从缓存加载数据"""
    import os
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # 检查缓存是否过期
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - cache_time < timedelta(hours=CACHE_EXPIRE_HOURS):
            return cache_data['data']
    except Exception as e:
        print(f"读取缓存失败：{e}")
    
    return None


def save_to_cache(data):
    """保存数据到缓存"""
    import os
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存缓存失败：{e}")


# ============ 主功能函数 ============

def get_today_ipos(date=None):
    """
    获取指定日期可申购新股
    
    Args:
        date: 日期字符串 YYYY-MM-DD，默认今天
        
    Returns:
        list: 新股列表，带申购建议
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 从多个数据源获取（自动处理缓存）
    all_ipos = get_all_ipos(refresh=False)
    
    # 如果获取失败，返回空列表
    if not all_ipos:
        return []
    
    # 筛选今日新股
    today_ipos = [ipo for ipo in all_ipos if ipo['apply_date'] == date]
    
    # 添加申购建议
    result = []
    for ipo in today_ipos:
        ipo_with_recommendation = ipo.copy()
        ipo_with_recommendation['recommendation'] = get_recommendation(ipo)
        result.append(ipo_with_recommendation)
    
    return result


def get_week_ipos(start_date=None, end_date=None):
    """
    获取新股申购日历
    
    Args:
        start_date: 开始日期 YYYY-MM-DD
        end_date: 结束日期 YYYY-MM-DD
        
    Returns:
        list: 日历数据
    """
    if start_date is None:
        start_date = datetime.now().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # 扩展到 2 周
    
    # 从多个数据源获取
    all_ipos = get_all_ipos(refresh=False)
    
    if not all_ipos:
        return []
    
    # 筛选日期范围内的
    result = []
    for ipo in all_ipos:
        ipo_date = ipo['apply_date']
        if start_date <= ipo_date <= end_date:
            result.append({
                'date': ipo_date,
                'code': ipo['code'],
                'name': ipo['name'],
                'price': ipo['issue_price'],
                'board': ipo['board'],
                'market': ipo.get('market', ''),
            })
    
    # 按日期排序
    result.sort(key=lambda x: x['date'])
    
    return result


def get_recommendation(ipo):
    """
    获取申购建议
    
    Args:
        ipo: 新股数据
        
    Returns:
        str: 申购建议
    """
    # 计算估值优势
    if ipo['industry_pe'] > 0:
        pe_ratio = ipo['issue_pe'] / ipo['industry_pe']
    else:
        pe_ratio = 1.0
    
    # 判断建议
    if pe_ratio < 0.8 and ipo['total_issue'] < 20:
        return "⭐⭐⭐ 积极申购（估值低 + 规模小）"
    elif pe_ratio < 0.9:
        return "⭐⭐ 建议申购（估值合理）"
    elif pe_ratio < 1.0:
        return "⭐ 谨慎申购（估值偏高）"
    else:
        return "⚠️ 不建议申购（估值过高）"


# ============ 测试入口 ============

if __name__ == "__main__":
    print("从东方财富获取新股数据...")
    ipos = fetch_from_dongfangcai()
    
    if ipos:
        print(f"获取到 {len(ipos)} 只新股\n")
        for ipo in ipos[:5]:  # 显示前 5 只
            print(f"{ipo['name']} ({ipo['code']})")
            print(f"  申购日期：{ipo['apply_date']}")
            print(f"  发行价：{ipo['issue_price']}元")
            print(f"  发行市盈率：{ipo['issue_pe']}倍")
            print(f"  行业：{ipo['industry']}")
            print()
    else:
        print("获取数据失败")
