#!/bin/bash
# Conservation Analysis Script
# Calculates Shannon entropy for each alignment position

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
mkdir -p "$OUTPUT_DIR/conservation"

echo "========================================="
echo "Conservation Analysis"
echo "========================================="
echo "Input: $ALIGNED_FASTA"
echo "Output: $OUTPUT_DIR/conservation/"
echo ""

# Check if input exists
if [ ! -f "$ALIGNED_FASTA" ]; then
    echo "Error: Input file not found: $ALIGNED_FASTA"
    exit 1
fi

# Create Python script for conservation analysis
cat > "$OUTPUT_DIR/conservation/calculate_conservation.py" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Calculate Shannon entropy for each alignment position
"""

import sys
import numpy as np
import pandas as pd
from Bio import AlignIO
from collections import Counter

def calculate_entropy(alignment, position):
    """Calculate Shannon entropy at a given position"""
    
    # Count amino acid frequencies
    aa_counts = Counter()
    for record in alignment:
        aa = str(record.seq[position])
        aa_counts[aa] += 1
    
    # Calculate probabilities
    total = sum(aa_counts.values())
    aa_probs = {aa: count/total for aa, count in aa_counts.items()}
    
    # Calculate entropy
    entropy = 0
    for prob in aa_probs.values():
        if prob > 0:
            entropy -= prob * np.log2(prob)
    
    # Normalize (max entropy for 20 amino acids + gap)
    max_entropy = np.log2(len(aa_probs)) if len(aa_probs) > 1 else 1
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    # Get most common amino acid
    most_common_aa = max(aa_counts, key=aa_counts.get)
    most_common_freq = aa_counts[most_common_aa] / total
    
    # Calculate gap ratio
    gap_count = aa_counts.get('-', 0)
    gap_ratio = gap_count / total
    
    # Number of variants
    num_variants = len([aa for aa in aa_counts if aa != '-'])
    
    # Classify conservation
    if norm_entropy < 0.3:
        category = "Highly conserved"
    elif norm_entropy < 0.6:
        category = "Moderately conserved"
    else:
        category = "Variable"
    
    return {
        'position': position + 1,
        'entropy': entropy,
        'norm_entropy': norm_entropy,
        'most_common_aa': most_common_aa,
        'most_common_freq': most_common_freq,
        'gap_ratio': gap_ratio,
        'num_variants': num_variants,
        'category': category
    }

def main():
    if len(sys.argv) < 3:
        print("Usage: python calculate_conservation.py <aligned.fasta> <output_dir>")
        sys.exit(1)
    
    aligned_fasta = sys.argv[1]
    output_dir = sys.argv[2]
    
    print("Reading alignment...")
    alignment = AlignIO.read(aligned_fasta, "fasta")
    num_seqs = len(alignment)
    aln_length = alignment.get_alignment_length()
    
    print(f"Sequences: {num_seqs}")
    print(f"Alignment length: {aln_length}")
    print()
    
    print("Calculating conservation...")
    results = []
    
    for pos in range(aln_length):
        if (pos + 1) % 50 == 0:
            print(f"  Position {pos + 1}/{aln_length}")
        
        result = calculate_entropy(alignment, pos)
        results.append(result)
    
    # Save to CSV
    df = pd.DataFrame(results)
    output_file = f"{output_dir}/conservation_detailed.csv"
    df.to_csv(output_file, index=False)
    
    print()
    print(f"✓ Results saved to: {output_file}")
    print()
    
    # Print summary
    highly_conserved = df[df['norm_entropy'] < 0.3]
    moderately_conserved = df[(df['norm_entropy'] >= 0.3) & (df['norm_entropy'] < 0.6)]
    variable = df[df['norm_entropy'] >= 0.6]
    
    print("="*60)
    print("Conservation Summary")
    print("="*60)
    print(f"Total positions: {len(df)}")
    print(f"Highly conserved (H < 0.3): {len(highly_conserved)} ({len(highly_conserved)/len(df)*100:.1f}%)")
    print(f"Moderately conserved (0.3 ≤ H < 0.6): {len(moderately_conserved)} ({len(moderately_conserved)/len(df)*100:.1f}%)")
    print(f"Variable (H ≥ 0.6): {len(variable)} ({len(variable)/len(df)*100:.1f}%)")
    print()
    
    # Top 10 conserved positions
    print("Top 10 conserved positions:")
    print("-"*60)
    top10 = df.nsmallest(10, 'norm_entropy')
    for _, row in top10.iterrows():
        print(f"  Position {row['position']:3d} ({row['most_common_aa']}): H = {row['norm_entropy']:.3f}")
    print()
    
    # Save summary
    with open(f"{output_dir}/conservation_summary.txt", 'w') as f:
        f.write("Conservation Analysis Summary\n")
        f.write("="*60 + "\n")
        f.write(f"Total positions: {len(df)}\n")
        f.write(f"Highly conserved (H < 0.3): {len(highly_conserved)} ({len(highly_conserved)/len(df)*100:.1f}%)\n")
        f.write(f"Moderately conserved (0.3 ≤ H < 0.6): {len(moderately_conserved)} ({len(moderately_conserved)/len(df)*100:.1f}%)\n")
        f.write(f"Variable (H ≥ 0.6): {len(variable)} ({len(variable)/len(df)*100:.1f}%)\n")
        f.write("\n")
        f.write("Top 10 conserved positions:\n")
        f.write("-"*60 + "\n")
        for _, row in top10.iterrows():
            f.write(f"Position {row['position']:3d} ({row['most_common_aa']}): H = {row['norm_entropy']:.3f}\n")
    
    print(f"✓ Summary saved to: {output_dir}/conservation_summary.txt")

if __name__ == "__main__":
    main()
PYTHON_EOF

# Run conservation analysis
echo "Running conservation analysis..."
python3 "$OUTPUT_DIR/conservation/calculate_conservation.py" "$ALIGNED_FASTA" "$OUTPUT_DIR/conservation"

echo ""
echo "========================================="
echo "Conservation analysis complete!"
echo "========================================="
echo "Output files:"
echo "  - $OUTPUT_DIR/conservation/conservation_detailed.csv"
echo "  - $OUTPUT_DIR/conservation/conservation_summary.txt"
echo ""
