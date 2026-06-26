#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
港股历史卖空数据获取工具
======================
免费获取港股历史卖空数据的多种方案

方案1: 从ETNet获取个股历史卖空数据 (免费)
方案2: 自建历史数据库 (每日积累)
方案3: 从港交所获取历史数据文件 (付费订阅)

作者: AI Assistant
日期: 2026-03-10
"""

import requests
import pandas as pd
import re
from datetime import datetime, timedelta
from typing import List, Optional
import time
import os


class ETNetHistoricalScraper:
    """
    从ETNet获取个股历史卖空数据
    =============================
    免费获取个股的历史卖空记录
    
    数据源: etnet.com.hk (免费公开数据)
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_stock_short_selling_history(
        self, 
        stock_code: str, 
        pages: int = 5
    ) -> pd.DataFrame:
        """
        获取指定股票的历史卖空数据
        
        参数:
        -----
        stock_code : str
            股票代码，如 '700' (腾讯)
        pages : int
            要获取的页数 (每页约30条记录)
        
        返回:
        -----
        pd.DataFrame
            历史卖空数据，包含以下字段:
            - date: 交易日期
            - short_volume: 卖空股数
            - short_amount: 卖空金额
            - avg_5d: 5天平均卖空金额
            - turnover: 股票成交金额
            - short_pct: 卖空占成交金额比例
            - total_short_value: 主板总卖空金额
            - pct_of_total: 卖空占总卖空金额比例
        
        示例:
        ------
        >>> scraper = ETNetHistoricalScraper()
        >>> df = scraper.get_stock_short_selling_history('700', pages=3)
        >>> print(df)
        """
        all_data = []
        
        for page in range(1, pages + 1):
            url = f"https://www.etnet.com.hk/www/eng/stocks/realtime/quote_shortsell.php?code={stock_code}&page={page}"
            
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                
                if response.status_code != 200:
                    print(f"页面 {page} 请求失败: {response.status_code}")
                    continue
                
                # 解析HTML
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 找到数据表格
                tables = soup.find_all('table')
                
                for table in tables:
                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all('td')
                        if len(cols) >= 8:
                            # 提取数据
                            date_text = cols[0].text.strip()
                            
                            # 验证日期格式
                            if re.match(r'\d{2}/\d{2}/\d{4}', date_text):
                                try:
                                    data = {
                                        'date': datetime.strptime(date_text, '%d/%m/%Y'),
                                        'short_volume': self._parse_number(cols[1].text),
                                        'short_amount': self._parse_amount(cols[2].text),
                                        'avg_5d': self._parse_amount(cols[3].text),
                                        'turnover': self._parse_amount(cols[4].text),
                                        'short_pct': self._parse_percentage(cols[5].text),
                                        'total_short_value': self._parse_amount(cols[6].text),
                                        'pct_of_total': self._parse_percentage(cols[7].text),
                                        'stock_code': stock_code.zfill(5)
                                    }
                                    all_data.append(data)
                                except Exception as e:
                                    continue
                
                #  polite delay
                time.sleep(0.5)
                
            except Exception as e:
                print(f"获取页面 {page} 时出错: {e}")
                continue
        
        df = pd.DataFrame(all_data)
        
        # 去重并排序
        if len(df) > 0:
            df = df.drop_duplicates(subset=['date', 'stock_code'])
            df = df.sort_values('date', ascending=False)
        
        return df
    
    def _parse_number(self, text: str) -> int:
        """解析数字 (处理逗号和单位)"""
        text = text.strip().replace(',', '')
        
        # 处理 "亿" (100 million)
        if '亿' in text or 'B' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return int(num * 100000000)
        
        # 处理 "万" (10 thousand)
        if '万' in text or 'M' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return int(num * 10000)
        
        # 处理 "千" (thousand)
        if '千' in text or 'K' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return int(num * 1000)
        
        try:
            return int(float(text))
        except:
            return 0
    
    def _parse_amount(self, text: str) -> float:
        """解析金额"""
        text = text.strip().replace(',', '')
        
        # 处理 "B" (Billion = 十亿 = 10亿)
        if 'B' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 1000000000
        
        # 处理 "M" (Million = 百万)
        if 'M' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 1000000
        
        # 处理 "亿" (100 million)
        if '亿' in text:
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 100000000
        
        # 处理 "万" (10 thousand)
        if '万' in text:
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 10000
        
        # 处理 "千" (thousand)
        if '千' in text:
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 1000
        
        # 处理 "K" (thousand)
        if 'K' in text.upper():
            num = float(re.sub(r'[^\d.]', '', text))
            return num * 1000
        
        try:
            return float(text)
        except:
            return 0.0
    
    def _parse_percentage(self, text: str) -> float:
        """解析百分比"""
        text = text.strip().replace('%', '')
        try:
            return float(text)
        except:
            return 0.0
    
    def get_multiple_stocks_history(
        self, 
        stock_codes: List[str], 
        pages: int = 3
    ) -> pd.DataFrame:
        """
        获取多只股票的历史卖空数据
        
        参数:
        -----
        stock_codes : List[str]
            股票代码列表
        pages : int
            每只股票获取的页数
        
        返回:
        -----
        pd.DataFrame
            合并后的历史数据
        """
        all_data = []
        
        for code in stock_codes:
            print(f"正在获取 {code} 的历史数据...")
            df = self.get_stock_short_selling_history(code, pages)
            if len(df) > 0:
                all_data.append(df)
            time.sleep(1)  # polite delay
        
        if all_data:
            return pd.concat(all_data, ignore_index=True)
        return pd.DataFrame()


class HistoricalDatabase:
    """
    自建历史卖空数据库
    =================
    通过每日自动抓取，积累历史数据
    """
    
    def __init__(self, db_path: str = './short_selling_history.csv'):
        self.db_path = db_path
        self.daily_scraper = HKEXDailyScraper()
    
    def update_database(self):
        """
        更新数据库 - 获取今日数据并追加到历史记录
        
        返回:
        -----
        pd.DataFrame
            更新后的完整历史数据
        """
        # 获取今日数据
        today_data = self.daily_scraper.get_short_selling_data()
        
        if len(today_data) == 0:
            print("未能获取今日数据")
            return self.load_database()
        
        # 加载现有历史数据
        historical_data = self.load_database()
        
        # 合并数据
        combined = pd.concat([historical_data, today_data], ignore_index=True)
        
        # 去重
        combined = combined.drop_duplicates(
            subset=['date', 'stock_code'], 
            keep='last'
        )
        
        # 保存
        combined.to_csv(self.db_path, index=False, encoding='utf-8-sig')
        
        print(f"数据库已更新，共 {len(combined)} 条记录")
        return combined
    
    def load_database(self) -> pd.DataFrame:
        """加载历史数据库"""
        if os.path.exists(self.db_path):
            return pd.read_csv(self.db_path, encoding='utf-8-sig')
        return pd.DataFrame()
    
    def query_stock_history(self, stock_code: str) -> pd.DataFrame:
        """查询指定股票的历史数据"""
        df = self.load_database()
        if len(df) > 0:
            return df[df['stock_code'] == stock_code.zfill(5)]
        return df


class HKEXDailyScraper:
    """
    从港交所获取每日卖空数据 (复用之前的代码)
    """
    
    MAIN_BOARD_URL = "https://www.hkex.com.hk/chi/stat/smstat/ssturnover/ncms/ashtmain_c.htm"
    GEM_URL = "https://www.hkex.com.hk/chi/stat/smstat/ssturnover/ncms/ashtgem_c.htm"
    
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0'}
    
    def _fetch_data(self, url: str) -> str:
        response = requests.get(url, headers=self.headers, timeout=30)
        response.encoding = 'big5'
        return response.text
    
    def _parse_data(self, html_content: str) -> List[dict]:
        pattern = r'\s+(\d{1,5})\s+([^\d]{2,20}?)\s+([\d,]+)\s+([\d,]+)'
        matches = re.findall(pattern, html_content)
        data = []
        for match in matches:
            stock_code, stock_name, volume, amount = match
            data.append({
                'stock_code': stock_code.strip(),
                'stock_name': stock_name.strip().replace('　', ''),
                'short_volume': int(volume.replace(',', '')),
                'short_amount': int(amount.replace(',', ''))
            })
        return data
    
    def _extract_date(self, html_content: str) -> Optional[str]:
        date_pattern = r'日期\s*:\s*(\d{1,2}\s+[A-Z]{3}\s+\d{4})'
        match = re.search(date_pattern, html_content)
        return match.group(1) if match else None
    
    def get_short_selling_data(self) -> pd.DataFrame:
        all_data = []
        html = self._fetch_data(self.MAIN_BOARD_URL)
        date_str = self._extract_date(html)
        data = self._parse_data(html)
        for item in data:
            item['market'] = '主板'
            item['date'] = date_str
        all_data.extend(data)
        
        df = pd.DataFrame(all_data)
        return df


# ==================== 使用示例 ====================

def demo_historical_data():
    """演示如何获取历史卖空数据"""
    
    print("=" * 70)
    print("港股历史卖空数据获取演示")
    print("=" * 70)
    
    # 方案1: 从ETNet获取个股历史数据
    print("\n【方案1】从ETNet获取个股历史卖空数据")
    print("-" * 70)
    
    etnet = ETNetHistoricalScraper()
    
    # 获取腾讯(00700)的历史数据
    print("\n获取腾讯(00700)最近的历史卖空数据...")
    df_tencent = etnet.get_stock_short_selling_history('700', pages=2)
    
    if len(df_tencent) > 0:
        print(f"获取到 {len(df_tencent)} 条历史记录")
        print("\n最近10条记录:")
        print(df_tencent.head(10)[['date', 'short_volume', 'short_amount', 'short_pct']].to_string(index=False))
    else:
        print("未能获取到数据")
    
    # 获取多只股票的历史数据
    print("\n\n获取多只股票的历史数据...")
    stocks = ['700', '9988', '1810']  # 腾讯、阿里、小米
    df_multiple = etnet.get_multiple_stocks_history(stocks, pages=2)
    
    if len(df_multiple) > 0:
        print(f"\n共获取到 {len(df_multiple)} 条记录")
        
        # 按股票分组统计
        print("\n各股票数据统计:")
        summary = df_multiple.groupby('stock_code').agg({
            'short_amount': ['mean', 'max', 'min'],
            'short_pct': 'mean'
        }).round(2)
        print(summary)
    
    # 方案2: 自建数据库
    print("\n\n【方案2】自建历史数据库")
    print("-" * 70)
    print("""
使用方法:
1. 每天运行 update_database() 获取当日数据
2. 数据会自动保存到CSV文件
3. 可以随时查询历史记录

示例代码:
    db = HistoricalDatabase('./my_short_selling_db.csv')
    db.update_database()  # 更新今日数据
    history = db.query_stock_history('00700')  # 查询腾讯历史
    """)


if __name__ == "__main__":
    demo_historical_data()
