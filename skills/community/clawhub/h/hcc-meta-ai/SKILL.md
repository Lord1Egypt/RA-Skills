---
name: hcc-meta-ai
description: AI-assisted meta-analysis workflow for hepatocellular carcinoma comparative effectiveness research. Six-element prompt framework covering full pipeline from literature screening to data extraction. Published skill accompanying the validated methodology paper.
metadata:
  version: "1.0.0"
  author: "Shandong University Qilu Hospital"
  domain: "hepatocellular carcinoma meta-analysis"
  models: ["GPT-5.2", "GPT-4o", "DeepSeek V3.1"]
---

# HCC Meta-Analysis AI Skill

## Overview

This skill implements a standardized, AI-assisted meta-analysis workflow for comparing treatment efficacy in hepatocellular carcinoma (HCC). It follows a six-element prompt architecture (Role–Objective–Skills–Constraints–Workflow–Output) validated across two independent clinical questions with three large language models.

The workflow covers the full meta-analysis pipeline:
1. Literature screening (fuzzy → precise → supplementation)
2. Full-text eligibility determination
3. Newcastle–Ottawa Scale (NOS) quality appraisal
4. Structured baseline data extraction
5. Clinical outcome data extraction

**Validation**: Benchmarked against dual-independent manual review across two HCC projects with GPT-5.2, GPT-4o, and DeepSeek V3.1. Best-performing models achieved >95% accuracy at most stages with >80% total time reduction.

## When to Use

- Conducting a meta-analysis comparing two HCC treatments
- Need rapid evidence synthesis for HCC therapeutic comparison
- Want to standardize the AI-assisted review process across projects
- Teaching or replicating the validated AI meta-analysis methodology

## Six-Element Prompt Framework

Every prompt in this workflow follows a standardized six-element structure:

| Element | Purpose | Example |
|---------|---------|---------|
| **Role** | Defines AI's academic persona | "You are a clinical epidemiologist specializing in HCC..." |
| **Objective** | States the specific task goal | "Screen titles for studies comparing treatment A vs B..." |
| **Skills** | Lists required capabilities | "Identify medical terms, apply synonym rules, extract structured data" |
| **Constraints** | Sets methodological boundaries | "Apply NOS scoring rules strictly; mark missing data as NA" |
| **Workflow** | Specifies step-by-step execution | "Read title → check for intervention terms → classify" |
| **Output** | Defines structured output format | "Output as JSON table with fields: PMID, Decision, Reason" |

## Workflow Stages

### Stage 1: Literature Screening

Three sub-stages with escalating cognitive demands:

1. **Fuzzy Screening** — Title-level keyword matching
   - Batch 100 records per query
   - Check for presence of target disease + intervention terms
   - Template: `scripts/01-fuzzy-screening.md`

2. **Precise Screening** — Abstract-level multi-constraint reasoning
   - Evaluate title + abstract against inclusion criteria
   - Requires comparison of two interventions with reported outcomes
   - Template: `scripts/02-precise-screening.md`

3. **Literature Supplementation** — Citation tracing from full texts
   - Upload PDFs of included studies
   - Extract reference lists; flag potentially missed eligible studies
   - Template: `scripts/03-literature-supplement.md`

### Stage 2: Full-Text Eligibility Determination

Full-text comprehension and multi-criteria decision-making:
- Study population (primary HCC confirmed)
- Direct comparison of two target treatments
- ≥1 clinical outcome reported
- Original study design (prospective/retrospective cohort, case-control, RCT)
- Data separable by treatment group
- Sample size ≥10
- Template: `scripts/04-eligibility.md`

### Stage 3: NOS Quality Appraisal

Structured scoring across three domains:
- **Selection** (4 items, max 4 pts): representativeness, non-exposed cohort, exposure ascertainment, outcome absent at baseline
- **Comparability** (1 item, max 2 pts): confounder control
- **Outcome** (3 items, max 3 pts): assessment objectivity, follow-up duration, follow-up completeness
- Template: `scripts/05-nos-scoring.md`

### Stage 4: Baseline Data Extraction

Structured extraction of study characteristics and patient demographics:
- Core fields: author, year, design, treatment groups, sample size, age, sex, tumor characteristics, follow-up, laboratory values
- Topic-specific extensions (see references)
- Template: `scripts/06-baseline-extraction.md`

### Stage 5: Outcome Data Extraction

Structured extraction of clinical endpoints:
- 1–5 year overall survival (OS), recurrence-free survival (RFS)
- Local tumor progression, distant recurrence, technical success
- Complication rates and subtypes
- Template: `scripts/07-outcome-extraction.md`

## Disease-Agnostic Design

The six-element scaffold is independent of specific diseases. To adapt this workflow for a different disease:

1. Replace disease terminology in `references/terminology.json`
2. Swap intervention names in each prompt template
3. Adjust topic-specific extraction fields in baseline/outcome templates
4. Keep the core logical structure intact

For HCC specifically, the pre-configured terminology and extraction fields in `references/` are ready to use.

## Platform

A web-based platform for deploying and sharing this workflow is available at:
http://8.149.142.6/metaexp/

## References

- Full methodology: see accompanying manuscript
- Supplementary prompt details: S1 (Project 1 prompts), S2 (Project 2 prompts)
- Terminology database: `references/terminology.json`
