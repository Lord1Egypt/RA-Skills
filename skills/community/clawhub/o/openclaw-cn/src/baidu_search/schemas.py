from __future__ import annotations

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """搜索请求参数"""
    query: str = Field(min_length=1, description="搜索关键词")
    top_k: int = Field(default=10, ge=1, le=20, description="返回结果数量")
    recency_filter: str | None = Field(
        default=None,
        description="时间过滤: day, week, month, year"
    )
    site_filter: list[str] | None = Field(
        default=None,
        description="限定搜索的网站列表"
    )


class SearchResult(BaseModel):
    """单条搜索结果"""
    title: str | None = None
    url: str | None = None
    snippet: str | None = None
    site_name: str | None = None


class SearchResponse(BaseModel):
    """搜索响应"""
    results: list[SearchResult]
    total: int
