#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深交所 (SZSE) 数据源模块
API 基础地址: https://www.szse.cn/
"""

import io
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import requests
import logging
import os
import pickle
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

# 深交所API基础地址
SZSE_BASE_URL = 'https://www.szse.cn'
SZSE_API_REPORT = f'{SZSE_BASE_URL}/api/report/ShowReport/data'
SZSE_API_ANNOUNCE = f'{SZSE_BASE_URL}/api/disc/announcement/annList'

SZSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.szse.cn/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
}

# CATALOGID 映射
CATALOG_MAP = {
    'a_stock_list': '1110',       # A股列表
    'index_quote': '1850',        # 指数行情
    'market_overview': '1803',    # 市场总貌
    'fund_list': '1218',          # 基金列表
    'bond_list': '1212',          # 债券列表
}


class SZSEFetcher:
    """深交所数据获取器"""

    def __init__(self, cache_dir=None):
        self.session = requests.Session()
        self.session.headers.update(SZSE_HEADERS)
        self.cache_dir = cache_dir or os.path.join(os.path.dirname(__file__), 'cache', 'szse')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, key):
        return os.path.join(self.cache_dir, f'{key}.pkl')

    def _load_cache(self, key, expire_hours=6):
        path = self._get_cache_path(key)
        if not os.path.exists(path):
            return None
        if datetime.now() - datetime.fromtimestamp(os.path.getmtime(path)) > timedelta(hours=expire_hours):
            return None
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    def _save_cache(self, key, data):
        try:
            with open(self._get_cache_path(key), 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.warning(f"保存缓存失败: {e}")

    def _fetch_report(self, catalog_id, page_no=1, page_count=20, cache_key=None, expire_hours=6):
        """获取报告数据"""
        if cache_key:
            cached = self._load_cache(cache_key, expire_hours)
            if cached is not None:
                return cached

        params = {
            'SHOWTYPE': 'JSON',
            'CATALOGID': catalog_id,
            'TABKEY': 'tab1',
            'PAGENO': str(page_no),
            'PAGECOUNT': str(page_count),
        }
        try:
            resp = self.session.get(SZSE_API_REPORT, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if len(data) > 0 and 'data' in data[0]:
                    if cache_key:
                        self._save_cache(cache_key, data)
                    return data
            return None
        except Exception as e:
            logger.warning(f"深交所报告获取失败: {e}")
            return None

    def get_a_stock_list(self, page_no=1, page_count=100):
        """
        获取深交所A股列表
        返回: list of dict, 包含代码、简称、上市日期、总股本、流通股本等
        """
        cache_key = f'a_stock_p{page_no}'
        data = self._fetch_report(CATALOG_MAP['a_stock_list'], page_no, page_count, cache_key)
        if not data:
            return []

        result = data[0]
        metadata = result.get('metadata', {})
        records = result.get('data', [])

        stocks = []
        for item in records:
            # 提取股票代码和简称（去除HTML标签）
            code = item.get('agdm', '')
            name_html = item.get('agjc', '')
            name = re.sub(r'<[^>]+>', '', name_html) if name_html else ''

            stocks.append({
                'code': code,
                'name': name,
                'list_date': item.get('agssrq', ''),
                'total_shares': item.get('agzgb', ''),  # 总股本(亿股)
                'float_shares': item.get('agltgb', ''),  # 流通股本(亿股)
                'industry': item.get('sshymc', ''),      # 所属行业
            })

        return {
            'stocks': stocks,
            'total': metadata.get('recordcount', 0),
            'page': metadata.get('pageno', 0),
            'page_count': metadata.get('pagecount', 0),
        }

    def get_all_a_stocks(self, batch_size=100):
        """获取全部深交所A股（自动分页）"""
        first = self.get_a_stock_list(page_no=1, page_count=batch_size)
        if not first['stocks']:
            return []

        all_stocks = first['stocks'][:]
        total_pages = first['page_count']

        for page in range(2, total_pages + 1):
            result = self.get_a_stock_list(page_no=page, page_count=batch_size)
            if result['stocks']:
                all_stocks.extend(result['stocks'])
            else:
                break

        logger.info(f"深交所A股列表获取完成: {len(all_stocks)} 只")
        return all_stocks

    def get_index_quote(self):
        """获取深市指数行情"""
        cache_key = 'index_quote'
        data = self._fetch_report(CATALOG_MAP['index_quote'], 1, 20, cache_key, expire_hours=1)
        if not data:
            return []

        records = data[0].get('data', [])
        indices = []
        for item in records:
            indices.append({
                'name': item.get('zwmc', item.get('ywmc', '')),
                'code': item.get('zsdm', ''),
                'open': item.get('qss', ''),
                'high': item.get('zg', ''),
                'low': item.get('zd', ''),
                'close': item.get('ss', ''),
                'change_pct': item.get('sdf', ''),
                'amount': item.get('cjje', ''),
            })
        return indices

    def get_announcements(self, stock_code=None, start_date=None, end_date=None,
                          page_no=1, page_size=10):
        """
        获取公告列表
        stock_code: 股票代码，如 '000858'
        """
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        payload = {
            'seDate': [start_date, end_date],
            'channelCode': ['listedNotice_disc'],
            'pageNum': page_no,
            'pageSize': page_size,
        }
        if stock_code:
            payload['stock'] = [stock_code]

        try:
            resp = self.session.post(SZSE_API_ANNOUNCE, json=payload, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'total': data.get('announceCount', 0),
                    'announcements': data.get('data', []),
                }
            return None
        except Exception as e:
            logger.warning(f"深交所公告获取失败: {e}")
            return None

    def download_announcement_pdf(self, attach_path, save_dir=None):
        """
        下载公告PDF
        attach_path: 如 '/disc/disk03/finalpage/2026-04-30/xxx.PDF'
        """
        if not save_dir:
            save_dir = os.path.join(self.cache_dir, 'pdfs')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        filename = os.path.basename(attach_path)
        save_path = os.path.join(save_dir, filename)

        if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            return save_path

        url = f'{SZSE_BASE_URL}{attach_path}'
        try:
            resp = self.session.get(url, timeout=30)
            if resp.status_code == 200 and resp.content[:5] == b'%PDF-':
                with open(save_path, 'wb') as f:
                    f.write(resp.content)
                return save_path
            return None
        except Exception as e:
            logger.warning(f"PDF下载失败: {e}")
            return None


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    fetcher = SZSEFetcher()

    print("=" * 60)
    print("深交所 (SZSE) 数据源测试")
    print("=" * 60)

    # 测试A股列表
    print("\n[1] 深交所A股列表...")
    result = fetcher.get_a_stock_list(page_no=1, page_count=5)
    if result['stocks']:
        print(f"  总计: {result['total']} 只")
        print(f"  当前页: {result['page']}/{result['page_count']}")
        for s in result['stocks']:
            print(f"  {s['code']} | {s['name']} | {s['industry']} | 总股本:{s['total_shares']}亿")
    else:
        print("  [FAIL] 获取失败")

    # 测试指数行情
    print("\n[2] 深市指数行情...")
    indices = fetcher.get_index_quote()
    if indices:
        for idx in indices[:5]:
            print(f"  {idx['name']} ({idx['code']}): {idx['close']} 涨跌:{idx['change_pct']}%")
    else:
        print("  [FAIL] 获取失败")

    # 测试公告查询
    print("\n[3] 五粮液(000858)公告...")
    ann = fetcher.get_announcements(stock_code='000858', page_size=5)
    if ann and ann['announcements']:
        print(f"  总公告数: {ann['total']}")
        for a in ann['announcements'][:5]:
            title = a.get('title', '')[:40]
            print(f"  {a.get('secCode')} | {a.get('publishTime','')[:10]} | {title}")
    else:
        print("  [FAIL] 获取失败")
