# Interpreting Results

## Quick Summary

After analysis, read `analysis_summary.json` and `conclusions.md`.

---

## Key Findings to Look For

### 1. Taxonomic Distribution
**Question:** Which genera are most abundant?

**Example:** "Escherichia (46), Pseudomonas (33), Klebsiella (23)"

**Meaning:** These organisms are good models for functional studies.

---

### 2. Support Values
**Question:** What % of nodes have high support?

**Example:** "62.6% high support (≥80%/≥95%)"

**Meaning:**
- > 70%: Very reliable
- 50-70%: Reliable
- < 50%: Uncertain

---

### 3. Branch Lengths
**Question:** Are there long branches?

**Example:** "Median 0.01, but some > 0.5"

**Meaning:** Long branches = rapid evolution or functional divergence

---

### 4. Clustering Pattern
**Question:** Do sequences cluster by genus?

**Example:** "Strong within-genus clustering"

**Meaning:** Vertical inheritance (not horizontal gene transfer)

---

## Scientific Implications

**For function prediction:**
- Same clade → similar function
- Long branch → unique function

**For enzyme engineering:**
- Conserved branch → high stability
- Divergent branch → unique activity

**For novel discovery:**
- Target underrepresented genera
- Focus on long branches

---

## Writing Results

**Template:**

> "Phylogenetic analysis of {N} sequences from {M} species revealed {finding}. The tree showed {pattern}, with {X}% high support. Branch length analysis indicated {observation}, suggesting {interpretation}."

**Example:**

> "Phylogenetic analysis of 487 IRED sequences from 121 species revealed high enrichment in Enterobacteriaceae (21%). The tree showed strong within-genus clustering, with 62.6% high support. Branch length analysis indicated most IREDs evolve slowly (median 0.01), but some long branches (> 0.5) suggest functional divergence."

---

**Full interpretation guide:** See `conclusions.md` in output directory
