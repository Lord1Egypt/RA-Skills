#!/bin/bash
# Report Generation Script
# Create comprehensive analysis report

set -e

# Check arguments
if [ $# -lt 2 ]; then
    echo "Usage: $0 <output_dir> <family_name>"
    echo ""
    echo "Example: $0 output/ \"Example Protein Family\""
    exit 1
fi

OUTPUT_DIR=$1
FAMILY_NAME=$2

echo "========================================="
echo "Generating Report"
echo "========================================="
echo "Family: $FAMILY_NAME"
echo "Output: $OUTPUT_DIR/report.md"
echo ""

# Check if required files exist
if [ ! -f "$OUTPUT_DIR/conservation/conservation_summary.txt" ]; then
    echo "Error: Conservation results not found. Run 02_conservation.sh first."
    exit 1
fi

if [ ! -f "$OUTPUT_DIR/coevolution/hub_positions.txt" ]; then
    echo "Error: Coevolution results not found. Run 03_coevolution.sh first."
    exit 1
fi

if [ ! -f "$OUTPUT_DIR/phylogeny/tree_summary.txt" ]; then
    echo "Error: Phylogeny results not found. Run 04_phylogeny.sh first."
    exit 1
fi

# Create Python script to generate report
cat > "$OUTPUT_DIR/generate_report.py" << 'PYTHON_EOF'
#!/usr/bin/env python3
"""
Generate comprehensive analysis report
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
from Bio import AlignIO, Phylo

def read_file_safe(filepath):
    """Safely read file content"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except:
        return "N/A"

def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_report.py <output_dir> <family_name>")
        sys.exit(1)
    
    output_dir = sys.argv[1]
    family_name = sys.argv[2]
    
    # Read data
    print("Reading analysis results...")
    
    # Conservation
    df_cons = pd.read_csv(f'{output_dir}/conservation/conservation_detailed.csv')
    highly_conserved = df_cons[df_cons['norm_entropy'] < 0.3]
    moderately_conserved = df_cons[(df_cons['norm_entropy'] >= 0.3) & (df_cons['norm_entropy'] < 0.6)]
    variable = df_cons[df_cons['norm_entropy'] >= 0.6]
    
    # Coevolution
    df_coev = pd.read_csv(f'{output_dir}/coevolution/coevolution_detailed.csv')
    strong_coev = df_coev[df_coev['MI'] > 0.5]
    moderate_coev = df_coev[(df_coev['MI'] > 0.3) & (df_coev['MI'] <= 0.5)]
    
    # Hubs
    hubs = []
    try:
        with open(f'{output_dir}/coevolution/hub_positions.txt', 'r') as f:
            for line in f:
                if line.startswith('Position'):
                    parts = line.split()
                    pos = int(parts[1].rstrip(':'))
                    degree = int(parts[3])
                    hubs.append((pos, degree))
    except:
        pass
    
    # Phylogeny
    try:
        tree = Phylo.read(f'{output_dir}/phylogeny/tree.contree', 'newick')
        bootstrap_values = [c.confidence for c in tree.find_clades() if c.confidence is not None]
        strong_bs = sum(1 for b in bootstrap_values if b >= 95)
        moderate_bs = sum(1 for b in bootstrap_values if 70 <= b < 95)
        weak_bs = sum(1 for b in bootstrap_values if b < 70)
        total_bs = len(bootstrap_values)
    except:
        bootstrap_values = []
        strong_bs = moderate_bs = weak_bs = total_bs = 0
    
    # Alignment
    try:
        alignment = AlignIO.read(f'{output_dir}/qc/final.fasta', 'fasta')
        num_seqs = len(alignment)
        aln_length = alignment.get_alignment_length()
    except:
        num_seqs = 0
        aln_length = 0
    
    # Generate report
    print("Generating report...")
    
    report = f"""# {family_name} Phylogenetic Analysis Report

**Analysis Date:** {datetime.now().strftime('%Y-%m-%d')}  
**Dataset:** {num_seqs} high-quality sequences  
**Analysis Type:** Quality control + Conservation + Coevolution + Phylogeny

---

## Executive Summary

This report presents a comprehensive phylogenetic analysis of the {family_name}, including:

1. **Quality Control:** Stringent filtering from raw sequences to high-quality non-redundant dataset
2. **Conservation Analysis:** Identification of {len(highly_conserved)} highly conserved positions using Shannon entropy
3. **Coevolution Analysis:** Detection of {len(strong_coev)} strongly coevolved position pairs using Normalized Mutual Information
4. **Phylogenetic Analysis:** Maximum likelihood tree with {strong_bs}/{total_bs} ({strong_bs/total_bs*100 if total_bs > 0 else 0:.1f}%) strongly supported branches

Key findings include identification of critical functional residues, coevolution networks, and evolutionary relationships within the family.

---

## Dataset Summary

| Metric | Value |
|--------|-------|
| Final sequences | {num_seqs} |
| Alignment length | {aln_length} positions |
| Highly conserved positions | {len(highly_conserved)} ({len(highly_conserved)/len(df_cons)*100:.1f}%) |
| Coevolved pairs (MI > 0.5) | {len(strong_coev)} |
| Hub positions (degree ≥ 5) | {len(hubs)} |
| Strong bootstrap support (≥95%) | {strong_bs}/{total_bs} ({strong_bs/total_bs*100 if total_bs > 0 else 0:.1f}%) |

---

## Conservation Analysis

### Methods

Shannon entropy calculated for each alignment position:

```
H_norm = H / log₂(20)
```

**Classification:**
- H < 0.3: Highly conserved
- 0.3 ≤ H < 0.6: Moderately conserved
- H ≥ 0.6: Variable

### Results

**Conservation distribution:**
- Highly conserved: {len(highly_conserved)} positions ({len(highly_conserved)/len(df_cons)*100:.1f}%)
- Moderately conserved: {len(moderately_conserved)} positions ({len(moderately_conserved)/len(df_cons)*100:.1f}%)
- Variable: {len(variable)} positions ({len(variable)/len(df_cons)*100:.1f}%)

**Top 10 conserved positions:**

| Position | Amino Acid | Entropy | Category |
|----------|------------|---------|----------|
"""
    
    # Add top 10 conserved positions
    top10_cons = df_cons.nsmallest(10, 'norm_entropy')
    for _, row in top10_cons.iterrows():
        report += f"| {int(row['position'])} | {row['most_common_aa']} | {row['norm_entropy']:.3f} | {row['category']} |\n"
    
    report += f"""
![Conservation Landscape](figures/conservation_landscape.png)

*Figure 1: Conservation landscape showing Shannon entropy across all alignment positions. Green: highly conserved (H < 0.3), Yellow: moderately conserved (0.3 ≤ H < 0.6), Red: variable (H ≥ 0.6).*

---

## Coevolution Analysis

### Methods

Normalized Mutual Information (NMI) calculated for all position pairs:

```
NMI(X,Y) = MI(X,Y) / sqrt(H(X) × H(Y))
```

**Threshold:** NMI > 0.5 for strong coevolution

### Results

**Coevolution statistics:**
- Total position pairs: {len(df_coev)}
- Strong coevolution (MI > 0.5): {len(strong_coev)} pairs ({len(strong_coev)/len(df_coev)*100:.1f}%)
- Moderate coevolution (0.3 < MI ≤ 0.5): {len(moderate_coev)} pairs ({len(moderate_coev)/len(df_coev)*100:.1f}%)

**Top 10 coevolved pairs:**

| Pair | MI Score | Number of Pairs |
|------|----------|-----------------|
"""
    
    # Add top 10 coevolved pairs
    top10_coev = df_coev.nlargest(10, 'MI')
    for _, row in top10_coev.iterrows():
        report += f"| {int(row['pos1'])} ↔ {int(row['pos2'])} | {row['MI']:.3f} | {int(row['num_pairs'])} |\n"
    
    report += f"""
**Hub positions (degree ≥ 5):**

| Position | Degree | Functional Prediction |
|----------|--------|----------------------|
"""
    
    # Add hub positions
    for pos, degree in hubs[:10]:
        report += f"| {pos} | {degree} | Hub position |\n"
    
    report += f"""
![Coevolution Network](figures/coevolution_network.png)

*Figure 2: Coevolution network showing position pairs with MI > 0.5. Red nodes: hub positions (degree ≥ 5), Blue nodes: non-hub positions. Edge width proportional to MI score.*

![Hub Heatmap](figures/hub_heatmap.png)

*Figure 3: Heatmap showing coevolution strength (MI scores) between top hub positions.*

---

## Phylogenetic Analysis

### Methods

Maximum likelihood tree built with IQ-TREE:
- **Model selection:** ModelFinder (AIC/BIC)
- **Bootstrap:** UFBoot2 (1000 replicates)
- **Convergence check:** Required > 0.99

### Results

**Bootstrap support distribution:**
- Strong (≥95%): {strong_bs} branches ({strong_bs/total_bs*100 if total_bs > 0 else 0:.1f}%)
- Moderate (70-95%): {moderate_bs} branches ({moderate_bs/total_bs*100 if total_bs > 0 else 0:.1f}%)
- Weak (<70%): {weak_bs} branches ({weak_bs/total_bs*100 if total_bs > 0 else 0:.1f}%)
- Total branches: {total_bs}

"""
    
    if len(bootstrap_values) > 0:
        report += f"""**Bootstrap statistics:**
- Mean: {np.mean(bootstrap_values):.1f}%
- Median: {np.median(bootstrap_values):.1f}%
- Min: {np.min(bootstrap_values):.1f}%
- Max: {np.max(bootstrap_values):.1f}%

"""
    
    report += f"""![Bootstrap Distribution](figures/bootstrap_distribution.png)

*Figure 4: Distribution of bootstrap support values across all branches. Green line: strong support threshold (95%), Orange line: moderate support threshold (70%).*

---

## Quality Assessment

### Comparison with Published Standards

| Metric | This Study | Typical Range | Status |
|--------|-----------|---------------|--------|
| Sequences | {num_seqs} | 50-500 | {'✓ Good' if 50 <= num_seqs <= 500 else '⚠ Check'} |
| Alignment length | {aln_length} | 200-500 | {'✓ Good' if 200 <= aln_length <= 500 else '⚠ Check'} |
| Strong bootstrap | {strong_bs/total_bs*100 if total_bs > 0 else 0:.1f}% | >50% | {'✓ Excellent' if (strong_bs/total_bs if total_bs > 0 else 0) > 0.5 else '⚠ Check'} |
| Conserved positions | {len(highly_conserved)/len(df_cons)*100:.1f}% | 10-20% | {'✓ Good' if 0.1 <= len(highly_conserved)/len(df_cons) <= 0.2 else '⚠ Check'} |
| Coevolved pairs | {len(strong_coev)/len(df_coev)*100:.1f}% | 20-40% | {'✓ Good' if 0.2 <= len(strong_coev)/len(df_coev) <= 0.4 else '⚠ Check'} |

---

## Conclusions

### Key Findings

1. **High-quality dataset:** {num_seqs} non-redundant sequences after stringent quality control
2. **Conserved functional regions:** {len(highly_conserved)} highly conserved positions identified
3. **Coevolution networks:** {len(strong_coev)} coevolved pairs, {len(hubs)} hub positions
4. **Robust phylogeny:** {strong_bs}/{total_bs} ({strong_bs/total_bs*100 if total_bs > 0 else 0:.1f}%) branches with strong bootstrap support

### Recommendations for Protein Engineering

Based on conservation and coevolution analysis, the following positions are recommended for mutagenesis studies:

**Priority 1: Hub positions (both conserved AND highly connected)**
"""
    
    # Find positions that are both conserved and hubs
    hub_positions = [h[0] for h in hubs]
    conserved_positions = highly_conserved['position'].tolist()
    critical_positions = [p for p in hub_positions if p in conserved_positions]
    
    if len(critical_positions) > 0:
        report += "\n"
        for pos in critical_positions[:5]:
            aa = df_cons[df_cons['position'] == pos]['most_common_aa'].values[0]
            entropy = df_cons[df_cons['position'] == pos]['norm_entropy'].values[0]
            degree = next((d for p, d in hubs if p == pos), 0)
            report += f"- **Position {pos} ({aa}):** Entropy = {entropy:.3f}, Degree = {degree}\n"
    else:
        report += "\n(No positions are both highly conserved and hub)\n"
    
    report += f"""
**Priority 2: Highly conserved positions (entropy < 0.1)**

"""
    
    perfectly_conserved = df_cons[df_cons['norm_entropy'] < 0.1]
    for _, row in perfectly_conserved.head(5).iterrows():
        report += f"- **Position {int(row['position'])} ({row['most_common_aa']}):** Entropy = {row['norm_entropy']:.3f} (perfectly conserved)\n"
    
    report += f"""
---

## Methods

### Software

- **CD-HIT** v4.8.1 (redundancy removal)
- **MAFFT** v7.490 (alignment)
- **trimAl** v1.4 (trimming)
- **IQ-TREE** v2.0 (phylogeny)
- **Python** 3.8+ (BioPython, NumPy, Pandas, Matplotlib, NetworkX)

### Parameters

**Quality control:**
- CD-HIT threshold: 90%
- Gap threshold: <30%

**Conservation:**
- Shannon entropy threshold: <0.3 (highly conserved)

**Coevolution:**
- Mutual information threshold: >0.5 (strong coevolution)
- Hub threshold: degree ≥ 5

**Phylogeny:**
- Model selection: ModelFinder (AIC/BIC)
- Bootstrap: 1000 replicates (UFBoot2)
- Convergence: >0.99 required

---

## References

1. Li, W. & Godzik, A. (2006). "Cd-hit: a fast program for clustering and comparing large sets of protein or nucleotide sequences". *Bioinformatics* 22(13): 1658-1659.

2. Katoh, K. & Standley, D.M. (2013). "MAFFT multiple sequence alignment software version 7: improvements in performance and usability". *Mol Biol Evol* 30(4): 772-780.

3. Capella-Gutiérrez, S. et al. (2009). "trimAl: a tool for automated alignment trimming in large-scale phylogenetic analyses". *Bioinformatics* 25(15): 1972-1973.

4. Nguyen, L.T. et al. (2015). "IQ-TREE: A fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies". *Mol Biol Evol* 32(1): 268-274.

5. Dunn, S.D. et al. (2008). "Mutual information without the influence of phylogeny or entropy dramatically improves residue contact prediction". *Bioinformatics* 24(3): 333-340.

---

**Report generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Save report
    with open(f'{output_dir}/report.md', 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to: {output_dir}/report.md")

if __name__ == "__main__":
    main()
PYTHON_EOF

# Run report generation
python3 "$OUTPUT_DIR/generate_report.py" "$OUTPUT_DIR" "$FAMILY_NAME"

echo ""
echo "========================================="
echo "Report generation complete!"
echo "========================================="
echo "Output: $OUTPUT_DIR/report.md"
echo ""
echo "To convert to PDF:"
echo "  pandoc $OUTPUT_DIR/report.md -o $OUTPUT_DIR/report.pdf --pdf-engine=xelatex"
echo ""
echo "To convert to HTML:"
echo "  pandoc $OUTPUT_DIR/report.md -o $OUTPUT_DIR/report.html --standalone --toc"
echo ""
