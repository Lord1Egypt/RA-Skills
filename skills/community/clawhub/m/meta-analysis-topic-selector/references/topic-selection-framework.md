# Meta-analysis Topic Selection Methodology Framework

This file is the core methodology reference for the meta-analysis-topic-selector skill. Load it when performing topic assessment, generating a topic report, or judging feasibility.

## 1. Four-dimension topic assessment model

Any meta-analysis topic should be assessed on the following four dimensions, each 0–5 points, total 20. We recommend total ≥14 with no dimension ≤2 to proceed.

### Dimension 1: Clinical significance

Assessment points:
- Does it address a controversial question (inconsistent RCT conclusions, divergent guideline recommendations)?
- Does it affect clinical decisions (changing first-line recommendations, revising guidelines, adjusting risk stratification)?
- Does it cover a high-frequency / high-burden disease (incidence, disability, mortality, economic burden)?
- Does it matter for specific subgroups (elderly, children, pregnant women, specific genotypes)?
- Does it address an unmet real-world need (resistance to current therapy, side effects, access)?

Score anchors:
- 5: Directly addresses a guideline-level controversy; expected to change clinical practice
- 4: Resolves a common clinical dilemma with clear decision impact
- 3: Supplements existing evidence; some clinical meaning
- 2: Marginal topic; limited clinical impact
- 1: Pure academic exploration; no direct clinical translation
- 0: No clinical value

### Dimension 2: Methodological feasibility

Assessment points:
- Can the question be answered with meta-analysis methods (pooled effect size possible; sufficient cross-study homogeneity base)?
- Are mature effect-size indicators available (RR/OR/HR/SMD/RD/DOR, etc.)?
- Can heterogeneity sources be identified a priori and analyzed by subgroup?
- Are special methods needed (NMA, IPD, dose-response, DTA), and are they mature and executable?
- Data extraction difficulty (does it depend on unpublished individual data; does it require contacting original authors)?

Score anchors:
- 5: Standard methods directly applicable; effect size clearly defined
- 4: Light methodological adaptation needed, but mature toolchain
- 3: Special meta type needed, but with precedent
- 2: Methodologically complex; may require a methodologist
- 1: Methodological uncertainty; feasibility doubtful
- 0: Methodologically infeasible

### Dimension 3: Data availability

Assessment points:
- Estimated number of included studies after pre-searching PubMed / Embase / Cochrane CENTRAL / CNKI (≥5 independent studies recommended for pooling; <3 suggests a narrative review instead)
- Consistency of primary outcome reporting across original studies (same definition, same measurement timepoint, same statistic)
- Is there an IPD need, and the estimated author response rate?
- Are gray-literature sources needed (conference abstracts, trial registries)?
- Language scope (English-only vs multilingual) and its impact on workload

Score anchors:
- 5: Pre-search ≥10 studies; outcomes consistently reported
- 4: 6–10 studies; outcomes mostly consistent
- 3: ~5 studies; minor data conversion needed
- 2: <5 studies but poolable
- 1: Sparse data; may not be poolable
- 0: No usable data

### Dimension 4: Novelty

Assessment points:
- Has a same-topic meta-analysis already been published (search PROSPERO, Cochrane Library, PubMed with systematic-review filter)?
- Publication date of the most recent prior meta-analysis (≥3 years → update is reasonable; <3 years → must clearly state the new evidence increment)
- Is there a previously uncovered angle (new subgroup, new outcome, new comparator, new methodology)?
- Are the latest studies integrated (especially large RCTs)?
- Is a new method applied (NMA, IPD, ML-assisted screening)?

Score anchors:
- 5: No prior meta-analysis; first integration of new evidence
- 4: Prior meta-analysis ≥3 years old; update is reasonable
- 3: Prior meta-analysis <3 years old, but with a clear evidence increment
- 2: Heavily overlaps with existing meta-analyses; limited added value
- 1: Pure duplication; no new evidence
- 0: Already fully covered by a Cochrane review

## 2. Meta-analysis type decision tree

Choose the appropriate meta type by question shape:

```
Research-question shape
│
├─ Single intervention vs comparator, ≥2 comparison arms, simple evidence network
│   └─ Traditional pairwise meta-analysis
│
├─ Multi-intervention comparison, complex evidence network, ranking needed
│   └─ Network meta-analysis (NMA)
│       ├─ Frequentist (e.g., mvmeta, netmeta)
│       └─ Bayesian (e.g., BUGS/JAGS + gemtc)
│
├─ Individual patient data needed for subgroup or dose analysis
│   └─ Individual patient data (IPD) meta-analysis
│
├─ Exposure/dose has a continuous relationship with outcome
│   └─ Dose-response meta-analysis
│       ├─ Restricted cubic splines (Greenland method)
│       └─ First-difference method (Orsini method)
│
├─ Diagnostic test accuracy
│   └─ Diagnostic test accuracy (DTA) meta-analysis
│       ├─ HSROC model (threshold varies)
│       └─ Bivariate model (threshold fixed)
│
├─ Proportion-type outcome (incidence, prevalence)
│   └─ Proportion meta-analysis (with/without transformation)
│
├─ Genetic polymorphism and disease association
│   └─ Genetic association meta-analysis (including HWE test)
│
└─ Multi-outcome aggregation, comprehensive benefit-risk
    └─ Multivariate meta-analysis
```

## 3. PICO/PECO element decomposition

Every topic must be explicitly decomposed into PICO (intervention studies) or PECO (exposure studies). See `pico-decomposition-guide.md` for details.

Core points:
- P (Population): population definition must be operational (disease stage, age, sex, comorbidities, prior therapy)
- I/E (Intervention/Exposure): precise definition (dose, duration, route, follow-up timepoint)
- C (Comparator): comparator type (placebo, active comparator, different dose, different regimen)
- O (Outcome): primary and secondary outcomes (with measurement tool, timepoint, effect-size type)

## 4. PRISMA 2020 and AMSTAR-2 compliance pre-check

At the topic stage, you should already preview compliance against the key items of PRISMA 2020 and AMSTAR-2. See:
- `prisma-2020-checklist.md`
- `amstar-2-checklist.md`

Topic-stage focus:
1. Can a clear search strategy be formed (PRISMA items #6 information sources + #7 search strategy)?
2. Can explicit eligibility criteria be defined (PRISMA item #5)?
3. Can two independent reviewers screen and extract data (PRISMA items #8 selection process + #10 data items)?
4. Can a RoB assessment be done (PRISMA item #11; Cochrane RoB 2 / ROBINS-I / QUADAS-2 by type)?
5. Can evidence grading be done (GRADE)?

## 5. Deduplication search flow

To avoid duplicate topics, you must run the following three-step dedup search at the topic stage:

1. **PROSPERO search** (https://www.crd.york.ac.uk/prospero/)
   - Query: core intervention + disease + "systematic review" or "meta-analysis"
   - Watch for ongoing registrations
2. **Cochrane Library search** (CDSR + CENTRAL)
   - Look for published or ongoing Cochrane reviews
3. **PubMed search**
   - Query: core terms + (filter: Systematic Review OR Meta-Analysis)
   - Limit to the last 5 years

Dedup decision rules:
- If PROSPERO has a same-topic registration → you must state the evidence increment or abandon
- If Cochrane has a same-topic review → usually abandon, unless there is major new evidence
- If a published meta-analysis is ≥3 years old → an "update meta-analysis" is acceptable, but the increment must be stated

See `novelty-assessment-guide.md` for details.

## 6. Topic output standard

The final topic should output the following structured content (rendered into a report by `scripts/generate_topic_report.py`). The report has 11 sections (the title and metadata header are not counted as a section):

1. Background and rationale
2. PICO/PECO decomposition
3. Meta-analysis type and rationale
4. Four-dimension assessment table (with scores and reasons)
5. Dedup search results summary
6. Pre-search strategy and estimated number of included studies
7. PRISMA 2020 key-item compliance preview
8. Primary outcomes and effect-size indicators
9. Planned subgroup and sensitivity analyses
10. Potential risks and mitigations
11. Recommended next steps (register PROSPERO / full search / abandon)
