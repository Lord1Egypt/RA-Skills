# Personal Genomics SNP Database Reference

**Document Type:** Reference Guide
**Version:** 1.0
**Last Updated:** 2026-03-18
**Purpose:** Human-readable reference for SNP analysis in consumer genetic testing

> **Note:** The SNP database is maintained in JSON-compatible format in the scripts directory for programmatic use. This document serves as a human-readable reference guide with detailed explanations and context.

---

## Table of Contents

1. [Health Risk SNPs](#health-risk-snps)
2. [Pharmacogenomics SNPs](#pharmacogenomics-snps)
3. [Nutrition & Metabolism SNPs](#nutrition--metabolism-snps)
4. [Exercise SNPs](#exercise-snps)
5. [Deep Risk Extended Panels](#deep-risk-extended-panels)
6. [Special Genotyping Cases](#special-genotyping-cases)
7. [Evidence Levels & Data Quality](#evidence-levels--data-quality)

---

## Health Risk SNPs

This section covers SNPs associated with increased disease risk across multiple pathways. Evidence levels range from strong (large GWAS studies) to moderate (replicated findings).

### Cancer Risk

#### BRCA1 rs80357906
- **Gene:** BRCA1
- **Variant Name:** c.68_69delAG (frameshift)
- **Risk Allele:** Deletion
- **Trait/Condition:** Breast and ovarian cancer predisposition
- **Evidence Level:** Strong (Clinical validity)
- **Inheritance Pattern:** Autosomal dominant
- **Description:** Classic pathogenic BRCA1 mutation conferring ~70% lifetime breast cancer risk and ~40% ovarian cancer risk. Requires immediate clinical genetic counseling and potentially preventive measures.

#### BRCA2 rs80357713
- **Gene:** BRCA2
- **Variant Name:** c.9097C>T (nonsense)
- **Risk Allele:** T (stop codon)
- **Trait/Condition:** Breast, ovarian, and pancreatic cancer predisposition
- **Evidence Level:** Strong (Clinical validity)
- **Inheritance Pattern:** Autosomal dominant
- **Description:** BRCA2 loss-of-function variant causing truncated protein. Associated with ~60% lifetime breast cancer risk, ~40% ovarian cancer risk, and increased pancreatic/prostate cancer risk.

### Diabetes Risk

#### TCF7L2 rs7903146
- **Gene:** TCF7L2 (Transcription Factor 7-Like 2)
- **Variant Name:** rs7903146 C→T
- **Risk Allele:** T
- **Trait/Condition:** Type 2 diabetes
- **Evidence Level:** Strong (largest GWAS effect size for T2D)
- **PMID:** 17463246
- **Allele Frequency:** ~35% (European ancestry)
- **Description:** Most robust genetic variant for T2D risk. Heterozygotes have ~1.4x increased risk; homozygotes ~2.4x. Affects glucose homeostasis and insulin secretion. Clinically actionable through lifestyle modification.

#### KCNJ11 rs5219
- **Gene:** KCNJ11 (Potassium inwardly rectifying channel)
- **Variant Name:** rs5219 E23K (c.68G>A)
- **Risk Allele:** A (K allele)
- **Trait/Condition:** Type 2 diabetes
- **Evidence Level:** Moderate (replicated meta-analyses)
- **PMID:** 17463246
- **Effect Size:** OR ~1.17 per risk allele
- **Description:** Encodes ATP-sensitive potassium channel subunit; variants impair insulin secretion response. Common variant with modest effect size but good effect replication.

#### SLC30A8 rs13266634
- **Gene:** SLC30A8 (Zinc transporter 8)
- **Variant Name:** rs13266634 C→T
- **Risk Allele:** T
- **Trait/Condition:** Type 2 diabetes
- **Evidence Level:** Moderate (GWAS-confirmed)
- **PMID:** 17463246
- **Effect Size:** OR ~1.12 per risk allele
- **Description:** Zinc transporter in pancreatic beta cells; affects insulin secretion. Particularly relevant in populations of East Asian descent.

#### PPARG rs1801282
- **Gene:** PPARG (Peroxisome proliferator-activated receptor gamma)
- **Variant Name:** rs1801282 C→G (Pro12Ala)
- **Risk Allele:** G (Ala)
- **Trait/Condition:** Type 2 diabetes (protective)
- **Evidence Level:** Strong (functional studies)
- **PMID:** 14564013
- **Allele Frequency:** ~10-15% (European)
- **Description:** Functional variant in thiazolidinedione drug target. G-allele is **protective** (0.8x risk), responsive to PPARG agonists. Strong pharmacogenomic relevance.

### Cardiovascular Risk

#### 9p21.3 rs1333049
- **Gene:** 9p21.3 (CDKN2A/B locus)
- **Variant Name:** rs1333049 C→T
- **Risk Allele:** T
- **Trait/Condition:** Coronary artery disease, myocardial infarction
- **Evidence Level:** Strong (GWAS with large effect)
- **PMID:** 17554300
- **Effect Size:** OR ~1.20 per allele
- **Description:** Strongest common genetic variant for CAD; affects cell cycle and vascular remodeling. Replicated across multiple populations. Suggested cutoff for preventive cardiology assessment.

#### 9p21.3 rs10757274
- **Gene:** 9p21.3
- **Variant Name:** rs10757274 G→A
- **Risk Allele:** A
- **Trait/Condition:** Coronary artery disease, myocardial infarction, aneurysm
- **Evidence Level:** Strong (GWAS)
- **Effect Size:** OR ~1.19 per allele
- **Description:** Independent signal in 9p21.3 region; distinct from rs1333049. Both SNPs tag same causal region with pleiotropic effects on vascular disease.

#### CXCL12 rs4665058
- **Gene:** CXCL12 (C-X-C motif chemokine ligand 12)
- **Variant Name:** rs4665058 G→A
- **Risk Allele:** A
- **Trait/Condition:** Coronary artery disease
- **Evidence Level:** Moderate (GWAS-identified)
- **Effect Size:** OR ~1.08 per allele
- **Description:** Chemokine involved in vascular inflammation and endothelial dysfunction. Pathway relevant for atherosclerosis development.

#### MTHFR rs1801133
- **Gene:** MTHFR (Methylenetetrahydrofolate reductase)
- **Variant Name:** rs1801133 C→T (Ala222Val)
- **Risk Allele:** T
- **Trait/Condition:** Cardiovascular disease, homocysteine elevation, thrombosis
- **Evidence Level:** Moderate (complex genetics)
- **Allele Frequency:** ~30-35% (European)
- **Description:** Reduces enzyme activity (TT genotype ~30% activity). Associated with elevated homocysteine in some populations. Frequently tested but clinical utility debated; responsive to B-vitamin therapy.

#### MTR rs1805087
- **Gene:** MTR (Methionine synthase)
- **Variant Name:** rs1805087 A→G (Asp919Gly)
- **Risk Allele:** G
- **Trait/Condition:** Elevated homocysteine, cardiovascular risk
- **Evidence Level:** Moderate (meta-analyses)
- **Description:** Involved in homocysteine metabolism. Often analyzed with MTHFR as part of methylation pathway assessment for cardiovascular risk stratification.

### Neurodegenerative Disease Risk

#### APOE rs429358 & rs7412
- **Gene:** APOE (Apolipoprotein E)
- **Variant Names:** rs429358 (C→T, Arg112Cys), rs7412 (C→T, Arg158Cys)
- **Risk Allele:** T for rs429358 (defines ε4 allele)
- **Trait/Condition:** Alzheimer's disease, cognitive decline
- **Evidence Level:** Strong (consistent replication)
- **PMID:** 7894484
- **Genotype Interpretation:** See Special Genotyping Cases section
- **Description:** APOE4 (ε4) carriers have 3-8x increased AD risk (dose-dependent). APOE2 (ε2) is protective. Most clinically significant genetic risk factor for late-onset Alzheimer's. Requires careful genetic counseling due to clinical significance.

### Gout Risk

#### ABCG2 rs2231142
- **Gene:** ABCG2 (ATP-binding cassette transporter)
- **Variant Name:** rs2231142 G→T (Gln141Lys)
- **Risk Allele:** T
- **Trait/Condition:** Gout, hyperuricemia
- **Evidence Level:** Strong (large GWAS)
- **PMID:** 18391955
- **Effect Size:** OR ~1.80 per T allele
- **Description:** Reduces urate transport efficiency in kidney; strongest common genetic determinant of gout. T-allele shows dose-dependent risk. Responsive to uricosuric therapy.

#### SLC2A9 rs505802
- **Gene:** SLC2A9 (Glucose transporter 9)
- **Variant Name:** rs505802 C→G
- **Risk Allele:** C
- **Trait/Condition:** Gout, hyperuricemia
- **Evidence Level:** Strong (GWAS)
- **PMID:** 18391955
- **Effect Size:** OR ~1.25 per C allele
- **Description:** Renal urate transporter; variants affect uric acid reabsorption. Second strongest common genetic variant for gout after ABCG2.

### Thrombosis Risk

#### Factor V (F5) rs6025
- **Gene:** F5 (Coagulation factor V)
- **Variant Name:** rs6025 G→A (Arg506Gln, Factor V Leiden)
- **Risk Allele:** A
- **Trait/Condition:** Venous thromboembolism, deep vein thrombosis, pulmonary embolism
- **Evidence Level:** Strong (clinical validity)
- **Inheritance Pattern:** Autosomal dominant
- **Prevalence:** ~5% (European), <1% (African)
- **Description:** Classic thrombophilia mutation reducing protein C inhibition. Heterozygotes ~7x VTE risk; homozygotes ~80x. Critical for surgical/immobilization risk assessment. Anticoagulation guidance dependent on genotype.

#### Prothrombin (F2) rs1799963
- **Gene:** F2 (Coagulation factor II/Prothrombin)
- **Variant Name:** rs1799963 G→A (20210 G>A)
- **Risk Allele:** A
- **Trait/Condition:** Venous thromboembolism
- **Evidence Level:** Strong (clinical validity)
- **Inheritance Pattern:** Autosomal dominant
- **Prevalence:** ~2-3% (European)
- **Description:** Elevates prothrombin mRNA levels and clotting activity. Heterozygotes ~3x VTE risk. Often tested alongside Factor V Leiden. May influence warfarin dosing.

### Age-Related Macular Degeneration (AMD)

#### Complement Factor H (CFH) rs1061170
- **Gene:** CFH (Complement factor H)
- **Variant Name:** rs1061170 C→T (Tyr402His)
- **Risk Allele:** T
- **Trait/Condition:** Age-related macular degeneration (AMD)
- **Evidence Level:** Strong (largest AMD GWAS)
- **PMID:** 16377562
- **Effect Size:** OR ~2.45 per T allele
- **Prevalence:** ~35% in European ancestry
- **Description:** Strongest genetic risk factor for AMD. T-allele impairs complement regulation in retina. Homozygotes show ~4x increased AMD risk. Influences anti-VEGF treatment response.

### Celiac Disease

#### HLA-DQ2.5 rs2187668
- **Gene:** HLA-DQA1
- **Variant Name:** rs2187668 (part of HLA-DQ2 molecule)
- **Risk Allele:** Allele encoding DQ2-α chain
- **Trait/Condition:** Celiac disease susceptibility
- **Evidence Level:** Strong (necessary but not sufficient)
- **Prevalence:** ~30-40% (Caucasian)
- **Description:** HLA-DQ2 required (but not sufficient) for celiac disease development. Present in ~95% of celiac patients. Negative predictive value useful for celiac exclusion. Always test alongside HLA-DQ8 and tissue transglutaminase (tTG) serology.

### Autoimmune Disease

#### PTPN22 rs2476601
- **Gene:** PTPN22 (Protein tyrosine phosphatase, non-receptor type 22)
- **Variant Name:** rs2476601 C→T (Arg620Trp)
- **Risk Allele:** T
- **Trait/Condition:** Rheumatoid arthritis, lupus, type 1 diabetes, autoimmune thyroid disease
- **Evidence Level:** Strong (replicated across autoimmune conditions)
- **PMID:** 15057824
- **Effect Size:** OR ~1.6 per T allele (RA)
- **Prevalence:** ~10-15% (European)
- **Description:** Loss of immune tolerance mechanism. Pleiotropic effects across multiple autoimmune disorders. T-allele confers risk to multiple autoimmune phenotypes. Clinically actionable for disease monitoring and prevention strategies.

### Parkinson's Disease

#### GBA rs76763715
- **Gene:** GBA (Glucosidase beta acid)
- **Variant Name:** rs76763715 (N370S, p.Asn370Ser)
- **Risk Allele:** Mutant allele
- **Trait/Condition:** Parkinson's disease, Gaucher disease
- **Evidence Level:** Strong (clinical validity)
- **Effect Size:** ~5x increased PD risk
- **Description:** Lysosomal enzyme mutation; homozygotes cause Gaucher disease. Heterozygotes show increased PD risk, especially in Ashkenazi Jewish populations. Biological mechanism involves alpha-synuclein accumulation.

#### LRRK2 rs34637584
- **Gene:** LRRK2 (Leucine-rich repeat kinase 2)
- **Variant Name:** rs34637584 G→A (Gly2019Ser)
- **Risk Allele:** A
- **Trait/Condition:** Parkinson's disease (late-onset)
- **Evidence Level:** Strong (large effect size)
- **Inheritance Pattern:** Autosomal dominant (incomplete penetrance ~70-80%)
- **Prevalence:** ~1-2% in PD patients
- **Description:** Gain-of-function mutation; most common known PD mutation. Particularly prevalent in North African and Middle Eastern ancestry. Strong kinase activity; target for therapeutic development.

---

## Pharmacogenomics SNPs

SNPs affecting drug metabolism, efficacy, and adverse reactions. Essential for precision medicine and dose optimization.

### CYP2D6 (Cytochrome P450 2D6)

#### CYP2D6 rs3892097
- **Gene:** CYP2D6
- **Variant Name:** rs3892097 (defines *4 allele, splice defect)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Poor metabolizer phenotype
- **Evidence Level:** Strong (functional studies)
- **Affected Drugs:** Codeine, tramadol, metoprolol, aripiprazole, venlafaxine, risperidone
- **Clinical Action:** Reduce dose or select alternative; codeine ineffective (no active metabolite)
- **Description:** Most common CYP2D6 loss-of-function allele in European populations (~1% frequency). Causes reduced/absent enzyme activity. Critical for opioid metabolism and antipsychotic dosing.

#### CYP2D6 rs16947
- **Gene:** CYP2D6
- **Variant Name:** rs16947 (part of *2 allele, increased function)
- **Status Allele:** Gain-of-function
- **Trait/Condition:** Ultra-rapid metabolizer phenotype
- **Evidence Level:** Strong
- **Affected Drugs:** Beta-blockers, antidepressants, antiarrhythmics
- **Clinical Action:** May require higher doses; monitor efficacy
- **Description:** *2 allele confers increased enzyme activity. Particularly important in Mediterranean and Middle Eastern populations. Drug level monitoring recommended for narrow therapeutic index drugs.

### CYP2C19 (Cytochrome P450 2C19)

#### CYP2C19 rs4244285
- **Gene:** CYP2C19
- **Variant Name:** rs4244285 G→A (defines *2 allele)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Intermediate/poor metabolizer
- **Evidence Level:** Strong (FDA-endorsed)
- **Affected Drugs:** Clopidogrel (Plavix), omeprazole, escitalopram, sertraline
- **Clinical Action:** Consider prasugrel/ticagrelor instead of clopidogrel; adjust SSRI dose
- **PMID:** 19668215
- **Description:** Most common CYP2C19 LoF variant. **Critical for clopidogrel efficacy:** *2 carriers show reduced antiplatelet effect and increased stent thrombosis risk (~50% reduction in active metabolite).

#### CYP2C19 rs4986893
- **Gene:** CYP2C19
- **Variant Name:** rs4986893 G→A (defines *3 allele)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Poor metabolizer
- **Evidence Level:** Strong
- **Affected Drugs:** Same as *2 (clopidogrel critical)
- **Prevalence:** ~0.5% (European), ~2-5% (Asian)
- **Description:** Rare in Caucasians but significant in East Asian populations. Premature termination codon. Produces no functional enzyme.

#### CYP2C19 rs12248560
- **Gene:** CYP2C19
- **Variant Name:** rs12248560 C→T (defines *17 allele)
- **Status Allele:** Gain-of-function
- **Trait/Condition:** Ultra-rapid/rapid metabolizer
- **Evidence Level:** Strong
- **Affected Drugs:** Clopidogrel (enhanced effect), omeprazole, escitalopram
- **Clinical Action:** Higher dose or alternative antiplatelet agent; monitor efficacy
- **Prevalence:** ~25-30% (European)
- **Description:** Increased enzyme expression (~3-fold in some tissues). Particularly relevant for clopidogrel where rapid metabolism may increase bleeding risk despite enhanced antiplatelet effect.

#### CYP2C19 Metabolizer Status Summary
| Genotype | Status | Frequency | Clinical Implication |
|----------|--------|-----------|----------------------|
| *1/*1 | Normal | ~40-50% | Standard dosing |
| *1/*2, *1/*3 | Intermediate | ~35-45% | Consider dose reduction (especially clopidogrel) |
| *2/*2, *2/*3, *3/*3 | Poor | ~2-5% | Significant dose reduction or alternative drug |
| *1/*17, *2/*17 | Rapid | ~20-30% | May require higher doses or alternative |
| *17/*17 | Ultra-rapid | ~2-5% | Higher doses or alternative therapy |

### CYP2C9 (Cytochrome P450 2C9)

#### CYP2C9 rs1799853
- **Gene:** CYP2C9
- **Variant Name:** rs1799853 C→T (defines *2 allele, Arg144Cys)
- **Status Allele:** Loss-of-function (~40% activity)
- **Trait/Condition:** Reduced metabolizer
- **Evidence Level:** Strong (FDA-endorsed for warfarin)
- **Affected Drugs:** Warfarin, NSAIDs, phenytoin, losartan
- **Clinical Action:** Reduce warfarin dose; increased bleeding risk at standard dose
- **Prevalence:** ~8-13% (European)
- **PMID:** 15173630
- **Description:** Affects warfarin metabolism directly. Carriers require ~20-30% dose reduction. Pharmacogenomic testing strongly recommended for warfarin initiation.

#### CYP2C9 rs1057910
- **Gene:** CYP2C9
- **Variant Name:** rs1057910 A→C (defines *3 allele, Ile359Leu)
- **Status Allele:** Loss-of-function (~5-10% activity)
- **Trait/Condition:** Poor metabolizer
- **Evidence Level:** Strong (FDA guidance)
- **Affected Drugs:** Warfarin (strong effect), NSAIDs, phenytoin
- **Clinical Action:** Significant warfarin dose reduction (~40-50%); high bleeding risk
- **Prevalence:** ~1-2% (European), ~0-1% (African)
- **PMID:** 15173630
- **Description:** Rare but functionally severe. *3 homozygotes can be genetically poor metabolizers requiring markedly reduced warfarin dosing.

### Vitamin K Epoxide Reductase (VKORC1)

#### VKORC1 rs9923231
- **Gene:** VKORC1 (Vitamin K epoxide reductase complex subunit 1)
- **Variant Name:** rs9923231 G→A (-1639 G→A, regulatory region)
- **Risk Allele:** A (low vitamin K recycling)
- **Trait/Condition:** Warfarin sensitivity
- **Evidence Level:** Strong (FDA-endorsed for warfarin dosing)
- **Affected Drugs:** Warfarin, acenocoumarol
- **Clinical Action:** A-allele carriers require lower warfarin doses
- **PMID:** 15173630
- **Description:** Regulatory variant reducing VKORC1 expression. Works synergistically with CYP2C9 status for warfarin dosing prediction. Included in FDA warfarin labeling. Essential for precision anticoagulation.

### N-Acetyltransferase 2 (NAT2)

#### NAT2 rs1799930
- **Gene:** NAT2
- **Variant Name:** rs1799930 G→A (defines slow acetylator)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Slow acetylator phenotype
- **Evidence Level:** Strong
- **Affected Drugs:** Isoniazid, sulfasalazine, dapsone, procainamide, hydralazine
- **Clinical Action:** Slow acetylators at increased risk of drug toxicity/lupus-like syndrome
- **Description:** Loss-of-function variant in drug-metabolizing enzyme. Slow acetylators (~50% population) have increased isoniazid-induced peripheral neuropathy risk.

#### NAT2 rs1801280
- **Gene:** NAT2
- **Variant Name:** rs1801280 G→A (slow acetylator determinant)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Slow acetylator phenotype
- **Evidence Level:** Strong
- **Description:** Combined analysis of NAT2 rs1799930 and rs1801280 determines phenotype. Individuals with two slow-alleles show significantly altered pharmacokinetics for NAT2 substrates.

### SLCO1B1 (Statin Transporter)

#### SLCO1B1 rs4149056
- **Gene:** SLCO1B1
- **Variant Name:** rs4149056 T→C (Val174Ala)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Increased statin myopathy risk
- **Evidence Level:** Strong (GWAS for statin side effects)
- **Affected Drugs:** Simvastatin (strong), atorvastatin, pravastatin, rosuvastatin
- **Clinical Action:** Consider alternative statin; if using simvastatin, use reduced dose and monitor CK
- **PMID:** 21151968
- **Description:** Reduces hepatic statin uptake, increasing plasma levels and myopathy risk. FDA warning for simvastatin in *5/*5 carriers. Effect strongest with simvastatin, less with pravastatin.

### Dihydropyrimidine Dehydrogenase (DPYD)

#### DPYD rs3918290
- **Gene:** DPYD
- **Variant Name:** rs3918290 (IVS14+1G>A, *2A allele)
- **Status Allele:** Loss-of-function (complete enzyme deficiency)
- **Trait/Condition:** Severe 5-fluorouracil (5-FU) toxicity/lethality
- **Evidence Level:** Strong (FDA black-box warning)
- **Affected Drugs:** 5-fluorouracil, capecitabine
- **Clinical Action:** **CONTRAINDICATED** - do not use fluoropyrimidines
- **Prevalence:** ~0.5% carriers
- **PMID:** 26244876
- **Description:** Classic pharmacogenetic variant causing deficiency in critical chemotherapy enzyme. Homozygotes experience life-threatening toxicity. Pretest recommended before fluoropyrimidine chemotherapy.

### CYP1A2 (Caffeine Metabolism)

#### CYP1A2 rs762551
- **Gene:** CYP1A2
- **Variant Name:** rs762551 A→C (-163 C→A, regulatory)
- **Status Allele:** Reduced function (C-allele)
- **Trait/Condition:** Slow caffeine metabolism
- **Evidence Level:** Moderate (caffeine metabolism studies)
- **Affected Drugs:** Caffeine, theophylline
- **Clinical Action:** Slow metabolizers should limit caffeine intake
- **Description:** Regulatory variant affecting CYP1A2 induction. C-allele carriers metabolize caffeine ~50% slower. Note: Same SNP classified under metabolism section for nutrition phenotyping.

### ALDH2 (Alcohol Metabolism)

#### ALDH2 rs671
- **Gene:** ALDH2 (Aldehyde dehydrogenase 2)
- **Variant Name:** rs671 G→A (Glu487Lys)
- **Status Allele:** Loss-of-function
- **Trait/Condition:** Alcohol flushing, reduced alcohol tolerance
- **Evidence Level:** Strong (functional studies)
- **Affected Drugs:** Alcohol, disulfiram interaction risk
- **Prevalence:** ~30-50% (East Asian), <5% (European)
- **Description:** Dramatically reduces aldehyde metabolism. Causes painful facial flushing, nausea, tachycardia after small alcohol amounts. ALDH2-deficient individuals advised to minimize alcohol. Increased risk of esophageal cancer with alcohol exposure.

### Alcohol Dehydrogenase (ADH1B)

#### ADH1B rs1229984
- **Gene:** ADH1B
- **Variant Name:** rs1229984 A→G (Arg48His)
- **Status Allele:** Increased function
- **Trait/Condition:** Rapid alcohol metabolism, reduced alcohol dependence risk
- **Evidence Level:** Strong (population genetic studies)
- **Prevalence:** ~50-70% (East Asian), ~5% (European)
- **Description:** Increased enzyme activity accelerates alcohol metabolism, causing rapid toxic acetaldehyde accumulation. Common in East Asia, associated with protective effects against alcoholism. Often co-occurs with ALDH2 variants.

---

## Nutrition & Metabolism SNPs

SNPs informing dietary and micronutrient metabolism, including lactose tolerance, folate, vitamin D, and fatty acid metabolism.

### Lactose Tolerance

#### MCM6 rs4988235
- **Gene:** MCM6 (Minichromosome maintenance complex component 6)
- **Variant Name:** rs4988235 C→T (-13910 C→T)
- **Risk Allele:** T (lactase persistence)
- **Trait/Condition:** Lactose intolerance vs. persistence
- **Evidence Level:** Strong (functional studies)
- **Prevalence:** ~35% (European), ~90% (Northern European), <10% (East Asian)
- **Description:** Regulatory variant controlling lactase expression into adulthood. T-allele enables lactase persistence; CC individuals typically lactose intolerant. Population-specific: common in Northern European and pastoral populations, rare elsewhere.

### Folate Metabolism

#### MTHFR rs1801133
- **Gene:** MTHFR
- **Variant Name:** rs1801133 C→T (Ala222Val, 677 C→T)
- **Risk Allele:** T
- **Trait/Condition:** Reduced folate metabolism efficiency
- **Evidence Level:** Strong (enzyme kinetics)
- **Prevalence:** ~30-35% heterozygotes, ~10-12% homozygotes (European)
- **Description:** Reduces enzyme activity: TT ~30% of normal activity, CT ~65% activity. Homozygotes may benefit from increased folate intake, methylfolate supplementation, and B-vitamin fortification. See also: Pharmacogenomics and Special Genotyping Cases sections.

### Vitamin D Metabolism

#### Vitamin D Receptor (VDR) rs2228570
- **Gene:** VDR (Vitamin D receptor)
- **Variant Name:** rs2228570 (Bsm1, 3'UTR variant)
- **Risk Allele:** A (associated with lower vitamin D production)
- **Trait/Condition:** Vitamin D efficiency, bone health
- **Evidence Level:** Moderate (observational studies)
- **Description:** 3' untranslated region variant affecting receptor expression. AA genotype associated with lower vitamin D bioavailability and lower bone mineral density. Dietary vitamin D intake and sun exposure more critical for AA carriers.

#### CYP2R1 rs10741657
- **Gene:** CYP2R1 (Cytochrome P450 family 2 subfamily R member 1)
- **Variant Name:** rs10741657 A→G
- **Risk Allele:** A (associated with lower 25-OH vitamin D levels)
- **Trait/Condition:** Vitamin D synthesis efficiency
- **Evidence Level:** Strong (GWAS-confirmed)
- **PMID:** 20053123
- **Effect Size:** ~3-4 nmol/L lower per risk allele
- **Description:** CYP2R1 catalyzes critical step in vitamin D activation. A-allele carriers show ~10% lower circulating 25-OH vitamin D levels. Suggests need for higher dietary vitamin D or sun exposure in A-carriers.

### Vitamin B12 Metabolism

#### FUT2 rs602662
- **Gene:** FUT2 (Fucosyltransferase 2)
- **Variant Name:** rs602662 G→A (Trp154Ser)
- **Risk Allele:** A
- **Trait/Condition:** Reduced B12 absorption, elevated homocysteine risk
- **Evidence Level:** Strong (GWAS)
- **PMID:** 18193044
- **Effect Size:** ~10% lower B12 in AA genotype
- **Description:** Affects gut microbiota composition and intrinsic factor binding, indirectly influencing B12 bioavailability. AA carriers show ~0.2 pg/mL lower B12 levels (not deficient but lower end). May benefit from B12 fortification/supplementation.

### Iron Metabolism

#### Hemochromatosis (HFE) rs1800562
- **Gene:** HFE (Hemochromatosis gene)
- **Variant Name:** rs1800562 G→A (Cys282Tyr)
- **Risk Allele:** A (HFE C282Y homozygotes at risk)
- **Trait/Condition:** Hereditary hemochromatosis, iron overload
- **Evidence Level:** Strong (clinical validity)
- **Inheritance Pattern:** Autosomal recessive (requires two mutant alleles)
- **Penetrance:** ~10% (homozygotes show phenotype)
- **Description:** Most common cause of hereditary hemochromatosis in Caucasians (~1 in 300 homozygous). Homozygotes at risk for iron overload, liver cirrhosis, heart disease. Heterozygotes typically unaffected. Population screening valuable in high-risk ancestry groups.

### Caffeine Metabolism

#### CYP1A2 rs762551
- **Gene:** CYP1A2
- **Variant Name:** rs762551 A→C (regulatory variant)
- **Status Allele:** Slow metabolizer (C-allele)
- **Trait/Condition:** Caffeine metabolism rate
- **Evidence Level:** Strong (pharmacokinetic studies)
- **Prevalence:** ~50% (both alleles common)
- **Description:** C-allele associated with ~50% slower caffeine metabolism. Slow metabolizers (CC) show higher caffeine sensitivity, increased risk of anxiety/sleep issues with coffee consumption. Note: Also listed under Pharmacogenomics as CYP1A2 rs762551.

### Taste Sensitivity

#### TAS2R38 rs713598
- **Gene:** TAS2R38 (Taste receptor type 2 member 38)
- **Variant Name:** rs713598 C→G (Pro49Ala, part of PTC tasting)
- **Risk Allele:** G (non-taster allele)
- **Trait/Condition:** Bitter taste perception (PTC/PROP tasting)
- **Evidence Level:** Strong (taste physiology)
- **Taster Classification:** CC/CG = Taster, GG = Non-taster (~25-30% population)
- **Description:** Determines perception of bitter compounds (PTC, PROP). Tasters perceive bitter cruciferous vegetables more intensely; may consume fewer vegetables. May inform dietary preferences/guidance for vegetable consumption.

### Saturated Fat Response

#### Apolipoprotein A2 (APOA2) rs5082
- **Gene:** APOA2 (Apolipoprotein A-II)
- **Variant Name:** rs5082 C→G (-265 C→G)
- **Risk Allele:** G
- **Trait/Condition:** Saturated fat response (waist circumference increase)
- **Evidence Level:** Moderate (interaction studies)
- **PMID:** 17673718
- **Effect Size:** GG carriers gain more waist circumference (0.5-1kg more) with high saturated fat diet
- **Description:** Gene-diet interaction: G-allele carriers show exaggerated waist circumference increase on high saturated fat diets. Suggests potential benefit of reduced saturated fat for GG genotypes; CC individuals less sensitive to dietary saturated fat.

### Omega-3 Fatty Acid Metabolism

#### FADS1 rs174547
- **Gene:** FADS1 (Fatty acid desaturase 1)
- **Variant Name:** rs174547 T→C
- **Risk Allele:** C (reduced conversion efficiency)
- **Trait/Condition:** Omega-3/Omega-6 fatty acid metabolism
- **Evidence Level:** Moderate (GWAS, pathway analysis)
- **Description:** FADS1 catalyzes rate-limiting step in LC-PUFA synthesis from dietary ALA. C-allele associated with lower EPA/DHA bioconversion. Suggests potential benefit of direct EPA/DHA supplementation (fish oil) vs. relying on ALA conversion (flax). Particularly relevant for vegetarians with C-alleles.

---

## Exercise SNPs

SNPs influencing exercise response phenotypes, muscle fiber composition, and cardiovascular fitness.

### Muscle Fiber Composition

#### ACTN3 rs1815739
- **Gene:** ACTN3 (Alpha-actinin-3)
- **Variant Name:** rs1815739 C→T (R577X, stop codon)
- **Risk Allele:** T (produces stop codon in some populations)
- **Trait/Condition:** Muscle fiber type composition, sprint/power performance
- **Evidence Level:** Strong (longitudinal exercise studies)
- **Athlete Enrichment:** T/T (stop codon) depleted in elite sprinters (~10-20%), enriched in endurance athletes (~30%)
- **PMID:** 10964986
- **Description:** Classic exercise genetics SNP determining fast/slow muscle fiber composition. C-allele enables full-length ACTN3 protein. RR genotype associated with sprint power capacity; XX genotype (from TT) associated with endurance potential. Predicts training response; helps personalize exercise programming.

### Fat Metabolism During Exercise

#### ADRB3 rs4994
- **Gene:** ADRB3 (Adrenergic receptor beta-3)
- **Variant Name:** rs4994 C→T (Trp64Arg)
- **Risk Allele:** T
- **Trait/Condition:** Fat oxidation during exercise, resting metabolic rate
- **Evidence Level:** Moderate (metabolic studies)
- **Effect Size:** T-allele carriers show ~20-30% lower fat oxidation during submaximal exercise
- **Description:** Beta-3 adrenergic receptor; T-allele associated with reduced fat mobilization and lower resting metabolic rate. May show reduced fat loss with aerobic training; responsive to resistance training. Suggests potential benefit of different exercise modality selection.

### Angiotensin-Converting Enzyme (ACE) Variants

#### ACE I/D rs4340
- **Gene:** ACE (Angiotensin-converting enzyme)
- **Variant Name:** rs4340 (part of I/D polymorphism)
- **Risk Allele:** D (deletion allele)
- **Trait/Condition:** ACE activity level, endurance performance
- **Evidence Level:** Moderate (athletic performance studies)
- **Description:** Insertion/Deletion polymorphism (indel); D-allele produces longer mRNA and higher ACE expression. II individuals show better endurance capacity; DD individuals show better sprint performance. Works synergistically with ACTN3 for exercise phenotype prediction.

#### ACE I/D rs4341
- **Gene:** ACE
- **Variant Name:** rs4341 (part of I/D polymorphism assessment)
- **Description:** Complements rs4340 assessment for complete ACE I/D genotyping. Both SNPs help determine I/D haplotype. Combined interpretation provides ACE activity prediction.

### Aerobic Capacity (VO2max)

#### PPARGC1A rs8192678
- **Gene:** PPARGC1A (Peroxisome proliferator-activated receptor gamma coactivator 1-alpha)
- **Variant Name:** rs8192678 G→A (Gly482Ser)
- **Risk Allele:** A
- **Trait/Condition:** VO2max response to aerobic training, mitochondrial biogenesis
- **Evidence Level:** Moderate (exercise training studies)
- **Effect Size:** G-allele carriers show greater VO2max improvements with endurance training (~5-10% difference)
- **Description:** Master regulator of mitochondrial biogenesis and oxidative metabolism. G-allele shows better aerobic training response and higher baseline VO2max capacity. A-allele carriers may benefit from more intensive aerobic training stimulus or different training protocols.

---

## Deep Risk Extended Panels

These sections detail expanded SNP panels for specific disease pathways, providing comprehensive assessment beyond core SNPs.

### Lipid Metabolism Panel (~20 SNPs)

#### LDLR (LDL Receptor)
- **Gene:** LDLR
- **Key SNPs:** Multiple variants across gene (promoter, exon regions)
- **Trait/Condition:** LDL cholesterol levels, familial hypercholesterolemia
- **Evidence Level:** Strong
- **Description:** Rate-limiting receptor for LDL clearance. Loss-of-function mutations cause familial hypercholesterolemia. Common variants explain ~2-3% of LDL variation. Responsive to statins; heterozygotes show 50% higher LDL.

#### APOB (Apolipoprotein B)
- **Gene:** APOB
- **Key SNPs:** rs693 (Arg3500Gln common variant)
- **Trait/Condition:** LDL cholesterol, familial ligand-defective apoB-100
- **Evidence Level:** Strong
- **Description:** Structural apolipoprotein in LDL; mutations in functional domains impair receptor binding. APOB R3500Q is common variant affecting LDL levels. Critical for comprehensive lipoprotein assessment.

#### PCSK9 (Proprotein convertase subtilisin/kexin type 9)
- **Gene:** PCSK9
- **Key SNPs:** Multiple loss and gain-of-function variants
- **Trait/Condition:** LDL cholesterol regulation, familial hypercholesterolemia
- **Evidence Level:** Strong (therapeutic target)
- **Description:** Degrades LDL receptors; loss-of-function variants lower LDL dramatically. Gain-of-function mutations cause familial hypercholesterolemia. PCSK9 inhibitors (evolocumab, alirocumab) target this pathway.

#### HMGCR (HMG-CoA Reductase)
- **Gene:** HMGCR
- **Trait/Condition:** LDL cholesterol, statin response
- **Evidence Level:** Moderate-Strong (GWAS, statin studies)
- **Description:** Rate-limiting enzyme in cholesterol synthesis; statin target. Variants influence baseline LDL and statin response magnitude. SLCO1B1 interaction important for statin metabolism.

#### CETP (Cholesteryl Ester Transfer Protein)
- **Gene:** CETP
- **Key SNPs:** rs3764261 and others
- **Trait/Condition:** HDL cholesterol levels
- **Evidence Level:** Strong
- **Description:** Transfers cholesterol esters to VLDL/LDL; loss-of-function variants increase HDL. Showed paradoxical lack of benefit in clinical trials despite HDL elevation, suggesting HDL quality matters more than quantity.

#### Lipoprotein Lipase (LPL)
- **Gene:** LPL
- **Trait/Condition:** Triglyceride metabolism, HDL cholesterol
- **Evidence Level:** Moderate-Strong
- **Description:** Hydrolyzes triglycerides from chylomicrons and VLDL. Variants affect triglyceride and HDL levels. Loss-of-function mutations cause severe hypertriglyceridemia.

#### APOA5 (Apolipoprotein A-V)
- **Gene:** APOA5
- **Key SNPs:** rs662799
- **Trait/Condition:** Triglyceride levels
- **Evidence Level:** Strong
- **Effect Size:** rs662799 shows strong triglyceride associations
- **Description:** Component of HDL; strong triglyceride regulator. Variants influence baseline triglycerides and response to fibrate therapy.

#### APOE (Apolipoprotein E)
- **Gene:** APOE
- **SNPs:** rs429358, rs7412 (define ε2/ε3/ε4 alleles)
- **Trait/Condition:** LDL cholesterol, triglycerides, Alzheimer's disease
- **Evidence Level:** Strong
- **Description:** See Health Risk SNPs section for APOE detailed information. APOE4 associated with higher LDL; APOE2 with lower LDL and higher triglycerides.

#### Angiopoietin-like 3 (ANGPTL3)
- **Gene:** ANGPTL3
- **Trait/Condition:** Triglyceride and LDL metabolism
- **Evidence Level:** Moderate-Strong
- **Description:** Inhibits lipoprotein lipase. Loss-of-function variants lower both triglycerides and LDL. Evinacumab (ANGPTL3 inhibitor) developed for severe hypertriglyceridemia.

#### SORT1 (Sortilin 1)
- **Gene:** SORT1
- **Key SNPs:** rs646776
- **Trait/Condition:** LDL cholesterol, CAD risk
- **Evidence Level:** Strong (GWAS)
- **Description:** Intracellular trafficking protein affecting APOB secretion. rs646776 associated with ~5-10 mg/dL LDL variation and CAD risk independent of lipid levels.

#### ABCA1 (ATP-binding cassette transporter A1)
- **Gene:** ABCA1
- **Trait/Condition:** HDL cholesterol, reverse cholesterol transport
- **Evidence Level:** Strong
- **Description:** Critical for HDL synthesis; loss-of-function causes Tangier disease (severe HDL deficiency). Common variants influence HDL levels.

#### FADS1 (Fatty acid desaturase 1)
- **Gene:** FADS1
- **Key SNPs:** rs174547 and others
- **Trait/Condition:** Lipid composition, PUFA levels
- **Evidence Level:** Strong
- **Description:** See Nutrition & Metabolism section. Affects LC-PUFA synthesis with secondary lipid metabolism effects.

---

### Coronary Artery Disease / Atherosclerosis Panel (~15 SNPs)

#### 9p21.3 Locus
- **SNPs:** rs1333049, rs10757274
- **Gene Region:** CDKN2A/2B
- **Trait/Condition:** Coronary artery disease, myocardial infarction
- **Evidence Level:** Strong
- **Description:** See Health Risk SNPs section for detailed information. Strongest common genetic signal for CAD.

#### MTHFR (Methylenetetrahydrofolate Reductase)
- **SNPs:** rs1801133
- **Trait/Condition:** Homocysteine metabolism, CAD risk
- **Evidence Level:** Moderate
- **Description:** See Health Risk SNPs section. Homocysteine is independent CAD risk factor; MTHFR variants influence levels.

#### Lipoprotein(a) (LPA)
- **Gene:** LPA
- **Key SNPs:** rs6417340, rs3798220
- **Trait/Condition:** Lipoprotein(a) levels, CAD, thrombosis risk
- **Evidence Level:** Strong (genetic studies)
- **Effect Size:** Strong genetic determinant of Lp(a) (~70% heritability)
- **Description:** Lp(a) is independent CAD risk factor. Genetic variants explain most Lp(a) variation. No lifestyle modification effective for Lp(a); targets for novel therapies under development.

#### Coagulation Factors (F5, F2)
- **SNPs:** rs6025 (Factor V Leiden), rs1799963 (Prothrombin)
- **Trait/Condition:** Thrombosis, CAD, stent thrombosis risk
- **Evidence Level:** Strong
- **Description:** See Health Risk SNPs section. Both thrombophilia variants increase CAD and stent thrombosis risk.

#### C-Reactive Protein (CRP)
- **Gene:** CRP
- **Key SNPs:** rs3091244, rs1130864
- **Trait/Condition:** Inflammation, CAD risk
- **Evidence Level:** Moderate
- **Description:** Inflammatory marker; genetic variants influence baseline CRP levels. CRP shows independent CAD prediction even with APOE/LDLR adjustment.

#### Interleukin-6 (IL6)
- **Gene:** IL6
- **Key SNPs:** rs1800795 (-174G/C)
- **Trait/Condition:** Inflammatory response, CAD risk
- **Evidence Level:** Moderate
- **Description:** IL6 involved in vascular inflammation. Variants affect baseline IL6 levels and inflammatory response.

#### Angiotensinogen (AGT)
- **Gene:** AGT
- **Key SNPs:** rs699 (M235T)
- **Trait/Condition:** Blood pressure, CAD risk
- **Evidence Level:** Moderate
- **Description:** Part of renin-angiotensin system. M235T variant influences blood pressure and CAD risk; ACE inhibitor/ARB response may vary by genotype.

#### Angiotensin-Converting Enzyme (ACE)
- **Gene:** ACE
- **SNPs:** rs4340, rs4341 (I/D polymorphism)
- **Trait/Condition:** ACE activity, blood pressure, CAD risk
- **Evidence Level:** Moderate
- **Description:** See Exercise SNPs section for detailed ACE information. D-allele associated with higher ACE activity, blood pressure, and CAD risk.

#### Angiotensin II Receptor Type 1 (AGTR1)
- **Gene:** AGTR1
- **Key SNPs:** rs5186 (A1166C)
- **Trait/Condition:** Blood pressure response, CAD risk
- **Evidence Level:** Moderate
- **Description:** AGTR1 mediates angiotensin II effects. A1166C associated with enhanced vascular responsiveness and higher blood pressure in some populations.

---

### Uric Acid / Gout Panel (~10 SNPs)

#### SLC2A9 (Glucose Transporter 9)
- **Gene:** SLC2A9
- **Key SNPs:** rs505802, rs11722228, rs6855911
- **Trait/Condition:** Uric acid levels, gout
- **Evidence Level:** Strong (largest GWAS effects)
- **PMID:** 18391955
- **Effect Size:** rs505802 C-allele ~0.5 mg/dL higher uric acid per allele
- **Description:** Primary renal urate transporter. Multiple independent GWAS signals. Most important genetic regulator of serum uric acid.

#### ABCG2 (ATP-binding Cassette Transporter G2)
- **Gene:** ABCG2
- **Key SNPs:** rs2231142 (Gln141Lys)
- **Trait/Condition:** Uric acid excretion, gout
- **Evidence Level:** Strong
- **PMID:** 18391955
- **Effect Size:** T-allele ~0.6 mg/dL higher uric acid
- **Description:** See Health Risk SNPs section. Second strongest genetic determinant of gout after SLC2A9.

#### SLC22A12 (Urate Transporter 1 / URAT1)
- **Gene:** SLC22A12
- **Key SNPs:** rs505802, rs13179870
- **Trait/Condition:** Uric acid reabsorption, gout
- **Evidence Level:** Strong
- **Description:** Primary renal urate reabsorber; opposite function to SLC2A9. Loss-of-function mutations cause renal hypouricemia but also gout protection. Target for uricosuric medications.

#### SLC17A1 (Urate Transporter 1)
- **Gene:** SLC17A1
- **Trait/Condition:** Uric acid secretion
- **Evidence Level:** Moderate
- **Description:** Secondary renal urate secretion pathway. Contributes to overall uric acid handling.

#### SLC22A11 (Organic Anion Transporter 4)
- **Gene:** SLC22A11
- **Trait/Condition:** Uric acid transport
- **Evidence Level:** Moderate
- **Description:** Secondary urate transporter involved in renal excretion.

#### Glucokinase Regulator (GCKR)
- **Gene:** GCKR
- **Key SNPs:** rs780094
- **Trait/Condition:** Uric acid levels, glucose metabolism
- **Evidence Level:** Strong (pleiotropic)
- **Effect Size:** ~0.3 mg/dL uric acid increase per risk allele
- **Description:** Metabolic regulator affecting glucose, lipid, and uric acid metabolism. Pleiotropic GWAS hit.

#### PDZK1 (PDZ Domain Containing 1)
- **Gene:** PDZK1
- **Trait/Condition:** Uric acid handling
- **Evidence Level:** Moderate
- **Description:** Scaffolding protein; variations affect urate transporter complex function.

---

### Type 2 Diabetes Extended Panel (~10 SNPs)

#### Core Diabetes SNPs
- **SNPs:** TCF7L2 rs7903146, KCNJ11 rs5219, SLC30A8 rs13266634, PPARG rs1801282
- **Description:** See Health Risk SNPs section for detailed information.

#### GCKR (Glucokinase Regulator)
- **Gene:** GCKR
- **Key SNPs:** rs780094
- **Trait/Condition:** Fasting glucose, T2D risk
- **Evidence Level:** Strong
- **Effect Size:** ~0.02 mmol/L fasting glucose increase per risk allele
- **Description:** Regulates glucokinase activity; affects glucose sensing and hepatic glucose output.

#### MTNR1B (Melatonin Receptor 1B)
- **Gene:** MTNR1B
- **Key SNPs:** rs10830963
- **Trait/Condition:** Fasting glucose, T2D risk
- **Evidence Level:** Strong (GWAS)
- **Effect Size:** ~0.03 mmol/L fasting glucose increase per G-allele
- **Description:** Melatonin signaling affects beta-cell function. G-allele increases T2D risk primarily through elevated fasting glucose.

#### IGF2BP2 (Insulin-like Growth Factor 2 mRNA Binding Protein 2)
- **Gene:** IGF2BP2
- **Key SNPs:** rs4402960
- **Trait/Condition:** T2D risk
- **Evidence Level:** Strong (GWAS)
- **Effect Size:** OR ~1.10 per T-allele
- **Description:** Glucose/insulin metabolism regulator. GWAS-identified variant with consistent replication.

#### CDKN2A/2B (Cyclin-dependent Kinase Inhibitor 2A/2B)
- **Gene:** CDKN2A/2B
- **Key SNPs:** rs10811661
- **Trait/Condition:** T2D risk, CAD risk (pleiotropic)
- **Evidence Level:** Strong
- **Effect Size:** OR ~1.23 per risk allele
- **Description:** Cell cycle regulation. Same locus contains 9p21.3 CAD signal. Shows pleiotropy across metabolic diseases.

#### JAZF1 (JAZF Zinc Finger 1)
- **Gene:** JAZF1
- **Key SNPs:** rs864745
- **Trait/Condition:** T2D risk
- **Evidence Level:** Strong (GWAS)
- **Effect Size:** OR ~1.13 per T-allele
- **Description:** Transcription factor involved in metabolic regulation. GWAS-identified.

---

### Statin Pharmacogenomics Panel (~5 SNPs)

#### SLCO1B1 (Statin Transporter)
- **SNPs:** rs4149056 (*5 allele)
- **Description:** See Pharmacogenomics section for detailed information. Primary determinant of statin myopathy risk.

#### VKORC1 (Vitamin K Epoxide Reductase)
- **SNPs:** rs9923231
- **Trait/Condition:** Statin-warfarin interaction risk
- **Evidence Level:** Moderate
- **Description:** When statins combined with warfarin, VKORC1 status affects warfarin metabolism. Interaction amplifies warfarin sensitivity.

#### CYP2C19 (Statin Metabolism)
- **SNPs:** rs4244285, rs4986893, rs12248560
- **Trait/Condition:** Some statin metabolism (particularly simvastatin)
- **Evidence Level:** Moderate
- **Description:** CYP2C19 metabolizes some statins. Interaction with SLCO1B1 important for overall statin response. See Pharmacogenomics section.

#### HMGCR (Statin Target Enzyme)
- **Gene:** HMGCR
- **Trait/Condition:** Statin efficacy, LDL-lowering response
- **Evidence Level:** Moderate
- **Description:** Statin directly inhibits HMGCR. Variants in HMGCR regulatory regions may influence statin response magnitude and baseline LDL.

---

## Special Genotyping Cases

Several SNPs and genetic variants require special interpretation protocols due to complex inheritance patterns, epistatic interactions, or multiple-allele systems.

### APOE Typing (Two-SNP System)

APOE genotyping requires **both** rs429358 and rs7412 because:

1. **rs429358 (Arg112Cys):** Defines ε4 allele
   - C = normal
   - T = defines ε4 allele

2. **rs7412 (Arg158Cys):** Defines ε2 allele
   - C = normal
   - T = defines ε2 allele

**Haplotype Interpretation:**

| rs429358 | rs7412 | Genotype | APOE Status | AD Risk |
|----------|--------|----------|-----------|---------|
| C/C | C/C | CC/CC | ε3/ε3 (wild-type) | Baseline |
| C/T | C/C | CC/TC | ε3/ε4 (carrier) | 3-5x increased |
| T/T | C/C | TC/TC | ε4/ε4 (homozygote) | 8-12x increased |
| C/C | C/T | CC/CT | ε2/ε3 | Protective |
| C/T | C/T | CC/TT | ε2/ε4 (rare) | Intermediate |
| C/C | T/T | CT/CT | ε2/ε2 | Protective |

**Clinical Implications:**
- ε4 carriers should prioritize cognitive engagement, cardiovascular health, sleep quality
- ε2 carriers have lower AD risk but may show different health profiles
- ε3/ε3 is baseline reference
- APOE status should trigger lifestyle counseling; genetic testing for APOE requires informed consent due to clinical significance

### CYP2C19 Metabolizer Status (Three-SNP System)

CYP2C19 phenotype requires integration of rs4244285 (*2), rs4986893 (*3), and rs12248560 (*17):

**Phenotype Classification:**
- **Poor Metabolizer (PM):** Two loss-of-function alleles (*2/*2, *2/*3, *3/*3)
  - 2-5% of Caucasians, 5-10% of East Asians
  - Clinical action: Significant dose reduction, consider alternative drugs

- **Intermediate Metabolizer (IM):** One loss-of-function + one normal (*1/*2, *1/*3)
  - 35-45% of Caucasians, 30-40% of East Asians
  - Clinical action: Consider dose reduction (especially clopidogrel)

- **Extensive Metabolizer (EM):** Two normal alleles (*1/*1)
  - 40-50% of all populations
  - Clinical action: Standard dosing

- **Rapid Metabolizer (RM):** One normal + one gain-of-function (*1/*17)
  - 20-30% of Caucasians
  - Clinical action: May need higher doses

- **Ultra-Rapid Metabolizer (UM):** Two gain-of-function alleles (*17/*17)
  - 2-5% of populations
  - Clinical action: Higher doses or alternative therapy

**Clopidogrel Response (Most Clinically Relevant):**
- **Poor/Intermediate metabolizers:** ~50% reduction in antiplatelet effect, higher stent thrombosis risk
- **Ultra-rapid metabolizers:** Enhanced effect but no major clinical concern
- **FDA label:** Consider prasugrel or ticagrelor in CYP2C19 loss-of-function carriers requiring dual antiplatelet therapy

### MTHFR Compound Heterozygosity & Haplotype Interpretation

MTHFR genotyping is complicated by:

1. **Reduced activity levels (rs1801133 C>T alone):**
   - CC: Normal activity (100%)
   - CT: Heterozygous, ~65% activity
   - TT: Homozygous, ~30% activity

2. **Compound Heterozygosity Concern (rs1801133 + other MTHFR variants):**
   - Two different loss-of-function mutations on separate alleles
   - May show more severe activity reduction than expected
   - Rare but relevant in populations with multiple MTHFR variants

3. **Clinical Considerations:**
   - Even TT genotype rarely causes severe deficiency (~30% activity usually adequate)
   - Symptomatic MTHFR deficiency is rare without other genetic factors
   - Supplementation (methylfolate, B12, B6) recommended for TT individuals, especially periconceptually
   - Warfarin interaction: TT individuals may show enhanced sensitivity (separate from CYP2C9/VKORC1)
   - Folic acid supplementation may be less effective in TT individuals (use methylfolate)

**Clinical Management:**
- TT genotype individuals: Preconception folic acid/methylfolate, B-vitamin support
- Consider MTHFR status when counseling on methylation capacity
- Not typically standalone indication for supplementation unless symptomatic or planning pregnancy

---

## Evidence Levels & Data Quality

### Definitions

**Strong Evidence:**
- Large, well-powered GWAS studies (N>50,000)
- Consistent replication across independent populations
- Functional studies confirming biological mechanism
- Clinical utility established (FDA guidance, clinical validity)
- Examples: TCF7L2, BRCA1/2, APOE, Factor V Leiden

**Moderate Evidence:**
- GWAS-identified variants with consistent replication
- Moderate effect sizes (OR 1.10-1.50)
- Biological plausibility but limited functional validation
- Population-specific findings
- Examples: SLC2A9, MTHFR, many exercise SNPs

**Preliminary Evidence:**
- Limited replication studies
- Small effect sizes
- Population-specific findings not yet replicated
- Functional mechanisms unclear
- Require further validation

### Quality Notes

- **Population Specificity:** Many SNP associations vary by ancestry. Frequencies and effect sizes may differ in non-European ancestry populations. This database uses European ancestry prevalence but notes ancestry-specific variants.

- **Allele Frequency Considerations:** Rare variants in one population may be common in another (e.g., ALDH2 rs671 in East Asian vs. European populations).

- **Pleiotropy:** Many SNPs affect multiple traits (e.g., APOE affects AD and lipids; GCKR affects uric acid and glucose). Multiple pathways may be relevant.

- **Gene-Environment Interaction:** Genetic risk requires environmental exposure. Examples: APOE4 + low cognitive activity; alcohol + ALDH2 deficiency; saturated fat + APOA2 genotype.

- **Incomplete Penetrance:** Genetic risk factors don't always cause phenotype. Clinical presentation depends on genetic background, environment, and stochastic factors.

---

## Additional Resources

- **Programmatic Access:** JSON-formatted SNP data available in `scripts/snp_data.json`
- **Database Updates:** Refer to NCBI dbSNP, PharmGKB, ClinVar for latest variants and reclassifications
- **Clinical Guidelines:** PharmGKB, CPIC, ACOG guidelines for pharmacogenomic interpretation
- **Ancestry Considerations:** gnomAD, 1000 Genomes for population-specific allele frequencies

---

**Document Version History:**
- v1.0 (2026-03-18): Initial comprehensive reference compilation

