---
name: meta-analysis-topic-selector
slug: meta-analysis-topic-selector
version: 1.0.1
description: "Topic selection assessment and topic-report generation for meta-analyses (systematic reviews). Triggered when: you want to do a meta-analysis but don't know what topic to pick; you have a research direction and want to assess whether it is suitable for a meta-analysis; you want to evaluate feasibility / novelty / clinical value of a candidate topic; you want to generate a structured topic report; you need PICO decomposition; you need to choose the meta-analysis type; you want PRISMA 2020 and AMSTAR-2 pre-checks; you need guidance on deduplication searches; you are preparing for PROSPERO registration. Covers intervention / exposure / diagnostic / prognostic meta-analysis topic selection in medicine, epidemiology, pharmacy, nursing, public health, psychology, education, and related fields. Keywords: meta-analysis topic selection, systematic review question, PICO, PRISMA 2020, AMSTAR-2, PROSPERO registration, deduplication search, network meta-analysis topic, IPD meta-analysis topic, dose-response meta-analysis topic."
description_zh: "Topic selection assessment and topic-report generation for meta-analyses (systematic reviews)."
author: wenhan9739
license: MIT-0
category: research
tags:
  - meta-analysis
  - systematic-review
  - research-methodology
  - prisma-2020
  - amstar-2
  - prospero
  - pico
  - evidence-based-medicine
  - academic-writing
  - medical-research
triggers:
  - meta-analysis topic selection
  - systematic review question
  - PICO decomposition
  - PRISMA 2020
  - AMSTAR-2
  - PROSPERO registration
  - deduplication search
  - network meta-analysis topic
  - IPD meta-analysis topic
  - dose-response meta-analysis topic
agent_created: true
---

# meta-analysis-topic-selector

## Overview

This Skill turns "meta-analysis topic selection" from an intuition-driven judgment into an auditable, output-driven standardized workflow. It covers the full pipeline from a vague research interest to a PROSPERO-ready topic report, with built-in:

- **Dual-path entry**: rapid assessment (≤30 min for a feasibility verdict) / full assessment (5 stages + PROSPERO pre-registration audit)
- **Four-dimension topic assessment model** (clinical value / methodological feasibility / data availability / novelty, 0–20 quantified)
- **Cross-check rules** (conservative style: auto-detect internal contradictions and force re-review)
- **PICO/PECO operational decomposition spec** (every qualifier must be expressible in a search string)
- **Three-layer deduplication search** (PROSPERO + Cochrane Library + PubMed, with non-English database extension and near-duplicate topic judgment)
- **PRISMA 2020 and AMSTAR-2 key-item compliance preview** (identify methodological risks at topic-selection stage)
- **Meta-analysis type decision tree** (traditional pairwise / NMA / IPD / dose-response / DTA / proportion / genetic association / multivariate)
- **Standardized topic-report generation** (11-section Markdown / HTML output)
- **PROSPERO registration form field mapping** (report fields map directly to the online form)

## When to Use

Triggered when:

1. The user says "I want to do a meta-analysis but don't have a topic" or "Can this direction be done as a meta-analysis?"
2. The user provides a research direction and wants to assess whether it is suitable for a meta-analysis
3. The user already has a concrete PICO and wants deduplication search + feasibility preview
4. The user asks for a structured meta-analysis topic report
5. The user is doing a methodological pre-audit before PROSPERO registration
6. The user already has a topic but a reviewer rejected it as "duplicate" or "no increment" and wants to re-assess

Not applicable when:

- The meta-analysis has already entered data extraction or synthesis (use an execution skill instead)
- Pure literature searching (use a search skill instead)
- Narrative review topic selection (different methodology; this Skill does not apply)
- Critical appraisal of a single RCT (not in scope of meta-analysis)

## Path Selection: Rapid vs Full Assessment

Before entering the workflow, decide which path to take:

| User situation | Path | Output |
|---|---|---|
| "Can this be done as a meta?" "Tell me in 5 min" | **Rapid assessment** | 1-page verdict card (rough 4-dim score + recommendation + key risks) |
| "Give me a topic report" "Pre-PROSPERO audit" | **Full assessment** | 11-section standardized report (dedup search + PRISMA/AMSTAR-2 pre-check) |
| "I was rejected as duplicate" | **Dedup re-audit** | Innovation-increment review report |

### Rapid assessment path (compact)

Execute only Stage 1 → Stage 2 (compact) → Stage 3 (rough scoring). **No dedup search** is performed, but the user must be warned that "rapid-assessment conclusions must be confirmed by dedup search in the full-assessment stage". Output a 1-page verdict card:

```
# Meta topic verdict card
- Research question: [one sentence]
- PICO (compact): P / I / C / O, one line each
- Meta type: [type] + one-sentence rationale
- Four-dim rough score: Clinical [?] / Methodology [?] / Data [?] / Novelty [?(tentative)] / Total [?/20]
- Recommendation: [proceed / hold / not recommended]
- Key risks: [1-2 items]
- Next step: [enter full assessment / re-pick topic / abandon]
- ⚠️ Rapid assessment did not perform a dedup search; the conclusion must be confirmed in the full-assessment stage
```

The "novelty" dimension in rapid assessment can only be a tentative score (anchor 3); it must be confirmed or revised after the three-layer dedup search in the full-assessment stage.

### Full assessment path

Execute the 5-stage workflow below in order.

## Workflow — Meta-analysis topic selection 5-stage workflow

Execute the following 5 stages in order. **Each stage has an explicit decision gate**: if the previous stage fails its threshold, do not enter the next stage; the blocker must be resolved first.

### Stage 1: Research-interest clarification

**Goal**: Narrow the user's vague direction into an assessable research question.

Execution points:
- Ask about the user's core research interest (disease, intervention/exposure, population, preferred study type)
- Ask about the meta-goal (degree thesis / journal publication / grant application / review-style learning); different goals set different rigor bars
- Ask about the user's methodological capability boundary (can they do NMA / IPD / Bayesian methods?)
- Ask about resource constraints (number of collaborators, accessible databases, time budget)

**Decision gate 1**: Output 1–3 candidate research directions, each with a one-sentence research question statement.
- 0 candidates (interest too vague) → ask one more round; if still no direction, suggest a narrative review as practice first
- ≥4 candidates → ask the user to pick 3 by priority to avoid evaluation sprawl
- Candidates highly overlapping (same intervention, different doses) → merge into 1 direction + internal subgroups

**Output**: 1–3 candidate research directions.

### Stage 2: PICO/PECO operational decomposition

**Goal**: Decompose the research direction into a "protocol-ready" PICO/PECO structure.

Load reference: `references/pico-decomposition-guide.md`

Execution points:
- Decompose along P / I (or E) / C / O
- Every qualifier on P must be expressible in a search string (not expressible → not operational enough)
- I/E must specify dose, duration, route, follow-up window
- **Complex interventions** (combination / titration / sequential / planned switch) → follow Section 6 "Complex intervention decomposition spec" of `pico-decomposition-guide.md`
- C and I must be matched in granularity
- O must specify ≥1–2 primary outcomes (one time-to-event outcome recommended); each outcome must specify measurement tool, timepoint, effect-measure type
- After completion, run the "PICO decomposition quality self-check list" of `pico-decomposition-guide.md` item by item
- Output a standard research-question statement: `In [P], does [I] compared with [C] improve [O]?`

**Decision gate 2**: All items on the self-check list pass.
- Any item fails → return to revise PICO; do not enter Stage 3
- If P cannot be operationalized (e.g., "immunotherapy patients" cannot be staged) → return to Stage 1 to re-narrow

**Output**: Full PICO/PECO decomposition + research-question statement + self-check pass confirmation.

### Stage 3: Four-dimension assessment + Meta-type selection

**Goal**: Quantify topic feasibility and decide the appropriate meta-analysis type.

Load references:
- `references/topic-selection-framework.md` (core methodology)
- `references/novelty-assessment-guide.md` (novelty judgment, paired with Stage 4 dedup results)

Execution points:

#### 3.1 Four-dimension assessment

Score each dimension 0–5 per the "four-dimension topic assessment model" of `topic-selection-framework.md`. **Every score must state a reason tied to an anchor** ("should be 4" is not acceptable; you must write "matches anchor 4: resolves a common clinical dilemma with clear decision impact").

Dimensions:
- Clinical value
- Methodological feasibility
- Data availability
- Novelty

#### 3.2 Cross-check rules (conservative style, enforced)

After scoring, **run the following 6 cross-check rules**. Triggering any rule → forced re-review; re-score and state the re-review reason:

| Rule | Trigger | Action |
|---|---|---|
| R1 All-5 | All four dimensions scored 5 | Forced re-review — usually means scoring was too lenient; at least one dimension should be lowered. Re-check against anchors |
| R2 High-clinical AND high-novelty without dedup | Clinical ≥4 AND Novelty ≥4 AND no dedup search done yet | Lower novelty to 3 (tentative); cannot raise until Stage 4 dedup confirms |
| R3 Data vs feasibility contradiction | Data availability ≥4 but Methodological feasibility ≤2 | Re-review — abundant data but infeasible methodology usually means a key blocker was missed |
| R4 Clinical vs data contradiction | Clinical ≥4 but Data ≤2 | Re-review — clinically important but sparse data; consider widening/narrowing PICO |
| R5 Any dimension ≤2 | Any dimension ≤2 | Even if total ≥14, hold; the weak dimension must be addressed first |
| R6 Reason not anchored | Any dimension's reason does not reference an anchor | Return and rewrite the reason |

**Cross-check pass criterion**: None of the 6 rules trigger, or triggered rules have been re-reviewed with a documented action.

#### 3.3 Total-score decision rules

- Total ≥17 and cross-check passes → strongly recommend proceeding
- Total ≥14, no dimension ≤2, cross-check passes → recommend proceeding
- Total ≥10 → hold; revise PICO or methodology
- Total <10 → not recommended
- **Any dimension ≤2 → veto; even total ≥17 is held** (take the stricter of the two)

#### 3.4 Meta-analysis type selection

Choose per the "Meta-analysis type decision tree" of `topic-selection-framework.md`:
- Single intervention vs comparator, simple evidence network → traditional pairwise
- Multi-intervention comparison, ranking needed → Network meta-analysis (NMA)
- Individual patient data needed → IPD meta-analysis
- Exposure/dose vs outcome continuous relationship → Dose-response meta-analysis
- Diagnostic test accuracy → DTA meta-analysis (HSROC or Bivariate)
- Proportion-type outcome → Proportion meta-analysis
- Genetic polymorphism → Genetic association meta-analysis
- Multi-outcome benefit-risk → Multivariate meta-analysis

**Decision gate 3**: Four-dim scoring passes cross-check + total meets bar + meta type selected.
- Total <10 or any dimension ≤2 → hold; return to Stage 2 to revise PICO or abandon
- Cross-check not passed → must re-review first; do not enter Stage 4

**Output**: Four-dim score table (with anchored reasons) + cross-check result + meta type + type rationale.

### Stage 4: Deduplication search + PRISMA/AMSTAR-2 pre-check

**Goal**: Identify prior same-topic work, assess compliance feasibility, decide whether to proceed.

Load references:
- `references/novelty-assessment-guide.md` (dedup flow + near-duplicate judgment)
- `references/prisma-2020-checklist.md` (PRISMA 2020 pre-check)
- `references/amstar-2-checklist.md` (AMSTAR-2 self-check)

#### 4.1 Three-layer deduplication search

Execute per "three-layer dedup search flow" of `novelty-assessment-guide.md`:

1. **PROSPERO search** (https://www.crd.york.ac.uk/prospero/)
   - Query: core intervention + disease (no need to add "meta-analysis")
   - Record hits and status (Ongoing / Completed / Stopped)

2. **Cochrane Library search** (CDSR + CENTRAL)
   - Query: core terms
   - Record hits and publication year

3. **PubMed published meta-analysis search**
   - Query: core terms + (filter: Systematic Review OR Meta-Analysis)
   - Limit to the last 5 years
   - Record hits and key papers

4. **Non-English database extension search** (when the topic involves non-English literature or populations)
   - CNKI / Wanfang / VIP / SinoMed: core intervention terms (in local language) + disease terms + "meta-analysis" or "systematic review" (in local language)
   - Record hits and key non-English meta-analyses

Note: This Skill does not directly query online databases. Use WebFetch to assist with PROSPERO and PubMed; or ask the user to run searches manually and back-fill results. Cochrane Library usually requires a subscription; recommend the user search within their institution.

#### 4.2 Exact-duplicate and near-duplicate judgment

**Exact duplicate** (all four PICO elements identical) → handle per the judgment matrix in `novelty-assessment-guide.md`.

**Near duplicate** (some PICO elements change) → handle per the "near-duplicate judgment matrix" in `novelty-assessment-guide.md`:

| Near-duplicate type | Counts as duplicate? | Action |
|---|---|---|
| Switch within-class intervention (e.g., PD-1 → PD-L1) | Usually no | Proceed, but justify the within-class substitution clinically |
| Switch dose/duration | Usually no | Proceed, but justify the clinical meaning of the dose difference |
| Switch primary outcome (OS → PFS) | Usually no | Proceed, but justify the clinical value of the new outcome |
| Switch subgroup population | Usually no | Proceed, but justify the independent clinical meaning of the subgroup |
| Only switch database scope (e.g., add CNKI) | Usually yes | ❌ Not a sufficient increment; must stack other increments |
| Only switch time window (1–2 yr later) | Borderline | Must stack a new-study increment |

#### 4.3 Innovation judgment

Per the "evidence-increment assessment" of `novelty-assessment-guide.md`:
- List all prior exact- and near-duplicate works
- Assess increment type (new studies / new subgroup / new outcome / new methodology / new scope / new question)
- Apply the "increment sufficiency matrix" to decide sufficiency
- Give a recommendation (proceed / hold / abandon)

**Back-fill the Stage-3 novelty score**: if the dedup result disagrees with the Stage-3 tentative score, you must update the four-dim score and re-run the cross-check rules.

#### 4.4 PRISMA 2020 and AMSTAR-2 pre-check

Per `prisma-2020-checklist.md`, preview compliance for 11 key items (✅ / ⚠️ / ❌). Item numbers follow PRISMA 2020 original (Page MJ et al., BMJ 2021;372:n71):
- #1 Title, #4 Objectives (PICO), #5 Eligibility, #6 Information sources, #7 Search strategy, #8 Selection process, #10 Data items, #11 RoB, #12 Effect measures, #13 Synthesis, #13c Heterogeneity, #16 Study selection (flow diagram), Equity (PROGRESS-Plus, PRISMA-Equity extension)

> **Note on rendering**: The report generator script renders these as `PASS` / `WARN` / `FAIL` (text tokens) for portability. ✅→PASS, ⚠️→WARN, ❌→FAIL. Risk level renders as `LOW` / `MEDIUM` / `HIGH`.

Per `amstar-2-checklist.md`, self-assess key items and avoid 7 critical weaknesses (AMSTAR-2 items 2, 4, 7, 9, 11, 13, 15 per Shea BJ et al., BMJ 2017;358:j4008).

Overall compliance risk:
- 🟢 Low: all ✅ → proceed; recommend PROSPERO registration
- 🟡 Medium: 1–2 ⚠️, no ❌ → proceed; shore up in the protocol
- 🔴 High: ≥3 ⚠️ or any ❌ → hold; re-assess

**Decision gate 4**: dedup + innovation + compliance all pass.
- Innovation "abandon" → terminate; recommend a new topic
- Innovation "hold" → return to Stage 2 to adjust PICO (e.g., new subgroup, new outcome) and re-run dedup
- Compliance 🔴 → pause; resolve the compliance blocker first (e.g., no second reviewer for screening)

**Output**: dedup report + near-duplicate judgment + innovation judgment + PRISMA/AMSTAR-2 preview table + overall compliance risk + (if needed) Stage-3 score back-fill.

### Stage 5: Topic-report generation

**Goal**: Integrate all Stage 1–4 outputs into a standardized topic report.

Two execution modes:

#### Mode A: Script generation (recommended; most complete structure)

1. Assemble structured data per the schema in `scripts/generate_topic_report.example.json`
2. Call `scripts/generate_topic_report.py`:
   ```bash
   # Markdown output (default)
   python scripts/generate_topic_report.py input.json output.md

   # HTML output (auto-detected by extension, or explicit --format)
   python scripts/generate_topic_report.py input.json output.html
   python scripts/generate_topic_report.py input.json output.md --format html
   ```
3. The script auto-generates an 11-section standardized report and emits WARNINGs for missing fields

Script dependency: Python 3.8+ standard library only.

#### Mode B: Manual template fill

Load `assets/topic_report_template.md` and fill by hand or have WorkBuddy populate it.

#### Required 11 sections

Regardless of mode, the final report must contain:
1. Background and rationale
2. PICO/PECO decomposition
3. Meta-analysis type and rationale
4. Four-dimension assessment (with scores, total, and cross-check result)
5. Dedup search report (PROSPERO + Cochrane + PubMed + non-English DB + near-duplicate + innovation judgment)
6. Pre-search strategy and estimated included studies
7. PRISMA 2020 key-item compliance preview
8. Primary outcomes and effect measures
9. Prespecified subgroup and sensitivity analyses
10. Potential risks and mitigations
11. Recommended next steps

**Output**: Full Markdown / HTML topic report (recommend saving to the working directory as `<topic-slug>-topic-report.md`).

#### PROSPERO registration field mapping

After the report is generated, if the user plans to register on PROSPERO, load `assets/prospero-registration-mapping.md` to map report fields directly to the PROSPERO online form to avoid omissions.

## Resources

### references/

Loaded by WorkBuddy on demand at each stage:

- `topic-selection-framework.md` — four-dim assessment model, meta-type decision tree, PICO decomposition points, PRISMA/AMSTAR-2 preview guidance, topic output standard (**core doc**)
- `pico-decomposition-guide.md` — PICO/PECO operational decomposition spec, quality self-check list, common decomposition errors, complex-intervention decomposition spec
- `prisma-2020-checklist.md` — PRISMA 2020 key items (topic-stage preview), #8 data-item and #10 effect-measure examples, risk-level decision, PROSPERO registration advice
- `amstar-2-checklist.md` — AMSTAR-2 key-item self-check, critical-weakness list with avoidance actions, relationship with PRISMA
- `novelty-assessment-guide.md` — three-layer dedup search flow, non-English DB extension, near-duplicate judgment matrix, evidence-increment assessment, increment sufficiency matrix, dedup report template

Loading strategy:
- Stage 2 loads `pico-decomposition-guide.md`
- Stage 3 loads `topic-selection-framework.md` (novelty is tentative; no need to load novelty-assessment-guide yet)
- Stage 4 loads `novelty-assessment-guide.md`, `prisma-2020-checklist.md`, `amstar-2-checklist.md`
- After Stage 5 (if registering PROSPERO) load `assets/prospero-registration-mapping.md`

### scripts/

- `generate_topic_report.py` — topic-report generator. Input JSON, output standardized Markdown or HTML report (11 sections). Python standard library only. Supports schema validation (warn mode) and missing-field warnings.
- `generate_topic_report.example.json` — full example of the input JSON; also serves as the schema doc.

### assets/

- `topic_report_template.md` — Markdown template (with Mustache placeholders) for manual fill.
- `prospero-registration-mapping.md` — mapping table between the PROSPERO online registration form fields and this Skill's report fields, with fill tips.

## Output Specification

Final deliverables:

1. **Topic-report Markdown / HTML file** (required): save to the working directory as `<topic-slug>-topic-report.md` or `.html`
2. **Structured JSON data file** (optional): retain for easy revision later
3. **Conversational summary** (required): a ≤200-word core conclusion including four-dim total + cross-check result, compliance risk, recommendation
4. **PROSPERO field-mapping table** (conditional): delivered when the recommendation is "proceed" and the user plans to register

## Common Pitfalls (must avoid during execution)

1. **Skipping dedup search**: scoring right after the user has a PICO → you must run dedup first; otherwise the topic may overlap heavily with a recent publication
2. **PICO too coarse**: P = "solid tumor patients", I = "PD-1 inhibitor" → heterogeneity explosion; must operationalize to a searchable granularity
3. **Complex intervention not decomposed**: I = "PD-1 + targeted" without specifying the targeted agent → dose-response not comparable; must follow Section 6 of `pico-decomposition-guide.md`
4. **Wrong meta type**: multi-intervention comparison but choosing traditional pairwise → should be NMA
5. **No prespecified subgroups**: total pool only → heterogeneity unexplained; must prespecify ≥3 subgroup analyses
6. **No prespecified heterogeneity threshold**: only looking at I² post hoc → must prespecify at topic stage (e.g., I² > 50% triggers subgroup analysis)
7. **Over-optimistic scoring**: all dimensions 5 → must check against anchors in `topic-selection-framework.md` and run cross-check rules R1–R6
8. **Cross-check not run**: pushing forward with raw scores → must run the 6 rules first; if triggered, forced re-review
9. **PROGRESS-Plus equity dimension missing**: PRISMA 2020 item #16 → must consider region, ethnicity, sex, socioeconomic status
10. **Recommending proceed but no PROSPERO mention**: any 🟢 or 🟡 topic → "Recommended next steps" must include PROSPERO registration
11. **Treating near-duplicate as exact duplicate**: abandoning a topic because the PD-1 class was switched → use the near-duplicate matrix to differentiate
12. **Non-English DB not searched**: only PubMed/PROSPERO but not CNKI → topics involving non-English populations or publications must extend to non-English DBs
13. **Rapid assessment giving a final verdict**: "proceed" without dedup → rapid assessment must say "tentative; confirm in full assessment"

## Reference Standards

This Skill is based on the following international standards and methodological literature:

- PRISMA 2020 — Page MJ et al., BMJ 2021;372:n71
- AMSTAR-2 — Shea BJ et al., BMJ 2017;358:j4008
- Cochrane Handbook for Systematic Reviews of Interventions (Version 6.x)
- GRADE Working Group guidance
- PROGRESS-Plus framework (equity dimensions)
- Cochrane RoB 2 / ROBINS-I / QUADAS-2 / ROBINS-E tool selection guidance

## Example User Prompts

The following user inputs should trigger this Skill:

- "I want to do a meta-analysis on hepatocellular carcinoma immunotherapy but don't know what topic to pick"
- "Can PD-1 + lenvatinib be done as a meta?"
- "Tell me in 5 min whether this can be a meta" (→ triggers rapid assessment path)
- "Help me assess the feasibility and novelty of this meta topic"
- "Generate a meta-analysis topic report"
- "Is this topic duplicated with an existing meta?"
- "Does switching to PD-L1 count as a duplicate?" (→ triggers near-duplicate judgment)
- "Should I choose NMA or traditional pairwise meta?"
- "Can my topic comply with PRISMA 2020?"
- "What do I need to prepare before PROSPERO registration?"
- "My meta was rejected by reviewers as duplicate; what now?" (→ triggers dedup re-audit path)
