#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 摘要生成

V1.5 新增。多结果自动总结，"用一句话告诉我答案"。

遵循死规则 9：基础功能自研，外部 API 按需接入，必须提供降级方案。

主方案：调用外部 LLM API（智谱 GLM-4-Flash 优先，免费）
降级方案：无 API Key 时 → 抽取式摘要（取 snippet 关键句拼接）

配置（config.yaml）：
  llm_summary:
    enabled: true
    provider: auto        # auto / zhipu / extractive
    api_key: ""           # 空 = 强制降级
    model: glm-4-flash
"""

import json
import sys
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True

# 降级摘要（无 API Key 时使用）
_MAX_EXTRACTIVE_SENTENCES = 5
_MAX_EXTRACTIVE_CHARS = 800


def _extractive_summarize(query: str, results: List[Any]) -> str:
    """
    抽取式摘要（降级方案）

    从排序最高的结果中抽取关键句拼接。
    不调用外部 API，纯本地计算。
    """
    if not results:
        return "没有找到相关结果。"

    # 取前 5 条结果
    top = results[:5]

    # 收集 snippet 和来源
    snippets = []
    for r in top:
        text = getattr(r, "snippet", "") or ""
        title = getattr(r, "title", "") or ""
        engine = getattr(r, "engine", "") or ""
        if isinstance(engine, (list, tuple)):
            engine = ", ".join(engine)
        if text:
            snippets.append((text, title, engine))

    if not snippets:
        return "没有找到可用的结果摘要。"

    # 简单抽取：取每条 snippet 的第一句
    extracted = []
    for text, title, engine in snippets:
        # 按句号、问号、感叹号分句
        sentences = []
        current = ""
        for ch in text:
            current += ch
            if ch in "。！？":
                sentences.append(current.strip())
                current = ""
        if current.strip():
            sentences.append(current.strip())

        if sentences:
            # 取第一句（通常是最重要的）
            extracted.append(sentences[0])

    if not extracted:
        return "无法从结果中提取摘要。"

    # 拼接，标注来源
    parts = []
    for i, sent in enumerate(extracted[:_MAX_EXTRACTIVE_SENTENCES], 1):
        parts.append(f"{i}. {sent}")

    summary = "\n".join(parts)
    if len(summary) > _MAX_EXTRACTIVE_CHARS:
        summary = summary[:_MAX_EXTRACTIVE_CHARS] + "..."

    return f"[抽取式摘要，建议查看原文]\n\n{summary}"


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
            {"role": "system", "content": "你是一个搜索助手。根据搜索结果回答问题，回答要简洁准确，标注信息来源。"},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 500,
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
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
    except Exception:
        pass
    return None


def _build_prompt(query: str, results: List[Any]) -> str:
    """构建 LLM prompt"""
    parts = [f"用户问题：{query}\n\n以下是搜索结果：\n"]

    for i, r in enumerate(results[:8], 1):
        title = getattr(r, "title", "") or "无标题"
        snippet = getattr(r, "snippet", "") or ""
        url = getattr(r, "url", "") or ""
        engine = getattr(r, "engine", "") or ""
        if isinstance(engine, (list, tuple)):
            engine = ", ".join(engine)

        parts.append(f"[{i}] {title}")
        if snippet:
            parts.append(f"    {snippet}")
        if url:
            parts.append(f"    链接：{url}")
        if engine:
            parts.append(f"    引擎：{engine}")
        parts.append("")

    parts.append("请用 3-5 句话总结搜索结果，回答用户问题。标注信息来源（如：根据搜索结果[1][3]...）。")
    return "\n".join(parts)


def summarize(query: str, results: List[Any], config: Optional[Dict[str, Any]] = None) -> str:
    """
    生成摘要

    主方案：调用外部 LLM API
    降级：无 API Key 时 → 抽取式摘要

    Returns:
        摘要文本
    """
    if not results:
        return "没有找到相关结果。"

    llm_cfg = (config or {}).get("llm_summary", {}) or {}

    # 禁用摘要
    if not llm_cfg.get("enabled", True):
        return _extractive_summarize(query, results)

    # 强制抽取式
    provider = llm_cfg.get("provider", "auto")
    if provider == "extractive":
        return _extractive_summarize(query, results)

    api_key = (llm_cfg.get("api_key") or "").strip()
    model = llm_cfg.get("model", "glm-4-flash")

    # 有 API Key → 调用 LLM
    if api_key:
        prompt = _build_prompt(query, results)
        llm_result = _call_zhipu(api_key, model, prompt)
        if llm_result:
            return llm_result

    # 降级
    return _extractive_summarize(query, results)
