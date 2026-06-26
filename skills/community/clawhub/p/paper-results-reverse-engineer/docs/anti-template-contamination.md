# Anti-Template Contamination — Full Specification

Moved from main SKILL.md.

## Absolute Prohibition List

Terms banned from output unless the current paper explicitly contains them:

**Neuroimaging-specific:** CA1, CA23DG, CA3, DG, dentate gyrus, subiculum, entorhinal cortex, perirhinal cortex, parahippocampal, RSA, MVPA, multi-voxel pattern, classifier, neural reinstatement, voxel pattern, pattern similarity, ROI.

**Sleep/EEG-specific:** SO, slow oscillation, spindle, delta power, NREM, SWR, sharp-wave ripple, TMR, targeted memory reactivation, cueing, sleep replay.

**Specific paradigm constructs:** room reliability, ROCN, RRCN, POCN, spatial context, episodic context (unless paper uses exact terms).

## Four-Tier Location Distinction

| Tier | Location | Definition | Handling |
|------|----------|-----------|----------|
| a | Analytic body (Modules A–F) | Term erroneously written as this paper's conclusion/finding | **Pollution — delete** |
| b | Method-background mention | Used when explaining compared methods | Allow, annotate as method background |
| c | N/A contrast | Explicitly declared "N/A" / "不适用" | Allow |
| d | Audit checklist only | Only in G2/G3/G4/G8 self-check tables as verification items | Allow |

Only Tier a counts as true template pollution. Terms appearing only in self-check tables (Tier d) are NOT pollution.

## Branch-Specific Whitelists

### Branch I (Simulation) — Additional Prohibited Terms

When appearing as conclusions (Tier a): pooled effect size, PRISMA, forest plot, funnel plot, literature search strategy, included/excluded studies, participant recruitment, fMRI, ROI, EEG, ERP, clinical diagnosis, DSM, ICD, questionnaire reliability, Cronbach's α, mediation, moderation model.

Allowed in Branch I: meta-analysis, meta-analytic methods, publication bias, QRPs, heterogeneity, Type I error, power, mean error, RMSE, coverage, RE meta-analysis, trim-and-fill, p-curve, p-uniform, PET-PEESE, 3PSM, Monte Carlo, simulation, performance metrics, bias correction, sensitivity analysis.

### Branch B (Clinical/Health Survey) — Whitelist

Terms NOT default-pollution in Branch B clinical/health surveys:

| Term | Allowed as | Pollution when |
|------|-----------|----------------|
| clinical diagnosis | Evidence-boundary mention ("SDS is screening, not clinical diagnosis") | Falsely claiming "clinical diagnosis was performed via structured interview" when not done |
| DSM / ICD | Criteria-reference mention ("SDS items based on DSM criteria") | Falsely claiming "DSM-5 diagnostic classification was used" |
| psychiatric diagnosis | Evidence-boundary mention ("screening cannot replace psychiatric diagnosis") | Falsely claiming "participants' diagnoses were confirmed" |

### Branch H (Qualitative) — Whitelist

Terms NOT default-pollution: theme/subtheme, saturation, member checking/focus group validation, reflexivity/reflexivity statement, intercoder reliability/coding agreement, supplementary appendices, purposive sampling.

Only pollution when falsely claiming the paper used a method step it didn't use (e.g., claiming quantified intercoder reliability for an interpretivist study, or claiming explicit reflexivity when researcher position was never mentioned).

## G3 Self-Check Statement

Module G must explicitly state:
> "Template pollution terms appear only in the self-check table's prohibited-term list, not in the analytic body content."
