# PRISM-Gen Demo

## Description

PRISM-Gen Demo is a read-only data analysis skill for exploring pre-calculated molecular screening results from the PRISM-Gen broad-spectrum coronavirus Mpro inhibitor discovery pipeline.

All analysis is performed locally on CSV files bundled with the skill. No network access, no external API calls, no credential requirements.

## What This Skill Does

- **Retrieve** data from any of 10 pipeline stage CSV files (step3a through step5b)
- **Filter** molecules by property thresholds (pIC50, QED, MW, LogP, gap_ev, hERG_Prob, etc.)
- **Sort** and rank molecules by any numeric column
- **Merge** data across pipeline stages using SMILES as join keys
- **Score** molecules with composite scoring, worst-case multi-target analysis, summary statistics, and Pareto front identification
- **Plot** property distributions, scatter plots, docking score heatmaps, pipeline attrition funnels, and Pareto fronts
- **Summarize** the full pipeline with attrition statistics and key findings

## What This Skill Does NOT Do

- Does NOT run any computational chemistry calculations (no DFT, no docking, no MD)
- Does NOT access any network or external services
- Does NOT require or use any credentials, API keys, or tokens
- Does NOT modify any files outside its own output directory
- Does NOT contain any shell scripts
- Does NOT use hardcoded absolute paths

## Commands

### retrieve
Retrieve and display data from any pipeline stage.
```
python3 scripts/retrieve.py --stage step5b --columns name,pIC50,Broad_Spectrum_Score --max_rows 10
python3 scripts/retrieve.py --list_stages
python3 scripts/retrieve.py --stage step4a --list_columns
python3 scripts/retrieve.py --stage step5b --name mol_16
```

### filter
Filter molecules by property thresholds. Multiple conditions are combined with AND.
```
python3 scripts/filter.py --stage step4a --where "pIC50>7.5" "QED>0.7" "hERG_Prob<0.5"
python3 scripts/filter.py --stage step5b --where "Broad_Spectrum_Score<-7.0" "Is_Final_Top==True"
```

### sort
Sort and rank molecules by any column.
```
python3 scripts/sort.py --stage step5b --by Broad_Spectrum_Score --ascending --top 10
python3 scripts/sort.py --stage step4c --by R_global --top 20
```

### merge
Merge data across pipeline stages on SMILES keys.
```
python3 scripts/merge.py --stages step3c,step4a --on smiles --columns pIC50,gap_ev,Lipinski_Pass,hERG_Prob
```

### score
Compute composite scores, worst-case analysis, statistics, and Pareto fronts.
```
python3 scripts/score.py --mode worst_case --stage step5a --top 10
python3 scripts/score.py --mode composite --stage step4c --weights "pIC50:1.0,QED:0.5,R_ADMET:2.0"
python3 scripts/score.py --mode stats --stage step5b --columns pIC50,QED,Broad_Spectrum_Score
python3 scripts/score.py --mode pareto --stage step5b --obj1 pIC50 --obj2 QED
```

### plot
Generate visualizations (requires matplotlib).
```
python3 scripts/plot.py --mode histogram --stage step4a --column pIC50 --output hist.png
python3 scripts/plot.py --mode scatter --stage step5b --x pIC50 --y Broad_Spectrum_Score --output scatter.png
python3 scripts/plot.py --mode heatmap --stage step5a --output heatmap.png
python3 scripts/plot.py --mode funnel --output funnel.png
python3 scripts/plot.py --mode pareto --stage step5b --x pIC50 --y QED --output pareto.png
```

### summary
Generate a full pipeline summary report.
```
python3 scripts/summary.py
python3 scripts/summary.py --detailed
```

## Available Pipeline Stages

| Stage Key | Description | Rows | Columns |
|-----------|-------------|------|---------|
| step3a | RL-optimized molecules (generation + surrogate scoring) | 200 | 10 |
| step3a_top | Top 200 molecules by Reward | 200 | 10 |
| step3b | GFN2-xTB electronic structure results | 200 | 6 |
| step3c | xTB-refined ranking with GEM scoring | 200 | 24 |
| step4a | ADMET filtering (Lipinski, hERG, QED) | 200 | 38 |
| step4b | B3LYP/6-31G* DFT validation (PySCF) | 46 | 34 |
| step4c | Master summary (all stages merged) | 200 | 65 |
| step5a | Broad-spectrum docking (3 targets) | 36 | 13 |
| step5b | Final candidates with full annotations | 36 | 75 |
| step5b_master | Master summary with docking | 200 | 74 |

## Dependencies

- **Required:** Python 3.7+ (core functionality uses only Python standard library: csv, json, argparse, math, os, sys)
- **Optional:** matplotlib (for visualization commands only; all non-plot commands work without it)

## Security

- Pure Python implementation — no shell scripts, no subprocess calls, no os.system calls
- No hardcoded paths — all file paths are resolved relative to the skill root directory
- No network access — all data is bundled locally in the data/ directory
- No credentials — no environment variables, API keys, or tokens required
- Read-only on input data — CSV files in data/ are never modified
- Output isolation — generated plots are written only to user-specified paths

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

## Author

@SenaZeng

## Related

- GitHub: https://github.com/SenaZeng/PRISM-Gen
- Zenodo: https://doi.org/10.5281/zenodo.18764996
