"""
gov_adapters.py — 政府与标准站点爬虫
覆盖：国家林草局、农业农村部、海关总署、国标全文公开系统
"""

import re
import json
from urllib.parse import urljoin, quote
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number


class ForestryScraper(BaseScraper):
    """
    国家林草局 forestry.gov.cn — 花椒种植面积、产量、政策
    核心数据页：/c/www/lcdt/522070.jhtml（花椒专题）
    """

    def __init__(self, config=None):
        super().__init__("forestry", config)

    def crawl(self):
        # 1. 目标页
        for page_url in self.site_cfg.get("target_pages", []):
            full_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(full_url)
            if soup:
                self._extract_forestry_data(soup, full_url)

        # 2. 搜索
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["花椒", "花椒种植", "花椒产业"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    self._parse_search(soup, url)

    def _extract_forestry_data(self, soup, source_url):
        """从林草局花椒专题页提取数据"""
        article = soup.select_one(".TRS_Editor, .article-content, .content, #zoom, .text")
        if article is None:
            article = soup
        text = article.get_text(" ", strip=True)

        # 种植面积
        for m in re.finditer(r"(?:种植面积|栽培面积|总面积|花椒[^\d]{0,8}?面积)[^\d]{0,15}?(\d+\.?\d*)\s*(万亩|亩|公顷|万公顷)", text):
            start = max(0, m.start() - 30)
            context = text[start:m.end() + 30]
            self.add_record(
                metric="花椒种植面积", value=float(m.group(1)), unit=m.group(2),
                source_url=source_url, original_text=context, confidence="high"
            )

        # 产量
        for m in re.finditer(r"(?:产量|年产|总产)[^\d]{0,15}?(\d+\.?\d*)\s*(万吨|吨|千吨)", text):
            start = max(0, m.start() - 30)
            context = text[start:m.end() + 30]
            self.add_record(
                metric="花椒产量", value=float(m.group(1)), unit=m.group(2),
                source_url=source_url, original_text=context, confidence="high"
            )

        # 产值
        for m in re.finditer(r"(?:产值|综合产值|总产值)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|万元)", text):
            start = max(0, m.start() - 30)
            context = text[start:m.end() + 30]
            self.add_record(
                metric="花椒产业产值", value=float(m.group(1)), unit=m.group(2),
                source_url=source_url, original_text=context, confidence="high"
            )

        # 消费量
        for m in re.finditer(r"(?:消费量|需求量|消耗量)[^\d]{0,15}?(\d+\.?\d*)\s*(万吨|吨)", text):
            start = max(0, m.start() - 30)
            context = text[start:m.end() + 30]
            self.add_record(
                metric="花椒消费量", value=float(m.group(1)), unit=m.group(2),
                source_url=source_url, original_text=context, confidence="high"
            )

        # 各省数据
        provinces = ["四川", "甘肃", "陕西", "云南", "贵州", "重庆", "河南", "河北", "山东", "湖北"]
        for prov in provinces:
            prov_pattern = rf"{prov}[^\d]{{0,30}}?(\d+\.?\d*)\s*(万亩|亩|万吨|吨|亿元|万元)"
            for m in re.finditer(prov_pattern, text):
                start = max(0, m.start() - 10)
                context = text[start:m.end() + 20]
                self.add_record(
                    metric=f"{prov}花椒数据", value=float(m.group(1)), unit=m.group(2),
                    region=prov, source_url=source_url,
                    original_text=context, confidence="medium"
                )

    def _parse_search(self, soup, source_url):
        for a in soup.select("a[href]")[:15]:
            title = a.get_text(strip=True)
            if len(title) > 8 and "花椒" in title:
                href = urljoin(source_url, a.get("href", ""))
                self.add_record(
                    metric="政策/资讯链接", value=None, unit="",
                    source_url=href, original_text=title, confidence="low",
                    extra={"type": "gov_article"}
                )


class MoaScraper(BaseScraper):
    """
    农业农村部 moa.gov.cn — 农产品市场价格信息
    """

    def __init__(self, config=None):
        super().__init__("moa", config)

    def crawl(self):
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["花椒", "花椒价格", "花椒产业"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    for a in soup.select("a[href]")[:15]:
                        title = a.get_text(strip=True)
                        if len(title) > 8 and any(k in title for k in ["花椒", "调味", "香料"]):
                            href = urljoin(url, a.get("href", ""))
                            self.add_record(
                                metric="农业部资讯", value=None, unit="",
                                source_url=href, original_text=title, confidence="low",
                                extra={"type": "gov_article"}
                            )


class CustomsScraper(BaseScraper):
    """
    海关总署 customs.gov.cn — 花椒进出口数据
    注意：统计查询系统需 JS + 验证码，此适配器只抓取公开页面的数据
    完整数据建议使用 stats.customs.gov.cn 手动查询
    """

    def __init__(self, config=None):
        super().__init__("customs", config)

    def crawl(self):
        base = self.site_cfg["base_url"]
        hs_codes = self.site_cfg.get("hs_codes", self.config.get("hs_codes", []))

        # 搜索海关网站公开的花椒相关新闻/数据
        for kw in ["花椒 出口", "花椒 进口", "0910991000"]:
            search_url = f"{base}/search/search?keyword={quote(kw)}"
            soup = self.fetch_and_parse(search_url)
            if soup:
                for a in soup.select("a[href]")[:10]:
                    title = a.get_text(strip=True)
                    if len(title) > 6:
                        href = urljoin(base, a.get("href", ""))
                        self.add_record(
                            metric="海关数据/资讯", value=None, unit="",
                            source_url=href, original_text=title, confidence="low",
                            extra={"type": "customs_article", "hs_codes": hs_codes}
                        )

        # 记录 HS 编码信息以便手动查询
        for code in hs_codes:
            self.add_record(
                metric="花椒HS编码",
                value=None, unit="",
                source_url=f"http://stats.customs.gov.cn/",
                original_text=f"HS编码 {code}：花椒、竹叶花椒和青花椒（2023年起独立编码）",
                confidence="high",
                extra={"hs_code": code, "note": "需在 stats.customs.gov.cn 手动查询进出口量"}
            )


class SamrStdScraper(BaseScraper):
    """
    国家标准全文公开系统 openstd.samr.gov.cn — 花椒油相关标准
    """

    def __init__(self, config=None):
        super().__init__("samr_std", config)

    def crawl(self):
        keywords = self.site_cfg.get("search_keywords", ["花椒油", "花椒", "GB/T 30391"])
        base = self.site_cfg["base_url"]

        # 已知标准列表（硬编码高价值数据）
        known_standards = [
            {"code": "DBS51/008-2019", "name": "食品安全地方标准 花椒油", "type": "四川地方标准",
             "note": "花椒油专项标准，含麻味物质检测方法"},
            {"code": "GB/T 30391-2024", "name": "花椒", "type": "国家标准",
             "note": "以挥发油含量为依据分级，2025年4月实施"},
            {"code": "GB/T 22479-2022", "name": "花椒籽油", "type": "国家标准",
             "note": "花椒籽油术语、分类、质量要求"},
            {"code": "GB/T 38495-2020", "name": "感官分析 花椒麻度评价 斯科维尔指数法", "type": "国家标准",
             "note": "花椒及制品麻度感官评价"},
            {"code": "GH/T 1290-2020", "name": "花椒酰胺总含量的测定", "type": "行业标准",
             "note": "紫外分光光度法"},
            {"code": "DB5118/T 19-2021", "name": "地理标志产品 汉源花椒油", "type": "地方标准",
             "note": "国内首个花椒油类地理标志标准"},
            {"code": "T/DCQHJY 01-2022", "name": "青花椒油", "type": "团体标准", "note": ""},
            {"code": "T/TSSP 039-2023", "name": "花椒芳香油", "type": "团体标准", "note": ""},
        ]

        for std in known_standards:
            self.add_record(
                metric=f"标准:{std['code']}",
                value=None, unit="",
                source_url=f"{base}/bzgk/gb/",
                original_text=f"{std['code']} {std['name']} ({std['type']}) {std['note']}",
                confidence="high",
                extra={"standard_code": std["code"], "standard_name": std["name"],
                       "standard_type": std["type"]}
            )

        # 尝试搜索更多标准
        for kw in keywords:
            search_url = f"{base}/bzgk/gb/std_list?p.p1=0&p.p90=circulation_date&p.p91=desc&p.p2={quote(kw)}"
            soup = self.fetch_and_parse(search_url)
            if soup:
                for row in soup.select("tr, .std-item, li"):
                    text = row.get_text(" ", strip=True)
                    if re.search(r"GB|DB|GH|T/", text) and ("花椒" in text or "椒" in text):
                        self.add_record(
                            metric="标准搜索结果",
                            value=None, unit="",
                            source_url=search_url,
                            original_text=text[:200], confidence="medium",
                            extra={"type": "standard_search"}
                        )
