#!/usr/bin/env python3
"""
GPA Batch Runner - 自动分批执行 GPA 分析，避免超时

策略：
1. 当变异数 > batch_size 时，自动按 batch_size 切分
2. 每批独立调用 dgra_core.py，有独立的 5 分钟超时
3. 合并结果时保留 tier 结构、multi-hit 标记、表型匹配
4. 支持 --resume 从失败的批次继续

用法:
    python3 scripts/dgra_batch_runner.py --input-file variants.tsv --tissue neurological --batch-size 500
"""

import json
import sys
import tempfile
import csv
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

SCRIPT_DIR = Path(__file__).resolve().parent
GPA_CORE = SCRIPT_DIR / "dgra_core.py"
WRAPPER = SCRIPT_DIR / "dgra_cli_wrapper.py"

def _write_tsv(variants: List[Dict[str, Any]], tsv_path: Path) -> None:
    REQUIRED_COLS = [
        "CHROM", "POS", "REF", "ALT", "GENE", "Feature", "EXON",
        "IMPACT", "Consequence", "HGVSp", "HGVSc", "CLIN_SIG",
        "GT", "DP", "GQ", "VAF", "gnomAD_AF"
    ]
    OPTIONAL_DEFAULTS = {
        "Feature": "", "EXON": "", "HGVSp": "", "HGVSc": "",
    }
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
                        val = ""
                    else:
                        val = OPTIONAL_DEFAULTS.get(col, "")
                row[col] = str(val)
            writer.writerow(row)


def run_batch(
    variants: List[Dict[str, Any]],
    tissue: str,
    user_phenotypes: Optional[str] = None,
    offline: bool = False,
    somatic: bool = False,
    target_population: Optional[str] = None,
    evidence_detail: str = "brief",
    config_path: Optional[Path] = None,
    timeout: int = 300,
    batch_id: int = 0,
) -> Dict[str, Any]:
    """Run a single batch of variants through GPA core."""
    
    with tempfile.TemporaryDirectory(prefix=f"dgra_batch_{batch_id}_") as tmpdir:
        tmp = Path(tmpdir)
        tsv_path = tmp / "variants.tsv"
        json_out = tmp / "results.json"
        md_out = tmp / "report.md"

        _write_tsv(variants, tsv_path)

        cmd = [
            sys.executable, str(GPA_CORE),
            "--input", str(tsv_path),
            "--output", str(md_out),
            "--json", str(json_out),
        ]
        if tissue:
            cmd.extend(["--tissue", tissue])
        if offline:
            cmd.append("--offline")
        if somatic:
            cmd.append("--somatic")
        if target_population:
            cmd.extend(["--target-population", target_population])
        if evidence_detail:
            cmd.extend(["--evidence-detail", evidence_detail])
        if user_phenotypes:
            cmd.extend(["--phenotypes", user_phenotypes])
        if config_path:
            cmd.extend(["--config", str(config_path)])

        try:
            start = time.time()
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=timeout, cwd=str(SCRIPT_DIR),
            )
            elapsed = time.time() - start
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Batch {batch_id} timed out after {timeout}s",
                "batch_id": batch_id,
                "variant_count": len(variants),
            }

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"Batch {batch_id} exited with code {result.returncode}",
                "stderr": result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr,
                "stdout": result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout,
                "batch_id": batch_id,
            }

        try:
            with open(json_out, "r", encoding="utf-8") as f:
                results = json.load(f)
        except Exception as e:
            return {
                "success": False,
                "error": f"Batch {batch_id} JSON parse failed: {e}",
                "batch_id": batch_id,
            }

        return {
            "success": True,
            "results": results,
            "batch_id": batch_id,
            "variant_count": len(variants),
            "elapsed_seconds": round(elapsed, 1),
        }


def merge_batch_results(batch_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Merge multiple batch results into a single report."""
    
    # Collect all variants by tier
    tier1_all = []
    tier2_all = []
    tier3_all = []
    all_meta = []
    total_time = 0
    total_variants = 0
    
    # Track gene-variant mapping for multi-hit recalculation
    gene_variants = {}  # gene -> set of variant signatures
    
    for br in batch_results:
        if not br.get("success"):
            continue
        results = br["results"]
        total_variants += br.get("variant_count", 0)
        total_time += br.get("elapsed_seconds", 0)
        
        # Track meta
        if "meta" in results:
            all_meta.append(results["meta"])
        
        # Collect variants
        for v in results.get("tier1_variants", []):
            sig = f"{v.get('chrom', v.get('CHROM', ''))}:{v.get('pos', v.get('POS', ''))}:{v.get('ref', v.get('REF', ''))}>{v.get('alt', v.get('ALT', ''))}"
            if sig not in {f"{x.get('chrom', x.get('CHROM', ''))}:{x.get('pos', x.get('POS', ''))}:{x.get('ref', x.get('REF', ''))}>{x.get('alt', x.get('ALT', ''))}" for x in tier1_all}:
                tier1_all.append(v)
            gene = v.get("gene", v.get("GENE", ""))
            if gene:
                gene_variants.setdefault(gene, set()).add(sig)
                
        for v in results.get("tier2_variants", []):
            sig = f"{v.get('chrom', v.get('CHROM', ''))}:{v.get('pos', v.get('POS', ''))}:{v.get('ref', v.get('REF', ''))}>{v.get('alt', v.get('ALT', ''))}"
            if sig not in {f"{x.get('chrom', x.get('CHROM', ''))}:{x.get('pos', x.get('POS', ''))}:{x.get('ref', x.get('REF', ''))}>{x.get('alt', x.get('ALT', ''))}" for x in tier1_all + tier2_all}:
                tier2_all.append(v)
            gene = v.get("gene", v.get("GENE", ""))
            if gene:
                gene_variants.setdefault(gene, set()).add(sig)
                
        for v in results.get("tier3_variants", []):
            sig = f"{v.get('chrom', v.get('CHROM', ''))}:{v.get('pos', v.get('POS', ''))}:{v.get('ref', v.get('REF', ''))}>{v.get('alt', v.get('ALT', ''))}"
            # Only include tier3 if not already in tier1/2
            existing = {f"{x.get('chrom', x.get('CHROM', ''))}:{x.get('pos', x.get('POS', ''))}:{x.get('ref', x.get('REF', ''))}>{x.get('alt', x.get('ALT', ''))}" for x in tier1_all + tier2_all}
            if sig not in existing:
                tier3_all.append(v)
            gene = v.get("gene", v.get("GENE", ""))
            if gene:
                gene_variants.setdefault(gene, set()).add(sig)
    
    # Recalculate multi-hit: genes with >=2 distinct variants
    multi_hit_genes = [g for g, sigs in gene_variants.items() if len(sigs) >= 2]
    
    # Build merged result
    merged = {
        "success": True,
        "results": {
            "meta": {
                "analysis_date": all_meta[0].get("analysis_date", "") if all_meta else "",
                "total_variants": total_variants,
                "batch_count": len(batch_results),
                "batch_details": [
                    {
                        "batch_id": br.get("batch_id"),
                        "variant_count": br.get("variant_count"),
                        "elapsed_seconds": br.get("elapsed_seconds"),
                        "success": br.get("success"),
                    }
                    for br in batch_results
                ],
                "total_elapsed_seconds": total_time,
                "offline_mode": all_meta[0].get("offline_mode", False) if all_meta else False,
            },
            "summary": {
                "tier1_gene_count": len(set(v.get("gene", v.get("GENE", "")) for v in tier1_all)),
                "tier1_variant_count": len(tier1_all),
                "tier2_gene_count": len(set(v.get("gene", v.get("GENE", "")) for v in tier2_all)),
                "tier2_variant_count": len(tier2_all),
                "tier3_gene_count": len(set(v.get("gene", v.get("GENE", "")) for v in tier3_all)),
                "tier3_variant_count": len(tier3_all),
                "multi_hit_genes": sorted(multi_hit_genes),
            },
            "tier1_variants": tier1_all,
            "tier2_variants": tier2_all,
            "tier3_variants": tier3_all,
        },
        "report_md": f"""# GPA Batch Analysis Report

## Summary
- Total variants analyzed: {total_variants}
- Batches: {len(batch_results)}
- Total time: {total_time:.1f}s

| Tier | Genes | Variants |
|------|-------|----------|
| Tier 1 | {len(set(v.get('gene', v.get('GENE', '')) for v in tier1_all))} | {len(tier1_all)} |
| Tier 2 | {len(set(v.get('gene', v.get('GENE', '')) for v in tier2_all))} | {len(tier2_all)} |
| Tier 3 | {len(set(v.get('gene', v.get('GENE', '')) for v in tier3_all))} | {len(tier3_all)} |

Multi-hit genes: {', '.join(sorted(multi_hit_genes)) if multi_hit_genes else 'None'}

## Batch Details
""" + "\n".join(
    f"- Batch {br.get('batch_id')}: {br.get('variant_count')} variants, {br.get('elapsed_seconds', 0):.1f}s, {'OK' if br.get('success') else 'FAILED: ' + br.get('error', '')}"
    for br in batch_results
        ),
    }
    
    return merged


def run_gpa_batched(
    variants: List[Dict[str, Any]],
    tissue: str = "general",
    user_phenotypes: Optional[str] = None,
    offline: bool = False,
    somatic: bool = False,
    target_population: Optional[str] = None,
    evidence_detail: str = "brief",
    config_path: Optional[Path] = None,
    batch_size: int = 500,
    timeout_per_batch: int = 300,
    max_retries: int = 1,
) -> Dict[str, Any]:
    """Run GPA with automatic batching for large variant sets."""
    
    if not variants:
        return {"success": False, "error": "variants list is empty"}
    
    # Validate tissue
    valid_tissues = {"general", "hematopoietic", "cardiovascular", "hepatic", "renal", "neurological"}
    if tissue not in valid_tissues:
        return {"success": False, "error": f"Invalid tissue '{tissue}'. Valid: {', '.join(sorted(valid_tissues))}"}
    
    # If small enough, run single batch
    if len(variants) <= batch_size:
        return run_batch(
            variants=variants, tissue=tissue, user_phenotypes=user_phenotypes,
            offline=offline, somatic=somatic, target_population=target_population,
            evidence_detail=evidence_detail, config_path=config_path,
            timeout=timeout_per_batch, batch_id=0,
        )
    
    # Large set: split into batches
    print(f"[GPA Batch] {len(variants)} variants > {batch_size} threshold, splitting into batches...", file=sys.stderr)
    
    batch_results = []
    failed_batches = []
    
    for i in range(0, len(variants), batch_size):
        batch_variants = variants[i:i+batch_size]
        batch_id = i // batch_size + 1
        total_batches = (len(variants) + batch_size - 1) // batch_size
        
        print(f"[GPA Batch] Running batch {batch_id}/{total_batches} ({len(batch_variants)} variants)...", file=sys.stderr)
        
        for attempt in range(max_retries + 1):
            result = run_batch(
                variants=batch_variants, tissue=tissue, user_phenotypes=user_phenotypes,
                offline=offline, somatic=somatic, target_population=target_population,
                evidence_detail=evidence_detail, config_path=config_path,
                timeout=timeout_per_batch, batch_id=batch_id,
            )
            
            if result.get("success"):
                print(f"[GPA Batch] Batch {batch_id} completed in {result.get('elapsed_seconds', 0):.1f}s", file=sys.stderr)
                batch_results.append(result)
                break
            else:
                if attempt < max_retries:
                    print(f"[GPA Batch] Batch {batch_id} failed (attempt {attempt+1}), retrying...", file=sys.stderr)
                    time.sleep(2)
                else:
                    print(f"[GPA Batch] Batch {batch_id} FAILED after {max_retries+1} attempts: {result.get('error')}", file=sys.stderr)
                    failed_batches.append(result)
                    batch_results.append(result)  # Include failed batch for reporting
    
    # Check if any batches succeeded
    successful = [br for br in batch_results if br.get("success")]
    if not successful:
        return {
            "success": False,
            "error": f"All {len(batch_results)} batches failed. Last error: {batch_results[-1].get('error', 'unknown')}",
            "batch_results": batch_results,
        }
    
    # Merge results
    print(f"[GPA Batch] Merging {len(successful)}/{len(batch_results)} successful batches...", file=sys.stderr)
    merged = merge_batch_results(batch_results)
    
    if failed_batches:
        merged["failed_batches"] = failed_batches
        merged["warning"] = f"{len(failed_batches)} batch(es) failed. Results are incomplete. Consider reducing batch_size or increasing timeout."
    
    return merged


def main():
    import argparse
    from dgra_cli_wrapper import run_gpa_from_file  # Reuse input parsing
    
    parser = argparse.ArgumentParser(description="GPA Batch Runner v0.7.1")
    parser.add_argument("--input-file", "-i", type=Path, required=True)
    parser.add_argument("--tissue", default="general")
    parser.add_argument("--phenotypes", default=None)
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--somatic", action="store_true")
    parser.add_argument("--batch-size", type=int, default=500, help="Variants per batch (default: 500)")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout per batch in seconds (default: 300)")
    parser.add_argument("--output-json", help="Write merged JSON result")
    parser.add_argument("--output", "-o", help="Write merged Markdown report")
    parser.add_argument("--format", choices=["auto", "vcf", "tsv", "csv", "excel", "freetext"], default="auto")
    parser.add_argument("--annotation-format", choices=["auto", "vep", "annovar", "snpeff"], default="auto")
    
    args = parser.parse_args()
    
    # Parse input
    sys.path.insert(0, str(SCRIPT_DIR))
    from dgra_input_parsers import parse_input
    
    try:
        variants = parse_input(args.input_file, fmt=args.format if args.format != "auto" else None,
                               annotation_fmt=args.annotation_format if args.annotation_format != "auto" else None)
    except Exception as e:
        print(json.dumps({"success": False, "error": f"Parse failed: {e}"}, indent=2))
        sys.exit(1)
    
    print(f"[GPA Batch] Loaded {len(variants)} variants from {args.input_file}")
    
    # Run batched analysis
    result = run_gpa_batched(
        variants=variants,
        tissue=args.tissue,
        user_phenotypes=args.phenotypes,
        offline=args.offline,
        somatic=args.somatic,
        batch_size=args.batch_size,
        timeout_per_batch=args.timeout,
    )
    
    # Write outputs
    if args.output_json:
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"[GPA Batch] JSON written to {args.output_json}")
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result.get("report_md", "No report generated"))
        print(f"[GPA Batch] Markdown written to {args.output}")
    
    # Print summary to stdout
    if result.get("success"):
        r = result["results"]
        s = r["summary"]
        print(f"\n=== GPA Batch Analysis Complete ===")
        print(f"Total variants: {r['meta']['total_variants']}")
        print(f"Batches: {r['meta']['batch_count']}")
        print(f"Total time: {r['meta']['total_elapsed_seconds']:.1f}s")
        print(f"Tier 1: {s['tier1_variant_count']} variants / {s['tier1_gene_count']} genes")
        print(f"Tier 2: {s['tier2_variant_count']} variants / {s['tier2_gene_count']} genes")
        print(f"Tier 3: {s['tier3_variant_count']} variants / {s['tier3_gene_count']} genes")
        print(f"Multi-hit: {', '.join(s['multi_hit_genes']) if s['multi_hit_genes'] else 'None'}")
        if "warning" in result:
            print(f"WARNING: {result['warning']}")
    else:
        print(f"FAILED: {result.get('error')}")
        sys.exit(1)
    
    # Also output JSON to stdout for piping
    print("\n" + json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
