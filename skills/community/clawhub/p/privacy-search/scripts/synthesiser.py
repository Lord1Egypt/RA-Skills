#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Perplexity 式答案合成（V1.6 新增）

功能：抓取搜索结果正文 → 分块编号 → LLM 带 citation 生成答案。
目标：答案可信度提升——每个论断都能追溯到具体来源。

遵循死规则 9：基础功能自研，外部 API 按需接入，必须提供降级方案。
遵循死规则 13：不生成 __pycache__。

主方案：调用外部 LLM API（智谱 GLM-4-Flash 优先，免费）
降级方案：无 API Key 时 → 抽取式摘要 + 来源列表（带编号引用）

配置（config.yaml）：
  synthesis:
    enabled: true
    provider: auto        # auto / zhipu / extractive
    api_key: ""           # 空 = 强制降级
    model: glm-4-flash
    max_sources: 5        # 最多引用几个来源
    chunk_size: 2000      # 每个正文块的最大字符数
    fetch_timeout: 10     # 单个页面抓取超时（秒）
"""

import json
import sys
from typing import Any, Dict, List, Optional, Tuple

sys.dont_write_bytecode = True

# ============================================================
# 正文抓取与分块
# ============================================================

def _fetch_contents(
    results: List[Any],
    max_sources: int = 5,
    timeout: int = 10,
    proxy: Optional[str] = None,
) -> List[Tuple[int, str, str, str]]:
    """
    抓取 Top-N 结果的正文内容

    Returns:
        [(source_id, url, content), ...] 列表，content 为空表示抓取失败
    """
    try:
        from page_fetcher import fetch_and_extract
    except ImportError:
        from .page_fetcher import fetch_and_extract

    contents: List[Tuple[int, str, str, str]] = []
    for i, r in enumerate(results[:max_sources], 1):
        url = getattr(r, "url", "") or ""
        title = getattr(r, "title", "") or ""
        if not url:
            continue
        try:
            _html, text = fetch_and_extract(url, timeout=timeout, proxy=proxy)
            if text and len(text.strip()) > 50:
                contents.append((i, url, text.strip()))
            else:
                # 正文太短或抓不到，用 snippet 兜底
                snippet = getattr(r, "snippet", "") or ""
                if snippet:
                    contents.append((i, url, snippet))
        except Exception:
            # 单个页面抓取失败不应中断整体流程
            snippet = getattr(r, "snippet", "") or ""
            if snippet:
                contents.append((i, url, snippet))
    return contents


def _chunk_text(text: str, chunk_size: int = 2000) -> List[str]:
    """
    按段落切分正文，每段不超过 chunk_size 字符

    优先按换行分段（保留语义完整性），超长段落再按句号切分。
    """
    if not text:
        return []
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    chunks: List[str] = []
    for para in paragraphs:
        if len(para) <= chunk_size:
            chunks.append(para)
        else:
            # 超长段落按句号切分
            sentences = []
            current = ""
            for ch in para:
                current += ch
                if ch in "。！？.!?" and len(current) > 20:
                    sentences.append(current.strip())
                    current = ""
            if current.strip():
                sentences.append(current.strip())
            # 合并短句到 chunk_size 以内
            buf = ""
            for sent in sentences:
                if len(buf) + len(sent) > chunk_size and buf:
                    chunks.append(buf)
                    buf = sent
                else:
                    buf += sent
            if buf:
                chunks.append(buf)
    return chunks


# ============================================================
# Prompt 构建
# ============================================================

def _build_pro_prompt(
    query: str,
    sources: List[Tuple[int, str, str, str]],
    chunk_size: int = 2000,
) -> str:
    """
    构建 Perplexity 式 prompt

    要求 LLM：
      1. 每个论断后标注来源编号 [1][2]...
      2. 无法从来源推断的信息必须明确说明「根据现有搜索结果无法确定」
      3. 答案简洁，重点突出
    """
    parts = [f"用户问题：{query}\n"]
    parts.append("以下是搜索结果的正文内容，每段标注了来源编号：\n")

    for source_id, url, content in sources:
        chunks = _chunk_text(content, chunk_size=chunk_size)
        # 每个来源只取前 2 个 chunk（控制 prompt 长度）
        for chunk_idx, chunk in enumerate(chunks[:2]):
            parts.append(f"[来源{source_id}] {url}")
            parts.append(chunk)
            parts.append("")

    parts.append(
        "请根据以上搜索结果回答用户问题。\n"
        "要求：\n"
        "1. 回答要简洁准确，直接回答问题\n"
        "2. 每个重要论断后标注来源编号，如 [1]、[2][3]\n"
        "3. 如果搜索结果不足以回答，请明确说明「根据现有搜索结果无法确定」\n"
        "4. 不要编造任何搜索结果中未出现的信息\n"
        "5. 用中文回答"
    )
    return "\n".join(parts)


# ============================================================
# LLM 调用（复用 summarizer 的模式）
# ============================================================

def _call_zhipu(api_key: str, model: str, prompt: str) -> Optional[str]:
    """
    调用智谱 GLM API

    智谱有免费额度（GLM-4-Flash），国内访问快。
    """
    try:
        import urllib.request
        import urllib.error
    except ImportError:
        return None

    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一个专业的研究助手。根据提供的搜索结果回答问题，"
                    "每个重要论断后标注来源编号（如 [1]、[2]）。"
                    "无法从搜索结果推断的信息必须明确说明。"
                    "回答要简洁、准确、有依据。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 1000,
        "temperature": 0.3,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None


# ============================================================
# 降级方案（抽取式 + 来源列表）
# ============================================================

def _extractive_synthesis(
    query: str,
    results: List[Any],
    max_sources: int = 5,
) -> str:
    """
    降级方案：抽取关键句 + 编号来源列表

    不调用外部 API，纯本地计算。
    """
    if not results:
        return "没有找到相关结果。"

    top = results[:max_sources]
    parts = []

    # 抽取关键句
    extracted: List[Tuple[int, str]] = []
    for i, r in enumerate(top, 1):
        text = getattr(r, "snippet", "") or ""
        title = getattr(r, "title", "") or ""
        if not text and not title:
            continue
        # 取 snippet 的第一句（通常是最重要的）
        content = text or title
        sentences = []
        current = ""
        for ch in content:
            current += ch
            if ch in "。！？.!?":
                sentences.append(current.strip())
                current = ""
        if current.strip():
            sentences.append(current.strip())

        if sentences:
            extracted.append((i, sentences[0]))

    if not extracted:
        return "无法从搜索结果中提取摘要。"

    parts.append("[抽取式摘要，建议查看原文]\n")
    for source_id, sent in extracted:
        parts.append(f"{source_id}. {sent} [{source_id}]")

    # 来源列表
    parts.append("\n--- 来源 ---")
    for i, r in enumerate(top, 1):
        title = getattr(r, "title", "") or "无标题"
        url = getattr(r, "url", "") or ""
        if url:
            parts.append(f"[{i}] {title}\n    {url}")
        else:
            parts.append(f"[{i}] {title}")

    return "\n".join(parts)


# ============================================================
# 主入口
# ============================================================

def synthesize_pro(
    query: str,
    results: List[Any],
    config: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Perplexity 式答案合成

    主方案：抓取正文 → 分块 → LLM 带 citation 生成
    降级：无 API Key 时 → 抽取式摘要 + 来源列表

    Args:
        query: 用户查询词
        results: 搜索结果列表
        config: 配置字典

    Returns:
        带 citation 的答案文本
    """
    if not results:
        return "没有找到相关结果。"

    synth_cfg = (config or {}).get("synthesis", {}) or {}

    # 禁用 Pro 合成
    if not synth_cfg.get("enabled", True):
        return _extractive_synthesis(query, results)

    provider = synth_cfg.get("provider", "auto")
    api_key = (synth_cfg.get("api_key") or "").strip()
    model = synth_cfg.get("model", "glm-4-flash")
    max_sources = int(synth_cfg.get("max_sources", 5))
    chunk_size = int(synth_cfg.get("chunk_size", 2000))
    fetch_timeout = int(synth_cfg.get("fetch_timeout", 10))

    # 读取代理配置（strict 模式下的代理）
    proxy = None
    privacy_cfg = (config or {}).get("privacy", {}) or {}
    strict_cfg = privacy_cfg.get("strict", {}) or {}
    proxy = strict_cfg.get("proxy", None)

    # 强制抽取式
    if provider == "extractive":
        return _extractive_synthesis(query, results, max_sources)

    # 无 API Key 时直接降级
    if not api_key:
        return _extractive_synthesis(query, results, max_sources)

    # 抓取正文
    sources = _fetch_contents(results, max_sources=max_sources, timeout=fetch_timeout, proxy=proxy)
    if not sources:
        # 所有页面都抓不到正文，降级为抽取式
        return _extractive_synthesis(query, results, max_sources)

    # 构建 prompt 并调用 LLM
    prompt = _build_pro_prompt(query, sources, chunk_size=chunk_size)
    llm_result = _call_zhipu(api_key, model, prompt)
    if llm_result:
        # 在答案末尾追加来源列表
        source_list = []
        for source_id, url, _content in sources:
            source_list.append(f"[{source_id}] {url}")
        
        # 事实核查层（V1.8 新增）
        full_answer = llm_result + "\n\n--- 来源 ---\n" + "\n".join(source_list)
        
        try:
            from fact_checker import fact_check, format_fact_check_report
            fc_result = fact_check(full_answer, sources, config)
            
            if fc_result["removed_claims"]:
                # 有论断被移除，使用清洗后的答案
                full_answer = fc_result["cleaned_answer"]
                # 追加来源列表
                full_answer += "\n\n--- 来源 ---\n" + "\n".join(source_list)
            
            # 追加事实核查报告
            full_answer += format_fact_check_report(fc_result)
        except Exception:
            # 事实核查失败不中断主流程
            pass
        
        return full_answer

    # LLM 调用失败，降级
    return _extractive_synthesis(query, results, max_sources)
