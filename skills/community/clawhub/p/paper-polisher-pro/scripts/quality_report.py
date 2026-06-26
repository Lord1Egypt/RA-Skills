#!/usr/bin/env python3
"""
Quality Report Generator — paper-polisher v1.0.0
Generate comprehensive quality assessment report for academic papers.

Usage:
    python3 quality_report.py <input_file>
    python3 quality_report.py <input_file> --before <before_file>  # Compare before/after
    python3 quality_report.py <input_file> --output report.json
"""

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from ai_detector import detect as ai_detect, detect_lang


@dataclass
class SectionCheck:
    name: str
    found: bool
    position: int = -1  # char offset, -1 if not found


@dataclass
class QualityReport:
    file: str = ""
    language: str = "auto"
    
    # Scores (0-100, higher = better except ai_score)
    ai_score: float = 0.0        # AI trace score (lower = better)
    ai_risk: str = "low"
    structure_score: float = 0.0  # Structure completeness
    readability_score: float = 0.0
    overall_quality: float = 0.0  # Weighted composite
    
    # Structure checks
    sections_found: list = field(default_factory=list)
    sections_missing: list = field(default_factory=list)
    
    # Readability metrics
    avg_sentence_len: float = 0.0
    sentence_len_cv: float = 0.0  # coefficient of variation
    ttr: float = 0.0
    total_chars: int = 0
    total_paragraphs: int = 0
    
    # Comparison (if --before provided)
    before_ai_score: float = -1
    improvement: float = 0.0
    
    summary: str = ""


# Standard academic sections (Chinese + English)
SECTION_PATTERNS = {
    "zh": [
        (r"(?:摘要|内容提要|摘\s*要)", "摘要"),
        (r"(?:关键词|关键字|主题词)", "关键词"),
        (r"(?:引言|前言|绪论|研究背景|问题的提出)", "引言"),
        (r"(?:材料与方法|研究对象与方法|资料与方法|方法|实验方法|研究方法)", "方法"),
        (r"(?:结果|研究结果|实验结果|数据结果)", "结果"),
        (r"(?:讨论|分析与讨论|结果讨论)", "讨论"),
        (r"(?:结论|小结|总结|结语)", "结论"),
        (r"(?:参考文献|引用文献|References)", "参考文献"),
    ],
    "en": [
        (r"(?:Abstract|Summary)", "Abstract"),
        (r"(?:Keywords?|Key\s+Words|Index\s+Terms)", "Keywords"),
        (r"(?:Introduction|Background|1\.\s*Introduction)", "Introduction"),
        (r"(?:Methods?|Materials?\s+and\s+Methods?|Methodology|Study\s+Design)", "Methods"),
        (r"(?:Results?|Findings)", "Results"),
        (r"(?:Discussion)", "Discussion"),
        (r"(?:Conclusion|Conclusions?|Summary)", "Conclusion"),
        (r"(?:References?|Bibliography)", "References"),
    ]
}


def check_structure(text: str, lang: str) -> tuple:
    """Check which standard sections are present."""
    patterns = SECTION_PATTERNS.get(lang, SECTION_PATTERNS["en"])
    found = []
    missing = []
    
    for regex, name in patterns:
        m = re.search(regex, text, re.IGNORECASE)
        if m:
            found.append(SectionCheck(name=name, found=True, position=m.start()))
        else:
            missing.append(SectionCheck(name=name, found=False))
    
    return found, missing


def calc_readability(text: str, lang: str) -> dict:
    """Calculate readability metrics."""
    if lang == "zh":
        sentences = re.split(r'[。！？；\n]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        chars = [ch for ch in text if '\u4e00' <= ch <= '\u9fff']
    else:
        sentences = re.split(r'(?<=[.!?])\s+|\n+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        chars = text.split()
    
    if not sentences:
        return {"avg_slen": 0, "cv": 0, "ttr": 0}
    
    lengths = [len(s) for s in sentences]
    avg_slen = sum(lengths) / len(lengths)
    
    if len(lengths) > 1 and avg_slen > 0:
        variance = sum((l - avg_slen) ** 2 for l in lengths) / len(lengths)
        cv = math.sqrt(variance) / avg_slen
    else:
        cv = 0
    
    # TTR
    if lang == "zh":
        tokens = [ch for ch in text if '\u4e00' <= ch <= '\u9fff']
    else:
        tokens = [w.lower() for w in re.findall(r'\b[a-zA-Z]+\b', text)]
    
    ttr = len(set(tokens)) / max(len(tokens), 1)
    
    return {"avg_slen": round(avg_slen, 1), "cv": round(cv, 3), "ttr": round(ttr, 3)}


def generate_report(file_path: str, before_path: str = None) -> QualityReport:
    """Generate comprehensive quality report."""
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    lang = detect_lang(text)
    
    # AI detection
    ai_report = ai_detect(text, lang)
    
    # Structure check
    found, missing = check_structure(text, lang)
    
    # Readability
    rd = calc_readability(text, lang)
    
    # Structure score: based on how many standard sections are present
    total_sections = len(found) + len(missing)
    structure_score = len(found) / max(total_sections, 1) * 100
    
    # Readability score: reward varied sentence length and good TTR
    # CV 0.3-0.6 is ideal (varied but not chaotic)
    cv_score = 100 - abs(rd["cv"] - 0.45) * 200
    cv_score = max(0, min(100, cv_score))
    
    # TTR: 0.4-0.7 is ideal for academic text
    if lang == "zh":
        ttr_score = 100 - abs(rd["ttr"] - 0.55) * 200
    else:
        ttr_score = 100 - abs(rd["ttr"] - 0.60) * 200
    ttr_score = max(0, min(100, ttr_score))
    
    readability_score = (cv_score * 0.5 + ttr_score * 0.5)
    
    # Overall quality (weighted)
    # Higher ai_score = worse, so invert
    ai_quality = 100 - ai_report.overall_ai_score
    overall = ai_quality * 0.4 + structure_score * 0.3 + readability_score * 0.3
    
    # Before/after comparison
    before_ai = -1
    improvement = 0
    if before_path and os.path.exists(before_path):
        with open(before_path, "r", encoding="utf-8") as f:
            before_text = f.read()
        before_report = ai_detect(before_text, lang)
        before_ai = before_report.overall_ai_score
        improvement = before_ai - ai_report.overall_ai_score  # positive = improved
    
    # Build summary
    lines = []
    if lang == "zh":
        lines.append(f"📊 论文质量报告")
        lines.append(f"{'='*40}")
        lines.append(f"AI痕迹: {ai_report.overall_ai_score:.1f}/100 ({'🔴高' if ai_report.overall_risk=='high' else '🟡中' if ai_report.overall_risk=='medium' else '🟢低'}风险)")
        lines.append(f"结构完整性: {structure_score:.0f}%（{len(found)}/{total_sections} 个标准章节）")
        if missing:
            lines.append(f"  缺失章节: {', '.join(s.name for s in missing)}")
        lines.append(f"可读性: {readability_score:.0f}/100")
        lines.append(f"  平均句长: {rd['avg_slen']}字 | 句长变异系数: {rd['cv']:.2f} | 词汇多样性: {rd['ttr']:.2f}")
        lines.append(f"综合评分: {overall:.1f}/100")
        if before_ai >= 0:
            lines.append(f"\n📈 改写对比:")
            lines.append(f"  AI评分: {before_ai:.1f} → {ai_report.overall_ai_score:.1f}（降低 {improvement:.1f} 分）")
            emoji = "✅" if improvement > 0 else "⚠️"
            lines.append(f"  {emoji} {'改善' if improvement > 0 else '未改善'}")
    else:
        lines.append(f"📊 Paper Quality Report")
        lines.append(f"{'='*40}")
        lines.append(f"AI Traces: {ai_report.overall_ai_score:.1f}/100 ({'🔴High' if ai_report.overall_risk=='high' else '🟡Medium' if ai_report.overall_risk=='medium' else '🟢Low'} risk)")
        lines.append(f"Structure: {structure_score:.0f}% ({len(found)}/{total_sections} standard sections)")
        if missing:
            lines.append(f"  Missing: {', '.join(s.name for s in missing)}")
        lines.append(f"Readability: {readability_score:.0f}/100")
        lines.append(f"  Avg sent len: {rd['avg_slen']} | CV: {rd['cv']:.2f} | TTR: {rd['ttr']:.2f}")
        lines.append(f"Overall: {overall:.1f}/100")
        if before_ai >= 0:
            lines.append(f"\n📈 Before/After:")
            lines.append(f"  AI Score: {before_ai:.1f} → {ai_report.overall_ai_score:.1f} ({improvement:+.1f})")
    
    return QualityReport(
        file=file_path,
        language=lang,
        ai_score=round(ai_report.overall_ai_score, 1),
        ai_risk=ai_report.overall_risk,
        structure_score=round(structure_score, 1),
        readability_score=round(readability_score, 1),
        overall_quality=round(overall, 1),
        sections_found=[asdict(s) for s in found],
        sections_missing=[asdict(s) for s in missing],
        avg_sentence_len=rd["avg_slen"],
        sentence_len_cv=rd["cv"],
        ttr=rd["ttr"],
        total_chars=len(text),
        total_paragraphs=len(re.split(r'\n\s*\n|\n', text)),
        before_ai_score=round(before_ai, 1),
        improvement=round(improvement, 1),
        summary="\n".join(lines)
    )


def main():
    parser = argparse.ArgumentParser(description="Quality Report Generator")
    parser.add_argument("input", help="Input text file")
    parser.add_argument("--before", help="Original file for before/after comparison")
    parser.add_argument("--output", help="Output JSON report")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    if args.before and not os.path.exists(args.before):
        print(f"Error: Before file not found: {args.before}", file=sys.stderr)
        sys.exit(1)
    report = generate_report(args.input, args.before)
    report.file = args.input

    if args.format == "json" or args.output:
        output_str = json.dumps(asdict(report), ensure_ascii=False, indent=2)
        if args.output:
            os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_str)
            print(f"Report saved to {args.output}", file=sys.stderr)
        else:
            print(output_str)
    else:
        print(report.summary)


if __name__ == "__main__":
    main()
