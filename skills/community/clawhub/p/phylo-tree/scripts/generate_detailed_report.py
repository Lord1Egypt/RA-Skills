#!/usr/bin/env python3
"""
Generate detailed scientific report from phylogenetic analysis results.

This script reads analysis_summary.json and conclusions.md, then fills
the detailed report template with algorithm principles, parameter justifications,
figure analysis, and biological interpretation.

Usage:
    python3 generate_detailed_report.py <output_dir>

Output:
    <output_dir>/detailed_report.md
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_summary(output_dir):
    """Load analysis_summary.json"""
    summary_file = Path(output_dir) / "analysis_summary.json"
    if not summary_file.exists():
        print(f"Error: {summary_file} not found")
        print("Run generate_summary.py first")
        sys.exit(1)
    
    with open(summary_file) as f:
        return json.load(f)

def load_conclusions(output_dir):
    """Load conclusions.md"""
    conclusions_file = Path(output_dir) / "conclusions.md"
    if conclusions_file.exists():
        with open(conclusions_file) as f:
            return f.read()
    return ""

def load_template():
    """Load detailed report template"""
    template_file = Path(__file__).parent.parent / "references" / "report_template_detailed.md"
    with open(template_file) as f:
        return f.read()

def fill_template(template, summary, conclusions):
    """Fill template with data"""
    
    # Extract data
    iqtree = summary.get("iqtree", {})
    support = summary.get("support", {})
    alignment = summary.get("alignment", {})
    taxonomy = summary.get("taxonomy", {})
    
    # Fill placeholders
    report = template
    
    # Basic info
    report = report.replace("{num_sequences}", str(iqtree.get("num_sequences", "N/A")))
    report = report.replace("{num_species}", str(taxonomy.get("num_species", "N/A")))
    report = report.replace("{num_genera}", str(taxonomy.get("num_genera", "N/A")))
    
    # Model info
    report = report.replace("{best_model}", iqtree.get("best_model", "N/A"))
    report = report.replace("{log_likelihood}", f"{iqtree.get('log_likelihood', 0):.3f}")
    report = report.replace("{tree_length}", f"{iqtree.get('tree_length', 0):.3f}")
    
    # Alignment info
    report = report.replace("{alignment_length}", str(alignment.get("length", "N/A")))
    report = report.replace("{conserved_sites}", str(alignment.get("conserved_sites", "N/A")))
    report = report.replace("{variable_sites}", str(alignment.get("variable_sites", "N/A")))
    
    # Support values
    report = report.replace("{total_nodes}", str(support.get("total_nodes", "N/A")))
    report = report.replace("{high_support_nodes}", str(support.get("high_support_nodes", "N/A")))
    report = report.replace("{high_support_percentage}", f"{support.get('high_support_percentage', 0):.1f}")
    
    # Branch lengths
    report = report.replace("{mean_branch_length}", f"{iqtree.get('mean_branch_length', 0):.4f}")
    report = report.replace("{median_branch_length}", f"{iqtree.get('median_branch_length', 0):.4f}")
    report = report.replace("{max_branch_length}", f"{iqtree.get('max_branch_length', 0):.4f}")
    
    # Top genera
    top_genera = taxonomy.get("top_genera", [])
    if top_genera:
        report = report.replace("{genus1}", top_genera[0] if len(top_genera) > 0 else "N/A")
        report = report.replace("{genus2}", top_genera[1] if len(top_genera) > 1 else "N/A")
        report = report.replace("{top_genus}", top_genera[0] if len(top_genera) > 0 else "N/A")
    
    # Date
    report = report.replace("{date}", datetime.now().strftime("%Y-%m-%d"))
    
    # Add conclusions section
    if conclusions:
        report += f"\n\n---\n\n## Appendix: Detailed Conclusions\n\n{conclusions}\n"
    
    return report

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_detailed_report.py <output_dir>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    
    print("=" * 70)
    print("Generating Detailed Scientific Report")
    print("=" * 70)
    print()
    
    # Load data
    print("[1] Loading analysis summary...")
    summary = load_summary(output_dir)
    
    print("[2] Loading conclusions...")
    conclusions = load_conclusions(output_dir)
    
    print("[3] Loading report template...")
    template = load_template()
    
    print("[4] Filling template...")
    report = fill_template(template, summary, conclusions)
    
    # Save report
    output_file = Path(output_dir) / "detailed_report.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"[5] Report saved: {output_file}")
    print()
    print("=" * 70)
    print("Detailed Report Generation Complete")
    print("=" * 70)
    print()
    print("Report includes:")
    print("  ✓ Algorithm principles and theory")
    print("  ✓ Parameter justifications")
    print("  ✓ Experimental process")
    print("  ✓ Detailed figure analysis")
    print("  ✓ Biological interpretation")
    print("  ✓ Discussion and conclusions")
    print()
    print(f"Length: ~{len(report.split())} words")
    print()

if __name__ == "__main__":
    main()
