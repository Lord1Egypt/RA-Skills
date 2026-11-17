---
name: nutrigenomics
description: Generate a personalised nutrition report from your genetic data (23andMe, AncestryDNA, or VCF). Analyses 24 genes (28 SNPs) across 12 nutrient domains affecting nutrient metabolism, absorption, and food sensitivities. All processing is local — your genetic data never leaves your device.
version: 0.3.12
license: MIT
compatibility: Requires Python 3.11+ with pandas, numpy, matplotlib and seaborn; runs fully offline with no network access
metadata:
  openclaw:
    requires:
      bins: [python3]
    emoji: "🧬"
  hermes:
    tags: [genetics, nutrition, nutrigenomics, health, 23andme, ancestrydna, vcf]
    category: health
---

# Nutrigenomics — Personalised Nutrition from Genetic Data

**Skill ID**: `nutrigenomics`
**Version**: 0.3.12
**Status**: Beta
**Author**: David de Lorenzo
**Requires**: Python 3.11+ (standard library only for the analysis; pandas, numpy, matplotlib and seaborn are needed only for figures)

---

## What This Skill Does

The Nutrigenomics generates a **personalised nutrition report** from consumer
genetic data (23andMe, AncestryDNA raw files or VCF). It interrogates a curated
set of nutritionally-relevant SNPs drawn from GWAS Catalog, ClinVar, and
peer-reviewed nutrigenomics literature, then translates genotype calls into
actionable dietary and supplementation guidance — all computed locally.

**Key outputs**
- Markdown nutrition report with risk scores and per-SNP genotype calls
- Radar chart of nutrient risk profile
- Gene × nutrient heatmap
- Reproducibility bundle (`README_reproducibility.txt`, `environment.yml`, `checksums.txt`, `provenance.json`)

---

## Trigger Phrases

The Bio Orchestrator should route to this skill when the user says anything like:

- "personalised nutrition", "nutrigenomics", "diet genetics"
- "what should I eat based on my DNA"
- "nutrient metabolism", "vitamin absorption genetics"
- "MTHFR", "APOE", "FTO", "BCMO1", "VDR", "FADS1/2"
- "folate", "omega-3", "vitamin D", "caffeine metabolism", "lactose", "gluten"
- Input files: `.txt` or `.csv` (23andMe), `.csv` (AncestryDNA), `.vcf`

---

## Curated SNP Panel

> **Implemented panel: 28 SNPs across 24 genes, 12 nutrient domains** (see
> `data/snp_panel.json`). The tables below also list **3 documented candidate variants not yet in
> the scoring panel** — `ADRB2 rs1042713`, `HLA-DQ2` (proxy SNPs), and `GSTT1` (deletion) — which
> require genotyping/scoring approaches not yet implemented. They are shown for scientific context;
> the scorer evaluates only the 28 SNPs present in the JSON.

### Macronutrient Metabolism

| Gene    | SNP        | Nutrient Impact                          | Evidence |
|---------|------------|------------------------------------------|----------|
| FTO     | rs9939609  | Energy balance, fat mass, carb sensitivity | Strong (GWAS) |
| PPARG   | rs1801282  | Fat metabolism, insulin sensitivity      | Moderate |
| APOA5   | rs662799   | Triglyceride response to dietary fat     | Strong |
| TCF7L2  | rs7903146  | Carbohydrate metabolism, T2D risk        | Strong |
| ADRB2   | rs1042713  | Fat oxidation, exercise × diet interaction | Moderate |

### Micronutrient Metabolism

| Gene    | SNP        | Nutrient                | Effect of risk allele            |
|---------|------------|-------------------------|----------------------------------|
| MTHFR   | rs1801133  | Folate / B12            | ↓ 5-MTHF conversion (~70%)       |
| MTHFR   | rs1801131  | Folate / B12            | ↓ enzyme activity (~30%)         |
| MTR     | rs1805087  | B12 / homocysteine      | ↑ homocysteine risk              |
| BCMO1   | rs7501331  | Beta-carotene → Vitamin A | ↓ conversion (~50%)             |
| BCMO1   | rs12934922 | Beta-carotene → Vitamin A | ↓ conversion (compound het)    |
| VDR     | rs2228570  | Vitamin D absorption    | ↓ VDR function                   |
| VDR     | rs731236   | Vitamin D               | ↓ bone mineral density response  |
| GC      | rs4588     | Vitamin D binding       | ↑ deficiency risk                |
| SLC23A1 | rs33972313 | Vitamin C transport     | ↓ renal reabsorption             |
| ALPL    | rs1256335  | Vitamin B6              | ↓ alkaline phosphatase activity  |

### Omega-3 / Fatty Acid Metabolism

| Gene    | SNP        | Nutrient             | Effect                          |
|---------|------------|----------------------|---------------------------------|
| FADS1   | rs174546   | LC-PUFA synthesis    | ↑/↓ EPA/DHA from ALA            |
| FADS2   | rs1535     | LC-PUFA synthesis    | Modulates omega-6:omega-3 ratio |
| ELOVL2  | rs953413   | DHA synthesis        | A allele: lower EPA→DHA conversion |
| APOE    | rs429358   | Saturated fat response | ε4 → ↑ LDL-C on high SFA diet |
| APOE    | rs7412     | Saturated fat response | Combined with rs429358 for ε typing |

### Caffeine & Alcohol

| Gene    | SNP        | Compound    | Effect                         |
|---------|------------|-------------|--------------------------------|
| CYP1A2  | rs762551   | Caffeine    | Slow/Fast metaboliser          |
| AHR     | rs4410790  | Caffeine    | Modulates CYP1A2 induction     |
| ADH1B   | rs1229984  | Alcohol     | Acetaldehyde accumulation risk |
| ALDH2   | rs671       | Alcohol     | Asian flush / toxicity risk    |

### Food Sensitivities

| Gene    | SNP        | Sensitivity          | Effect                          |
|---------|------------|----------------------|---------------------------------|
| MCM6    | rs4988235  | Lactose intolerance  | Risk allele G (-13910C) is non-persistence; the persistence allele A (-13910T) is dominant |
| HLA-DQ2 | Proxy SNPs | Coeliac / gluten     | HLA-DQA1/DQB1 risk haplotypes   |

### Antioxidant & Detoxification

| Gene    | SNP        | Pathway              | Effect                          |
|---------|------------|----------------------|---------------------------------|
| SOD2    | rs4880     | Manganese SOD        | ↓ mitochondrial antioxidant     |
| GPX1    | rs1050450  | Selenium / GSH-Px    | ↓ glutathione peroxidase        |
| GSTT1   | Deletion   | Glutathione-S-trans  | Null genotype → ↑ oxidative risk|
| NQO1    | rs1800566  | Coenzyme Q10         | ↓ CoQ10 regeneration            |
| COMT    | rs4680     | Catechol / B vitamins | Met/Val → methylation load     |

---

## Algorithm

### 1. Input Parsing (`parse_input.py`)

Accepts:
- 23andMe `.txt` or `.csv` (tab-separated: rsid, chromosome, position, genotype)
- AncestryDNA `.csv`
- Standard VCF (extracts GT field)

Auto-detects format from header lines. Normalises alleles to forward strand using
a hard-coded reference table (avoids requiring external databases).

### 2. Genotype Extraction (`extract_genotypes.py`)

For each SNP in the panel:
1. Look up rsid in parsed data
2. Return genotype string (e.g. `"AT"`, `"TT"`, `"AA"`)
3. Flag as `"NOT_TESTED"` if absent (common for chip-to-chip variation)

### 3. Risk Scoring (`score_variants.py`)

Each SNP is scored on a **0 / 0.5 / 1.0** scale by default:
- `0.0` — homozygous reference (lowest risk)
- `0.5` — heterozygous
- `1.0` — homozygous risk allele

Lactose (`rs4988235`) instead declares `inheritance: dominant_protective` in the panel. Lactase
non-persistence is autosomal recessive, so one copy of the persistence allele is sufficient: AA
and AG both score 0.0, and only GG scores 1.0. Any panel entry without an `inheritance` field is
scored additively as above.

Composite **Nutrient Risk Scores** (0–10) are computed per nutrient domain by
summing weighted SNP scores. Weights are derived from reported effect sizes
(beta coefficients or OR) in the primary literature.

Risk categories:
- **0–3**: Low risk — standard dietary advice applies
- **3–6**: Moderate risk — dietary optimisation recommended
- **6–10**: Elevated risk — consider testing and targeted supplementation

> **Important caveat**: These are polygenic risk indicators based on common
> variants. They are not diagnostic. Rare pathogenic variants (e.g. MTHFR
> compound heterozygosity with high homocysteine) require clinical confirmation.

### 4. Report Generation (`generate_report.py`)

Outputs a structured Markdown report with:
- Executive summary (top 3 personalised findings)
- Per-nutrient sections: genotype table → interpretation → recommendation
- Radar chart (matplotlib) of nutrient risk scores
- Gene × nutrient heatmap (seaborn)
- Supplement interactions table
- Disclaimer section
- Reproducibility block

### 5. Reproducibility Bundle (`repro_bundle.py`)

Exports to the output directory (not committed to the repo):
- `README_reproducibility.txt` — step-by-step instructions to reproduce the analysis manually
- `environment.yml` — pinned conda environment
- `checksums.txt` — SHA-256 checksums of the SNP panel and output report (input file intentionally excluded to avoid persisting a fingerprint of genetic data)
- `provenance.json` — timestamp, version, and format arguments (input filename intentionally omitted)

**Note**: No executable scripts are generated. The reproducibility bundle contains
only text files for documentation and integrity verification.

---

## Execution

To run the analysis on a user-provided genetic file:

```bash
python <skill-dir>/nutrigenomics.py --input <path_to_genetic_file> --format auto
```

To run a demo without real genetic data (synthetic patient file included with the skill):

```bash
python <skill-dir>/nutrigenomics.py --input <skill-dir>/tests/synthetic_patient.csv --format 23andme
```

**Two rules make these commands work, and both matter.**

**1. Replace `<skill-dir>` with the absolute path to this skill's folder.** Each platform
supplies it:

- **Hermes** states it as `[Skill directory: ...]` when it loads this skill, and substitutes
  `${HERMES_SKILL_DIR}` anywhere that token appears.
- **OpenClaw** substitutes `{baseDir}` at runtime — e.g.
  `python {baseDir}/nutrigenomics.py --input ...`. Do not substitute it manually.
- Otherwise, use the literal absolute path of the skill folder.

**2. Run from the user's working directory — never `cd` into the skill folder.** The script
confines output to the current working directory (`path_safety.validate_output_dir`), so the
working directory decides where the report lands. Running from the user's directory puts it
there, which is correct. Running from inside the skill folder makes the skill folder the *only*
permitted destination, writing a report full of per-SNP genotype calls into the skill itself —
where it is liable to be swept into a publish, a commit, or a shared bundle.

Output is written to the directory named by `--output` (default: `nutrigenomics_results/`),
created under the current working directory, and persists until manually deleted. OpenClaw's
structured entry point (`openclaw_adapter.py`, declared in `openclaw.json`) instead defaults to
a timestamped `nutrigenomics_output_YYYYMMDD_HHMMSS/` directory.

Supported `--format` values: `auto` (default), `23andme`, `ancestry`, `vcf`.

## Usage

Ask the agent in plain language — it routes to this skill and runs the command above:

- "Generate my personalised nutrition report from genome.csv"
- "Run a nutrigenomics analysis on variants.vcf and flag any folate pathway risks"
- "What does my APOE status mean for my saturated fat intake?"
- "Run a demo nutrigenomics report using the synthetic patient file"

---

## File Structure

```
skills/nutrigenomics/
├── SKILL.md                      ← this file (agent instructions)
├── nutrigenomics.py            ← main entry point
├── parse_input.py                ← multi-format parser
├── extract_genotypes.py          ← SNP lookup engine
├── score_variants.py             ← risk scoring algorithm
├── generate_report.py            ← Markdown + figures
├── repro_bundle.py               ← reproducibility export
├── data/
│   └── snp_panel.json            ← curated SNP definitions
├── tests/
│   ├── synthetic_patient.csv     ← fixed 23andMe-format test data (for pytest)
│   └── test_nutrigenomics.py           ← pytest suite
└── examples/
    ├── generate_patient.py       ← random patient generator (demo use)
    ├── data/                     ← generated patient files land here (gitignored)
    └── output/
        ├── nutrigenomics_report.md     ← pre-rendered demo report
        ├── nutrigenomics_radar.png     ← demo radar chart (nutrient risk profile)
        └── nutrigenomics_heatmap.png   ← demo gene × nutrient heatmap
```

> **Note**: Runtime output directories and randomly generated patient files are
> excluded from version control. Only the pre-rendered demo
> report in `examples/output/` is committed.

---

## Privacy

All computation runs **locally** — no genetic data is ever transmitted to external
servers or third-party services.

**What the report contains**: The Markdown report includes per-SNP genotype calls
(e.g. `AT`, `TT`) for each of the 28 panel SNPs analysed. This is intentional:
knowing your specific genotype at each nutrition-related locus is what makes the
report actionable. Full raw genome data from the input file is not reproduced in
the report; only the 28 panel SNPs are included.

**The input filename appears in the report header.** It is shown so you can tell which file a
report came from, but a name like `jane_smith_genome.csv` identifies a person, and the report
is the artefact most likely to be shared with a clinician. Rename the input file first if that
matters to you. The filename is sanitised before it is written, so a name containing Markdown
or HTML cannot inject content into the report; the full path is never recorded anywhere.

**File persistence**: Output files (report, figures, reproducibility bundle) are
written to a timestamped `nutrigenomics_output_YYYYMMDD_HHMMSS/` directory under
the working directory and **persist on disk until manually deleted**. The input
file is read-only and is never copied into the output directory.

If you are running this skill on behalf of others or in a shared environment,
delete the output directory once the user has downloaded their results.

---

## Evidence Quality

Not every SNP in this panel rests on equally strong evidence, and the report does not weight
them by evidence quality — only by effect size. Every citation in `data/snp_panel.json` has
been checked against PubMed, and the panel splits into two tiers.

**Tier 1 — GWAS-backed.** A catalogued genome-wide association exists for this exact variant
and a trait matching its nutrient domain: MTHFR `rs1801133` and `rs1801131`, GC `rs4588`,
FADS1 `rs174546`, FADS2 `rs1535`, APOE `rs429358` and `rs7412`,
SLC23A1 `rs33972313`, ALPL `rs1256335`, FTO `rs9939609`, TCF7L2 `rs7903146`,
PPARG `rs1801282`, APOA5 `rs662799`, AHR `rs4410790`, ADH1B `rs1229984`, ALDH2 `rs671`,
MCM6 `rs4988235`.

**Tier 2 — candidate-gene evidence only.** No catalogued genome-wide association for the
assigned nutrient domain; the entry rests on functional or candidate-gene studies:
BCMO1 `rs7501331` and `rs12934922`, VDR `rs2228570` and `rs731236`, MTR `rs1805087`,
CYP1A2 `rs762551`, SOD2 `rs4880`, GPX1 `rs1050450`, NQO1 `rs1800566`, COMT `rs4680`.

Four Tier 2 entries carry caveats that a reader should know about:

- **`rs762551` (CYP1A2, caffeine)** — the widely used "fast vs slow caffeine metaboliser"
  interpretation is weaker than usually presented. In the source study (Sachse et al. 1999),
  caffeine metabolite ratios did **not** differ significantly between genotypes in 185
  non-smokers; the effect appeared only in 51 smokers, and is best understood as an
  inducibility effect. A contemporaneous study (Welfare et al. 1999) concluded that CYP1A2
  shows no functionally significant polymorphism at all.
- **`rs731236` (VDR, TaqI)** — the standard review of VDR polymorphisms describes the
  BsmI/ApaI/TaqI cluster as probably non-functional, with observed associations attributed to
  linkage disequilibrium with functional variants elsewhere in the gene. It is scored here as
  a haplotype tag, not as a causal variant.
- **`rs1050450` (GPX1, antioxidant)** — the phenotype study for this variant found no
  significant difference in erythrocyte glutathione peroxidase activity between genotypes and
  no association with stroke. It is retained for completeness; the evidence for a functional
  effect on antioxidant defence is weak.
- **`rs4680` (COMT, antioxidant)** — the three-to-four-fold effect on COMT enzyme activity is
  well established, but COMT inactivates catecholamines and catechol drugs. Its placement in
  the antioxidant domain reflects catechol handling rather than direct antioxidant defence.

`rs1805087` (MTR) is a genuine but modest determinant of homocysteine; its source study reports
an effect independent of folate and B12 status, and larger in people with low vitamin B6.

**`rs953413` (ELOVL2, omega-3)** sits between the tiers and is described on its own. The ELOVL2
locus is genome-wide significant for n-3 fatty acids (Lemaitre et al. 2011), but through other,
correlated SNPs; the GWAS Catalog holds no omega-3 association for `rs953413` itself. The direct
evidence is:

- **Association.** In Tanaka et al. 2009 (PMID 19148276) DHA fell from GG through AG to AA in two
  cohorts, and the minor A allele went with higher EPA and DPA and lower DHA. The discovery signal
  did not reach genome-wide significance; the DHA association replicated.
- **Mechanism.** In liver cell lines the G allele gives higher ELOVL2 enhancer activity than A
  (iScience 2020, PMID 31928966), consistent with A carriers converting less EPA to DHA.
- **Supplementation.** Mixed. A carriers showed larger rises in blood EPA and DHA in the MARINA
  trial (PMID 24292947) and a small 2025 study (PMID 40114193), but not in the seAFOod trial
  (PMID 42135634).

It is scored as an association with **lower EPA-to-DHA conversion**, not as a requirement: none of
these studies shows that any genotype is deficient or needs a particular daily intake. The effect is
modest, about 0.2 percentage points of DHA between GG and AA. Other ELOVL2 variants such as
`rs3734398`, `rs2236212` and `rs3798713` are strongly correlated with it in European, East and South
Asian ancestry, so they are not added as independent risks; doing so would count one signal several
times.

Treat Tier 2 scores as weaker signals than Tier 1 scores when interpreting a report.

---

## Threat Model and Limits

The input is a genetic data file. It is treated as **untrusted**: it may not have come from the
person reading the report, and everything derived from it reaches a Markdown document that is
likely to be shared onward. Four classes of risk are handled explicitly, so that new instances
are covered by an existing rule rather than fixed one at a time.

**1. Untrusted values reaching the report.** Every value written into the report is filtered
before rendering, not just the ones known to be attacker-controlled today: genotype calls, the
input filename, and the gene, rsID and effect text taken from the SNP panel. Genotypes are
additionally validated at parse time and non-nucleotide calls are discarded rather than scored.

**2. Resource exhaustion.** Parsing streams, but a genotype table still grows with the number of
variants, so streaming alone bounds nothing. Explicit caps in `path_safety.py`:

| Limit | Value | Why |
|---|---|---|
| `MAX_INPUT_BYTES` | 512 MB | a 23andMe export is ~25 MB |
| `MAX_VARIANTS` | 10,000,000 | a consumer export holds ~600,000 |
| `MAX_LINE_BYTES` | 64 KB | a real variant line is under 100 bytes |
| `MAX_HEADER_LINES` | 1,000 | only the header can identify a format |

Exceeding the file limit fails with a clear error; the others discard the excess and carry on.

**3. Filesystem safety.** Output is confined to the working directory, writes refuse to follow a
symbolic link at either the file or its parent directory, and output directories are created
exclusively with entropy added on collision, so concurrent runs cannot overwrite one another's
report.

**4. Provenance leakage.** No absolute path is written to any artefact. The input filename
appears in the report header only, and is sanitised.

**Out of scope.** Dependencies are declared with version bounds but not cryptographic hashes;
the skill installs nothing itself, and the four packages involved are needed only for figures.
The report necessarily contains per-SNP genotype calls — that is the point of it — and output
files persist until deleted.

---

## Limitations & Disclaimer

1. **Not a medical device.** This skill provides educational, research-oriented
   nutrigenomics analysis. It does not constitute medical advice.
2. **Common variants only.** The panel covers SNPs with MAF > 1% in at least one
   major population. Rare pathogenic variants are out of scope.
3. **Population context.** Effect sizes are predominantly derived from European
   GWAS cohorts. Risk estimates may not generalise equally across all ancestries.
4. **Gene–environment interaction.** Genetic risk scores interact with baseline
   diet, lifestyle, microbiome, and epigenetic state. A "high risk" score does not
   mean a nutrient deficiency is present — it means the individual may benefit from
   monitoring.
5. **Simpson's Paradox note.** Population-level associations used to derive weights
   may not reflect individual trajectories (see Corpas 2025, *Nutrigenomics and
   the Ecological Fallacy*).

---

## Roadmap

- [ ] **v0.2**: Microbiome × genotype interaction module (16S rRNA input)
- [ ] **v0.3**: Longitudinal tracking — compare reports across time
- [ ] **v0.4**: HLA typing for immune-mediated food reactions (coeliac, gluten sensitivity)
- [ ] **v1.0**: Multi-omics integration (metabolomics + genomics + dietary recall)

---

## References

This skill's SNP panel and methodology are informed by peer-reviewed nutrigenomics research. For verification and additional details, consult:

- **PubMed MEDLINE**: https://pubmed.ncbi.nlm.nih.gov/
- **GWAS Catalog**: https://www.ebi.ac.uk/gwas/ (published genome-wide association studies)
- **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/ (variant interpretations)

Users are encouraged to verify specific claims through these authoritative sources and with qualified healthcare providers.

---

## Contributing

The SNP panel (`data/snp_panel.json`) is maintained by the skill author.
To suggest additions or corrections, contact David de Lorenzo directly via
GitHub ([@drdaviddelorenzo](https://github.com/drdaviddelorenzo)) or open
an issue on GitHub.
