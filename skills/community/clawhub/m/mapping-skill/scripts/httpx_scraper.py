"""
异步 HTTP 爬虫模板

使用 httpx 进行高并发的异步网页爬取，适用于需要批量处理大量 URL 的场景。

依赖:
    pip install httpx

使用示例:
    import asyncio
    from httpx_scraper import batch_scrape

    async def main():
        urls = ["https://example1.edu/~phd1/", "https://example2.edu/~phd2/"]
        results = await batch_scrape(urls, max_concurrent=5)
        for r in results:
            if r["status"] == "success":
                print(f"Success: {r['url']}")

    asyncio.run(main())
"""

import asyncio
import httpx
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ScrapeResult:
    """爬取结果数据类"""
    url: str
    status: str  # success, error, skipped
    content: Optional[str] = None
    error: Optional[str] = None
    status_code: Optional[int] = None


# 默认请求头
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# 需要 BrightData 的域名
BRIGHTDATA_DOMAINS = ["linkedin.com", "twitter.com", "x.com", "facebook.com"]


async def async_scrape(
    url: str,
    client: httpx.AsyncClient,
    headers: Optional[Dict[str, str]] = None,
    max_content_length: int = 50000
) -> ScrapeResult:
    """
    异步爬取单个页面

    Args:
        url: 目标 URL
        client: httpx 异步客户端
        headers: 自定义请求头 (可选)
        max_content_length: 最大内容长度 (字符数)

    Returns:
        ScrapeResult 对象，包含状态和内容
    """
    # 检查是否需要 BrightData
    if any(domain in url.lower() for domain in BRIGHTDATA_DOMAINS):
        return ScrapeResult(
            url=url,
            status="skipped",
            error="This domain requires BrightData MCP service"
        )

    request_headers = {**DEFAULT_HEADERS, **(headers or {})}

    try:
        response = await client.get(url, headers=request_headers)

        if response.status_code == 200:
            return ScrapeResult(
                url=url,
                status="success",
                content=response.text[:max_content_length],
                status_code=200
            )
        else:
            return ScrapeResult(
                url=url,
                status="error",
                error=f"HTTP {response.status_code}",
                status_code=response.status_code
            )

    except httpx.TimeoutException:
        return ScrapeResult(url=url, status="error", error="Timeout")

    except httpx.TooManyRedirects:
        return ScrapeResult(url=url, status="error", error="Too many redirects")

    except httpx.HTTPStatusError as e:
        return ScrapeResult(
            url=url,
            status="error",
            error=f"HTTP {e.response.status_code}",
            status_code=e.response.status_code
        )

    except Exception as e:
        return ScrapeResult(url=url, status="error", error=str(e))


async def batch_scrape(
    urls: List[str],
    max_concurrent: int = 5,
    timeout: float = 30.0,
    verbose: bool = True
) -> List[ScrapeResult]:
    """
    并发爬取多个 URL

    Args:
        urls: URL 列表
        max_concurrent: 最大并发数 (默认 5)
        timeout: 请求超时时间 (秒)
        verbose: 是否打印进度信息

    Returns:
        ScrapeResult 列表，顺序与输入 URLs 一致
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []

    async def scrape_with_semaphore(url: str, client: httpx.AsyncClient, index: int):
        async with semaphore:
            if verbose:
                print(f"[{index}] Scraping: {url[:60]}...")

            result = await async_scrape(url, client)

            if verbose:
                status_icon = "✓" if result.status == "success" else "✗"
                print(f"    -> {status_icon} {result.status}")

            return result

    # 配置客户端
    limits = httpx.Limits(max_connections=max_concurrent)

    async with httpx.AsyncClient(
        timeout=timeout,
        follow_redirects=True,
        limits=limits
    ) as client:
        tasks = [
            scrape_with_semaphore(url, client, i + 1)
            for i, url in enumerate(urls)
        ]
        results = await asyncio.gather(*tasks)

    # 统计
    if verbose:
        success_count = sum(1 for r in results if r.status == "success")
        error_count = sum(1 for r in results if r.status == "error")
        skipped_count = sum(1 for r in results if r.status == "skipped")

        print(f"\nSummary: {success_count} success, {error_count} error, {skipped_count} skipped")

    return results


async def smart_batch_scrape(
    urls: List[str],
    max_concurrent: int = 5,
    retry_failed: bool = True
) -> List[ScrapeResult]:
    """
    智能批量爬取，支持失败重试

    Args:
        urls: URL 列表
        max_concurrent: 最大并发数
        retry_failed: 是否重试失败的请求

    Returns:
        ScrapeResult 列表
    """
    # 第一轮爬取
    results = await batch_scrape(urls, max_concurrent, verbose=True)

    if not retry_failed:
        return results

    # 收集失败的 URL
    failed_indices = [
        i for i, r in enumerate(results)
        if r.status == "error" and "Timeout" in str(r.error)
    ]

    if not failed_indices:
        return results

    print(f"\nRetrying {len(failed_indices)} failed URLs...")

    # 重试失败的请求
    failed_urls = [urls[i] for i in failed_indices]
    retry_results = await batch_scrape(
        failed_urls,
        max_concurrent=max(1, max_concurrent // 2),
        verbose=True
    )

    # 合并结果
    for i, retry_result in zip(failed_indices, retry_results):
        results[i] = retry_result

    return results


class AsyncScraper:
    """
    异步爬虫类，支持更灵活的配置和状态管理
    """

    def __init__(
        self,
        max_concurrent: int = 5,
        timeout: float = 30.0,
        delay: float = 0.0,
        headers: Optional[Dict[str, str]] = None
    ):
        """
        初始化爬虫

        Args:
            max_concurrent: 最大并发数
            timeout: 请求超时时间
            delay: 请求之间的延迟 (秒)
            headers: 自定义请求头
        """
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.delay = delay
        self.headers = {**DEFAULT_HEADERS, **(headers or {})}
        self.results: List[ScrapeResult] = []

    async def scrape(self, urls: List[str]) -> List[ScrapeResult]:
        """
        爬取 URL 列表

        Args:
            urls: URL 列表

        Returns:
            ScrapeResult 列表
        """
        semaphore = asyncio.Semaphore(self.max_concurrent)
        self.results = []

        async def scrape_one(url: str, client: httpx.AsyncClient):
            async with semaphore:
                result = await async_scrape(url, client, self.headers)
                self.results.append(result)

                if self.delay > 0:
                    await asyncio.sleep(self.delay)

                return result

        limits = httpx.Limits(max_connections=self.max_concurrent)

        async with httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            limits=limits
        ) as client:
            tasks = [scrape_one(url, client) for url in urls]
            await asyncio.gather(*tasks)

        return self.results

    def get_successful(self) -> List[ScrapeResult]:
        """获取成功的结果"""
        return [r for r in self.results if r.status == "success"]

    def get_failed(self) -> List[ScrapeResult]:
        """获取失败的结果"""
        return [r for r in self.results if r.status == "error"]

    def get_stats(self) -> Dict[str, int]:
        """获取统计信息"""
        return {
            "total": len(self.results),
            "success": len(self.get_successful()),
            "error": len(self.get_failed()),
            "skipped": sum(1 for r in self.results if r.status == "skipped")
        }


# 使用示例
if __name__ == "__main__":
    async def main():
        # 示例 URL 列表
        urls = [
            "https://www.example.edu/~phd1/",
            "https://www.example.edu/~phd2/",
            "https://linkedin.com/in/example",  # 会被跳过
        ]

        # 方式 1: 使用函数
        results = await batch_scrape(urls, max_concurrent=3)

        print("\n--- Results ---")
        for r in results:
            print(f"{r.status}: {r.url}")
            if r.error:
                print(f"  Error: {r.error}")

        # 方式 2: 使用类
        scraper = AsyncScraper(max_concurrent=5, delay=0.5)
        await scraper.scrape(urls)
        print(f"\nStats: {scraper.get_stats()}")

    asyncio.run(main())
