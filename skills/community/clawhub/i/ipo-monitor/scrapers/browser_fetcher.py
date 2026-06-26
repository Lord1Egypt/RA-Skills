#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器抓取器 - 使用OpenClaw browser工具抓取IPO数据

使用方法:
    from scrapers.browser_fetcher import BrowserFetcher
    fetcher = BrowserFetcher(config)
    data = fetcher.fetch_sse(browser)  # browser是OpenClaw的browser工具
"""
import logging
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class BrowserFetcher:
    """使用浏览器抓取IPO数据"""
    
    # 交易所URL配置
    EXCHANGES = {
        # A股
        "上交所": "https://www.sse.com.cn/listing/renewal/ipo/",
        "深交所": "https://www.szse.cn/listing/projectdynamic/ipo/",
        "北交所": "https://www.bse.cn/audit/project_news.html",
        # 港股
        "港股新上市": "https://www.hkex.com.hk/Services/Trading/Securities/Trading-News/Newly-Listed-Securities",
        "港股申请": "https://www.hkexnews.hk/app/appindex.html",
        # 美股
        "纳斯达克": "https://www.nasdaq.com/market-activity/ipos",
        "纽交所": "https://www.nyse.com/ipo-center/ipo-calendar",
    }
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('browser_fetcher')
    
    def fetch(self, browser, exchange: str) -> List[Dict]:
        """抓取指定交易所的数据
        
        Args:
            browser: OpenClaw的browser工具
            exchange: 交易所名称
            
        Returns:
            IPO数据列表
        """
        url = self.EXCHANGES.get(exchange)
        if not url:
            self.logger.warning(f"未找到交易所: {exchange}")
            return []
        
        try:
            # 打开页面
            result = browser.action(action="open", url=url)
            tab_id = result.get("targetId")
            
            # 等待加载
            browser.action(
                action="snapshot",
                targetId=tab_id,
                loadState="networkidle",
                timeoutMs=30000
            )
            
            # 根据交易所类型获取不同内容
            if exchange in ["上交所", "深交所", "北交所"]:
                # A股：获取表格HTML
                html = browser.action(
                    action="act",
                    targetId=tab_id,
                    request={
                        "kind": "evaluate",
                        "fn": "document.querySelector('table') ? document.querySelector('table').outerHTML : ''"
                    }
                )
                table_html = html.get('result', '')
            else:
                # 港股/美股：获取整个页面内容
                html = browser.action(
                    action="act",
                    targetId=tab_id,
                    request={
                        "kind": "evaluate",
                        "fn": "document.body.innerText"
                    }
                )
                table_html = html.get('result', '')
            
            if not table_html:
                self.logger.warning(f"{exchange} 未找到内容")
                return []
            
            # 解析数据
            if exchange == "上交所":
                return self._parse_sse(table_html)
            elif exchange == "深交所":
                return self._parse_szse(table_html)
            elif exchange == "北交所":
                return self._parse_bse(table_html)
            elif exchange == "港股新上市":
                return self._parse_hkex_new(table_html)
            elif exchange == "港股申请":
                return self._parse_hkex_app(table_html)
            elif exchange == "纳斯达克":
                return self._parse_nasdaq(table_html)
            elif exchange == "纽交所":
                return self._parse_nyse(table_html)
            else:
                return []
                
        except Exception as e:
            self.logger.exception(f"{exchange} 抓取失败: {e}")
            return []
    
    def _parse_sse(self, html: str) -> List[Dict]:
        """解析上交所表格"""
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        
        if not table:
            return []
        
        results = []
        
        # 遍历数据行（跳过表头）
        for row in table.find_all('tr')[1:]:
            cells = row.find_all('td')
            if len(cells) < 9:
                continue
            
            # 提取文本
            def get_text(cell):
                span = cell.find('span')
                div = cell.find('div')
                if span:
                    return span.get('title', span.get_text(strip=True))
                if div:
                    return div.get('title', div.get_text(strip=True))
                return cell.get_text(strip=True)
            
            # 获取详情链接
            link = row.get('href', '')
            if link and not link.startswith('http'):
                link = 'https://www.sse.com.cn' + link
            
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
                'accept_date': get_text(cells[9]) if len(cells) > 9 else '',
                'stock_code': '',
                'exchange': '上交所',
                'source_url': link or self.EXCHANGES["上交所"],
                'source': '上交所',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            if ipo_info['company_name']:
                results.append(ipo_info)
        
        self.logger.info(f"上交所: 获取 {len(results)} 条记录")
        return results
    
    def _parse_szse(self, html: str) -> List[Dict]:
        """解析深交所表格"""
        # 结构类似上交所
        return self._parse_sse(html)
    
    def _parse_bse(self, html: str) -> List[Dict]:
        """解析北交所表格"""
        soup = BeautifulSoup(html, 'html.parser')
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
                'exchange': '北交所',
                'application_status': get_text(cells[2]) if len(cells) > 2 else '',
                'province': '',
                'industry': '',
                'sponsor': '',
                'law_firm': '',
                'accounting_firm': '',
                'update_date': '',
                'accept_date': '',
                'source_url': self.EXCHANGES["北交所"],
                'source': '北交所',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            
            if ipo_info['company_name']:
                results.append(ipo_info)
        
        self.logger.info(f"北交所: 获取 {len(results)} 条记录")
        return results
    
    def _parse_hkex_new(self, text: str) -> List[Dict]:
        """解析港股新上市页面 - 使用正则表达式提取结构化数据"""
        results = []
        
        # 港股新上市页面常见格式：
        # 公司名称  股票代码  上市日期  发行价  募资金额
        # 使用正则表达式匹配各种格式
        
        # 模式1: 股票代码 + 公司名 + 日期
        # 如: "00123 公司名称 2026-01-15"
        pattern1 = re.compile(
            r'(\d{4,5})\s+([^\d\n]{2,50})\s+(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})',
            re.MULTILINE
        )
        
        # 模式2: 带发行价和募资金额
        # 如: "1234 公司名称 HK$10.00 HK$100M 2026-01-15"
        pattern2 = re.compile(
            r'(\d{4,5})\s+([^\d\n]{2,50})\s+(?:HK)?\$?([\d,.]+)\s*(?:M|m|百万|千万)?\s+(?:HK)?\$?([\d,.]+)?\s*([\d]{4}[-/年]\d{1,2}[-/月]\d{1,2})?',
            re.MULTILINE
        )
        
        for match in pattern1.finditer(text):
            stock_code = match.group(1).strip()
            company_name = match.group(2).strip()
            expected_date = match.group(3).strip()
            
            # 转换日期格式
            expected_date = expected_date.replace('年', '-').replace('月', '-').replace('日', '')
            
            if company_name and len(company_name) >= 2:
                ipo_info = {
                    'company_name': company_name[:50],
                    'stock_code': stock_code,
                    'exchange': '港股新上市',
                    'application_status': '已上市',
                    'expected_date': expected_date,
                    'fundraising_amount': '',
                    'issue_price_range': '',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': '',
                    'accept_date': '',
                    'source_url': self.EXCHANGES["港股新上市"],
                    'source': '港股新上市',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                results.append(ipo_info)
        
        # 如果模式1没匹配到，尝试模式2
        if not results:
            for match in pattern2.finditer(text):
                stock_code = match.group(1).strip()
                company_name = match.group(2).strip()
                issue_price = match.group(3).strip() if match.group(3) else ''
                fundraising = match.group(4).strip() if match.group(4) else ''
                expected_date = match.group(5).strip() if match.group(5) else ''
                
                if expected_date:
                    expected_date = expected_date.replace('年', '-').replace('月', '-').replace('日', '')
                
                if company_name and len(company_name) >= 2:
                    ipo_info = {
                        'company_name': company_name[:50],
                        'stock_code': stock_code,
                        'exchange': '港股新上市',
                        'application_status': '已上市',
                        'expected_date': expected_date,
                        'fundraising_amount': fundraising,
                        'issue_price_range': f'HK${issue_price}' if issue_price else '',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': '',
                        'accept_date': '',
                        'source_url': self.EXCHANGES["港股新上市"],
                        'source': '港股新上市',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    results.append(ipo_info)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r['stock_code']}_{r['company_name']}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        self.logger.info(f"港股新上市: 获取 {len(unique_results)} 条记录")
        return unique_results
    
    def _parse_hkex_app(self, text: str) -> List[Dict]:
        """解析港股申请页面 - 使用正则表达式提取结构化数据"""
        results = []
        
        # 港股申请页面字段：
        # - 公司名称
        # - 股票代码 (4-5位数字)
        # - 发布日期 (YYYY-MM-DD 或 DD/MM/YYYY)
        # - 公告类型 (OC Announcement, Application Proof, 招股书, etc.)
        
        # 模式1: 股票代码 + 公司名 + 日期 + 公告类型
        # 如: "1234 公司名称 15/01/2026 OC Announcement"
        pattern1 = re.compile(
            r'(\d{4,5})\s+([^\d\n]{2,80})\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\s+(OC\s*Announcement|Application\s*Proof|招股说明书|上市申请|披露易|修订|补充)',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 模式2: 公司名 + 股票代码 + 日期 (不同顺序)
        # 如: "公司名称 1234 2026-01-15"
        pattern2 = re.compile(
            r'([^\d\n]{5,80})\s+(\d{4,5})\s+(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})',
            re.MULTILINE
        )
        
        # 模式3: 招股书相关公告
        # 如: "公司名称 招股书 2026-01-15"
        pattern3 = re.compile(
            r'([^\d\n]{5,80})\s*(?:招股说明书|招股书|Prospectus|上市申请)\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})?',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 尝试模式1
        for match in pattern1.finditer(text):
            stock_code = match.group(1).strip()
            company_name = match.group(2).strip()
            pub_date = match.group(3).strip()
            announcement_type = match.group(4).strip()
            
            # 转换日期格式
            try:
                if '/' in pub_date:
                    parts = pub_date.split('/')
                    if len(parts[2]) == 2:
                        year = '20' + parts[2] if int(parts[2]) < 50 else '19' + parts[2]
                    else:
                        year = parts[2]
                    pub_date = f"{year}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
            except:
                pub_date = pub_date.replace('年', '-').replace('月', '-').replace('日', '')
            
            if company_name and len(company_name) >= 2:
                ipo_info = {
                    'company_name': company_name[:80],
                    'stock_code': stock_code,
                    'exchange': '港股申请',
                    'application_status': announcement_type,
                    'expected_date': pub_date,
                    'fundraising_amount': '',
                    'issue_price_range': '',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': pub_date,
                    'accept_date': '',
                    'source_url': self.EXCHANGES["港股申请"],
                    'source': '港股申请',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                results.append(ipo_info)
        
        # 尝试模式2
        if not results:
            for match in pattern2.finditer(text):
                company_name = match.group(1).strip()
                stock_code = match.group(2).strip()
                pub_date = match.group(3).strip()
                
                pub_date = pub_date.replace('年', '-').replace('月', '-').replace('日', '')
                
                if company_name and len(company_name) >= 2:
                    ipo_info = {
                        'company_name': company_name[:80],
                        'stock_code': stock_code,
                        'exchange': '港股申请',
                        'application_status': '上市申请',
                        'expected_date': pub_date,
                        'fundraising_amount': '',
                        'issue_price_range': '',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': pub_date,
                        'accept_date': '',
                        'source_url': self.EXCHANGES["港股申请"],
                        'source': '港股申请',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    results.append(ipo_info)
        
        # 尝试模式3
        if not results:
            for match in pattern3.finditer(text):
                company_name = match.group(1).strip()
                pub_date = match.group(2).strip() if match.group(2) else ''
                
                if pub_date:
                    pub_date = pub_date.replace('年', '-').replace('月', '-').replace('日', '')
                
                if company_name and len(company_name) >= 2:
                    ipo_info = {
                        'company_name': company_name[:80],
                        'stock_code': '',
                        'exchange': '港股申请',
                        'application_status': '招股说明书',
                        'expected_date': pub_date,
                        'fundraising_amount': '',
                        'issue_price_range': '',
                        'province': '',
                        'industry': '',
                        'sponsor': '',
                        'law_firm': '',
                        'accounting_firm': '',
                        'update_date': pub_date,
                        'accept_date': '',
                        'source_url': self.EXCHANGES["港股申请"],
                        'source': '港股申请',
                        'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }
                    results.append(ipo_info)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r['stock_code']}_{r['company_name']}_{r.get('update_date', '')}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        self.logger.info(f"港股申请: 获取 {len(unique_results)} 条记录")
        return unique_results
    
    def _parse_nasdaq(self, text: str) -> List[Dict]:
        """解析纳斯达克IPO页面 - 使用正则表达式提取结构化数据"""
        results = []
        
        # 纳斯达克页面字段：
        # - Symbol代码 (股票代码，如 AAPL)
        # - 公司名称
        # - 发行价
        # - 股数
        # - 上市日期
        # - 募集金额
        
        # 月份映射
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        
        def parse_date(date_str: str) -> str:
            """解析日期格式"""
            try:
                match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})', date_str, re.IGNORECASE)
                if match:
                    month = month_map.get(match.group(1).lower()[:3], '01')
                    day = match.group(2).zfill(2)
                    year = match.group(3)
                    return f"{year}-{month}-{day}"
            except:
                pass
            return ''
        
        # 模式1: Symbol + 公司名 + 发行价 + 股数 + 日期 + 募集金额
        # 如: "AAPL Apple Inc. $150.00 50M Jan 15, 2026 $7.5B"
        pattern1 = re.compile(
            r'([A-Z]{1,5})\s+([A-Za-z][^$]{2,60})\s+\$?([\d,.]+)\s+M\s+(\d+(?:,\d{3})*(?:\.\d+)?)\s*M?\s+([A-Za-z]{3})\s+(\d{1,2}),?\s+(\d{4})\s+\$?([\d,.]+)\s*B?',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 模式2: 发行价区间
        # 如: "GOOGL Google LLC $120-$140 30M Feb 20, 2026"
        pattern2 = re.compile(
            r'([A-Z]{1,5})\s+([A-Za-z][^$]{2,60})\s+\$?([\d,.]+)\s*-\s*\$?([\d,.]+)\s+(\d+)\s*M?\s+([A-Za-z]{3})\s+(\d{1,2}),?\s+(\d{4})',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 模式3: 简化格式 - Symbol + 公司名 + 日期
        # 如: "MSFT Microsoft Corporation Mar 10, 2026"
        pattern3 = re.compile(
            r'([A-Z]{1,5})\s+([A-Za-z][^.]{2,60})\s+([A-Za-z]{3})\s+(\d{1,2}),?\s+(\d{4})',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 尝试模式1
        for match in pattern1.finditer(text):
            symbol = match.group(1).strip()
            company_name = match.group(2).strip()
            price = match.group(3).strip()
            shares = match.group(4).strip()
            expected_date = parse_date(match.group(0))
            raised = match.group(8).strip() if match.group(8) else ''
            
            # 排除非股票代码
            if symbol in ['IPO', 'ETF', 'NYSE', 'SEC', 'USA', 'USD', 'CEO', 'NEWS', 'CALENDAR', 'NEW', 'YORK']:
                continue
                
            ipo_info = {
                'company_name': company_name[:80],
                'stock_code': symbol,
                'exchange': 'NASDAQ',
                'application_status': 'Upcoming',
                'expected_date': expected_date,
                'fundraising_amount': f'${raised}M' if raised else '',
                'issue_price_range': f'${price}',
                'province': '',
                'industry': '',
                'sponsor': '',
                'law_firm': '',
                'accounting_firm': '',
                'update_date': '',
                'accept_date': f'{shares}M',
                'source_url': self.EXCHANGES["纳斯达克"],
                'source': '纳斯达克',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            results.append(ipo_info)
        
        # 尝试模式2 (发行价区间)
        if not results:
            for match in pattern2.finditer(text):
                symbol = match.group(1).strip()
                company_name = match.group(2).strip()
                price_low = match.group(3).strip()
                price_high = match.group(4).strip()
                shares = match.group(5).strip()
                expected_date = f"{match.group(8)}-{month_map.get(match.group(6).lower()[:3], '01')}-{match.group(7).zfill(2)}"
                
                if symbol in ['IPO', 'ETF', 'NYSE', 'SEC', 'USA', 'USD', 'CEO', 'NEWS', 'CALENDAR', 'NEW', 'YORK']:
                    continue
                
                ipo_info = {
                    'company_name': company_name[:80],
                    'stock_code': symbol,
                    'exchange': 'NASDAQ',
                    'application_status': 'Upcoming',
                    'expected_date': expected_date,
                    'fundraising_amount': '',
                    'issue_price_range': f'${price_low}-${price_high}',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': '',
                    'accept_date': f'{shares}M',
                    'source_url': self.EXCHANGES["纳斯达克"],
                    'source': '纳斯达克',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                results.append(ipo_info)
        
        # 尝试模式3 (简化格式)
        if not results:
            for match in pattern3.finditer(text):
                symbol = match.group(1).strip()
                company_name = match.group(2).strip()
                expected_date = f"{match.group(5)}-{month_map.get(match.group(3).lower()[:3], '01')}-{match.group(4).zfill(2)}"
                
                if symbol in ['IPO', 'ETF', 'NYSE', 'SEC', 'USA', 'USD', 'CEO', 'NEWS', 'CALENDAR', 'NEW', 'YORK']:
                    continue
                
                ipo_info = {
                    'company_name': company_name[:80],
                    'stock_code': symbol,
                    'exchange': 'NASDAQ',
                    'application_status': 'Upcoming',
                    'expected_date': expected_date,
                    'fundraising_amount': '',
                    'issue_price_range': '',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': '',
                    'accept_date': '',
                    'source_url': self.EXCHANGES["纳斯达克"],
                    'source': '纳斯达克',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                results.append(ipo_info)
        
        # 如果还没匹配到，尝试更通用的模式
        if not results:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                # 查找包含Symbol的行 (1-5个大写字母)
                symbol_match = re.search(r'\b([A-Z]{1,5})\b', line)
                if symbol_match and len(line) > 5:
                    symbol = symbol_match.group(1)
                    # 排除常见非股票代码的单词
                    if symbol in ['IPO', 'ETF', 'NYSE', 'SEC', 'USA', 'USD', 'CEO', 'NEWS', 'CALENDAR', 'NEW', 'YORK']:
                        continue
                    
                    # 尝试提取公司名（去掉Symbol后的部分）
                    remaining = line.replace(symbol, '', 1).strip()
                    if remaining:
                        ipo_info = {
                            'company_name': remaining[:80],
                            'stock_code': symbol,
                            'exchange': 'NASDAQ',
                            'application_status': 'Upcoming',
                            'expected_date': '',
                            'fundraising_amount': '',
                            'issue_price_range': '',
                            'province': '',
                            'industry': '',
                            'sponsor': '',
                            'law_firm': '',
                            'accounting_firm': '',
                            'update_date': '',
                            'accept_date': '',
                            'source_url': self.EXCHANGES["纳斯达克"],
                            'source': '纳斯达克',
                            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        results.append(ipo_info)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r['stock_code']}_{r['company_name']}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        self.logger.info(f"纳斯达克: 获取 {len(unique_results)} 条记录")
        return unique_results
    
    def _parse_nyse(self, text: str) -> List[Dict]:
        """解析纽交所IPO页面 - 使用正则表达式提取结构化数据"""
        results = []
        
        # 纽交所页面字段与纳斯达克类似
        # Symbol + 公司名 + 发行价 + 股数 + 日期 + 募集金额
        
        # 模式1: Symbol + 公司名 + 发行价 + 股数 + 日期 + 募集金额
        pattern1 = re.compile(
            r'([A-Z]{1,5})\s+([^\$#\n]{3,80})\s+\$?([\d,.]+)\s*(?:M|m|Million)?\s+(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:M|m)?\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}\s+\$?([\d,.]+)\s*(?:B|b|M|m)?',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 模式2: 简化格式 - Symbol + 公司名 + 日期
        pattern2 = re.compile(
            r'([A-Z]{1,5})\s+([^\d\n]{3,80})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',
            re.MULTILINE | re.IGNORECASE
        )
        
        # 月份映射
        month_map = {
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
            'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
            'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        
        def parse_date(date_str: str) -> str:
            """解析日期格式"""
            try:
                match = re.search(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+(\d{1,2}),?\s+(\d{4})', date_str, re.IGNORECASE)
                if match:
                    month = month_map.get(match.group(1).lower()[:3], '01')
                    day = match.group(2).zfill(2)
                    year = match.group(3)
                    return f"{year}-{month}-{day}"
            except:
                pass
            return ''
        
        # 尝试模式1
        for match in pattern1.finditer(text):
            symbol = match.group(1).strip()
            company_name = match.group(2).strip()
            price = match.group(3).strip()
            shares = match.group(4).strip()
            raised = match.group(5).strip() if match.group(5) else ''
            
            ipo_info = {
                'company_name': company_name[:80],
                'stock_code': symbol,
                'exchange': 'NYSE',
                'application_status': 'Upcoming',
                'expected_date': '',
                'fundraising_amount': f'${raised}M' if raised else '',
                'issue_price_range': f'${price}',
                'province': '',
                'industry': '',
                'sponsor': '',
                'law_firm': '',
                'accounting_firm': '',
                'update_date': '',
                'accept_date': shares,
                'source_url': self.EXCHANGES["纽交所"],
                'source': '纽交所',
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            results.append(ipo_info)
        
        # 尝试模式2
        if not results:
            for match in pattern2.finditer(text):
                symbol = match.group(1).strip()
                company_name = match.group(2).strip()
                expected_date = parse_date(match.group(0))
                
                ipo_info = {
                    'company_name': company_name[:80],
                    'stock_code': symbol,
                    'exchange': 'NYSE',
                    'application_status': 'Upcoming',
                    'expected_date': expected_date,
                    'fundraising_amount': '',
                    'issue_price_range': '',
                    'province': '',
                    'industry': '',
                    'sponsor': '',
                    'law_firm': '',
                    'accounting_firm': '',
                    'update_date': '',
                    'accept_date': '',
                    'source_url': self.EXCHANGES["纽交所"],
                    'source': '纽交所',
                    'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
                results.append(ipo_info)
        
        # 如果还没匹配到，使用通用Symbol匹配
        if not results:
            lines = text.split('\n')
            for line in lines:
                line = line.strip()
                symbol_match = re.search(r'\b([A-Z]{1,5})\b', line)
                if symbol_match and len(line) > 5:
                    symbol = symbol_match.group(1)
                    # 排除常见非股票代码
                    if symbol in ['IPO', 'ETF', 'NYSE', 'SEC', 'USA', 'USD', 'CEO', 'IPO', 'NEWS', 'CALENDAR', 'NEW', 'YORK']:
                        continue
                    
                    remaining = line.replace(symbol, '', 1).strip()
                    if remaining:
                        ipo_info = {
                            'company_name': remaining[:80],
                            'stock_code': symbol,
                            'exchange': 'NYSE',
                            'application_status': 'Upcoming',
                            'expected_date': '',
                            'fundraising_amount': '',
                            'issue_price_range': '',
                            'province': '',
                            'industry': '',
                            'sponsor': '',
                            'law_firm': '',
                            'accounting_firm': '',
                            'update_date': '',
                            'accept_date': '',
                            'source_url': self.EXCHANGES["纽交所"],
                            'source': '纽交所',
                            'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        }
                        results.append(ipo_info)
        
        # 去重
        seen = set()
        unique_results = []
        for r in results:
            key = f"{r['stock_code']}_{r['company_name']}"
            if key not in seen:
                seen.add(key)
                unique_results.append(r)
        
        self.logger.info(f"纽交所: 获取 {len(unique_results)} 条记录")
        return unique_results


# 导出
__all__ = ['BrowserFetcher']
