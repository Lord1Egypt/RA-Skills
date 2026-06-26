"""
media_adapters.py — 财经媒体站点爬虫
覆盖：36氪、界面新闻、CBNData、央广网
策略：抓取文章正文，提取内嵌的数据点（营收、市场规模、份额等）
"""

import re
from urllib.parse import urljoin, quote
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number


class _MediaBaseScraper(BaseScraper):
    """媒体站点通用基类：目标文章抓取 + 数据提取"""

    def crawl(self):
        # 1. 目标文章
        for page_url in self.site_cfg.get("target_pages", []):
            if not page_url.startswith("http"):
                page_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(page_url)
            if soup:
                self._extract_article_data(soup, page_url)

        # 2. 搜索
        search_tpl = self.site_cfg.get("search_url", "")
        if search_tpl:
            for kw in ["花椒油", "藤椒油", "幺麻子"]:
                url = search_tpl.format(keyword=quote(kw))
                soup = self.fetch_and_parse(url)
                if soup:
                    self._parse_search(soup, url)

    def _extract_article_data(self, soup, source_url):
        """从文章正文提取所有关键数据"""
        # 获取正文
        selectors = [
            "article", ".article-content", ".article_content",
            ".entry-content", ".post-content", ".richtext",
            "#artibody", ".content", ".TRS_Editor", ".text",
            ".article-detail-content", ".article-body"
        ]
        article = None
        for sel in selectors:
            article = soup.select_one(sel)
            if article:
                break
        if article is None:
            article = soup

        text = article.get_text(" ", strip=True)

        # 标题
        title = ""
        title_el = soup.select_one("h1, .article-title, .title")
        if title_el:
            title = title_el.get_text(strip=True)

        # 数据模式匹配
        patterns = {
            "营业收入": [
                r"(?:营业收入|营收|收入)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|万元|百万元)"
            ],
            "净利润": [
                r"(?:净利润|归母净利|利润)[^\d]{0,15}?(\d+\.?\d*)\s*(亿元|万元|百万元)"
            ],
            "毛利率": [
                r"(?:毛利率|综合毛利率)[^\d]{0,10}?(\d+\.?\d*)\s*%"
            ],
            "市场规模": [
                r"(?:市场规模|市场总值|行业规模)[^\d]{0,20}?(\d+\.?\d*)\s*(亿元|万元|亿美元)",
                r"(\d+\.?\d*)\s*(亿元|亿美元)[^\d]{0,10}?(?:市场|规模)"
            ],
            "市场份额": [
                r"(?:市场份额|市占率|占比)[^\d]{0,10}?(\d+\.?\d*)\s*%",
                r"(\d+\.?\d*)\s*%[^\d]{0,10}?(?:份额|占比|市占)"
            ],
            "CAGR": [
                r"(?:CAGR|年均增长|复合增长率)[^\d]{0,15}?(\d+\.?\d*)\s*%"
            ],
            "产能": [
                r"(?:产能|年产能)[^\d]{0,10}?(\d+\.?\d*)\s*(万吨|吨)"
            ],
            "种植面积": [
                r"(?:种植面积|总面积)[^\d]{0,10}?(\d+\.?\d*)\s*(万亩|亩)"
            ],
            "产量": [
                r"(?:产量|年产量|总产量)[^\d]{0,10}?(\d+\.?\d*)\s*(万吨|吨)"
            ],
        }

        for metric, pats in patterns.items():
            for pat in pats:
                for m in re.finditer(pat, text):
                    start = max(0, m.start() - 50)
                    end = min(len(text), m.end() + 50)
                    context = text[start:end]

                    unit = m.group(2) if len(m.groups()) >= 2 else "%"
                    year_match = re.search(r"20[12]\d", context)
                    period = year_match.group() if year_match else ""

                    self.add_record(
                        metric=metric,
                        value=float(m.group(1)), unit=unit,
                        period=period, source_url=source_url,
                        original_text=context.strip(),
                        confidence="medium",
                        extra={"article_title": title[:100]}
                    )

    def _parse_search(self, soup, source_url):
        for a in soup.select("a[href]")[:15]:
            title = a.get_text(strip=True)
            if len(title) > 10 and any(kw in title for kw in ["花椒", "藤椒", "幺麻子", "调味", "麻"]):
                href = urljoin(source_url, a.get("href", ""))
                if href.startswith("http"):
                    self.add_record(
                        metric="媒体文章",
                        value=None, unit="",
                        source_url=href,
                        original_text=title, confidence="low",
                        extra={"type": "media_article"}
                    )


class Kr36Scraper(_MediaBaseScraper):
    """36氪 36kr.com"""
    def __init__(self, config=None):
        super().__init__("kr36", config)


class JiemianScraper(_MediaBaseScraper):
    """界面新闻 jiemian.com"""
    def __init__(self, config=None):
        super().__init__("jiemian", config)


class CbndataScraper(_MediaBaseScraper):
    """CBNData cbndata.com"""
    def __init__(self, config=None):
        super().__init__("cbndata", config)


class CnrScraper(_MediaBaseScraper):
    """
    央广网 cnr.cn — 花椒产业研究报告
    这是数据密度最高的来源之一，包含花椒产业全链条数据
    """
    def __init__(self, config=None):
        super().__init__("cnr", config)

    def _extract_article_data(self, soup, source_url):
        """央广网的花椒产业报告数据极其丰富，增加更多提取模式"""
        # 先调用通用提取
        super()._extract_article_data(soup, source_url)

        # 额外提取：产区数据表
        article = soup.select_one("article, .article_content, .TRS_Editor, .content")
        if article is None:
            article = soup
        text = article.get_text(" ", strip=True)

        # 各省种植面积
        for m in re.finditer(r"(四川|甘肃|陕西|云南|贵州|重庆|河南|河北|山东|湖北)[^\d]{0,30}?(\d+\.?\d*)\s*(万亩|亩|万吨|吨|亿元)", text):
            context_start = max(0, m.start() - 20)
            context = text[context_start:m.end() + 20]
            self.add_record(
                metric=f"{m.group(1)}花椒数据",
                value=float(m.group(2)), unit=m.group(3),
                region=m.group(1), source_url=source_url,
                original_text=context, confidence="medium"
            )

        # 渠道占比
        for m in re.finditer(r"(餐饮|家庭|食品加工|零售|电商)[^\d]{0,15}?(\d+\.?\d*)\s*%", text):
            context_start = max(0, m.start() - 20)
            context = text[context_start:m.end() + 20]
            self.add_record(
                metric=f"{m.group(1)}渠道占比",
                value=float(m.group(2)), unit="%",
                source_url=source_url,
                original_text=context, confidence="medium"
            )

        # 产品形态占比
        for m in re.finditer(r"(干花椒|花椒油|保鲜花椒|花椒酱|花椒提取物)[^\d]{0,10}?(?:占|约)?(\d+\.?\d*)\s*%", text):
            self.add_record(
                metric=f"{m.group(1)}产品占比",
                value=float(m.group(2)), unit="%",
                source_url=source_url,
                original_text=m.group(0), confidence="medium"
            )
