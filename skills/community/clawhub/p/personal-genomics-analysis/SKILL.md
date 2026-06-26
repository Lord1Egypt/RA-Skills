---
name: personal-genomics
description: >
  Analyze consumer DNA data from WeGene, 23andMe, AncestryDNA, VCF, BAM, or CRAM files.
  Generate evidence-based reports covering health risks, pharmacogenomics, ancestry,
  nutrition, exercise traits, and supplement guidance. Runs locally and keeps raw genetic
  data on the user's machine.
---

# Personal Genomics Analysis Skill

## Overview

This skill guides you through a structured, multi-phase workflow for analyzing consumer
genetic testing data and producing actionable health insights. The workflow is interactive —
you gather information from the user at key decision points rather than making assumptions.

The analysis pipeline is designed to be:
- **Evidence-based**: every risk assessment cites published research (PMIDs)
- **Interactive**: the user's medical history, lifestyle, and concerns shape the analysis
- **Progressive**: start broad, then deep-dive into areas that matter most to the user
- **Actionable**: end with concrete recommendations (supplements, lifestyle, screening schedule)

## Phase 1: Data Intake & Format Detection

### Supported Input Formats

Read `references/supported_formats.md` for detailed format specifications. In brief:

| Platform | File Type | Key Characteristics |
|----------|-----------|-------------------|
| WeGene | TSV (.txt) | `rsid \t chromosome \t position \t genotype` |
| 23andMe | TSV (.txt) | `# rsid \t chromosome \t position \t genotype` (comment header with `#`) |
| AncestryDNA | TSV (.txt) | `rsid \t chromosome \t position \t allele1 \t allele2` (separate allele columns) |
| VCF | .vcf / .vcf.gz | Standard VCF v4.x, may contain WGS or chip data |
| CRAM/BAM | .cram / .bam | Alignment files for variant verification, depth analysis |

### What to Do

1. **List the user's uploaded files** and identify their formats by reading the first 20-50 lines
2. **Report back** what you found: platform, number of variants, reference genome build (GRCh37/GRCh38 if detectable), data quality indicators
3. **Ask the user** what they'd like to focus on. Present the available analysis modules:
   - Health risk assessment (disease predisposition)
   - Pharmacogenomics (drug metabolism & response)
   - Nutrition & metabolism genetics
   - Exercise & fitness genetics
   - Ancestry (mtDNA/Y haplogroups if WGS data available)
   - All of the above (recommended for first-time analysis)

### Parsing Strategy

Write a Python script that:
- Auto-detects the input format from file headers
- Builds a unified genotype dictionary: `{rsid: genotype_string}`
- For VCF files, also indexes by `chr:pos` for position-based lookups
- Handles both compressed (.gz) and uncompressed files
- Reports parsing statistics (total variants, by chromosome, etc.)

When both chip data (WeGene/23andMe) and WGS (VCF) are available, use a **dual-source
lookup** strategy: check chip data first (faster), fall back to VCF by rsid or chr:pos.
This maximizes coverage since chip and WGS may cover different variant sets.

## Phase 2: Initial Comprehensive Analysis

### SNP Database

Read `references/snp_database.md` for the curated SNP database organized by category.
The database covers ~120 clinically relevant SNPs across these categories:

- **Health risks**: cancer (BRCA1/2), cardiovascular (9p21.3, MTHFR), metabolic (TCF7L2),
  neurological (APOE, LRRK2), autoimmune, and more
- **Pharmacogenomics**: CYP2C19, CYP2D6, CYP2C9, CYP1A2, SLCO1B1, VKORC1, ALDH2, etc.
- **Nutrition**: lactose tolerance (MCM6), vitamin metabolism (MTHFR, VDR, BCMO1, FUT2),
  caffeine sensitivity (CYP1A2), alcohol flush (ALDH2)
- **Exercise**: muscle fiber type (ACTN3), endurance (PPARGC1A), recovery (IL6), VO2max (ACE)

Each SNP entry includes: gene, variant name, risk allele, condition/trait, evidence level,
PMID reference, and a plain-language explanation.

### Analysis Script Structure

Generate a Python analysis script that:

1. Loads the unified genotype dictionary from Phase 1
2. Looks up each SNP in the database
3. Determines risk level based on genotype (homozygous risk, heterozygous, or normal)
4. Handles special cases:
   - **APOE typing**: requires combining rs429358 + rs7412 to determine ε2/ε3/ε4 status
   - **CYP2C19 metabolizer status**: combines multiple star-allele SNPs
   - **MTHFR compound**: checks both C677T (rs1801133) and A1298C (rs1801131)
5. Generates an HTML report with:
   - Summary dashboard (key findings, risk counts by category)
   - Tabbed sections for each category
   - Color-coded risk levels (high/medium/low/protective)
   - Citations for each finding

### Report Output

Generate an interactive HTML report with:
- Clean, readable design with high contrast (dark text on light backgrounds)
- Sticky navigation tabs
- Risk indicators with clear color coding
- Expandable detail sections for each SNP
- A summary section with the most clinically significant findings

Follow the user's language (Chinese or English) for all report text.

## Phase 3: User Interview & Deep Dive

This is the critical interactive phase. After presenting initial results:

### Gather Context

Ask the user about:
1. **Known health conditions** — what diagnoses do they already have?
2. **Family history** — especially first-degree relatives with serious conditions
3. **Current medications** — for drug interaction awareness
4. **Lifestyle factors** — diet, exercise, sun exposure, smoking/alcohol
5. **Specific concerns** — what worries them most?

This information is essential because genetic risk is only part of the picture. A person
with a family history of early heart attack AND multiple CAD risk SNPs faces very different
odds than someone with the same SNPs but no family history.

### Deep Risk Analysis

Based on the user's health profile, conduct a targeted deep-dive. Read
`references/deep_risk_snps.md` for extended SNP panels organized by disease pathway:

- **Lipid metabolism** (~20 SNPs): LDLR, APOB, PCSK9, HMGCR, CETP, LPL, APOA5, etc.
- **Coronary artery disease** (~15 SNPs): 9p21.3, LPA, MTHFR, CRP, IL6, F5, F2, etc.
- **Uric acid / gout** (~10 SNPs): SLC2A9, ABCG2, SLC22A12, SLC17A1, etc.
- **Diabetes risk** (~10 SNPs): TCF7L2, KCNJ11, SLC30A8, PPARG, FTO, etc.
- **Statin pharmacogenomics** (~5 SNPs): SLCO1B1, CYP3A4, ABCB1, etc.

For each category relevant to the user:
1. Query ALL SNPs in the extended panel (use both chip + VCF dual-source)
2. Tally risk alleles and categorize (high/moderate/low/protective)
3. Compute a qualitative risk profile (not a numeric "score" — explain why)
4. Cross-reference with the user's actual health status and family history
5. Note any SNPs that could NOT be found (missing data)

### Variant Verification (if CRAM/BAM available)

If the user has provided alignment files:
- Use samtools/bcftools to verify key high-risk variants directly from reads
- Report read depth and allele balance for critical SNPs
- Flag any low-confidence calls

Note: samtools may need to be compiled from source in sandboxed environments.
See `references/tool_setup.md` for instructions.

### Ancestry Analysis (if WGS available)

For whole-genome sequencing data:
- **mtDNA haplogroup**: Check diagnostic variants against PhyloTree. Important: VCF
  files report variants against rCRS (which is haplogroup H). Absence of a variant
  means the person carries the rCRS allele at that position. Look for the 9bp deletion
  at position 8270-8278 (B haplogroup marker, common in East Asian populations).
- **Y chromosome haplogroup** (if male): Check ISOGG diagnostic SNPs (e.g., M122 for
  O2 haplogroup, common in East Asian populations).

## Phase 4: Personalized Recommendations

Based on all gathered information, produce actionable recommendations.

### Supplement Plan

Read `references/supplement_guide.md` for evidence-based supplement recommendations
mapped to genetic findings. The guide covers:

- Which genetic variants warrant which supplements
- Dosage ranges with citations
- Drug-supplement interactions to watch for
- Priority tiers (core / recommended / optional)
- Age-specific timing and duration advice
- When to recheck labs

Always organize supplements into tiers:
1. **Core**: strongly supported by genetics + current health status
2. **Recommended**: good evidence, beneficial given risk profile
3. **Optional**: supporting evidence, lower priority

### Screening & Monitoring Schedule

Based on the risk profile, suggest:
- Which lab tests to monitor and how often
- Age milestones for specific screenings (e.g., coronary CTA at 30 if strong family history)
- Target values for key metrics

### Output Formats

Offer to generate:
- **HTML report** — comprehensive, interactive, printable
- **Excel spreadsheet** — dosing schedule table for daily reference
- **Summary document** — one-page overview for sharing with a physician

## Important Principles

### Medical Disclaimer
Every report MUST include a clear disclaimer: genetic analysis provides risk estimates,
not diagnoses. Results should be discussed with a qualified healthcare provider. Consumer
genetic testing has limitations in coverage and accuracy compared to clinical-grade testing.

### Evidence Standards
- Always cite PMIDs for risk associations
- Distinguish between GWAS-level evidence and functional/clinical evidence
- Note when evidence is primarily from non-Asian populations (if the user appears to be
  of East Asian descent based on their data or stated ethnicity)
- Use language like "increased risk" rather than "you will get"

### Language
Follow the user's language. If the user writes in Chinese, produce reports in Chinese.
If in English, use English. For SNP names and gene symbols, always keep the standard
scientific nomenclature regardless of language.

### Iterative Approach
Don't try to do everything at once. The workflow is designed as a conversation:
1. Parse → show what you found → ask what to focus on
2. Initial analysis → present results → gather health context
3. Deep dive → present findings → discuss implications
4. Recommendations → deliver in requested format

Each phase should end with a clear handoff to the user before proceeding.
