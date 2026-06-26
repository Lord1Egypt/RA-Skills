"""
report_adapters.py — 行业研究报告站点爬虫
覆盖：观研天下、中商产业研究院、智研咨询、前瞻产业研究院、中研网、共研网
策略：抓取报告摘要页的公开数据（市场规模、增长率、图表描述等）
"""

import re
import json
from urllib.parse import urljoin, quote
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number, extract_all_numbers


class _ReportBaseScraper(BaseScraper):
    """研报站点通用基类：搜索 + 目标页 + 数据提取"""

    def crawl(self):
        # 1. 抓取目标页面（已知的高价值页面）
        for page_url in self.site_cfg.get("target_pages", []):
            if not page_url.startswith("http"):
                page_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(page_url)
            if soup:
                self._extract_report_data(soup, page_url)

        # 2. 搜索关键词
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["花椒油", "藤椒油", "花椒市场", "调味油"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    self._parse_search_results(soup, url)

    def _extract_report_data(self, soup, source_url):
        """从报告摘要页提取数据：市场规模、CAGR、份额等"""
        text = soup.get_text(" ", strip=True)

        # 市场规模模式："XX市场规模为/达到 123.4 亿元"
        for pattern in [
            r"(?:市场规模|市场总值|行业规模|产值)[^\d]{0,20}?(\d+\.?\d*)\s*(亿元|万元|百万元|亿美元)",
            r"(\d+\.?\d*)\s*(亿元|亿美元)[^\d]{0,10}?(?:市场规模|的规模|规模约)",
            r"(?:预计|预测|将达|达到)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|亿美元)",
        ]:
            for m in re.finditer(pattern, text):
                value, unit = float(m.group(1)), m.group(2)
                # 找前后文做上下文
                start = max(0, m.start() - 50)
                end = min(len(text), m.end() + 50)
                context = text[start:end]

                metric = "市场规模"
                if "藤椒" in context:
                    metric = "藤椒油市场规模"
                elif "花椒油" in context:
                    metric = "花椒油市场规模"
                elif "调味油" in context:
                    metric = "调味油市场规模"

                # 尝试找年份
                year_match = re.search(r"20[12]\d", context)
                period = year_match.group() if year_match else ""

                self.add_record(
                    metric=metric, value=value, unit=unit,
                    period=period, source_url=source_url,
                    original_text=context, confidence="medium"
                )

        # CAGR 模式
        for m in re.finditer(r"(?:CAGR|年均增长率|复合增长率|年复合)[^\d]{0,15}?(\d+\.?\d*)\s*%", text):
            start = max(0, m.start() - 60)
            context = text[start:m.end() + 30]
            self.add_record(
                metric="CAGR", value=float(m.group(1)), unit="%",
                source_url=source_url,
                original_text=context, confidence="medium"
            )

        # 产量/面积
        for m in re.finditer(r"(?:产量|种植面积|总面积)[^\d]{0,15}?(\d+\.?\d*)\s*(万吨|万亩|吨|亩)", text):
            start = max(0, m.start() - 40)
            context = text[start:m.end() + 30]
            self.add_record(
                metric=m.group(0)[:20], value=float(m.group(1)), unit=m.group(2),
                source_url=source_url,
                original_text=context, confidence="medium"
            )

        # 市场份额
        for m in re.finditer(r"([\u4e00-\u9fa5]{2,8})[^\d]{0,10}?(?:市场份额|占比|市占率)[^\d]{0,10}?(\d+\.?\d*)\s*%", text):
            self.add_record(
                metric=f"{m.group(1)}市场份额",
                value=float(m.group(2)), unit="%",
                source_url=source_url,
                original_text=m.group(0), confidence="medium"
            )

    def _parse_search_results(self, soup, source_url):
        """解析搜索结果，收集报告链接和摘要"""
        for a in soup.select("a[href]")[:20]:
            title = a.get_text(strip=True)
            if len(title) < 8:
                continue
            if any(kw in title for kw in ["花椒", "藤椒", "调味油", "调味品", "麻椒"]):
                href = urljoin(source_url, a.get("href", ""))
                self.add_record(
                    metric="相关报告",
                    value=None, unit="",
                    source_url=href,
                    original_text=title, confidence="low",
                    extra={"type": "report_link"}
                )


class ChinabaogaoScraper(_ReportBaseScraper):
    """观研天下 chinabaogao.com"""
    def __init__(self, config=None):
        super().__init__("chinabaogao", config)


class AskciScraper(_ReportBaseScraper):
    """中商产业研究院 askci.com"""
    def __init__(self, config=None):
        super().__init__("askci", config)


class ChyxxScraper(_ReportBaseScraper):
    """智研咨询 chyxx.com"""
    def __init__(self, config=None):
        super().__init__("chyxx", config)


class QianzhanScraper(_ReportBaseScraper):
    """前瞻产业研究院 qianzhan.com"""
    def __init__(self, config=None):
        super().__init__("qianzhan", config)


class ChinairnScraper(_ReportBaseScraper):
    """中研网 chinairn.com"""
    def __init__(self, config=None):
        super().__init__("chinairn", config)


class GonynScraper(_ReportBaseScraper):
    """共研网 gonyn.com"""
    def __init__(self, config=None):
        super().__init__("gonyn", config)
