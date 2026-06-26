# Quality Control Reference

## Overview

Quality control is the foundation of reliable phylogenetic analysis. Poor quality sequences introduce noise, bias results, and waste computational resources.

## Why Quality Control Matters

### Problems with Raw Sequences

1. **Predicted sequences** - No experimental validation, may contain errors
2. **Fragments** - Incomplete sequences from genome assemblies
3. **Redundancy** - Multiple identical/near-identical sequences bias sampling
4. **Low complexity** - Repetitive regions (polyA, polyQ) inflate similarity
5. **Annotation errors** - Wrong family assignment, domain boundaries

### Impact on Downstream Analysis

- **Phylogeny:** Wrong topology, low bootstrap support, long-branch attraction
- **Conservation:** False variable sites, inflated gap ratios
- **Coevolution:** Noise drowns real signal, false positive pairs
- **Computation:** Wasted time on uninformative sequences

## 8-Stage QC Pipeline

### Stage 1: Literature Validation

**Goal:** Keep only experimentally validated sequences

**Method:**
```bash
# Filter by evidence level
grep "evidence=experimental" input.fasta > validated.fasta
```

**Criteria:**
- UniProt evidence level 1-3 (experimental)
- Exclude evidence level 4-5 (predicted)
- PDB structures automatically pass

**Expected reduction:** 50-70%

### Stage 2: Length Filtering

**Goal:** Remove fragments and fusion proteins

**Method:**
```python
# Calculate mean and SD
lengths = [len(seq) for seq in sequences]
mean_len = np.mean(lengths)
std_len = np.std(lengths)

# Keep sequences within mean ± 2 SD
min_len = mean_len - 2 * std_len
max_len = mean_len + 2 * std_len
```

**Rationale:** 95% of normal distribution within ±2 SD

**Expected reduction:** 5-10%

### Stage 3: CD-HIT Redundancy Removal

**Goal:** Reduce sequence similarity to avoid sampling bias

**Algorithm:** Greedy incremental clustering
1. Sort sequences by length (longest first)
2. First sequence becomes cluster representative
3. For each new sequence:
   - Compare to all representatives
   - If similarity ≥ threshold → join cluster
   - If similarity < threshold → new cluster
4. Output all representatives

**Command:**
```bash
cd-hit -i input.fasta -o output.fasta \
  -c 0.90 \     # 90% identity threshold
  -n 5 \        # word length (for 0.7-1.0 similarity)
  -M 0 \        # unlimited memory
  -T 0          # use all CPUs
```

**Threshold selection:**
- 95%: Very stringent (closely related species)
- 90%: Standard (recommended)
- 85%: Relaxed (diverse families)
- 70%: Very relaxed (superfamilies)

**Expected reduction:** 30-50%

### Stage 4: Complexity Check

**Goal:** Remove low-complexity regions

**Method:** SEG algorithm (Wootton & Federhen 1996)
```bash
segmasker -in input.fasta -outfmt fasta > masked.fasta
```

**Criteria:**
- Mask regions with < 2.2 bits/residue
- Remove sequences with > 30% masked

**Common low-complexity patterns:**
- Polyalanine (AAAAAAA)
- Polyglutamine (QQQQQQQ)
- Tandem repeats (ABCABCABC)

**Expected reduction:** 1-5%

### Stage 5: Motif Validation

**Goal:** Confirm family membership

**Method:** HMMER profile search
```bash
# Build HMM from known family members
hmmbuild family.hmm seed_alignment.sto

# Search sequences
hmmsearch --tblout results.txt family.hmm sequences.fasta

# Keep sequences with E-value < 1e-10
```

**Alternative:** PROSITE pattern matching
```bash
# Example: Rossmann fold motif
grep -E "G.{1,3}G.{2}G" sequences.fasta
```

**Expected reduction:** 5-15%

### Stage 6: MAFFT Alignment

**Goal:** High-quality multiple sequence alignment

**Command:**
```bash
mafft --maxiterate 1000 \    # iterative refinement
      --localpair \          # L-INS-i algorithm
      --thread -1 \          # use all CPUs
      input.fasta > aligned.fasta
```

**Algorithm selection:**
- **L-INS-i** (--localpair): < 200 sequences, high accuracy
- **G-INS-i** (--globalpair): Global homology
- **FFT-NS-2** (default): > 2000 sequences, fast

**Quality check:**
```bash
# Calculate alignment score
mafft --maxiterate 1000 --localpair --quiet input.fasta 2>&1 | grep "score"
```

**Expected time:** 1-10 minutes per 100 sequences

### Stage 7: trimAl Trimming

**Goal:** Remove poorly aligned regions

**Command:**
```bash
trimal -in aligned.fasta \
       -out trimmed.fasta \
       -automated1           # automatic strategy selection
```

**Strategies:**
- **automated1:** Balance conservation and gap removal
- **gappyout:** Remove very gappy columns (> 50% gaps)
- **strict:** Remove columns with any gaps
- **-gt 0.7:** Keep columns with < 30% gaps

**Quality metrics:**
```bash
# Check gap ratio
trimal -in trimmed.fasta -sgc  # show gap count
```

**Expected reduction:** 10-30% of positions

### Stage 8: Final Validation

**Goal:** Ensure dataset meets quality standards

**Checks:**
1. **Gap ratio:** < 30% per position
2. **Sequence coverage:** > 80% of alignment length
3. **Sequence similarity:** 25-60% (optimal for phylogeny)
4. **Alignment length:** > 100 positions

**Validation script:**
```python
def validate_alignment(fasta_file):
    alignment = AlignIO.read(fasta_file, "fasta")
    
    # Check gap ratio
    for i in range(alignment.get_alignment_length()):
        column = alignment[:, i]
        gap_ratio = column.count('-') / len(column)
        if gap_ratio > 0.3:
            print(f"Warning: Position {i} has {gap_ratio:.1%} gaps")
    
    # Check coverage
    for record in alignment:
        coverage = 1 - str(record.seq).count('-') / len(record.seq)
        if coverage < 0.8:
            print(f"Warning: {record.id} has {coverage:.1%} coverage")
    
    # Check similarity
    similarities = []
    for i, seq1 in enumerate(alignment):
        for seq2 in alignment[i+1:]:
            sim = calculate_similarity(seq1, seq2)
            similarities.append(sim)
    
    mean_sim = np.mean(similarities)
    print(f"Mean pairwise similarity: {mean_sim:.1%}")
    
    if mean_sim < 0.25:
        print("Warning: Low similarity, alignment may be unreliable")
    if mean_sim > 0.60:
        print("Warning: High similarity, consider stricter CD-HIT threshold")
```

## Quality Standards

### Excellent (Publication-ready)
- Gap ratio: < 20%
- Coverage: > 85%
- Similarity: 40-60%
- Redundancy: < 90%
- Motif coverage: > 70%
- Bootstrap convergence: > 0.99

### Good (Acceptable)
- Gap ratio: 20-30%
- Coverage: 80-85%
- Similarity: 25-40% or 60-70%
- Redundancy: 90-95%
- Motif coverage: 50-70%
- Bootstrap convergence: 0.95-0.99

### Poor (Needs improvement)
- Gap ratio: > 30%
- Coverage: < 80%
- Similarity: < 25% or > 70%
- Redundancy: > 95%
- Motif coverage: < 50%
- Bootstrap convergence: < 0.95

## Common Issues

### Issue: Too few sequences after QC

**Cause:** Overly stringent filters  
**Solution:**
- Relax CD-HIT threshold (90% → 85%)
- Accept predicted sequences with high confidence
- Expand search to related families

### Issue: High gap ratio after trimming

**Cause:** Diverse family, poor alignment  
**Solution:**
- Use profile HMM alignment (HMMER)
- Align conserved domains only
- Try different MAFFT algorithms

### Issue: Low sequence similarity

**Cause:** Distant homologs, superfamily analysis  
**Solution:**
- Use structural alignment (DALI, TM-align)
- Increase CD-HIT threshold (90% → 95%)
- Consider domain-based analysis

### Issue: Motif validation fails

**Cause:** Wrong family, domain boundaries  
**Solution:**
- Verify family assignment (BLAST, InterPro)
- Adjust motif pattern
- Use HMM instead of pattern matching

## Automation

### Full QC Pipeline Script

```bash
#!/bin/bash
# 01_quality_control.sh

INPUT=$1
OUTPUT_DIR=$2

# Stage 1: Literature validation
echo "Stage 1: Literature validation..."
python scripts/filter_by_evidence.py $INPUT $OUTPUT_DIR/stage1.fasta

# Stage 2: Length filtering
echo "Stage 2: Length filtering..."
python scripts/filter_by_length.py $OUTPUT_DIR/stage1.fasta $OUTPUT_DIR/stage2.fasta

# Stage 3: CD-HIT
echo "Stage 3: CD-HIT redundancy removal..."
cd-hit -i $OUTPUT_DIR/stage2.fasta -o $OUTPUT_DIR/stage3.fasta -c 0.90 -n 5 -M 0 -T 0

# Stage 4: Complexity check
echo "Stage 4: Complexity check..."
python scripts/filter_complexity.py $OUTPUT_DIR/stage3.fasta $OUTPUT_DIR/stage4.fasta

# Stage 5: Motif validation
echo "Stage 5: Motif validation..."
python scripts/validate_motifs.py $OUTPUT_DIR/stage4.fasta $OUTPUT_DIR/stage5.fasta

# Stage 6: MAFFT alignment
echo "Stage 6: MAFFT alignment..."
mafft --maxiterate 1000 --localpair --thread -1 $OUTPUT_DIR/stage5.fasta > $OUTPUT_DIR/stage6.fasta

# Stage 7: trimAl
echo "Stage 7: trimAl trimming..."
trimal -in $OUTPUT_DIR/stage6.fasta -out $OUTPUT_DIR/stage7.fasta -automated1

# Stage 8: Final validation
echo "Stage 8: Final validation..."
python scripts/validate_final.py $OUTPUT_DIR/stage7.fasta $OUTPUT_DIR/qc_report.json

# Copy to final location
cp $OUTPUT_DIR/stage7.fasta $OUTPUT_DIR/final.fasta

echo "Quality control complete!"
echo "Input: $(grep -c ">" $INPUT) sequences"
echo "Output: $(grep -c ">" $OUTPUT_DIR/final.fasta) sequences"
```

## Performance

**Typical runtime (1000 sequences):**
- Stage 1-2: < 1 minute
- Stage 3 (CD-HIT): 2-5 minutes
- Stage 4-5: < 1 minute
- Stage 6 (MAFFT): 10-30 minutes
- Stage 7 (trimAl): < 1 minute
- Stage 8: < 1 minute

**Total:** 15-40 minutes

**Memory usage:** 2-8 GB (depends on sequence count and length)

## References

- CD-HIT: Li & Godzik (2006) Bioinformatics 22:1658
- MAFFT: Katoh & Standley (2013) Mol Biol Evol 30:772
- trimAl: Capella-Gutiérrez et al. (2009) Bioinformatics 25:1972
- SEG: Wootton & Federhen (1996) Comput Chem 20:149
