#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
垂直搜索路由（V1.8 新增）

功能：news / realtime / academic / image 四类垂直搜索，各配引擎优先级与参数。
目标：不同信息时效性需求用不同引擎组合和排序策略。

遵循死规则 9：学术搜索 Semanticscholar API 不可用时降级到通用引擎+学术关键词。
遵循死规则 10：控制并发，不影响用户设备。
遵循死规则 13：不生成 __pycache__。
"""

import asyncio
import sys
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True

# 垂直搜索配置
VERTICAL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "news": {
        "display_name": "新闻",
        "description": "时效性新闻，优先最近24小时",
        "engines": ["baidu_news", "bing_news", "baidu", "bing"],
        "ranking_overrides": {
            "freshness": 2.5,
            "relevance": 1.5,
            "position": 1.0,
            "authority": 0.5,
            "consensus": 0.5,
        },
        "time_filter": "day",
        "fallback_message": "新闻搜索暂不可用，已降级为普通搜索+时效性排序",
    },
    "realtime": {
        "display_name": "实时",
        "description": "最新实时信息，优先秒级/分钟级更新",
        "engines": ["searxng", "bing", "baidu"],
        "ranking_overrides": {
            "freshness": 3.0,
            "relevance": 1.0,
            "position": 0.8,
            "authority": 0.3,
            "consensus": 0.3,
        },
        "time_filter": "hour",
        "fallback_message": "实时搜索暂不可用，已降级为普通搜索",
    },
    "academic": {
        "display_name": "学术",
        "description": "学术论文与研究成果，优先引用量和相关性",
        "engines": ["semanticscholar", "bing", "baidu"],
        "ranking_overrides": {
            "citations": 2.0,
            "relevance": 1.5,
            "authority": 1.0,
            "position": 0.5,
            "consensus": 0.5,
        },
        "time_filter": None,
        "fallback_message": "学术数据库暂不可用，已降级为通用引擎+学术关键词搜索",
    },
    "image": {
        "display_name": "图片",
        "description": "图片搜索，返回缩略图URL与来源",
        "engines": ["baidu_img", "bing_img", "baidu", "bing"],
        "ranking_overrides": {
            "relevance": 2.0,
            "authority": 1.0,
            "position": 0.8,
            "consensus": 0.5,
        },
        "time_filter": None,
        "fallback_message": "图片搜索暂不可用，已降级为普通搜索+图片关键词",
    },
}

# 学术关键词后缀（降级时使用）
ACADEMIC_SUFFIXES = ["论文", "研究", "学术", "期刊", "会议", "review", "survey"]


def get_vertical_config(vertical_type: str) -> Optional[Dict[str, Any]]:
    """获取垂直搜索配置"""
    return VERTICAL_CONFIGS.get(vertical_type)


def list_vertical_types() -> List[str]:
    """列出所有可用的垂直搜索类型"""
    return list(VERTICAL_CONFIGS.keys())


def apply_vertical_ranking(
    results: List[Any],
    vertical_type: str,
    query: str = "",
) -> List[Any]:
    """
    应用垂直搜索排序覆盖

    根据垂直类型调整排序权重，重新排序结果。
    """
    if not results:
        return results

    config = VERTICAL_CONFIGS.get(vertical_type)
    if not config:
        return results

    overrides = config.get("ranking_overrides", {})
    if not overrides:
        return results

    try:
        from ranking import rank_results, RankWeights
    except ImportError:
        from .ranking import rank_results, RankWeights

    # 构建覆盖权重
    base_weights = RankWeights()
    for key, value in overrides.items():
        if hasattr(base_weights, key):
            setattr(base_weights, key, value)

    # 对于学术搜索，如果有引用数据，按引用数排序
    if vertical_type == "academic":
        # 检查是否有 citation_count 属性
        has_citations = any(
            hasattr(r, "citation_count") and getattr(r, "citation_count", 0) > 0
            for r in results
        )
        if has_citations:
            # 按引用数降序
            results.sort(
                key=lambda r: (
                    -getattr(r, "citation_count", 0),
                    -r.score if hasattr(r, "score") else 0,
                )
            )
            return results

    # 通用排序
    try:
        results = rank_results(
            results,
            query=query,
            weights=base_weights,
        )
    except Exception:
        pass  # 排序失败不中断

    return results


def add_academic_suffix(query: str) -> str:
    """
    降级时给查询添加学术关键词后缀
    """
    if not query:
        return query

    # 如果已经有学术相关词，不再添加
    lower = query.lower()
    for suffix in ACADEMIC_SUFFIXES:
        if suffix in lower:
            return query

    return f"{query} {ACADEMIC_SUFFIXES[0]}"


def build_vertical_fallback_engines(vertical_type: str) -> List[str]:
    """
    构建降级引擎列表

    当垂直专用引擎不可用时，回退到通用引擎。
    """
    config = VERTICAL_CONFIGS.get(vertical_type)
    if not config:
        return ["baidu", "bing", "duckduckgo"]

    # 取配置的引擎列表中的通用引擎（排在后面的）
    engines = config.get("engines", [])
    # 返回最后两个（通常是通用引擎）
    fallback = [e for e in engines if not _is_vertical_engine(e)]
    return fallback if fallback else ["baidu", "bing", "duckduckgo"]


def _is_vertical_engine(engine_name: str) -> bool:
    """判断是否为垂直专用引擎"""
    vertical_engines = {
        "baidu_news", "bing_news", "semanticscholar",
        "baidu_img", "bing_img", "searxng",
    }
    return engine_name in vertical_engines


def format_vertical_results(
    results: List[Any],
    vertical_type: str,
    query: str = "",
) -> str:
    """
    格式化垂直搜索结果

    根据垂直类型添加特定的展示信息。
    """
    if not results:
        return "没有找到相关结果。"

    config = VERTICAL_CONFIGS.get(vertical_type, {})
    display_name = config.get("display_name", "搜索")

    lines = [
        f"\n{display_name}搜索: {query} | 结果: {len(results)} 条\n"
    ]

    for idx, r in enumerate(results, 1):
        title = getattr(r, "title", "") or "无标题"
        url = getattr(r, "url", "") or ""
        snippet = getattr(r, "snippet", "") or ""

        lines.append(f"[{idx}] {title}")
        if url:
            lines.append(f"    {url}")
        if snippet:
            lines.append(f"    {snippet[:120]}")

        # 学术搜索：显示引用数和年份
        if vertical_type == "academic":
            citations = getattr(r, "citation_count", 0)
            year = getattr(r, "year", None)
            if citations > 0 or year:
                meta_parts = []
                if year:
                    meta_parts.append(f"年份: {year}")
                if citations > 0:
                    meta_parts.append(f"引用: {citations}")
                if meta_parts:
                    lines.append(f"    — {' | '.join(meta_parts)}")

        # 图片搜索：显示缩略图URL
        if vertical_type == "image":
            thumbnail = getattr(r, "thumbnail_url", "") or ""
            if thumbnail:
                lines.append(f"    缩略图: {thumbnail}")

        # 新闻搜索：显示发布时间
        if vertical_type == "news":
            pub_date = getattr(r, "publish_date", "") or ""
            if pub_date:
                lines.append(f"    发布时间: {pub_date}")

        # 多引擎收录标注
        sources = getattr(r, "engine_set", []) or ([r.engine] if getattr(r, "engine", "") else [])
        if len(sources) > 1:
            lines.append(f"    — {', '.join(sources)}（{len(sources)} 个引擎收录）")

        lines.append("")

    return "\n".join(lines)


async def execute_vertical_search(
    query: str,
    vertical_type: str,
    config: Dict[str, Any],
    num: int = 10,
    privacy_mode: str = "normal",
) -> List[Any]:
    """
    执行垂直搜索（异步入口）

    根据垂直类型选择引擎和排序策略，调用 SearchOrchestrator。
    """
    vertical_cfg = VERTICAL_CONFIGS.get(vertical_type)
    if not vertical_cfg:
        return []

    try:
        from search import SearchOrchestrator
    except ImportError:
        from .search import SearchOrchestrator

    orchestrator = SearchOrchestrator(config)

    # 解析引擎列表
    engines = vertical_cfg.get("engines", [])
    available = orchestrator.engine_manager.available_engines()

    # 过滤出可用的引擎
    usable = [e for e in engines if e in available]

    # 如果专用引擎不可用，降级
    if not usable:
        usable = build_vertical_fallback_engines(vertical_type)
        if vertical_type == "academic":
            query = add_academic_suffix(query)
        # 添加降级提示
        fallback_msg = vertical_cfg.get("fallback_message", "已降级为通用引擎")
        orchestrator._notices.append(fallback_msg)

    # 执行搜索
    results = await orchestrator.search(
        query=query,
        engines=usable,
        num=num,
        privacy_mode=privacy_mode,
        use_cache=True,
    )

    # 应用垂直排序
    results = apply_vertical_ranking(results, vertical_type, query)

    return results


def run_vertical_search(
    query: str,
    vertical_type: str,
    config: Optional[Dict[str, Any]] = None,
    num: int = 10,
    privacy_mode: str = "normal",
) -> List[Any]:
    """
    执行垂直搜索（同步入口，供CLI调用）
    """
    cfg = config or {}
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        execute_vertical_search(query, vertical_type, cfg, num, privacy_mode)
    )


if __name__ == "__main__":
    print("垂直搜索类型：")
    for vt in list_vertical_types():
        cfg = get_vertical_config(vt)
        print(f"  --vertical {vt:10} {cfg['display_name']:6} | {cfg['description']}")
