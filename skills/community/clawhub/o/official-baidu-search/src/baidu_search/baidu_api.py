from __future__ import annotations

import logging
import os
from typing import Any

import httpx
from fastapi import HTTPException

from baidu_search.schemas import SearchRequest, SearchResponse, SearchResult

BAIDU_API_URL = "https://qianfan.baidubce.com/v2/ai_search/web_search"
logger = logging.getLogger("baidu_search.api")


def _get_api_key() -> str:
    """获取百度 API Key"""
    api_key = os.getenv("BAIDU_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="BAIDU_API_KEY is not set.",
        )
    return api_key


def _build_request_body(request: SearchRequest) -> dict[str, Any]:
    """构建百度 API 请求体"""
    body: dict[str, Any] = {
        "messages": [
            {
                "content": request.query,
                "role": "user"
            }
        ],
        "search_source": "baidu_search_v2",
        "resource_type_filter": [
            {
                "type": "web",
                "top_k": request.top_k
            }
        ]
    }

    # 时间过滤
    if request.recency_filter:
        valid_filters = ["day", "week", "month", "year"]
        if request.recency_filter in valid_filters:
            body["search_recency_filter"] = request.recency_filter

    # 网站过滤
    if request.site_filter:
        body["search_filter"] = {
            "match": {
                "site": request.site_filter
            }
        }

    return body


def _parse_response(data: dict[str, Any]) -> SearchResponse:
    """解析百度 API 响应"""
    results: list[SearchResult] = []
    
    # 从响应中提取搜索结果
    # 百度 AI 搜索返回格式可能包含 search_results 或在 choices 中
    search_results = data.get("search_results", [])
    
    # 如果在 choices 中有结构化数据
    if not search_results and "choices" in data:
        for choice in data.get("choices", []):
            message = choice.get("message", {})
            # 尝试从 tool_calls 或其他字段提取
            if "search_results" in message:
                search_results = message["search_results"]
                break
    
    # 也可能直接在顶层
    if not search_results:
        search_results = data.get("web_search_results", [])
    
    for item in search_results:
        results.append(SearchResult(
            title=item.get("title"),
            url=item.get("url") or item.get("link"),
            snippet=item.get("snippet") or item.get("content") or item.get("abstract"),
            site_name=item.get("site_name") or item.get("source")
        ))

    return SearchResponse(
        results=results,
        total=len(results)
    )


def search(request: SearchRequest) -> SearchResponse:
    """执行百度搜索"""
    api_key = _get_api_key()
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    body = _build_request_body(request)
    
    logger.info("Searching Baidu: %s", request.query)
    
    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                BAIDU_API_URL,
                headers=headers,
                json=body
            )
    except httpx.HTTPError as exc:
        logger.error("Baidu API request failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail="Baidu API unavailable."
        ) from exc

    if response.status_code != 200:
        logger.error(
            "Baidu API error: status=%d, body=%s",
            response.status_code,
            response.text
        )
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Baidu API error: {response.text}"
        )

    data = response.json()
    return _parse_response(data)
