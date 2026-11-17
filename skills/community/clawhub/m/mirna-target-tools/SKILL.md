---
name: mirna-target-tools
version: 3.0.0
description: >-
  End-to-end miRNA target analysis from miRNA sequences alone: whole-transcriptome
  target prediction across built-in species (human, mouse, rat, sheep, goat, cow,
  pig, chicken) or your own transcriptome/genome, with TargetScan-style seed
  sites, miRanda duplex confirmation and 3'UTR-restricted scanning; TargetScan
  and miRanda workflows, gene annotation, GO/KEGG enrichment with
  Benjamini-Hochberg FDR, seed-region conservation analysis, publication-quality
  R/ggplot2 figures, and Cytoscape network export. Fetches miRNA sequences from
  public databases itself (miRBase / RNAcentral), by name or for a whole species.
---

# miRNA Target Tools — miRNA target gene prediction toolkit

## Overview

An end-to-end toolkit for miRNA target analysis — from raw miRNA sequences to a
Cytoscape-ready regulatory network:

- **Target prediction** — TargetScan and miRanda workflows, or genome-wide
  seed-based prediction across an **entire species transcriptome from miRNA
  sequences alone** (no pre-built TargetScan database required)
- **Built-in species** — human, mouse, rat, sheep, goat, cow, pig, chicken
  (Ensembl transcriptomes downloaded on demand and cached), plus your own
  transcriptome FASTA or genome + GTF annotation
- **Annotation and enrichment** — gene-symbol annotation plus GO (BP/CC/MF) and
  KEGG enrichment reporting raw p-values **and** Benjamini-Hochberg FDR q-values
  computed over the full tested family
- **Conservation** — multi-species homolog extraction from miRBase, free-end-gap
  multiple alignment, Shannon information content and seed-region statistics
- **Publication figures** — every plot is drawn with **R + ggplot2** in a clean
  journal-friendly style (300 dpi PNG plus editable-text SVG, matplotlib
  fallback), with a one-command installer for R and the required packages
- **Networks** — `.sif` network plus node-attribute export for Cytoscape

## Core features

### 1. TargetScan miRNA target prediction
Run TargetScan to predict target genes for input miRNA sequences and output the target gene list with scores.

Script: `scripts/targetscan_predict.py`

### 2. miRanda miRNA target analysis
Run miRanda for miRNA-mRNA binding prediction, with free-energy calculation and conservation analysis.

Script: `scripts/miranda_predict.py`

### 3. Result merging and deduplication
Merge predictions from multiple tools and take the intersection to raise confidence, producing a gene list.

Script: `scripts/merge_targets.py`

### 4. Target gene annotation
Functional annotation and enrichment analysis of high-confidence target genes:

- **Gene annotation**: gene symbol -> Entrez ID / Ensembl ID / functional description (via the MyGene.info online API, no local database needed)
- **GO/KEGG enrichment**: GO (BP/CC/MF) + KEGG pathway enrichment (via the g:Profiler REST API; standard-library implementation with zero third-party dependencies)
- **Species support**: human / mouse / rat / **sheep** / **goat** / cow

Script: `scripts/annotate_targets.py`

### 5. Enrichment result visualization
Plot enrichment results as publication-grade dot plots (clusterProfiler style): terms ranked by significance, bubble size = genes in term, bubble colour = -log10(p) on a blue-to-red ramp, size legend + slim colour bar. 300 dpi PNG and (with `--svg`) an editable vector file.

**Rendering engine:** every figure in this skill is drawn with **R + ggplot2** by default (script `scripts/plot_enrichment.R`). If R or the required packages are missing, install them with `bash scripts/install_r_deps.sh`; the scripts auto-detect that and fall back to a matplotlib implementation (`--engine python` forces it, `--engine r` requires R).

Script: `scripts/plot_enrichment.py`

### 6. Cytoscape network file generation
Generate `.sif` network files and attribute files that can be imported directly into Cytoscape for regulatory network visualization.

Script: `scripts/format_cytoscape.py`

### 7. miRNA conserved sequence analysis
Multi-species conservation analysis of a target miRNA (publication grade):

- **Homolog extraction**: automatically extract the mature sequence of the target miRNA across multiple species from miRBase (exact mirbase-id matching, avoiding prefix collisions such as miR-21 vs miR-210)
- **Multiple sequence alignment**: free-end-gap global alignment (a Needleman-Wunsch variant, pure standard library), with gaps pushed to the 5'/3' ends (isomiR variation) and the seed region strictly aligned
- **Conservation quantification**: Shannon information content (bits, Schneider-Stevens 1990) + per-position percent identity + separate seed-region (default 2-8 nt) statistics
- **Publication-grade visualization**: information-content sequence logo + multiple sequence alignment figure (300 dpi PNG + SVG vector, WebLogo colors)

Script: `scripts/conservation_analysis.py`

### 8. Whole-transcriptome target prediction (new in 2.0.0)
Predict **every target site** of user-supplied mature miRNA sequences across the **entire mRNA set (transcriptome) of a species** — no TargetScan database required.

- **Target source** — built-in species presets, auto-downloaded from Ensembl on first use and cached, or your own sequences:
  - `--species human|mouse|rat|sheep|goat|cow|pig|chicken` (aliases such as `hsa`/`chi`/`oar` work too; run `--list-species`)
  - `--mrna-fa my_transcripts.fa` — your own mRNA/cDNA FASTA
  - `--genome-fa genome.fa --gtf annotation.gtf` — your own genome + annotation (mRNA rebuilt by joining exons)
- **miRNA source** — any of:
  - `--mirna-fa mirna.fa` — your own FASTA of mature sequences
  - `--mirna miR-21-5p,chi-miR-504-5p` — resolve name(s) from the database (species prefix optional)
  - `--mirna-species goat` (or `chi`) — **fetch every mature miRNA of that species** from the database
  - database access goes through `scripts/fetch_mirnas.py`: local `--mature-fa` > cache > miRBase download (several URLs) > RNAcentral name lookup. Everything is cached under `~/.cache/mirna-target-tools/`, so later runs work offline. If the network is blocked, `python scripts/fetch_mirnas.py --species goat --mature-fa /path/to/mature.fa` still works from a local copy.
- **Prediction engine** (`--method`):
  - `seed` — canonical TargetScan seed sites (8mer / 7mer-m8 / 7mer-A1 / 6mer, weights 4/3/2/1). This is TargetScan's *site definition* only, **not** context++: that model needs pre-computed multi-species UTR alignments and does not exist for sheep/goat
  - `miranda` — run miRanda (Enright et al. 2003) over every miRNA x transcript pair: full duplex alignment with score and dG
  - `hybrid` — (**recommended**, and the default when miRanda is installed) seed sites are kept only when a miRanda alignment overlaps them, and each confirmed site carries its miRanda score and dG; this combines the precise seed definition with thermodynamic evidence
  - `auto` — hybrid when miRanda is available, otherwise seed
- **Target region** (`--target-region`): `cdna` (full spliced transcript) or `utr` (3'UTR only, sliced from the Ensembl GTF - miRNA targeting is 3'UTR-dominant, so this is the biologically faithful choice)
- **Tuning**: `--miranda-score` (default 140), `--miranda-energy` (default -20 kcal/mol), `--rnahybrid-energy` (default -20 kcal/mol), `--rnahybrid-dataset` (p-value dataset; only fly/worm/human ship with the tool), `--rnahybrid-max-target` (default 10000 nt - RNAhybrid silently skips longer targets), `--min-utr-length` (default 30 nt), `--jobs`

#### Two documented strategies (pick one)

**Strategy A - three-stage cascade (fast, recommended default)**

```bash
# stage 1 seed scan (whole transcriptome, seconds) -> stage 2 miRanda confirmation
# -> stage 3 RNAhybrid exact-MFE refinement of the top N targets per miRNA
python predict_targets_genome.py --mirna-fa mirna.fa --species goat \
    --target-region utr --method hybrid --refine-rnahybrid 200 \
    --outdir results/genome --prefix goat_cascade
```

Cheap because RNAhybrid (by far the slowest engine) only ever sees a few hundred
transcripts; `mfe_verified` in `*_targets.tsv` marks whether the refined target
actually passed the MFE cutoff.

**Strategy B - triple parallel + intersection (slow, most complete data)**

```bash
# all three engines run over everything; only targets supported by ALL THREE survive
python predict_targets_genome.py --mirna-fa mirna.fa --species goat \
    --target-region utr --method triple \
    --outdir results/genome --prefix goat_triple
```

Every surviving row carries all three evidence types (seed site types + miRanda
score/dG + RNAhybrid MFE/p-value) in the `evidence` column
(`seed+miranda+rnahybrid`). This is the most complete and most conservative
result, but RNAhybrid over a whole transcriptome is ~60-100x slower than miRanda,
so expect hours per handful of miRNAs - run it on 3'UTRs, not full cDNAs, and use
`--jobs`. For a quick single-engine check use `--method rnahybrid` on a small
candidate set.
- **Scale** — seed mode is standard library only (~5 s for the goat transcriptome); hybrid/3'UTR mode needs the miRanda binary and downloads the Ensembl GTF alongside the cDNA

Script: `scripts/predict_targets_genome.py`

## Runtime and hardware

Prediction time depends on **your machine and the engine you pick**, not only on the
dataset. Reference measurements on the development box (16 cores, WSL2; Ensembl goat
cDNA = 34,136 transcripts):

| Step | Reference time | What it scales with |
|---|---|---|
| seed scan, 1 miRNA, full cDNA | ~5 s | single-threaded Python: CPU clock, total sequence length x miRNA count |
| seed scan, 1 miRNA, 3'UTR only | ~1-2 s | same, but 3'UTRs are far smaller than cDNAs |
| miRanda, 1 miRNA, full cDNA | ~48 s (parallel with `--jobs`) | C code, scales roughly linearly with cores |
| RNAhybrid, 1 miRNA, full cDNA | **60-100x slower than miRanda** | exact MFE dynamic programming; cost grows with target length |
| Ensembl download (first run per species) | goat: cDNA 20 MB + GTF 13 MB | your network speed; cached afterwards |

Practical notes:

- `--jobs` parallelises miRanda/RNAhybrid across miRNAs; use `min(cores, #miRNAs)`.
- Scanning is memory-bound: all target transcripts are held in RAM (the goat
  transcriptome fits in a few hundred MB; the human cDNA set may need a few GB).
- A slow laptop or a busy shared server can be 5-20x slower than the table above.
  Prefer `--target-region utr` and the cheaper engines first, then refine the top hits.
- Nothing is downloaded twice: Ensembl cDNA/GTF and miRBase are cached under
  `~/.cache/mirna-target-tools/`.

## Full analysis workflow

**Standard miRNA target prediction + annotation + regulatory network workflow:**

1. Check the environment: confirm TargetScan, miRanda, and Python dependencies are installed
2. Provide the input miRNA list/sequence file
3. Predict targets with TargetScan and miRanda separately — **or**, if you have no TargetScan database, predict genome-wide directly from miRNA sequences with `predict_targets_genome.py`
4. Merge results and take the intersection to obtain high-confidence targets
5. Annotate the target genes (gene annotation + GO/KEGG enrichment) and generate enrichment bubble plots
6. (Optional) Run multi-species conserved sequence analysis on the target miRNA to validate seed-region conservation
7. Generate Cytoscape network files (`.sif`)
8. Guide the user through importing into Cytoscape for visualization and clustering

## Environment check

Run `scripts/check_env.py` before use to check whether the tools are installed:

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/check_env.py
```

If a tool is missing, the script prints installation steps.

## Input formats

- `.txt` file: one miRNA name per line (e.g. hsa-miR-21-5p) — for TargetScan/miRanda
- `.fa` file: FASTA-format miRNA sequence file — usable by every script, including `predict_targets_genome.py`

## Output files

**Target prediction stage:**
- `{sample}_targetscan_results.txt` - raw TargetScan output
- `{sample}_miranda_results.txt` - raw miRanda output
- `{sample}_merged_high_confidence.txt` - merged high-confidence target gene list

**Whole-transcriptome prediction stage (predict_targets_genome.py):**
- `{prefix}_sites.tsv` - one row per predicted site (miRNA, transcript, gene, position, site type, weight, site sequence)
- `{prefix}_targets.tsv` - one row per (miRNA, transcript) ranked by total score, with `site_density_per_kb` / `score_per_kb` for a length-fair comparison (`--sort-by density`) and miRanda hit counts
- `{prefix}_miranda.tsv` - raw miRanda hits (query/target ranges, score, dG) when the miranda or hybrid engine is used
- `{prefix}_run_info.tsv` - run metadata (source, counts, parameters, site weights)

**Annotation stage (output of annotate_targets.py):**
- `{sample}_gene_annotation.tsv` - gene annotation table (symbol -> Entrez/Ensembl ID + description)
- `{sample}_enrichment_all.tsv` - **every tested term** with raw p-value, BH-FDR `q_value`, `significant` flag (GO:BP/CC/MF + KEGG)
- `{sample}_GO_BP.tsv` / `{sample}_GO_CC.tsv` / `{sample}_GO_MF.tsv` / `{sample}_KEGG.tsv` - per-source results filtered to significant terms
- `{sample}_enrichment_dotplot.png` (+ `.svg` with `--svg`) - enrichment dot plot (output of plot_enrichment.py)

**Conservation stage (output of conservation_analysis.py):**
- `{prefix}_aligned.fa` - multiple sequence alignment (with gaps)
- `{prefix}_conservation.tsv` - per-position conservation statistics (identity %, bits, base counts, coverage)
- `{prefix}_summary.tsv` - summary statistics (seed/core region conservation, mean pairwise identity)
- `{prefix}_sequence_logo.png/.svg` - information-content sequence logo
- `{prefix}_alignment.png/.svg` - multiple sequence alignment figure

**Network construction stage:**
- `{sample}_mirna_target_network.sif` - Cytoscape network file
- `{sample}_node_attributes.txt` - node attribute file (importable into Cytoscape)

## Example usage

### Target prediction
```
python targetscan_predict.py --input mirna.txt --output results/targetscan.txt
python miranda_predict.py --mirna mirna.fa --mrna 3utr.fa --output results/miranda.txt
python merge_targets.py --targetscan targetscan.txt --miranda miranda.txt --output merged.txt
```

### Whole-transcriptome prediction from miRNA sequences (new in 2.0.0)
```
# Built-in species (Ensembl cDNA auto-download + cache) - sheep example
python predict_targets_genome.py --mirna-fa mirna.fa --species sheep \
    --outdir results/genome --prefix sheep_targets

# Which species are built in?
python predict_targets_genome.py --list-species

# Your own transcriptome FASTA (any species / assembly)
python predict_targets_genome.py --mirna-fa mirna.fa \
    --mrna-fa my_transcripts.fa --outdir results/genome --prefix my_targets

# Your own genome + GTF annotation (mRNA rebuilt from exons)
python predict_targets_genome.py --mirna-fa mirna.fa \
    --genome-fa genome.fa --gtf annotation.gtf \
    --outdir results/genome --prefix custom_targets

# Quick smoke test: first 2,000 transcripts only, keep top 20 targets per miRNA
python predict_targets_genome.py --mirna-fa mirna.fa --species goat \
    --max-transcripts 2000 --top 20 --outdir results/genome --prefix quick
```

### Target gene annotation
```
# Extract targets from the merged result, then annotate + run GO/KEGG enrichment (goat example)
python annotate_targets.py --input merged.txt --gene-col TargetGene \
    --species goat --output-dir results/annotation

# Visualize enrichment results (dot plot, 300 dpi PNG + editable SVG)
python plot_enrichment.py --input results/annotation/merged_enrichment_all.tsv \
    --output results/annotation/merged_dotplot.png --source KEGG --top 15 --svg

# Other useful knobs: --sort size, --wrap, --figsize "9,7", --title "...", --dpi 600
```

### miRNA conserved sequence analysis
```
# Auto-extract multi-species homologs of miR-21-5p from miRBase, then run conservation analysis
python conservation_analysis.py --mirna miR-21-5p \
    --reference-species hsa --outdir results/conservation --prefix miR-21

# Or supply your own multiple sequence FASTA
python conservation_analysis.py --input-fa homologs.fa \
    --reference-species hsa --outdir results/conservation

# Restrict to a species allow-list + custom seed region
python conservation_analysis.py --mirna miR-21-5p \
    --species hsa,mmu,rno,bta,ssc --seed-start 2 --seed-end 8
```

### Network construction
```
python format_cytoscape.py --input merged.txt --output network.sif --attr-output node_attributes.txt
```

## Dependency installation

**R + ggplot2 (default plotting engine):**

```bash
bash scripts/install_r_deps.sh          # R itself + ggplot2, dplyr, stringr, scales (+ optional svglite, ggrepel, patchwork, ggsci, forcats)
bash scripts/install_r_deps.sh --minimal  # required packages only
```

The installer puts R packages in the user library (`~/R/library`), so it needs no root; if R itself is missing it tries conda/mamba first and otherwise prints the `apt`/`brew` command to run. `scripts/check_env.py` reports whether the R engine is ready.

**Python:**

```bash
bash scripts/install_dependencies.sh    # Ubuntu/Debian and macOS
```

- `pandas`, `numpy` (required for the TargetScan/miRanda merge scripts and enrichment FDR)
- `mygene` (optional; only needed for gene annotation - GO/KEGG enrichment is pure standard library with zero extra dependencies)
- `matplotlib` (optional; **fallback only** - used when R is unavailable)

`predict_targets_genome.py` and the conservation core are pure standard library. Built-in species mRNA sets are **downloaded on demand** from Ensembl and cached under `~/.cache/mirna-target-tools/genomes/` (tens of MB compressed each; human ~ 70 MB), so they are not bundled with the skill — the first run for a species needs network access.
