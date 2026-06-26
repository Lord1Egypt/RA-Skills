# Coevolution Analysis - Normalized Mutual Information Method

## Overview

Coevolution analysis identifies pairs of residues that evolve together, indicating structural or functional coupling. When two positions coevolve, mutations at one position are compensated by mutations at the other to maintain protein function.

## Algorithm: Normalized Mutual Information (NMI)

### Mathematical Foundation

**Mutual Information (MI)** measures the statistical dependence between two alignment positions:

```
MI(X, Y) = Σ Σ p(x, y) × log₂[p(x, y) / (p(x) × p(y))]
```

Where:
- `X, Y`: Two alignment positions
- `x, y`: Amino acid types at positions X and Y
- `p(x, y)`: Joint probability of observing amino acids x and y together
- `p(x), p(y)`: Marginal probabilities of x and y independently
- `log₂`: Logarithm base 2

**Interpretation:**
- `MI = 0`: Positions are independent (no coevolution)
- `MI > 0`: Positions are dependent (coevolution)
- Higher MI → stronger coevolution

### Normalized Mutual Information

Raw MI is biased by entropy, so we normalize:

```
NMI(X, Y) = MI(X, Y) / sqrt(H(X) × H(Y))
```

Where:
- `H(X), H(Y)`: Shannon entropy of positions X and Y
- `NMI`: Normalized MI (range 0-1)

**Advantages of NMI:**
1. Corrects for entropy bias (conserved positions have low MI)
2. Makes different position pairs comparable
3. Range 0-1 is easier to interpret

**Threshold:**
- `NMI > 0.5`: Strong coevolution (likely functional coupling)
- `NMI 0.3-0.5`: Moderate coevolution
- `NMI < 0.3`: Weak or no coevolution

### Average Product Correction (APC)

To remove phylogenetic bias, we apply APC correction:

```
MI_APC(X, Y) = MI(X, Y) - [MI_avg(X) × MI_avg(Y)] / MI_avg_all
```

Where:
- `MI_avg(X)`: Average MI of position X with all other positions
- `MI_avg(Y)`: Average MI of position Y with all other positions
- `MI_avg_all`: Average MI across all position pairs

**Why APC?**
- Phylogenetic relationships create spurious correlations
- APC removes background correlation due to shared ancestry
- Improves specificity for true functional coupling

## Implementation

### Step 1: Calculate Joint Probabilities

```python
import numpy as np
from collections import Counter

def calculate_joint_prob(alignment, pos1, pos2):
    """Calculate joint probability distribution for two positions"""
    
    # Extract amino acid pairs
    pairs = []
    for record in alignment:
        aa1 = record.seq[pos1]
        aa2 = record.seq[pos2]
        # Skip if either position has a gap
        if aa1 != '-' and aa2 != '-':
            pairs.append((aa1, aa2))
    
    # Count frequencies
    pair_counts = Counter(pairs)
    total = len(pairs)
    
    # Calculate probabilities
    joint_prob = {pair: count/total for pair, count in pair_counts.items()}
    
    return joint_prob, pairs
```

### Step 2: Calculate Marginal Probabilities

```python
def calculate_marginal_prob(pairs):
    """Calculate marginal probabilities from pairs"""
    
    # Extract individual amino acids
    aa1_list = [pair[0] for pair in pairs]
    aa2_list = [pair[1] for pair in pairs]
    
    # Count frequencies
    aa1_counts = Counter(aa1_list)
    aa2_counts = Counter(aa2_list)
    
    total = len(pairs)
    
    # Calculate probabilities
    p_aa1 = {aa: count/total for aa, count in aa1_counts.items()}
    p_aa2 = {aa: count/total for aa, count in aa2_counts.items()}
    
    return p_aa1, p_aa2
```

### Step 3: Calculate Mutual Information

```python
def calculate_MI(joint_prob, p_aa1, p_aa2):
    """Calculate mutual information"""
    
    MI = 0
    for (aa1, aa2), p_xy in joint_prob.items():
        p_x = p_aa1[aa1]
        p_y = p_aa2[aa2]
        
        if p_xy > 0 and p_x > 0 and p_y > 0:
            MI += p_xy * np.log2(p_xy / (p_x * p_y))
    
    return MI
```

### Step 4: Calculate Normalized MI

```python
def calculate_entropy(prob_dist):
    """Calculate Shannon entropy"""
    H = 0
    for p in prob_dist.values():
        if p > 0:
            H -= p * np.log2(p)
    return H

def calculate_NMI(MI, H_X, H_Y):
    """Calculate normalized mutual information"""
    if H_X > 0 and H_Y > 0:
        NMI = MI / np.sqrt(H_X * H_Y)
    else:
        NMI = 0
    return NMI
```

### Step 5: Apply APC Correction

```python
def apply_APC(MI_matrix):
    """Apply Average Product Correction"""
    
    n_pos = MI_matrix.shape[0]
    
    # Calculate average MI for each position
    MI_avg = np.mean(MI_matrix, axis=1)
    
    # Calculate global average MI
    MI_avg_all = np.mean(MI_matrix)
    
    # Apply APC correction
    MI_APC = np.zeros_like(MI_matrix)
    for i in range(n_pos):
        for j in range(n_pos):
            if i != j:
                MI_APC[i, j] = MI_matrix[i, j] - (MI_avg[i] * MI_avg[j]) / MI_avg_all
    
    return MI_APC
```

### Step 6: Identify Coevolved Pairs

```python
def identify_coevolved_pairs(alignment, threshold=0.5):
    """Identify all coevolved position pairs"""
    
    aln_length = alignment.get_alignment_length()
    coevolved_pairs = []
    
    # Calculate MI for all pairs
    for i in range(aln_length):
        for j in range(i+1, aln_length):
            # Calculate joint and marginal probabilities
            joint_prob, pairs = calculate_joint_prob(alignment, i, j)
            p_aa1, p_aa2 = calculate_marginal_prob(pairs)
            
            # Calculate MI
            MI = calculate_MI(joint_prob, p_aa1, p_aa2)
            
            # Calculate entropies
            H_X = calculate_entropy(p_aa1)
            H_Y = calculate_entropy(p_aa2)
            
            # Calculate NMI
            NMI = calculate_NMI(MI, H_X, H_Y)
            
            # Store if above threshold
            if NMI > threshold:
                coevolved_pairs.append({
                    'pos1': i + 1,
                    'pos2': j + 1,
                    'MI': MI,
                    'NMI': NMI,
                    'num_pairs': len(pairs)
                })
    
    # Sort by NMI score
    coevolved_pairs.sort(key=lambda x: x['NMI'], reverse=True)
    
    return coevolved_pairs
```

## Biological Interpretation

### Strong Coevolution (NMI > 0.5)

**Likely mechanisms:**

1. **Structural contacts** (< 8 Å distance in 3D structure)
   - Direct physical interaction
   - Maintain protein fold stability
   - Example: Hydrophobic core residues

2. **Functional coupling** (active site residues)
   - Catalytic triad coordination
   - Substrate binding pocket
   - Example: Ser-His-Asp in serine proteases

3. **Allosteric networks** (long-range communication)
   - Signal transduction pathways
   - Conformational changes
   - Example: Kinase activation loops

4. **Compensatory mutations** (maintain charge balance)
   - Salt bridge partners
   - Electrostatic interactions
   - Example: Arg-Asp pairs

### Example: Example Protein Family

**Top coevolved pairs:**

```
Position 14 ↔ 34: NMI = 0.625
- Position 14 (G): Rossmann fold, NADPH binding
- Position 34 (T): Structural support
- Mechanism: Structural coupling for cofactor binding

Position 18 ↔ 92: NMI = 0.614
- Position 18 (A): Hydrophobic core
- Position 92 (E): Catalytic network
- Mechanism: Hydrophobic-charged interface stability

Position 117 ↔ 156: NMI = 0.579
- Position 117 (D): Substrate binding
- Position 156 (N): Polar network
- Mechanism: Substrate specificity determination
```

## Network Analysis

### Building Coevolution Network

**Nodes:** Alignment positions  
**Edges:** Coevolved pairs (NMI > 0.5)  
**Edge weight:** NMI score

```python
import networkx as nx

def build_coevolution_network(coevolved_pairs, threshold=0.5):
    """Build coevolution network graph"""
    
    G = nx.Graph()
    
    for pair in coevolved_pairs:
        if pair['NMI'] > threshold:
            G.add_edge(pair['pos1'], pair['pos2'], weight=pair['NMI'])
    
    return G
```

### Hub Identification

**Hub:** Position with high degree (many coevolution partners)

```python
def identify_hubs(G, min_degree=5):
    """Identify hub positions in coevolution network"""
    
    degrees = dict(G.degree())
    hubs = {pos: deg for pos, deg in degrees.items() if deg >= min_degree}
    
    # Sort by degree
    hubs = sorted(hubs.items(), key=lambda x: x[1], reverse=True)
    
    return hubs
```

**Biological significance of hubs:**
- Central to protein function
- Mutations likely to be deleterious
- Prime targets for protein engineering
- Often catalytic or binding residues

### Community Detection

**Community:** Cluster of highly interconnected positions

```python
def detect_communities(G):
    """Detect communities in coevolution network"""
    
    from networkx.algorithms import community
    
    # Louvain algorithm
    communities = community.louvain_communities(G, seed=42)
    
    return communities
```

**Biological significance:**
- Functional modules (e.g., active site, binding pocket)
- Structural domains
- Allosteric pathways

## Visualization

### 1. Coevolution Network Graph

```python
import matplotlib.pyplot as plt
import networkx as nx

def plot_coevolution_network(G, hubs):
    """Plot coevolution network with hub highlighting"""
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Layout
    pos = nx.spring_layout(G, k=0.5, iterations=50, seed=42)
    
    # Node colors (hubs in red)
    node_colors = ['red' if node in [h[0] for h in hubs] else 'lightblue' 
                   for node in G.nodes()]
    
    # Node sizes (proportional to degree)
    node_sizes = [G.degree(node) * 50 for node in G.nodes()]
    
    # Edge widths (proportional to NMI)
    edge_widths = [G[u][v]['weight'] * 3 for u, v in G.edges()]
    
    # Draw network
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                           node_size=node_sizes, alpha=0.7, ax=ax)
    nx.draw_networkx_edges(G, pos, width=edge_widths, 
                           alpha=0.3, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
    
    ax.set_title('Coevolution Network (NMI > 0.5)', fontsize=16)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig('coevolution_network.png', dpi=300)
```

### 2. Hub Heatmap

```python
import seaborn as sns

def plot_hub_heatmap(coevolved_pairs, hubs):
    """Plot heatmap of hub positions and their partners"""
    
    # Extract hub positions
    hub_positions = [h[0] for h in hubs[:10]]  # Top 10 hubs
    
    # Build matrix
    matrix = np.zeros((len(hub_positions), len(hub_positions)))
    
    for pair in coevolved_pairs:
        if pair['pos1'] in hub_positions and pair['pos2'] in hub_positions:
            i = hub_positions.index(pair['pos1'])
            j = hub_positions.index(pair['pos2'])
            matrix[i, j] = pair['NMI']
            matrix[j, i] = pair['NMI']
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(matrix, cmap='YlOrRd', 
                xticklabels=hub_positions, 
                yticklabels=hub_positions,
                cbar_kws={'label': 'NMI Score'},
                ax=ax)
    ax.set_title('Hub Position Coevolution Heatmap', fontsize=16)
    plt.tight_layout()
    plt.savefig('hub_heatmap.png', dpi=300)
```

### 3. MI Distribution

```python
def plot_MI_distribution(coevolved_pairs):
    """Plot distribution of MI scores"""
    
    MI_scores = [pair['MI'] for pair in coevolved_pairs]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(MI_scores, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax.axvline(x=0.5, color='red', linestyle='--', 
               label='Strong coevolution threshold')
    ax.set_xlabel('Mutual Information (MI)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Distribution of Coevolution Scores', fontsize=14)
    ax.legend()
    plt.tight_layout()
    plt.savefig('MI_distribution.png', dpi=300)
```

## Quality Control

### Reliable Coevolution Analysis Requires:

1. **Sufficient sequences** (≥ 100 recommended, ≥ 200 ideal)
   - Too few: Spurious correlations
   - Statistical power increases with sample size

2. **Phylogenetic diversity** (avoid overrepresentation)
   - Use CD-HIT clustering (70-90% identity)
   - Apply sequence weighting
   - Use APC correction

3. **High-quality alignment** (gap ratio < 30%)
   - Misalignment creates false coevolution signals
   - Use structural alignment when possible

4. **Sufficient variability** (avoid perfectly conserved positions)
   - Conserved positions have low MI by definition
   - Focus on moderately conserved positions

## Common Pitfalls

### Pitfall 1: Phylogenetic Bias

**Problem:** Closely related sequences create spurious correlations

**Solution:**
- Apply APC correction
- Use CD-HIT to remove redundancy
- Weight sequences by phylogenetic distance

### Pitfall 2: Alignment Errors

**Problem:** Misaligned positions appear to coevolve

**Solution:**
- Manually inspect high-scoring pairs
- Validate with 3D structure (if available)
- Use structural alignment (DALI, TM-align)

### Pitfall 3: Transitive Correlations

**Problem:** A→B and B→C creates spurious A→C correlation

**Solution:**
- Use partial correlation analysis
- Apply APC correction
- Validate with network analysis

### Pitfall 4: Small Sample Size

**Problem:** Unreliable MI estimates with < 50 sequences

**Solution:**
- Collect more sequences
- Use Bayesian MI estimation
- Report confidence intervals

## Advanced Methods

### 1. Direct Coupling Analysis (DCA)

More sophisticated method that removes indirect correlations:

```
E(X, Y) = -Σ Σ J_ij(x_i, y_j) × δ(x_i, X) × δ(y_j, Y)
```

Where:
- `J_ij`: Coupling matrix (learned by maximum entropy model)
- `δ`: Indicator function

**Advantages:**
- Removes transitive correlations
- Better for structure prediction
- More computationally intensive

**Tools:** EVcouplings, plmc, CCMpred

### 2. Partial Correlation

Removes indirect correlations through intermediate positions:

```
ρ_XY|Z = (ρ_XY - ρ_XZ × ρ_YZ) / sqrt((1 - ρ_XZ²) × (1 - ρ_YZ²))
```

Where:
- `ρ_XY|Z`: Partial correlation of X and Y given Z
- `ρ_XY`: Correlation between X and Y

### 3. Phylogenetic Weighting

Henikoff & Henikoff weighting to correct for phylogenetic bias:

```
w_i = Σ (1 / (r_k × s_k))
```

Applied before calculating MI.

## Output Files

### coevolution_pairs.csv

```csv
pos1,pos2,MI,NMI,num_pairs,gap1,gap2
19,40,0.625,0.812,450,0.013,0.000
23,110,0.614,0.798,450,0.011,0.002
...
```

### hub_positions.txt

```
Hub Positions (degree ≥ 5)
==========================
Position 14: Degree 8
Position 92: Degree 6
Position 117: Degree 5
...
```

### network_data.json

```json
{
  "nodes": [
    {"id": 14, "degree": 8, "hub": true},
    {"id": 92, "degree": 6, "hub": true},
    ...
  ],
  "edges": [
    {"source": 14, "target": 34, "weight": 0.625},
    {"source": 18, "target": 92, "weight": 0.614},
    ...
  ]
}
```

## Validation with 3D Structure

If crystal structure is available, validate coevolution predictions:

```python
def validate_with_structure(coevolved_pairs, pdb_file, distance_threshold=8.0):
    """Validate coevolution with 3D structure"""
    
    from Bio.PDB import PDBParser
    
    parser = PDBParser()
    structure = parser.get_structure('protein', pdb_file)
    
    validated_pairs = []
    
    for pair in coevolved_pairs:
        pos1 = pair['pos1']
        pos2 = pair['pos2']
        
        # Get Cα atoms
        ca1 = structure[0]['A'][pos1]['CA']
        ca2 = structure[0]['A'][pos2]['CA']
        
        # Calculate distance
        distance = ca1 - ca2
        
        # Validate
        if distance < distance_threshold:
            validated_pairs.append({
                **pair,
                'distance': distance,
                'validated': True
            })
    
    return validated_pairs
```

**Expected validation rate:**
- 30-50% of top coevolved pairs are in contact (< 8 Å)
- Higher for DCA methods (60-80%)
- Lower for long-range allosteric coupling

## References

1. Dunn, S.D. et al. (2008). "Mutual information without the influence of phylogeny or entropy dramatically improves residue contact prediction". *Bioinformatics* 24(3): 333-340.

2. Marks, D.S. et al. (2011). "Protein 3D structure computed from evolutionary sequence variation". *PLoS ONE* 6(12): e28766.

3. Morcos, F. et al. (2011). "Direct-coupling analysis of residue coevolution captures native contacts across many protein families". *PNAS* 108(49): E1293-E1301.

4. Weigt, M. et al. (2009). "Identification of direct residue contacts in protein-protein interaction by message passing". *PNAS* 106(1): 67-72.

## See Also

- [Conservation Analysis](02-conservation.md) - Identify conserved residues
- [Phylogenetic Analysis](04-phylogeny.md) - Build evolutionary tree
