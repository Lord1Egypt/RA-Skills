#!/usr/bin/env python3
"""
GPA CLI Wrapper - 简化基因组表型关联分析的调用接口
供 OpenClaw agent 直接使用。

用法:
    python3 scripts/dgra_cli_wrapper.py --variants '[{...}]' --tissue general
    python3 scripts/dgra_cli_wrapper.py --input-file variants.tsv --tissue general

功能:
    1. 将 variant list (JSON) 写入临时 TSV 输入文件
    2. 调用 dgra_core.py 执行分析
    3. 解析 JSON 输出并返回结构化 dict
    4. 失败时返回 error dict,不抛异常
"""

import json
import sys
import tempfile
import csv
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional

# v0.5 P0-1: Unified input parsing layer
from dgra_input_parsers import parse_input, FreeTextParser, auto_detect


# GPA core script path
SCRIPT_DIR = Path(__file__).resolve().parent
GPA_CORE = SCRIPT_DIR / "dgra_core.py"
REFS_DIR = SCRIPT_DIR.parent / "references"

# Required TSV columns
REQUIRED_COLS = [
    "CHROM", "POS", "REF", "ALT", "GENE", "Feature", "EXON",
    "IMPACT", "Consequence", "HGVSp", "HGVSc", "CLIN_SIG",
    "GT", "DP", "GQ", "VAF", "gnomAD_AF", "CLNREVSTAT"
]

# v0.5 P0-7: Missing field sentinel. Critical fields are NOT backfilled with
# false defaults (e.g., IMPACT="MODERATE", VAF="0.5") that systematically
# underestimate risk. Empty strings are passed to core.py, which maps them to
# _UNKNOWN and applies conservative assessment.
OPTIONAL_DEFAULTS = {
    "Feature": "",       # transcript - harmless when missing
    "EXON": "",          # exon info - harmless when missing
    "HGVSp": "",         # protein change - harmless when missing
    "HGVSc": "",         # cDNA change - harmless when missing
    "CLNREVSTAT": "",    # v0.7.2: ClinVar review status - harmless when missing
    # NOTE: The following fields are CRITICAL and are NOT given defaults:
    #   IMPACT, Consequence, CLIN_SIG, VAF, DP, GQ, gnomAD_AF
    # Missing values are written as empty strings and core.py treats them
    # as _UNKNOWN with conservative rules (e.g., UNKNOWN impact → HIGH).
}

# Legacy critical defaults (REMOVED in v0.5 P0-7 - see note above):
#   IMPACT: "MODERATE"    → now empty / UNKNOWN (conservatively treated as HIGH)
#   Consequence: "missense_variant" → now empty / UNKNOWN
#   CLIN_SIG: ""          → unchanged (was already empty)
#   GT: "0/1"            → removed (GT missing means no genotype info)
#   DP: "30"             → now empty / 0 (quality filter skips UNKNOWN)
#   GQ: "99"             → now empty / 0.0 (quality filter skips UNKNOWN)
#   VAF: "0.5"           → now empty / None (no frequency assumption)
#   gnomAD_AF: ""        → unchanged (was already empty)


def _write_tsv(variants: List[Dict[str, Any]], tsv_path: Path) -> None:
    """将 variant dict list 写入 TSV,补全缺失列。
    v0.5 P0-7: 关键字段(IMPACT, Consequence, CLIN_SIG, VAF, DP, GQ, gnomAD_AF)
    缺失时不注入虚假默认值,而是写空字符串,由 core.py 标记为 UNKNOWN
    并应用保守评估规则。
    """
    # Critical fields that must NOT receive synthetic defaults
    CRITICAL_FIELDS = {"IMPACT", "Consequence", "CLIN_SIG", "VAF", "DP", "GQ", "gnomAD_AF", "GT"}

    with open(tsv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=REQUIRED_COLS, delimiter="\t")
        writer.writeheader()
        for v in variants:
            row = {}
            for col in REQUIRED_COLS:
                val = v.get(col)
                if val is None or val == "":
                    if col in CRITICAL_FIELDS:
                        # P0-7: Do NOT backfill critical fields with defaults.
                        # Pass empty string to core.py → _UNKNOWN → conservative assessment.
                        val = ""
                    else:
                        val = OPTIONAL_DEFAULTS.get(col, "")
                row[col] = str(val)
            writer.writerow(row)


def run_gpa_from_file(
    input_path: Path,
    tissue: str = "general",
    user_phenotypes: Optional[str] = None,
    offline: bool = False,
    somatic: bool = False,
    fmt: Optional[str] = None,
    annotation_fmt: Optional[str] = None,
    target_population: Optional[str] = None,
    multi_organ: Optional[List[str]] = None,
    force_sync: bool = False,
    evidence_detail: str = "brief",  # v0.5 P1-9
    database_version: Optional[str] = None,  # v0.5 P1-15
    config_path: Optional[Path] = None,  # v0.5 P2-3
    # v0.7.1: Variant pre-filtering
    filter_preset: Optional[str] = None,
    # v0.7.1: Auto-batch parameters
    auto_batch: bool = True,
    batch_size: int = 500,
    timeout_per_batch: int = 300,
    max_batch_retries: int = 1,
    # v0.8.0: SpliceAI
    spliceai_enabled: bool = False,
    spliceai_concurrency: int = 5,
) -> Dict[str, Any]:
    """
    v0.5 P0-1/P0-2/P1-1: Run GPA from an input file (VCF, Excel, TSV, CSV, or free text).
    Auto-detects format unless fmt is specified. Annotation adapter auto-detects
    unless annotation_fmt is specified.
    v0.5 P1-7: Supports multi_organ multi-organ assessment.
    v0.5 P1-8: Supports force_sync for gene list sync.
    v0.5 P1-9: Supports evidence_detail for evidence chain detail level.
    v0.5 P2-3: Supports config_path for YAML config file.
    """
    try:
        variants = parse_input(input_path, fmt=fmt, annotation_fmt=annotation_fmt)
    except Exception as e:
        return {"success": False, "error": f"Failed to parse {input_path}: {e}"}
    return run_gpa(
        variants=variants,
        tissue=tissue,
        user_phenotypes=user_phenotypes,
        offline=offline,
        somatic=somatic,
        target_population=target_population,
        multi_organ=multi_organ,
        force_sync=force_sync,
        evidence_detail=evidence_detail,
        database_version=database_version,
        config_path=config_path,
        # v0.7.1: variant pre-filtering
        filter_preset=filter_preset,
        # v0.7.1: batch control
        auto_batch=auto_batch,
        batch_size=batch_size,
        timeout_per_batch=timeout_per_batch,
        max_batch_retries=max_batch_retries,
        # v0.8.0: SpliceAI
        spliceai_enabled=spliceai_enabled,
        spliceai_concurrency=spliceai_concurrency,
    )


def run_gpa(
    variants: List[Dict[str, Any]],
    tissue: str = "general",
    user_phenotypes: Optional[str] = None,
    offline: bool = False,
    somatic: bool = False,
    target_population: Optional[str] = None,
    multi_organ: Optional[List[str]] = None,
    force_sync: bool = False,
    evidence_detail: str = "brief",
    database_version: Optional[str] = None,
    config_path: Optional[Path] = None,
    # v0.7.1: Variant pre-filtering
    filter_preset: Optional[str] = None,
    filter_stats: Optional[Dict[str, Any]] = None,
    # v0.7.1: Auto-batch parameters
    auto_batch: bool = True,
    batch_size: int = 500,
    timeout_per_batch: int = 300,
    max_batch_retries: int = 1,
    # v0.8.0: SpliceAI splice-prediction integration (default OFF)
    spliceai_enabled: bool = False,
    spliceai_concurrency: int = 5,
) -> Dict[str, Any]:
    """
    v0.5 P1-1: 运行 GPA 分析管道。
    v0.5 P1-7: 支持 multi_organ 多器官联合评估。
    v0.5 P1-8: 支持 force_sync 强制同步基因列表。
    v0.5 P2-3: 支持 config_path YAML 配置文件。
    v0.7: 支持 user_phenotypes 表型关联分析。

    Args:
        variants: variant dict 列表,每个 dict 至少包含 CHROM, POS, REF, ALT, GENE
        tissue: 组织类型,默认 general (v0.5 P0-6)
        user_phenotypes: 用户临床表型描述，用于基因-表型关联分析
        offline: 是否离线模式(跳过 API)
        target_population: gnomAD 目标人群亚组 (EAS/AMR/AFR/NFE/SAS/ASJ/FIN/MID/OTH)
        multi_organ: 多器官评估 profile 列表(如 ["hematopoietic", "cardiovascular"]),
                      与 tissue 互斥。非 None 时覆盖 tissue 参数。
        force_sync: 强制同步 special_gene_lists(绕过缓存 TTL)
        config_path: YAML 配置文件路径 (v0.5 P2-3)

    Returns:
        dict: {"success": True, "results": {...}, "report_md": "..."}
        或 {"success": False, "error": "..."}
    """
    # v0.7.1: Auto-batch for large variant sets
    if auto_batch and len(variants) > batch_size:
        from dgra_batch_runner import run_gpa_batched
        return run_gpa_batched(
            variants=variants,
            tissue=tissue,
            user_phenotypes=user_phenotypes,
            offline=offline,
            somatic=somatic,
            target_population=target_population,
            evidence_detail=evidence_detail,
            config_path=config_path,
            batch_size=batch_size,
            timeout_per_batch=timeout_per_batch,
            max_retries=max_batch_retries,
        )
    
    if not variants:
        return {"success": False, "error": "variants list is empty"}

    # v0.7.1: Apply variant pre-filtering if requested
    filter_stats_out = None
    if filter_preset:
        from dgra_variant_filter import filter_variants, get_tissue_relevant_genes
        tissue_genes = get_tissue_relevant_genes(tissue)
        variants, filter_stats_out = filter_variants(variants, preset=filter_preset, tissue_relevant_genes=tissue_genes)
        if not variants:
            return {
                "success": False,
                "error": f"All variants filtered out by preset '{filter_preset}'. Stats: {filter_stats_out}",
            }

    # Validate tissue
    valid_tissues = {"general", "hematopoietic", "cardiovascular", "hepatic", "renal", "neurological"}
    if tissue not in valid_tissues:
        return {
            "success": False,
            "error": f"Invalid tissue '{tissue}'. Valid: {', '.join(sorted(valid_tissues))}",
        }

    # Validate multi_organ profiles
    if multi_organ:
        invalid = [p for p in multi_organ if p not in valid_tissues]
        if invalid:
            return {
                "success": False,
                "error": f"Invalid multi-organ profile(s): {', '.join(invalid)}. Valid: {', '.join(sorted(valid_tissues))}",
            }

    # 创建临时文件
    with tempfile.TemporaryDirectory(prefix="dgra_wrapper_") as tmpdir:
        tmp = Path(tmpdir)
        tsv_path = tmp / "variants.tsv"
        json_out = tmp / "results.json"
        md_out = tmp / "report.md"

        # 写输入
        try:
            _write_tsv(variants, tsv_path)
        except Exception as e:
            return {"success": False, "error": f"Failed to write TSV: {e}"}

        # 构造命令行
        cmd = [
            sys.executable,
            str(GPA_CORE),
            "--input", str(tsv_path),
            "--output", str(md_out),
            "--json", str(json_out),
        ]
        if multi_organ:
            cmd.extend(["--multi-organ", ",".join(multi_organ)])
        else:
            cmd.extend(["--tissue", tissue])
        if offline:
            cmd.append("--offline")
        if somatic:
            cmd.append("--somatic")
        if force_sync:
            cmd.append("--sync-gene-lists")
        if target_population:
            cmd.extend(["--target-population", target_population])
        if evidence_detail:
            cmd.extend(["--evidence-detail", evidence_detail])
        if database_version:
            cmd.extend(["--database-version", database_version])
        if user_phenotypes:
            cmd.extend(["--phenotypes", user_phenotypes])
        # v0.7.1: filter stats
        if filter_stats:
            import json as _json
            cmd.extend(["--filter-stats", _json.dumps(filter_stats)])
        if filter_preset:
            cmd.extend(["--filter-preset", filter_preset])
        # v0.5 P2-3: YAML config file
        if config_path:
            cmd.extend(["--config", str(config_path)])
        # v0.8.0: SpliceAI
        if spliceai_enabled:
            cmd.append("--spliceai")
            cmd.extend(["--spliceai-concurrency", str(spliceai_concurrency)])

        # 执行
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 分钟上限
                cwd=str(SCRIPT_DIR),
            )
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "DGRA analysis timed out after 5 minutes"}
        except Exception as e:
            return {"success": False, "error": f"Subprocess failed: {e}"}

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"dgra_core.py exited with code {result.returncode}",
                "stderr": result.stderr,
                "stdout": result.stdout,
            }

        # 解析输出
        try:
            with open(json_out, "r", encoding="utf-8") as f:
                results = json.load(f)
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to parse JSON output: {e}",
                "stdout": result.stdout,
            }

        try:
            with open(md_out, "r", encoding="utf-8") as f:
                report_md = f.read()
        except Exception:
            report_md = ""

        return {
            "success": True,
            "results": results,
            "report_md": report_md,
            "json_report": results.get("json_report", {}),
            "stdout": result.stdout,
            "filter_stats": filter_stats_out,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="GPA CLI Wrapper v0.7")
    # v0.5 P0-1: --input-file and --format replace / augment --variants
    parser.add_argument(
        "--variants",
        help='JSON array of variant dicts, e.g. \'[{"CHROM":"1","POS":12345,"REF":"A","ALT":"G","GENE":"VWF"}]\'',
    )
    parser.add_argument(
        "--input-file", "-i",
        type=Path,
        help="Input file path (.vcf, .vcf.gz, .xlsx, .tsv, .csv, .txt)",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["auto", "vcf", "tsv", "csv", "excel", "freetext"],
        default="auto",
        help="Input file format (default: auto-detect)",
    )
    parser.add_argument(
        "--annotation-format", "-a",
        choices=["auto", "vep", "annovar", "snpeff"],
        default="auto",
        help="Annotation format for TSV/CSV/VCF columns (default: auto-detect from headers)",
    )
    parser.add_argument(
        "--free-text",
        help='Free-text variant description, e.g. "TP53 c.722C>T" or "chr17:7578406C>A"',
    )
    parser.add_argument("--tissue", default="general", help="Tissue profile: general (default), hematopoietic, cardiovascular, hepatic, renal, neurological")
    parser.add_argument("--multi-organ", default=None,
                        help="Multi-organ assessment: comma-separated profiles, e.g. 'hematopoietic,cardiovascular'. "
                             "Mutually exclusive with --tissue. (v0.5 P1-7)")
    parser.add_argument("--target-population", "--population", default=None,
                        choices=["EAS", "AMR", "AFR", "NFE", "SAS", "ASJ", "FIN", "MID", "OTH"],
                        help="Target population for gnomAD subgroup AF classification (v0.5 P1-1). "
                             "When specified, uses that population's AF instead of overall AF.")
    parser.add_argument("--offline", action="store_true", help="Offline mode")
    parser.add_argument("--somatic", action="store_true",
                        help="Somatic mode: tumor driver mutation analysis. "
                             "TSG truncating + oncogene hotspots = Tier 1")
    parser.add_argument("--sync-gene-lists", action="store_true",
                        help="Force sync special_gene_lists from external sources (Orphanet, OMIM) before analysis. "
                             "Bypasses cache TTL. (v0.5 P1-8)")
    parser.add_argument("--evidence-detail", choices=["brief", "full"], default="brief",
                        help="Evidence chain detail level in report: brief (top 3) or full (all). (v0.5 P1-9)")
    parser.add_argument("--database-version",
                        help="Freeze analysis to a specific database version for reproducibility "
                             "(e.g., 'gnomAD v4.1'). Recorded in output meta. (v0.5 P1-15)")
    # v0.7: Phenotype association
    parser.add_argument("--phenotypes", default=None,
                        help="Clinical phenotype description for phenotype-gene association analysis.")
    parser.add_argument("--llm-model", default="gpt-4o-mini",
                        help="LLM model for phenotype semantic matching. Default: gpt-4o-mini.")
    # v0.7.1: Batch control
    parser.add_argument("--no-auto-batch", action="store_true",
                        help="Disable automatic batching for large variant sets (default: auto-batch enabled)")
    parser.add_argument("--batch-size", type=int, default=500,
                        help="Variants per batch when auto-batching (default: 500)")
    parser.add_argument("--timeout", type=int, default=300,
                        help="Timeout per batch in seconds (default: 300)")
    # v0.5 P2-3: YAML config file support
    parser.add_argument("--config", "-c", type=Path, default=None,
                        help="Path to dgra.yaml configuration file. Overrides built-in defaults. (v0.5 P2-3)")
    parser.add_argument("--filter-preset", choices=["strict", "clinical", "broad"], default=None,
                        help="Pre-filter variants before analysis. strict=HIGH/MODERATE only; "
                             "clinical=HIGH/MODERATE + splice + tissue-synonymous (default if set); "
                             "broad=includes LOW. (v0.7.1)")
    parser.add_argument("--spliceai", action="store_true",
                        help="Enable SpliceAI splice-prediction lookup for splice variants. "
                             "Default OFF — only applies to canonical splice (acceptor/donor) and splice_region. "
                             "(v0.8.0)")
    parser.add_argument("--spliceai-concurrency", type=int, default=5,
                        help="Max concurrent SpliceAI API requests (default: 5). (v0.8.0)")
    parser.add_argument("--output-json", help="Write result JSON to this file")

    args = parser.parse_args()

    # v0.5 P1-7: Validate --multi-organ vs --tissue mutual exclusion
    multi_organ = None
    if args.multi_organ:
        if args.tissue != "general":
            # tissue was explicitly set
            print(json.dumps({"success": False, "error": "--tissue and --multi-organ are mutually exclusive. Use one or the other."}, indent=2))
            sys.exit(1)
        multi_organ = [p.strip() for p in args.multi_organ.split(",") if p.strip()]
        if len(multi_organ) < 1 or len(multi_organ) > 3:
            print(json.dumps({"success": False, "error": "--multi-organ requires 1-3 profiles."}, indent=2))
            sys.exit(1)

    # Determine variants source
    variants: Optional[List[Dict[str, Any]]] = None
    input_source = "inline"

    if args.input_file:
        input_source = f"file:{args.input_file}"
    elif args.free_text:
        input_source = f"text:{args.free_text[:40]}"
    elif args.variants:
        input_source = "inline_json"
    else:
        print(json.dumps({"success": False, "error": "No input provided. Use --variants, --input-file, or --free-text."}, indent=2))
        sys.exit(1)

    # Dispatch by input type
    if args.input_file:
        result = run_gpa_from_file(
            input_path=args.input_file,
            tissue=args.tissue,
            user_phenotypes=args.phenotypes,
            offline=args.offline,
            somatic=args.somatic,
            fmt=args.format if args.format != "auto" else None,
            annotation_fmt=args.annotation_format if args.annotation_format != "auto" else None,
            target_population=args.target_population,
            multi_organ=multi_organ,
            force_sync=args.sync_gene_lists,
            evidence_detail=args.evidence_detail,
            database_version=args.database_version,
            config_path=args.config,
            # v0.7.1: variant pre-filtering
            filter_preset=args.filter_preset,
            # v0.7.1: batch control
            auto_batch=not args.no_auto_batch,
            batch_size=args.batch_size,
            timeout_per_batch=args.timeout,
            max_batch_retries=0,
            # v0.8.0: SpliceAI
            spliceai_enabled=args.spliceai,
            spliceai_concurrency=args.spliceai_concurrency,
        )
    elif args.free_text:
        try:
            ftp = FreeTextParser()
            variants = ftp.parse_text(args.free_text)
        except Exception as e:
            print(json.dumps({"success": False, "error": f"Failed to parse free text: {e}"}, indent=2))
            sys.exit(1)
        result = run_gpa(
            variants=variants,
            tissue=args.tissue,
            user_phenotypes=args.phenotypes,
            offline=args.offline,
            somatic=args.somatic,
            target_population=args.target_population,
            multi_organ=multi_organ,
            force_sync=args.sync_gene_lists,
            evidence_detail=args.evidence_detail,
            database_version=args.database_version,
            config_path=args.config,
            # v0.7.1: variant pre-filtering
            filter_preset=args.filter_preset,
            # v0.7.1: batch control
            auto_batch=not args.no_auto_batch,
            batch_size=args.batch_size,
            timeout_per_batch=args.timeout,
            max_batch_retries=0,
            # v0.8.0: SpliceAI
            spliceai_enabled=args.spliceai,
            spliceai_concurrency=args.spliceai_concurrency,
        )
    else:
        # Inline JSON variants
        try:
            variants = json.loads(args.variants)
        except json.JSONDecodeError as e:
            print(json.dumps({"success": False, "error": f"Invalid variants JSON: {e}"}, indent=2))
            sys.exit(1)
        result = run_gpa(
            variants=variants,
            tissue=args.tissue,
            user_phenotypes=args.phenotypes,
            offline=args.offline,
            somatic=args.somatic,
            target_population=args.target_population,
            multi_organ=multi_organ,
            force_sync=args.sync_gene_lists,
            evidence_detail=args.evidence_detail,
            database_version=args.database_version,
            config_path=args.config,
            # v0.7.1: variant pre-filtering
            filter_preset=args.filter_preset,
            # v0.7.1: batch control
            auto_batch=not args.no_auto_batch,
            batch_size=args.batch_size,
            timeout_per_batch=args.timeout,
            max_batch_retries=0,
            # v0.8.0: SpliceAI
            spliceai_enabled=args.spliceai,
            spliceai_concurrency=args.spliceai_concurrency,
        )
    
    output = json.dumps(result, indent=2, ensure_ascii=False, default=str)

    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
