# PhyloTree | Publication-Grade Phylogenetic Analysis

**One-line:** Build Nature/Science-level phylogenetic trees from enzyme names or sequences.

---

## 🚀 Quick Start (3 steps)

```bash
# 1. Activate environment
conda activate r43

# 2. Run analysis
python3 scripts/run_v2.py --query "imine reductase" --output ./output

# 3. Done! Check ./output/figures/ for publication-ready figures
```

**Output:** ML tree + 6 figures + QC reports + scientific conclusions

---

## 📋 Common Use Cases

### Use Case 1: Analyze from FASTA file (Recommended)
```bash
python3 scripts/run_v2.py --fasta sequences.fasta --output ./my_analysis
```

**How to get sequences:**
1. Go to UniProt: https://www.uniprot.org/
2. Search for your enzyme (e.g., "imine reductase")
3. Click "Download" → "FASTA (canonical)"
4. Save as `sequences.fasta`

### Use Case 2: Analyze by enzyme name (requires UniProt API)
```bash
python3 scripts/run_v2.py --query "imine reductase" --output ./ired_analysis
```

**Note:** This uses UniProt API which may change. Manual download (Use Case 1) is more reliable.

### Use Case 3: Custom parameters
```bash
python3 scripts/run_v2.py \
  --query "lipase" \
  --output ./lipase \
  --threads 10 \
  --bootstrap 1000 \
  --identity 0.90
```

---

## 📊 What You Get

**Files generated:**
- `trees/phylo.treefile` - ML tree (Newick format)
- `figures/*.png` - 6 publication-ready figures (300 DPI)
- `analysis_summary.json` - Key statistics
- `conclusions.md` - Scientific findings

**Figures:**
1. Main tree (rectangular layout)
2. Circular tree
3. Heatmap tree (branch length gradient)
4. Branch length distribution
5. Genus distribution
6. Combined multi-panel

---

## 🔧 Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--query` | - | Enzyme name (UniProt search) |
| `--fasta` | - | Input FASTA file |
| `--output` | - | Output directory |
| `--threads` | 10 | CPU threads |
| `--bootstrap` | 1000 | Bootstrap replicates |

**Full parameter list:** See `references/parameters.md`

---

## 📖 Need More?

**First time setup:** `references/installation.md`  
**Troubleshooting:** `references/troubleshooting.md`  
**Interpreting results:** `references/interpretation.md`  
**Publication checklist:** `references/publication.md`  
**AI report generation:** `references/ai_workflow.md`

---

## ✅ Quality Standards

- ✅ IQ-TREE ML + ModelFinder (1232 models)
- ✅ UFBoot2 + SH-aLRT ≥ 1000
- ✅ Alignment trimming (trimAl)
- ✅ Deduplication (CD-HIT 90%)
- ✅ 300 DPI figures
- ✅ Nature/Science color schemes

**Suitable for:** Nature, Science, Cell, MBE, Systematic Biology, PNAS

---

## 🤖 For AI Agents

**After analysis, read:**
1. `analysis_summary.json` - Structured statistics
2. `conclusions.md` - Scientific findings
3. `references/report_template.md` - Writing template

**No need to parse log files!**

---

## 📚 References

1. Nguyen et al. (2015). IQ-TREE. *Mol Biol Evol* 32:268-274.
2. Hoang et al. (2018). UFBoot2. *Mol Biol Evol* 35:518-522.
3. Kalyaanamoorthy et al. (2017). ModelFinder. *Nat Methods* 14:587-589.
4. Yu et al. (2017). ggtree. *Methods Ecol Evol* 8:28-36.

**Full references:** `references/citations.md`

---

## 🔒 Security & Privacy

**This skill is safe and transparent:**

✅ **No malicious code** - All scripts are open source and auditable  
✅ **External tools only** - Calls standard bioinformatics tools (IQ-TREE, MAFFT, trimAl, CD-HIT)  
✅ **Optional API** - UniProt API is optional, manual FASTA download recommended  
✅ **Local processing** - All analysis runs locally, no data sent to third parties  
✅ **No network when using --fasta** - Completely offline when using local FASTA files  

**Why flagged as suspicious?**

ClawHub's automated scanner detected:
- `subprocess` calls (to run IQ-TREE, MAFFT, R)
- Optional network requests (UniProt API for `--query` mode)
- File system operations (creating output directories)

These are **normal and necessary** for phylogenetic analysis. All external commands are:
- Standard bioinformatics tools (installed via conda)
- Called with explicit arguments (no shell injection)
- Logged for transparency

**Recommended usage:**
- Use `--fasta` with manually downloaded sequences (no network requests)
- Only use `--query` if you trust UniProt API (public, no authentication)

**Verification:**
- Review all scripts in `scripts/` directory
- Check `run_v2.py` for the complete workflow
- All external commands are documented in SKILL.md

---

**Version:** 2.0 | **Updated:** 2026-04-23
