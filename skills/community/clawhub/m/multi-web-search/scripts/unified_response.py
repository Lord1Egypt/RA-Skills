#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unified_response.py - 统一响应格式

所有搜索脚本使用统一的响应格式，便于解析和处理。

Usage:
    from unified_response import UnifiedResponse, success_response, error_response

    resp = success_response("ddgs", "test query", [...results...])
    print(resp.to_json())
"""
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class UnifiedResponse:
    """
    统一搜索响应格式。

    所有搜索脚本（search.py, multi_engine_search.py, arxiv_search.py 等）
    都应返回此格式，确保输出一致性。

    格式：
    {
        "provider": str,          # 提供者：ddgs, arxiv, duckduckgo-lite, etc.
        "success": bool,          # 是否成功
        "query": str,             # 原始查询
        "results": [              # 结果列表
            {
                "title": str,
                "url": str,
                "snippet": str,
                "published_date": str | None,  # ISO 格式或 YYYY-MM-DD
                "source": str,                  # 来源引擎
                "extra": {}                     # 额外信息（如 authors, pdf_url）
            }
        ],
        "metadata": {
            "count": int,         # 结果数量
            "engine": str,        # 使用的引擎
            "cached": bool,       # 是否来自缓存
            "cache_age": int | None,  # 缓存年龄（秒）
            "time_filter": str | None,
            "domain_filter": str | None,
        },
        "error": str | None       # 错误信息（如有）
    }
    """

    def __init__(
        self,
        provider: str = "",
        success: bool = True,
        query: str = "",
        results: Optional[List[Dict]] = None,
        metadata: Optional[Dict] = None,
        error: Optional[str] = None
    ):
        self.provider = provider
        self.success = success
        self.query = query
        self.results = results or []
        self.metadata = metadata or {
            "count": 0,
            "engine": "",
            "cached": False,
            "cache_age": None,
            "time_filter": None,
            "domain_filter": None,
        }
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "provider": self.provider,
            "success": self.success,
            "query": self.query,
            "results": self.results,
            "metadata": {
                **self.metadata,
                "count": len(self.results),
            },
            "error": self.error,
            "timestamp": self.timestamp,
        }

    def to_json(self, **kwargs) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, **kwargs)

    @classmethod
    def from_dict(cls, data: Dict) -> "UnifiedResponse":
        """从字典创建"""
        resp = cls(
            provider=data.get("provider", ""),
            success=data.get("success", True),
            query=data.get("query", ""),
            results=data.get("results", []),
            metadata=data.get("metadata", {}),
            error=data.get("error")
        )
        resp.timestamp = data.get("timestamp", datetime.now().isoformat())
        return resp

    def add_result(
        self,
        title: str,
        url: str,
        snippet: str = "",
        published_date: Optional[str] = None,
        source: str = "",
        **extra
    ):
        """添加一个结果"""
        result = {
            "title": title,
            "url": url,
            "snippet": snippet,
            "published_date": published_date,
            "source": source,
        }
        if extra:
            result["extra"] = extra
        self.results.append(result)
        self.metadata["count"] = len(self.results)

    def merge(self, other: "UnifiedResponse") -> "UnifiedResponse":
        """合并另一个响应（结果去重）"""
        seen_urls = {r["url"] for r in self.results if r.get("url")}
        merged_results = self.results.copy()

        for r in other.results:
            url = r.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                merged_results.append(r)

        return UnifiedResponse(
            provider=f"{self.provider}+{other.provider}",
            success=self.success or other.success,
            query=self.query,
            results=merged_results,
            metadata={
                **self.metadata,
                "count": len(merged_results),
                "merged_providers": [self.provider, other.provider],
            },
            error=self.error or other.error
        )


def success_response(
    provider: str,
    query: str,
    results: List[Dict],
    engine: str = "",
    cached: bool = False,
    cache_age: Optional[int] = None,
    **metadata
) -> UnifiedResponse:
    """创建成功响应"""
    return UnifiedResponse(
        provider=provider,
        success=True,
        query=query,
        results=results,
        metadata={
            "engine": engine,
            "cached": cached,
            "cache_age": cache_age,
            **metadata
        }
    )


def error_response(
    provider: str,
    query: str,
    error: str,
    **metadata
) -> UnifiedResponse:
    """创建错误响应"""
    return UnifiedResponse(
        provider=provider,
        success=False,
        query=query,
        results=[],
        metadata={**metadata},
        error=error
    )


def adapt_arxiv_response(arxiv_data: Dict) -> UnifiedResponse:
    """将 arXiv 响应格式转换为统一格式"""
    results = []
    for r in arxiv_data.get("results", []):
        result = {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", ""),
            "published_date": r.get("published_date"),
            "source": "arxiv",
            "extra": {
                "pdf_url": r.get("pdf_url"),
                "authors": r.get("authors", []),
                "author_count": r.get("author_count", 0),
                "categories": r.get("categories", []),
                "arxiv_id": r.get("arxiv_id", ""),
            }
        }
        results.append(result)

    return success_response(
        provider="arxiv",
        query=arxiv_data.get("query", ""),
        results=results,
        engine="arxiv",
        sort_by=arxiv_data.get("sort_by"),
        sort_order=arxiv_data.get("sort_order")
    )


def adapt_ddgs_response(ddgs_data: Dict, provider: str = "ddgs") -> UnifiedResponse:
    """将 ddgs 响应格式转换为统一格式"""
    results = []
    for r in ddgs_data.get("results", []):
        result = {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", ""),
            "published_date": r.get("published_date"),
            "source": ddgs_data.get("backend", provider),
        }
        results.append(result)

    return success_response(
        provider=provider,
        query=ddgs_data.get("query", ""),
        results=results,
        engine=ddgs_data.get("backend", provider),
        backend=ddgs_data.get("backend")
    )


if __name__ == "__main__":
    # 测试
    print("=== 统一响应格式测试 ===\n")

    # 创建成功响应
    resp = success_response(
        provider="ddgs",
        query="python tutorial",
        results=[
            {"title": "Python Tutorial", "url": "https://example.com/python", "snippet": "Learn Python"},
            {"title": "Python Guide", "url": "https://example.com/guide", "snippet": "Python guide"},
        ],
        engine="google",
        cached=False
    )

    print("成功响应:")
    print(json.dumps(resp.to_dict(), indent=2, ensure_ascii=False))

    print("\n错误响应:")
    err = error_response("ddgs", "test", "Connection timeout")
    print(err.to_json(indent=2))

    print("\n添加结果:")
    resp.add_result("New Result", "https://new.com", "New snippet", source="bing")
    print(f"结果数量: {resp.metadata['count']}")

    print("\n合并响应:")
    resp2 = success_response("arxiv", "python", [{"title": "ArXiv Paper", "url": "https://arxiv.org/..."}])
    merged = resp.merge(resp2)
    print(f"合并后结果数量: {merged.metadata['count']}")