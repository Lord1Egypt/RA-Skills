#!/usr/bin/env python3
"""
Quality Control Module for PhyloTree
=====================================

Generates comprehensive QC reports for each stage of the phylogenetic analysis.

Author: PhyloTree Skill
Version: 2.0.0
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

def generate_final_qc_report(project_dir: Path) -> Dict:
    """
    Generate comprehensive QC report combining all stages
    
    Args:
        project_dir: Project directory path
    
    Returns:
        Dictionary containing all QC metrics
    """
    reports_dir = project_dir / "reports"
    
    qc_report = {
        "generated_at": datetime.now().isoformat(),
        "project_dir": str(project_dir),
        "stages": {}
    }
    
    # Load individual stage reports
    stage_files = {
        "01_sequence_collection": reports_dir / "01_sequence_collection_qc.json",
        "02_alignment": reports_dir / "02_alignment_qc.json",
    }
    
    for stage_name, report_file in stage_files.items():
        if report_file.exists():
            with open(report_file) as f:
                qc_report["stages"][stage_name] = json.load(f)
    
    # Overall assessment
    qc_report["assessment"] = assess_quality(qc_report)
    
    # Save final report
    final_report = reports_dir / "00_final_qc_report.json"
    with open(final_report, "w") as f:
        json.dump(qc_report, f, indent=2)
    
    return qc_report

def assess_quality(qc_report: Dict) -> Dict:
    """
    Assess overall quality and provide recommendations
    
    Args:
        qc_report: QC report dictionary
    
    Returns:
        Assessment dictionary with pass/fail and recommendations
    """
    assessment = {
        "overall_status": "PASS",
        "warnings": [],
        "recommendations": []
    }
    
    # Check sequence collection
    if "01_sequence_collection" in qc_report["stages"]:
        seq_qc = qc_report["stages"]["01_sequence_collection"]
        
        if seq_qc["total_sequences"] < 20:
            assessment["warnings"].append(
                f"Low sequence count ({seq_qc['total_sequences']}). "
                "Minimum 20 sequences recommended for reliable phylogeny."
            )
            assessment["overall_status"] = "WARNING"
        
        if seq_qc["unique_organisms"] < 10:
            assessment["warnings"].append(
                f"Low organism diversity ({seq_qc['unique_organisms']}). "
                "More diverse sampling recommended."
            )
    
    # Check alignment
    if "02_alignment" in qc_report["stages"]:
        aln_qc = qc_report["stages"]["02_alignment"]
        
        if aln_qc["average_gap_proportion"] > 0.3:
            assessment["warnings"].append(
                f"High gap proportion ({aln_qc['average_gap_proportion']:.1%}). "
                "Consider using trimAl to remove poorly aligned regions."
            )
            assessment["overall_status"] = "WARNING"
        
        if aln_qc["alignment_length"] < 100:
            assessment["warnings"].append(
                f"Short alignment ({aln_qc['alignment_length']} sites). "
                "May not provide sufficient phylogenetic signal."
            )
            assessment["overall_status"] = "WARNING"
    
    # Recommendations
    if assessment["overall_status"] == "PASS":
        assessment["recommendations"].append(
            "Quality checks passed. Proceed with publication."
        )
    else:
        assessment["recommendations"].append(
            "Review warnings before publication. Consider re-running with adjusted parameters."
        )
    
    return assessment

def print_qc_summary(qc_report: Dict):
    """Print QC summary to console"""
    print("\n" + "="*70)
    print("Quality Control Summary")
    print("="*70 + "\n")
    
    assessment = qc_report["assessment"]
    
    # Overall status
    status_color = "\033[92m" if assessment["overall_status"] == "PASS" else "\033[93m"
    print(f"Overall Status: {status_color}{assessment['overall_status']}\033[0m\n")
    
    # Warnings
    if assessment["warnings"]:
        print("Warnings:")
        for warning in assessment["warnings"]:
            print(f"  ⚠ {warning}")
        print()
    
    # Recommendations
    if assessment["recommendations"]:
        print("Recommendations:")
        for rec in assessment["recommendations"]:
            print(f"  → {rec}")
        print()
    
    print("="*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 qc.py <project_directory>")
        sys.exit(1)
    
    project_dir = Path(sys.argv[1])
    
    if not project_dir.exists():
        print(f"Error: Project directory not found: {project_dir}")
        sys.exit(1)
    
    qc_report = generate_final_qc_report(project_dir)
    print_qc_summary(qc_report)
