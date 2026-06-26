# 🧬 Personal Genomics — Your AI Genetic Analyst

**[中文版](README.md)**

> Turn consumer genetic testing data into actionable health insights.

Got your raw data from 23andMe, AncestryDNA, or WeGene but not sure what to do with it? This Claude Skill transforms Claude into a professional genomics analyst that walks you through a complete analysis pipeline — from raw genotypes to personalized health reports, medication guidance, and supplement plans.

## ✨ What It Does

The analysis follows a four-phase conversational workflow, like consulting with a specialist:

### Phase 1 · Data Intake
Drop your genetic data files into the conversation. Claude auto-detects the source and format, reports data quality, variant counts, and reference genome build.

### Phase 2 · Comprehensive Screening
Scans **~120 clinically relevant SNPs** across six domains:

| Domain | What's Covered | Key Genes |
|--------|---------------|-----------|
| 🏥 Health Risks | Cancer, cardiovascular, metabolic, neurodegenerative | BRCA1/2, APOE, TCF7L2, 9p21.3 |
| 💊 Pharmacogenomics | Drug metabolizer status, medication sensitivity | CYP2D6, CYP2C19, VKORC1, SLCO1B1 |
| 🥗 Nutrition | Lactose tolerance, folate, vitamin D, omega-3 | MTHFR, VDR, FADS1, ALDH2 |
| 🏃 Exercise | Muscle fiber type, endurance tendency, recovery | ACTN3, ACE, PPARGC1A |
| 🌍 Ancestry | mtDNA/Y-chromosome haplogroups (WGS data required) | — |
| 🔬 Deep Risk Panels | 10-20 loci per pathway: lipid, CAD, gout, diabetes | LDLR, PCSK9, SLC2A9, ABCG2 |

Every finding comes with published research citations (PMIDs).

### Phase 3 · Deep Dive
Claude asks about your known conditions, family history, current medications, and lifestyle. Then it runs **50+ extended SNPs** across disease pathways most relevant to you, cross-referencing genetics with your actual medical context.

### Phase 4 · Personalized Recommendations
Delivers actionable plans:
- **Supplement protocol** — tiered by priority (core / recommended / optional) with dosages, timing, and drug interaction notes
- **Screening schedule** — customized lab tests and frequencies based on your risk profile
- **Age milestones** — proactive screening reminders at key ages

Output formats: interactive HTML report, Excel dosing schedule, one-page physician summary.

## 📂 Supported Data Formats

| Platform | File Type | Notes |
|----------|-----------|-------|
| 23andMe | `.txt` (TSV) | Raw data download |
| AncestryDNA | `.txt` (TSV) | Raw DNA data download |
| WeGene (微基因) | `.txt` (TSV) | Exported core data file |
| WGS/WES | `.vcf` / `.vcf.gz` | Standard VCF v4.x |
| Alignment | `.cram` / `.bam` | For read-level variant verification |

Multiple files can be loaded simultaneously — e.g., chip data + VCF. The skill automatically uses a **dual-source lookup strategy** to maximize SNP coverage.

## 🚀 Installation & Usage

### Option 1: Install the .skill File (Recommended)

1. Download `personal-genomics.skill` from the [Releases](../../releases) page
2. Install the skill in Claude Desktop
3. Place your genetic data files in the working directory
4. Tell Claude: "Analyze my genetic data"

### Option 2: Install from Source

```bash
git clone https://github.com/yanzhanglee/personal-genomics--.git
# Configure the cloned directory as a Claude Skill path
```

### Usage Example

```
👤 I have my 23andMe raw data and a VCF from whole genome sequencing.
   Can you analyze them?

🤖 [Auto-detects formats → Parses data → Generates initial report]

👤 I have high cholesterol and gout. My father had a heart attack at 54.
   Can you do a deeper analysis on these risks?

🤖 [Launches deep risk panels → 50+ SNPs across lipid/CAD/gout pathways]

👤 Based on the results, create a supplement plan and daily dosing schedule.

🤖 [Generates tiered supplement plan + Excel schedule + monitoring timeline]
```

## 📁 Project Structure

```
personal-genomics/
├── SKILL.md                         # Core workflow instructions
├── scripts/
│   └── parse_genotypes.py           # Universal genotype parser
├── references/
│   ├── supported_formats.md         # Data format specifications
│   ├── snp_database.md              # Curated SNP database (~120 entries w/ PMIDs)
│   ├── supplement_guide.md          # Evidence-based supplement guide
│   └── tool_setup.md               # samtools/bcftools build guide
└── evals/
    ├── evals.json                   # Test case definitions
    └── test_data/                   # Mock test data
```

## ⚠️ Disclaimer

This skill provides genetic risk estimates for informational purposes only and does not constitute medical diagnosis or treatment advice. Genetic risk assessments reflect statistical probabilities, not certainties. All findings should be discussed with a qualified healthcare provider before making decisions. Consumer genetic testing differs from clinical-grade testing in coverage and accuracy.

## 📄 License

MIT License — free to use, modify, and distribute.

---

<p align="center">
  <i>Read your genome with AI. Take charge of your health.</i>
</p>
