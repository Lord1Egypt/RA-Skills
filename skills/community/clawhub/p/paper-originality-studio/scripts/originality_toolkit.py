#!/usr/bin/env python3
"""Local originality optimization toolkit for paper-originality-studio.

Subcommands:
  scan    Analyze a manuscript for repetition, template phrases, AI-style markers and citation patterns.
  compare Compare original and revised text for closeness and shared fragments.
  chunk   Split a long manuscript into manageable section files.
  prompt  Generate a structured rewrite prompt template.

This script uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import difflib
import json
import math
import os
from pathlib import Path
import re
import sys
from typing import Dict, Iterable, List, Sequence, Tuple

BASE_DIR = Path(__file__).resolve().parents[1]
RESOURCES = BASE_DIR / "resources" / "rewrite_patterns_zh.json"


def read_text(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {p}")
    return p.read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")


def load_patterns() -> Dict[str, object]:
    if not RESOURCES.exists():
        raise FileNotFoundError(f"Resource file missing: {RESOURCES}")
    return json.loads(RESOURCES.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def simplify_for_compare(text: str) -> str:
    text = normalize_text(text)
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[，。；：、“”‘’（）()【】\[\],.;:!?！？\-—…·]", "", text)
    return text.lower()


def split_paragraphs(text: str) -> List[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", normalize_text(text)) if p.strip()]


def split_sentences(text: str) -> List[str]:
    normalized = normalize_text(text)
    raw = re.split(r"(?<=[。！？!?；;])|\n", normalized)
    out = []
    for part in raw:
        s = part.strip()
        if not s:
            continue
        if len(s) < 2:
            continue
        out.append(s)
    return out


def heading_like(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r"^#{1,6}\s+\S+", stripped):
        return True
    if re.match(r"^[一二三四五六七八九十]+[、.．]\s*\S+", stripped):
        return True
    if re.match(r"^\d+(\.\d+){0,3}\s+\S+", stripped):
        return True
    if stripped in {"摘要", "关键词", "引言", "绪论", "方法", "结果", "讨论", "结论", "参考文献", "附录"}:
        return True
    return False


def count_shingles(text: str, size: int = 8) -> collections.Counter:
    clean = simplify_for_compare(text)
    if len(clean) < size:
        return collections.Counter()
    return collections.Counter(clean[i:i + size] for i in range(len(clean) - size + 1))


def top_repeated_items(counter: collections.Counter, minimum: int = 2, limit: int = 10) -> List[Tuple[str, int]]:
    items = [(k, v) for k, v in counter.items() if v >= minimum]
    items.sort(key=lambda x: (-x[1], -len(x[0]), x[0]))
    return items[:limit]


def citation_counts(text: str) -> Dict[str, int]:
    numeric = len(re.findall(r"\[[0-9,\-–— ]+\]", text))
    year_en = len(re.findall(r"\([A-Z][A-Za-z .,&-]+,\s*\d{4}[a-z]?\)", text))
    year_cn = len(re.findall(r"（[^（）]{1,20}[，,]\s*\d{4}[a-z]?）", text))
    doi = len(re.findall(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", text, flags=re.I))
    return {
        "numeric_style": numeric,
        "author_year_en": year_en,
        "author_year_zh": year_cn,
        "doi_mentions": doi,
    }


def quote_ratio(text: str) -> float:
    quoted = sum(len(m.group(1)) for m in re.finditer(r"[“\"]([^”\"]+)[”\"]", text))
    total = max(len(text), 1)
    return quoted / total


def scan_text(text: str, patterns: Dict[str, object]) -> Dict[str, object]:
    paragraphs = split_paragraphs(text)
    sentences = split_sentences(text)
    normalized_sentences = [simplify_for_compare(s) for s in sentences]
    sentence_counter = collections.Counter(s for s in normalized_sentences if len(s) >= 8)
    repeated_sentences = top_repeated_items(sentence_counter, minimum=2, limit=8)

    shingles = count_shingles(text, size=8)
    repeated_shingles = [(frag, count) for frag, count in top_repeated_items(shingles, minimum=3, limit=12) if len(frag) >= 8]

    phrase_hits = []
    total_template_hits = 0
    for group in patterns.get("template_phrases", []):
        category = group.get("category", "未分类")
        phrases = group.get("phrases", [])
        hits = []
        for phrase in phrases:
            count = text.count(phrase)
            if count:
                hits.append({"phrase": phrase, "count": count})
                total_template_hits += count
        if hits:
            phrase_hits.append({"category": category, "hits": hits})

    ai_hits = []
    ai_total = 0
    for marker in patterns.get("ai_style_markers", []):
        count = text.count(marker)
        if count:
            ai_hits.append({"phrase": marker, "count": count})
            ai_total += count

    paragraph_lengths = [len(p) for p in paragraphs]
    long_paragraphs = [i + 1 for i, n in enumerate(paragraph_lengths) if n >= 220]
    short_paragraphs = [i + 1 for i, n in enumerate(paragraph_lengths) if n <= 40]

    warnings = []
    for phrase in patterns.get("warning_phrases", []):
        if phrase in text:
            warnings.append(f"命中敏感表达：{phrase}")

    quote_r = quote_ratio(text)
    citations = citation_counts(text)

    score = 0
    score += min(total_template_hits * 2, 25)
    score += min(ai_total * 2, 20)
    score += min(len(repeated_sentences) * 6, 18)
    score += min(len(repeated_shingles), 10)
    if quote_r > 0.18:
        score += 8
    if long_paragraphs:
        score += min(len(long_paragraphs) * 2, 8)

    if score >= 45:
        risk = "高"
    elif score >= 25:
        risk = "中"
    else:
        risk = "低"

    recommendations = []
    if total_template_hits >= 3:
        recommendations.append("优先清理套话开头和空泛过渡句，不要只做近义词替换。")
    if ai_total >= 4:
        recommendations.append("减少机械连接词，改为显式因果、对比或限制关系。")
    if repeated_sentences:
        recommendations.append("存在重复句式，建议重组段落信息顺序并改写句法骨架。")
    if long_paragraphs:
        recommendations.append("长段落建议拆分为“问题—解释—结论”或“现象—原因—影响”结构。")
    if quote_r > 0.18:
        recommendations.append("直接引语比例偏高，核查是否可改为转述并保留引用。")
    if not recommendations:
        recommendations.append("整体表达风险可控，建议聚焦术语统一与逻辑精炼。")

    return {
        "summary": {
            "paragraphs": len(paragraphs),
            "sentences": len(sentences),
            "characters": len(text),
            "risk_level": risk,
            "risk_score": score,
        },
        "phrase_hits": phrase_hits,
        "ai_style_hits": ai_hits,
        "repeated_sentences_count": len(repeated_sentences),
        "repeated_sentences": repeated_sentences,
        "repeated_shingles": repeated_shingles,
        "paragraph_lengths": paragraph_lengths,
        "long_paragraph_indexes": long_paragraphs,
        "short_paragraph_indexes": short_paragraphs,
        "quote_ratio": round(quote_r, 4),
        "citation_counts": citations,
        "warnings": warnings,
        "recommendations": recommendations,
    }


def render_scan_markdown(result: Dict[str, object], source_name: str = "input") -> str:
    s = result["summary"]
    lines = [
        f"# Originality Scan Report - {source_name}",
        "",
        "## Summary",
        f"- 段落数：{s['paragraphs']}",
        f"- 句子数：{s['sentences']}",
        f"- 字符数：{s['characters']}",
        f"- 风险等级：{s['risk_level']}",
        f"- 风险分：{s['risk_score']}",
        "",
        "## Recommendations",
    ]
    for rec in result["recommendations"]:
        lines.append(f"- {rec}")

    lines.extend(["", "## Template / Cliche Hits"])
    if result["phrase_hits"]:
        for group in result["phrase_hits"]:
            lines.append(f"### {group['category']}")
            for hit in group["hits"]:
                lines.append(f"- `{hit['phrase']}` × {hit['count']}")
    else:
        lines.append("- 未发现明显高频套话。")

    lines.extend(["", "## AI-style Marker Hits"])
    if result["ai_style_hits"]:
        for hit in result["ai_style_hits"]:
            lines.append(f"- `{hit['phrase']}` × {hit['count']}")
    else:
        lines.append("- 未发现显著 AI 风格标记。")

    lines.extend(["", "## Repetition Signals"])
    lines.append(f"- 重复句数量：{result['repeated_sentences_count']}")
    if result["repeated_sentences"]:
        for sentence, count in result["repeated_sentences"]:
            lines.append(f"- 重复标准化句片段：`{sentence[:60]}` × {count}")
    else:
        lines.append("- 未发现重复标准化句。")

    if result["repeated_shingles"]:
        lines.append("- 高频共享片段：")
        for frag, count in result["repeated_shingles"]:
            lines.append(f"  - `{frag}` × {count}")

    lines.extend([
        "",
        "## Paragraph Signals",
        f"- 长段落索引：{result['long_paragraph_indexes'] or '无'}",
        f"- 短段落索引：{result['short_paragraph_indexes'] or '无'}",
        f"- 直接引语比例：{result['quote_ratio']}",
        "",
        "## Citation Patterns",
    ])
    for key, value in result["citation_counts"].items():
        lines.append(f"- {key}: {value}")

    if result["warnings"]:
        lines.extend(["", "## Warnings"])
        for item in result["warnings"]:
            lines.append(f"- {item}")

    return "\n".join(lines) + "\n"


def compare_texts(original: str, revised: str) -> Dict[str, object]:
    original_simple = simplify_for_compare(original)
    revised_simple = simplify_for_compare(revised)
    seq_ratio = difflib.SequenceMatcher(None, original_simple, revised_simple).ratio()

    s1 = set(split_sentences(original))
    s2 = set(split_sentences(revised))
    norm_s1 = {simplify_for_compare(s) for s in s1 if len(simplify_for_compare(s)) >= 8}
    norm_s2 = {simplify_for_compare(s) for s in s2 if len(simplify_for_compare(s)) >= 8}
    shared_sentences = sorted(norm_s1 & norm_s2, key=lambda x: (-len(x), x))

    sh1 = count_shingles(original, size=8)
    sh2 = count_shingles(revised, size=8)
    shared_shingles = set(sh1) & set(sh2)
    if sh1:
        shingle_retention = len(shared_shingles) / len(set(sh1))
    else:
        shingle_retention = 0.0
    if (set(sh1) | set(sh2)):
        shingle_jaccard = len(shared_shingles) / len(set(sh1) | set(sh2))
    else:
        shingle_jaccard = 0.0

    length_delta = len(revised_simple) - len(original_simple)
    warnings = []
    if seq_ratio >= 0.82:
        warnings.append("整体文本过于接近，仍可能属于表层替换。")
    if shingle_retention >= 0.65:
        warnings.append("原文 8 字共享片段保留较多，建议继续做结构性改写。")
    if len(shared_sentences) >= 3:
        warnings.append("完整句重合较多，建议减少原句直接保留。")
    if not warnings:
        warnings.append("接近度处于可继续人工审读的范围。")

    return {
        "sequence_ratio": round(seq_ratio, 4),
        "shingle_retention": round(shingle_retention, 4),
        "shingle_jaccard": round(shingle_jaccard, 4),
        "shared_sentences_count": len(shared_sentences),
        "shared_sentences": shared_sentences[:12],
        "original_chars": len(original),
        "revised_chars": len(revised),
        "length_delta": length_delta,
        "warnings": warnings,
    }


def render_compare_markdown(result: Dict[str, object], original_name: str, revised_name: str) -> str:
    lines = [
        f"# Compare Report - {original_name} vs {revised_name}",
        "",
        "## Metrics",
        f"- Sequence ratio: {result['sequence_ratio']}",
        f"- Shared 8-char shingle retention: {result['shingle_retention']}",
        f"- Shingle Jaccard: {result['shingle_jaccard']}",
        f"- Shared normalized sentences: {result['shared_sentences_count']}",
        f"- Original chars: {result['original_chars']}",
        f"- Revised chars: {result['revised_chars']}",
        f"- Length delta: {result['length_delta']}",
        "",
        "## Warnings",
    ]
    for item in result["warnings"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Shared Sentences"])
    if result["shared_sentences"]:
        for item in result["shared_sentences"]:
            lines.append(f"- `{item[:80]}`")
    else:
        lines.append("- 无完整句重合。")
    return "\n".join(lines) + "\n"


def chunk_text(text: str) -> List[Tuple[str, str]]:
    lines = normalize_text(text).splitlines()
    chunks: List[Tuple[str, List[str]]] = []
    current_title = "chunk-01"
    current_lines: List[str] = []
    unnamed_index = 1

    def flush():
        nonlocal current_lines, current_title, chunks
        body = "\n".join(current_lines).strip()
        if body:
            chunks.append((current_title, body))
        current_lines = []

    for line in lines:
        if heading_like(line):
            flush()
            current_title = line.strip().replace(" ", "_")
        else:
            current_lines.append(line)
    flush()

    if not chunks:
        paragraphs = split_paragraphs(text)
        chunks = []
        for i in range(0, len(paragraphs), 3):
            title = f"chunk-{unnamed_index:02d}"
            chunks.append((title, "\n\n".join(paragraphs[i:i + 3])))
            unnamed_index += 1
    return chunks


def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", name).strip("_")
    return name or "chunk"


def generate_prompt(section: str, goal: str, preserve: str = "") -> str:
    preserve_hint = preserve or "保留事实、数据、引用位置、术语边界"
    return f"""你现在是学术文本原创性优化助手。请按下面流程处理“{section}”部分：

目标：{goal}
必须保留：{preserve_hint}

请先输出：
1. 这一段 / 这一节最明显的 3-5 个问题；
2. 哪些问题需要结构重组，哪些只需句法重写；
3. 哪些信息不能改动。

然后再输出改写版本，要求：
- 不做机械同义词替换；
- 优先重组句子顺序与信息层次；
- 避免空泛套话与 AI 腔；
- 保持学术表达自然、准确、可复核；
- 不新增未被原文支持的事实、数据和引文；
- 改写后再补 3 条人工复核建议。
"""


def resolve_python() -> str:
    return sys.executable or "python3"


def cmd_scan(args: argparse.Namespace) -> int:
    patterns = load_patterns()
    text = read_text(args.input)
    result = scan_text(text, patterns)
    if args.json_out:
        write_text(args.json_out, json.dumps(result, ensure_ascii=False, indent=2))
    if args.report_md:
        write_text(args.report_md, render_scan_markdown(result, Path(args.input).name))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    original = read_text(args.original)
    revised = read_text(args.revised)
    result = compare_texts(original, revised)
    if args.json_out:
        write_text(args.json_out, json.dumps(result, ensure_ascii=False, indent=2))
    if args.report_md:
        write_text(args.report_md, render_compare_markdown(result, Path(args.original).name, Path(args.revised).name))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_chunk(args: argparse.Namespace) -> int:
    text = read_text(args.input)
    chunks = chunk_text(text)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    index_lines = ["# Chunk Index", ""]
    for idx, (title, body) in enumerate(chunks, start=1):
        filename = f"{idx:02d}-{sanitize_filename(title)}.txt"
        write_text(out_dir / filename, body + "\n")
        index_lines.append(f"- {filename}: {title}")
    write_text(out_dir / "INDEX.md", "\n".join(index_lines) + "\n")
    print(f"Wrote {len(chunks)} chunks to {out_dir}")
    return 0


def cmd_prompt(args: argparse.Namespace) -> int:
    print(generate_prompt(args.section, args.goal, args.preserve))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Originality optimization toolkit for academic rewriting.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Analyze a manuscript.")
    p_scan.add_argument("input", help="Input text file path.")
    p_scan.add_argument("--json-out", help="Write JSON report.")
    p_scan.add_argument("--report-md", help="Write Markdown report.")
    p_scan.set_defaults(func=cmd_scan)

    p_compare = sub.add_parser("compare", help="Compare original and revised texts.")
    p_compare.add_argument("original", help="Original file path.")
    p_compare.add_argument("revised", help="Revised file path.")
    p_compare.add_argument("--json-out", help="Write JSON report.")
    p_compare.add_argument("--report-md", help="Write Markdown report.")
    p_compare.set_defaults(func=cmd_compare)

    p_chunk = sub.add_parser("chunk", help="Split a manuscript into section chunks.")
    p_chunk.add_argument("input", help="Input text file path.")
    p_chunk.add_argument("--out-dir", required=True, help="Output directory.")
    p_chunk.set_defaults(func=cmd_chunk)

    p_prompt = sub.add_parser("prompt", help="Generate a structured rewrite prompt.")
    p_prompt.add_argument("--section", required=True, help="Section name, e.g. 摘要 / 引言 / 讨论")
    p_prompt.add_argument("--goal", required=True, help="Rewrite goal.")
    p_prompt.add_argument("--preserve", default="", help="Explicit preserve constraints.")
    p_prompt.set_defaults(func=cmd_prompt)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover
        print(f"[error] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
