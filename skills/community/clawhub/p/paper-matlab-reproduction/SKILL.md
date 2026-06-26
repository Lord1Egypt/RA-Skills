---
name: paper-matlab-reproduction
description: Use this skill when the user wants to reproduce an academic paper in MATLAB from a paper file path, URL, DOI, or PDF. It extracts algorithm figures/tables into pseudocode, resolves cited operations through Google Scholar when needed, builds MATLAB simulation code, runs main scripts, compares results with the paper, and iteratively fixes mismatches up to 3 rounds. Trigger for requests like "复现这篇论文", "根据论文生成 MATLAB 仿真", "paper reproduction", "reproduce algorithm figures", or "把论文算法图表转成 MATLAB 代码".
---

# Paper MATLAB Reproduction

This skill turns a paper into a traceable MATLAB reproduction package. The goal is not only to write code, but to preserve the evidence chain from paper text, algorithm figures/tables, cited operations, parameter sources, and simulation-result comparisons.

## Required input

Ask for missing essentials before implementation:

- Paper source: local file path, URL, DOI, arXiv link, or uploaded PDF.
- Output directory rule: by default, place generated MATLAB code and Chinese documentation in the same folder as the user-provided paper file. If the paper location is not a resolvable local file path, or the folder cannot be found or written to, ask the user to provide an output folder before generating files.
- MATLAB execution availability. If MATLAB is unavailable, generate code and provide a dry-run checklist; if Octave compatibility is requested, keep syntax conservative.

Optional but useful:

- Which figures/tables/results the user most cares about.
- Whether to reproduce all algorithms or only selected ones.
- Whether approximate visual similarity is acceptable when the paper omits exact data.

## Optimized workflow

Follow this sequence. Keep a brief `reproduction_log.md` so later changes are explainable.

1. **Ingest and map the paper**
   - Read the paper source and extract title, authors, year, venue, abstract, keywords, system model, algorithm figures/tables, simulation setup, result figures/tables, and references.
   - Determine the output directory from the paper file's parent folder. If that folder is unavailable, ambiguous, or not writable, ask the user for an output directory instead of silently writing elsewhere.
   - Build an artifact map: `Algorithm Fig/Table -> Section -> Variables -> Related Results -> MATLAB file`.
   - If the PDF text extraction is weak, use OCR or visual inspection for the affected pages and note the limitation.

2. **Generate pseudocode from algorithm figures/tables**
   - For every algorithm figure or algorithm-like table, create one pseudocode block.
   - Preserve the paper's algorithm numbering when available, e.g. `Algorithm 1`, `Fig. 3 flowchart`, `Table II procedure`.
   - Normalize symbols, dimensions, input/output variables, loops, stopping criteria, constraints, and objective functions.
   - Save each pseudocode block in the log before writing MATLAB.

3. **Resolve cited operations**
   - When an algorithm step says or implies "using [n]", "as in [n]", "following Method X", or depends on an undefined operation from another paper, search Google Scholar for the cited work.
   - Read the cited paper or an accessible authoritative source for the specific operation only.
   - Add a compact operation note: citation, source link, operation definition, assumptions, and how it maps into MATLAB.
   - If Google Scholar is inaccessible, state that and use publisher pages, arXiv, Semantic Scholar, Crossref, or the cited PDF as fallback sources.

4. **Extract parameters with a strict priority order**
   - First look in the simulation/results section.
   - If incomplete, look in captions, algorithm descriptions, tables, appendices, and experiment text.
   - If still missing, infer a reasonable value from the system model, field norms, or dimensional consistency.
   - Mark every parameter as one of: `paper-explicit`, `caption-or-table`, `cited-source`, or `inferred`.
   - Tell the user about all inferred parameters before or alongside the final result; do not hide guesses inside code.

5. **Design the MATLAB reproduction structure**
   - Put system model construction, shared configuration, simulation loop, baselines, metrics, plotting, and result export in `main.m`.
   - If the paper has multiple materially different simulation environments, create multiple main scripts named by the differing environment, such as `main_snr_sweep.m`, `main_user_density.m`, or `main_channel_model_rayleigh.m`.
   - Create one MATLAB function file per pseudocode block, e.g. `alg1_resource_allocation.m`.
   - Put helper functions in separate files only when shared by multiple algorithms or needed for clarity.
   - Use deterministic seeds and vectorized MATLAB where practical.

6. **Define comparison targets before running**
   - For every reproduced result, identify the paper target: figure/table number, axes, units, legends, operating points, and expected trend.
   - If exact paper data is unavailable, digitize curves from figures when possible or compare against textual/tabular values.
   - Use multiple similarity measures when appropriate: normalized RMSE, relative error at key points, Pearson correlation, rank/order agreement, and qualitative trend match.

7. **Run and repair**
   - Run every `main*.m` script.
   - Compare generated outputs to the paper targets.
   - If results differ materially, inspect in this order:
     1. parameter source and units,
     2. system model equations,
     3. cited operations,
     4. algorithm translation,
     5. random seeds and Monte Carlo count,
     6. metric definitions and plotting scale.
   - Optimize the MATLAB code up to 3 repair rounds. After each round, record what changed and why.

8. **Deliver final package**
   - Provide MATLAB source files, generated plots/results, `reproduction_log.md`, and a concise final report.
   - Write all descriptive documents in Chinese, including pseudocode explanations, parameter notes, citation-operation notes, reproduction logs, run instructions, and the final report. MATLAB code comments may be Chinese or concise English when needed for compatibility, but user-facing documentation should be Chinese.
   - Report similarity per figure/table and overall similarity.
   - Clearly list unreproduced parts, inferred parameters, unavailable cited papers, and residual gaps.

## File layout

Use this default layout unless the repository already has a suitable structure:

```text
paper-title-reproduction/
├── main.m
├── main_<environment_suffix>.m
├── alg1_<short_name>.m
├── alg2_<short_name>.m
├── helpers/
├── data/
├── results/
│   ├── figures/
│   └── metrics/
├── paper_artifacts/
│   ├── pseudocode.md
│   ├── parameter_table.csv
│   ├── citation_operations.md
│   └── target_results.md
└── reproduction_log.md
```

## Pseudocode format

For each algorithm figure/table, use this template:

```markdown
## Algorithm [paper label]: [short name]

Source: [figure/table/section/page]
Purpose: [one sentence]

Inputs:
- [name, dimension, meaning, source]

Outputs:
- [name, dimension, meaning]

Parameters:
- [symbol] = [value or unknown], source=[paper-explicit/caption-or-table/cited-source/inferred]

Steps:
1. ...
2. ...

Stopping criteria:
- ...

MATLAB function:
- `algN_<short_name>.m`
```

## Parameter table format

Track parameters before coding:

```text
symbol,name,value,unit,source_priority,source_location,notes
N,number of users,20,,paper-explicit,Simulation section p.8,
alpha,path loss exponent,3.5,,inferred,System model typical range,User must be told this was inferred
```

## MATLAB coding rules

- Keep `main*.m` readable: configuration, system model, algorithm calls, metrics, plots, exports.
- Pass parameters through a `cfg` struct instead of scattering constants across files.
- Match the paper's notation in comments when useful, but use MATLAB-safe variable names.
- Save numerical outputs to `results/metrics/*.mat` or `.csv` and plots to `results/figures/`.
- Add short comments for non-obvious equation translations and cited operations.
- Avoid silent magic numbers. Every constant should come from the parameter table or be explained.

## Similarity report

Use this final structure:

```markdown
# MATLAB Reproduction Report

## Paper
- Title:
- Source:

## Reproduced artifacts
- Algorithm figures/tables:
- Result figures/tables:
- Main scripts:

## Parameter audit
- Explicit parameters:
- Caption/table parameters:
- Cited-source parameters:
- Inferred parameters disclosed to user:

## Similarity
| Paper result | Script | Metric | Similarity | Notes |
|---|---|---:|---:|---|

## Repair rounds
| Round | Issue found | Change made | Similarity after change |
|---:|---|---|---:|

## Residual gaps
- ...
```

## Important behavior

- Be transparent about uncertainty. A reproducible approximation with clearly marked assumptions is better than pretending the paper contains missing values.
- Use Chinese for all user-facing description documents and reports unless the user explicitly asks for another language.
- Save generated code and description documents beside the user's paper file by default. If the paper folder cannot be identified or used, ask the user for the target folder before writing outputs.
- Do not overfit a plot by changing algorithms arbitrarily. Repairs should be tied to evidence: parameters, equations, cited methods, or metrics.
- If a paper's results cannot be fairly compared because data is missing or the model is underspecified, say so and provide the closest defensible reproduction.
- When using web sources, cite links in the report.

## Self-Evolution Mechanism

After each execution of this Skill:

1. Evaluate whether the output achieved the intended goal: **pass / fail**.
2. If it fails, reflect on the cause of failure and append a “failure case + improvement suggestion” to `diary/YYYY-MM-DD.md`.
3. If a certain improvement suggestion is repeatedly mentioned in the most recent three executions, refine it into a formal rule and submit a PR to modify this `SKILL.md`.
