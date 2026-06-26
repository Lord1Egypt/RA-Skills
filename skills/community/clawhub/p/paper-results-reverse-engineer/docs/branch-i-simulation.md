# Branch I: Methodological / Simulation Study — Detailed Rules

Activated when Axis 1 = Methodological / Simulation study (not true meta-analysis).

## I1: Simulation Study Profile

Additional fields beyond standard Study Profile:
- Methodological domain (meta-analysis methods / psychometric / statistical inference / estimator comparison)
- Simulation purpose (what methods are compared, what problem is solved)
- Simulation factors (all manipulated factors + levels)
- Number of conditions (e.g., 432 unique conditions)
- Number of replications (e.g., 1,000 datasets per condition)
- Data-generating process (how simulated data are generated)
- Compared methods/estimators (full list)
- Performance metrics (Type I error, power, mean error, RMSE, coverage, convergence, bias)
- Real-data illustration (if present, mark as "Application illustration — not core simulation Results")

## I2: N/A Rule

Traditional meta-analysis fields must be marked N/A, not force-filled:
- Literature search: N/A
- Inclusion criteria: N/A
- Number of included real studies (k): N/A (unless real-data illustration)
- Pooled effect size: N/A
- Heterogeneity Q/I² from real studies: N/A (τ is a simulated manipulation factor)
- PRISMA flow: N/A

Supplement with simulation-specific fields: simulated k, simulated δ, simulated τ, publication bias levels, QRP levels, Monte Carlo replications, performance metrics.

## I3: Module B Results Structure

Do NOT use: participant flow, main effect/interaction, pooled effect, heterogeneity Q/I²/τ², publication bias funnel, moderator analysis, PRISMA, inclusion/exclusion, forest plot.

Use instead:
1. Overall simulation design
2. Baseline/ideal condition performance
3. Bias condition performance
4. Heterogeneity condition performance
5. QRP/assumption violation condition performance
6. Estimator-specific strengths and weaknesses
7. Performance metrics comparison: Type I error → power → mean error/bias → RMSE → coverage → convergence
8. Robustness/sensitivity across conditions
9. Real-data illustration (if present)
10. Practical recommendation for method users

## I4: Module D Chart Rules

Priority chart types:
- Simulation design table
- Parameter table
- Multi-panel performance plot (x-y coordinates, lines/points, color groups — NOT heatmap unless color-coded matrix cells)
- Bias/error distribution plot
- Coverage plot
- Power curve
- Convergence table
- Real-data illustration table

**Heatmap naming rule:** "Heatmap" only for color-encoded 2D matrix cells. Multi-panel line/point plots with x-y axes are "multi-panel line plot" / "performance plot" / "panel plot" — not heatmaps.

Each chart must note: which simulation factor, what each panel represents, axes/colors meaning, performance metric, which methods perform best/worst, method × condition interaction, what cannot be inferred.

## I5: Module E Evidence Boundary

Evidence type: "Computational simulation evidence / method performance comparison evidence."

Must state:
- Results describe method performance under specified simulation assumptions and parameter ranges
- Cannot directly infer real psychological effect sizes
- Cannot prove a real psychological phenomenon exists or does not exist
- Method recommendations depend on how closely simulation conditions match real research contexts
- If simulation assumptions change, method performance may change

**Allowed:** "Under these simulation conditions…" / "This method performs well/poorly under this data-generating mechanism"
**Prohibited:** "proves no effect exists" / "proves this method is always best" / "simulation results can directly replace real data analysis"

## I6: Anti-Template Contamination

Four-tier location distinction:

| Tier | Location | Definition | Handling |
|------|----------|-----------|----------|
| a | Analytic body as conclusion | Term erroneously written as this paper's finding | Delete |
| b | Method-background mention | Used when explaining compared methods | Allow with annotation |
| c | N/A contrast | Explicitly declared "N/A" | Allow |
| d | Audit checklist only | Only in G2/G3/G4/G8 self-check tables | Allow |

Specific prohibited terms (Tier a, if appearing as conclusions): pooled effect, PRISMA, included studies, participant sample, intervention group, clinical diagnosis, fMRI, ROI, EEG, mediation, moderation, questionnaire reliability.

Allowed terms: meta-analysis methods, publication bias, QRPs, heterogeneity, Type I error, power, mean error, RMSE, coverage, RE meta-analysis, trim-and-fill, p-curve, p-uniform, PET-PEESE, 3PSM, Monte Carlo, simulation, performance metrics, bias correction, sensitivity analysis.
