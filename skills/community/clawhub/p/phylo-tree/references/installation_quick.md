# Installation Guide

## Quick Check

```bash
conda env list | grep r43  # Check if environment exists
```

If exists, skip to "Usage". If not, continue below.

---

## Full Installation

### Step 1: Fix conda solver
```bash
sed -i 's/solver: libmamba/solver: classic/' ~/.condarc
```

### Step 2: Create environment
```bash
conda create -n r43 python=3.14 -y
conda activate r43
```

### Step 3: Install tools
```bash
# Bioinformatics tools
conda install -n r43 -c bioconda iqtree=3.1.1 trimal=1.5 cd-hit=4.8.1 -y

# R and packages
conda install -n r43 -c conda-forge r-base=4.3 r-ape r-ggtree r-ggplot2 r-patchwork r-dplyr r-viridis -y

# Python packages
conda install -n r43 -c conda-forge biopython requests -y
```

### Step 4: Verify
```bash
conda activate r43
which iqtree mafft trimal
R --version
```

**Expected:** All commands found, R version 4.3.x

---

## Troubleshooting

**Problem:** `conda install` fails  
**Solution:** Use `solver: classic` in ~/.condarc

**Problem:** R packages missing  
**Solution:** Install via conda, not CRAN

**Problem:** IQ-TREE not found  
**Solution:** Command is `iqtree`, not `iqtree2`

---

**Time:** ~10 minutes  
**Disk:** ~2 GB
