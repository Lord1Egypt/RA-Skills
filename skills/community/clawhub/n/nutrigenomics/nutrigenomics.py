#!/usr/bin/env python3
"""
nutrigenomics.py — Nutrigenomics: Personalised Nutrition from Genetic Data
Nutrigenomics OpenClaw Skill v0.3.2

Usage:
    python nutrigenomics.py --input genome.csv --output results/
    python nutrigenomics.py --input variants.vcf --output results/ --format vcf
"""

import argparse
import json
import sys
from pathlib import Path

from parse_input import parse_genetic_file
from extract_genotypes import extract_snp_genotypes
from score_variants import compute_nutrient_risk_scores
from generate_report import generate_report
from repro_bundle import create_reproducibility_bundle
from path_safety import validate_input_file, validate_output_dir, validate_panel_file


def main():
    parser = argparse.ArgumentParser(
        description="Nutrigenomics — personalised nutrigenomics report from genetic data"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to genetic data file (23andMe .txt/.csv, AncestryDNA .csv, or .vcf)"
    )
    parser.add_argument(
        "--output", default="nutrigenomics_results",
        help="Output directory (created if absent)"
    )
    parser.add_argument(
        "--format", choices=["auto", "23andme", "ancestry", "vcf"], default="auto",
        help="Input file format (default: auto-detect)"
    )
    parser.add_argument(
        "--panel", default=None,
        help="Path to custom SNP panel JSON (default: data/snp_panel.json)"
    )
    parser.add_argument(
        "--no-figures", action="store_true",
        help="Skip figure generation (useful in headless environments)"
    )
    args = parser.parse_args()

    workspace_root = Path.cwd().resolve()
    output_dir = validate_output_dir(args.output, workspace_root)

    # Resolve SNP panel
    skill_root = Path(__file__).parent.resolve()
    panel_path = (
        validate_panel_file(args.panel, skill_root) if args.panel
        else (skill_root / "data" / "snp_panel.json").resolve()
    )
    if not panel_path.exists():
        print(f"[ERROR] SNP panel not found at {panel_path}", file=sys.stderr)
        sys.exit(1)

    with open(panel_path, encoding="utf-8") as f:
        snp_panel = json.load(f)

    try:
        input_path = validate_input_file(args.input)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"[Nutrigenomics] Parsing input: {input_path}")
    genotype_table = parse_genetic_file(str(input_path), fmt=args.format)
    print(f"[Nutrigenomics] Loaded {len(genotype_table):,} variants")

    print("[Nutrigenomics] Extracting SNP genotypes from panel ...")
    snp_calls = extract_snp_genotypes(genotype_table, snp_panel)

    present = sum(1 for v in snp_calls.values() if v["status"] == "found")
    print(f"[Nutrigenomics] Panel coverage: {present}/{len(snp_panel)} SNPs found")

    print("[Nutrigenomics] Computing nutrient risk scores ...")
    risk_scores = compute_nutrient_risk_scores(snp_calls, snp_panel)

    print("[Nutrigenomics] Generating report ...")
    report_path = generate_report(
        snp_calls=snp_calls,
        risk_scores=risk_scores,
        snp_panel=snp_panel,
        output_dir=str(output_dir),
        figures=not args.no_figures,
        input_file=str(input_path)
    )

    print("[Nutrigenomics] Creating reproducibility bundle ...")
    create_reproducibility_bundle(
        input_file=str(input_path),
        output_dir=str(output_dir),
        panel_path=str(panel_path),
        args=vars(args)
    )

    print(f"\n[Nutrigenomics] Done. Report: {report_path}")
    print(f"[Nutrigenomics] Results in: {output_dir}/")


if __name__ == "__main__":
    main()
