#!/usr/bin/env python3
"""
lunheng RAG Pipeline v2
案情输入 → 要素解析 → 并行检索 → 三段论组装 → 判决草稿

重构于 2026-07-18：从 1701 行拆分为 4 个模块
- parser.py    — 要素解析
- retriever.py — 并行检索
- assembler.py — 三段论组装
- formatter.py — 输出格式化

本文件保留为入口 + 向后兼容（consistency_checker 从 pipeline 导入）
"""

import json
import sys
from dataclasses import asdict
from pathlib import Path

# ─── 从拆分模块导入 ────────────────────────────────────
from parser import (
    CaseElements,
    parse_case_elements,
    CAUSE_LAW_MAP,
)

from retriever import (
    RetrievalResult,
    retrieve_all,
    ima_search,
    KB_CASES,
    KB_LEGAL,
    _filter_case_results,
)

from assembler import (
    JudgmentDraft,
    assemble_judgment,
)

from formatter import (
    format_judgment_text,
    format_judgment_markdown,
    format_judgment_html,
    format_judgment_docx,
)

# ─── 可选模块导入 ──────────────────────────────────────
try:
    from law_checker import check_law_references, LawCheckResult
except ImportError:
    LawCheckResult = None
    def check_law_references(text, cause=''): return None

try:
    from quality_checker import check_quality, QualityReport
except ImportError:
    QualityReport = None
    def check_quality(text, cause='', elements=None): return None

try:
    from consistency_checker import check_consistency, ConsistencyReport
except ImportError:
    ConsistencyReport = None
    def check_consistency(elements, draft_verdict='', cause=''): return None

try:
    from fee_calculator import calculate_fee
except ImportError:
    def calculate_fee(case_type='财产', amount=0, **kw): return None


# ─── 主函数 ────────────────────────────────────────────
def run_pipeline(
    case_text: str,
    cause: str = "",
    output_format: str = "markdown",
) -> dict:
    """
    运行完整的 RAG Pipeline。

    Returns:
        {
            "elements": CaseElements dict,
            "retrieval": {source: [RetrievalResult]},
            "draft": JudgmentDraft dict,
            "formatted": str,
        }
    """
    print("=" * 60, file=sys.stderr)
    print("⚖️  论衡 RAG Pipeline v2", file=sys.stderr)
    print("=" * 60, file=sys.stderr)

    # Step 1: 要素解析
    print("\n📋 Step 1: 解析案情要素...", file=sys.stderr)
    elements = parse_case_elements(case_text, cause)
    print(f"   案由: {elements.cause}", file=sys.stderr)
    print(f"   当事人: {elements.parties}", file=sys.stderr)
    print(f"   争议焦点: {len(elements.disputes)} 个", file=sys.stderr)
    print(f"   关键事实: {len(elements.facts)} 条", file=sys.stderr)
    print(f"   法律问题: {elements.legal_issues}", file=sys.stderr)
    print(f"   适用法条: {elements.applicable_laws}", file=sys.stderr)

    # Step 2: 并行检索
    print("\n🔍 Step 2: 并行检索...", file=sys.stderr)
    retrieval = retrieve_all(elements)

    # Step 3: 三段论组装
    print("\n📝 Step 3: 三段论组装...", file=sys.stderr)
    draft = assemble_judgment(elements, retrieval)

    # Step 4: 格式化输出
    if output_format == "html":
        formatted = format_judgment_html(draft)
    elif output_format == "text":
        formatted = format_judgment_text(draft)
    elif output_format == "docx":
        # DOCX 需要输出路径，先用 markdown 作为 formatted
        formatted = format_judgment_markdown(draft)
    else:
        formatted = format_judgment_markdown(draft)

    # Step 5: 质量校验
    print("\n📊 Step 4: 质量校验...", file=sys.stderr)

    law_check = check_law_references(formatted, elements.cause)
    if law_check:
        print(f"   📜 法条校验: {law_check.valid_refs}/{law_check.total_refs} 有效, 得分 {law_check.score:.0f}", file=sys.stderr)
        for w in law_check.warnings[:3]:
            print(f"      {w}", file=sys.stderr)

    quality_check = check_quality(formatted, elements.cause, asdict(elements))
    if quality_check:
        print(f"   📋 质量检查: {quality_check.passed_checks}/{quality_check.total_checks} 通过, 得分 {quality_check.score:.0f}", file=sys.stderr)
        if quality_check.errors > 0:
            print(f"      ❌ {quality_check.errors} 个严重问题", file=sys.stderr)

    consistency_check = check_consistency(
        asdict(elements),
        draft.verdict_section,
        elements.cause,
    )
    if consistency_check:
        print(f"   📊 一致性检查: {consistency_check.similar_cases_count} 件类案, 得分 {consistency_check.score:.0f}", file=sys.stderr)

    print(f"\n✅ Pipeline 完成", file=sys.stderr)
    print(f"   草稿长度: {len(formatted)} 字符", file=sys.stderr)
    if draft.warnings:
        print(f"   ⚠️  {len(draft.warnings)} 条注意事项", file=sys.stderr)

    all_warnings = list(draft.warnings)
    if law_check:
        all_warnings.extend(law_check.warnings)
    if quality_check:
        all_warnings.extend([f"[质量]{i.message}" for i in quality_check.items if not i.passed and i.severity == 'error'])
    if consistency_check:
        all_warnings.extend(consistency_check.warnings)

    return {
        "elements": asdict(elements),
        "retrieval": {
            k: [asdict(r) for r in v] for k, v in retrieval.items()
        },
        "draft": asdict(draft),
        "draft_obj": draft,  # 供 DOCX 格式化使用
        "formatted": formatted,
        "law_check": {
            "score": law_check.score,
            "valid_refs": law_check.valid_refs,
            "total_refs": law_check.total_refs,
            "warnings": law_check.warnings,
            "missing_laws": law_check.missing_laws,
        } if law_check else None,
        "quality_check": {
            "score": quality_check.score,
            "passed": quality_check.passed_checks,
            "total": quality_check.total_checks,
            "errors": quality_check.errors,
            "warnings": quality_check.warnings,
            "summary": quality_check.summary,
        } if quality_check else None,
        "consistency_check": {
            "score": consistency_check.score,
            "similar_cases": consistency_check.similar_cases_count,
            "amount_deviation": consistency_check.amount_deviation,
            "warnings": consistency_check.warnings,
            "summary": consistency_check.summary,
        } if consistency_check else None,
        "all_warnings": all_warnings,
    }


# ─── CLI ───────────────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(description="论衡 RAG Pipeline v2")
    parser.add_argument("--input", "-i", help="案情描述文本")
    parser.add_argument("--file", "-f", help="案情描述文件路径")
    parser.add_argument("--stdin", action="store_true", help="从 stdin 读取案情")
    parser.add_argument("--cause", "-c", help="案由(可选,自动识别)")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--format", choices=["markdown", "text", "html", "docx"], default="markdown")
    parser.add_argument("--json", action="store_true", help="输出完整 JSON")
    args = parser.parse_args()

    case_text = ""
    if args.input:
        case_text = args.input
    elif args.file:
        raw_text = Path(args.file).read_text(encoding="utf-8")
        # 尝试解析 JSON 格式的案情文件
        try:
            case_data = json.loads(raw_text)
            # 如果是结构化 JSON，转换为文本格式
            if isinstance(case_data, dict) and "facts" in case_data:
                parts = []
                if case_data.get("cause"):
                    parts.append(f"案由：{case_data['cause']}")
                if case_data.get("parties"):
                    p = case_data["parties"]
                    if p.get("plaintiff"):
                        parts.append(f"原告：{p['plaintiff']}")
                    if p.get("defendant"):
                        parts.append(f"被告：{p['defendant']}")
                if case_data.get("facts"):
                    parts.append("案情描述：")
                    parts.extend(case_data["facts"])
                if case_data.get("claims"):
                    parts.append("诉讼请求：")
                    parts.extend(case_data["claims"])
                if case_data.get("evidence"):
                    parts.append("证据：")
                    parts.extend(case_data["evidence"])
                case_text = "\n".join(parts)
            else:
                case_text = raw_text
        except json.JSONDecodeError:
            case_text = raw_text
    elif args.stdin:
        case_text = sys.stdin.read()
    else:
        print("请提供案情描述:--input, --file, 或 --stdin")
        sys.exit(1)

    result = run_pipeline(case_text, args.cause, args.format)

    if args.json:
        output = json.dumps(result, ensure_ascii=False, indent=2)
    else:
        output = result["formatted"]

    if args.output:
        if args.format == "docx" and not args.output.endswith(".docx"):
            args.output += ".docx"
        if args.format == "docx":
            format_judgment_docx(result["draft_obj"], args.output)
            print(f"\n📄 已保存到: {args.output}", file=sys.stderr)
        else:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"\n📄 已保存到: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
