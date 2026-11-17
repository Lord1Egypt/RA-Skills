#!/usr/bin/env python3
"""
case_search.py — 类案实时检索器

整合多数据源的类案检索：
1. IMA 知识库 API（快速，有日限额）
2. 裁判文书网 CDP 自动化（需 Chrome 登录态）
3. 本地 shape_spirit 数据（离线 fallback）

用法：
    from case_search import search_similar_cases
    results = search_similar_cases("民间借贷纠纷", ["借贷合意", "利息"])
"""

import json
import sys
import os
import time
import urllib.request
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

# ─── 路径 ───────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).parent
SKILL_DIR = SCRIPTS_DIR.parent
REFS_DIR = SKILL_DIR / "refs"

sys.path.insert(0, str(SCRIPTS_DIR))
from error_utils import retry_with_backoff, log_error, log_warning, log_info

# ─── IMA API 配置（从统一配置模块导入）──────────────
from config import IMA_API_KEY
IMA_API_URL = "https://api.ima-ai.com/v1/search"


@dataclass
class CaseResult:
    """类案检索结果"""
    case_number: str            # 案号
    court: str                  # 法院
    cause: str                  # 案由
    date: str                   # 裁判日期
    summary: str                # 裁判要旨（前 500 字）
    source: str                 # 数据源（ima/wenshu/local）
    relevance_score: float      # 相关性评分（0-1）
    url: str = ""               # 原文链接


@dataclass
class SearchResult:
    """检索结果汇总"""
    query_cause: str            # 查询案由
    query_keywords: list        # 查询关键词
    total_results: int          # 总结果数
    results: list               # CaseResult 列表
    sources_used: list          # 使用的数据源
    search_time_ms: int         # 搜索耗时


def _search_ima(cause: str, keywords: list[str], limit: int = 5) -> list[CaseResult]:
    """通过 IMA API 检索类案"""
    if not IMA_API_KEY:
        log_warning("case_search", "IMA API Key 未配置")
        return []
    
    query = f"{cause} {' '.join(keywords[:3])}"
    
    body = json.dumps({
        "query": query,
        "limit": limit,
        "filters": {
            "case_type": cause,
        },
    }).encode("utf-8")
    
    req = urllib.request.Request(
        IMA_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {IMA_API_KEY}",
        },
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = []
            for item in data.get("results", []):
                results.append(CaseResult(
                    case_number=item.get("case_number", ""),
                    court=item.get("court", ""),
                    cause=item.get("cause", cause),
                    date=item.get("date", ""),
                    summary=item.get("summary", "")[:500],
                    source="ima",
                    relevance_score=item.get("score", 0.5),
                    url=item.get("url", ""),
                ))
            return results
    except Exception as e:
        log_warning("case_search", f"IMA API 调用失败: {e}")
        return []


def _search_local(cause: str, keywords: list[str], limit: int = 5) -> list[CaseResult]:
    """从本地 shape_spirit 数据检索"""
    from shape_spirit_index import ShapeSpiritIndex
    
    index = ShapeSpiritIndex()
    results = []
    
    # 按案由搜索
    cases = index.search_by_cause(cause)
    for lc in cases[:limit]:
        try:
            case_num = int(lc["num"])
        except (ValueError, TypeError):
            case_num = lc["num"]
        case_data = index.get_case_summary(lc["volume"], case_num)
        if case_data:
            results.append(CaseResult(
                case_number=case_data.get("title", "")[:20],
                court="",
                cause=cause,
                date="",
                summary=case_data.get("brief_facts", "")[:500],
                source="local",
                relevance_score=0.6,
            ))
    
    # 补充：按关键词搜索
    if len(results) < limit:
        for kw in keywords[:2]:
            kw_cases = index.search_by_keyword(kw)
            for kc in kw_cases[:2]:
                case_data = index.get_case_summary(kc["volume"], int(kc["num"]))
                if case_data:
                    results.append(CaseResult(
                        case_number=case_data.get("title", "")[:20],
                        court="",
                        cause=cause,
                        date="",
                        summary=case_data.get("brief_facts", "")[:500],
                        source="local",
                        relevance_score=0.5,
                    ))
    
    return results[:limit]


def search_similar_cases(
    cause: str,
    keywords: list[str] = None,
    limit: int = 5,
    sources: list[str] = None,
) -> SearchResult:
    """
    多数据源类案检索。
    
    Args:
        cause: 案由
        keywords: 关键词列表
        limit: 最大返回数
        sources: 数据源列表（默认 ["ima", "local"]）
    
    Returns:
        SearchResult 包含类案列表和元数据
    """
    if keywords is None:
        keywords = []
    if sources is None:
        sources = ["ima", "local"]
    
    start_time = time.time()
    all_results = []
    sources_used = []
    
    # 1. IMA API 检索（快速）
    if "ima" in sources:
        ima_results = _search_ima(cause, keywords, limit)
        if ima_results:
            all_results.extend(ima_results)
            sources_used.append("ima")
    
    # 2. 本地数据检索（fallback）
    if "local" in sources and len(all_results) < limit:
        local_results = _search_local(cause, keywords, limit - len(all_results))
        if local_results:
            all_results.extend(local_results)
            sources_used.append("local")
    
    # 去重（按案号）
    seen = set()
    unique_results = []
    for r in all_results:
        key = r.case_number or r.summary[:50]
        if key not in seen:
            seen.add(key)
            unique_results.append(r)
    
    # 按相关性排序
    unique_results.sort(key=lambda r: r.relevance_score, reverse=True)
    
    elapsed_ms = int((time.time() - start_time) * 1000)
    
    return SearchResult(
        query_cause=cause,
        query_keywords=keywords,
        total_results=len(unique_results),
        results=unique_results[:limit],
        sources_used=sources_used,
        search_time_ms=elapsed_ms,
    )


def format_search_results(result: SearchResult) -> str:
    """格式化检索结果为可读文本"""
    lines = []
    lines.append(f"## 类案检索结果（案由：{result.query_cause}）")
    lines.append(f"检索耗时：{result.search_time_ms}ms | 数据源：{', '.join(result.sources_used)} | 结果数：{result.total_results}")
    lines.append("")
    
    for i, r in enumerate(result.results, 1):
        lines.append(f"### 类案 {i}")
        if r.case_number:
            lines.append(f"**案号**：{r.case_number}")
        if r.court:
            lines.append(f"**法院**：{r.court}")
        if r.date:
            lines.append(f"**裁判日期**：{r.date}")
        if r.summary:
            lines.append(f"**裁判要旨**：{r.summary}")
        lines.append(f"**来源**：{r.source} | **相关度**：{r.relevance_score}")
        lines.append("")
    
    return "\n".join(lines)


# ─── CLI 入口 ─────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 case_search.py <案由> [关键词1 关键词2 ...]")
        print("示例: python3 case_search.py 民间借贷纠纷 借贷合意 利息")
        sys.exit(1)
    
    cause = sys.argv[1]
    keywords = sys.argv[2:] if len(sys.argv) > 2 else []
    
    result = search_similar_cases(cause, keywords)
    print(format_search_results(result))
