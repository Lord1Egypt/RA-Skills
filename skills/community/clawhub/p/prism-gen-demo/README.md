# PRISM-Gen Demo Skill (v2.0.0)

Interactive data analysis tool for exploring pre-calculated molecular screening results from the **PRISM-Gen** broad-spectrum coronavirus Mpro inhibitor discovery framework.

## Features

| Command | Description |
|---------|-------------|
| `retrieve` | Display data from any pipeline stage (step3a–step5b) |
| `filter` | Filter molecules by property thresholds (pIC50, QED, MW, gap_ev, hERG, etc.) |
| `sort` | Sort and rank by any column |
| `merge` | Join data across pipeline stages on SMILES keys |
| `score` | Composite scoring, worst-case analysis, Pareto front, summary statistics |
| `plot` | Histograms, scatter plots, docking heatmaps, attrition funnel, Pareto plots |
| `summary` | Full pipeline summary report |

## Available Pipeline Stages

| Key | Description | Rows |
|-----|-------------|------|
| `step3a` | RL-optimized molecules (generation + surrogate scoring) | 200 |
| `step3b` | GFN2-xTB electronic structure results | 200 |
| `step3c` | xTB-refined ranking with GEM scoring | 200 |
| `step4a` | ADMET filtering (Lipinski, hERG, QED) | 200 |
| `step4b` | B3LYP/6-31G* DFT validation (top candidates) | 46 |
| `step4c` | Master summary (all stages merged) | 200 |
| `step5a` | Broad-spectrum docking (36 candidates, 3 targets) | 36 |
| `step5b` | Final candidates with all annotations | 36 |

## Quick Examples

```bash
# List all stages
python3 scripts/retrieve.py --list_stages

# View top 10 final candidates
python3 scripts/sort.py --stage step5b --by Broad_Spectrum_Score --ascending --top 10

# Filter for drug-like molecules with good activity
python3 scripts/filter.py --stage step4a --where "pIC50>7.5" "QED>0.7" "hERG_Prob<0.5"

# Worst-case multi-target analysis
python3 scripts/score.py --mode worst_case --stage step5a --top 10

# Generate docking heatmap
python3 scripts/plot.py --mode heatmap --stage step5a --output heatmap.png

# Full pipeline summary
python3 scripts/summary.py --detailed
```

## Requirements

- Python 3.7+ (core functionality has no external dependencies)
- matplotlib (optional, for visualization only)

## License

MIT-0 — Free to use, modify, and redistribute.
