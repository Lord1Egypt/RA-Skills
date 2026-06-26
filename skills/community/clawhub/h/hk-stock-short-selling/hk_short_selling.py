#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股卖空数据获取库
"""

import requests
import pandas as pd
import re
import os
import json
from datetime import datetime, timedelta
from typing import List, Optional


class HKShortSeller:
    """港股卖空数据获取"""
    
    MAIN_URL = "https://www.hkex.com.hk/chi/stat/smstat/ssturnover/ncms/ashtmain_c.htm"
    GEM_URL = "https://www.hkex.com.hk/chi/stat/smstat/ssturnover/ncms/ashtgem_c.htm"
    
    def __init__(self, data_dir: str = None):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        if data_dir is None:
            data_dir = os.path.expanduser("~/.openclaw/workspace/data/hk-short")
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def _fetch_html(self, url: str) -> str:
        """获取HTML"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.encoding = 'big5'
            return resp.text
        except Exception as e:
            print(f"获取失败: {e}")
            return ""
    
    def _parse(self, html: str) -> List[dict]:
        """解析HTML"""
        data = []
        pattern = r'\s+(\d{1,5})\s+([^\d]{2,20}?)\s+([\d,]+)\s+([\d,]+)'
        for match in re.findall(pattern, html):
            code, name, vol, amt = match
            data.append({
                'stock_code': code.strip(),
                'stock_name': name.strip().replace('　', ''),
                'short_volume': int(vol.replace(',', '')),
                'short_amount': int(amt.replace(',', ''))
            })
        return data
    
    def _extract_date(self, html: str) -> str:
        """提取日期"""
        match = re.search(r'日期\s*:\s*(\d{1,2}\s+[A-Z]{3}\s+\d{4})', html)
        return match.group(1) if match else ""
    
    def get_today_data(self, stock_codes: List[str] = None, market: str = 'all') -> pd.DataFrame:
        """获取当天卖空数据"""
        all_data = []
        date_str = ""
        
        if market in ['all', 'main']:
            html = self._fetch_html(self.MAIN_URL)
            if html:
                data = self._parse(html)
                for d in data:
                    d['market'] = '主板'
                all_data.extend(data)
                date_str = self._extract_date(html)
        
        if market in ['all', 'gem']:
            html = self._fetch_html(self.GEM_URL)
            if html:
                data = self._parse(html)
                for d in data:
                    d['market'] = '创业板'
                all_data.extend(data)
                if not date_str:
                    date_str = self._extract_date(html)
        
        df = pd.DataFrame(all_data)
        df['date'] = date_str
        
        # 过滤指定股票
        if stock_codes:
            codes = [str(int(c)) for c in stock_codes]
            df = df[df['stock_code'].apply(lambda x: str(x) in codes)]
        
        return df
    
    def get_history(self, stock_code: str, days: int = 30) -> pd.DataFrame:
        """获取历史数据"""
        code = str(int(stock_code))
        history_file = os.path.join(self.data_dir, f"{code}.csv")
        
        if not os.path.exists(history_file):
            return pd.DataFrame()
        
        df = pd.read_csv(history_file)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='%d %b %Y', errors='coerce')
            df = df.sort_values('date', ascending=False)
            if days:
                df = df.head(days)
        
        return df
    
    def save_today(self) -> bool:
        """保存当天数据到历史"""
        df = self.get_today_data()
        if df.empty:
            return False
        
        date_str = df['date'].iloc[0] if 'date' in df.columns and len(df) > 0 else ""
        
        for code in df['stock_code'].unique():
            code_file = os.path.join(self.data_dir, f"{code}.csv")
            code_df = df[df['stock_code'] == code].copy()
            
            if os.path.exists(code_file):
                old_df = pd.read_csv(code_file)
                if date_str and date_str not in old_df['date'].values:
                    code_df = pd.concat([old_df, code_df], ignore_index=True)
                else:
                    continue
            code_df.to_csv(code_file, index=False, encoding='utf-8')
        
        return True
    
    def get_top(self, n: int = 10, by: str = 'amount') -> pd.DataFrame:
        """获取排行榜"""
        df = self.get_today_data()
        if df.empty:
            return df
        col = 'short_amount' if by == 'amount' else 'short_volume'
        return df.nlargest(n, col)


# 兼容旧API
class HKEXShortSellingScraper(HKShortSeller):
    """兼容旧API"""
    pass
