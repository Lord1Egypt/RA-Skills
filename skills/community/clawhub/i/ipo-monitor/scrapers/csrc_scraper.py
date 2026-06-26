#!/usr/bin/env python3
"""
证监会IPO抓取器 - A股科创板/主板
数据来源: 证监会官网
"""
from typing import List, Dict
from datetime import datetime
from bs4 import BeautifulSoup
import re

from scrapers.base import BaseScraper


class CSRCScraper(BaseScraper):
    """证监会IPO抓取器"""
    
    # 证监会IPO公示页面（需根据实际URL调整）
    URLS = {
        '科创板': 'https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/',
        '主板': 'https://www.csrc.gov.cn/ccczbjgs/xxf/xxfb/gsgg/',
    }
    
    def fetch(self) -> List[Dict]:
        """抓取A股IPO数据"""
        url = self.URLS.get(self.exchange, self.URLS['科创板'])
        response = self.fetch_with_retry(url)
        
        if not response:
            return []
        
        return self.parse(response.text)
    
    def parse(self, html: str) -> List[Dict]:
        """解析HTML - 需根据实际页面结构调整选择器"""
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        # 示例：根据表格行解析（实际需调整）
        # 这里使用通用逻辑，需要根据实际页面结构调整
        try:
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')
                for row in rows[1:]:  # 跳过表头
                    cols = row.find_all('td')
                    if len(cols) < 3:
                        continue
                    
                    ipo_info = self._parse_row(cols)
                    if ipo_info:
                        results.append(ipo_info)
        except Exception as e:
            self.logger.error(f"解析页面失败: {e}")
        
        return results
    
    def _parse_row(self, cols) -> Dict:
        """解析表格行"""
        try:
            # 需要根据实际列位置调整
            ipo_info = {
                'company_name': self._clean_text(cols[0].get_text()) if len(cols) > 0 else '',
                'stock_code': self._extract_code(cols[1].get_text()) if len(cols) > 1 else '',
                'exchange': self.exchange,
                'application_status': self._clean_text(cols[2].get_text()) if len(cols) > 2 else '',
                'expected_date': self._extract_date(cols[3].get_text()) if len(cols) > 3 else '',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_url': self._extract_link(cols[0]) if len(cols) > 0 else '',
                'source': '证监会',
            }
            
            # 只有有股票代码才返回
            if ipo_info['stock_code']:
                return ipo_info
        except Exception as e:
            self.logger.warning(f"解析行失败: {e}")
        
        return None
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        return text.strip().replace('\n', '').replace('\r', '').replace(' ', '')
    
    def _extract_code(self, text: str) -> str:
        """提取股票代码"""
        # 匹配6位数字
        match = re.search(r'\d{6}', text)
        return match.group() if match else ''
    
    def _extract_date(self, text: str) -> str:
        """提取日期"""
        match = re.search(r'\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?', text)
        if match:
            date_str = match.group()
            return date_str.replace('年', '-').replace('月', '-').replace('日', '')
        return ''
    
    def _extract_link(self, col) -> str:
        """提取链接"""
        link = col.find('a')
        if link and link.get('href'):
            href = link['href']
            return href if href.startswith('http') else f'https://www.csrc.gov.cn{href}'
        return ''


# 导出
__all__ = ['CSRCScraper']
