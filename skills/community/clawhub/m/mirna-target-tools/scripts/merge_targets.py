#!/usr/bin/env python3
"""
Merge results from TargetScan and miRanda, take intersection for high-confidence targets.
Usage: python merge_targets.py --targetscan targetscan.tsv --miranda miranda.tsv --output merged.txt
"""

import argparse
import pandas as pd
import sys

def main():
    parser = argparse.ArgumentParser(
        description='Merge TargetScan and miRanda results, find overlapping targets')
    parser.add_argument('--targetscan', required=True, help='TargetScan results (TSV)')
    parser.add_argument('--miranda', required=True, help='miRanda results (TSV)')
    parser.add_argument('--output', required=True, help='Output file for merged results')
    parser.add_argument('--context-cutoff', type=float, default=-0.2, 
                        help='Context+ score cutoff for TargetScan (default: -0.2, more negative = stricter)')
    parser.add_argument('--energy-cutoff', type=float, default=-10,
                        help='Energy cutoff for miRanda (default: -10 kcal/mol)')
    parser.add_argument('--only-intersection', action='store_true', default=True,
                        help='Only keep targets predicted by both tools (default: True)')
    
    args = parser.parse_args()
    
    # Read TargetScan
    print(f"Reading TargetScan from {args.targetscan}")
    ts_df = pd.read_csv(args.targetscan, sep='\t')
    print(f"TargetScan: {len(ts_df)} total interactions")
    
    # Filter by context score
    if 'context_score' in ts_df.columns:
        ts_filtered = ts_df[ts_df['context_score'] <= args.context_cutoff]
        print(f"After context score cutoff ({args.context_cutoff}): {len(ts_filtered)} interactions")
    else:
        ts_filtered = ts_df
        print("Warning: No context_score column found, using all TargetScan results")
    
    # Read miRanda
    print(f"\nReading miRanda from {args.miranda}")
    mir_df = pd.read_csv(args.miranda, sep='\t')
    print(f"miRanda: {len(mir_df)} total interactions")
    
    # Filter by energy
    if 'energy' in mir_df.columns:
        mir_filtered = mir_df[mir_df['energy'] <= args.energy_cutoff]
        print(f"After energy cutoff ({args.energy_cutoff}): {len(mir_filtered)} interactions")
    else:
        mir_filtered = mir_df
        print("Warning: No energy column found, using all miRanda results")
    
    # Extract interactions
    ts_interactions = set()
    for _, row in ts_filtered.iterrows():
    # Different column name variations
        mirna = row.get('mirna', row.get('miRNA', '')).strip()
        gene = row.get('target_gene', row.get('gene', row.get('target', ''))).strip()
        if mirna and gene:
            ts_interactions.add((mirna, gene))
    
    mir_interactions = set()
    for _, row in mir_filtered.iterrows():
        mirna = row.get('mirna', row.get('miRNA', '')).strip()
        gene = row.get('target_gene', row.get('target', row.get('gene', ''))).strip()
        if mirna and gene:
            mir_interactions.add((mirna, gene))
    
    print(f"\nUnique interactions after filtering:")
    print(f"  TargetScan: {len(ts_interactions)}")
    print(f"  miRanda: {len(mir_interactions)}")
    
    # Find intersection
    common = ts_interactions.intersection(mir_interactions)
    print(f"  Common (predicted by both): {len(common)}")
    
    if len(common) == 0:
        print("\nWarning: No overlapping targets found. Check your cutoffs might be too strict.")
        if len(ts_interactions) > 0 and len(mir_interactions) > 0:
            # Still output all unique from both
            union = ts_interactions.union(mir_interactions)
            print(f"Outputting all {len(union)} unique targets from both tools.")
            common = union
    
    # Write output
    with open(args.output, 'w') as f:
        f.write("miRNA\tTargetGene\tFoundInBoth\n")
        for mirna, gene in sorted(common):
            in_both = (mirna, gene) in ts_interactions and (mirna, gene) in mir_interactions
            f.write(f"{mirna}\t{gene}\t{in_both}\n")
    
    print(f"\nMerged results written to {args.output}")
    print(f"Done!")

if __name__ == '__main__':
    main()
