"""
company_adapters.py — 企业与财报站点爬虫
覆盖：巨潮资讯网、东方财富、新浪财经、导油网
"""

import re
import json
from urllib.parse import urljoin, quote
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number


class CninfoScraper(BaseScraper):
    """
    巨潮资讯网 cninfo.com.cn — 年报/招股书 PDF 链接
    策略：通过公告查询 API 搜索目标公司的年报和招股书
    注意：PDF 下载需额外处理，此处只采集公告列表与链接
    """

    def __init__(self, config=None):
        super().__init__("cninfo", config)

    def crawl(self):
        api_url = self.site_cfg.get("api_url", "http://www.cninfo.com.cn/new/hisAnnouncement/query")
        companies = self.config.get("companies", {})

        for name, info in companies.items():
            code = info.get("stock_code")
            if not code:
                continue

            # 查询年报
            self._query_announcements(api_url, code, name, "年度报告")
            # 查询招股书
            self._query_announcements(api_url, code, name, "招股说明书")

    def _query_announcements(self, api_url, stock_code, company_name, keyword):
        """通过巨潮 API 查询公告"""
        params = {
            "stock": stock_code,
            "searchkey": keyword,
            "category": "",
            "pageNum": 1,
            "pageSize": 10,
            "column": "szse",  # 深交所/北交所
            "tabName": "fulltext",
            "sortName": "",
            "sortType": "",
            "limit": "",
            "seDate": "",
        }

        resp = self.fetch(api_url, method="POST", data=params)
        if resp is None:
            # 尝试 GET
            resp = self.fetch(f"{api_url}?stock={stock_code}&searchkey={quote(keyword)}&pageNum=1&pageSize=10")

        if resp is None:
            self.logger.warning(f"Cannot fetch announcements for {company_name}")
            return

        try:
            data = resp.json()
        except (json.JSONDecodeError, ValueError):
            # 可能返回 HTML，尝试解析
            self._parse_announcement_html(resp, company_name, keyword)
            return

        announcements = data.get("announcements", data.get("classifiedAnnouncements", []))
        if isinstance(announcements, list):
            for ann in announcements[:5]:
                title = ann.get("announcementTitle", "")
                adj_url = ann.get("adjunctUrl", "")
                ann_time = ann.get("announcementTime", "")

                pdf_url = ""
                if adj_url:
                    pdf_url = f"http://static.cninfo.com.cn/{adj_url}"

                self.add_record(
                    metric=f"{company_name}{keyword}",
                    value=None, unit="",
                    period=str(ann_time)[:10] if ann_time else "",
                    source_url=pdf_url,
                    original_text=title,
                    confidence="high",
                    extra={"company": company_name, "stock_code": stock_code, "doc_type": keyword}
                )

    def _parse_announcement_html(self, resp, company_name, keyword):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(resp.text, "lxml")
        for a in soup.select("a[href*='.pdf'], a[href*='announcement']")[:5]:
            title = a.get_text(strip=True)
            href = a.get("href", "")
            if keyword[:2] in title or company_name[:2] in title:
                self.add_record(
                    metric=f"{company_name}公告",
                    value=None, unit="",
                    source_url=urljoin("http://www.cninfo.com.cn", href),
                    original_text=title, confidence="medium",
                    extra={"company": company_name}
                )


class EastmoneyScraper(BaseScraper):
    """
    东方财富 eastmoney.com — 财务数据 API
    策略：利用东方财富开放 API 获取目标公司财务指标
    """

    def __init__(self, config=None):
        super().__init__("eastmoney", config)

    def crawl(self):
        companies = self.config.get("companies", {})
        for name, info in companies.items():
            code = info.get("stock_code")
            exchange = info.get("exchange", "")
            if not code:
                continue

            # 构建东方财富股票代码格式
            if exchange == "SH":
                em_code = f"SH{code}"
                secid = f"1.{code}"
            elif exchange == "NQ":
                em_code = f"BJ{code}"
                secid = f"0.{code}"
            elif exchange == "HK":
                continue  # 港股走不同 API
            else:
                em_code = code
                secid = f"0.{code}"

            # 利润表核心指标
            self._fetch_financial_summary(secid, em_code, name, code)

    def _fetch_financial_summary(self, secid, em_code, company_name, stock_code):
        """获取最近几年的营收、净利润等"""
        # 东方财富财务数据 API
        url = (
            f"https://datacenter.eastmoney.com/securities/api/data/v1/get?"
            f"reportName=RPT_LICO_FN_CPD&columns=ALL&quoteColumns=&"
            f"filter=(SECURITY_CODE%3D%22{stock_code}%22)&"
            f"pageNumber=1&pageSize=5&sortTypes=-1&sortColumns=REPORT_DATE"
        )

        resp = self.fetch(url)
        if resp is None:
            return

        try:
            data = resp.json()
        except (json.JSONDecodeError, ValueError):
            return

        result = data.get("result", {})
        records = result.get("data", [])

        for rec in records:
            period = rec.get("REPORT_DATE", "")[:10]
            revenue = rec.get("TOTAL_OPERATE_INCOME")
            net_profit = rec.get("PARENT_NETPROFIT")
            gross_margin = rec.get("GROSS_PROFIT_RATIO")

            if revenue is not None:
                self.add_record(
                    metric=f"{company_name}营业收入",
                    value=revenue / 1e8, unit="亿元",
                    period=period, source_url=url,
                    original_text=f"营收{revenue}", confidence="high",
                    extra={"company": company_name, "stock_code": stock_code}
                )
            if net_profit is not None:
                self.add_record(
                    metric=f"{company_name}净利润",
                    value=net_profit / 1e8, unit="亿元",
                    period=period, source_url=url,
                    original_text=f"净利润{net_profit}", confidence="high",
                    extra={"company": company_name, "stock_code": stock_code}
                )
            if gross_margin is not None:
                self.add_record(
                    metric=f"{company_name}毛利率",
                    value=gross_margin, unit="%",
                    period=period, source_url=url,
                    original_text=f"毛利率{gross_margin}%", confidence="high",
                    extra={"company": company_name, "stock_code": stock_code}
                )


class SinaFinanceScraper(BaseScraper):
    """
    新浪财经 finance.sina.com.cn — 企业新闻、财报解读
    """

    def __init__(self, config=None):
        super().__init__("sina_finance", config)

    def crawl(self):
        # 抓目标页面
        for page_url in self.site_cfg.get("target_pages", []):
            if not page_url.startswith("http"):
                page_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(page_url)
            if soup:
                self._extract_article(soup, page_url)

        # 搜索
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["幺麻子", "藤椒油", "花椒油 企业"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    self._parse_search(soup, url)

    def _extract_article(self, soup, source_url):
        """从文章正文中提取关键财务数据"""
        # 获取正文
        article = soup.select_one("#artibody, .article-content, .main-content, article")
        if article is None:
            article = soup
        text = article.get_text(" ", strip=True)

        # 营收/净利润
        for pattern in [
            r"(?:营业收入|营收|总收入)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|万元)",
            r"(?:净利润|归母净利)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|万元)",
            r"(?:毛利率|净利率)[^\d]{0,10}?(\d+\.?\d*)\s*%",
        ]:
            for m in re.finditer(pattern, text):
                start = max(0, m.start() - 40)
                context = text[start:m.end() + 30]
                metric = "财务指标"
                if "营" in context: metric = "营业收入"
                elif "净利" in context: metric = "净利润"
                elif "毛利率" in context: metric = "毛利率"
                elif "净利率" in context: metric = "净利率"

                unit = m.group(2) if len(m.groups()) >= 2 else "%"
                self.add_record(
                    metric=metric,
                    value=float(m.group(1)), unit=unit,
                    source_url=source_url,
                    original_text=context, confidence="medium"
                )

    def _parse_search(self, soup, source_url):
        for a in soup.select("a[href]")[:15]:
            title = a.get_text(strip=True)
            if len(title) > 10 and any(kw in title for kw in ["幺麻子", "藤椒", "花椒", "天味", "颐海"]):
                href = a.get("href", "")
                self.add_record(
                    metric="新闻链接",
                    value=None, unit="",
                    source_url=href,
                    original_text=title, confidence="low",
                    extra={"type": "news_link"}
                )


class OilcnScraper(BaseScraper):
    """
    导油网 oilcn.com — 食用油行业资讯
    """

    def __init__(self, config=None):
        super().__init__("oilcn", config)

    def crawl(self):
        for page_url in self.site_cfg.get("target_pages", []):
            if not page_url.startswith("http"):
                page_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(page_url)
            if soup:
                article = soup.select_one(".article-content, .entry-content, .content, article")
                if article is None:
                    article = soup
                text = article.get_text(" ", strip=True)

                # 提取关键数据点
                for pattern in [
                    r"(?:营[业收入]*|营收)[^\d]{0,10}?(\d+\.?\d*)\s*(亿元|万元)",
                    r"(?:产能|产量)[^\d]{0,10}?(\d+\.?\d*)\s*(万?吨)",
                    r"(?:市场[规模份额]*)[^\d]{0,10}?(\d+\.?\d*)\s*(亿元|%)",
                ]:
                    for m in re.finditer(pattern, text):
                        start = max(0, m.start() - 30)
                        context = text[start:m.end() + 20]
                        self.add_record(
                            metric="行业数据",
                            value=float(m.group(1)), unit=m.group(2),
                            source_url=page_url,
                            original_text=context, confidence="medium"
                        )

        # 搜索
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["花椒油", "藤椒油"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    for a in soup.select("a[href]")[:10]:
                        title = a.get_text(strip=True)
                        if len(title) > 8:
                            self.add_record(
                                metric="资讯链接",
                                value=None, unit="",
                                source_url=urljoin(url, a.get("href", "")),
                                original_text=title, confidence="low",
                                extra={"type": "article_link"}
                            )
