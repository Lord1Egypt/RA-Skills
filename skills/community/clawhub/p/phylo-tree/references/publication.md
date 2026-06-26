# Publication Checklist

## Before Submission

### Data Quality
- [ ] ≥ 100 sequences analyzed
- [ ] ≥ 1000 bootstrap replicates
- [ ] High support (≥60% nodes with SH-aLRT ≥80% or UFBoot ≥95%)
- [ ] Alignment trimmed (trimAl)
- [ ] Sequences deduplicated (CD-HIT)

### Methods Section
- [ ] Software versions cited (IQ-TREE, MAFFT, trimAl)
- [ ] Model selection method described (ModelFinder)
- [ ] Bootstrap method specified (UFBoot2 + SH-aLRT)
- [ ] Alignment parameters documented

### Figures
- [ ] 300 DPI resolution
- [ ] Support values visible
- [ ] Scale bar present
- [ ] Genus/species labels readable
- [ ] Color scheme accessible (color-blind friendly)

### Data Deposition
- [ ] Tree file deposited (TreeBASE or Dryad)
- [ ] Alignment deposited
- [ ] Accession numbers provided

---

## Methods Template

> "Sequences were collected from UniProt and deduplicated at 90% identity using CD-HIT v4.8.1. Multiple sequence alignment was performed with MAFFT v7.520 (L-INS-i algorithm) and trimmed using trimAl v1.5 (automated1 mode). Maximum likelihood phylogenetic tree was inferred using IQ-TREE v3.1.1 with ModelFinder to select the best-fit model from 1232 candidates. Branch support was assessed using 1000 ultrafast bootstrap replicates (UFBoot2) and SH-aLRT test. The tree was visualized using ggtree v3.8.0 in R v4.3.3."

---

## Citation Format

**IQ-TREE:**
Nguyen et al. (2015). IQ-TREE: A fast and effective stochastic algorithm for estimating maximum-likelihood phylogenies. *Mol Biol Evol* 32:268-274.

**UFBoot2:**
Hoang et al. (2018). UFBoot2: Improving the ultrafast bootstrap approximation. *Mol Biol Evol* 35:518-522.

**ModelFinder:**
Kalyaanamoorthy et al. (2017). ModelFinder: fast model selection for accurate phylogenetic estimates. *Nat Methods* 14:587-589.

**ggtree:**
Yu et al. (2017). ggtree: an R package for visualization and annotation of phylogenetic trees. *Methods Ecol Evol* 8:28-36.

**Full citations:** `references/citations.md`

---

## Suitable Journals

**Top tier:**
- Nature, Science, Cell (if part of larger study)
- Molecular Biology and Evolution
- Systematic Biology

**Mid tier:**
- PNAS
- Bioinformatics
- BMC Evolutionary Biology

**Specialized:**
- Journal of Molecular Evolution
- Molecular Phylogenetics and Evolution
