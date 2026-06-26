#!/usr/bin/env python3
"""
港交所IPO抓取器
数据来源: 港交所披露易
支持两个页面:
1. 新上市: https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities
2. 上市申请: https://www.hkexnews.hk/app/appindex.html
"""
from typing import List, Dict
from datetime import datetime
import json
import re
import logging

from scrapers.base import BaseScraper


class HKEXScraper(BaseScraper):
    """港交所IPO抓取器"""
    
    # 两个URL
    URL_NEW_LISTED = 'https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities'
    URL_APPLICATION = 'https://www.hkexnews.hk/app/appindex.html'
    
    def __init__(self, config, exchange: str = "港股"):
        super().__init__(config, exchange)
        # 获取配置的两个URL
        self.urls = [
            config.exchange_urls.get('港股新上市', self.URL_NEW_LISTED),
            config.exchange_urls.get('港股申请', self.URL_APPLICATION),
        ]
    
    def fetch(self) -> List[Dict]:
        """抓取港股IPO数据（两个页面）"""
        all_results = []
        
        # 抓取新上市页面
        results_new = self._fetch_url(self.urls[0], '新上市')
        all_results.extend(results_new)
        
        # 抓取上市申请页面
        results_app = self._fetch_url(self.urls[1], '上市申请')
        all_results.extend(results_app)
        
        return all_results
    
    def _fetch_url(self, url: str, category: str) -> List[Dict]:
        """抓取单个URL"""
        response = self.fetch_with_retry(url)
        
        if not response:
            return []
        
        return self.parse(response.text, category)
    
    def parse(self, html: str, category: str = '新上市') -> List[Dict]:
        """解析港股IPO数据"""
        results = []
        
        # 方法1: 提取JSON数据
        json_patterns = [
            r'IPO\s*:\s*(\[.*?\]);',
            r'var\s+ipoList\s*=\s*(\[.*?\]);',
            r'"list"\s*:\s*(\[.*?\])',
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    ipo_data = json.loads(match.group(1))
                    if isinstance(ipo_data, list):
                        results.extend(self._parse_json(ipo_data, category))
                        if results:
                            break
                except (json.JSONDecodeError, Exception) as e:
                    self.logger.warning(f"JSON解析失败: {e}")
        
        # 方法2: 解析表格
        if not results:
            results = self._parse_table(html, category)
        
        return results
    
    def _parse_json(self, data: List[Dict], category: str) -> List[Dict]:
        """解析JSON数据"""
        results = []
        
        for item in data:
            ipo_info = {
                'company_name': item.get('name_cn') or item.get('name_en') or item.get('companyName') or item.get('name', ''),
                'stock_code': item.get('stock_code') or item.get('code') or item.get('symbol', ''),
                'exchange': '港股主板',
                'application_status': item.get('listing_stage') or item.get('status') or category,
                'expected_date': item.get('expected_date') or item.get('expectedDate') or item.get('listingDate', ''),
                'fundraising_amount': item.get('fundraising') or item.get('fundraisingAmount') or item.get('raiseAmount', ''),
                'issue_price_range': item.get('price_range') or item.get('priceRange') or item.get('price', ''),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': self.urls[0] if category == '新上市' else self.urls[1],
                'source': '港交所',
            }
            
            if ipo_info['stock_code']:
                results.append(ipo_info)
        
        return results
    
    def _parse_table(self, html: str, category: str) -> List[Dict]:
        """解析表格数据"""
        from bs4 import BeautifulSoup
        results = []
        
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all(['td', 'th'])
                if len(cols) < 4:
                    continue
                
                try:
                    ipo_info = {
                        'company_name': cols[0].get_text(strip=True),
                        'stock_code': cols[1].get_text(strip=True),
                        'exchange': '港股主板',
                        'application_status': cols[2].get_text(strip=True) if len(cols) > 2 else category,
                        'expected_date': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'fundraising_amount': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                        'issue_price_range': cols[5].get_text(strip=True) if len(cols) > 5 else '',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': self.urls[0] if category == '新上市' else self.urls[1],
                        'source': '港交所',
                    }
                    
                    # 提取链接
                    link = cols[0].find('a')
                    if link and link.get('href'):
                        href = link['href']
                        if not href.startswith('http'):
                            href = 'https://www.hkex.com.hk' + href
                        ipo_info['source_url'] = href
                    
                    if ipo_info['stock_code']:
                        results.append(ipo_info)
                        
                except Exception as e:
                    self.logger.warning(f"解析行失败: {e}")
        
        return results


# 导出
__all__ = ['HKEXScraper']
