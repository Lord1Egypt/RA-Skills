#!/usr/bin/env python3
"""
上交所IPO抓取器
数据来源: 上交所科创板股票发行上市审核
"""
from typing import List, Dict
from datetime import datetime
import json
import re
import logging

from scrapers.base import BaseScraper


class SSEScraper(BaseScraper):
    """上交所IPO抓取器"""
    
    URL = 'https://www.sse.com.cn/listing/renewal/ipo/'
    
    def __init__(self, config, exchange: str = "上交所"):
        super().__init__(config, exchange)
        self.url = config.exchange_urls.get('上交所', self.URL)
    
    def fetch(self) -> List[Dict]:
        """抓取上交所IPO数据"""
        response = self.fetch_with_retry(self.url)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析上交所IPO数据"""
        results = []
        
        # 方法1: 尝试提取页面中的JSON数据
        # 上交所页面通常有IPO审核进度数据
        json_patterns = [
            r'IPO_DATA\s*=\s*(\[.*?\]);',
            r'var\s+ipoList\s*=\s*(\[.*?\]);',
            r'"list"\s*:\s*(\[.*?\])',
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
            # 尝试多种字段名
            ipo_info = {
                'company_name': item.get('companyName') or item.get('company_name') or item.get('name', ''),
                'stock_code': item.get('stockCode') or item.get('stock_code') or item.get('code', ''),
                'exchange': '上交所',
                'application_status': item.get('status') or item.get('applicationStatus') or item.get('auditStatus', '待审核'),
                'expected_date': item.get('expectedDate') or item.get('expected_date') or item.get('listingDate', ''),
                'fundraising_amount': item.get('fundraising') or item.get('fundraisingAmount') or item.get('raiseAmount', ''),
                'issue_price_range': item.get('priceRange') or item.get('price_range') or item.get('issuePrice', ''),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': self.url,
                'source': '上交所',
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
            headers = []
            
            # 获取表头
            header_row = rows[0] if rows else None
            if header_row:
                headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # 解析数据行
            for row in rows[1:]:
                cols = row.find_all(['td', 'th'])
                if len(cols) < 3:
                    continue
                
                try:
                    # 根据常见列位置提取数据
                    ipo_info = {
                        'company_name': cols[0].get_text(strip=True) if len(cols) > 0 else '',
                        'stock_code': cols[1].get_text(strip=True) if len(cols) > 1 else '',
                        'exchange': '上交所',
                        'application_status': cols[2].get_text(strip=True) if len(cols) > 2 else '待审核',
                        'expected_date': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'fundraising_amount': cols[4].get_text(strip=True) if len(cols) > 4 else '',
                        'issue_price_range': cols[5].get_text(strip=True) if len(cols) > 5 else '',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': self.url,
                        'source': '上交所',
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
        # 尝试从script标签中提取数据
        results = []
        
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        scripts = soup.find_all('script')
        for script in scripts:
            text = script.string or ''
            # 尝试匹配IPO相关数据
            if 'IPO' in text or 'ipo' in text:
                # 查找可能的JSON数组
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
__all__ = ['SSEScraper']
