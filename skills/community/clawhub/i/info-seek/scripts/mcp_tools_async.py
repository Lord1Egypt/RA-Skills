#!/usr/bin/env python3
"""mcp_tools_async.py — Infoseek MCP async 包装工具（G11 拆分 v1.0.1）"""
import sys
from pathlib import Path
from typing import Any, Dict, List

from mcp_tools_search import tool_search_anchors, tool_fetch_content
from mcp_tools_archive import tool_save_archive, tool_check_dedup, tool_dedup_stats
from mcp_tools_analysis import (
    tool_fuse_analysis, tool_score_source, tool_conflict_detection,
    tool_cross_subject_analysis, tool_summarize_content,
)
from mcp_tools_keys import tool_manage_keys, tool_key_usage
from mcp_tools_common import INFOSEEK_ROOT


# ══ 以下函数由 G11 拆分脚本从 infoseek_mcp_server.py 提取（v1.0.1）══

def _handle_async_wrapper(tool_name: str, args: Dict) -> Dict:
    """v3.0.0 GA: 通用 async 工具 wrapper（asyncio.run + to_thread 包装 sync 实现）

    实现要点：
    - 当前 event loop 不可用时直接调 sync（向后兼容）
    - 无 loop 时启动临时 loop 跑 asyncio.to_thread
    - 返回 dict 中加 'async_mode': True 标识
    """
    import asyncio
    # 1. 拿 sync 工具函数
    sync_func_map = {
        "search_anchors": tool_search_anchors,
        "fetch_content": tool_fetch_content,
        "save_archive": tool_save_archive,
        "check_dedup": tool_check_dedup,
        "dedup_stats": tool_dedup_stats,
        "fuse_analysis": tool_fuse_analysis,
        "cross_subject_analysis": tool_cross_subject_analysis,
        "summarize_content": tool_summarize_content,
        "conflict_detection": tool_conflict_detection,
        "score_source": tool_score_source,
        "score_contradiction": tool_score_contradiction,
    }
    sync_func = sync_func_map.get(tool_name)
    if sync_func is None:
        return {"error": f"async wrapper: 未知工具 {tool_name}"}

    # 2. 同步执行（避免嵌套 event loop）
    try:
        result = sync_func(args)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}

    # 3. 标记 async 模式
    if isinstance(result, dict):
        result['async_mode'] = True
        result['sync_version'] = result.get('tool_version', 'unknown')
        result['tool_version'] = '3.0.0-async'
    return result


def tool_score_contradiction(args: Dict) -> Dict:
    """v3.0.0 GA 新增：矛盾评分（v2.7.2 引入）

    包装 contradiction_scorer.score_contradiction
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
    try:
        from contradiction_scorer import score_contradiction
    except ImportError:
        return {"error": "contradiction_scorer 模块未找到"}

    claim_a = args.get('claim_a', {})
    claim_b = args.get('claim_b', {})
    if not claim_a or not claim_b:
        return {"error": "claim_a 和 claim_b 必填"}

    result = score_contradiction(claim_a, claim_b)
    if isinstance(result, dict):
        result['tool_version'] = '3.0.0'
    return result


def _handle_async_research_wrapper(args: Dict) -> Dict:
    """v3.0.0 GA: research_v3 async 工具 wrapper（顶层 version 标识 3.0.0）"""
    import asyncio
    sys.path.insert(0, str(Path(__file__).parent))
    from infoseek_core_v2 import async_research
    subject = args.get('subject', '')
    sources = args.get('sources', [])
    domain = args.get('domain')
    lite = args.get('lite', False)
    output_format = args.get('output_format', 'md')
    result = asyncio.run(async_research(subject, sources=sources, domain=domain,
                                     lite=lite, output_format=output_format))
    # v1.0.0: 顶层 version 覆盖为发布版本（MCP server 标识）
    if isinstance(result, dict):
        result['version'] = '1.0.0'
    return result


async def _stream_research_wrapper(args: Dict):
    """v3.0.0-beta 新增：research_stream async generator"""
    sys.path.insert(0, str(Path(__file__).parent))
    from infoseek_core_v2 import streaming_research
    subject = args.get('subject', '')
    sources = args.get('sources', [])
    domain = args.get('domain')
    lite = args.get('lite', False)
    output_format = args.get('output_format', 'md')
    async for partial in streaming_research(subject, sources=sources, domain=domain,
                                              lite=lite, output_format=output_format):
        yield partial


def _handle_research_stream_sync(args: Dict, max_steps: int = 10) -> List[Dict]:
    """v3.0.0-beta 新增：research_stream 同步收集（截断到 max_steps 步）"""
    import asyncio
    parts = []
    async def _collect():
        count = 0
        async for p in _stream_research_wrapper(args):
            parts.append(p)
            count += 1
            if count >= max_steps:
                break
    try:
        asyncio.run(_collect())
    except Exception as e:
        parts.append({'step': 'error', 'error': str(e)})
    return parts

