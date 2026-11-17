# Standard miRNA target prediction + annotation workflow

## Full workflow steps

### 1. Prepare input files

**Input 1: miRNA list (`mirna_list.txt`)**
```
hsa-miR-21-5p
hsa-miR-155-5p
hsa-miR-146a-5p
```

**Input 2: miRNA FASTA (`mirna.fa`)**
```
>hsa-miR-21-5p
UAGCUUAUCAGACUGAUGAUGA
>hsa-miR-155-5p
UUAAUGCUAAUCGUGAUAGGGGU
```

**Input 3: 3'UTR FASTA (`3utr.fa`)**  
Downloadable from Ensembl/UCSC.

### 2. Check the environment

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/check_env.py
```

If anything is missing, run the installer:
```bash
bash ~/.openclaw/skills/mirna-target-tools/scripts/install_dependencies.sh
```

### 3. Run TargetScan

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/targetscan_predict.py \
  --input mirna_list.txt \
  --output results/targetscan_raw.txt \
  --database /path/to/targetscan_db \
  --species human \
  --parse
```

Output:
- `results/targetscan_raw.txt` - raw output
- `results/targetscan_raw.txt.tsv` - parsed table

### 4. Run miRanda

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/miranda_predict.py \
  --mirna mirna.fa \
  --mrna 3utr.fa \
  --output results/miranda_raw.txt \
  --energy-cutoff -15 \
  --score-cutoff 60 \
  --parse
```

Output:
- `results/miranda_raw.txt` - raw output
- `results/miranda_raw.txt.tsv` - parsed table

### 5. Merge results

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/merge_targets.py \
  --targetscan results/targetscan_raw.txt.tsv \
  --miranda results/miranda_raw.txt.tsv \
  --output results/merged_high_confidence.tsv
```

### 6. Target gene annotation (new)

Functional annotation + GO/KEGG enrichment of the merged high-confidence targets:

```bash
# Extract targets from the merged result (column name TargetGene), then annotate + enrich
python3 ~/.openclaw/skills/mirna-target-tools/scripts/annotate_targets.py \
  --input results/merged_high_confidence.tsv \
  --gene-col TargetGene \
  --species goat \
  --output-dir results/annotation
```

Output (under `results/annotation/`):
- `merged_high_confidence_gene_annotation.tsv` - gene annotation (symbol -> Entrez/Ensembl ID + description)
- `merged_high_confidence_enrichment_all.tsv` - all enrichment results
- `merged_high_confidence_GO_BP.tsv` / `_GO_CC.tsv` / `_GO_MF.tsv` / `_KEGG.tsv` - per-source results

**Supported species**: human / mouse / rat / sheep / goat / cow

**Direct gene list input** (no need to extract from the merged result):
```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/annotate_targets.py \
  --input gene_list.txt --plain-list \
  --species human --output-dir results/annotation
```
where `gene_list.txt` has one gene symbol per line.

### 7. Enrichment result visualization (new)

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/plot_enrichment.py \
  --input results/annotation/merged_high_confidence_enrichment_all.tsv \
  --output results/annotation/enrichment_bubble.png \
  --source KEGG --top 15
```

Output: `results/annotation/enrichment_bubble.png` (300 dpi bubble plot)

### 8. Generate the Cytoscape network

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/format_cytoscape.py \
  --input results/merged_high_confidence.tsv \
  --output results/mirna_target_network.sif \
  --attr-output results/node_attributes.txt
```

### 9. Cytoscape visualization

1. Open Cytoscape
2. `File -> Import -> Network from File` -> select the `.sif` file
3. `File -> Import -> Table from File` -> select `node_attributes.txt`, choosing "Import as Node Table"
4. Apply a layout: `Layout -> yFiles Organic`
5. Styling:
   - Map `NodeType` to **Node Fill Color**
   - Adjust **Node Size** by node degree to highlight hub genes
   - Apply a default style template or use VizMapper to polish

## Whole-transcriptome target prediction from miRNA sequences (v2.0.0)

Use this when you have **only miRNA sequences** and want every target site across a
species' mRNA set - no TargetScan database needed. It is independent of the
TargetScan/miRanda workflow above and can be used on its own.

### 0. Get the miRNA sequences (optional)

You do not have to prepare a FASTA - the toolkit can fetch sequences itself:

```bash
# every mature miRNA of a species
python3 ~/.openclaw/skills/mirna-target-tools/scripts/fetch_mirnas.py \
  --species goat --out goat_mirnas.fa

# a few by name (species prefix optional)
python3 ~/.openclaw/skills/mirna-target-tools/scripts/fetch_mirnas.py \
  --names miR-21-5p,chi-miR-504-5p --out picked.fa
```

Sources are tried in order: a local `--mature-fa` > the cache > the miRBase download
(several URLs) > an RNAcentral name lookup; everything is cached under
`~/.cache/mirna-target-tools/`. The predictor accepts the same shortcuts directly:
`--mirna-species goat` or `--mirna miR-21-5p,chi-miR-504-5p`.

### 1. Pick the built-in species

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py --list-species
```

Built-in presets: human, mouse, rat, sheep, goat, cow, pig, chicken (aliases such as
`hsa`, `chi`, `oar`, `mmu` are accepted). The Ensembl cDNA FASTA for the species is
downloaded on first use and cached in `~/.cache/mirna-target-tools/genomes/`.

### 2. Run the prediction

```bash
# built-in species (sheep example)
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --species sheep \
  --outdir results/genome --prefix sheep_targets

# your own transcriptome FASTA (any species / assembly)
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --mrna-fa my_transcripts.fa \
  --outdir results/genome --prefix my_targets

# your own genome + GTF annotation (mRNA rebuilt by joining exons)
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --genome-fa genome.fa --gtf annotation.gtf \
  --outdir results/genome --prefix custom_targets

# quick smoke test: first 2,000 transcripts, top 20 targets per miRNA
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --species goat --max-transcripts 2000 --top 20 \
  --outdir results/genome --prefix quick
```

### 3. Output

- `{prefix}_sites.tsv` - one row per predicted site (position, site type, weight, site sequence)
- `{prefix}_targets.tsv` - one row per (miRNA, transcript), ranked by total score
- `{prefix}_run_info.tsv` - run metadata (source, counts, parameters, site weights)

### 4. Engines and target region

- `--method seed` (default fallback): TargetScan site definitions only.
- `--method miranda`: full miRanda duplex scan (score + dG) - works for any species,
  but permissive on its own; tighten with `--miranda-score` / `--miranda-energy`.
- `--method hybrid` (**recommended**, default when miRanda is installed): keeps only seed
  sites that a miRanda alignment overlaps, and reports score + dG for each.
- `--target-region utr`: scan only 3'UTRs (sliced from the Ensembl GTF, downloaded
  automatically for built-in species) instead of full transcripts; `--min-utr-length`
  controls how short a 3'UTR may be to stay in the run.

Example:

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --species goat --target-region utr --method hybrid \
  --outdir results/genome --prefix goat_hybrid
```

### 5. Which strategy: cascade or triple?

| | A - three-stage cascade (**fast**) | B - triple parallel (**slow, most complete**) |
|---|---|---|
| Command | `--method hybrid --refine-rnahybrid N` | `--method triple` |
| Engines | seed -> miRanda -> RNAhybrid on the top N only | seed + miRanda + RNAhybrid over everything |
| Keeps | seed sites confirmed by a miRanda alignment, with exact MFE for the refined top N | only targets supported by **all three** engines |
| Evidence per row | seed type + miRanda score/dG (+ MFE, `mfe_verified`) | seed type + miRanda score/dG + RNAhybrid MFE/p-value (`evidence` column) |
| Runtime | seconds-to-minutes per miRNA | RNAhybrid is ~60-100x slower than miRanda: hours per few miRNAs; keep to 3'UTRs and use `--jobs` |

```bash
# A: cascade
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --species goat --target-region utr --method hybrid \
  --refine-rnahybrid 200 --outdir results/genome --prefix goat_cascade

# B: triple + intersection
python3 ~/.openclaw/skills/mirna-target-tools/scripts/predict_targets_genome.py \
  --mirna-fa mirna.fa --species goat --target-region utr --method triple \
  --outdir results/genome --prefix goat_triple
```

### 6. Method and caveats

Sites use the canonical TargetScan seed types (8mer / 7mer-m8 / 7mer-A1 / 6mer) with
transparent weights 4 / 3 / 2 / 1 and a per-transcript sum. This is a transparent
**seed heuristic, not TargetScan context++** - use it to prioritise candidates, then
confirm key hits with TargetScan/miRanda or experimental validation.

Quick knobs: `--max-transcripts N`, `--top N`, `--min-score X`, `--refresh`.

### 7. Continue downstream

Feed `{prefix}_targets.tsv` (column `gene_name`) straight into the annotation step:

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/annotate_targets.py \
  --input results/genome/sheep_targets.tsv --gene-col gene_name \
  --species sheep --output-dir results/annotation
```

## miRNA conserved sequence analysis (standalone)

Multi-species conservation analysis of a target miRNA to validate seed-region conservation (publication grade). This feature is independent of the target prediction workflow and can be used on its own.

### Auto-extract homologs from miRBase

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/conservation_analysis.py \
  --mirna miR-21-5p \
  --reference-species hsa \
  --outdir results/conservation \
  --prefix miR-21
```

On first run it downloads miRBase `mature.fa` (cached in `~/.cache/mirna-target-tools/`).
You can also point to a local file with `--mature-fa`.

### Supply your own multiple sequence FASTA

```bash
python3 ~/.openclaw/skills/mirna-target-tools/scripts/conservation_analysis.py \
  --input-fa homologs.fa \
  --reference-species hsa \
  --outdir results/conservation
```

### Key parameters

| Parameter | Description | Default |
|------|------|------|
| `--mirna` | target miRNA (e.g. miR-21-5p, without species prefix) | - |
| `--input-fa` | user-supplied multiple sequence FASTA (mutually exclusive with --mirna) | - |
| `--reference-species` | reference species prefix used as the alignment anchor (e.g. chi/hsa) | first sequence |
| `--species` | allow-list of species prefixes (comma-separated) | all |
| `--seed-start/--seed-end` | seed region range | 2 / 8 |
| `--mature-fa` | local miRBase mature.fa | auto-download |
| `--no-plot` | skip plotting (TSV output only) | plot |

### Output

- `{prefix}_aligned.fa` - multiple sequence alignment (with gaps)
- `{prefix}_conservation.tsv` - per-position conservation (identity %, bits, base counts, coverage)
- `{prefix}_summary.tsv` - summary (seed/core region conservation, mean pairwise identity)
- `{prefix}_sequence_logo.png/.svg` - information-content sequence logo
- `{prefix}_alignment.png/.svg` - multiple sequence alignment figure

## Plotting engine

All figures (enrichment dot plots, sequence logo, alignment) are drawn with **R + ggplot2**
by default:

```bash
bash scripts/install_r_deps.sh   # R + ggplot2/dplyr/stringr/scales (no root needed)
python3 scripts/check_env.py     # reports whether the R engine is ready
```

Every plotting script accepts `--engine auto|r|python` (`auto` = R when available, else the
matplotlib fallback). Both engines write 300 dpi PNG; add `--svg` for an editable vector file.

## Statistical notes

- Enrichment: `{prefix}_enrichment_all.tsv` keeps **all tested terms** with raw `p_value`
  and a Benjamini-Hochberg `q_value` computed within each source over the full tested
  family; `significant` marks `p < 0.05 & q < 0.05`. The per-source `_GO_*.tsv` / `_KEGG.tsv`
  files contain the significant subset.
- Whole-transcriptome prediction: raw scores scale with transcript length, so
  `site_density_per_kb` / `score_per_kb` are provided for a fair comparison
  (`--sort-by density`). Seed-based ranking is a prioritisation aid, not TargetScan context++.

## Runtime depends on your computer

Reference numbers (16-core WSL2 box, goat cDNA = 34,136 transcripts): seed scan ~5 s
per miRNA (single-threaded, so CPU clock matters most); miRanda ~48 s per miRNA,
parallelised with `--jobs` and scaling roughly with cores; RNAhybrid 60-100x slower
than miRanda. Memory is proportional to the target set held in RAM (goat: a few
hundred MB; human cDNA: a few GB). An older laptop or a busy shared server can be
5-20x slower. Strategy: cheap engines and 3'UTRs first, then refine the top hits.

## Parameter guidance

| Parameter | Lenient | Strict |
|------|------|------|
| TargetScan context score | -0.1 | -0.5 |
| miRanda energy | -10 | -20 |
| miRanda score | 50 | 80 |
| enrichment p-value threshold | 0.05 | 0.01 |

## FAQ

**Q: TargetScan can't find a database?**  
A: Download the database for your species manually from https://www.targetscan.org/ and point to it with `--database`.

**Q: miRanda fails to compile?**  
A: Check that gcc is installed. On Ubuntu: `sudo apt-get install build-essential`.

**Q: Too few results?**  
A: Loosen the cutoff parameters, or stop taking only the intersection.

**Q: Annotation reports "Invalid organism"?**  
A: Confirm the species name. Use `goat` for goat (mapped to g:Profiler's `chircus`) and `sheep` for sheep (`oarambouillet`). The script maps them automatically, so the common names work directly.

**Q: Does annotation need internet access?**  
A: Yes. Gene annotation uses MyGene.info and enrichment uses g:Profiler, both online APIs (no local database download). For offline use, cache the results in advance.

**Q: The enrichment results are empty?**  
A: Possibly no pathway in that species' annotation database is significantly enriched for this gene set; relax the p threshold or confirm the gene symbols match the chosen species.
