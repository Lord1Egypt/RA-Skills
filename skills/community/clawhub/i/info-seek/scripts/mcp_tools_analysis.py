#!/usr/bin/env python3
"""mcp_tools_analysis.py — Infoseek MCP 分析工具（G11 拆分 v1.0.1）"""
import os
import sys
from typing import Any, Dict

from mcp_tools_common import INFOSEEK_ROOT


# ══ 以下函数由 G11 拆分脚本从 infoseek_mcp_server.py 提取（v1.0.1）══

def tool_fuse_analysis(args: Dict) -> Dict:
    """融合分析（结构化分层根因表）+ v1.8.1 多平台导出"""
    sources = args['sources']
    min_score = args.get('min_score', 40)
    # v1.8.1 新增：导出格式参数
    export_formats = args.get('export_formats', [])  # 列表，可选 md/json/csv

    # 过滤低分源
    qualified = [s for s in sources if s.get('score', 0) >= min_score]

    # 按 score 分层
    layers = {'🥇': [], '🥈': [], '🥉': []}
    for s in qualified:
        score = s.get('score', 0)
        if score >= 70:
            layers['🥇'].append(s)
        elif score >= 55:
            layers['🥈'].append(s)
        else:
            layers['🥉'].append(s)

    subject = args.get('subject', 'Untitled')

    result = {
        "subject": subject,
        "total_sources": len(sources),
        "qualified_sources": len(qualified),
        "min_score_filter": min_score,
        "fused_layers": layers,
        "report_format": "| 层级 | 根因 | 来源 |",
        "version": "1.8.1",
    }

    # v1.8.1 多平台导出
    if export_formats:
        result['exports'] = _export_fuse_to_formats(subject, sources, layers, export_formats)

    return result


def _export_fuse_to_formats(subject: str, sources: list, layers: dict, formats: list) -> dict:
    """v1.8.1 多平台导出辅助函数

    调用 exporter.py 的 to_markdown / to_csv / to_json 生成对应格式。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from exporter import to_markdown, to_csv, to_json
    except ImportError:
        return {"error": "exporter 模块未找到"}

    # 构造报告 dict
    report = {
        'subject': subject,
        'domain': 'general',
        'summary': f'融合分析报告（{subject}），共 {sum(len(v) for v in layers.values())} 个有效源。',
        'anchors': [{
            'title': s.get('title', 'Untitled'),
            'url': s.get('url', ''),
            'platform': s.get('platform', ''),
            'score': s.get('score', 0),
            'credibility': s.get('credibility', 0),
            'snippet': s.get('snippet', s.get('text', ''))[:300],
            'layer': next((k for k, v in layers.items() if s in v), '🥉'),
        } for s in sources],
    }

    exports = {}
    for fmt in formats:
        try:
            if fmt == 'md':
                exports['md'] = to_markdown(report)
            elif fmt == 'csv':
                exports['csv'] = to_csv(report)
            elif fmt == 'json':
                exports['json'] = to_json(report)
            elif fmt == 'lobehub':
                from exporter import to_lobehub_skill
                exports['lobehub'] = to_lobehub_skill(report)
            elif fmt == 'claude':
                from exporter import to_claude_skill
                exports['claude'] = to_claude_skill(report)
            elif fmt == 'openai':
                from exporter import to_openai_plugin
                exports['openai'] = to_openai_plugin(report)
            else:
                exports[fmt] = f"❌ 未知格式: {fmt}"
        except Exception as e:
            exports[fmt] = f"❌ 导出失败: {type(e).__name__}: {str(e)[:60]}"

    return exports


def tool_score_source(args: Dict) -> Dict:
    """v2 评分（v2.0.1 新增第 10 工具）

    包装 infoseek_core_v2.score_source()。
    单个源 v2 评分：trust_bonus + Jaccard + domain_bonus。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
    try:
        from infoseek_core_v2 import score_source
    except ImportError:
        return {"error": "infoseek_core_v2 模块未找到"}

    source = args.get('source', {})
    subject = args.get('subject', '')
    with_domain = args.get('with_domain', True)

    if not source or not subject:
        return {"error": "source 和 subject 必填"}

    result = score_source(source, subject, with_domain=with_domain)
    result['tool_version'] = '2.0.1'
    return result


def tool_research(args: Dict) -> Dict:
    """v2 端到端调研（v2.0.1 新增第 11 工具）

    包装 infoseek_core_v2.research()。
    detect_domain → score → conflict → render → report 全流程。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    sys.path.insert(0, str(INFOSEEK_ROOT / 'core'))
    try:
        from infoseek_core_v2 import research
    except ImportError:
        return {"error": "infoseek_core_v2 模块未找到"}

    subject = args.get('subject', '')
    if not subject:
        return {"error": "subject 必填"}

    sources = args.get('sources', [])
    domain = args.get('domain')
    with_llm = args.get('with_llm', False)
    output_format = args.get('output_format', 'md')

    result = research(
        subject,
        sources=sources,
        domain=domain,
        with_llm=with_llm,
        output_format=output_format,
    )
    result['tool_version'] = '2.0.1'
    return result


def tool_conflict_detection(args: Dict) -> Dict:
    """跨源冲突检测（v1.8.1 新增第 9 工具）

    包装 conflict_detection.detect_conflicts()。
    内部检测同一事实（实体+数值）在不同源中的不同表述。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from conflict_detection import detect_conflicts
    except ImportError:
        return {"error": "conflict_detection 模块未找到"}

    sources = args.get('sources', [])
    subject = args.get('subject', '')
    min_sources = args.get('min_sources', 2)
    max_conflicts = args.get('max_conflicts', 20)

    if len(sources) < min_sources:
        return {
            "error": f"来源数 {len(sources)} < min_sources {min_sources}",
            "sources_count": len(sources),
            "required": min_sources,
        }

    result = detect_conflicts(sources, subject=subject)

    # 应用 max_conflicts 截断
    if 'conflicts' in result and len(result['conflicts']) > max_conflicts:
        result['conflicts'] = result['conflicts'][:max_conflicts]
        result['truncated'] = True

    # 加 metadata
    result['tool_version'] = '1.8.1'
    result['min_sources_used'] = min_sources
    result['max_conflicts_used'] = max_conflicts

    return result


def tool_cross_subject_analysis(args: Dict) -> Dict:
    """跨主题关联分析（v1.6.0 新增第 7 工具）"""
    # v3.0.0 GA 兼容性修复: 同时支持 subjects[] 和 (subject_a, subject_b) 两种入参
    subjects = args.get('subjects', [])
    if not subjects:
        a = args.get('subject_a', '').strip()
        b = args.get('subject_b', '').strip()
        if a and b:
            subjects = [a, b]
    min_correlation = args.get('min_correlation', 1)

    if len(subjects) < 2:
        return {"error": f"至少需要 2 个主题（当前 subjects={subjects}，请传 subjects=[..] 或 subject_a + subject_b）"}

    # 动态导入 anchor_adapter（避免循环依赖）
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from anchor_adapter import cross_subject_analysis
        result = cross_subject_analysis(subjects)
    except ImportError:
        return {"error": "anchor_adapter 模块未找到"}

    # 应用 min_correlation 过滤
    if 'correlation_matrix' in result:
        filtered = {}
        for s1, row in result['correlation_matrix'].items():
            filtered[s1] = {
                s2: v for s2, v in row.items()
                if v['shared_sources'] >= min_correlation or s1 == s2
            }
        result['correlation_matrix'] = filtered

    return result


def tool_summarize_content(args: Dict) -> Dict:
    """文本摘要 + 关键词提取（v1.7.0 新增第 8 工具）

    主路径: summa TextRank（沙箱内置，零依赖）
    兜底路径: LLM API（用户配 INFOSEEK_LLM_API_KEY）
    无 LLM 时自动降级到文本截断
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))

    text = args.get('text', '').strip()
    max_words = args.get('max_words', 100)
    prefer = args.get('prefer', 'summa')

    if not text:
        return {"error": "text 参数不能为空"}

    try:
        from summarize_adapter import summarize
        # v1.0.1 PATCH: LLM key 经 KeyManager 归一化读取（无注册时退化 env）
        try:
            from core.key_manager import KeyManager
            _llm_key = KeyManager.instance().get('infoseek_llm')
        except Exception:
            _llm_key = os.environ.get('INFOSEEK_LLM_API_KEY')
        result = summarize(
            text=text,
            max_words=max_words,
            prefer=prefer,
            llm_api_key=_llm_key,
            llm_api_base=os.environ.get('INFOSEEK_LLM_API_BASE'),
            llm_model=os.environ.get('INFOSEEK_LLM_MODEL')
        )
        return result
    except ImportError:
        # summarize_adapter 未找到 → 最简单的截断
        return {
            "summary": text[:500] + ("..." if len(text) > 500 else ""),
            "keywords": [],
            "method": "emergency_truncation",
            "fallback_used": True,
            "input_length": len(text)
        }
    except Exception as e:
        return {"error": f"summarize 调用失败: {type(e).__name__}: {e}"}

