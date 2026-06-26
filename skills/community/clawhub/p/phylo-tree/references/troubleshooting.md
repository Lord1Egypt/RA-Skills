# Troubleshooting

## Common Issues

### Issue 1: "Command not found: iqtree"

**Cause:** Environment not activated or tools not installed

**Solution:**
```bash
conda activate r43
which iqtree  # Should show path
```

If not found, reinstall:
```bash
conda install -n r43 -c bioconda iqtree=3.1.1 -y
```

---

### Issue 2: "No sequences found"

**Cause:** Query too specific or no UniProt results

**Solution:**
- Try broader query: "reductase" instead of "imine reductase IRED"
- Check UniProt manually: https://www.uniprot.org/
- Use `--fasta` with your own sequences

---

### Issue 3: "R package not found"

**Cause:** R packages not installed

**Solution:**
```bash
conda activate r43
conda install -n r43 -c conda-forge r-ggtree r-ggplot2 r-viridis -y
```

**Don't use:** `install.packages()` in R (use conda instead)

---

### Issue 4: Analysis too slow

**Cause:** Too many sequences or low CPU

**Solution:**
- Increase `--threads`
- Reduce `--max-sequences`
- Increase `--identity` (more aggressive deduplication)

**Example:**
```bash
python3 scripts/run_v2.py \
  --query "lipase" \
  --output ./output \
  --threads 20 \
  --max-sequences 500 \
  --identity 0.95
```

---

### Issue 5: Low support values

**Cause:** Insufficient data or conflicting signal

**Solution:**
- Increase `--bootstrap` to 2000
- Add more sequences
- Check alignment quality in `alignment/trimmed.fasta`

---

### Issue 6: Figures not generated

**Cause:** R script error or missing packages

**Solution:**
```bash
# Check R environment
conda activate r43
R --version  # Should be 4.3.x

# Reinstall packages
conda install -n r43 -c conda-forge r-ggtree r-ggplot2 r-patchwork -y

# Run visualization manually
Rscript scripts/visualize_enhanced.R \
  ./output/trees/phylo_rooted.nwk \
  ./output/figures
```

---

## Still Having Issues?

**Check logs:**
```bash
cat ./output/logs/iqtree.log
cat ./output/logs/mafft.log
```

**Verify environment:**
```bash
conda activate r43
which iqtree mafft trimal
R --version
python3 --version
```

**Test with small dataset:**
```bash
python3 scripts/run_v2.py \
  --query "lipase" \
  --output ./test \
  --max-sequences 50 \
  --bootstrap 100
```
