#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
brief.py
将结构化新闻数据生成可读的文字简报
"""

import re
import requests
from datetime import datetime

# 分类 emoji
CATEGORY_EMOJI = {
    "时政": "🏛",
    "经济": "💹",
    "社会": "🌐",
    "国际": "🌍",
    "科技": "🔬",
    "体育": "⚽",
    "文娱": "🎬",
    "军事": "🛡",
    "教育": "📚",
    "法治": "⚖️",
    "环境": "🌱",
    "农业": "🌾",
}


def _gen_overview(all_news: dict, deepseek_key: str) -> str:
    """用 DeepSeek 生成3句话总览"""
    titles = []
    for cat, items in all_news.items():
        for it in items[:3]:
            titles.append(f"[{cat}] {it.get('title','')}")
    if not titles:
        return ""

    prompt = (
        f"以下是今日各分类的重要新闻标题，请用3句话概括今日最重要的动态。\n"
        f"要求：简洁，客观，不重复，覆盖不同领域。直接输出3句话，不加序号。\n\n"
        + "\n".join(titles[:15])
    )
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 200, "temperature": 0.3},
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def _gen_insight(all_news: dict, deepseek_key: str) -> str:
    """用 DeepSeek 生成1句话趋势洞察"""
    titles = []
    for cat, items in all_news.items():
        for it in items[:2]:
            titles.append(it.get("title", ""))
    if not titles:
        return ""

    prompt = (
        f"根据以下今日新闻，用1句话点出最值得关注的趋势或信号（不超过50字）：\n"
        + "\n".join(titles[:10])
    )
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 80, "temperature": 0.5},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        return ""


def generate_brief(all_news: dict, config: dict, deepseek_key: str) -> str:
    """
    生成完整简报文本
    all_news: {category: [items...]}
    config:   来自 config.yaml
    """
    today      = datetime.now().strftime("%Y/%m/%d")
    categories = list(all_news.keys())
    cat_str    = " · ".join(categories)
    lines      = []

    # ── 标题行 ──────────────────────────────────────────────
    lines.append(f"【今日简报】{today}  {cat_str}")
    lines.append("")

    # ── 今日概览 ────────────────────────────────────────────
    if config.get("include_overview", True):
        overview = _gen_overview(all_news, deepseek_key)
        if overview:
            lines.append("📌 今日概览")
            lines.append(overview)
            lines.append("")

    # ── 各分类新闻 ───────────────────────────────────────────
    for cat, items in all_news.items():
        if not items:
            continue
        emoji = CATEGORY_EMOJI.get(cat, "📰")
        lines.append(f"{'━'*20}")
        lines.append(f"{emoji} {cat}（{len(items)}条）")
        lines.append(f"{'━'*20}")

        for idx, it in enumerate(items, 1):
            title     = it.get("title", "")
            source_cn = it.get("source_cn") or it.get("source", "")
            pub_time  = it.get("pub_time", "")
            location  = it.get("location", "")
            content   = it.get("content") or it.get("desc", "")
            url       = it.get("url", "")

            # 元信息行
            meta_parts = [f"来源：{source_cn}"]
            if pub_time:
                meta_parts.append(f"{pub_time}")
            if location:
                meta_parts.append(f"{location}")
            meta = "｜".join(meta_parts)

            lines.append(f"{idx}. {title}")
            lines.append(f"   {meta}")
            if content:
                # 自动折行（每行不超过40字）
                wrapped = _wrap_text(content, 40, prefix="   ")
                lines.append(wrapped)
            if url:
                lines.append(f"   🔗 {url}")
            lines.append("")

    # ── 今日洞察 ────────────────────────────────────────────
    if config.get("include_insight", True):
        insight = _gen_insight(all_news, deepseek_key)
        if insight:
            lines.append(f"{'━'*20}")
            lines.append(f"💡 今日洞察")
            lines.append(f"   {insight}")
            lines.append("")

    # ── 页脚 ────────────────────────────────────────────────
    total = sum(len(v) for v in all_news.values())
    lines.append(f"{'─'*20}")
    lines.append(f"共 {total} 条新闻  数据来自权威媒体  仅供参考")

    return "\n".join(lines)


def _wrap_text(text: str, width: int, prefix: str = "") -> str:
    """简单按字数折行"""
    if len(text) <= width:
        return prefix + text
    result, line = [], ""
    for ch in text:
        line += ch
        if len(line) >= width:
            result.append(prefix + line)
            line = ""
    if line:
        result.append(prefix + line)
    return "\n".join(result)
