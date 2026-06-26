# Detailed Scientific Report Template

**Title:** Phylogenetic Analysis of {Enzyme Family}

---

## 1. Introduction

### 1.1 Background

{Enzyme family} is a {description}. Understanding the evolutionary relationships within this family is crucial for {reasons}.

### 1.2 Objectives

This study aims to:
1. Construct a comprehensive phylogenetic tree of {enzyme family}
2. Identify evolutionary patterns and taxonomic distribution
3. Detect potential functional divergence events
4. Provide a framework for function prediction and enzyme engineering

---

## 2. Theoretical Background

### 2.1 Maximum Likelihood Phylogenetic Inference

**Principle:**

Maximum likelihood (ML) estimates the tree topology and branch lengths that maximize the probability of observing the sequence data under a specific evolutionary model.

**Mathematical Foundation:**

For a tree T with topology τ and branch lengths v, the likelihood is:

```
L(T|D) = P(D|τ, v, θ)
```

where D is the sequence data and θ represents model parameters (substitution rates, base frequencies, gamma shape, etc.).

**Advantages over other methods:**
- **vs. Distance methods (NJ, UPGMA):** ML explicitly models evolution, handles rate heterogeneity
- **vs. Parsimony:** ML is statistically consistent, better for long branches
- **vs. Bayesian:** ML is faster, no prior specification needed

**Why ML is the gold standard:**
- Used in >80% of phylogenetic studies in Nature/Science
- Statistically rigorous framework
- Allows model selection and hypothesis testing

### 2.2 Model Selection (ModelFinder)

**Principle:**

Different proteins evolve under different substitution models. ModelFinder (Kalyaanamoorthy et al. 2017) tests 1232 models and selects the best-fit model using:

- **AIC (Akaike Information Criterion):** Balances fit and complexity
- **BIC (Bayesian Information Criterion):** Penalizes complexity more strongly
- **AICc (corrected AIC):** Better for small datasets

**Formula:**

```
AIC = -2 ln(L) + 2K
BIC = -2 ln(L) + K ln(N)
```

where L is likelihood, K is number of parameters, N is sample size.

**Why model selection matters:**
- Wrong model → biased branch lengths and support values
- Overly simple model → underestimates uncertainty
- Overly complex model → overfitting

### 2.3 Bootstrap Support

**UFBoot2 (Ultrafast Bootstrap):**

Traditional bootstrap resamples alignment columns and rebuilds trees (slow). UFBoot2 (Hoang et al. 2018) uses a fast approximation:

1. Generate bootstrap alignments
2. Optimize branch lengths on fixed topology
3. Compute likelihood
4. Estimate support from likelihood distribution

**Advantages:**
- 100-1000× faster than standard bootstrap
- Comparable accuracy
- Allows ≥1000 replicates in reasonable time

**SH-aLRT (Shimodaira-Hasegawa approximate Likelihood Ratio Test):**

Tests whether a branch is significantly better than collapsing it:

```
LR = 2(ln L_best - ln L_collapsed)
```

**Interpretation:**
- SH-aLRT ≥80% → strong support
- UFBoot ≥95% → strong support
- Both high → very confident

---

## 3. Methods

### 3.1 Sequence Collection

**Strategy:** {query} search in UniProt database

**Rationale:**
- UniProt is the most comprehensive protein database
- Reviewed entries (Swiss-Prot) are manually curated
- Includes functional annotations for interpretation

**Parameters:**
- Database: UniProt (Swiss-Prot + TrEMBL)
- Query: "{query}"
- Date: {date}
- Initial sequences: {N}

### 3.2 Quality Control & Filtering

**Step 1: Length filtering**
- Min length: 100 aa
- Max length: 2000 aa
- **Rationale:** Remove fragments and fusion proteins

**Step 2: Deduplication (CD-HIT)**
- Identity threshold: 90%
- **Rationale:** 
  - Reduce computational cost
  - Remove near-identical sequences (same strain, minor variants)
  - Retain diversity (90% allows ~10% divergence)
  - Standard in phylogenetic studies (Li & Godzik 2006)

**Result:** {N_filtered} sequences retained

### 3.3 Multiple Sequence Alignment

**Algorithm:** MAFFT v7.520, L-INS-i strategy

**Rationale:**
- **MAFFT:** Fastest accurate aligner (Katoh & Standley 2013)
- **L-INS-i:** Most accurate for <200 sequences
  - Uses local pairwise alignment
  - Iterative refinement
  - Consistency-based scoring

**Parameters:**
- Strategy: L-INS-i
- Gap opening penalty: 1.53
- Gap extension penalty: 0.123
- **Rationale:** Default values optimized for protein sequences

**Alternative considered:**
- MUSCLE: Faster but less accurate
- Clustal Omega: Good for large datasets but slower
- **Decision:** L-INS-i for best accuracy

### 3.4 Alignment Trimming

**Algorithm:** trimAl v1.5, automated1 mode

**Rationale:**
- Remove poorly aligned regions
- Reduce noise in phylogenetic inference
- Automated1 uses heuristics to balance information vs. noise

**Parameters:**
- Mode: automated1
- Gap threshold: Auto-determined
- Similarity threshold: Auto-determined

**Result:**
- Original alignment: {length_before} sites
- Trimmed alignment: {length_after} sites
- Retained: {percentage}%

### 3.5 Phylogenetic Inference

**Software:** IQ-TREE v3.1.1

**Model Selection:**
- Method: ModelFinder
- Candidate models: 1232 (all protein models)
- Selection criterion: BIC
- **Best model:** {best_model}

**Model interpretation:**
- **Q.PFAM:** Empirical substitution matrix from Pfam database
- **+R7:** FreeRate model with 7 rate categories (accounts for rate heterogeneity)

**Tree Search:**
- Algorithm: Hill-climbing + stochastic perturbation
- Starting trees: 100 random + 100 parsimony
- **Rationale:** Multiple starts avoid local optima

**Bootstrap:**
- UFBoot2: 1000 replicates
- SH-aLRT: 1000 replicates
- **Rationale:** 
  - 1000 replicates standard for publication
  - Both methods provide complementary support measures

**Computational Resources:**
- Threads: {threads}
- RAM: ~{ram} GB
- Time: ~{time} hours

### 3.6 Tree Rooting

**Method:** Midpoint rooting

**Rationale:**
- No outgroup available
- Midpoint assumes molecular clock (reasonable for closely related sequences)
- Alternative (unrooted) less interpretable

---

## 4. Results

### 4.1 Dataset Summary

- **Total sequences analyzed:** {num_sequences}
- **Number of species:** {num_species}
- **Number of genera:** {num_genera}
- **Alignment length:** {alignment_length} sites
- **Conserved sites:** {conserved_sites} ({conserved_percentage}%)
- **Variable sites:** {variable_sites} ({variable_percentage}%)

### 4.2 Model Selection

**Best-fit model:** {best_model}

**Model parameters:**
- Log-likelihood: {log_likelihood}
- AIC: {aic}
- BIC: {bic}
- Number of parameters: {num_params}

**Interpretation:**
The {best_model} model was selected from 1232 candidates, indicating {interpretation}.

### 4.3 Tree Statistics

- **Tree length:** {tree_length} substitutions/site
- **Mean branch length:** {mean_branch_length}
- **Median branch length:** {median_branch_length}
- **Max branch length:** {max_branch_length}

**Interpretation:**
The median branch length of {median_branch_length} indicates {interpretation}. The presence of long branches (>{threshold}) suggests {interpretation}.

### 4.4 Support Values

- **Total internal nodes:** {total_nodes}
- **High support nodes (SH-aLRT ≥80% OR UFBoot ≥95%):** {high_support_nodes} ({high_support_percentage}%)
- **Very high support (SH-aLRT ≥80% AND UFBoot ≥95%):** {very_high_support_nodes} ({very_high_support_percentage}%)

**Interpretation:**
{high_support_percentage}% of nodes have high support, indicating {interpretation}.

### 4.5 Taxonomic Distribution

**Top 10 genera:**

| Genus | Count | Percentage |
|-------|-------|------------|
| {genus1} | {count1} | {pct1}% |
| {genus2} | {count2} | {pct2}% |
| ... | ... | ... |

**Interpretation:**
The enrichment of {top_genus} ({count}, {pct}%) suggests {interpretation}.

---

## 5. Figure Analysis

### Figure 1: Maximum Likelihood Phylogenetic Tree

**Description:**
Rectangular layout phylogenetic tree showing {num_sequences} sequences. Branch lengths are proportional to evolutionary distance (substitutions/site). Internal nodes with high support (SH-aLRT ≥80% or UFBoot ≥95%) are marked with red dots. Tip labels are colored by genus (top 12 genera).

**Key Observations:**

1. **Genus-level clustering:**
   - Sequences from the same genus form monophyletic clades
   - High support for genus-level branches
   - **Interpretation:** Vertical inheritance is the primary evolutionary mechanism

2. **Taxonomic distribution:**
   - {genus1} ({count1} sequences) forms a large clade
   - {genus2} ({count2} sequences) is also prominent
   - **Interpretation:** {enzyme} is enriched in {family/order}

3. **Branch length variation:**
   - Most branches are short (median {median_bl})
   - Some branches exceed {threshold} substitutions/site
   - **Interpretation:** Periods of rapid evolution or functional divergence

4. **Support values:**
   - {pct}% of nodes have high support
   - Deep nodes have lower support
   - **Interpretation:** Main topology is reliable, but ancient relationships are uncertain

**Biological Significance:**
The tree structure reveals {interpretation}. This has implications for {applications}.

### Figure 2: Circular Phylogenetic Tree

**Description:**
Same tree as Figure 1, but in circular layout for better visualization of large datasets.

**Advantages:**
- More compact
- Easier to see overall structure
- Better for presentations

**Key Features:**
- Clear separation of major clades
- Radial symmetry highlights taxonomic groups

### Figure 3: Heatmap Tree (Branch Length Visualization)

**Description:**
Tree with branches colored by length using a plasma gradient (purple = short, yellow = long).

**Key Observations:**

1. **Most branches are purple (short):**
   - Indicates slow, steady evolution
   - Conserved function

2. **Yellow branches (long):**
   - Located at {positions}
   - **Interpretation:** Rapid evolution, possibly functional divergence

3. **Gradient patterns:**
   - Gradual color changes indicate steady evolution
   - Abrupt changes indicate acceleration events

**Biological Significance:**
Long branches may represent:
- Adaptation to new substrates
- Positive selection on active site residues
- Gene duplication followed by neofunctionalization

**Experimental validation:**
- Test substrate specificity of enzymes from long branches
- Compare with closely related enzymes
- Identify key amino acid changes

### Figure 4: Branch Length Distribution

**Description:**
Histogram showing the distribution of branch lengths across the tree.

**Statistical Summary:**
- Mean: {mean}
- Median: {median}
- Standard deviation: {sd}
- Skewness: {skew}

**Key Observations:**

1. **Right-skewed distribution:**
   - Most branches are short
   - Few long branches (outliers)
   - **Interpretation:** Most evolution is gradual, with occasional bursts

2. **Median vs. Mean:**
   - Median ({median}) < Mean ({mean})
   - **Interpretation:** Long branches pull the mean up

3. **Outliers:**
   - Branches > {threshold} are outliers
   - Represent {percentage}% of branches
   - **Interpretation:** Rare but significant divergence events

**Biological Significance:**
The distribution suggests {interpretation}.

### Figure 5: Genus Distribution

**Description:**
Bar chart showing the number of sequences per genus (top 15).

**Key Observations:**

1. **Dominant genera:**
   - {genus1}: {count1} sequences ({pct1}%)
   - {genus2}: {count2} sequences ({pct2}%)
   - **Interpretation:** {enzyme} is abundant in {family}

2. **Long tail:**
   - Many genera with few sequences
   - **Interpretation:** Widespread but unevenly distributed

3. **Ecological context:**
   - {genus1} is a {description}
   - **Interpretation:** {enzyme} may play a role in {process}

**Biological Significance:**
The taxonomic distribution suggests {interpretation}.

### Figure 6: Combined Multi-Panel Figure

**Description:**
Three-panel figure combining:
- Panel A: Main tree
- Panel B: Branch length distribution
- Panel C: Genus distribution

**Advantages:**
- Comprehensive view
- Suitable for publication
- Tells complete story

**Key Message:**
{enzyme} shows {pattern} with {features}.

---

## 6. Discussion

### 6.1 Evolutionary Patterns

**Vertical Inheritance:**
The strong genus-level clustering indicates vertical inheritance is the primary evolutionary mechanism. This is consistent with {literature}.

**Horizontal Gene Transfer:**
We found limited evidence for HGT, as sequences from distantly related genera do not cluster together. This contrasts with {other enzyme families}.

**Functional Divergence:**
Long branches suggest periods of rapid evolution, possibly driven by:
- Adaptation to new substrates
- Positive selection on active site residues
- Gene duplication and neofunctionalization

### 6.2 Taxonomic Distribution

**Enrichment in {family}:**
The high abundance of {enzyme} in {family} suggests it plays an important role in {process}. This is supported by {evidence}.

**Ecological Context:**
{genus1} is commonly found in {environment}, where {enzyme} may be involved in {process}.

### 6.3 Functional Implications

**Function Prediction:**
Enzymes in the same clade likely have similar substrate specificity. For example, {genus1} enzymes may prefer {substrate}.

**Enzyme Engineering:**
- **Stability:** Target conserved clades (short branches)
- **Activity:** Target divergent clades (long branches)
- **Chimeras:** Combine sequences from different clades

**Novel Enzyme Discovery:**
Underrepresented genera (e.g., {genus}) may harbor novel activities.

### 6.4 Limitations

1. **Sampling bias:** UniProt is biased toward model organisms
2. **Alignment quality:** Short alignment ({length} sites) limits resolution
3. **Model assumptions:** ML assumes tree-like evolution (no recombination)
4. **Functional annotation:** Many sequences lack experimental validation

### 6.5 Future Directions

1. **Experimental validation:**
   - Test substrate specificity of representative enzymes
   - Measure catalytic efficiency (kcat/Km)
   - Determine crystal structures

2. **Expanded sampling:**
   - Include more sequences from underrepresented genera
   - Add environmental sequences (metagenomes)

3. **Functional genomics:**
   - Correlate phylogeny with gene context
   - Analyze co-evolution with other enzymes

4. **Structural analysis:**
   - Map active site residues onto tree
   - Identify structural determinants of specificity

---

## 7. Conclusions

### 7.1 Key Findings

1. **High-quality phylogenetic tree:** {num_sequences} sequences, {support_pct}% high support
2. **Vertical inheritance:** Strong genus-level clustering
3. **Taxonomic enrichment:** {genus1} and {genus2} dominate
4. **Functional divergence:** Long branches suggest rapid evolution events

### 7.2 Scientific Significance

This study provides:
- A comprehensive evolutionary framework for {enzyme}
- Insights into taxonomic distribution and ecological roles
- A foundation for function prediction and enzyme engineering

### 7.3 Practical Applications

- **Function prediction:** Use phylogeny to infer substrate specificity
- **Enzyme engineering:** Target conserved or divergent clades
- **Novel discovery:** Screen underrepresented genera

---

## 8. References

1. Nguyen et al. (2015). IQ-TREE: A fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies. *Mol Biol Evol* 32:268-274.

2. Hoang et al. (2018). UFBoot2: Improving the ultrafast bootstrap approximation. *Mol Biol Evol* 35:518-522.

3. Kalyaanamoorthy et al. (2017). ModelFinder: fast model selection for accurate phylogenetic estimates. *Nat Methods* 14:587-589.

4. Katoh & Standley (2013). MAFFT multiple sequence alignment software version 7. *Mol Biol Evol* 30:772-780.

5. Li & Godzik (2006). Cd-hit: a fast program for clustering and comparing large sets of protein or nucleotide sequences. *Bioinformatics* 22:1658-1659.

6. Yu et al. (2017). ggtree: an R package for visualization and annotation of phylogenetic trees. *Methods Ecol Evol* 8:28-36.

---

**Report generated:** {date}  
**Analysis version:** PhyloTree v2.0  
**Contact:** {email}
