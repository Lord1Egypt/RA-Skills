#!/usr/bin/env python3
"""
生成 HuggingFace Papers 分析报告
包含论文列表、趋势分析、阅读推荐（含 DeepLX 中文翻译）

Usage:
    python generate_report.py --period weekly --limit 10
    python generate_report.py --period weekly --output report.md
    python generate_report.py --period weekly --no-translate  # 输出英文原文
    python generate_report.py --period daily --date 2026-04-29  # 指定日期
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import List, Dict, Optional

from get_papers import get_papers

# DeepLX / OpenAI LLM 翻译配置 - 从环境变量读取，禁止硬编码 token
# 设置方式（优先级从高到低）：
#   1. export 环境变量（任意框架通用）
#   2. 在 skill 目录下创建 .env 文件（任意框架通用）
#   3. 在 agent 的默认 env 文件中配置（如 ~/.hermes/.env）
import os
from dotenv import load_dotenv

# 优先加载本地 .env（与脚本同目录或 skill 根目录）
_local_env = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(_local_env)

# --- DeepLX 配置 ---
DEEPLX_URL = os.environ.get("DEEPLX_URL", "")
DEEPLX_TIMEOUT = 10

# --- OpenAI LLM 配置（备选翻译后端） ---
TRANSLATE_BACKEND = os.environ.get("TRANSLATE_BACKEND", "deeplx")  # deeplx / openai
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TIMEOUT = 30

TRANSLATION_SYSTEM_PROMPT = (
    "You are a professional translator. Translate the following English academic paper "
    "abstract into Chinese. Keep all technical terms accurate. Output only the translation, "
    "no explanations, no notes."
)


def translate_deeplx(text: str, target_lang: str = "ZH", source_lang: str = "EN") -> Optional[str]:
    """使用 DeepLX API 翻译"""
    payload = json.dumps({
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang
    }).encode("utf-8")

    req = urllib.request.Request(
        DEEPLX_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=DEEPLX_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("code") == 200:
                return result.get("data", "").strip()
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"  ⚠️ DeepLX 翻译失败 ({type(e).__name__})", file=sys.stderr)

    return None


def translate_openai(text: str, target_lang: str = "ZH", source_lang: str = "EN") -> Optional[str]:
    """使用 OpenAI 兼容 API 翻译"""
    if not OPENAI_API_KEY:
        print("  ⚠️ OPENAI_API_KEY 未设置，跳过 LLM 翻译", file=sys.stderr)
        return None

    payload = json.dumps({
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
            {"role": "user", "content": f"Translate from {source_lang} to {target_lang}:\n\n{text}"}
        ],
        "temperature": 0.1,
        "max_tokens": 4096
    }).encode("utf-8")

    url = OPENAI_BASE_URL.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "User-Agent": "hf-papers-skill/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
            if content:
                return content
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"  ⚠️ OpenAI 翻译失败 ({type(e).__name__})", file=sys.stderr)

    return None


def translate_text(text: str, target_lang: str = "ZH", source_lang: str = "EN") -> Optional[str]:
    """翻译文本（根据 TRANSLATE_BACKEND 选择后端）"""
    if not text or not text.strip():
        return text

    if TRANSLATE_BACKEND == "openai":
        result = translate_openai(text, target_lang, source_lang)
        if result:
            return result
        print("  ⚠️ LLM 翻译失败，降级到 DeepLX...", file=sys.stderr)
        return translate_deeplx(text, target_lang, source_lang) or text

    # 默认：DeepLX
    result = translate_deeplx(text, target_lang, source_lang)
    if result:
        return result
    print("  ⚠️ DeepLX 翻译失败，降级到 OpenAI LLM...", file=sys.stderr)
    return translate_openai(text, target_lang, source_lang) or text


def batch_translate(texts: List[str], target_lang: str = "ZH", source_lang: str = "EN") -> List[str]:
    """批量翻译（逐个调用，打印进度）"""
    results = []
    total = len(texts)
    for i, text in enumerate(texts, 1):
        if not text or not text.strip():
            results.append(text)
            continue
        print(f"  🌐 翻译中 ({i}/{total})...", file=sys.stderr)
        translated = translate_text(text, target_lang, source_lang)
        results.append(translated)
    return results


def analyze_categories(papers: List[Dict]) -> tuple[Dict[str, int], Dict[int, List[str]]]:
    """分析论文类别分布"""
    categories = {
        "Agentic AI": ["agent", "tool", "autonomous", "multi-agent", "llm agent", "agentic", "reasoning agent"],
        "多模态": ["multimodal", "vision", "video", "3d", "image", "visual", "vlm", "vision-language"],
        "生成模型": ["generation", "diffusion", "generative", "synthesis", "gans", "image generation"],
        "大语言模型": ["llm", "language model", "gpt", "claude", "gemini", "chatbot"],
        "推理优化": ["reasoning", "inference", "optimization", "efficient", "fast", "latency"],
        "架构创新": ["transformer", "architecture", "attention", "moe", "mixture", "mamba"],
        "训练方法": ["training", "fine-tuning", "rl", "reinforcement", "distillation", "sft"],
        "安全与对齐": ["safety", "alignment", "rlhf", "preference", "ethics", "bias"]
    }

    category_counts: Dict[str, int] = {cat: 0 for cat in categories}
    paper_categories: Dict[int, List[str]] = {}

    for i, paper in enumerate(papers):
        text = (paper.get("title", "") + " " + paper.get("abstract", "")).lower()
        matched: List[str] = []
        for cat, keywords in categories.items():
            if any(kw in text for kw in keywords):
                category_counts[cat] += 1
                matched.append(cat)
        paper_categories[i] = matched

    return category_counts, paper_categories


def generate_trend_analysis(papers: List[Dict]) -> str:
    """生成趋势分析"""
    category_counts, _ = analyze_categories(papers)
    sorted_cats = sorted(list(category_counts.items()), key=lambda x: x[1], reverse=True)

    lines = ["### 热门方向\n"]
    for cat, count in sorted_cats:
        if count > 0:
            bar = "█" * count + "░" * max(0, 5 - count)
            lines.append(f"- **{cat}**: {bar} ({count}篇)")

    lines.append("\n### 技术趋势\n")

    top_cats = [c for c, n in sorted_cats if n > 0][:3]
    if top_cats:
        lines.append(f"1. **{top_cats[0]}** 是当前最热门方向")
        if len(top_cats) > 1:
            lines.append(f"2. **{top_cats[1]}** 紧随其后")

    return "\n".join(lines)


def generate_recommendations(papers: List[Dict]) -> str:
    """生成阅读推荐"""
    if not papers:
        return ""

    sorted_papers = sorted(papers, key=lambda x: x.get("upvotes", 0), reverse=True)

    lines = ["### 推荐阅读\n"]

    must_read = sorted_papers[:3]
    lines.append("**⭐⭐⭐ 必读 (高热度):**")
    for i, p in enumerate(must_read, 1):
        title = p.get("title", "Unknown")[:70]
        upvotes = p.get("upvotes", 0)
        lines.append(f"{i}. [{title}]({p.get('url', '')}) (👍 {upvotes})")

    if len(sorted_papers) > 3:
        important = sorted_papers[3:7]
        lines.append("\n**⭐⭐ 值得关注:**")
        for p in important:
            title = p.get("title", "Unknown")[:60]
            lines.append(f"- [{title}]({p.get('url', '')})")

    return "\n".join(lines)


def format_report(papers: List[Dict], period: str, no_translate: bool = False) -> str:
    """格式化完整报告"""
    period_names = {
        "daily": "今日",
        "weekly": "本周",
        "monthly": "本月"
    }

    lines = [
        f"# 📄 HuggingFace Papers {period_names.get(period, period)}热门 TOP{len(papers)}",
        "",
        f"**获取时间:** {datetime.now().strftime('%Y年%m月%d日 %H:%M')} (GMT+8)",
        "",
        "---",
        ""
    ]

    sorted_papers = sorted(papers, key=lambda x: x.get("upvotes", 0), reverse=True)

    # 批量翻译摘要（除非指定 --no-translate）
    if not no_translate:
        abstracts = [p.get("abstract", "") for p in sorted_papers]
        translated_abstracts = batch_translate(abstracts)
    else:
        translated_abstracts = [p.get("abstract", "") for p in sorted_papers]

    for i, (paper, cn_abstract) in enumerate(zip(sorted_papers, translated_abstracts), 1):
        title = paper.get("title", "Unknown")
        paper_id = paper.get("paper_id", "")
        url = paper.get("url", f"https://huggingface.co/papers/{paper_id}")
        upvotes = paper.get("upvotes", 0)
        abstract = paper.get("abstract", "")

        lines.append(f"## {i}. {title}")
        lines.append(f"- 👍 **{upvotes}** upvotes")
        lines.append(f"- 🔗 {url}")

        # 如果有中文摘要，显示中英文
        if cn_abstract and cn_abstract != abstract:
            lines.append(f"- 📝 **中文摘要：** {cn_abstract}")
            if abstract:
                lines.append(f"- 📄 **原文摘要：** {abstract}")
        elif abstract:
            lines.append(f"- 📝 {abstract}")

        lines.append("")

    lines.extend([
        "---",
        "",
        "## 📊 趋势分析",
        "",
        generate_trend_analysis(papers),
        "",
        "---",
        "",
        generate_recommendations(papers),
        "",
        "---",
        "",
        "## 🔗 相关资源",
        "",
        "- [HuggingFace Papers](https://huggingface.co/papers)",
        "- [arXiv CS.AI](https://arxiv.org/list/cs.AI/recent)",
        "",
        f"*由 🤖 生成于 {datetime.now().strftime('%Y-%m-%d')}*"
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成 HuggingFace Papers 分析报告")
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"], default="weekly",
                        help="时间范围: daily/weekly/monthly")
    parser.add_argument("--limit", type=int, default=10,
                        help="论文数量 (默认: 10)")
    parser.add_argument("--output", type=str, default=None,
                        help="输出文件路径")
    parser.add_argument("--no-translate", action="store_true",
                        help="不翻译为中文，输出英文原文")

    args = parser.parse_args()

    print(f"🔍 正在获取 HuggingFace Papers {args.period} 数据...")

    try:
        papers = get_papers(args.period, args.limit)
    except Exception as e:
        print(f"❌ 获取失败: {e}", file=sys.stderr)
        sys.exit(1)

    if not papers:
        print("❌ 未能获取论文数据", file=sys.stderr)
        sys.exit(1)

    print(f"✅ 成功获取 {len(papers)} 篇论文")

    if not args.no_translate:
        print(f"🌐 正在通过 DeepLX 翻译摘要为中文...")

    report = format_report(papers, args.period, no_translate=args.no_translate)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"✅ 报告已保存到: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
