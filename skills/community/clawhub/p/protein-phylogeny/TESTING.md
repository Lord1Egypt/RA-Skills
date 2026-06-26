# Complete Installation and Usage Test

## Test Scenario: Fresh Machine Setup

This document tests whether the skill can be used on a completely fresh machine.

---

## Step 1: Install Skill

```bash
# On a fresh machine
clawhub install protein-phylogeny@1.3.0
```

**Expected output:**
```
✓ Downloaded protein-phylogeny@1.3.0
✓ Installed to ~/.agents/skills/protein-phylogeny
```

---

## Step 2: Install Dependencies

```bash
cd ~/.agents/skills/protein-phylogeny
bash scripts/install_dependencies.sh
```

**What it installs:**
- CD-HIT (redundancy removal)
- MAFFT (alignment)
- trimAl (trimming)
- IQ-TREE (phylogeny)
- Python packages (BioPython, NumPy, Pandas, Matplotlib, Seaborn, NetworkX)

**Expected output:**
```
✓ CD-HIT installed
✓ MAFFT installed
✓ trimAl installed
✓ IQ-TREE installed
✓ Python packages installed
```

---

## Step 3: Prepare Test Data

```bash
# Download example sequences (e.g., from UniProt)
# Or use your own FASTA file

# Example: Download kinase sequences
wget "https://rest.uniprot.org/uniprotkb/stream?query=family:kinase+AND+reviewed:true&format=fasta&limit=200" -O kinase.fasta
```

**Or create a test file:**
```bash
cat > test_sequences.fasta << 'EOF'
>seq1
MKTAIAVLGIGRMGSALARALIRADFDVRVWNRTADKCAPLAALGATAAATVPDAVADSD
>seq2
MKTAIAVLGIGRMGSALARALIRADFDVRVWNRTADKCAPLAALGATAAATVPDAVADSE
>seq3
MKTAIAVLGIGRMGSALARALIRADFDVRVWNRTADKCAPLAALGATAAATVPDAVADSF
EOF
```

---

## Step 4: Run Complete Analysis

### Option A: One-Command Analysis (Python)

```bash
cd ~/.agents/skills/protein-phylogeny/scripts/python

# Step 1: Quality control (manual, or use CD-HIT + MAFFT)
cd-hit -i ../../test_sequences.fasta -o nr90.fasta -c 0.9 -n 5
mafft --auto nr90.fasta > aligned.fasta

# Step 2: Run complete analysis
python complete_analysis.py aligned.fasta results/
```

**Expected output:**
```
================================================================================
Complete Phylogenetic Analysis Pipeline
================================================================================

Input: aligned.fasta
Output: results/

Reading alignment...
  Sequences: 200
  Alignment length: 350

================================================================================
Conservation Analysis
================================================================================

Total positions: 350
Highly conserved (H < 0.3): 45 (12.9%)
Moderately conserved (0.3 ≤ H < 0.6): 140 (40.0%)
Variable (H ≥ 0.6): 165 (47.1%)

Top 10 conserved positions:
  Position  15 (G): H = 0.000
  Position  16 (I): H = 0.005
  ...

✓ Conservation results saved to: results/conservation_detailed.csv

================================================================================
Coevolution Analysis
================================================================================

Calculating MI for 61075 position pairs...
  Position 10/350
  Position 20/350
  ...

Total pairs: 61075
Strong coevolution (MI > 0.5): 8500 (13.9%)
Moderate coevolution (0.3 < MI ≤ 0.5): 15200 (24.9%)

Top 10 coevolved pairs:
   15 ↔  35: MI = 0.625
   18 ↔  92: MI = 0.614
  ...

Hub positions (degree ≥ 5): 8
  Position  15: Degree 8
  Position  92: Degree 6
  ...

✓ Coevolution results saved to: results/coevolution_detailed.csv
✓ Hub positions saved to: results/hub_positions.txt
✓ Network data saved to: results/network_data.json

================================================================================
Generating Figures
================================================================================

1. Conservation landscape...
   ✓ conservation_landscape.png
2. Coevolution network...
   ✓ coevolution_network.png
3. Hub heatmap...
   ✓ hub_heatmap.png
4. MI distribution...
   ✓ MI_distribution.png
5. Bootstrap distribution...
   ⚠ Tree file not found, skipping bootstrap plot

✓ All figures saved to: results/

================================================================================
Analysis Complete!
================================================================================

Output files:
  - results/conservation_detailed.csv
  - results/coevolution_detailed.csv
  - results/hub_positions.txt
  - results/network_data.json
  - results/conservation_landscape.png
  - results/coevolution_network.png
  - results/hub_heatmap.png
  - results/MI_distribution.png
```

### Option B: Full Workflow (Shell Scripts)

```bash
cd ~/.agents/skills/protein-phylogeny

# Run complete workflow
bash scripts/run_full_workflow.sh test_sequences.fasta output/ "Test Enzyme Family"
```

**Expected output:**
```
========================================
Complete Phylogenetic Analysis Workflow
========================================
Input: test_sequences.fasta
Output: output/
Family: Test Enzyme Family

Step 1/6: Quality control...
✓ Quality control complete (200 → 180 sequences)

Step 2/6: Conservation analysis...
✓ Conservation analysis complete (45 highly conserved positions)

Step 3/6: Coevolution analysis...
✓ Coevolution analysis complete (8500 coevolved pairs)

Step 4/6: Phylogenetic analysis...
✓ Phylogenetic tree built (bootstrap convergence: 0.995)

Step 5/6: Visualization...
✓ All figures generated

Step 6/6: Report generation...
✓ Report generated: output/report.md

========================================
Analysis Complete!
========================================

Results:
  - output/qc/final.fasta (180 sequences)
  - output/conservation/conservation_detailed.csv
  - output/coevolution/coevolution_detailed.csv
  - output/phylogeny/tree.treefile
  - output/figures/*.png (5 figures)
  - output/report.md

Next steps:
  1. Review report: cat output/report.md
  2. View figures: open output/figures/
  3. Analyze conserved positions for mutagenesis
```

---

## Step 5: Verify Results

### Check Output Files

```bash
cd output/

# Conservation results
head conservation/conservation_detailed.csv
# Expected: position,entropy,norm_entropy,most_common_aa,...

# Coevolution results
head coevolution/coevolution_detailed.csv
# Expected: pos1,pos2,MI,num_pairs,...

# Hub positions
cat coevolution/hub_positions.txt
# Expected: Position 15: Degree 8

# Figures
ls -lh figures/
# Expected: 5 PNG files, each ~500KB-2MB

# Report
head -50 report.md
# Expected: Markdown report with summary
```

### Validate Figure Quality

```bash
# Check DPI
file figures/conservation_landscape.png
# Expected: PNG image data, 6000 x 1200 (or similar, 300 DPI)

# View figures
open figures/conservation_landscape.png
# or
xdg-open figures/conservation_landscape.png
```

---

## Step 6: Use Results for Protein Engineering

### Identify Mutation Targets

```bash
# Top conserved positions
python << 'EOF'
import pandas as pd

df = pd.read_csv('conservation/conservation_detailed.csv')
top10 = df.nsmallest(10, 'norm_entropy')

print("Top 10 mutation targets (highly conserved):")
for _, row in top10.iterrows():
    print(f"  Position {int(row['position'])} ({row['most_common_aa']}): H = {row['norm_entropy']:.3f}")
EOF
```

### Identify Hub Positions

```bash
# Hub positions (critical for function)
cat coevolution/hub_positions.txt
```

### Generate Mutation List

```bash
# Create mutation list for top 3 positions
python << 'EOF'
import pandas as pd

df = pd.read_csv('conservation/conservation_detailed.csv')
top3 = df.nsmallest(3, 'norm_entropy')

print("Recommended mutations:")
for _, row in top3.iterrows():
    pos = int(row['position'])
    wt = row['most_common_aa']
    print(f"\nPosition {pos} ({wt}):")
    print(f"  {wt}{pos}A - Test hydrophobic requirement")
    print(f"  {wt}{pos}S - Test polar interaction")
    print(f"  {wt}{pos}P - Negative control (disrupt structure)")
EOF
```

---

## Common Issues and Solutions

### Issue 1: Dependencies Not Installed

**Error:**
```
bash: cd-hit: command not found
```

**Solution:**
```bash
# Install via conda
conda install -c bioconda cd-hit mafft trimal iqtree

# Or via apt (Ubuntu/Debian)
sudo apt-get install cd-hit mafft trimal

# IQ-TREE
wget https://github.com/iqtree/iqtree2/releases/download/v2.2.0/iqtree-2.2.0-Linux.tar.gz
tar -xzf iqtree-2.2.0-Linux.tar.gz
sudo cp iqtree-2.2.0-Linux/bin/iqtree2 /usr/local/bin/
```

### Issue 2: Python Packages Missing

**Error:**
```
ModuleNotFoundError: No module named 'Bio'
```

**Solution:**
```bash
pip install biopython numpy pandas matplotlib seaborn networkx
```

### Issue 3: Out of Memory

**Error:**
```
MemoryError: Unable to allocate array
```

**Solution:**
```bash
# Reduce sequence count
cd-hit -i input.fasta -o reduced.fasta -c 0.95 -n 5

# Or split analysis
# Analyze conservation and coevolution separately
```

### Issue 4: Analysis Too Slow

**Problem:** Coevolution analysis takes hours

**Solution:**
```bash
# Use sampling for large datasets
python << 'EOF'
# Sample 50% of position pairs
import random
pairs = [(i, j) for i in range(n) for j in range(i+1, n)]
sampled = random.sample(pairs, len(pairs) // 2)
EOF
```

---

## Validation Checklist

- [ ] Skill installs successfully
- [ ] Dependencies install without errors
- [ ] Quality control runs and reduces sequences
- [ ] Conservation analysis produces CSV with entropy values
- [ ] Coevolution analysis produces CSV with MI scores
- [ ] Hub positions are identified (degree ≥ 5)
- [ ] Phylogenetic tree builds with bootstrap > 0.99
- [ ] All 5 figures generate at 300 DPI
- [ ] Report generates with all sections
- [ ] Results match expected patterns (12-15% highly conserved, 20-30% coevolved)

---

## Expected Results for Different Protein Families

### Kinases (200 sequences)
- Highly conserved: 40-50 positions (12-15%)
- Coevolved pairs: 8,000-12,000 (20-30%)
- Hub positions: 6-10
- Bootstrap support: 60-70% strong (≥95%)

### Proteases (150 sequences)
- Highly conserved: 30-40 positions (10-13%)
- Coevolved pairs: 5,000-8,000 (25-35%)
- Hub positions: 4-8
- Bootstrap support: 65-75% strong

### Transporters (300 sequences)
- Highly conserved: 50-70 positions (8-12%)
- Coevolved pairs: 15,000-25,000 (15-25%)
- Hub positions: 8-15
- Bootstrap support: 70-80% strong

---

## Success Criteria

✅ **The skill is complete and reproducible if:**

1. All scripts run without modification
2. Output files are generated in expected locations
3. Figures are publication-quality (300 DPI)
4. Results are biologically meaningful:
   - Conserved positions correspond to known functional sites
   - Hub positions are in active sites or binding pockets
   - Phylogenetic tree matches known taxonomy
5. Analysis completes in reasonable time (<1 hour for 200 sequences)
6. No proprietary data or machine-specific paths

---

## Conclusion

**This skill is production-ready if all steps above work on a fresh machine with only:**
- Linux/macOS operating system
- Python 3.8+
- Standard bioinformatics tools (installable via conda/apt)
- No prior knowledge of the specific protein family

**Test on a fresh machine to confirm!**
