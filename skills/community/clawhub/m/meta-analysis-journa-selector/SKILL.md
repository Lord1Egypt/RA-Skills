---
name: meta-analysis-journal-selector
description: >
  SCI journal selection assistant for meta-analysis and systematic review papers. Use this skill when the user has completed or is completing a meta-analysis and needs journal recommendations, wants a tiered submission strategy (Reach/Target/Safety), asks which SCI journals accept meta-analyses, or needs to compare journals by impact factor, acceptance rate, review speed, and scope match. Trigger phrases include: "which journal for my meta-analysis", "help me select a journal", "meta-analysis journal recommendation", "where to submit meta-analysis", "SCI journal selection for systematic review", "find journals that accept meta-analyses", "我的meta分析投什么期刊", "帮我选刊", "meta分析SCI投稿", "meta选刊建议".
agent_created: true
---

# Meta-Analysis SCI Journal Selector

## Overview

This skill provides systematic, data-driven SCI journal selection for meta-analysis and systematic review papers. It evaluates the user's manuscript against a curated database of 316 meta-analysis-friendly journals across 30 medical specialties, cross-references with verified 2025 JCR and CAS quartile data, applies a context-aware weighted scoring algorithm, assesses desk-rejection risk, and delivers a tiered submission strategy with a pre-submission checklist and post-rejection decision framework.

## Pain Points Addressed

This skill is designed to solve the real-world frustrations researchers face that existing tools (JANE, Elsevier Journal Finder, Scopus, LetPub) do not address:

1. **No existing tool is MA-specific** — JANE and publisher tools match by text similarity but do not know which journals actually accept meta-analyses vs. which desk-reject them.
2. **CAS vs JCR confusion** — Chinese researchers need CAS quartile for domestic evaluation (graduation, promotion, funding) but JCR quartile for international recognition. No tool provides both side-by-side with context-aware guidance.
3. **Desk rejection is the #1 waste of time** — Most rejections happen at editor screening due to scope mismatch, not quality. This skill explicitly assesses desk-rejection risk for each recommendation.
4. **Hidden costs and timelines** — APC, review time, and total pipeline time are scattered across different sources. This skill consolidates them and estimates the full submission-to-publication timeline.
5. **No post-rejection strategy** — Existing tools give recommendations but no guidance on what to do when rejected. This skill includes a decision framework.
6. **PROSPERO and PRISMA compliance as hidden gatekeepers** — Many top journals silently reject MAs lacking PROSPERO registration or PRISMA compliance. This skill checks these as mandatory pre-conditions.

## Core Design Principles

1. **Use verified JCR data.** The `references/jcr_verified_data.csv` file contains exact IF, JCR quartile, and CAS quartile for all 316 journals, sourced from ShowJCR/hitfyd GitHub repository (2025 JCR, released June 2026). Always cross-reference with this CSV for numeric metrics.
2. **CAS quartile matters as much as JCR.** For Chinese researchers, CAS quartile often matters MORE than JCR quartile. Always present both and explain which to prioritize based on the user's goals.
3. **Calibrate against real publications.** Before recommending a journal, verify that it has published similar meta-analyses in the past 3 years. This is the single most reliable predictor of acceptance.
4. **Assess desk-rejection risk explicitly.** For each recommended journal, state the desk-rejection risk level (Low/Moderate/High) with reasoning.
5. **Default to the three-tier strategy** with explicit submission sequencing and post-rejection decision tree.
6. **Adapt to user context.** Scoring weights, tier constraints, and advice adapt based on the user's career stage, funding situation, and institutional requirements.

## Workflow

Execute the following steps in order. Do not skip steps.

### Step 1: Collect Paper Profile and User Context

Gather these data points. If information is missing, ask follow-up questions — no more than 3 questions at a time.

**Required — Paper:**
1. **Research topic** — Specific clinical question (e.g., "efficacy of CAR-T therapy in relapsed/refractory B-ALL")
2. **Primary discipline** — Main specialty (e.g., oncology, cardiology, psychiatry)

**Required — User context (NEW — critical for personalization):**
3. **Primary goal** — Domestic evaluation (graduation/promotion/funding in China) / International recognition (overas study, collaboration) / Both
4. **Institutional requirement** — Minimum CAS quartile or JCR quartile required by their institution (e.g., "must be CAS Q2 or above for PhD graduation")
5. **PROSPERO registration status** — Registered / Not registered / Not sure what this is

**Important — Paper details (can be inferred from description):**
6. **Meta-analysis type** — Intervention / Diagnostic accuracy / Network MA / Dose-response / Prevalence / Prognostic / Genetic association / Umbrella review
7. **Number of included studies** — Approximate count
8. **Study design of included studies** — RCTs only / Observational / Mixed
9. **Key findings** — Primary effect estimate and statistical significance
10. **Novelty** — First MA on this topic? Methodological innovation? Clinical impact?

**Important — User constraints:**
11. **Time constraints** — Hard deadline? (graduation, promotion, grant submission)
12. **Budget** — APC limit? Institutional OA agreements? Self-funded?
13. **Language preference for report** — Chinese / English / Both

**Questioning strategy:**
- If the user provides a detailed description, infer items 6-10 from context
- Always ask items 3-5 if not provided — these determine the entire recommendation strategy
- Phrase conversationally: "Your institution requires CAS Q2 minimum — got it. And have you registered the protocol on PROSPERO?"

### Step 2: Pre-Submission Compliance Gate (NEW)

Before proceeding to journal selection, verify mandatory pre-conditions. If any fail, flag immediately — these are non-negotiable for most journals.

**Gate 1: PROSPERO Registration**
- If not registered: Strongly recommend registration before submission. Many top journals (BMJ, Cochrane, JAMA series, most Q1 journals) require or strongly prefer PROSPERO registration. Lack of registration is a common desk-rejection trigger.
- Exception: If the user is submitting to a lower-tier journal (CAS Q3-Q4, IF <3), PROSPERO may not be required but is still recommended.
- Action: If not registered, provide PROSPERO registration URL (https://www.crd.york.ac.uk/prospero/) and note that it takes 1-2 weeks for review.

**Gate 2: PRISMA 2020 Compliance**
- Ask: "Have you completed the PRISMA 2020 checklist?"
- If no: Provide the checklist URL and note that most journals require it as a supplementary file.

**Gate 3: Risk of Bias Assessment**
- Verify that a standard tool was used (RoB 2 for RCTs, ROBINS-I for non-randomized, NOS for observational, QUADAS-2 for diagnostic).
- If missing: Flag as critical — most MA-accepting journals require this.

**Communication:** Present gate results as a checklist:
```
Pre-Submission Compliance Check:
[x] PROSPERO registered (CRDXXXXXXXX) — Pass
[!] PRISMA 2020 checklist not completed — Action needed
[x] Risk of bias assessment (RoB 2) — Pass
```

Only proceed to journal selection after the user acknowledges the gate results.

### Step 3: Grade Manuscript Competitiveness

Classify into A/B/C based on scope, methodology, and novelty:

**Grade A — High Competitiveness**
- Included >30 studies (or >15 for RCT-MA)
- PROSPERO registered, PRISMA 2020 compliant, comprehensive risk-of-bias, robust sensitivity/subgroup analyses
- First or largest MA on a clinically impactful question
- GRADE assessment completed

**Grade B — Moderate Competitiveness**
- Included 10-30 studies
- Methodologically sound but without notable innovation
- Clinically useful but not practice-changing
- Update MA with meaningful new data

**Grade C — Modest Competitiveness**
- Fewer than 10 studies
- Methodologically adequate but limited scope
- Confirmatory or narrow topic

State the grade and rationale concisely.

### Step 4: Load Verified Journal Data and Calibrate

**Step 4a — Load data sources:**
1. Read `references/jcr_verified_data.csv` — authoritative IF, JCR Q, CAS Q, CAS Top for all 316 journals
2. Read `references/journal_database.md` — acceptance rates, review times, APC, MA friendliness (★/☆), scope notes

**Step 4b — Match by discipline:**
Start with the user's primary discipline section. For cross-disciplinary topics, pull from all relevant sections.

**Step 4c — Calibrate against real publications (MANDATORY for Reach tier):**
For each Reach-tier candidate, verify that the journal has published similar MAs:
```
PubMed search: "Journal Name"[Journal] AND (meta-analysis[Publication Type]) AND "user's topic keyword"
```
If zero results in the past 3 years, demote from Reach to Target and note "No similar MA published in this journal recently — elevated desk-rejection risk."

For Target and Safety tiers, calibration is recommended but not mandatory.

**Step 4d — Expand via PubMed if database is insufficient:**
```
("[disease/condition keywords]") AND (meta-analysis[Publication Type] OR "systematic review"[Publication Type])
```
Scan the first 50 results to identify which journals publish this type of MA.

### Step 5: Score with Context-Aware Weights (REvised)

**Step 5a — Determine adaptive weight profile based on user context:**

| Factor | Default | Domestic-focused | International | Time-pressed | Budget-constrained |
|--------|---------|-----------------|---------------|-------------|-------------------|
| Scope Match | 25% | 25% | 25% | 20% | 25% |
| MA History | 20% | 20% | 20% | 15% | 20% |
| IF + Quartile | 25% | 25% | 25% | 20% | 15% |
| Review Speed | 15% | 10% | 10% | **30%** | 15% |
| Cost (APC) | 15% | 20% | 20% | 15% | **25%** |

Select the profile that best matches the user's stated context. If the user has multiple constraints (e.g., time-pressed AND budget-constrained), blend the profiles by averaging the weights.

**Step 5b — Score each candidate (1-5 scale):**

| Factor | 5 | 4 | 3 | 2 | 1 |
|--------|---|---|---|---|---|
| Scope Match | Core scope | Strong overlap | Partial | Marginal | Peripheral |
| MA History | >10 MAs/yr | 5-10/yr | 2-5/yr | 1-2/yr | Rarely |
| IF + Quartile | IF in reach, CAS Q1 | IF in reach, CAS Q2 | IF competitive, CAS Q2-Q3 | IF stretch, CAS Q3 | IF long shot, CAS Q4 |
| Review Speed | <4 wks | 4-6 wks | 6-8 wks | 8-12 wks | >12 wks |
| Cost (APC) | No APC | <2,000 | 2,000-3,000 | 3,000-4,000 | >4,000 |

**Note on IF + Quartile scoring:** The score depends on BOTH the journal's metrics AND the user's institutional requirements. If the user needs CAS Q2 minimum, a CAS Q3 journal scores 1-2 regardless of IF. If the user needs JCR Q1 for international applications, a JCR Q2 journal scores 2-3.

**Step 5c — Apply tier constraints (IF reality check):**

| Paper Grade | Safety IF Floor | Target IF Floor | Reach IF Floor |
|-------------|-----------------|-----------------|----------------|
| A (High) | IF >= 3 | IF >= 8 | IF >= 15 |
| B (Medium) | IF >= 1 | IF >= 3 | IF >= 7 |
| C (Modest) | IF >= 0.5 | IF >= 1 | IF >= 3 |

**Additional CAS constraint (NEW):** If the user stated a minimum CAS quartile requirement:
- Exclude any journal below that threshold entirely
- Do not recommend as Safety — a journal that doesn't meet institutional requirements is not a "safety" option

Rules:
- Final tier = minimum of (score-based tier, IF-constraint tier)
- A journal below the user's CAS minimum → excluded entirely
- Ensure at least 2 different publishers represented

### Step 6: Desk-Rejection Risk Assessment (NEW)

For each recommended journal, assess desk-rejection risk:

**Low Risk (Green):**
- Journal has published 3+ similar MAs in the past 3 years
- Paper topic is clearly within journal scope
- PROSPERO registered, PRISMA compliant
- Paper grade matches or exceeds the journal's typical MA grade

**Moderate Risk (Yellow):**
- Journal has published 1-2 similar MAs, or topic is adjacent to core scope
- Paper is at the lower end of the journal's typical quality range
- Some scope ambiguity (e.g., cross-disciplinary topic)

**High Risk (Red):**
- No similar MA found in this journal in the past 3 years
- Topic is peripheral to journal scope
- Paper grade is below the journal's typical MA grade (e.g., Grade C paper targeting a Grade A journal)
- Missing PROSPERO registration for a journal that requires it

Include the risk level in the report with a one-line explanation.

### Step 7: Anti-Predatory Verification

Screen all candidates against the checklist in `references/journal_database.md`. If any candidate fails, remove and substitute.

### Step 8: Deliver Structured Report

Output the report using this format. Adapt language to user's stated language preference.

```
# Meta-Analysis Journal Selection Report

## Paper Summary
- **Topic**: [one-line description]
- **Discipline**: [primary] / [secondary]
- **MA Type**: [intervention/NMA/prevalence/etc.]
- **Studies Included**: [N] ([RCT/observational/mixed])
- **Competitiveness Grade**: [A/B/C] — [one-line rationale]

## Your Context
- **Primary goal**: [Domestic evaluation / International / Both]
- **Institutional requirement**: [e.g., CAS Q2 minimum for graduation]
- **PROSPERO**: [Registered CRDXXXXXXXX / Pending / Not registered]
- **Time constraint**: [e.g., Must publish before June 2027]
- **Budget**: [e.g., APC limit 3,000 USD]
- **Quartile guidance**: [Personalized note: "Since your goal is domestic promotion, prioritize CAS quartile. For the journals below, CAS Q is the primary ranking metric."]

## Pre-Submission Compliance Status
[x] PROSPERO registration — [status]
[!] PRISMA 2020 checklist — [status]
[x] Risk of bias assessment — [status]
→ [Action items if any gate failed]

## Submission Strategy

### Reach Tier (1-2 journals)
| Rank | Journal | IF | JCR Q | CAS Q | Top | Desk-Reject Risk | Review | APC | Key Reason |
|------|---------|-----|-------|-------|-----|-----------------|--------|-----|------------|
| 1 | ... | ... | ... | ... | ... | Low/Moderate/High | ... | ... | ... |

### Target Tier (2-3 journals)
| Rank | Journal | IF | JCR Q | CAS Q | Top | Desk-Reject Risk | Review | APC | Key Reason |
|------|---------|-----|-------|-------|-----|-----------------|--------|-----|------------|
| ... |

### Safety Tier (1-2 journals)
| Rank | Journal | IF | JCR Q | CAS Q | Top | Desk-Reject Risk | Review | APC | Key Reason |
|------|---------|-----|-------|-------|-----|-----------------|--------|-----|------------|
| ... |

## Timeline Estimate
- **Reach tier**: First decision in [X-Y] weeks → if accepted, publication in [X-Y] months total
- **Target tier**: First decision in [X-Y] weeks → if accepted, publication in [X-Y] months total
- **Safety tier**: First decision in [X-Y] weeks → if accepted, publication in [X-Y] months total
- **Worst-case full sequence** (Reach → Target → Safety): [X-Y] months if all reject, [X-Y] months if Target accepts

## Cost Analysis
- **If Reach accepts (first try)**: [APC amount] + [any additional fees]
- **If Target accepts (after 1 rejection)**: [APC amount] + [any additional fees]
- **If Safety accepts (after 2 rejections)**: [APC amount] + [any additional fees]
- **Note on waivers**: [Any applicable waiver policies]

## Submission Sequence and Post-Rejection Decision Tree

### Sequence:
1. Submit to [Reach #1]
2. If desk-rejected → immediately submit to [Target #1] (no revision needed)
3. If reviewed but rejected → revise based on feedback, submit to [Target #2]
4. If Target tier exhausted → submit to [Safety #1]

### If Desk-Rejected (editor rejection without review):
- **Do NOT appeal** unless the rejection was factually incorrect (e.g., editor mistakenly said topic is out of scope when similar MAs exist)
- **Do NOT reformat and resubmit to the same journal** — editorial systems track history
- **Action**: Immediately submit to the next journal in sequence. Desk rejection usually means scope mismatch, not quality. Move on within 1-2 days.

### If Reviewed but Rejected:
- **Read the reviews carefully** — reviewer feedback is free expert consultation
- **Categorize the feedback**: Fixable (language, analysis, presentation) vs. Structural (fundamental design flaw, insufficient novelty)
- **If fixable**: Revise thoroughly (1-2 weeks), then submit to next journal with a fresh cover letter
- **If structural**: Consider whether the paper needs fundamental rework before submitting elsewhere
- **Use reviewer feedback** to strengthen the manuscript even when submitting to a different journal

### If Given Major Revision:
- **Respond point-by-point** to every comment, even those you disagree with
- **Provide a detailed response letter** with line numbers showing changes
- **Do not rush** — a thorough revision takes 2-4 weeks but dramatically improves acceptance odds

## Pre-Submission Checklist for [Target Journal #1]
- [ ] PROSPERO registration number included in methods
- [ ] PRISMA 2020 checklist completed and ready as supplementary file
- [ ] PRISMA flow diagram finalized
- [ ] Cover letter tailored to this journal (see guidance below)
- [ ] Abstract follows journal format ([structured/unstructured], [word limit])
- [ ] Reference format matches journal requirements ([Vancouver/APA/AMA])
- [ ] Word count within limits ([limit])
- [ ] Figures in required format ([TIFF/EPS/PDF, DPI])
- [ ] Supplementary materials prepared
- [ ] All authors approve final version
- [ ] Conflict of interest and funding statements included

## Cover Letter Guidance for [Target Journal #1]
**Key points to include:**
1. **Scope alignment**: "This meta-analysis on [topic] is highly relevant to [Journal Name]'s scope because [specific reason]"
2. **Novelty statement**: "To our knowledge, this is the [first/largest/most comprehensive] meta-analysis to [specific contribution]"
3. **Clinical significance**: "These findings are clinically important because [specific impact]"
4. **Methodology highlight**: "We followed PRISMA 2020 guidelines, registered on PROSPERO (CRDXXXXXXXX), and used [specific quality assessment tool]"
5. **Similar work in journal**: "We note that [Journal Name] recently published [similar MA reference], and our work extends this by [specific difference]"

## Data Freshness Note
IF, JCR quartile, and CAS quartile sourced from 2025 JCR (released June 2026) via ShowJCR/hitfyd GitHub repository. Verified against 22,643 journals.
```

### Step 9: Follow-Up Offer

After delivering the report, offer:
- "Would you like me to draft a cover letter for your top choice?"
- "Would you like me to search PubMed for similar MAs published in these journals to calibrate expectations?"
- "Would you like me to check the specific formatting requirements for [journal name]?"
- "Would you like me to help you prepare the PRISMA checklist?"

## CAS vs JCR Decision Guidance

Include this section in the report when the user's context involves Chinese institutional evaluation:

```
## CAS vs JCR: Which Matters for You?

Your situation: [personalized based on user context]

**CAS quartile** (中科院分区) — Prioritize if:
- You need the paper for domestic graduation, promotion, or funding
- Your institution explicitly requires CAS Q2 or above
- You are being evaluated by a Chinese university or hospital

**JCR quartile** — Prioritize if:
- You plan to apply for overseas positions (postdoc, faculty)
- You seek international collaboration
- Your institution uses JCR quartile (some do, especially newer programs)

**Both matter** — If you have both goals, prioritize journals that are CAS Q1-Q2 AND JCR Q1. The journals recommended above are filtered to meet your stated minimum requirement.

Key fact: Only ~31% of JCR Q1 journals are also CAS Q1. A JCR Q1 journal may be CAS Q2 or even Q3. Always check both.
```

## PubMed Search Templates

### Finding journals that publish similar MAs:
```
("[disease]"[MeSH Terms] OR "disease"[Title/Abstract]) AND (meta-analysis[Publication Type] OR "systematic review"[Publication Type]) AND ("2023"[Date - Publication] : "2026"[Date - Publication])
```

### Checking if a specific journal publishes MAs in the topic:
```
"Journal Name"[Journal] AND (meta-analysis[Publication Type] OR "systematic review"[Publication Type]) AND "topic keyword"
```

### Finding high-impact MAs for benchmarking:
```
("[disease]"[MeSH Terms]) AND (meta-analysis[Publication Type]) AND (jama[Journal] OR lancet[Journal] OR bmj[Journal])
```

## Anti-Predatory Checklist (Quick Reference)

For each candidate journal, confirm ALL:
- [ ] Listed in SCIE (verify at https://mjl.clarivate.com/)
- [ ] Has a legitimate ISSN
- [ ] Editorial board lists real, verifiable researchers
- [ ] Peer review process is clearly described
- [ ] APC is transparently listed
- [ ] Not on Beall's List or Cabells Predatory Reports
- [ ] No aggressive email solicitation

**Never recommend:**
- OMICS, WASET, or known predatory publishers
- Journals with fake impact factors
- Journals promising acceptance within days

## Edge Cases

### Very narrow/niche topics with few published MAs
Broaden to the next-highest discipline level. If a rare pediatric cancer MA has no direct precedent, look at general pediatric oncology journals. Increase desk-rejection risk to Moderate for all tiers.

### Cross-disciplinary MAs
Score journals from each relevant discipline separately. Present both options. Let the user decide based on career goals (e.g., an endocrinologist might prefer Diabetes Care over a cardiology journal for a cardio-metabolic MA).

### Updated MA (not first on the topic)
Grade down one level. The paper must demonstrate clear added value (new trials, different conclusions, better methodology) to compete at the same tier as the original MA. In the cover letter, explicitly state what is new vs. the previous MA.

### Negative/null result MA
Do not penalize. Many journals explicitly value "negative" MAs that resolve clinical uncertainty. BMJ Open, PLOS ONE, BMC-series, and Journal of Clinical Epidemiology are particularly receptive. Note this as a strength in the cover letter: "This meta-analysis resolves clinical uncertainty by demonstrating no significant difference..."

### MA of non-RCT studies
Grade based on study quality (NOS for cohort, ROBINS-I for non-randomized). Observational MAs are harder to place in top-tier journals. Adjust IF expectations downward by approximately one tier. Note in cover letter that RCT evidence is not available, making this MA the best available evidence.

### User has no PROSPERO registration and deadline is imminent
If the user cannot wait 1-2 weeks for PROSPERO, target journals that do not require it (typically CAS Q3-Q4, IF <3). Explicitly warn that this limits options significantly. List which recommended journals require PROSPERO and which do not.

### User's institution requires CAS Q1 but paper is Grade C
Be honest: "Your paper's competitiveness (Grade C) makes CAS Q1 acceptance very unlikely. Consider strengthening the manuscript (add subgroup analyses, update search, improve discussion) before targeting CAS Q1 journals. Alternatively, if you have a hard deadline, CAS Q2 journals in your field are more realistic." Never set unrealistic expectations.

## Data Freshness Protocol

- **Authoritative data**: `references/jcr_verified_data.csv` contains exact IF, JCR quartile, and CAS quartile from the 2025 JCR (released June 2026), sourced from ShowJCR/hitfyd GitHub repository. This is the single source of truth for numeric metrics.
- **Qualitative data**: `references/journal_database.md` provides acceptance rates, review times, APC estimates, and MA friendliness ratings. These are estimates — flag as such.
- Quote exact IF from the CSV in the report, not approximate ranges from the markdown.
- If the user's session is more than 12 months after June 2026, note that JCR data may have updated and suggest verification.
