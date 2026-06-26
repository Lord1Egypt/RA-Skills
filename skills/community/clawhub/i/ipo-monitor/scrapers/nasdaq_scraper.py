#!/usr/bin/env python3
"""
纳斯达克IPO抓取器
数据来源: NASDAQ IPO Calendar
"""
from typing import List, Dict
from datetime import datetime
import json
import re
import logging

from scrapers.base import BaseScraper


class NASDAQScraper(BaseScraper):
    """纳斯达克IPO抓取器"""
    
    URL = 'https://www.nasdaq.com/market-activity/ipos'
    
    def __init__(self, config, exchange: str = "纳斯达克"):
        super().__init__(config, exchange)
        self.url = config.exchange_urls.get('纳斯达克', self.URL)
    
    def fetch(self) -> List[Dict]:
        """抓取纳斯达克IPO数据"""
        response = self.fetch_with_retry(self.url)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析纳斯达克IPO数据"""
        results = []
        
        # 方法1: 尝试提取页面中的JSON数据
        json_patterns = [
            r'IPO_DATA\s*=\s*(\[.*?\]);',
            r'window\.IPO\s*=\s*(\[.*?\]);',
            r'var\s+ipoCalendar\s*=\s*(\[.*?\]);',
            r'"ipos"\s*:\s*(\[.*?\])',
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, html, re.DOTALL)
            if match:
                try:
                    ipo_data = json.loads(match.group(1))
                    if isinstance(ipo_data, list):
                        results.extend(self._parse_json(ipo_data))
                        if results:
                            break
                except (json.JSONDecodeError, Exception) as e:
                    self.logger.warning(f"JSON解析失败: {e}")
        
        # 方法2: 解析表格
        if not results:
            results = self._parse_table(html)
        
        # 方法3: 解析动态加载的数据
        if not results:
            results = self._parse_dynamic(html)
        
        return results
    
    def _parse_json(self, data: List[Dict]) -> List[Dict]:
        """解析JSON数据"""
        results = []
        
        for item in data:
            ipo_info = {
                'company_name': item.get('companyName') or item.get('company_name') or item.get('name', ''),
                'stock_code': item.get('symbol') or item.get('stock_code') or item.get('ticker', ''),
                'exchange': 'NASDAQ',
                'application_status': item.get('status') or item.get('applicationStatus') or 'Upcoming',
                'expected_date': item.get('expectedDate') or item.get('expected_date') or item.get('date', ''),
                'fundraising_amount': item.get('fundraising') or item.get('fundraisingAmount') or item.get('offerAmount', ''),
                'issue_price_range': item.get('priceRange') or item.get('price_range') or item.get('price', ''),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': self.url,
                'source': 'NASDAQ',
            }
            
            if ipo_info['stock_code']:
                results.append(ipo_info)
        
        return results
    
    def _parse_table(self, html: str) -> List[Dict]:
        """解析表格数据"""
        from bs4 import BeautifulSoup
        results = []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找表格
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            # 解析数据行
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all(['td', 'th'])
                if len(cols) < 3:
                    continue
                
                try:
                    ipo_info = {
                        'company_name': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                        'stock_code': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                        'exchange': 'NASDAQ',
                        'application_status': cols[2].get_text(strip=True) if len(cols) > 2 else 'Upcoming',
                        'expected_date': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'fundraising_amount': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                        'issue_price_range': cols[5].get_text(strip=True) if len(cols) > 5 else '',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': self.url,
                        'source': 'NASDAQ',
                    }
                    
                    # 提取链接
                    link = cols[0].find('a')
                    if link and link.get('href'):
                        ipo_info['source_url'] = link['href']
                    
                    if ipo_info['stock_code']:
                        results.append(ipo_info)
                        
                except Exception as e:
                    self.logger.warning(f"解析行失败: {e}")
        
        return results
    
    def _parse_dynamic(self, html: str) -> List[Dict]:
        """解析动态加载的数据"""
        results = []
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        scripts = soup.find_all('script')
        for script in scripts:
            text = script.string or ''
            if 'IPO' in text or 'ipo' in text:
                matches = re.findall(r'\[.*?"[^"]+".*?\]', text, re.DOTALL)
                for match in matches:
                    try:
                        data = json.loads(match)
                        if isinstance(data, list):
                            results.extend(self._parse_json(data))
                    except:
                        pass
        
        return results


# 导出
__all__ = ['NASDAQScraper']
