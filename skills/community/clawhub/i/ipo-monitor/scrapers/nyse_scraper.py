#!/usr/bin/env python3
"""
纽交所IPO抓取器
数据来源: NYSE IPO Center
"""
from typing import List, Dict
from datetime import datetime
import json
import re
import logging

from scrapers.base import BaseScraper


class NYSEScraper(BaseScraper):
    """纽交所IPO抓取器"""
    
    URL = 'https://www.nyse.com/ipo-center/ipo-calendar'
    
    def fetch(self) -> List[Dict]:
        """抓取NYSE IPO数据"""
        response = self.fetch_with_retry(self.URL)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析NYSE IPO数据"""
        results = []
        
        # 方法1: 尝试提取页面中的JSON数据
        json_pattern = r'window\.IPO_DATA\s*=\s*(\[.*?\]);'
        match = re.search(json_pattern, html, re.DOTALL)
        
        if match:
            try:
                ipo_list = json.loads(match.group(1))
                results.extend(self._parse_json(ipo_list))
            except (json.JSONDecodeError, Exception) as e:
                self.logger.warning(f"JSON解析失败: {e}")
        
        # 方法2: 尝试解析表格
        if not results:
            results = self._parse_table(html)
        
        return results
    
    def _parse_json(self, data: List[Dict]) -> List[Dict]:
        """解析JSON数据"""
        results = []
        
        for item in data:
            # 过滤NYSE相关的IPO
            exchange = item.get('exchange', '').upper()
            if 'NYSE' not in exchange and 'NEW YORK' not in exchange:
                continue
            
            ipo_info = {
                'company_name': item.get('companyName', ''),
                'stock_code': item.get('symbol', ''),
                'exchange': 'NYSE',
                'application_status': item.get('status', 'Upcoming'),
                'expected_date': item.get('expectedDate', ''),
                'fundraising_amount': item.get('offerAmount', ''),
                'issue_price_range': item.get('priceRange', ''),
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': f"https://www.nyse.com/ipo-center/ipo-profile/{item.get('symbol', '')}",
                'source': 'NYSE',
            }
            
            if ipo_info['stock_code']:
                results.append(ipo_info)
        
        return results
    
    def _parse_table(self, html: str) -> List[Dict]:
        """解析表格数据"""
        from bs4 import BeautifulSoup
        results = []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # 查找IPO表格
        tables = soup.find_all('table', class_=re.compile('ipo|calendar', re.I))
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue
                
                try:
                    ipo_info = {
                        'company_name': cols[0].get_text(strip=True),
                        'stock_code': cols[1].get_text(strip=True),
                        'exchange': 'NYSE',
                        'application_status': cols[2].get_text(strip=True) if len(cols) > 2 else 'Upcoming',
                        'expected_date': cols[3].get_text(strip=True) if len(cols) > 3 else '',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'source_url': '',
                        'source': 'NYSE',
                    }
                    
                    # 提取链接
                    link = cols[0].find('a')
                    if link and link.get('href'):
                        href = link['href']
                        ipo_info['source_url'] = href if href.startswith('http') else f'https://www.nyse.com{href}'
                    
                    if ipo_info['stock_code']:
                        results.append(ipo_info)
                        
                except Exception as e:
                    self.logger.warning(f"解析行失败: {e}")
        
        return results


# 导出
__all__ = ['NYSEScraper']
