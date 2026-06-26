# Phase: Literature Review

## Goal

Build a comprehensive, auditable evidence map that validates the novelty gap, identifies
baselines and methods, and surfaces risks — using a documented, reproducible search process.

## Entry Conditions

- A research statement exists (from Brainstorming or a user-provided question)
- Primary metric, dataset, and baseline are tentatively identified

## Step-by-Step Protocol

### Step 1: Define the Review Protocol

Before searching, write down:

```
REVIEW PROTOCOL
- Research question(s): [from brainstorming output]
- Inclusion criteria: [topic, methodology, data regime, outcome type, date range]
- Exclusion criteria: [irrelevant domains, non-peer-reviewed if applicable, languages]
- Databases to search: [see database list below]
- Search string structure: [Boolean terms with AND/OR/NOT]
- Screening process: [title/abstract first, then full-text]
- Expected timeline: [dates]
```

**Database selection** (use at least 3 for comprehensive coverage):
- **arXiv** — preprints (CS, physics, math, quantitative biology)
- **Semantic Scholar** — AI-powered search with citation graphs
- **Google Scholar** — broadest coverage, includes grey literature
- **PubMed** — biomedical and life sciences
- **IEEE Xplore / ACM DL** — engineering and computing
- **Scopus / Web of Science** — multidisciplinary indexed literature
- **DBLP** — computer science bibliography

### Step 2: Execute Search

For each database:
1. Run the search string
2. Record: database name, exact query, date, number of results
3. Export results to a common format (BibTeX, CSV, or reference manager)

**Search string design tips:**
- Start broad, then narrow with filters
- Use synonyms and related terms (e.g., "large language model" OR "LLM" OR "foundation model")
- Combine concept blocks with AND: (method terms) AND (task terms) AND (evaluation terms)
- Test the string: does it retrieve known relevant papers? If not, revise.

**Complementary strategies** (beyond database search):
- **Citation chasing**: forward/backward citations from key papers
- **Author tracking**: prolific authors in the area
- **Conference proceedings**: targeted venues (NeurIPS, ICML, ACL, EMNLP, ICLR, etc.)
- **Twitter/social media**: recent work not yet indexed

### Step 3: Screen and Select

**Title/abstract screening** (first pass):
- Skim each result: is it plausibly relevant based on title and abstract?
- Decision: INCLUDE / EXCLUDE / MAYBE
- Record reason for every exclusion (even brief: "wrong task", "survey only", etc.)

**Full-text screening** (second pass):
- Read included + maybe papers more carefully
- Apply inclusion/exclusion criteria strictly
- Final decision: IN / OUT with reason

**Track in a single source of truth** (spreadsheet or tool):
```
| # | Paper title | Authors | Year | Database | Screen 1 | Screen 2 | Decision | Reason |
```

### Step 4: PRISMA-Style Audit Trail

Document the flow of papers through screening:

```
Records identified through database searching: N1
Additional records from citation chasing: N2
─── Duplicates removed: N3
Records screened (title/abstract): N4
─── Excluded at screening: N5
Full-text articles assessed: N6
─── Excluded at full-text (with reasons): N7
Studies included in synthesis: N8
```

You do not need a formal PRISMA diagram for every project, but you DO need these numbers
and the exclusion reasons to be recoverable.

### Step 5: Read and Extract (Three-Pass Method)

For each included paper, use a structured reading approach:

**Pass 1 — Gist (5-10 min):**
- Read title, abstract, introduction, section headings, conclusion
- Determine: what is claimed, what method, what data, what result
- Decide if deeper reading is needed

**Pass 2 — Understanding (30-60 min):**
- Read fully, annotate key claims and methods
- Identify strengths and weaknesses
- Note how it relates to YOUR research question

**Pass 3 — Verification (for critical papers only):**
- Check math/proofs, re-derive key results if feasible
- Look at data details, code availability, reproducibility claims
- Assess whether results would replicate

**Extraction schema** (fill for each paper):

```
PAPER EXTRACTION
- Citation: [authors, year, title, venue]
- Claim: [one-sentence summary of main contribution]
- Method: [approach in 2-3 sentences]
- Data: [datasets used, sizes, splits]
- Evaluation: [metrics, baselines compared against]
- Key result: [headline number or finding]
- Limitations: [stated + unstated]
- Relevance to our work: [how it connects: baseline? comparison? building block?]
- Artifacts available: [code? data? models? configs?]
```

### Step 6: Synthesize into Evidence Map

Cluster papers by **claims and mechanisms**, not by venue or chronology:

```
EVIDENCE MAP
Theme 1: [e.g., "Scaling laws for X"]
  - Paper A claims... with evidence...
  - Paper B claims... with contradicting evidence...
  - Gap: [what is not addressed]

Theme 2: [e.g., "Evaluation methods for Y"]
  - Paper C proposes metric M1...
  - Paper D shows M1 is flawed because...
  - Gap: [what metric is needed]

Cross-cutting concerns:
  - Reproducibility: [which results have been replicated?]
  - Baselines: [what is the current strongest baseline?]
  - Datasets: [standard benchmarks, limitations, emerging alternatives]
```

### Artifact Locations

When using the exploration structure, save outputs to the active exploration:
- Search protocol, screening log, PRISMA numbers, extractions, evidence map →
  `explorations/NNN-slug/lit-review.md` (single consolidated file)
- If the evidence map is **reusable across explorations** (e.g., covers a broad topic),
  also save it to `shared/literature/` so future explorations can reference it
- Shared bibliography → `shared/literature/references.bib`

### Step 7: Validate Novelty Gap

Ask explicitly:
- Does our research question still have a novel answer to contribute?
- Has someone already done what we planned? If so, how do we differentiate?
- Are our planned baselines still the right ones given what we found?

**If the novelty gap is closed**: log this in LOGBOX and transition BACK to Brainstorming
with the evidence. This is not a failure — it is the system working correctly.

## Exit Criteria

- [ ] Search protocol is documented (databases, queries, dates, filters)
- [ ] Screening is tracked with inclusion/exclusion reasons
- [ ] PRISMA-style numbers are recorded
- [ ] Extraction schema filled for all included papers
- [ ] Evidence map synthesized with themes, gaps, and baseline identification
- [ ] Novelty gap validated (or backtrack triggered)
- [ ] LOGBOX entry recorded

## Transition

**Forward → Experiment Design**: carry the evidence map, baseline set, dataset candidates,
and validated research statement.

**Backward → Brainstorm**: if novelty gap is false, archive the exploration and carry the
evidence that invalidates the original idea. Promote reusable artifacts (evidence map,
bibliography) to `shared/literature/` before archiving.

**Backward ← Experiment Design**: if design reveals missing baselines or datasets, return
here to find them.

**Backward ← Analysis**: if new related work is discovered during analysis that changes
assumptions, return here to update the evidence map.
