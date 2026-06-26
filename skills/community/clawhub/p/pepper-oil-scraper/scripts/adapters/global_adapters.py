"""
global_adapters.py — 全球市场研究站点爬虫
覆盖：Business Research Insights、Verified Market Reports、WiseGuy Reports
策略：抓取报告摘要页的公开数据（市场规模、CAGR、区域占比）
"""

import re
from urllib.parse import urljoin
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number


class _GlobalReportScraper(BaseScraper):
    """全球研报站点通用基类"""

    def crawl(self):
        for page_url in self.site_cfg.get("target_pages", []):
            if not page_url.startswith("http"):
                page_url = urljoin(self.site_cfg["base_url"], page_url)
            soup = self.fetch_and_parse(page_url)
            if soup:
                self._extract_global_data(soup, page_url)

    def _extract_global_data(self, soup, source_url):
        """提取全球市场报告的关键数据"""
        text = soup.get_text(" ", strip=True)

        # USD market size: "$1.5 billion" / "USD 100 million"
        for m in re.finditer(
            r"(?:USD|US\$|\$)\s*(\d+\.?\d*)\s*(billion|million|B|M)\b",
            text, re.IGNORECASE
        ):
            raw_val = float(m.group(1))
            mult_str = m.group(2).lower()
            if mult_str in ("billion", "b"):
                unit = "USD billion"
            else:
                unit = "USD million"

            start = max(0, m.start() - 80)
            end = min(len(text), m.end() + 80)
            context = text[start:end]

            year_match = re.search(r"20[2-3]\d", context)
            period = year_match.group() if year_match else ""

            metric = "全球市场规模"
            if "sichuan" in context.lower() or "四川" in context:
                metric = "四川风味全球市场规模"
            elif "prickly" in context.lower() or "pepper oil" in context.lower():
                metric = "花椒油全球市场规模"

            self.add_record(
                metric=metric,
                value=raw_val, unit=unit,
                period=period, source_url=source_url,
                original_text=context.strip(), confidence="medium"
            )

        # CAGR
        for m in re.finditer(r"(?:CAGR|compound annual growth rate)[^\d]{0,20}?(\d+\.?\d*)\s*%", text, re.IGNORECASE):
            start = max(0, m.start() - 60)
            context = text[start:m.end() + 40]
            self.add_record(
                metric="全球CAGR", value=float(m.group(1)), unit="%",
                source_url=source_url, original_text=context.strip(),
                confidence="medium"
            )

        # Regional share
        for m in re.finditer(
            r"(North America|Asia Pacific|Europe|Latin America|MEA|China|APAC)[^\d]{0,20}?(\d+\.?\d*)\s*%",
            text, re.IGNORECASE
        ):
            self.add_record(
                metric=f"{m.group(1)}市场份额",
                value=float(m.group(2)), unit="%",
                source_url=source_url,
                original_text=m.group(0), confidence="medium"
            )

        # Forecast year range
        for m in re.finditer(r"(20[2-3]\d)\s*(?:to|–|-|—)\s*(20[2-3]\d)", text):
            self.add_record(
                metric="预测期",
                value=None, unit="",
                period=f"{m.group(1)}-{m.group(2)}",
                source_url=source_url,
                original_text=m.group(0), confidence="high"
            )

        # Key players
        player_section = re.search(
            r"(?:key players|major players|leading companies|competitive landscape)[:\s]*(.*?)(?:\n\n|\.\s[A-Z])",
            text, re.IGNORECASE | re.DOTALL
        )
        if player_section:
            players_text = player_section.group(1)[:500]
            self.add_record(
                metric="全球主要企业",
                value=None, unit="",
                source_url=source_url,
                original_text=players_text, confidence="medium",
                extra={"type": "competitive_landscape"}
            )


class BriScraper(_GlobalReportScraper):
    """Business Research Insights"""
    def __init__(self, config=None):
        super().__init__("bri", config)


class VmrScraper(_GlobalReportScraper):
    """Verified Market Reports"""
    def __init__(self, config=None):
        super().__init__("vmr", config)


class WiseguyScraper(_GlobalReportScraper):
    """WiseGuy Reports"""
    def __init__(self, config=None):
        super().__init__("wiseguy", config)
