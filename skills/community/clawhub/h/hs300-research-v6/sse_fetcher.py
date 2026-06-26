#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
上交所(SSE) 数据采集模块

数据源: AKShare封装的SSE接口 (底层来自 sse.com.cn)
- 沪市股票列表
- 沪市新股上市
- 沪市指数行情
"""

import os
import logging
import pandas as pd
import akshare as ak
import pickle
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SSEFetcher:
    """上交所数据采集类"""

    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir
        if self.cache_dir and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _get_cache_path(self, key):
        if not self.cache_dir:
            return None
        return os.path.join(self.cache_dir, f'{key}.pkl')

    def _load_cache(self, key, expire_hours=24):
        if not self.cache_dir:
            return None
        path = self._get_cache_path(key)
        if not path or not os.path.exists(path):
            return None
        expire = timedelta(hours=expire_hours)
        if datetime.now() - datetime.fromtimestamp(os.path.getmtime(path)) > expire:
            return None
        try:
            with open(path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None

    def _save_cache(self, key, data):
        if not self.cache_dir:
            return
        try:
            with open(self._get_cache_path(key), 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            logger.warning(f"SSE保存缓存失败 {key}: {e}")

    def get_sh_stocks(self):
        """获取沪市A股股票列表"""
        cached = self._load_cache('sh_stocks', expire_hours=48)
        if cached:
            return cached
        try:
            df = ak.stock_info_sh_name_code()
            if df is not None and len(df) > 0:
                # 统一列名
                if '证券代码' in df.columns:
                    df = df.rename(columns={'证券代码': 'code', '证券简称': 'name'})
                stocks = df[['code', 'name']].to_dict('records') if 'code' in df.columns else []
                self._save_cache('sh_stocks', stocks)
                return stocks
            return []
        except Exception as e:
            logger.warning(f"SSE获取沪市股票列表失败: {e}")
            return []

    def get_sh_index(self):
        """获取沪市指数行情"""
        cached = self._load_cache('sh_index', expire_hours=1)
        if cached:
            return cached
        try:
            # 上证指数通过AKShare获取
            df = ak.stock_zh_index_spot_em()
            if df is not None and len(df) > 0:
                # 筛选上证指数
                sh_indices = df[df['代码'].isin(['000001', '000300', '000016', '000905'])]
                if len(sh_indices) > 0:
                    result = sh_indices.to_dict('records')
                    self._save_cache('sh_index', result)
                    return result
            return []
        except Exception as e:
            logger.warning(f"SSE获取沪市指数失败: {e}")
            return []

    def get_new_ipo(self):
        """获取新股上市信息"""
        cached = self._load_cache('sh_new_ipo', expire_hours=24)
        if cached:
            return cached
        try:
            df = ak.stock_new_ipo_cninfo()
            if df is not None and len(df) > 0:
                result = df.head(20).to_dict('records')
                self._save_cache('sh_new_ipo', result)
                return result
            return []
        except Exception as e:
            logger.warning(f"SSE获取新股信息失败: {e}")
            return []


if __name__ == '__main__':
    import io, sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    logging.basicConfig(level=logging.INFO)
    
    fetcher = SSEFetcher(cache_dir='sse_cache')
    
    print("=== 上交所(SSE) 数据测试 ===")
    stocks = fetcher.get_sh_stocks()
    print(f"沪市股票: {len(stocks)} 只")
    if stocks:
        print(f"  示例: {stocks[0]}")
    
    indices = fetcher.get_sh_index()
    print(f"沪市指数: {len(indices)} 个")
    for idx in indices[:3]:
        print(f"  {idx.get('名称', 'N/A')}: {idx.get('最新价', 'N/A')}")
    
    ipos = fetcher.get_new_ipo()
    print(f"新股上市: {len(ipos)} 只")
