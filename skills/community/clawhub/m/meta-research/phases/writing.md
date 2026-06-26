# Phase: Writing & Dissemination

## Goal

Produce a transparent, reproducible research document and release artifacts that allow
others to evaluate, replicate, and build on the work.

## Entry Conditions

- Analysis is complete with claim assessment
- Confirmatory/exploratory boundary is clear
- Results tables, figures, and run ID mappings are ready

## Step-by-Step Protocol

### Step 1: Choose Reporting Framework

Select the appropriate reporting guideline for your study type:

| Study Type              | Reporting Guideline | Key Resource                |
|-------------------------|--------------------|-----------------------------|
| Randomized experiment   | CONSORT            | consort-statement.org       |
| Observational study     | STROBE             | strobe-statement.org        |
| Systematic review       | PRISMA             | prisma-statement.org        |
| ML/AI experiment        | ML Reproducibility | NeurIPS/ICML checklists     |
| Diagnostic accuracy     | STARD              | stard-statement.org         |
| Case report             | CARE               | care-statement.org          |

For most AI research, the **ML Reproducibility Checklist** (see
[templates/reproducibility-checklist.md](../templates/reproducibility-checklist.md))
is the primary framework, augmented by venue-specific requirements.

### Step 2: Structure the Paper (Methods-First)

Write in this order (not the order sections appear in the paper):

1. **Methods** — what you did, exactly, so someone could reproduce it
2. **Results** — what happened, with uncertainty and ablations
3. **Introduction** — why it matters, what the gap is, what you claim
4. **Related Work** — how this connects to existing evidence (from Lit Review)
5. **Discussion/Limitations** — what the results mean, what they don't mean
6. **Abstract** — last, because it summarizes everything else
7. **Conclusion** — tightest summary of contribution and implications

**Why methods-first?** It forces precision. If you can't write the methods clearly,
the experiment may not be well-defined enough.

### Step 3: Methods Section Essentials

The methods section is the paper's reproducibility interface. Include:

```
METHODS CHECKLIST
[ ] Task/problem definition with formal notation
[ ] Dataset(s): source, version, splits, preprocessing, license
[ ] Model/method: architecture, key design choices, pseudocode if novel
[ ] Training: hyperparameters (tuned and fixed), optimizer, schedule, seeds
[ ] Evaluation: primary metric definition, secondary metrics, averaging
[ ] Baselines: what they are, how they were run (same conditions? re-implemented?)
[ ] Compute: hardware, runtime, any platform-specific details
[ ] Statistical analysis: tests used, CI method, multiple comparison handling
```

### Step 4: Results Section Essentials

Present results transparently:

- **Primary result table**: all conditions, all seeds, with uncertainty
- **Ablation table**: component contributions isolated
- **Error analysis**: slices, behavioral tests, qualitative examples
- **Negative results**: things that did NOT work (and why)
- **Figures**: learning curves, calibration plots, distribution comparisons

**Presentation principles:**
- Show distributions, not just means (violin/box plots when possible)
- Use consistent notation and formatting across all tables
- Include absolute numbers alongside percentages
- Never round in a way that hides meaningful differences

### Step 5: Limitations Section

Write an honest limitations section. This is not a weakness — it is a strength of
rigorous work. Cover:

```
LIMITATIONS TEMPLATE
- Scope limitations: [what populations/domains/conditions were NOT tested]
- Data limitations: [size, quality, representativeness, label noise]
- Method limitations: [assumptions, failure modes, computational cost]
- Evaluation limitations: [metric limitations, missing comparisons]
- Generalizability: [would this result hold in deployment? at different scales?]
- What we would do differently: [with more time/compute/data]
```

### Step 6: Prepare Artifacts for Release

**Code release:**
- Clean the repository: remove dead code, add comments where non-obvious
- Create a `README.md` with reproduction instructions (use template from SKILL.md)
- Tag the exact commit that produces the paper's results
- Pin environment (conda env export / pip freeze / Docker)

**Data release** (if applicable):
- Provide Datasheet/Data Statement documentation
- Use FAIR principles: findable (DOI), accessible (open repo), interoperable
  (standard format), reusable (license + documentation)
- If data cannot be released: document why and provide access instructions

**Model release** (if applicable):
- Provide Model Card documentation
- Include: intended use, out-of-scope use, evaluation across conditions, limitations
- Consider licensing: what are users allowed to do with the model?

**Experiment artifacts:**
- Map from paper tables/figures to tracked run IDs
- Export configs used for all reported experiments
- Archive logs and metrics (not just final numbers)

### Step 7: Pre-Submission Checklist

Run through the reproducibility checklist:
[templates/reproducibility-checklist.md](../templates/reproducibility-checklist.md)

Additionally:
```
PRE-SUBMISSION CHECKS
[ ] All claims match the evidence (no overclaiming)
[ ] Confirmatory vs exploratory clearly labeled
[ ] All baselines reported fairly (same conditions, same tuning budget)
[ ] Negative results included (not hidden)
[ ] Code runs end-to-end from a clean environment
[ ] Paper compiles without errors
[ ] References are complete and correctly formatted
[ ] Acknowledgments and funding sources listed
[ ] Ethics statement included (if venue requires it)
[ ] Author contributions documented (CRediT taxonomy)
```

### Step 8: Dissemination Strategy

**Preprint:**
- Post to arXiv (or relevant preprint server) for rapid visibility
- Note: preprints are not peer-reviewed — frame accordingly

**Archival submission:**
- Choose target venue based on scope, audience, and timeline
- Adapt formatting to venue requirements
- Address reproducibility requirements specific to the venue

**Archival repository:**
- Archive code + data + artifacts to Zenodo (or similar) for DOI and long-term access
- Connect GitHub releases to Zenodo for automatic archiving

**Software citation:**
- Add CITATION.cff to the repository
- Include DOI from Zenodo or other archive

### Artifact Locations

When using the exploration structure:
- Paper draft → `explorations/NNN-slug/draft.md`
- Release-ready code → `explorations/NNN-slug/src/` (cleaned, tagged)
- Figures → `explorations/NNN-slug/figures/` (if many; or inline in draft.md)

### Step 9: Post-Publication Maintenance

- Monitor for questions, issues, and replication attempts
- Fix bugs in released code (tag patches separately from paper version)
- Update Model Cards or Datasheets if new issues are discovered
- Respond to criticism constructively — this is science working correctly

## Exit Criteria

- [ ] Paper structured with all required sections
- [ ] Methods section passes the methods checklist
- [ ] Results section includes primary, ablation, and error analysis
- [ ] Limitations section is honest and comprehensive
- [ ] Code/data/model artifacts prepared for release
- [ ] Reproducibility checklist passes
- [ ] Pre-submission checklist complete
- [ ] Dissemination plan documented
- [ ] LOGBOX final entry recorded

## Transition

**Backward → Analysis**: if writing reveals missing ablations, insufficient evidence, or
errors in the analysis, return to fill gaps.

**Backward → Experiment Design**: if scope changes require new experiments (e.g., reviewer
requests additional baselines), return to design them properly before running.

**Backward → Lit Review**: if a reviewer identifies missed related work that changes
positioning, return to update the evidence map.
