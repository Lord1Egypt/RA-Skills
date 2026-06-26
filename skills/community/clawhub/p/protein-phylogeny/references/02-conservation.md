# Conservation Analysis - Shannon Entropy Method

## Overview

Conservation analysis identifies functionally important residues by measuring sequence variability at each alignment position. Highly conserved positions (low entropy) typically indicate structural or catalytic importance.

## Algorithm: Shannon Entropy

### Mathematical Foundation

**Shannon entropy** measures the uncertainty or variability of amino acid distribution at each position:

```
H(X) = -Σ p(x_i) × log₂(p(x_i))
```

Where:
- `X`: Alignment position
- `x_i`: The i-th amino acid type (20 standard amino acids)
- `p(x_i)`: Frequency of amino acid x_i at position X
- `log₂`: Logarithm base 2 (information theory standard)

### Normalized Entropy

To make entropy comparable across positions, we normalize by the maximum possible entropy:

```
H_norm(X) = H(X) / log₂(N)
```

Where:
- `N`: Number of possible amino acid types (typically 20)
- `H_norm`: Normalized entropy (range 0-1)

**Interpretation:**
- `H_norm = 0`: Perfectly conserved (all sequences have same amino acid)
- `H_norm = 1`: Maximally variable (all amino acids equally frequent)
- `H_norm < 0.3`: Highly conserved (functional importance likely)
- `H_norm 0.3-0.6`: Moderately conserved
- `H_norm > 0.6`: Variable (less functionally constrained)

### Gap Handling

Gaps are treated as a 21st character type:

```
H_gap(X) = -Σ p(x_i) × log₂(p(x_i)) - p(gap) × log₂(p(gap))
H_norm_gap(X) = H_gap(X) / log₂(21)
```

**Gap ratio** is calculated separately:
```
gap_ratio(X) = count(gaps) / total_sequences
```

Positions with `gap_ratio > 0.3` are flagged as unreliable.

## Implementation

### Step 1: Read Alignment

```python
from Bio import AlignIO
import numpy as np

alignment = AlignIO.read("aligned.fasta", "fasta")
num_seqs = len(alignment)
aln_length = alignment.get_alignment_length()
```

### Step 2: Calculate Entropy for Each Position

```python
def calculate_entropy(alignment, position):
    """Calculate Shannon entropy at a given position"""
    
    # Count amino acid frequencies
    aa_counts = {}
    for record in alignment:
        aa = record.seq[position]
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    
    # Calculate probabilities
    total = sum(aa_counts.values())
    aa_probs = {aa: count/total for aa, count in aa_counts.items()}
    
    # Calculate entropy
    entropy = 0
    for prob in aa_probs.values():
        if prob > 0:
            entropy -= prob * np.log2(prob)
    
    # Normalize
    max_entropy = np.log2(len(aa_probs))
    norm_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    return entropy, norm_entropy, aa_counts
```

### Step 3: Identify Conserved Positions

```python
conserved_positions = []

for pos in range(aln_length):
    entropy, norm_entropy, aa_counts = calculate_entropy(alignment, pos)
    
    # Calculate gap ratio
    gap_count = aa_counts.get('-', 0)
    gap_ratio = gap_count / num_seqs
    
    # Classify conservation
    if norm_entropy < 0.3 and gap_ratio < 0.3:
        # Highly conserved
        most_common_aa = max(aa_counts, key=aa_counts.get)
        conserved_positions.append({
            'position': pos + 1,
            'entropy': entropy,
            'norm_entropy': norm_entropy,
            'most_common_aa': most_common_aa,
            'gap_ratio': gap_ratio
        })
```

### Step 4: Output Results

```python
import pandas as pd

# Save to CSV
df = pd.DataFrame(conserved_positions)
df.to_csv('conservation.csv', index=False)

# Print summary
print(f"Total positions: {aln_length}")
print(f"Highly conserved (H < 0.3): {len(conserved_positions)}")
print(f"Moderately conserved (0.3 ≤ H < 0.6): {count_moderate}")
print(f"Variable (H ≥ 0.6): {count_variable}")
```

## Biological Interpretation

### Highly Conserved Positions (H < 0.3)

**Likely functional roles:**
1. **Catalytic residues** (e.g., Ser-His-Asp triad in serine proteases)
2. **Substrate binding** (e.g., active site residues)
3. **Cofactor binding** (e.g., NAD(P)H binding motifs)
4. **Structural integrity** (e.g., disulfide bonds, metal coordination)
5. **Protein-protein interfaces** (e.g., oligomerization sites)

**Example: Rossmann Fold**
```
Position 9-15: GxGxxG motif (NADPH binding)
- Position 9 (G): H = 0.000 (perfectly conserved)
- Position 10 (I): H = 0.005 (nearly conserved)
- Position 14 (G): H = 0.279 (highly conserved)
- Position 15 (S): H = 0.005 (nearly conserved)
```

### Moderately Conserved Positions (0.3 ≤ H < 0.6)

**Likely roles:**
1. **Substrate specificity** (determines which substrates are accepted)
2. **Regulatory sites** (allosteric regulation)
3. **Surface loops** (protein recognition)

### Variable Positions (H ≥ 0.6)

**Likely roles:**
1. **Surface residues** (no functional constraint)
2. **Linker regions** (flexible loops)
3. **Species-specific adaptations**

## Conservation Patterns

### Pattern 1: Catalytic Triad

Example: Serine protease
```
Position 57 (S): H = 0.000 (catalytic nucleophile)
Position 102 (H): H = 0.000 (proton shuttle)
Position 195 (D): H = 0.000 (charge stabilization)
```

### Pattern 2: Binding Pocket

Example: ATP binding site
```
Position 15-22: GxGxxGxT motif (phosphate binding)
Position 50-55: DFG motif (Mg²⁺ coordination)
Position 166 (E): H = 0.000 (catalytic base)
```

### Pattern 3: Structural Motif

Example: Zinc finger
```
Position 10 (C): H = 0.000 (Zn²⁺ coordination)
Position 13 (C): H = 0.000 (Zn²⁺ coordination)
Position 27 (H): H = 0.000 (Zn²⁺ coordination)
Position 31 (H): H = 0.000 (Zn²⁺ coordination)
```

## Visualization

### 1. Conservation Heatmap

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Create heatmap
fig, ax = plt.subplots(figsize=(20, 4))
sns.heatmap(entropy_matrix, cmap='RdYlGn_r', 
            cbar_kws={'label': 'Normalized Entropy'},
            xticklabels=50, yticklabels=False)
ax.set_xlabel('Alignment Position')
ax.set_ylabel('Sequences')
ax.set_title('Conservation Landscape')
plt.tight_layout()
plt.savefig('conservation_heatmap.png', dpi=300)
```

### 2. Conservation Profile

```python
# Line plot of entropy across positions
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(positions, norm_entropies, linewidth=1, color='steelblue')
ax.axhline(y=0.3, color='red', linestyle='--', label='Highly conserved threshold')
ax.fill_between(positions, 0, norm_entropies, 
                 where=(norm_entropies < 0.3), 
                 alpha=0.3, color='green', label='Highly conserved')
ax.set_xlabel('Alignment Position')
ax.set_ylabel('Normalized Entropy')
ax.set_title('Conservation Profile')
ax.legend()
plt.tight_layout()
plt.savefig('conservation_profile.png', dpi=300)
```

### 3. Gap vs Conservation Scatter

```python
# Scatter plot: gap ratio vs entropy
fig, ax = plt.subplots(figsize=(8, 6))
scatter = ax.scatter(gap_ratios, norm_entropies, 
                     c=norm_entropies, cmap='RdYlGn_r',
                     alpha=0.6, s=20)
ax.axhline(y=0.3, color='red', linestyle='--', label='Conservation threshold')
ax.axvline(x=0.3, color='blue', linestyle='--', label='Gap threshold')
ax.set_xlabel('Gap Ratio')
ax.set_ylabel('Normalized Entropy')
ax.set_title('Gap Ratio vs Conservation')
ax.legend()
plt.colorbar(scatter, label='Normalized Entropy')
plt.tight_layout()
plt.savefig('gap_vs_conservation.png', dpi=300)
```

## Quality Control

### Reliable Conservation Analysis Requires:

1. **Sufficient sequences** (≥ 50 recommended, ≥ 100 ideal)
   - Too few: Entropy estimates unreliable
   - Too many: Computational cost increases

2. **High-quality alignment** (gap ratio < 30%)
   - Poor alignment → incorrect conservation estimates
   - Use MAFFT L-INS-i or MUSCLE for accuracy

3. **Homologous sequences** (≥ 25% identity)
   - Too divergent: Alignment unreliable
   - Too similar: No evolutionary signal

4. **Balanced sampling** (avoid overrepresentation)
   - Use CD-HIT to remove redundancy
   - Aim for 70-90% identity clustering

## Common Pitfalls

### Pitfall 1: Ignoring Gaps

**Problem:** Gaps can inflate entropy estimates

**Solution:** 
- Calculate gap ratio separately
- Exclude positions with gap_ratio > 0.3
- Use gap-aware entropy formula

### Pitfall 2: Small Sample Size

**Problem:** Entropy estimates unstable with < 20 sequences

**Solution:**
- Collect more sequences
- Use Bayesian entropy estimation
- Report confidence intervals

### Pitfall 3: Alignment Errors

**Problem:** Misaligned positions appear variable

**Solution:**
- Manually inspect conserved regions
- Use structural alignment (DALI, TM-align)
- Validate with 3D structure

### Pitfall 4: Phylogenetic Bias

**Problem:** Overrepresentation of certain clades

**Solution:**
- Weight sequences by phylogenetic distance
- Use CD-HIT clustering
- Apply sequence weighting (Henikoff & Henikoff)

## Advanced Methods

### 1. Relative Entropy (Kullback-Leibler Divergence)

Measures deviation from background amino acid frequencies:

```
D_KL(P || Q) = Σ p(x_i) × log₂[p(x_i) / q(x_i)]
```

Where:
- `P`: Observed amino acid distribution at position
- `Q`: Background amino acid frequencies (e.g., from UniProt)

**Use case:** Identify positions with unusual amino acid preferences

### 2. Jensen-Shannon Divergence

Symmetric version of KL divergence:

```
JSD(P || Q) = 0.5 × D_KL(P || M) + 0.5 × D_KL(Q || M)
M = 0.5 × (P + Q)
```

**Use case:** Compare conservation between subfamilies

### 3. Sequence Weighting

Henikoff & Henikoff position-based weighting:

```
w_i = Σ (1 / (r_k × s_k))
```

Where:
- `w_i`: Weight for sequence i
- `r_k`: Number of different amino acids at position k
- `s_k`: Number of sequences with same amino acid as sequence i at position k

**Use case:** Correct for phylogenetic bias

## Output Files

### conservation.csv

```csv
position,entropy,norm_entropy,most_common_aa,most_common_freq,gap_ratio,num_variants,category
1,0.135,0.031,M,0.95,0.02,3,Highly conserved
2,0.146,0.034,K,0.93,0.03,4,Highly conserved
...
```

### conservation_summary.txt

```
Conservation Analysis Summary
=============================
Total positions: 259
Highly conserved (H < 0.3): 32 (12.4%)
Moderately conserved (0.3 ≤ H < 0.6): 105 (40.5%)
Variable (H ≥ 0.6): 122 (47.1%)

Top 10 conserved positions:
Position 9 (G): H = 0.000
Position 10 (I): H = 0.005
Position 15 (S): H = 0.005
...
```

## References

1. Shannon, C.E. (1948). "A Mathematical Theory of Communication". *Bell System Technical Journal* 27: 379-423.

2. Valdar, W.S. (2002). "Scoring residue conservation". *Proteins* 48(2): 227-241.

3. Capra, J.A. & Singh, M. (2007). "Predicting functionally important residues from sequence conservation". *Bioinformatics* 23(15): 1875-1882.

4. Henikoff, S. & Henikoff, J.G. (1994). "Position-based sequence weights". *J Mol Biol* 243(4): 574-578.

## See Also

- [Quality Control](01-quality-control.md) - Prepare high-quality alignment
- [Coevolution Analysis](03-coevolution.md) - Identify residue coupling
