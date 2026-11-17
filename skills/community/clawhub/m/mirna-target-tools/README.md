# mirna-target-tools

A complete bioinformatics toolkit for **miRNA target analysis** — from raw miRNA sequences to a Cytoscape-ready network: TargetScan/miRanda workflows, whole-transcriptome seed-based prediction (built-in species or your own genome/transcriptome), gene annotation, GO/KEGG enrichment with Benjamini–Hochberg FDR, seed-region conservation analysis, and publication-quality figures drawn with **R + ggplot2**.

## What it does

- **Sequence fetching** — pull mature miRNA sequences from public databases itself (miRBase / RNAcentral), by name or for a whole species
- **Target prediction** — run TargetScan and miRanda to predict miRNA target genes
- **Whole-transcriptome prediction (v2.0.0)** — predict every target site of your miRNA sequences across a species' full mRNA set; built-in Ensembl presets (human, mouse, rat, sheep, goat, cow, pig, chicken) or bring your own transcriptome / genome+GTF; no TargetScan database needed
- **Result merging** — intersect multiple predictors to obtain high-confidence targets
- **Target annotation & enrichment** — annotate genes (symbol → Entrez/Ensembl ID + description) and run GO (BP/CC/MF) + KEGG enrichment via g:Profiler
- **Conservation analysis** — extract multi-species homologous miRNA sequences from miRBase (or supply your own FASTA), align them with free-end-gap global alignment, and quantify per-position conservation (Shannon bits + identity) with seed-region highlighting and publication-ready sequence logo + alignment plots
- **Enrichment plots** — publication-style dot plots (clusterProfiler-style: size = genes, colour = -log10 p), drawn with **R + ggplot2** by default (matplotlib fallback), 300 dpi PNG plus optional editable SVG
- **Rigor built in** — enrichment reports raw p *and* Benjamini–Hochberg q-values over the full tested family; whole-transcriptome hits carry length-normalised densities
- **Network visualization** — generate Cytoscape-ready `.sif` network files

## Species support

- Annotation / enrichment: human, mouse, rat, **sheep (Ovis aries)**, **goat (Capra hircus)**, cow.
- Whole-transcriptome prediction presets: human, mouse, rat, sheep, goat, cow, pig, chicken — or any species you supply via `--mrna-fa` / `--genome-fa` + `--gtf`.

## Quick start

```bash
# 1. Check environment
python3 scripts/check_env.py

# 2. Predict targets
python3 scripts/targetscan_predict.py --input mirna_list.txt --output targetscan.txt
python3 scripts/miranda_predict.py --mirna mirna.fa --mrna 3utr.fa --output miranda.txt

# 3. Merge (intersection = high confidence)
python3 scripts/merge_targets.py --targetscan targetscan.txt --miranda miranda.txt --output merged.txt

# 4. Annotate + enrich target genes
python3 scripts/annotate_targets.py --input merged.txt --gene-col TargetGene \
    --species goat --output-dir results/annotation

# 5. Plot enrichment (dot plot: size = genes, colour = -log10 p)
python3 scripts/plot_enrichment.py --input results/annotation/merged_enrichment_all.tsv \
    --output enrichment_dotplot.png --source GO:BP --top 15 --svg

# 6. Build Cytoscape network
python3 scripts/format_cytoscape.py --input merged.txt --output network.sif

# 7. Conservation analysis (multi-species homologous miRNAs)
python3 scripts/conservation_analysis.py --mirna miR-21-5p \
    --reference-species hsa --outdir results/conservation --prefix miR-21

# 8. Whole-transcriptome targets straight from miRNA sequences (no TargetScan DB)
python3 scripts/predict_targets_genome.py --mirna-fa mirna.fa --species sheep \
    --outdir results/genome --prefix sheep_targets
```

## Whole-transcriptome prediction (detail)

Predict targets across an entire species transcriptome from **miRNA sequences alone**:

```bash
# built-in species preset (Ensembl cDNA auto-downloaded + cached)
python3 scripts/predict_targets_genome.py --mirna-fa mirna.fa --species sheep \
    --outdir results/genome --prefix sheep_targets

# which species are built in?
python3 scripts/predict_targets_genome.py --list-species

# your own transcriptome FASTA (any species / assembly)
python3 scripts/predict_targets_genome.py --mirna-fa mirna.fa \
    --mrna-fa my_transcripts.fa --outdir results/genome --prefix my_targets

# your own genome + GTF (mRNA rebuilt from exons)
python3 scripts/predict_targets_genome.py --mirna-fa mirna.fa \
    --genome-fa genome.fa --gtf annotation.gtf --outdir results/genome --prefix custom

# quick test: first 2,000 transcripts, keep the top 20 per miRNA
python3 scripts/predict_targets_genome.py --mirna-fa mirna.fa --species goat \
    --max-transcripts 2000 --top 20 --outdir results/genome --prefix quick
```

Two documented strategies: **(A)** three-stage cascade `--method hybrid --refine-rnahybrid N`
(seed -> miRanda -> RNAhybrid exact-MFE on the top N; fast) and **(B)** triple parallel
`--method triple` (seed + miRanda + RNAhybrid over everything, keep only the three-way
intersection; slow but the most complete evidence). See SKILL.md for the full write-up.

Engines (`--method`): `seed` (canonical TargetScan site types), `miranda` (full duplex
alignment with score + dG) or `hybrid` (seed sites confirmed by a miRanda alignment -
recommended, and the default when miRanda is installed). Region (`--target-region`):
`cdna` or `utr` (3'UTR-only, sliced from the Ensembl GTF).

Method: canonical TargetScan seed site types (8mer / 7mer-m8 / 7mer-A1 / 6mer) with
transparent weights 4 / 3 / 2 / 1 and a per-transcript score. It is a transparent
**seed heuristic, not TargetScan context++** — prioritise with it, then confirm key
candidates. Pure standard library; a goat transcriptome (34k transcripts) x 1 miRNA
scans in ~5 s.

Outputs:

- `{prefix}_sites.tsv` — every predicted site (position, site type, weight, site sequence)
- `{prefix}_targets.tsv` — per (miRNA, transcript) ranking by total score
- `{prefix}_run_info.tsv` — run metadata and parameters

Built-in species mRNA sets are downloaded on demand from Ensembl and cached under
`~/.cache/mirna-target-tools/genomes/` (tens of MB compressed each), so they are not
bundled with the skill.

## Conservation analysis (detail)

Two input modes, one pipeline:

```bash
# Mode 1 — auto-extract homologs from miRBase (exact miRBase-ID match, no prefix-collision false hits (e.g. miR-21 vs miR-210))
python3 scripts/conservation_analysis.py --mirna miR-21-5p \
    --reference-species hsa --outdir results/conservation --prefix miR-21

# Mode 2 — supply your own multi-species FASTA
python3 scripts/conservation_analysis.py --input-fa homologs.fa \
    --reference-species hsa --outdir results/conservation --prefix miR-21

# Optional: species whitelist + custom seed region
python3 scripts/conservation_analysis.py --mirna miR-21-5p \
    --species hsa,mmu,rno,bta,ssc --seed-start 2 --seed-end 8
```

Key options:

| Option | Description | Default |
|--------|-------------|---------|
| `--mirna` | Target miRNA ID (e.g. `miR-21-5p`), auto-extract homologs from miRBase | — |
| `--input-fa` | User-provided multi-sequence FASTA (alternative to `--mirna`) | — |
| `--mature-fa` | Local `mature.fa` path (otherwise downloaded & cached to `~/.cache/mirna-target-tools/`) | auto-download |
| `--reference-species` | Alignment anchor species prefix (e.g. `chi`, `hsa`) | first sequence |
| `--species` | Comma-separated species whitelist (e.g. `hsa,chi,bta`) | all |
| `--seed-start` / `--seed-end` | Seed region nt range (highlighted + separately scored) | `2` / `8` |
| `--no-plot` | Skip plots, output TSV only | off |

Outputs (all prefixed with `--prefix`):

- `{prefix}_aligned.fa` — multiple sequence alignment (with gaps)
- `{prefix}_conservation.tsv` — per-position conservation (identity %, Shannon bits, base counts, coverage)
- `{prefix}_summary.tsv` — seed/core-region stats, mean pairwise identity
- `{prefix}_sequence_logo.png/.svg` — information-content sequence logo (WebLogo colors)
- `{prefix}_alignment.png/.svg` — MSA figure (300 dpi)

> Alignment uses free-end-gap global alignment (Needleman–Wunsch variant, pure stdlib): gaps concentrate at the 5'/3' termini (isomiR variation) while the seed region stays strictly aligned.

## Performance

Runtime depends on your hardware and the engine chosen. Measured on a 16-core box
(goat cDNA, 34,136 transcripts): seed scan ~5 s per miRNA; miRanda ~48 s per miRNA
(parallelised by `--jobs`); RNAhybrid 60-100x slower than miRanda. 3'UTR scanning is
far cheaper than full cDNA, and everything downloaded (Ensembl cDNA/GTF, miRBase) is
cached under `~/.cache/mirna-target-tools/`.

## Dependencies

- **Required:** `pandas`, `numpy`
- **R (default plotting engine):** `bash scripts/install_r_deps.sh` — installs R if needed, plus ggplot2/dplyr/stringr/scales into `~/R/library` (no root required)
- **Optional:** `mygene` (gene annotation), `matplotlib` (fallback plots only, used when R is unavailable)

> Conservation analysis core (FASTA/MSA/conservation scoring) is pure standard library — zero third-party deps; it downloads miRBase `mature.fa` on first run (cached) or accepts a local file via `--mature-fa`. Enrichment (GO/KEGG via g:Profiler REST API) is also stdlib-only; `mygene` is only needed for gene-symbol annotation.

See `references/workflow.md` for the full walkthrough.

## Author

**DestinQu**

## License

MIT
