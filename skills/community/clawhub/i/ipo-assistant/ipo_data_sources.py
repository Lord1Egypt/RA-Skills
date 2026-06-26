#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新股数据源聚合模块
支持多个数据源：东方财富、akshare、Tushare
"""

from datetime import datetime, timedelta
import json
import os

# ============ 数据源 1: 东方财富 ============

def fetch_from_dongfangcai():
    """
    从东方财富获取新股申购数据
    
    Returns:
        list: 新股数据列表
    """
    import requests
    
    url = "http://datacenter-web.eastmoney.com/api/data/v1/get"
    params = {
        'reportName': 'RPTA_APP_IPOAPPLY',
        'columns': 'ALL',
        'pageNum': 1,
        'pageSize': 100,  # 增加数量
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
        print(f"[东方财富] 获取数据失败：{e}")
    
    return []


def parse_dongfangcai_data(data):
    """解析东方财富数据"""
    result = []
    
    if 'result' in data and 'data' in data['result']:
        for item in data['result']['data']:
            # 处理日期格式
            apply_date = item.get('APPLY_DATE', '')
            if apply_date and ' ' in apply_date:
                apply_date = apply_date.split(' ')[0]
            
            ipo = {
                'source': '东方财富',
                'code': item.get('SECURITY_CODE', ''),
                'name': item.get('SECURITY_NAME', ''),
                'apply_date': apply_date,
                'issue_price': float(item.get('ISSUE_PRICE', 0) or 0),
                'issue_pe': float(item.get('ISSUE_PE', 0) or 0),
                'industry_pe': float(item.get('INDUSTRY_PE', 0) or 0),
                'online_max': int(item.get('ONLINE_ISSUE_MAX', 0) or 0),
                'total_issue': float(item.get('TOTAL_ISSUE_AMOUNT', 0) or 0),
                'raised_funds': float(item.get('RAISED_FUNDS', 0) or 0),
                'industry': item.get('INDUSTRY_NAME', '') or '未知',
                'board': item.get('BOARD_NAME', '') or '未知',
                'market': item.get('MARKET', '') or '未知',
                'status': '已公布',  # 发行状态
            }
            result.append(ipo)
    
    return result


# ============ 数据源 2: akshare ============

def fetch_from_akshare():
    """
    从 akshare 获取新股数据
    
    需要安装：pip install akshare
    
    Returns:
        list: 新股数据列表
    """
    try:
        import akshare as ak
        
        # 获取新股申购信息
        ipo_info = ak.stock_ipo_summary()
        
        result = []
        for _, row in ipo_info.iterrows():
            ipo = {
                'source': 'akshare',
                'code': row.get('申购代码', ''),
                'name': row.get('股票名称', ''),
                'apply_date': str(row.get('申购日期', '')),
                'issue_price': float(row.get('发行价格', 0) or 0),
                'issue_pe': float(row.get('发行市盈率', 0) or 0),
                'industry_pe': 0,  # akshare 不提供
                'online_max': int(row.get('网上申购上限', 0) or 0),
                'total_issue': float(row.get('发行总量', 0) or 0),
                'raised_funds': float(row.get('募集资金', 0) or 0),
                'industry': row.get('所属行业', '') or '未知',
                'board': row.get('板块', '') or '未知',
                'market': '',
                'status': '已公布',
            }
            result.append(ipo)
        
        return result
    
    except Exception as e:
        print(f"[akshare] 获取数据失败：{e}")
        return []


# ============ 数据源 3: Tushare Pro ============

def fetch_from_tushare():
    """
    从 Tushare Pro 获取新股数据
    
    需要安装：pip install tushare
    需要 token: 从 tushare.pro 注册获取
    
    Returns:
        list: 新股数据列表
    """
    try:
        import tushare as ts
        
        # 读取 token（从配置文件或环境变量）
        token = os.getenv('TUSHARE_TOKEN', '')
        if not token:
            # 尝试从配置文件读取
            config_file = "data/tushare_token.txt"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    token = f.read().strip()
        
        if not token:
            print("[Tushare] 未配置 token，跳过")
            return []
        
        ts.set_token(token)
        pro = ts.pro_api()
        
        # 获取 IPO 信息
        ipo_info = pro.ipo_basic()
        
        result = []
        for _, row in ipo_info.iterrows():
            ipo = {
                'source': 'Tushare',
                'code': row.get('ts_code', '').split('.')[0],
                'name': row.get('name', ''),
                'apply_date': str(row.get('ann_date', '')),
                'issue_price': float(row.get('issue_price', 0) or 0),
                'issue_pe': float(row.get('pe', 0) or 0),
                'industry_pe': 0,
                'online_max': 0,
                'total_issue': float(row.get('total_shares', 0) or 0),
                'raised_funds': float(row.get('raise', 0) or 0),
                'industry': row.get('industry', '') or '未知',
                'board': row.get('board', '') or '未知',
                'market': row.get('market', ''),
                'status': '已公布',
            }
            result.append(ipo)
        
        return result
    
    except Exception as e:
        print(f"[Tushare] 获取数据失败：{e}")
        return []


# ============ 数据聚合 ============

def fetch_all_sources():
    """
    从所有数据源获取数据并合并
    
    Returns:
        list: 合并后的新股列表（去重）
    """
    all_ipos = []
    
    # 1. 东方财富（主要数据源）
    dfc_ipos = fetch_from_dongfangcai()
    all_ipos.extend(dfc_ipos)
    print(f"[数据聚合] 东方财富：{len(dfc_ipos)} 只")
    
    # 2. akshare（补充数据源）
    aks_ipos = fetch_from_akshare()
    all_ipos.extend(aks_ipos)
    print(f"[数据聚合] akshare: {len(aks_ipos)} 只")
    
    # 3. Tushare（可选数据源）
    ts_ipos = fetch_from_tushare()
    all_ipos.extend(ts_ipos)
    print(f"[数据聚合] Tushare: {len(ts_ipos)} 只")
    
    # 去重（按股票代码）
    seen_codes = set()
    unique_ipos = []
    for ipo in all_ipos:
        if ipo['code'] not in seen_codes:
            seen_codes.add(ipo['code'])
            unique_ipos.append(ipo)
    
    print(f"[数据聚合] 去重后：{len(unique_ipos)} 只")
    
    return unique_ipos


# ============ 缓存管理 ============

CACHE_FILE = "data/ipo_cache.json"
CACHE_EXPIRE_HOURS = 12


def load_from_cache():
    """从缓存加载数据"""
    if not os.path.exists(CACHE_FILE):
        return None
    
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        cache_time = datetime.fromisoformat(cache_data['timestamp'])
        if datetime.now() - cache_time < timedelta(hours=CACHE_EXPIRE_HOURS):
            return cache_data['data']
    except Exception as e:
        print(f"[缓存] 读取失败：{e}")
    
    return None


def save_to_cache(data):
    """保存数据到缓存"""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data,
                'sources': list(set(ipo['source'] for ipo in data))
            }, f, ensure_ascii=False, indent=2)
        
        print(f"[缓存] 已保存 {len(data)} 只新股")
    except Exception as e:
        print(f"[缓存] 保存失败：{e}")


# ============ 主功能函数 ============

def get_all_ipos(refresh=False):
    """
    获取所有新股数据
    
    Args:
        refresh: 是否强制刷新（忽略缓存）
        
    Returns:
        list: 新股列表
    """
    if not refresh:
        # 尝试从缓存加载
        cached = load_from_cache()
        if cached:
            print(f"[缓存] 加载 {len(cached)} 只新股")
            return cached
    
    # 从多个数据源获取
    all_ipos = fetch_all_sources()
    
    # 保存到缓存
    if all_ipos:
        save_to_cache(all_ipos)
    
    return all_ipos


# ============ 测试入口 ============

if __name__ == "__main__":
    print("=" * 60)
    print("新股数据源测试")
    print("=" * 60)
    
    all_ipos = get_all_ipos(refresh=True)
    
    if all_ipos:
        print(f"\n✅ 总共获取到 {len(all_ipos)} 只新股\n")
        
        # 按日期排序
        sorted_ipos = sorted(all_ipos, key=lambda x: x['apply_date'])
        
        # 显示前 10 只
        print("最新 10 只新股：")
        for ipo in sorted_ipos[:10]:
            date_str = ipo['apply_date']
            price = f"{ipo['issue_price']}元" if ipo['issue_price'] > 0 else "待公布"
            print(f"  {date_str}: {ipo['name']} ({ipo['code']}) - {price} - [{ipo['source']}]")
    else:
        print("\n❌ 获取数据失败")
