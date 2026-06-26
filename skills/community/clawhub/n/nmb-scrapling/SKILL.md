---
name: nmb-scrapling
description: Web scraping framework with anti-bot bypass and adaptive parsing. Use when the user needs to: (1) Scrape data from websites, (2) Bypass Cloudflare/anti-bot protection, (3) Build large-scale crawlers, (4) Extract structured data from web pages, (5) Monitor website changes, (6) Collect data for AI training/RAG. Triggers on phrases like "scrape this website", "抓取这个网站", "爬取数据", "帮我抓一下", "extract data from", "monitor this site".
---

# Scrapling

自适应Web爬虫框架，能过反爬、能大规模爬取、网站改版不崩。

## Installation

```bash
# 基础安装（仅解析器）
pip install scrapling

# 完整安装（含fetchers和浏览器）
pip install "scrapling[all]"
scrapling install

# 或单独安装功能
pip install "scrapling[fetchers]"  # 抓取功能
pip install "scrapling[ai]"        # MCP服务
pip install "scrapling[shell]"     # 交互式shell
```

## Quick Start

### 基础抓取

```python
from scrapling.fetchers import Fetcher

page = Fetcher.get('https://quotes.toscrape.com/')
quotes = page.css('.quote .text::text').getall()
print(quotes)
```

### 过反爬（Cloudflare等）

```python
from scrapling.fetchers import StealthyFetcher

# 自动过Cloudflare Turnstile
page = StealthyFetcher.fetch(
    'https://目标网站',
    headless=True,
    solve_cloudflare=True
)
data = page.css('.content::text').getall()
```

### 动态页面（JS渲染）

```python
from scrapling.fetchers import DynamicFetcher

# 完整浏览器渲染
page = DynamicFetcher.fetch(
    'https://spa网站',
    headless=True,
    network_idle=True  # 等网络请求完成
)
```

## Fetcher Types

| Fetcher | 用途 | 特点 |
|---------|------|------|
| `Fetcher` | 普通HTTP请求 | 最快，适合静态页面 |
| `StealthyFetcher` | 隐身模式 | 过反爬，过Cloudflare |
| `DynamicFetcher` | 浏览器模式 | JS渲染，SPA页面 |

## Element Selection

```python
page = Fetcher.get('https://example.com')

# CSS选择器
items = page.css('.item')
title = page.css('h1::text').get()
titles = page.css('h2::text').getall()

# XPath
items = page.xpath('//div[@class="item"]')

# BeautifulSoup风格
items = page.find_all('div', class_='item')
items = page.find_by_text('关键词', tag='div')

# 链式选择
quote_text = page.css('.quote')[0].css('.text::text').get()

# 导航
first = page.css('.item')[0]
parent = first.parent
sibling = first.next_sibling
similar = first.find_similar()  # 找相似元素
```

## Session Management

```python
from scrapling.fetchers import FetcherSession, StealthySession

# 保持会话（cookie复用）
with StealthySession(headless=True, solve_cloudflare=True) as session:
    page1 = session.fetch('https://example.com/login')
    page2 = session.fetch('https://example.com/dashboard')  # 已登录状态

# 异步Session
from scrapling.fetchers import AsyncStealthySession

async with AsyncStealthySession(headless=True) as session:
    page = await session.fetch('https://example.com')
```

## Building Spiders (大规模爬取)

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "products"
    start_urls = ["https://shop.example.com/"]
    concurrent_requests = 10  # 并发数

    async def parse(self, response: Response):
        for item in response.css('.product'):
            yield {
                "title": item.css('h2::text').get(),
                "price": item.css('.price::text').get(),
            }

        # 翻页
        next_page = response.css('.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page)

# 运行
result = MySpider().start()
print(f"爬取了 {len(result.items)} 条")

# 导出
result.items.to_json("output.json")
result.items.to_jsonl("output.jsonl")
```

### 断点续爬

```python
# 指定crawl目录，支持暂停/恢复
MySpider(crawldir="./crawl_data").start()

# Ctrl+C 暂停，再次运行从断点继续
```

### 多Session混用

```python
from scrapling.spiders import Spider, Request
from scrapling.fetchers import FetcherSession, AsyncStealthySession

class MultiSpider(Spider):
    name = "multi"

    def configure_sessions(self, manager):
        # 普通请求 - 快
        manager.add("fast", FetcherSession(impersonate="chrome"))
        # 隐身请求 - 过反爬
        manager.add("stealth", AsyncStealthySession(headless=True), lazy=True)

    async def parse(self, response):
        for link in response.css('a::attr(href)').getall():
            if "protected" in link:
                yield Request(link, sid="stealth")  # 用隐身session
            else:
                yield Request(link, sid="fast")      # 用快速session
```

## Adaptive Parsing (自适应解析)

网站改版后自动重新定位元素：

```python
# 首次爬取，保存元素特征
products = page.css('.product', auto_save=True)

# 网站改版后，用adaptive=True自动重新定位
products = page.css('.product', adaptive=True)
```

## Proxy Rotation

```python
from scrapling.fetchers import StealthyFetcher, ProxyRotator

proxies = ProxyRotator([
    "http://proxy1:8080",
    "http://proxy2:8080",
])

page = StealthyFetcher.fetch(
    'https://example.com',
    proxy=proxies.next()
)
```

## CLI Commands

```bash
# 交互式shell
scrapling shell

# 直接抓取（不用写代码）
scrapling extract get 'https://example.com' output.md
scrapling extract stealthy-fetch 'https://protected.com' output.html --solve-cloudflare

# 安装浏览器
scrapling install
scrapling install --force
```

## MCP Server (AI集成)

让Claude/Cursor直接调Scrapling爬数据：

```bash
pip install "scrapling[ai]"

# 启动MCP服务
scrapling mcp
```

配置到Claude Desktop的config：

```json
{
  "mcpServers": {
    "scrapling": {
      "command": "scrapling",
      "args": ["mcp"]
    }
  }
}
```

## Common Use Cases

### 电商比价

```python
from scrapling.fetchers import StealthyFetcher

page = StealthyFetcher.fetch('https://item.jd.com/12345.html', headless=True)
price = page.css('.price::text').get()
title = page.css('.sku-name::text').get()
```

### 招聘信息

```python
from scrapling.spiders import Spider, Response

class JobsSpider(Spider):
    name = "jobs"
    start_urls = ["https://www.zhipin.com/job_detail/?query=Python"]

    async def parse(self, response: Response):
        for job in response.css('.job-list li'):
            yield {
                "title": job.css('.job-name::text').get(),
                "salary": job.css('.salary::text').get(),
                "company": job.css('.company-name::text').get(),
            }
```

### 竞品监控

```python
from scrapling.fetchers import Fetcher
import json

def check_competitor(url):
    page = Fetcher.get(url)
    return {
        "products": len(page.css('.product')),
        "price_range": page.css('.price::text').getall(),
        "updated": page.css('.update-time::text').get(),
    }
```

## Tips

1. **先测试后规模化**：用`scrapling shell`调试选择器
2. **合理设置并发**：`concurrent_requests`别太高，容易被封
3. **用Session复用**：登录态、cookie保持用Session
4. **断点续爬**：长时间爬取务必设置`crawldir`
5. **尊重robots.txt**：合规爬取

## References

- 官方文档：https://scrapling.readthedocs.io
- GitHub：https://github.com/D4Vinci/Scrapling
