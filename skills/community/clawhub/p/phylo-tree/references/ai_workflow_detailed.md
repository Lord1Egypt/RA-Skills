# AI Report Generation - Complete Scientific Report

## Goal

Generate a **complete scientific report** with:
1. Algorithm principles
2. Method selection rationale
3. Experimental parameters and justification
4. Experimental process
5. Figures with detailed analysis
6. Conclusions with interpretation

---

## Report Structure

### 1. Introduction & Background
- What is phylogenetic analysis?
- Why use maximum likelihood?
- Why IQ-TREE?

### 2. Algorithm Principles
- Maximum likelihood theory
- Model selection (ModelFinder)
- Bootstrap methods (UFBoot2 + SH-aLRT)
- Tree rooting strategies

### 3. Methods & Parameters
- Sequence collection strategy
- Alignment algorithm (MAFFT L-INS-i)
- Trimming method (trimAl automated1)
- Deduplication threshold (CD-HIT 90%)
- Model selection criteria
- Bootstrap replicates (1000)
- **Justification for each choice**

### 4. Experimental Process
- Step-by-step workflow
- Quality control at each stage
- Decision points and rationale

### 5. Results
- Tree statistics
- Support values
- Taxonomic distribution
- Branch length analysis

### 6. Figure Analysis
- Figure 1: Main tree - what it shows, key features
- Figure 2: Circular tree - layout advantages
- Figure 3: Heatmap tree - evolutionary rate visualization
- Figure 4: Branch length distribution - statistical interpretation
- Figure 5: Genus distribution - taxonomic insights
- Figure 6: Combined figure - integrated view

### 7. Discussion
- Biological interpretation
- Evolutionary insights
- Functional implications
- Limitations and caveats

### 8. Conclusions
- Key findings
- Scientific significance
- Future directions

---

## Data Sources

### From analysis_summary.json
```json
{
  "iqtree": {
    "best_model": "Q.PFAM+R7",
    "log_likelihood": -53461.908,
    "tree_length": 82.851,
    "num_sequences": 487
  },
  "support": {
    "total_nodes": 401,
    "high_support_nodes": 251,
    "high_support_percentage": 62.6
  },
  "alignment": {
    "length": 232,
    "conserved_sites": 45,
    "variable_sites": 187
  }
}
```

### From conclusions.md
- Scientific findings
- Biological interpretation
- Evolutionary insights

### From figures/
- All 6 publication-ready figures

---

## Report Template

See `references/report_template_detailed.md` for the complete template with:
- Algorithm explanations
- Parameter justifications
- Figure analysis guidelines
- Discussion frameworks

---

## Generation Workflow

```bash
# 1. Run analysis
python3 scripts/run_v2.py --query "enzyme" --output ./output

# 2. Generate JSON summary
python3 scripts/generate_summary.py ./output

# 3. Generate detailed report
python3 scripts/generate_detailed_report.py ./output

# Output: ./output/detailed_report.md
```

---

## Example Report Sections

### Algorithm Principles

> **Maximum Likelihood (ML) Method**
> 
> Maximum likelihood phylogenetic inference estimates the tree topology and branch lengths that maximize the probability of observing the given sequence data under a specific evolutionary model. Unlike distance-based methods (e.g., neighbor-joining), ML explicitly models the evolutionary process and can incorporate complex substitution models.
> 
> **Mathematical Foundation:**
> The likelihood L of a tree T given sequence data D is:
> 
> L(T|D) = P(D|T, θ)
> 
> where θ represents model parameters (substitution rates, base frequencies, etc.). IQ-TREE uses hill-climbing algorithms to search tree space and optimize L.
> 
> **Why ML over other methods?**
> - More accurate than distance methods for divergent sequences
> - Statistically rigorous framework
> - Allows model selection and hypothesis testing
> - Standard for publication in top journals

### Parameter Justification

> **Bootstrap Replicates: 1000**
> 
> **Rationale:** 
> - Felsenstein (1985) recommended ≥100 for basic support
> - Hillis & Bull (1993) showed 1000 replicates provide stable estimates
> - UFBoot2 (Hoang et al. 2018) is computationally efficient, allowing ≥1000
> - Top journals (Nature, Science) typically require ≥1000
> 
> **Trade-off:**
> - More replicates = more accurate support values
> - Diminishing returns beyond 1000-2000
> - Computational cost scales linearly
> 
> **Decision:** 1000 replicates balance accuracy and efficiency for publication-grade analysis.

### Figure Analysis

> **Figure 1: Maximum Likelihood Phylogenetic Tree**
> 
> **What it shows:**
> - 487 IRED sequences from 121 species
> - Branch lengths proportional to evolutionary distance
> - Support values at internal nodes (SH-aLRT/UFBoot)
> - Color-coded by genus (top 12 genera)
> 
> **Key observations:**
> 1. **Strong genus-level clustering** - Sequences from the same genus form monophyletic clades with high support (red dots), indicating vertical inheritance as the primary evolutionary mechanism.
> 
> 2. **Enterobacteriaceae enrichment** - Escherichia (46), Pseudomonas (33), and Klebsiella (23) dominate the tree, suggesting IRED plays an important role in gut bacterial metabolism.
> 
> 3. **Variable branch lengths** - Most branches are short (median 0.0105), but some exceed 0.5 substitutions/site, indicating periods of rapid evolution or functional divergence.
> 
> 4. **High support for major clades** - 62.6% of nodes have SH-aLRT ≥80% or UFBoot ≥95%, indicating the main topology is statistically robust.
> 
> **Biological interpretation:**
> The tree structure suggests IRED evolved primarily through vertical inheritance with occasional functional divergence events. The enrichment in Enterobacteriaceae may reflect metabolic requirements in the gut environment, where diverse nitrogen-containing compounds must be processed.

---

## AI Agent Instructions

When generating a detailed report:

1. **Read all data sources:**
   - analysis_summary.json
   - conclusions.md
   - QC reports (reports/*.json)

2. **Use the detailed template:**
   - references/report_template_detailed.md

3. **For each section:**
   - Explain the theory/algorithm
   - Justify parameter choices
   - Interpret results biologically
   - Connect to literature

4. **For each figure:**
   - Describe what it shows
   - Highlight key features
   - Provide biological interpretation
   - Explain significance

5. **Maintain scientific rigor:**
   - Cite methods papers
   - Use precise terminology
   - Acknowledge limitations
   - Suggest future work

---

## Output Format

**Markdown report with:**
- Clear section headers
- Inline citations
- Figure captions
- Statistical details
- Biological interpretation

**Length:** 3000-5000 words (suitable for supplementary methods)

---

**This approach generates a complete, publication-ready scientific report that explains not just WHAT was done, but WHY and WHAT IT MEANS.**
