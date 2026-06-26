#!/usr/bin/env python3
"""
N-gram Similarity Calculator — paper-polisher v1.0.0
Calculate n-gram overlap/repetition rate for paraphrase evaluation.

Usage:
    python3 ngram_similarity.py <original_file> <rewritten_file>
    python3 ngram_similarity.py <original_file> <rewritten_file> --n 3
    python3 ngram_similarity.py <file> --self-repeat  # Check internal repetition
"""

import argparse
import json
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class NgramResult:
    ngram_size: int
    original_unique: int
    rewritten_unique: int
    overlap_count: int
    overlap_ratio: float  # ratio of overlapping n-grams to original
    repetition_rate_original: float
    repetition_rate_rewritten: float
    estimated_reduction: float  # estimated repetition reduction


def tokenize(text: str) -> list:
    """Simple tokenization: split on whitespace and punctuation, keep CJK chars individually."""
    # For Chinese: char-level
    # For English: word-level
    cjk = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
    total = max(len(text.strip()), 1)
    
    if cjk / total > 0.3:
        # Chinese: character-level n-grams
        chars = [ch for ch in text if ch.strip() and (
            '\u4e00' <= ch <= '\u9fff' or ch.isalnum()
        )]
        return chars
    else:
        # English: word-level n-grams
        return re.findall(r'\b[a-zA-Z]+\b', text.lower())


def get_ngrams(tokens: list, n: int) -> Counter:
    """Get n-gram counts."""
    return Counter(tuple(tokens[i:i+n]) for i in range(max(len(tokens) - n + 1, 0)))


def calc_repetition_rate(ngram_counts: Counter) -> float:
    """Calculate what fraction of n-grams are repeated (count > 1)."""
    if not ngram_counts:
        return 0.0
    total = sum(ngram_counts.values())
    repeated = sum(c - 1 for c in ngram_counts.values() if c > 1)
    return repeated / total if total > 0 else 0.0


def compare_files(original_path: str, rewritten_path: str, n: int = 3) -> dict:
    """Compare n-gram overlap between original and rewritten text."""
    with open(original_path, "r", encoding="utf-8") as f:
        orig_text = f.read()
    with open(rewritten_path, "r", encoding="utf-8") as f:
        rewrite_text = f.read()

    orig_tokens = tokenize(orig_text)
    rewrite_tokens = tokenize(rewrite_text)

    orig_ngrams = get_ngrams(orig_tokens, n)
    rewrite_ngrams = get_ngrams(rewrite_tokens, n)

    # Overlap: n-grams in rewrite that also appear in original
    orig_set = set(orig_ngrams.keys())
    rewrite_set = set(rewrite_ngrams.keys())
    overlap = orig_set & rewrite_set

    orig_unique = len(orig_set)
    rewrite_unique = len(rewrite_set)
    overlap_count = len(overlap)
    overlap_ratio = overlap_count / max(orig_unique, 1)

    orig_repeat = calc_repetition_rate(orig_ngrams)
    rewrite_repeat = calc_repetition_rate(rewrite_ngrams)
    reduction = max(0, orig_repeat - rewrite_repeat)

    results = []
    # Run for multiple n-gram sizes
    for size in [2, 3, 4]:
        on = get_ngrams(orig_tokens, size)
        rn = get_ngrams(rewrite_tokens, size)
        os_, rs_ = set(on.keys()), set(rn.keys())
        ov = os_ & rs_
        results.append(asdict(NgramResult(
            ngram_size=size,
            original_unique=len(os_),
            rewritten_unique=len(rs_),
            overlap_count=len(ov),
            overlap_ratio=round(len(ov) / max(len(os_), 1), 3),
            repetition_rate_original=round(calc_repetition_rate(on), 3),
            repetition_rate_rewritten=round(calc_repetition_rate(rn), 3),
            estimated_reduction=round(max(0, calc_repetition_rate(on) - calc_repetition_rate(rn)), 3)
        )))

    # Summary
    main = results[0] if n == 2 else results[1] if n == 3 else results[2]
    avg_overlap = sum(r["overlap_ratio"] for r in results) / len(results)
    
    if avg_overlap > 0.6:
        assessment = "🔴 降重效果有限 — 大量n-gram重复，建议进一步改写"
    elif avg_overlap > 0.3:
        assessment = "🟡 降重中等 — 部分表述仍相似，可考虑局部调整"
    else:
        assessment = "🟢 降重效果良好 — 文本差异显著"

    summary_lines = [
        f"N-gram对比分析（2/3/4-gram）:",
        f"  2-gram: 重叠率 {results[0]['overlap_ratio']:.1%} | 重复率 {results[0]['repetition_rate_original']:.1%} → {results[0]['repetition_rate_rewritten']:.1%}",
        f"  3-gram: 重叠率 {results[1]['overlap_ratio']:.1%} | 重复率 {results[1]['repetition_rate_original']:.1%} → {results[1]['repetition_rate_rewritten']:.1%}",
        f"  4-gram: 重叠率 {results[2]['overlap_ratio']:.1%} | 重复率 {results[2]['repetition_rate_original']:.1%} → {results[2]['repetition_rate_rewritten']:.1%}",
        f"  平均重叠率: {avg_overlap:.1%}",
        f"  {assessment}"
    ]

    return {
        "results": results,
        "avg_overlap": round(avg_overlap, 3),
        "summary": "\n".join(summary_lines)
    }


def self_repetition(file_path: str) -> dict:
    """Check internal repetition within a single file."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    tokens = tokenize(text)
    results = []
    for n in [2, 3, 4, 5]:
        ngrams = get_ngrams(tokens, n)
        rate = calc_repetition_rate(ngrams)
        top = ngrams.most_common(5)
        results.append({
            "n": n,
            "unique_ngrams": len(ngrams),
            "repetition_rate": round(rate, 3),
            "top_repeated": [
                {"ngram": " ".join(str(t) for t in ng), "count": c}
                for ng, c in top if c > 1
            ]
        })

    overall = sum(r["repetition_rate"] for r in results) / len(results)
    if overall > 0.15:
        level = "🔴 高重复"
    elif overall > 0.05:
        level = "🟡 中等重复"
    else:
        level = "🟢 低重复"

    lines = [f"内部重复率分析: {level}（平均 {overall:.1%}）"]
    for r in results:
        lines.append(f"  {r['n']}-gram: 重复率 {r['repetition_rate']:.1%}（{r['unique_ngrams']} 个唯一）")
        for t in r["top_repeated"][:3]:
            lines.append(f"    ↳ \"{t['ngram']}\" ×{t['count']}")

    return {"results": results, "overall_rate": round(overall, 3), "summary": "\n".join(lines)}


def main():
    parser = argparse.ArgumentParser(description="N-gram Similarity Calculator")
    parser.add_argument("files", nargs="+", help="Input file(s)")
    parser.add_argument("--n", type=int, default=3, help="N-gram size (default: 3)")
    parser.add_argument("--self-repeat", action="store_true", help="Check internal repetition")
    parser.add_argument("--output", help="Output JSON file")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args()

    for fp in args.files:
        if not os.path.exists(fp):
            print(f"Error: File not found: {fp}", file=sys.stderr)
            sys.exit(1)

    if args.self_repeat:
        result = self_repetition(args.files[0])
    elif len(args.files) >= 2:
        result = compare_files(args.files[0], args.files[1], args.n)
    else:
        print("Error: Need 2 files for comparison, or --self-repeat with 1 file", file=sys.stderr)
        sys.exit(1)

    if args.format == "json" or args.output:
        output_str = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"Saved to {args.output}", file=sys.stderr)
        else:
            print(output_str)
    else:
        print(result["summary"])


if __name__ == "__main__":
    main()
