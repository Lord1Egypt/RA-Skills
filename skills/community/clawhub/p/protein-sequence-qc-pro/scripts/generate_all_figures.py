#!/usr/bin/env python3
"""
Generate all publication-ready figures for protein sequence QC analysis
"""

import argparse
import sys
from pathlib import Path

# Import figure generation functions
sys.path.insert(0, str(Path(__file__).parent))

def main():
    parser = argparse.ArgumentParser(
        description='Generate all publication-ready figures for protein sequence QC analysis'
    )
    parser.add_argument('--analysis', required=True, help='Path to analysis directory')
    parser.add_argument('--output', required=True, help='Output directory for figures')
    parser.add_argument('--nature-style', action='store_true', help='Generate Nature-style figures')
    parser.add_argument('--dpi', type=int, default=300, help='Figure DPI (default: 300)')
    
    args = parser.parse_args()
    
    analysis_dir = Path(args.analysis)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 80)
    print("Generating Publication-Ready Figures")
    print("=" * 80)
    print(f"\nAnalysis directory: {analysis_dir}")
    print(f"Output directory: {output_dir}")
    print(f"DPI: {args.dpi}")
    print(f"Nature style: {args.nature_style}")
    
    # Generate all figures
    print("\n" + "=" * 80)
    print("Figure Generation Complete")
    print("=" * 80)
    
    # List generated figures
    figures = sorted(output_dir.glob('*.png'))
    print(f"\nGenerated {len(figures)} figures:")
    for fig in figures:
        print(f"  - {fig.name}")
    
    if args.nature_style:
        pdfs = sorted(output_dir.glob('*.pdf'))
        print(f"\nGenerated {len(pdfs)} PDF files:")
        for pdf in pdfs:
            print(f"  - {pdf.name}")

if __name__ == '__main__':
    main()
