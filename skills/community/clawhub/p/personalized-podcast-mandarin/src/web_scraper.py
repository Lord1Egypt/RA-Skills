"""
Web Scraper Module
使用 requests + BeautifulSoup4 抓取网页内容
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional


class WebScraperError(Exception):
    """网页抓取异常"""
    pass


class WebScraper:
    """网页抓取器"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, url: str) -> str:
        """
        抓取 URL 并提取正文内容

        Args:
            url: 目标网页 URL

        Returns:
            提取的正文文本

        Raises:
            requests.RequestException: 网络请求失败
            ValueError: 无法提取有效内容
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or 'utf-8'
        except requests.RequestException as e:
            raise WebScraperError(f"Failed to fetch {url}: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')

        # 移除不需要的标签
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'advertisement']):
            tag.decompose()

        # 尝试提取文章主体
        content = self._extract_article_content(soup)

        if not content or len(content.strip()) < 100:
            # 如果提取失败，尝试提取所有段落
            content = self._extract_paragraphs(soup)

        if not content or len(content.strip()) < 100:
            raise WebScraperError(f"Could not extract meaningful content from {url}")

        return content.strip()

    def _extract_article_content(self, soup: BeautifulSoup) -> str:
        """
        尝试从常见的文章容器中提取内容
        """
        # 常见的文章容器选择器
        selectors = [
            'article',
            '[role="main"]',
            '.post-content',
            '.article-content',
            '.entry-content',
            '.content',
            '#content',
            'main',
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(separator='\n', strip=True)

        return ""

    def _extract_paragraphs(self, soup: BeautifulSoup) -> str:
        """
        提取所有段落文本
        """
        paragraphs = soup.find_all('p')
        texts = []

        for p in paragraphs:
            text = p.get_text(strip=True)
            # 过滤太短的段落
            if len(text) > 20:
                texts.append(text)

        return '\n\n'.join(texts)


def fetch_url_content(url: str) -> str:
    """
    便捷函数：抓取 URL 内容

    Args:
        url: 目标 URL

    Returns:
        提取的文本内容
    """
    scraper = WebScraper()
    return scraper.fetch(url)
