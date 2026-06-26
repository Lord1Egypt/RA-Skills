# Nutrigenomics for OpenClaw

**Transform your genetic data into actionable nutrition insights.**

Generate personalised nutrition recommendations based on your DNA in minutes. Nutrigenomics analyzes 40+ genes affecting how your body metabolises nutrients, absorbs vitamins, and responds to dietary compounds.

## 🚀 Quick Start

### 1. Get Your Genetic Data

Download your raw DNA file from:
- **23andMe**: Account → Download Your Data → Raw Data
- **AncestryDNA**: Account → DNA → Download your DNA
- **Already have a VCF file?** You can use that too

### 2. Upload to OpenClaw

Simply tell OpenClaw:
```
"Generate my personalised nutrition report from my genome file"
```

Then upload your `.txt`, `.csv`, or `.vcf` file.

### 3. Get Your Report

Within seconds, you'll receive:
- ✅ **Personalised nutrition recommendations**
- ✅ **Risk scores for 8 nutrient categories**
- ✅ **Visual breakdown** (radar chart of your nutrient profile)
- ✅ **Gene-nutrient interaction map** (heatmap)
- ✅ **Actionable guidance** (what to eat, what to supplement)

---

## 🧬 What Gets Analysed?

Nutrigenomics examines genes in these key areas:

### Micronutrient Metabolism
- **MTHFR** (Folate & B12 processing)
- **VDR** (Vitamin D absorption)
- **BCMO1** (Beta-carotene to Vitamin A conversion)

### Macronutrient Metabolism
- **APOE** (Saturated fat response)
- **FTO** (Energy balance & carb sensitivity)
- **PPARG** (Fat metabolism)

### Omega-3 & PUFA Metabolism
- **FADS1/2** (Omega-3 conversion efficiency)
- **ELOVL2** (DHA synthesis)

### Caffeine & Alcohol
- **CYP1A2** (Caffeine metabolism speed)
- **ADH1B/ALDH2** (Alcohol tolerance)

### Food Sensitivities
- **MCM6** (Lactose tolerance)
- **HLA-DQ2/8** (Coeliac risk proxies)

### Antioxidant & Detox
- **SOD2**, **GPX1**, **COMT**, and more

Plus **40+ total SNPs** from peer-reviewed nutrigenomics literature.

---

## 📊 Understanding Your Results

### Nutrient Risk Scores (0–10 scale)

| Score | Level | Meaning |
|-------|-------|---------|
| 0–3 | 🟢 Low Risk | Standard nutrition guidelines apply |
| 3–6 | 🟡 Moderate Risk | Dietary optimisation recommended |
| 6–10 | 🔴 Elevated Risk | Consider testing & supplementation |

### Example Report Section

```
FOLATE METABOLISM (B9)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Risk Score: 7.8/10 (Elevated)

Your Genotype Profile:
• MTHFR C677T: Heterozygous (CT)
• MTHFR A1298C: Homozygous Reference (AA)
• MTR A2756G: Heterozygous (AG)

Interpretation:
You carry a MTHFR variant affecting ~70% of enzyme activity.
This impacts your ability to convert dietary folate to active
5-methyltetrahydrofolate (5-MTHF). Combined with elevated
homocysteine genetic risk (MTR variant), you may benefit from:

Recommendations:
✓ Increase folate-rich foods: spinach, kale, lentils, chickpeas
✓ Consider methylfolate supplementation (400-800 mcg/day)
✓ Regular homocysteine testing (every 1-2 years)
✓ Ensure adequate B12 intake (cobalamin-rich foods or supplements)
✓ Avoid high-heat cooking of leafy greens (destroys folate)
```

---

## 🔒 Privacy & Security

**Your genetic data is 100% private.**

- ✅ All analysis runs **locally** on your device — no data is sent to external servers
- ✅ No account creation required
- ✅ Input file is never copied into the output directory
- ✅ Reports include per-SNP genotype calls for the 58 analysed SNPs only — your full raw genome data is not reproduced
- ✅ Output files persist in a local timestamped folder until you delete them
- ✅ Designed with privacy-first principles

You can share your final report with a healthcare provider. Be aware it will include genotype calls for the 58 nutrition-related SNPs analysed (e.g. `CT` for MTHFR rs1801133), which is the information that makes the report actionable.

---

## ⚠️ Important Disclaimers

### Not Medical Diagnosis
This skill provides **educational, research-oriented analysis**. It does not constitute:
- Medical diagnosis
- Medical advice
- Treatment recommendations
- Healthcare provider consultation replacement

**Always consult a qualified healthcare provider before making significant dietary changes or starting supplements.**

### Limitations
1. **Common variants only** — The panel covers SNPs with MAF > 1%. Rare pathogenic variants require clinical genetic testing.
2. **Population context** — Effect sizes derived primarily from European GWAS cohorts. Accuracy may vary across ancestries.
3. **Gene × Environment** — A "high risk" score indicates *potential*, not deficiency. Genetics interact with diet, lifestyle, stress, sleep, microbiome, and life stage.
4. **Simpson's Paradox** — Population-level associations may not perfectly reflect your individual trajectory.

---

## 📋 Input File Requirements

Your genetic data must be in one of these formats:

### 23andMe Format
```
rsid	chromosome	position	genotype
rs3094315	1	742429	AA
rs12562034	1	758311	AG
rs12124819	1	776546	AA
```

### AncestryDNA Format
```
rsid,chromosome,position,allele1,allele2
rs3094315,1,742429,A,A
rs12562034,1,758311,A,G
```

### VCF (Variant Call Format)
```
##fileformat=VCFv4.1
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	SAMPLE
1	742429	rs3094315	A	.	.	.	.	GT	0/0
1	758311	rs12562034	A	G	.	.	.	GT	0/1
```

**File size**: Typically 1-10 MB for consumer genetic data.

---

## 📥 What You'll Download

After analysis, you'll receive:

1. **nutrigenomics_report.md** — Full personalised report (Markdown)
   - Executive summary
   - Per-nutrient gene tables and interpretations
   - Actionable dietary recommendations
   - Supplement interaction guidance

2. **nutrigenomics_radar.png** — Nutrient risk profile radar chart
   - Visual overview of your 8 nutrient categories
   - Easy to share with healthcare providers

3. **nutrigenomics_heatmap.png** — Gene-nutrient interaction matrix
   - Which genes affect which nutrients
   - Color-coded risk levels

4. **README_reproducibility.txt** — Step-by-step instructions to reproduce the analysis
   - No executable scripts are generated

5. **environment.yml** — Pinned conda environment for reproducibility

6. **checksums.txt** — SHA-256 checksums of the SNP panel and output report only
   - The input file is intentionally excluded: checksumming a genetic file creates
     a stable fingerprint that could re-identify the dataset

7. **provenance.json** — Analysis metadata
   - Timestamp, software version, and analysis settings
   - Input filename is intentionally not recorded (avoids persisting a
     personally identifiable label alongside your genetic results)

> **Note on file persistence**: output files are saved to a timestamped folder
> (`nutrigenomics_output_YYYYMMDD_HHMMSS/`) in your working directory and remain
> there until you delete them.

---

## 🛠 Troubleshooting

### "File format not recognised"
- Ensure your file is genuine 23andMe, AncestryDNA, or VCF
- Check for unexpected line breaks or special characters
- Try re-downloading your raw data file from your test provider

### "Panel coverage low (< 50% SNPs found)"
- **This is normal.** Not all SNPs are tested by every genotyping chip
- The report will flag "NOT_TESTED" where data is absent
- Low coverage still provides valuable insights for well-covered pathways
- Different chips (23andMe, AncestryDNA, FTDNA, etc.) test different SNPs

### "No recommendations generated"
- Your genetic profile shows low risk across all nutrients
- This doesn't mean perfect health—genetics are only one factor
- You'll still benefit from standard nutritional guidance
- Consider consulting a registered dietitian for personalised advice

### "Error during analysis"
- Check that your file is under 100 MB
- Ensure it's unmodified from your test provider
- Try uploading again
- Contact support if the issue persists

---

## 🔬 Scientific Basis

The SNP panel and risk scoring algorithm are informed by peer-reviewed nutrigenomics research. For scientific verification:

**Verified Data Sources:**
- **PubMed MEDLINE**: https://pubmed.ncbi.nlm.nih.gov/
- **GWAS Catalog**: https://www.ebi.ac.uk/gwas/
- **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/

Users should consult these authoritative sources and healthcare providers for specific scientific claims and medical decisions.

**SNP Panel Design:**
- 58 SNPs across 40+ genes
- Evidence sourced from: GWAS Catalog, ClinVar, PubMed MEDLINE
- Minor allele frequency > 1% in major populations
- Effect sizes from peer-reviewed publications
- Regular updates as new evidence emerges

---

## 🚀 Next Steps After Your Report

### For Personalized Guidance
- **Registered Dietitian**: Share your report for professional interpretation
- **Functional Medicine Doctor**: Specialises in nutrigenomics-guided care
- **Clinical Nutritionist**: Can design tailored dietary protocols

### For Deeper Analysis
- Request **nutrient biomarker testing** (serum folate, B12, vitamin D, etc.)
- Consider **homocysteine testing** (if high folate/B12 risk)
- Get **genetic counselling** if you want to understand results more deeply

### For Ongoing Monitoring
- Rerun analysis periodically (yearly or after major diet changes)
- Track nutrient levels over time
- Monitor health outcomes and adjust recommendations

---

## 💬 Feedback & Contribution

Found a bug? Suggestions for SNPs to add? Want to contribute?

- **GitHub Issues**: [nutrigenomics/issues](https://github.com/clawbio/nutrigenomics/issues)
- **GitHub Discussions**: Community-driven questions and feature requests
- **GitHub**: [@drdaviddelorenzo](https://github.com/drdaviddelorenzo)
- **Website**: https://drdaviddelorenzo.github.io
- **Email**: david@drdaviddelorenzo.dev
- **Twitter**: [@drdaviddelorenzo](https://twitter.com/drdaviddelorenzo)

---

## 📜 License

Nutrigenomics is **free and open source** under the MIT License. You're free to:
- ✅ Use it personally
- ✅ Modify the code
- ✅ Redistribute it
- ✅ Use it commercially

See `LICENSE` file for details.

---

## 🙏 Acknowledgments


- **OpenClaw team** for platform integration
- **Nutrigenomics researchers** whose work underpins the SNP panel
- **Community contributors** who've helped refine the skill

---

## Quick Links

- 📚 [Full Documentation](SKILL_OPENCLAW.md)
- 🧬 [SNP Panel Reference](data/snp_panel.json)
- 🧪 [Test Data](tests/synthetic_patient.csv)
- 📖 [Example Report](examples/output/nutrigenomics_report.md)

---

**Nutrigenomics: Democratising personalised nutrition through open science and genetic literacy.**

*Made with 🧬 and ❤️ for health-conscious individuals everywhere.*
