# Phylogenetic Analysis - Maximum Likelihood Method

## Overview

Phylogenetic analysis reconstructs evolutionary relationships among protein sequences, revealing how proteins diverged from common ancestors. This information is crucial for understanding functional evolution, identifying subfamilies, and predicting protein properties.

## Algorithm: Maximum Likelihood (ML)

### Mathematical Foundation

Maximum likelihood finds the tree topology and branch lengths that maximize the probability of observing the given sequence data:

```
L(T, θ | D) = P(D | T, θ)
```

Where:
- `L`: Likelihood
- `T`: Tree topology
- `θ`: Model parameters (substitution rates, branch lengths)
- `D`: Observed sequence data

**Goal:** Find `T` and `θ` that maximize `L`

### Substitution Models

Amino acid substitution models describe the probability of one amino acid changing to another over evolutionary time.

#### 1. JTT Model (Jones-Taylor-Thornton)

Empirical model based on observed substitutions:

```
P(j | i, t) = Σ π_j × Q_ij × exp(λ_k × t)
```

Where:
- `P(j | i, t)`: Probability of amino acid i changing to j in time t
- `π_j`: Equilibrium frequency of amino acid j
- `Q_ij`: Instantaneous substitution rate from i to j
- `λ_k`: Eigenvalue of rate matrix
- `t`: Branch length (evolutionary time)

**Use case:** General protein evolution

#### 2. WAG Model (Whelan-And-Goldman)

Improved empirical model with better fit for globular proteins:

```
Q_ij = π_j × S_ij
```

Where:
- `S_ij`: Exchangeability parameter (symmetric)
- Estimated from large protein database

**Use case:** Most protein families (recommended default)

#### 3. LG Model (Le-Gascuel)

Most recent empirical model with best overall performance:

```
Q_ij = π_j × S_ij × f(site)
```

Where:
- `f(site)`: Site-specific rate variation

**Use case:** Large diverse protein families

### Rate Heterogeneity

Real proteins evolve at different rates across sites. We model this with:

#### Gamma Distribution (+G)

```
P(rate = r) = Γ(α, β)
```

Where:
- `α`: Shape parameter (typically 4-8 categories)
- Lower α → more rate variation

**Notation:** `WAG+G4` (WAG model with 4 gamma categories)

#### Invariant Sites (+I)

Some sites never change:

```
P(site invariant) = p_inv
```

**Notation:** `WAG+I+G4` (WAG with invariant sites and gamma)

### Model Selection

**ModelFinder** algorithm tests all models and selects best by:

1. **Akaike Information Criterion (AIC)**
   ```
   AIC = -2 × ln(L) + 2 × k
   ```
   Where `k` = number of parameters

2. **Bayesian Information Criterion (BIC)**
   ```
   BIC = -2 × ln(L) + k × ln(n)
   ```
   Where `n` = number of sequences

**Best model:** Lowest AIC/BIC

## Implementation: IQ-TREE

### Step 1: Prepare Input

```bash
# Input: Multiple sequence alignment (FASTA format)
# Requirements:
# - High-quality alignment (MAFFT L-INS-i)
# - Trimmed (trimAl -automated1)
# - Non-redundant (CD-HIT 90%)
# - ≥ 50 sequences (≥ 100 recommended)

# Check alignment quality
iqtree2 -s aligned.fasta --check
```

### Step 2: Model Selection

```bash
# Automatic model selection with ModelFinder
iqtree2 -s aligned.fasta -m MFP -nt AUTO

# Output: Best model (e.g., WAG+I+G4)
```

**Common models for proteins:**
- `WAG+I+G4`: General proteins
- `LG+I+G4`: Large diverse families
- `JTT+I+G4`: Older standard
- `Q.pfam+I+G4`: Pfam database-derived

### Step 3: Tree Search

```bash
# Maximum likelihood tree search
iqtree2 -s aligned.fasta -m WAG+I+G4 -nt AUTO -seed 12345

# Parameters:
# -m: Substitution model
# -nt AUTO: Automatic thread detection
# -seed: Random seed (for reproducibility)
```

**Tree search algorithm:**
1. Generate initial tree (neighbor-joining or parsimony)
2. Optimize branch lengths
3. Test tree rearrangements (NNI, SPR)
4. Accept if likelihood improves
5. Repeat until convergence

### Step 4: Bootstrap Analysis

**Purpose:** Assess confidence in tree topology

**UFBoot2 (Ultrafast Bootstrap):**
```bash
iqtree2 -s aligned.fasta -m WAG+I+G4 -bb 1000 -nt AUTO -seed 12345

# Parameters:
# -bb 1000: 1000 bootstrap replicates
# -seed: Fixed seed for reproducibility
```

**Bootstrap procedure:**
1. Resample alignment columns with replacement
2. Build tree from resampled data
3. Repeat 1000 times
4. Count how often each branch appears

**Bootstrap support:**
- ≥ 95%: Strong support (highly confident)
- 70-95%: Moderate support (reasonably confident)
- < 70%: Weak support (uncertain)

### Step 5: Convergence Check

```bash
# Check bootstrap convergence
iqtree2 -s aligned.fasta -m WAG+I+G4 -bb 1000 -wbtl -nt AUTO

# Output: Bootstrap convergence value
# Required: > 0.99 (99% convergence)
```

**Convergence criterion:**
```
C = 1 - (SD / mean)
```

Where:
- `SD`: Standard deviation of bootstrap support values
- `mean`: Mean bootstrap support

**If C < 0.99:**
- Increase bootstrap replicates (2000+)
- Check alignment quality
- Consider different substitution model

### Step 6: Tree Visualization

```bash
# Generate tree figure
# (Use R, Python, or FigTree)
```

## Tree Interpretation

### Branch Lengths

**Meaning:** Expected number of substitutions per site

```
Branch length = 0.1 → 10% of sites changed
Branch length = 1.0 → 100% of sites changed (saturation)
```

**Long branches indicate:**
- Rapid evolution
- Ancient divergence
- Positive selection
- Relaxed functional constraints

**Short branches indicate:**
- Recent divergence
- Slow evolution
- Strong purifying selection
- Functional constraints

### Bootstrap Support

**Interpretation:**
- **95-100%:** Highly reliable, publish with confidence
- **70-95%:** Moderately reliable, mention uncertainty
- **50-70%:** Weak support, polytomy likely
- **< 50%:** Unreliable, collapse to polytomy

### Tree Topology

**Monophyletic clade:** All descendants of common ancestor
- Indicates functional subfamily
- Shared biochemical properties
- Example: Clade A vs Clade B

**Paraphyletic group:** Some descendants excluded
- May indicate incomplete sampling
- Or convergent evolution

**Polyphyletic group:** Multiple independent origins
- Indicates convergent evolution
- Or misalignment

## Quality Assessment

### 1. Log-Likelihood

```
ln(L) = -50000 (typical for 100 sequences, 300 sites)
```

**Higher (less negative) is better**

### 2. Tree Length

```
Total tree length = Σ all branch lengths
```

**Typical range:** 5-50 substitutions per site

**Too short (< 1):** Sequences too similar, little phylogenetic signal  
**Too long (> 100):** Sequences too divergent, saturation

### 3. Substitution Saturation

**Test:** Plot pairwise distance vs tree distance

```python
import matplotlib.pyplot as plt

# If linear: No saturation
# If plateau: Saturation (unreliable tree)
plt.scatter(pairwise_dist, tree_dist)
plt.xlabel('Pairwise Distance')
plt.ylabel('Tree Distance')
```

**If saturated:**
- Use amino acid properties (Dayhoff groups)
- Focus on conserved regions only
- Consider structural alignment

### 4. Compositional Heterogeneity

**Test:** Chi-square test for amino acid composition

```
χ² = Σ (observed - expected)² / expected
```

**If significant (p < 0.05):**
- Sequences have different amino acid compositions
- May violate model assumptions
- Use composition-heterogeneous models (e.g., `C10` to `C60`)

## Visualization

### 1. Rectangular Tree

```R
library(ape)
library(phytools)

# Read tree
tree <- read.tree("tree.treefile")

# Plot
pdf("phylogenetic_tree.pdf", width=12, height=20)
plot(tree, type="phylogram", cex=0.6, 
     edge.width=2, label.offset=0.01)
add.scale.bar()
nodelabels(tree$node.label, cex=0.5, bg="white", frame="circle")
dev.off()
```

### 2. Circular Tree

```R
# Circular layout (better for large trees)
pdf("circular_tree.pdf", width=15, height=15)
plot(tree, type="fan", cex=0.5, 
     edge.width=1.5, label.offset=0.02)
add.scale.bar()
dev.off()
```

### 3. Bootstrap Heatmap

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Extract bootstrap values
bootstrap_values = [...]  # From tree file

# Plot distribution
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(bootstrap_values, bins=20, color='steelblue', edgecolor='black')
ax.axvline(x=95, color='red', linestyle='--', label='Strong support threshold')
ax.axvline(x=70, color='orange', linestyle='--', label='Moderate support threshold')
ax.set_xlabel('Bootstrap Support (%)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Bootstrap Support Distribution', fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig('bootstrap_distribution.png', dpi=300)
```

### 4. Tree Depth Distribution

```python
# Calculate tree depth for each sequence
from Bio import Phylo

tree = Phylo.read("tree.treefile", "newick")
depths = []

for leaf in tree.get_terminals():
    depth = tree.distance(tree.root, leaf)
    depths.append(depth)

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(depths, bins=30, color='forestgreen', edgecolor='black')
ax.set_xlabel('Tree Depth (substitutions/site)', fontsize=12)
ax.set_ylabel('Frequency', fontsize=12)
ax.set_title('Tree Depth Distribution', fontsize=14)
plt.tight_layout()
plt.savefig('tree_depth_distribution.png', dpi=300)
```

## Common Pitfalls

### Pitfall 1: Long-Branch Attraction (LBA)

**Problem:** Fast-evolving sequences cluster together artificially

**Symptoms:**
- Unexpected groupings
- Long branches clustering
- Low bootstrap support

**Solutions:**
- Remove fast-evolving sequences
- Use site-heterogeneous models (e.g., `CAT` model)
- Try Bayesian methods (MrBayes)

### Pitfall 2: Insufficient Phylogenetic Signal

**Problem:** Sequences too similar or too divergent

**Symptoms:**
- Low bootstrap support throughout tree
- Star-like topology (polytomy)
- Very short or very long branches

**Solutions:**
- Add more sequences
- Use conserved regions only
- Consider alternative markers

### Pitfall 3: Model Misspecification

**Problem:** Wrong substitution model

**Symptoms:**
- Poor model fit (high AIC/BIC)
- Unrealistic branch lengths
- Low bootstrap support

**Solutions:**
- Use ModelFinder for automatic selection
- Try multiple models and compare
- Use mixture models (e.g., `LG+C20+F+G`)

### Pitfall 4: Alignment Errors

**Problem:** Misaligned sequences

**Symptoms:**
- Extremely long branches
- Unexpected topology
- Low bootstrap support

**Solutions:**
- Manually inspect alignment
- Use structural alignment (DALI, TM-align)
- Remove poorly aligned regions (trimAl)

## Advanced Methods

### 1. Bayesian Inference (MrBayes)

**Advantages:**
- Accounts for uncertainty in tree and parameters
- Posterior probabilities (more conservative than bootstrap)
- Better for complex models

**Disadvantages:**
- Computationally intensive
- Requires convergence diagnostics
- Longer runtime

```bash
# MrBayes example
mb
> execute aligned.fasta
> lset nst=6 rates=invgamma
> mcmc ngen=1000000 samplefreq=100
> sumt burnin=2500
```

### 2. Approximately Unbiased (AU) Test

**Purpose:** Test alternative tree topologies

```bash
# Generate alternative trees
iqtree2 -s aligned.fasta -m WAG+I+G4 -z alternative_trees.nwk -au

# Output: p-values for each tree
# p > 0.05: Cannot reject tree
```

### 3. Partition Models

For multi-domain proteins:

```bash
# Define partitions
# partition.nex:
# charset domain1 = 1-100;
# charset domain2 = 101-300;

iqtree2 -s aligned.fasta -p partition.nex -m MFP -bb 1000
```

### 4. Constrained Tree Search

Force monophyly of certain groups:

```bash
# constraint.nwk: (seq1, seq2, seq3);
iqtree2 -s aligned.fasta -m WAG+I+G4 -g constraint.nwk -bb 1000
```

## Output Files

### tree.treefile

Newick format tree with branch lengths:
```
((seq1:0.05,seq2:0.03)95:0.10,(seq3:0.08,seq4:0.06)88:0.12);
```

Numbers after `)` are bootstrap support values.

### tree.iqtree

Complete analysis log:
```
Model: WAG+I+G4
Log-likelihood: -50234.567
Tree length: 12.345
Bootstrap convergence: 0.992
```

### tree.contree

Consensus tree (majority-rule):
```
Only branches appearing in > 50% of bootstrap trees
```

## Validation

### Cross-Validation

1. **Split alignment** into training and test sets
2. **Build tree** on training set
3. **Predict** test set sequences
4. **Compare** predicted vs actual placement

### Comparison with Known Phylogeny

If reference phylogeny exists:

```python
from Bio import Phylo

# Robinson-Foulds distance
def RF_distance(tree1, tree2):
    """Calculate topological distance between trees"""
    # Number of bipartitions unique to each tree
    return len(set(tree1.bipartitions) ^ set(tree2.bipartitions))
```

**RF = 0:** Identical topology  
**RF > 0:** Different topology

## References

1. Nguyen, L.T. et al. (2015). "IQ-TREE: A fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies". *Mol Biol Evol* 32(1): 268-274.

2. Kalyaanamoorthy, S. et al. (2017). "ModelFinder: fast model selection for accurate phylogenetic estimates". *Nat Methods* 14(6): 587-589.

3. Hoang, D.T. et al. (2018). "UFBoot2: Improving the ultrafast bootstrap approximation". *Mol Biol Evol* 35(2): 518-522.

4. Felsenstein, J. (2004). *Inferring Phylogenies*. Sinauer Associates.

5. Yang, Z. (2006). *Computational Molecular Evolution*. Oxford University Press.

## See Also

- [Quality Control](01-quality-control.md) - Prepare high-quality alignment
- [Conservation Analysis](02-conservation.md) - Identify conserved residues
- [Coevolution Analysis](03-coevolution.md) - Find coevolved pairs
