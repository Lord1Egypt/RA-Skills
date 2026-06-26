---
name: protein-phylogeny
description: "Comprehensive protein family phylogenetic analysis workflow with quality control, conservation analysis, coevolution network analysis, and publication-ready visualization. Use when: (1) analyzing protein family evolution, (2) building phylogenetic trees from sequences, (3) identifying conserved/coevolved residues, (4) generating publication-quality figures and reports, (5) quality-controlling sequence datasets, or (6) performing systematic evolutionary analysis of enzyme families, protein superfamilies, or any homologous protein groups."
---

# Protein Family Phylogenetic Analysis

Complete workflow for protein family evolutionary analysis: quality control → conservation → coevolution → phylogeny → publication report.

## Quick Start

**Input:** FASTA file with protein sequences (any family, any size)  
**Output:** Publication-ready report with phylogenetic tree, conservation analysis, coevolution networks, and high-quality figures

**Typical workflow:**
```bash
# 1. Quality control (removes low-quality sequences)
bash scripts/01_quality_control.sh input.fasta output_dir/

# 2. Conservation analysis
bash scripts/02_conservation.sh output_dir/qc/final.fasta output_dir/

# 3. Coevolution analysis
bash scripts/03_coevolution.sh output_dir/qc/final.fasta output_dir/

# 4. Phylogenetic tree
bash scripts/04_phylogeny.sh output_dir/qc/final.fasta output_dir/

# 5. Generate figures
bash scripts/05_visualize.sh output_dir/

# 6. Create report
bash scripts/06_report.sh output_dir/ "Family Name"
```

## Workflow Overview

### Stage 1: Quality Control (references/01-quality-control.md)

**Purpose:** Filter raw sequences to high-quality, non-redundant dataset

**Steps:**
1. Literature validation (remove predicted sequences)
2. Length filtering (remove fragments/fusions)
3. CD-HIT redundancy removal (90% identity)
4. Complexity check (remove low-complexity regions)
5. Motif validation (confirm family membership)
6. MAFFT alignment (high accuracy mode)
7. trimAl trimming (automatic strategy)
8. Final validation (gap ratio, coverage)

**Key parameters:**
- CD-HIT threshold: 90% (adjustable 70-95%)
- Length range: mean ± 2 SD
- Gap threshold: < 30% per position
- Motif coverage: > 50%

**Output:** `qc/final.fasta` (high-quality aligned sequences)

### Stage 2: Conservation Analysis (references/02-conservation.md)

**Purpose:** Identify functionally important conserved residues

**Method:** Shannon entropy
- H_norm < 0.3: Highly conserved
- H_norm 0.3-0.6: Moderately conserved
- H_norm > 0.6: Variable

**Output:**
- Conserved positions list
- Conservation landscape plot
- Gap vs conservation scatter plot

### Stage 3: Coevolution Analysis (references/03-coevolution.md)

**Purpose:** Identify residue pairs that evolve together

**Method:** Normalized Mutual Information (NMI)
- Corrects for phylogenetic bias
- Identifies structural/functional coupling
- Builds coevolution network

**Output:**
- Coevolved position pairs (MI scores)
- Network graph (hub identification)
- Hub residue heatmap

### Stage 4: Phylogenetic Analysis (references/04-phylogeny.md)

**Purpose:** Reconstruct evolutionary relationships

**Method:** IQ-TREE maximum likelihood
- Automatic model selection (ModelFinder)
- UFBoot2 ultrafast bootstrap (1000 replicates)
- Convergence check (> 0.99 required)

**Output:**
- Phylogenetic tree (.treefile)
- Bootstrap consensus tree (.contree)
- Model parameters (.iqtree)

### Stage 5: Visualization (references/05-visualization.md)

**Purpose:** Generate publication-quality figures (300 DPI)

**Figures:**
1. Workflow diagram
2. Conservation heatmap
3. Coevolution network
4. Hub analysis
5. Quality metrics
6. Phylogenetic tree
7. Bootstrap distribution
8. Supplementary plots

**Style:** Clean, colorblind-friendly, Nature/Science standards

### Stage 6: Report Generation (references/06-report.md)

**Purpose:** Create comprehensive analysis report

**Sections:**
1. Overview (dataset summary)
2. Quality control (methods + results)
3. Conservation analysis (algorithms + findings)
4. Coevolution analysis (networks + hubs)
5. Phylogenetic analysis (tree + support)
6. Quality assessment (standards comparison)
7. Conclusions (biological insights)

**Format:** Markdown → Feishu/Word/PDF

## Key Features

### AI-Friendly Design

- **Modular scripts:** Each stage is independent
- **Clear parameters:** All thresholds documented
- **Error handling:** Automatic validation at each step
- **Progress tracking:** JSON state files
- **Resume capability:** Skip completed stages

### Token Efficiency

- **Progressive disclosure:** Load only needed references
- **Compact instructions:** Essential info only
- **Script execution:** No need to read code
- **Cached results:** Reuse intermediate files

### Professional Quality

- **Publication standards:** All methods peer-reviewed
- **Reproducible:** Fixed random seeds, versioned tools
- **Validated:** Tested on 10+ protein families
- **Documented:** Complete algorithm explanations

## Dependencies

**Required tools:**
- CD-HIT v4.8.1+
- MAFFT v7.490+
- trimAl v1.4+
- IQ-TREE v2.0+
- Python 3.8+ (BioPython, NumPy, Matplotlib, NetworkX)
- R 4.0+ (ape, phytools)

**Installation:**
```bash
bash scripts/install_dependencies.sh
```

## Common Pitfalls

### 1. Low Sequence Similarity (< 25%)

**Problem:** Alignment unreliable, phylogeny uncertain  
**Solution:** 
- Use profile HMM (HMMER) instead of MAFFT
- Consider domain-based analysis
- Increase CD-HIT threshold to 95%

### 2. High Gap Ratio (> 30%)

**Problem:** Many unreliable positions  
**Solution:**
- Stricter trimAl settings (`-gt 0.8`)
- Manual inspection of alignment
- Remove problematic sequences

### 3. Bootstrap Convergence Failure (< 0.99)

**Problem:** Tree topology unstable  
**Solution:**
- Increase bootstrap replicates (2000+)
- Try different substitution models
- Check for long-branch attraction

### 4. No Conserved Motifs

**Problem:** Family definition unclear  
**Solution:**
- Verify sequences are truly homologous
- Use structural alignment (DALI, TM-align)
- Consider broader superfamily analysis

## Advanced Usage

### Custom Quality Control

Edit `scripts/01_quality_control.sh` parameters:
```bash
CDHIT_THRESHOLD=0.85  # More stringent
MIN_LENGTH=200        # Shorter proteins
MAX_LENGTH=600        # Longer proteins
GAP_THRESHOLD=0.25    # Stricter gap cutoff
```

### Alternative Phylogeny Methods

See `references/04-phylogeny.md` for:
- Bayesian inference (MrBayes)
- Distance methods (FastTree)
- Parsimony (PAUP*)

### Custom Visualization

Edit `scripts/05_visualize.sh` for:
- Color schemes
- Figure dimensions
- Font sizes
- Layout styles

## Troubleshooting

**Issue:** CD-HIT crashes with large datasets  
**Fix:** Split input, process in batches, merge results

**Issue:** IQ-TREE runs forever  
**Fix:** Use `-fast` mode or reduce bootstrap replicates

**Issue:** Figures look pixelated  
**Fix:** Increase DPI in `scripts/05_visualize.sh` (default 300)

**Issue:** Report generation fails  
**Fix:** Check all intermediate files exist, rerun failed stages

## References

For detailed methodology, see:
- [Quality Control](references/01-quality-control.md)
- [Conservation Analysis](references/02-conservation.md)
- [Coevolution Analysis](references/03-coevolution.md)
- [Phylogenetic Analysis](references/04-phylogeny.md)
- [Visualization](references/05-visualization.md)
- [Report Generation](references/06-report.md)

## Citation

If you use this workflow, please cite:
- CD-HIT: Li & Godzik (2006) Bioinformatics
- MAFFT: Katoh & Standley (2013) Mol Biol Evol
- trimAl: Capella-Gutiérrez et al. (2009) Bioinformatics
- IQ-TREE: Nguyen et al. (2015) Mol Biol Evol
- This workflow: [Your publication]

## Example Usage

```bash
# Download your sequences
# (from UniProt, NCBI, or your own database)

# Run full workflow
bash scripts/run_full_workflow.sh sequences.fasta analysis_output/ "Your Family Name"

# Results in analysis_output/:
# - qc/final.fasta (high-quality sequences)
# - conservation/ (conserved positions)
# - coevolution/ (coevolved pairs)
# - phylogeny/ (phylogenetic tree)
# - figures/ (publication-quality plots)
# - report.md (complete analysis)
```

