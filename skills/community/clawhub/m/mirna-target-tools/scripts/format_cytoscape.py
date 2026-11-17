#!/usr/bin/env python3
"""
Convert merged miRNA-target results to Cytoscape SIF network format.
Usage: python format_cytoscape.py --input merged_results.txt --output network.sif
"""

import argparse
import pandas as pd
import sys

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
    
    with open(args.output, 'w') as f:
        for _, row in df.iterrows():
            mirna = str(row['miRNA']).replace(' ', '_')
            target = str(row['TargetGene']).replace(' ', '_')
            interaction = args.interaction_type
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
