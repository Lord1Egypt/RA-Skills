#!/usr/bin/env python3
"""
Convert merged miRNA-target results to Cytoscape SIF network format.
Usage: python format_cytoscape.py --input merged_results.txt --output network.sif
"""

import argparse
import math
import os
import re
import sys

import pandas as pd


def clean_label(value, limit=200):
    """Make a value safe as a SIF/Cytoscape node label."""
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return ''
    text = re.sub(r'[\s\x00-\x1f]+', '_', str(value)).strip('_')
    return text[:limit] if text else 'NA'

def main():
    parser = argparse.ArgumentParser(
        description='Convert miRNA-target gene results to Cytoscape SIF format')
    parser.add_argument('--input', required=True, help='Merged results file (TSV)')
    parser.add_argument('--output', required=True, help='Output SIF file for Cytoscape')
    parser.add_argument('--attr-output', help='Output node attributes file')
    parser.add_argument('--interaction-type', default='regulates', 
                        help='Interaction type name for SIF (default: regulates)')
    
    args = parser.parse_args()
    
    # Read input
    df = pd.read_csv(args.input, sep='\t')
    
    # Check columns
    required_cols = ['miRNA', 'TargetGene']
    for col in required_cols:
        if col not in df.columns:
            print(f"Error: Column '{col}' not found in input file")
            print(f"Found columns: {list(df.columns)}")
            sys.exit(1)
    
    # Write SIF format: source interaction target
    edges = []
    nodes = {}
    interaction = clean_label(args.interaction_type, limit=40) or 'regulates'
    out_dir = os.path.dirname(os.path.abspath(args.output))
    os.makedirs(out_dir, exist_ok=True)

    with open(args.output, 'w') as f:
        for _, row in df.iterrows():
            mirna = clean_label(row.get('miRNA'))
            target = clean_label(row.get('TargetGene'))
            if not mirna or not target:
                continue
            f.write(f"{mirna}\t{interaction}\t{target}\n")
            edges.append((mirna, interaction, target))
            
            # Track node types for attributes
            nodes[mirna] = 'miRNA'
            nodes[target] = 'TargetGene'
    
    print(f"Created Cytoscape SIF network: {args.output}")
    print(f"  {len(edges)} edges")
    print(f"  {len(nodes)} nodes")
    
    # Write node attributes if requested
    if args.attr_output:
        with open(args.attr_output, 'w') as f:
            f.write("NodeName\tNodeType\n")
            for node, ntype in nodes.items():
                f.write(f"{node}\t{ntype}\n")
        print(f"Node attributes written to {args.attr_output}")
    
    print("\nHow to use in Cytoscape:")
    print("1. Open Cytoscape")
    print("2. File -> Import -> Network from File... -> Select your .sif file")
    print("3. If you have node attributes: File -> Import -> Table from File... -> Select attributes file")
    print("4. Use Layout -> yFiles -> Organic or ForceDirected to visualize the network")
    print("5. You can map 'NodeType' to node color to easily distinguish miRNAs and target genes")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
