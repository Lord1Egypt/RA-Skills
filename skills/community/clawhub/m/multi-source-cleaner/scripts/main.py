#!/usr/bin/env python3
"""
Multi-Source Data Cleanser — main orchestrator.

Usage (CLI):
    python main.py clean --input data.xlsx --output cleaned.xlsx
    python main.py merge --sources data1.csv data2.csv --on "手机号" --output merged.csv
    python main.py report --input cleaned.xlsx --output report.md

Usage (import):
    from main import run_clean_pipeline
    result = run_clean_pipeline("data.xlsx")
"""

import os
import sys
import json
import argparse
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Any

import pandas as pd

# ─── Import skill modules ───────────────────────────────────────────────────────

from parser          import parse_file, parse_text, load_sources
from field_identifier import identify_fields, FieldType, FieldInfo
from cleaner         import DataCleaner, clean_dataframe, CleaningReport
from classifier      import DataClassifier, ClassificationReport
from merger          import DataMerger, MergeResult
from reporter        import DataQualityReporter
from output          import DataExporter
from tier_limits     import (
    Tier, get_user_tier, check_feature, check_tier, record_usage,
    get_usage_summary, tier_display_name, FeatureNotAvailable,
    TierLimitExceeded,
)

# ─── Tier-based feature availability check ────────────────────────────────────

def _resolve_tier(tier_name: Optional[str]) -> Tier:
    if tier_name:
        try:
            return Tier(tier_name.lower())
        except ValueError:
            pass
    return get_user_tier()

# ─── Main pipeline ─────────────────────────────────────────────────────────────

def run_clean_pipeline(
    sources: Optional[List[str]] = None,
    texts:  Optional[List[str]] = None,
    *,
    tier: Optional[str] = None,
    output_format: str = "xlsx",
    output_path: Optional[str] = None,
    custom_field_mapping: Optional[Dict[str, str]] = None,
    dedup_strategy: str = "auto",
    fill_strategy: str = "auto",
    classify: bool = False,
    ai_model: Optional[str] = None,
    generate_report: bool = True,
    bitable_output: bool = False,
    feishu_open_id: Optional[str] = None,
    feishu_folder_token: Optional[str] = None,
    report_title: str = "数据质量报告",
) -> Dict[str, Any]:
    """
    Full cleaning pipeline.

    Parameters
    ----------
    sources         : list of file paths
    texts           : list of pasted text blocks
    tier            : subscription tier override (free/basic/std/pro)
    output_format   : "xlsx" | "csv"
    output_path     : output file path
    custom_field_mapping : {col_name: field_type} overrides
    dedup_strategy  : "exact" | "fuzzy" | "auto"
    fill_strategy   : "auto" | "mean" | "mode" | "leave_blank"
    classify        : whether to run AI classification
    ai_model        : "minimax" or "deepseek" for AI features
    generate_report : whether to generate quality report
    bitable_output  : write to Feishu Bitable (PRO only)
    feishu_open_id  : user's Feishu open_id
    feishu_folder_token : Feishu folder token for doc output
    report_title    : title for the quality report document

    Returns
    -------
    Dict with keys:
      cleaned_df, report_md, report_dict,
      file_path, bitable_result, doc_result, tier, usage_summary
    """
    t = _resolve_tier(tier)
    result: Dict[str, Any] = {"tier": tier_display_name(t)}

    # ── Load sources ────────────────────────────────────────────────────────────
    src_list = sources or []
    if not src_list and not (texts or []):
        raise ValueError("请提供至少一个数据源（文件路径或粘贴文本）。")

    # Tier: check max sources
    n_sources = len(src_list) + len(texts or [])
    check_tier(t, sources=n_sources)

    raw_sources = load_sources(src_list, texts)

    if len(raw_sources) == 1:
        raw_name, raw_df = raw_sources[0]
    else:
        # Multiple sources → merge first
        merger = DataMerger(raw_sources)
        try:
            merge_result = merger.merge(how="outer")
        except Exception:
            # Fallback: concatenate
            raw_df = pd.concat([df for _, df in raw_sources], ignore_index=True)
            raw_name = "+".join([n for n, _ in raw_sources])
            merge_result = None
        else:
            raw_df = merge_result.df
            raw_name = f"{merge_result.left_name}+{merge_result.right_name}"

    # Tier: check columns
    check_tier(t, columns=len(raw_df.columns))

    # ── Identify fields ────────────────────────────────────────────────────────
    field_info = identify_fields(
        raw_df,
        custom_rules=custom_field_mapping,
        ai_model=ai_model,
    )

    # ── Clean ──────────────────────────────────────────────────────────────────
    check_tier(t, rows=len(raw_df))
    df_clean, clean_report = clean_dataframe(
        raw_df,
        field_info,
        dedup_strategy=dedup_strategy,
        fill_strategy=fill_strategy,
    )

    # ── Classify (PRO only) ────────────────────────────────────────────────────
    class_report: Optional[ClassificationReport] = None
    if classify:
        try:
            check_feature(t, "ai_classification")
        except FeatureNotAvailable:
            pass  # Silently skip if tier doesn't support
        else:
            clf = DataClassifier(field_info, use_ai=(ai_model is not None))
            df_clean, _, class_report = clf.classify_with_ai(df_clean)

    # ── Export cleaned data ───────────────────────────────────────────────────
    exporter = DataExporter(df_clean, field_info, tier=t.value)

    if output_format == "csv":
        out_path = output_path or tempfile.mktemp(suffix=".csv")
        file_path = exporter.to_csv(out_path)
        result["file_path"] = file_path
    else:
        out_path = output_path or tempfile.mktemp(suffix=".xlsx")
        file_path = exporter.to_excel(out_path)
        result["file_path"] = file_path

    result["cleaned_rows"] = len(df_clean)
    result["cleaned_columns"] = len(df_clean.columns)

    # ── Record usage ──────────────────────────────────────────────────────────
    usage = record_usage(rows=len(raw_df))
    result["usage"] = get_usage_summary(t)

    # ── Bitable output (PRO only) ─────────────────────────────────────────────
    bitable_result: Optional[Dict] = None
    if bitable_output:
        try:
            check_feature(t, "bitable_output")
            bitable_result = exporter.to_bitable(
                table_name="清洗结果",
                folder_token=feishu_folder_token,
                open_id=feishu_open_id,
            )
            result["bitable"] = bitable_result
        except FeatureNotAvailable:
            result["bitable_error"] = "飞书多维表格导出仅限专业版使用。"
        except ExportError as e:
            result["bitable_error"] = str(e)

    # ── Quality report ────────────────────────────────────────────────────────
    report_md: Optional[str] = None
    doc_result: Optional[Dict] = None

    if generate_report:
        try:
            check_feature(t, "data_quality_report")
        except FeatureNotAvailable:
            # Still generate dict report
            reporter = DataQualityReporter(
                raw_df, df_clean, field_info,
                source_name=raw_name,
                tier=tier_display_name(t),
                cleaning_report=clean_report,
                classification_report=class_report,
            )
            report = reporter.generate()
            result["report_dict"] = reporter.to_dict(report)
        else:
            reporter = DataQualityReporter(
                raw_df, df_clean, field_info,
                source_name=raw_name,
                tier=tier_display_name(t),
                cleaning_report=clean_report,
                classification_report=class_report,
            )
            report = reporter.generate()
            report_md = reporter.to_markdown(report)
            result["report_md"] = report_md
            result["report_dict"] = reporter.to_dict(report)

            # Create Feishu doc
            try:
                doc_result = exporter.to_feishu_doc(
                    report_markdown=report_md,
                    title=report_title,
                    folder_token=feishu_folder_token,
                )
                result["doc"] = doc_result
            except ExportError as e:
                result["doc_error"] = str(e)

    result["clean_report"] = {
        "original_rows":    clean_report.original_rows,
        "cleaned_rows":     clean_report.cleaned_rows,
        "duplicates_removed": clean_report.duplicates_removed,
        "missing_filled":   clean_report.missing_filled,
        "formatted_cells":  clean_report.formatted_cells,
    }

    return result


# ─── Standalone merge pipeline ─────────────────────────────────────────────────

def run_merge_pipeline(
    sources: List[str],
    on: Optional[List[str]] = None,
    fuzzy_on: Optional[List[str]] = None,
    *,
    tier: Optional[str] = None,
    output_format: str = "xlsx",
    output_path: Optional[str] = None,
    fuzzy_threshold: int = 85,
) -> Dict[str, Any]:
    """
    Multi-source merge pipeline.

    Parameters
    ----------
    sources         : list of file paths (2 or more)
    on              : list of column names for exact join
    fuzzy_on        : list of column names for fuzzy join
    fuzzy_threshold : fuzzy match score threshold (0-100)
    """
    t = _resolve_tier(tier)
    check_feature(t, "fuzzy_join")

    raw_sources = load_sources(sources)
    merger = DataMerger(raw_sources)

    # Build (left_col, right_col) pairs
    on_pairs = []
    fuzzy_pairs = []
    if on:
        for col in on:
            on_pairs.append((col, col))
    if fuzzy_on:
        for col in fuzzy_on:
            fuzzy_pairs.append((col, col))

    merge_result = merger.merge(
        how="outer",
        on=on_pairs or None,
        fuzzy_on=fuzzy_pairs or None,
        fuzzy_threshold=fuzzy_threshold,
    )

    # Clean merged result
    field_info = identify_fields(merge_result.df)
    df_clean, clean_report = clean_dataframe(merge_result.df, field_info)

    # Export
    exporter = DataExporter(df_clean, field_info, tier=t.value)
    out_path = output_path or tempfile.mktemp(suffix=f".{output_format}")
    if output_format == "csv":
        file_path = exporter.to_csv(out_path)
    else:
        file_path = exporter.to_excel(out_path)

    usage = record_usage(rows=len(merge_result.df))

    return {
        "file_path":      file_path,
        "merge_summary":  merge_result.summary(),
        "clean_report":   {
            "original_rows":    clean_report.original_rows,
            "cleaned_rows":     clean_report.cleaned_rows,
            "duplicates_removed": clean_report.duplicates_removed,
        },
        "tier":   tier_display_name(t),
        "usage":  get_usage_summary(t),
    }


# ─── CLI entry point ───────────────────────────────────────────────────────────

def _cli():
    parser = argparse.ArgumentParser(
        description="多源数据清洗器 - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    # clean
    c = sub.add_parser("clean", help="清洗数据")
    c.add_argument("--input",   "-i", help="输入文件路径")
    c.add_argument("--output",  "-o", help="输出文件路径")
    c.add_argument("--format",  "-f", default="xlsx",
                   choices=["xlsx", "csv"],
                   help="输出格式（默认 xlsx）")
    c.add_argument("--tier",          default=None)
    c.add_argument("--dedup",         default="auto",
                   choices=["exact", "fuzzy", "auto"])
    c.add_argument("--fill",          default="auto",
                   choices=["auto", "mean", "mode", "leave_blank"])
    c.add_argument("--classify",      action="store_true")
    c.add_argument("--ai",            default=None,
                   choices=["minimax", "deepseek"])
    c.add_argument("--no-report",     action="store_true")
    c.add_argument("--text",         "-t", help="粘贴文本（会覆盖 --input）")
    c.add_argument("--report-title", default="数据质量报告")

    args = parser.parse_args()

    kwargs = dict(
        tier=args.tier,
        output_format=args.format,
        output_path=args.output,
        dedup_strategy=args.dedup,
        fill_strategy=args.fill,
        classify=args.classify,
        ai_model=args.ai,
        generate_report=not args.no_report,
        report_title=args.report_title,
    )

    if args.text:
        kwargs["texts"] = [args.text]
    elif args.input:
        kwargs["sources"] = [args.input]
    else:
        print("错误：必须提供 --input 或 --text", file=sys.stderr)
        sys.exit(1)

    result = run_clean_pipeline(**kwargs)

    print("\n✅ 清洗完成！")
    print(f"输出文件：{result.get('file_path')}")
    print(f"清洗后行数：{result.get('cleaned_rows', '?')}")
    print(f"版本：{result.get('tier')}")
    print(f"本月已用：{result.get('usage', {}).get('rows_used', '?')} 条")
    if "bitable" in result:
        print(f"飞书多维表格：{result['bitable']['url']}")
    if "doc" in result:
        print(f"质量报告文档：{result['doc']['url']}")


if __name__ == "__main__":
    _cli()
