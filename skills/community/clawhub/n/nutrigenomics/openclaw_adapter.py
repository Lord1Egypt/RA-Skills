#!/usr/bin/env python3
"""
openclaw_adapter.py — OpenClaw compatibility layer for Nutrigenomics

Nutrigenomics: Personalised Nutrition from Genetic Data
Author: David de Lorenzo (https://github.com/drdaviddelorenzo)
Website: https://drdaviddelorenzo.github.io
License: MIT
Repository: https://github.com/drdaviddelorenzo/nutrigenomics

This module wraps the core Nutrigenomics analysis for use via OpenClaw's platform.
It handles file uploads, manages output, and formats results for web delivery.

Usage (via OpenClaw):
    openclaw "Generate my personalised nutrition report from my genome file"
    openclaw "I uploaded my 23andMe data, what should I eat based on my genes?"
    openclaw "What does my APOE status mean for my diet?"
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

# Import core Nutrigenomics modules
from parse_input import parse_genetic_file
from extract_genotypes import extract_snp_genotypes
from score_variants import compute_nutrient_risk_scores
from generate_report import generate_report
from repro_bundle import create_reproducibility_bundle
from path_safety import validate_input_file, validate_output_dir, validate_panel_file


# OpenClaw entry point (called by the platform)
def run_analysis(input_file: str, file_format: str = "auto") -> Dict[str, Any]:
    """
    Main entry point for OpenClaw.
    
    Args:
        input_file: Path to uploaded genetic data file
        file_format: File format hint ("auto", "23andme", "ancestry", "vcf")
    
    Returns:
        Result dictionary with analysis outputs
    """
    adapter = NutrigenomicsOpenClaw()
    return adapter.analyse_file(input_file, file_format=file_format)



class NutrigenomicsOpenClaw:
    """
    OpenClaw adapter for Nutrigenomics.
    
    Handles:
    - File upload and format detection
    - Analysis pipeline
    - Output formatting for web delivery
    - Error handling and user-friendly messages
    """
    
    def __init__(self, panel_path: Optional[str] = None):
        """
        Initialise the adapter.
        
        Args:
            panel_path: Path to custom SNP panel JSON (default: data/snp_panel.json)
        """
        # Resolve SNP panel
        skill_root = Path(__file__).parent.resolve()
        if panel_path is None:
            panel_path = (skill_root / "data" / "snp_panel.json").resolve()
        else:
            panel_path = validate_panel_file(panel_path, skill_root)
        
        if not panel_path.exists():
            raise FileNotFoundError(f"SNP panel not found at {panel_path}")
        
        with open(panel_path, encoding="utf-8") as f:
            self.snp_panel = json.load(f)
        
        self.panel_path = panel_path
    
    def analyse_file(
        self,
        input_file: str,
        file_format: str = "auto",
        output_dir: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run the complete Nutrigenomics analysis on a genetic data file.
        
        Args:
            input_file: Path to genetic data file (23andMe, AncestryDNA, or VCF)
            file_format: Auto-detect or specify "23andme", "ancestry", "vcf"
            output_dir: Where to save results (default: timestamped directory
                under the working directory; persists until manually deleted)
        
        Returns:
            Dict with keys:
            - "status": "success" or "error"
            - "output_dir": Absolute path to the output directory
            - "report_path": Filename of the Markdown report (relative to output_dir)
            - "figures": Dict of figure filenames (relative to output_dir)
            - "summary": Executive summary as string
            - "risk_scores": Dict of nutrient risk scores
            - "message": Human-readable status message
            - "cleanup_reminder": Reminder to delete output_dir after download
        """
        
        try:
            try:
                input_path = validate_input_file(input_file)
            except Exception as exc:
                return {
                    "status": "error",
                    "message": str(exc),
                    "report_path": None,
                    "figures": {},
                    "summary": None,
                    "risk_scores": {}
                }

            if not input_path.exists():
                return {
                    "status": "error",
                    "message": f"File not found: {input_file}",
                    "report_path": None,
                    "figures": {},
                    "summary": None,
                    "risk_scores": {}
                }
            
            # Set up output directory
            # A timestamped directory is created under the working directory and
            # persists on disk until the caller deletes it — there is no auto-cleanup.
            workspace_root = Path.cwd().resolve()
            if output_dir is None:
                ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                output_dir = str(workspace_root / f"nutrigenomics_output_{ts}")
                Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            output_path = validate_output_dir(output_dir, workspace_root)
            
            print(f"[Nutrigenomics] Parsing genetic file: {input_path.name}")
            
            # Parse genetic data
            try:
                genotype_table = parse_genetic_file(str(input_path), fmt=file_format)
            except Exception as e:
                return {
                    "status": "error",
                    "message": f"Failed to parse genetic file: {str(e)}. Please ensure it's valid 23andMe, AncestryDNA, or VCF format.",
                    "report_path": None,
                    "figures": {},
                    "summary": None,
                    "risk_scores": {}
                }
            
            if not genotype_table:
                return {
                    "status": "error",
                    "message": "No variants found in input file. Please check file format.",
                    "report_path": None,
                    "figures": {},
                    "summary": None,
                    "risk_scores": {}
                }
            
            print(f"[Nutrigenomics] Loaded {len(genotype_table):,} variants")
            
            # Extract SNP genotypes
            print("[Nutrigenomics] Extracting SNP genotypes from panel...")
            snp_calls = extract_snp_genotypes(genotype_table, self.snp_panel)
            
            present = sum(1 for v in snp_calls.values() if v["status"] == "found")
            coverage = (present / len(self.snp_panel)) * 100
            print(f"[Nutrigenomics] Panel coverage: {present}/{len(self.snp_panel)} SNPs ({coverage:.1f}%)")
            
            # Compute risk scores
            print("[Nutrigenomics] Computing nutrient risk scores...")
            risk_scores = compute_nutrient_risk_scores(snp_calls, self.snp_panel)
            
            # Generate report
            print("[Nutrigenomics] Generating personalised report...")
            report_path = generate_report(
                snp_calls=snp_calls,
                risk_scores=risk_scores,
                snp_panel=self.snp_panel,
                output_dir=str(output_path),
                figures=True,
                input_file=str(input_path)
            )
            
            # Generate reproducibility bundle
            print("[Nutrigenomics] Creating reproducibility bundle...")
            create_reproducibility_bundle(
                input_file=str(input_path),
                output_dir=str(output_path),
                panel_path=str(self.panel_path),
                args={"format": file_format}
            )
            
            # Prepare output summary
            summary = self._generate_summary(risk_scores, snp_calls)
            
            # Locate generated figures.
            # Return filenames relative to output_dir — the caller can join
            # them with output_dir to get the full path if needed.
            # Absolute paths are intentionally not returned here to avoid
            # embedding system paths in the result dict for sensitive data.
            figures = {}
            for fig_file in ["nutrigenomics_radar.png", "nutrigenomics_heatmap.png"]:
                if (output_path / fig_file).exists():
                    figures[fig_file.replace(".png", "")] = fig_file

            result = {
                "status": "success",
                "message": f"✅ Analysis complete. Panel coverage: {present}/{len(self.snp_panel)} SNPs ({coverage:.1f}%)",
                "output_dir": str(output_path),
                "report_path": "nutrigenomics_report.md",   # relative to output_dir
                "figures": figures,                         # filenames relative to output_dir
                "summary": summary,
                "risk_scores": risk_scores,
                "cleanup_reminder": (
                    "Output files persist in the output directory until manually deleted. "
                    "Delete output_dir after the user has downloaded their results."
                ),
            }
            
            print(f"[Nutrigenomics] Success! Results in: {output_path}/")
            return result
        
        except Exception as e:
            print(f"[Nutrigenomics] Unexpected error: {str(e)}", file=sys.stderr)
            return {
                "status": "error",
                "message": f"Unexpected error during analysis: {str(e)}",
                "report_path": None,
                "figures": {},
                "summary": None,
                "risk_scores": {}
            }
    
    def _generate_summary(self, risk_scores: Dict, snp_calls: Dict) -> str:
        """
        Generate a brief executive summary of the analysis.
        
        Args:
            risk_scores: Dict of nutrient risk scores from compute_nutrient_risk_scores()
            snp_calls: SNP genotype calls from extract_snp_genotypes()
        
        Returns:
            Formatted summary string suitable for OpenClaw display
        """
        
        if not risk_scores:
            return "No nutrient risk scores computed. Please check your input data."
        
        # Find top 3 elevated nutrients
        top_nutrients = sorted(
            risk_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        summary_lines = [
            "🧬 **Your Personalised Nutrition Profile**",
            ""
        ]
        
        for nutrient, score in top_nutrients:
            risk_level = self._score_to_risk_level(score)
            emoji = self._risk_emoji(risk_level)
            summary_lines.append(
                f"{emoji} **{nutrient.title()}**: {score:.1f}/10 ({risk_level})"
            )
        
        summary_lines.extend([
            "",
            "📋 See your full report for:",
            "• Gene-by-gene breakdown",
            "• Detailed recommendations",
            "• Nutrient-risk visualisations",
            "• Supplement interaction guidance",
            "",
            "⚠️ **Disclaimer**: This is educational analysis, not medical advice. "
            "Consult a registered dietitian or physician before making changes."
        ])
        
        return "\n".join(summary_lines)
    
    @staticmethod
    def _score_to_risk_level(score: float) -> str:
        """Convert numeric risk score to risk level category."""
        if score < 3:
            return "Low Risk"
        elif score < 6:
            return "Moderate Risk"
        else:
            return "Elevated Risk"
    
    @staticmethod
    def _risk_emoji(risk_level: str) -> str:
        """Return emoji for risk level."""
        if "Low" in risk_level:
            return "🟢"
        elif "Moderate" in risk_level:
            return "🟡"
        else:
            return "🔴"


if __name__ == "__main__":
    # CLI fallback (for testing outside OpenClaw)
    import argparse
    
    cli_parser = argparse.ArgumentParser(
        description="Nutrigenomics — OpenClaw Edition"
    )
    cli_parser.add_argument("--input", required=True, help="Path to genetic data file")
    cli_parser.add_argument("--output", help="Output directory")
    cli_parser.add_argument("--format", default="auto", help="File format")
    
    cli_args = cli_parser.parse_args()
    
    adapter = NutrigenomicsOpenClaw()
    result = adapter.analyse_file(
        input_file=cli_args.input,
        file_format=cli_args.format,
        output_dir=cli_args.output
    )
    
    print(json.dumps(result, indent=2, default=str))
