"""
price_adapters.py — 原料价格类站点爬虫
覆盖：惠农网、一亩田、新华花椒价格指数、花椒大数据网、中国花椒网
"""

import re
import json
from urllib.parse import urljoin, quote
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_scraper import BaseScraper, extract_number, extract_all_numbers


class CnhnbScraper(BaseScraper):
    """
    惠农网 cnhnb.com — 花椒/藤椒实时批发价、历史走势
    策略：抓取行情列表页，解析产品名、价格、产地、日期
    """

    def __init__(self, config=None):
        super().__init__("cnhnb", config)

    def crawl(self):
        base = self.site_cfg["base_url"]

        # 1. 抓取固定行情页
        for endpoint in self.site_cfg.get("endpoints", []):
            url = urljoin(base, endpoint)
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue
            self._parse_price_list(soup, url)

        # 2. 关键词搜索
        search_tpl = self.site_cfg.get("search_url", "")
        for kw in ["花椒", "藤椒", "青花椒", "红花椒"]:
            url = search_tpl.format(keyword=quote(kw))
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue
            self._parse_price_list(soup, url)

    def _parse_price_list(self, soup, source_url):
        # 惠农网行情列表通常在 .market-list 或 table 中
        # 尝试多种选择器适配
        rows = soup.select(".market-list li, .quote-list li, table.quote-table tr, .hangqing-list .item")
        if not rows:
            # 通用回退：找所有含价格模式的文本块
            rows = soup.find_all(string=re.compile(r"\d+\.?\d*\s*元/?(斤|公斤|kg)"))
            for text in rows:
                parent = text.find_parent()
                if parent:
                    self._extract_price_from_text(parent.get_text(strip=True), source_url)
            return

        for row in rows:
            text = row.get_text(" ", strip=True)
            self._extract_price_from_text(text, source_url)

    def _extract_price_from_text(self, text, source_url):
        """从文本行中提取品名、价格、产地"""
        # 匹配 "XX花椒 30.00元/斤 四川汉源" 模式
        price_match = re.search(r"(\d+\.?\d*)\s*元[/／](斤|公斤|kg)", text)
        if not price_match:
            return

        value = float(price_match.group(1))
        unit = f"元/{price_match.group(2)}"

        # 尝试提取品名
        name = ""
        for kw in ["大红袍", "九叶青", "藤椒", "青花椒", "红花椒", "花椒", "麻椒"]:
            if kw in text:
                name = kw
                break

        # 尝试提取产地
        region = ""
        for r in ["汉源", "韩城", "武都", "金阳", "江津", "茂县", "盐源", "秦安", "洪雅"]:
            if r in text:
                region = r
                break

        self.add_record(
            metric=f"{name or '花椒'}批发价",
            value=value, unit=unit,
            region=region, source_url=source_url,
            original_text=text, confidence="high"
        )


class YmtScraper(BaseScraper):
    """
    一亩田 ymt.com — 花椒产地收购价
    """

    def __init__(self, config=None):
        super().__init__("ymt", config)

    def crawl(self):
        base = self.site_cfg["base_url"]
        for endpoint in self.site_cfg.get("endpoints", []):
            url = urljoin(base, endpoint)
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue
            self._parse_ymt_list(soup, url)

        # 搜索
        search_tpl = self.site_cfg.get("search_url", "")
        for kw in ["花椒", "藤椒"]:
            url = search_tpl.format(keyword=quote(kw))
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue
            self._parse_ymt_list(soup, url)

    def _parse_ymt_list(self, soup, source_url):
        # 一亩田价格列表
        items = soup.select(".price-item, .list-item, .product-item, tr")
        for item in items:
            text = item.get_text(" ", strip=True)
            price_match = re.search(r"(\d+\.?\d*)\s*元[/／](斤|公斤|kg)", text)
            if not price_match:
                continue

            region = ""
            for r in ["四川", "陕西", "甘肃", "重庆", "贵州", "云南", "河南", "河北", "山东"]:
                if r in text:
                    region = r
                    break

            self.add_record(
                metric="花椒产地收购价",
                value=float(price_match.group(1)),
                unit=f"元/{price_match.group(2)}",
                region=region, source_url=source_url,
                original_text=text, confidence="high"
            )


class CnfinIndexScraper(BaseScraper):
    """
    新华·中国（武都）花椒价格指数 indices.cnfin.com
    策略：优先尝试 API 接口，回退到页面解析
    """

    def __init__(self, config=None):
        super().__init__("cnfin_index", config)

    def crawl(self):
        # 尝试 API
        for api_url in self.site_cfg.get("api_endpoints", []):
            resp = self.fetch(api_url)
            if resp and resp.status_code == 200:
                try:
                    data = resp.json()
                    self._parse_api_data(data, api_url)
                    continue
                except (json.JSONDecodeError, KeyError):
                    pass

        # 回退到页面
        base = self.site_cfg["base_url"]
        for endpoint in self.site_cfg.get("endpoints", []):
            url = urljoin(base, endpoint)
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue
            self._parse_index_page(soup, url)

    def _parse_api_data(self, data, source_url):
        """解析 API 返回的指数数据"""
        records = data if isinstance(data, list) else data.get("data", data.get("result", []))
        if isinstance(records, dict):
            records = records.get("list", records.get("items", []))
        if not isinstance(records, list):
            return

        for rec in records[-30:]:  # 最近 30 条
            date  = rec.get("date", rec.get("tradingDay", ""))
            value = rec.get("closeIndex", rec.get("value", rec.get("close", "")))
            if value:
                self.add_record(
                    metric="新华花椒价格指数",
                    value=value, unit="点",
                    period=str(date), region="甘肃武都",
                    source_url=source_url,
                    original_text=json.dumps(rec, ensure_ascii=False)[:300],
                    confidence="high"
                )

    def _parse_index_page(self, soup, source_url):
        """解析指数首页的最新数据"""
        # 通常页面上有当日指数值
        for el in soup.select(".index-value, .current-value, .num, .data-value"):
            text = el.get_text(strip=True)
            num = extract_number(text)
            if num and 100 < num < 3000:  # 合理范围
                self.add_record(
                    metric="新华花椒价格指数(最新)",
                    value=num, unit="点",
                    region="甘肃武都", source_url=source_url,
                    original_text=text, confidence="high"
                )
                break

        # 找页面中嵌入的 JSON 数据
        for script in soup.find_all("script"):
            if script.string and ("indexData" in script.string or "chartData" in script.string):
                # 提取 JSON
                json_match = re.search(r'\[[\s\S]*?\]', script.string)
                if json_match:
                    try:
                        arr = json.loads(json_match.group())
                        self._parse_api_data(arr, source_url)
                    except json.JSONDecodeError:
                        pass


class HuajiaoBigdataScraper(BaseScraper):
    """
    花椒大数据网 860938.cn — 各产区价格、面积、产量
    """

    def __init__(self, config=None):
        super().__init__("huajiao_bigdata", config)

    def crawl(self):
        base = self.site_cfg["base_url"]
        for endpoint in self.site_cfg.get("endpoints", []):
            url = urljoin(base, endpoint)
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue

            if "price" in endpoint or "yaotree" in endpoint:
                self._parse_price_page(soup, url)
            else:
                self._parse_news_page(soup, url)

    def _parse_price_page(self, soup, source_url):
        """解析价格/产区数据页面"""
        # 尝试表格
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            for row in rows[1:]:  # skip header
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    text = " ".join(c.get_text(strip=True) for c in cells)
                    price_match = re.search(r"(\d+\.?\d*)\s*元?[/／]?(斤|公斤|kg)?", text)
                    if price_match:
                        self.add_record(
                            metric="花椒产区价格",
                            value=float(price_match.group(1)),
                            unit=f"元/{price_match.group(2) or '斤'}",
                            source_url=source_url,
                            original_text=text, confidence="medium"
                        )

        # 尝试列表
        for item in soup.select(".price-item, .list-item, li"):
            text = item.get_text(" ", strip=True)
            if re.search(r"\d+\.?\d*\s*元", text) and ("花椒" in text or "藤椒" in text):
                nums = extract_all_numbers(text)
                if nums:
                    self.add_record(
                        metric="花椒报价",
                        value=nums[0], unit="元/斤",
                        source_url=source_url,
                        original_text=text, confidence="medium"
                    )

    def _parse_news_page(self, soup, source_url):
        """解析新闻/动态页，提取数据亮点"""
        articles = soup.select("a[href]")
        for a in articles[:20]:
            title = a.get_text(strip=True)
            if any(kw in title for kw in ["价格", "产量", "面积", "种植", "行情", "走势"]):
                href = urljoin(source_url, a.get("href", ""))
                self.add_record(
                    metric="行业动态",
                    value=None, unit="",
                    source_url=href,
                    original_text=title, confidence="low",
                    extra={"type": "article_link"}
                )


class HuajiaoCnScraper(BaseScraper):
    """
    中国花椒网 huajiao.cn — 花椒行情、产区动态
    """

    def __init__(self, config=None):
        super().__init__("huajiao_cn", config)

    def crawl(self):
        base = self.site_cfg["base_url"]
        for endpoint in self.site_cfg.get("endpoints", []):
            url = urljoin(base, endpoint)
            soup = self.fetch_and_parse(url)
            if soup is None:
                continue

            # 通用解析：找价格和文章
            for item in soup.select("li, .item, .article, tr"):
                text = item.get_text(" ", strip=True)
                if re.search(r"\d+\.?\d*\s*元", text):
                    nums = extract_all_numbers(text)
                    if nums:
                        self.add_record(
                            metric="花椒行情报价",
                            value=nums[0], unit="元/斤",
                            source_url=url,
                            original_text=text[:200], confidence="medium"
                        )

            # 文章链接
            for a in soup.select("a[href]")[:15]:
                title = a.get_text(strip=True)
                if len(title) > 10 and any(kw in title for kw in ["花椒", "藤椒", "价格", "产量"]):
                    href = urljoin(url, a.get("href", ""))
                    self.add_record(
                        metric="资讯链接",
                        value=None, unit="",
                        source_url=href,
                        original_text=title, confidence="low",
                        extra={"type": "article_link"}
                    )
