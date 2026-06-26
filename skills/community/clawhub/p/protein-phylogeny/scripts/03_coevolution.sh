#!/bin/bash
# Coevolution Analysis Script
# Calculates Normalized Mutual Information for all position pairs

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <aligned.fasta> <output_dir>"
    echo ""
    echo "Example: $0 aligned.fasta output/"
    exit 1
fi

ALIGNED_FASTA=$1
OUTPUT_DIR=$2

# Create output directory
mkdir -p "$OUTPUT_DIR/coevolution"

echo "========================================="
echo "Coevolution Analysis"
echo "========================================="
echo "Input: $ALIGNED_FASTA"
echo "Output: $OUTPUT_DIR/coevolution/"
echo ""

# Check if input exists
if [ ! -f "$ALIGNED_FASTA" ]; then
    echo "Error: Input file not found: $ALIGNED_FASTA"
    exit 1
fi

# Create Python script for coevolution analysis
cat > "$OUTPUT_DIR/coevolution/calculate_coevolution.py" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Calculate Normalized Mutual Information for all position pairs
"""

import sys
import numpy as np
import pandas as pd
from Bio import AlignIO
from collections import Counter
import json

def calculate_joint_prob(alignment, pos1, pos2):
    """Calculate joint probability distribution"""
    pairs = []
    for record in alignment:
        aa1 = str(record.seq[pos1])
        aa2 = str(record.seq[pos2])
        # Skip if either position has a gap
        if aa1 != '-' and aa2 != '-':
            pairs.append((aa1, aa2))
    
    if len(pairs) == 0:
        return {}, []
    
    pair_counts = Counter(pairs)
    total = len(pairs)
    joint_prob = {pair: count/total for pair, count in pair_counts.items()}
    
    return joint_prob, pairs

def calculate_marginal_prob(pairs):
    """Calculate marginal probabilities"""
    aa1_list = [pair[0] for pair in pairs]
    aa2_list = [pair[1] for pair in pairs]
    
    aa1_counts = Counter(aa1_list)
    aa2_counts = Counter(aa2_list)
    
    total = len(pairs)
    
    p_aa1 = {aa: count/total for aa, count in aa1_counts.items()}
    p_aa2 = {aa: count/total for aa, count in aa2_counts.items()}
    
    return p_aa1, p_aa2

def calculate_MI(joint_prob, p_aa1, p_aa2):
    """Calculate mutual information"""
    MI = 0
    for (aa1, aa2), p_xy in joint_prob.items():
        p_x = p_aa1[aa1]
        p_y = p_aa2[aa2]
        
        if p_xy > 0 and p_x > 0 and p_y > 0:
            MI += p_xy * np.log2(p_xy / (p_x * p_y))
    
    return MI

def calculate_entropy(prob_dist):
    """Calculate Shannon entropy"""
    H = 0
    for p in prob_dist.values():
        if p > 0:
            H -= p * np.log2(p)
    return H

def main():
    if len(sys.argv) < 3:
        print("Usage: python calculate_coevolution.py <aligned.fasta> <output_dir>")
        sys.exit(1)
    
    aligned_fasta = sys.argv[1]
    output_dir = sys.argv[2]
    
    print("Reading alignment...")
    alignment = AlignIO.read(aligned_fasta, "fasta")
    num_seqs = len(alignment)
    aln_length = alignment.get_alignment_length()
    
    print(f"Sequences: {num_seqs}")
    print(f"Alignment length: {aln_length}")
    print(f"Total pairs to calculate: {aln_length * (aln_length - 1) // 2}")
    print()
    
    print("Calculating coevolution (this may take a while)...")
    results = []
    
    total_pairs = aln_length * (aln_length - 1) // 2
    calculated = 0
    
    for i in range(aln_length):
        if (i + 1) % 10 == 0:
            print(f"  Position {i + 1}/{aln_length} ({calculated}/{total_pairs} pairs, {calculated/total_pairs*100:.1f}%)")
        
        for j in range(i + 1, aln_length):
            # Calculate joint and marginal probabilities
            joint_prob, pairs = calculate_joint_prob(alignment, i, j)
            
            if len(pairs) == 0:
                continue
            
            p_aa1, p_aa2 = calculate_marginal_prob(pairs)
            
            # Calculate MI
            MI = calculate_MI(joint_prob, p_aa1, p_aa2)
            
            # Calculate entropies
            H_X = calculate_entropy(p_aa1)
            H_Y = calculate_entropy(p_aa2)
            
            # Calculate gap ratios
            gap1 = sum(1 for record in alignment if str(record.seq[i]) == '-') / num_seqs
            gap2 = sum(1 for record in alignment if str(record.seq[j]) == '-') / num_seqs
            
            results.append({
                'pos1': i + 1,
                'pos2': j + 1,
                'MI': MI,
                'num_pairs': len(pairs),
                'gap1': gap1,
                'gap2': gap2
            })
            
            calculated += 1
    
    print()
    print(f"✓ Calculated {len(results)} position pairs")
    print()
    
    # Save to CSV
    df = pd.DataFrame(results)
    df = df.sort_values('MI', ascending=False)
    output_file = f"{output_dir}/coevolution_detailed.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✓ Results saved to: {output_file}")
    print()
    
    # Identify hub positions
    print("Identifying hub positions...")
    hub_counts = {}
    
    # Count how many times each position appears in top coevolved pairs
    top_pairs = df.nlargest(100, 'MI')
    for _, row in top_pairs.iterrows():
        pos1 = int(row['pos1'])
        pos2 = int(row['pos2'])
        hub_counts[pos1] = hub_counts.get(pos1, 0) + 1
        hub_counts[pos2] = hub_counts.get(pos2, 0) + 1
    
    # Sort by degree
    hubs = sorted(hub_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Save hub positions
    with open(f"{output_dir}/hub_positions.txt", 'w') as f:
        f.write("Hub Positions (degree ≥ 5)\n")
        f.write("="*60 + "\n")
        for pos, degree in hubs:
            if degree >= 5:
                f.write(f"Position {pos}: Degree {degree}\n")
    
    print(f"✓ Hub positions saved to: {output_dir}/hub_positions.txt")
    print()
    
    # Print summary
    print("="*60)
    print("Coevolution Summary")
    print("="*60)
    print(f"Total position pairs: {len(df)}")
    print(f"Strong coevolution (MI > 0.5): {len(df[df['MI'] > 0.5])}")
    print(f"Moderate coevolution (0.3 < MI ≤ 0.5): {len(df[(df['MI'] > 0.3) & (df['MI'] <= 0.5)])}")
    print()
    
    print("Top 10 coevolved pairs:")
    print("-"*60)
    top10 = df.nlargest(10, 'MI')
    for _, row in top10.iterrows():
        print(f"  {int(row['pos1']):3d} ↔ {int(row['pos2']):3d}: MI = {row['MI']:.3f}")
    print()
    
    print("Top 10 hub positions:")
    print("-"*60)
    for pos, degree in hubs[:10]:
        print(f"  Position {pos:3d}: Degree {degree}")
    print()
    
    # Save network data for visualization
    network_data = {
        'nodes': [{'id': pos, 'degree': degree} for pos, degree in hubs if degree >= 5],
        'edges': [
            {
                'source': int(row['pos1']),
                'target': int(row['pos2']),
                'weight': float(row['MI'])
            }
            for _, row in df[df['MI'] > 0.5].iterrows()
        ]
    }
    
    with open(f"{output_dir}/network_data.json", 'w') as f:
        json.dump(network_data, f, indent=2)
    
    print(f"✓ Network data saved to: {output_dir}/network_data.json")

if __name__ == "__main__":
    main()
PYTHON_EOF

# Run coevolution analysis
echo "Running coevolution analysis..."
python3 "$OUTPUT_DIR/coevolution/calculate_coevolution.py" "$ALIGNED_FASTA" "$OUTPUT_DIR/coevolution"

echo ""
echo "========================================="
echo "Coevolution analysis complete!"
echo "========================================="
echo "Output files:"
echo "  - $OUTPUT_DIR/coevolution/coevolution_detailed.csv"
echo "  - $OUTPUT_DIR/coevolution/hub_positions.txt"
echo "  - $OUTPUT_DIR/coevolution/network_data.json"
echo ""
