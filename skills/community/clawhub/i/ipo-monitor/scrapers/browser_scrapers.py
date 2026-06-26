#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BrowserScraper子类 - A股、港股和美股交易所

为以下交易所创建BrowserScraper子类：
- 上交所 (sse)
- 深交所 (szse)  
- 北交所 (bse)
- 港股新上市 (hkex_new)
- 港股申请 (hkex_app)
- 纳斯达克 (nasdaq)
- 纽交所 (nyse)
"""
import logging
from typing import List, Dict
from .browser_scraper import BrowserScraper


class SSEBrowserScraper(BrowserScraper):
    """上交所BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.sse.com.cn/listing/renewal/ipo/"
    
    @property
    def name(self) -> str:
        return "上交所"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析上交所页面"""
        try:
            # 获取表格HTML
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.querySelector('table') ? document.querySelector('table').outerHTML : ''"}
            )
            table_html = html.get('result', '')
            
            if not table_html:
                self.logger.warning("上交所: 未找到表格")
                return []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(table_html, 'html.parser')
            table = soup.find('table')
            
            if not table:
                return []
            
            results = []
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) < 9:
                    continue
                
                def get_text(cell):
                    span = cell.find('span')
                    div = cell.find('div')
                    if span:
                        return span.get('title', span.get_text(strip=True))
                    if div:
                        return div.get('title', div.get_text(strip=True))
                    return cell.get_text(strip=True)
                
                ipo_info = {
                    'company_name': get_text(cells[0]),
                    'board': get_text(cells[1]),
                    'application_status': get_text(cells[2]),
                    'province': get_text(cells[3]),
                    'industry': get_text(cells[4]),
                    'sponsor': get_text(cells[5]),
                    'law_firm': get_text(cells[6]),
                    'accounting_firm': get_text(cells[7]),
                    'update_date': get_text(cells[8]),
                    'stock_code': '',
                    'exchange': '上交所',
                    'source_url': self.url,
                    'source': '上交所',
                }
                
                if ipo_info['company_name']:
                    results.append(ipo_info)
            
            self.logger.info(f"上交所: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析上交所失败: {e}")
            return []


class SZSEBrowserScraper(BrowserScraper):
    """深交所BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.szse.cn/listing/projectdynamic/ipo/"
    
    @property
    def name(self) -> str:
        return "深交所"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析深交所页面"""
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.querySelector('table') ? document.querySelector('table').outerHTML : ''"}
            )
            table_html = html.get('result', '')
            
            if not table_html:
                self.logger.warning("深交所: 未找到表格")
                return []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(table_html, 'html.parser')
            table = soup.find('table')
            
            if not table:
                return []
            
            results = []
            for row in table.find_all('tr')[1:]:
                cells = row.find_all('td')
                if len(cells) < 8:
                    continue
                
                def get_text(cell):
                    return cell.get_text(strip=True)
                
                ipo_info = {
                    'company_name': get_text(cells[0]),
                    'stock_code': get_text(cells[1]),
                    'board': get_text(cells[2]),
                    'application_status': get_text(cells[3]),
                    'province': get_text(cells[4]),
                    'industry': get_text(cells[5]),
                    'sponsor': get_text(cells[6]),
                    'update_date': get_text(cells[7]),
                    'exchange': '深交所',
                    'source_url': self.url,
                    'source': '深交所',
                    'law_firm': '',
                    'accounting_firm': '',
                    'accept_date': '',
                }
                
                if ipo_info['company_name']:
                    results.append(ipo_info)
            
            self.logger.info(f"深交所: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析深交所失败: {e}")
            return []


class BSEBrowserScraper(BrowserScraper):
    """北交所BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.bse.cn/audit/project_news.html"
    
    @property
    def name(self) -> str:
        return "北交所"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析北交所页面"""
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.querySelector('table') ? document.querySelector('table').outerHTML : ''"}
            )
            table_html = html.get('result', '')
            
            if not table_html:
                self.logger.warning("北交所: 未找到表格")
                return []
            
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(table_html, 'html.parser')
            table = soup.find('table')
            
            if not table:
                return []
            
            results = []
            for row in table.find_all('tr')[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 5:
                    continue
                
                def get_text(cell):
                    return cell.get_text(strip=True)
                
                ipo_info = {
                    'company_name': get_text(cells[0]),
                    'stock_code': get_text(cells[1]) if len(cells) > 1 else '',
                    'application_status': get_text(cells[2]) if len(cells) > 2 else '',
                    'exchange': '北交所',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': '',
                    'accept_date': '',
                    'source_url': self.url,
                    'source': '北交所',
                }
                
                if ipo_info['company_name']:
                    results.append(ipo_info)
            
            self.logger.info(f"北交所: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析北交所失败: {e}")
            return []


class HKEXNewBrowserScraper(BrowserScraper):
    """港股新上市BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities"
    
    @property
    def name(self) -> str:
        return "港股新上市"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析港股新上市页面"""
        # 获取页面内容
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.body.innerText"}
            )
            text = html.get('result', '')
            
            results = []
            for line in text.split('\n'):
                line = line.strip()
                if len(line) >= 3:
                    results.append({
                        'company_name': line[:50],
                        'stock_code': '',
                        'exchange': '港股新上市',
                        'application_status': '已上市',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': '',
                        'accept_date': '',
                        'source_url': self.url,
                        'source': '港股新上市',
                    })
            
            self.logger.info(f"港股新上市: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析港股新上市失败: {e}")
            return []


class HKEXAppBrowserScraper(BrowserScraper):
    """港股申请BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.hkexnews.hk/app/appindex.html"
    
    @property
    def name(self) -> str:
        return "港股申请"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析港股申请页面"""
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.body.innerText"}
            )
            text = html.get('result', '')
            
            results = []
            for line in text.split('\n'):
                line = line.strip()
                if len(line) >= 3:
                    results.append({
                        'company_name': line[:50],
                        'stock_code': '',
                        'exchange': '港股申请',
                        'application_status': '申请中',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': '',
                        'accept_date': '',
                        'source_url': self.url,
                        'source': '港股申请',
                    })
            
            self.logger.info(f"港股申请: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析港股申请失败: {e}")
            return []


class NASDAQBrowserScraper(BrowserScraper):
    """纳斯达克BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.nasdaq.com/market-activity/ipos"
    
    @property
    def name(self) -> str:
        return "纳斯达克"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析纳斯达克IPO页面"""
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.body.innerText"}
            )
            text = html.get('result', '')
            
            results = []
            for line in text.split('\n'):
                line = line.strip()
                if len(line) >= 3:
                    results.append({
                        'company_name': line[:50],
                        'stock_code': '',
                        'exchange': '纳斯达克',
                        'application_status': '待上市',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': '',
                        'accept_date': '',
                        'source_url': self.url,
                        'source': '纳斯达克',
                    })
            
            self.logger.info(f"纳斯达克: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析纳斯达克失败: {e}")
            return []


class NYSEBrowserScraper(BrowserScraper):
    """纽交所BrowserScraper"""
    
    @property
    def url(self) -> str:
        return "https://www.nyse.com/ipo-center/ipo-calendar"
    
    @property
    def name(self) -> str:
        return "纽交所"
    
    def parse(self, snapshot: Dict) -> List[Dict]:
        """解析纽交所IPO页面"""
        try:
            html = self.browser.action(
                action="act",
                targetId=self.tab_id,
                request={"kind": "evaluate", "fn": "document.body.innerText"}
            )
            text = html.get('result', '')
            
            results = []
            for line in text.split('\n'):
                line = line.strip()
                if len(line) >= 3:
                    results.append({
                        'company_name': line[:50],
                        'stock_code': '',
                        'exchange': '纽交所',
                        'application_status': '待上市',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': '',
                        'accept_date': '',
                        'source_url': self.url,
                        'source': '纽交所',
                    })
            
            self.logger.info(f"纽交所: 获取 {len(results)} 条记录")
            return results
        except Exception as e:
            self.logger.error(f"解析纽交所失败: {e}")
            return []


# 导出
__all__ = [
    # A股
    'SSEBrowserScraper',
    'SZSEBrowserScraper',
    'BSEBrowserScraper',
    # 港股
    'HKEXNewBrowserScraper',
    'HKEXAppBrowserScraper',
    # 美股
    'NASDAQBrowserScraper',
    'NYSEBrowserScraper',
]
