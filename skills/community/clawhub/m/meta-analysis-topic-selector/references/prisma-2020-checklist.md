# PRISMA 2020 Checklist (topic-stage preview)

This file is a condensed version of the main PRISMA 2020 items, used at the topic stage to assess "compliance feasibility". Full version: Page MJ et al., BMJ 2021;372:n71.

At the topic stage, you need not confirm all 27 items, but you must preview the following "pre-compliance" key items, marked ✅ compliant / ⚠️ at risk / ❌ not compliant.

> **Note on item numbering**: This checklist uses PRISMA 2020 original item numbers (Page MJ et al., BMJ 2021;372:n71). The "equity" item references the PRISMA-Equity extension (Welch V et al., PLoS Med 2012) and PROGRESS-Plus framework, as PRISMA 2020 itself does not have a standalone equity item — equity is addressed within item 23 (Discussion) and the PRISMA-Equity extension.

## PRISMA 2020 items to preview at the topic stage

### Title and abstract

**Item #1 — Title**: Can you write a title that identifies the work as a systematic review / meta-analysis?
- Preview: ✅ / ⚠️ / ❌

### Background

**Item #3 — Rationale**: Can you clearly state the controversy or gap in existing evidence in the protocol?
- Preview: ✅ / ⚠️ / ❌

**Item #4 — Objectives**: Is the research question (PICO) clear and operational?
- Preview: ✅ / ⚠️ / ❌
- Key risk: vague PICO → ❌

### Methods

**Item #5 — Eligibility criteria**: Can you write explicit eligibility criteria consistent with PICO?
- Preview: ✅ / ⚠️ / ❌

**Item #6 — Information sources**: Can you list ≥3 databases (PubMed, Embase, Cochrane CENTRAL) + gray-literature sources?
- Preview: ✅ / ⚠️ / ❌
- Gray-literature sources: ClinicalTrials.gov, ICTRP, conference abstracts, reference snowballing

**Item #7 — Search strategy**: Can you write a complete search string (MeSH, Emtree, free terms, Boolean logic)?
- Preview: ✅ / ⚠️ / ❌

**Item #8 — Selection process**: Can you implement at least two independent reviewers + arbitration?
- Preview: ✅ / ⚠️ / ❌
- Key risk: single-reviewer screening → ❌ (PRISMA 2020 mandates two)

**Item #10 — Data items**: Can you define a standardized data-extraction form (fields, value specs, responsible person)?
- Preview: ✅ / ⚠️ / ❌
- Minimum required data-extraction fields (example):

  | Field category | Example fields |
  |---|---|
  | Study identifier | First author, publication year, PMID, registration number |
  | Study design | Design type (RCT/NRSI/cohort), randomization method, blinding |
  | Population | n (intervention/control), age, sex, stage, comorbidities |
  | Intervention | Drug, dose, duration, route, follow-up length |
  | Outcome (one set per outcome) | n events, effect size (HR/RR/OR/SMD), 95% CI, p value, measurement timepoint |
  | Risk of bias | RoB 2 / ROBINS-I / QUADAS-2 domain ratings |
  | Funding | Funding source, conflict-of-interest statement |

- ⚠️ risk signal: only "study name + effect size" → data-extraction form too narrow; cannot subgroup later
- ❌ not-compliant signal: no prespecified data-extraction form, relying on "read-and-note-as-you-go" → not compliant

**Item #11 — Risk of bias assessment**: Can you choose an appropriate RoB tool?
- Preview: ✅ / ⚠️ / ❌
- RoB tool selection:
  - RCT → Cochrane RoB 2
  - Non-randomized intervention study → ROBINS-I
  - Diagnostic test → QUADAS-2
  - Observational study → ROBINS-E / Newcastle-Ottawa Scale

**Item #12 — Effect measures**: Can you prespecify the effect-size type and direction for each outcome?
- Preview: ✅ / ⚠️ / ❌
- Effect-size prespecification examples (by outcome type):

  | Outcome type | Recommended effect size | Direction definition | Data extraction format |
  |---|---|---|---|
  | Time-to-event (OS/PFS) | HR + 95% CI | HR<1 = intervention better | log HR + SE, or HR + 95% CI + n events |
  | Binary (ORR/SAE) | RR + 95% CI | RR<1 = intervention better (benefit); RR>1 = intervention higher risk (adverse) | 2×2 table (a/b/c/d) |
  | Continuous (QoL/score) | SMD + 95% CI | SMD>0 = intervention better | mean + SD + n (both arms) |
  | Proportion (prevalence) | Proportion + 95% CI (transformed) | — | n events + n total |
  | Diagnostic accuracy | DOR / sensitivity / specificity | — | TP/FP/FN/TN |

- ⚠️ risk signal: direction not specified (e.g., "use RR" without saying whether RR<1 is good) → direction chaos in subgroups
- ❌ not-compliant signal: effect-size type not prespecified; choosing post hoc whichever has p<0.05 → serious violation of the prespecification principle

**Item #13 — Synthesis methods**: Can you prespecify the synthesis method (fixed/random effects, subgroups, sensitivity)?
- Preview: ✅ / ⚠️ / ❌

**Item #13c — Heterogeneity (sub-item of #13)**: Can you compute I², τ², Q test and prespecify a threshold (e.g., I² > 50% triggers subgroup analysis)?
- Preview: ✅ / ⚠️ / ❌

### Equity (PRISMA-Equity extension + PROGRESS-Plus)

**Equity / PROGRESS-Plus**: Do you consider PROGRESS-Plus dimensions (place, race, occupation, sex, age, socioeconomic status)?
- Preview: ✅ / ⚠️ / ❌
- Note: PRISMA 2020 does not have a standalone equity item; equity is addressed in item 23 (Discussion, interpretation) and the PRISMA-Equity extension (Welch V et al., PLoS Med 2012). At the topic stage, prespecify PROGRESS-Plus subgroup analyses.

### Results / Reporting

**Item #16 — Study selection (flow diagram)**: Can you draw a standard PRISMA 2020 flow diagram (identification → screening → included → analysis)?
- Preview: ✅ / ⚠️ / ❌
- Note: The PRISMA 2020 flow diagram is reported as a Figure alongside item 16 (Study selection).

## Topic-stage risk-level decision

| Risk level | Criterion | Suggestion |
|---|---|---|
| 🟢 Low | All the above items ✅, no ⚠️ or ❌ | Proceed; recommend PROSPERO registration |
| 🟡 Medium | 1–2 items ⚠️, no ❌ | Proceed; state risk-mitigation measures in the protocol |
| 🔴 High | ≥3 items ⚠️, or any ❌ | Hold; re-assess PICO or methodology |

> **Note on report rendering**: The report generator script (`generate_topic_report.py`) renders these items as `PASS` / `WARN` / `FAIL` (text tokens) rather than emoji, for portability. The mapping is: ✅ → PASS, ⚠️ → WARN, ❌ → FAIL. The risk level renders as `LOW` / `MEDIUM` / `HIGH`.

## Common topic-stage non-compliance risks

1. **#8 two-reviewer screening not guaranteed**: common in single-person projects → bring in a second reviewer or external collaborator
2. **#7 search string cannot cover multilingual**: e.g., including Chinese studies but the search string is English-only → limit language scope or extend
3. **#11 RoB tool mismatched to study type**: e.g., using an RCT tool on real-world studies → choose ROBINS-I for NRSI
4. **Equity / PROGRESS-Plus dimension missing**: often ignoring race/sex subgroups → state PROGRESS-Plus dimensions in the protocol
5. **#13c heterogeneity threshold insufficient**: only looking at I² post hoc → must prespecify the threshold and analysis path at the topic stage

## PROSPERO registration advice

If the topic stage yields 🟢 or 🟡 risk, we recommend registering on PROSPERO immediately after completing the full search strategy, because:
- Locks topic priority (prevents others from publishing first)
- Forces protocol completion (improves methodological rigor; also addresses AMSTAR-2 item 2)
- Is a plus at journal submission (most high-quality journals require or prefer registration)
- Avoids later accusations of "post-hoc outcome picking"

Pre-registration preparation:
- Complete PICO
- Complete search strategy (at least one database)
- Prespecified eligibility criteria
- Prespecified primary and secondary outcomes
- Prespecified synthesis method
