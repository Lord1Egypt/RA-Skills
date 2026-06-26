# Pediatrics Pediatrics-PMPH-10edition
<div align="center">

> *「21st Century Medical Student Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical skill handbook based on "Pediatrics" (PMPH 10th Edition) — 184 Core Pediatric Clinical Skills
<br>
<br>

Why struggle through an entire textbook?<br>
Just ask a question, and instantly find the solution from the textbook.

<br>

**Other Languages:**

[中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## About This Project

This project systematically integrates core domains of pediatrics, including neonatology, child growth and development, infectious disease prevention and control, genetic and metabolic disease diagnosis and treatment, and emergency and critical care. It covers **184 key clinical skills** organized into **15 categories**.

**Target Audience**: Pediatricians, Medical Students, Neonatal Care Teams, Public Health Workers, Resident Training Participants

**Reference Textbook**: "Pediatrics" (People's Medical Publishing House, 10th Edition)

**⚠️Risk⚠️**: High-risk clinical treatments, procedures, and dosage guidance may not be suitable for general installation or unsupervised use.

**Mitigation**: Only for use by qualified pediatricians, neonatologists, pediatric intensivists, or supervised medical education environments. Require clinician review before acting on output.

**⚠️Risk⚠️**: Guidance may conflict with current local guidelines, institutional protocols, or patient-specific contraindications.

**Mitigation**: Verify that plans, procedures, thresholds, and follow-up recommendations align with the latest local standards and institutional policies before use.

**⚠️Risk⚠️**: Emergency procedures, invasive interventions, neonatal resuscitation, pediatric drug dosage calculations, and sensitive developmental/behavioral topics may compromise patient safety or privacy if handled too casually.

**Mitigation**: Add explicit warnings for these scenarios, redirect emergencies to emergency/ICU care, and restrict access to users with appropriate clinical or supervised educational needs.

## Project Structure

```
Pediatrics-PMPH-10edition/
├── SKILL.md                  # Core config — 184-skill registry
├── README.md                 # This document — project overview & usage guide
├── <skill-name>/             # Detailed skill definitions
│   └── SKILL.md              #   Skill details (when to use, steps, references)
├── scripts/                  # Executable scripts
│   └── .gitkeep
├── config/                   # Configuration files
│   └── .gitkeep
└── tests/                    # Validation & tests
    └── .gitkeep
```

## Skill Categories

| Category | Skills | Description |
|----------|--------|-------------|
| 👶 Neonatology & Perinatal Medicine | 18 | Jaundice, RDS, hemolysis, hemorrhage, NEC, ROP, BPD |
| 📏 Growth, Development & Nutrition | 18 | Growth assessment, complementary feeding, sleep, micronutrients |
| 💉 Immunization & Infectious Disease Control | 20 | Vaccination schedule, measles, HFMD, TB, Kawasaki disease |
| 🫁 Respiratory Diseases | 12 | Pneumonia, asthma, mycoplasma, bronchoscopy, blood gas analysis |
| ❤️ Cardiovascular Diseases | 10 | CHD classification, heart failure, myocarditis, Duke criteria |
| 🫃 Digestive & Hepatobiliary Diseases | 12 | Intussusception, Hirschsprung, IBD, biliary atresia, GERD |
| 🫘 Urinary & Renal Diseases | 10 | Hematuria, nephritis, nephrotic syndrome, AKI, RTA |
| ⚖️ Endocrine & Metabolic Diseases | 13 | GHD, precocious puberty, hypothyroidism, diabetes, DKA |
| 🩸 Hematology & Oncology | 9 | ITP, AIHA, hemophilia, thalassemia, LCH |
| 🧠 Neurology & Behavioral Disorders | 12 | Epilepsy, febrile seizures, ADHD, GBS, myasthenia gravis |
| 🚑 Emergency & Critical Care | 10 | CPR, trauma, drowning, respiratory failure, dehydration |
| 🧬 Genetic & Congenital Diseases | 7 | Three-level prevention, genetic classification, CHARGE, DMD/BMD |
| 🔬 Laboratory & Diagnostic Imaging | 11 | CSF, PKU, CAH, rickets, MRI, ultrasound |
| 📚 Textbook & Evidence-Based Medicine | 7 | Textbook authority assessment, revision principles, literature |
| 🏋️ Comprehensive Health Management | 9 | Exercise, diet, immune system, drug dosage, physical exam |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install pediatrics-pmph-10edition
```

Prompt:
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Pediatrics-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Find a Skill

```bash
# Search by keyword
bash scripts/skill-search.sh neonatal jaundice

# Generate skill report
bash scripts/skill-report.sh
```

### How to Use

Each skill contains four sections:
1. **When to Use** — Clinical scenarios that trigger this skill
2. **Execution Steps** — Standardized operating procedure
3. **Cautions** — Contraindications and warnings
4. **References** — Supplementary materials

### Query Strategies

#### 1. **Concept**

Question:
```bash
Concept of physiological neonatal jaundice
```

Answer：
```bash
## Concept of Physiological Neonatal Jaundice

**Physiological neonatal jaundice** is a transient elevation of serum unconjugated bilirubin in newborns due to the unique characteristics of bilirubin metabolism. It is a benign, self-limiting process that typically resolves without intervention.

### Diagnostic Criteria

| Parameter | Term Infant | Preterm Infant |
|-----------|-------------|----------------|
| Onset | Day 2–3 after birth | Day 3–5 after birth |
| Peak | Day 4–5 after birth | Day 5–7 after birth |
| Resolution | Day 5–7 after birth | Day 7–9 after birth |
| Peak bilirubin | < 221 μmol/L (12.9 mg/dL) | < 256 μmol/L (15 mg/dL) |
| Daily increase | < 85 μmol/L (5 mg/dL) | < 85 μmol/L (5 mg/dL) |

### Key Differential Diagnosis

- **Physiological jaundice**: Meets time window and thresholds; infant appears well
- **Pathological jaundice**: Onset < 24h, excessive levels, prolonged course, rapid daily rise, or elevated direct bilirubin
- **Breast milk jaundice**: Onset at 1 week, peaks at 2–3 weeks; significant drop after 3-day breastfeeding pause

### Management

No specific treatment required. Ensure adequate feeding to promote meconium passage. If TSB approaches intervention threshold, initiate phototherapy assessment.

---

**Related skill:** [Neonatal Jaundice Risk Assessment & Physiological Jaundice Diagnosis](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md)
```

#### 2. **Clinical Case Analysis**

Question:
```bash
A full-term infant, 38 weeks gestation, vaginal delivery, birth weight 3.2 kg. Skin jaundice appeared within 24 hours of birth and rapidly worsened. At 36 hours of life, TSB measured 15 mg/dL, predominantly unconjugated. Maternal blood type: O Rh(+); Infant blood type: A Rh(+). What is the most likely diagnosis?
```

Answer：
```bash
## Case Analysis

**Most likely diagnosis: ABO hemolytic disease of the newborn (ABO-HDN)**

### Diagnostic Evidence

| Clinical Feature | Significance |
|-----------------|-------------|
| **Jaundice within 24 hours of birth** | Pathological jaundice — onset too early |
| **TSB 15 mg/dL (257 μmol/L)** | Significantly above physiological range (peak < 12.9 mg/dL) |
| **Predominantly unconjugated bilirubin** | Consistent with hemolytic jaundice |
| **Mother O + Infant A** | Most common ABO-HDN combination (maternal anti-A IgG crosses placenta) |
| **Coombs test positive** | Definitive evidence of immune-mediated hemolysis |

### Management

1. **Initiate phototherapy immediately** — high-intensity blue light (425–475 nm)
2. **Monitor TSB q4–6h** — assess need for exchange transfusion
3. **CBC + reticulocyte count** — evaluate anemia severity
4. **IVIG 0.5–1 g/kg** — interrupt hemolysis
5. **Exchange transfusion** — if TSB ≥ exchange threshold or phototherapy fails

---

**Related skills:** [Neonatal Jaundice Risk Assessment & Diagnosis](neonatal-jaundice-risk-assessment-diagnosis/SKILL.md) · [Bilirubin Encephalopathy Staging & Diagnosis](bilirubin-encephalopathy-staging-and-diagnosis/SKILL.md)
```

#### 3. **Exam Question**

Question:
```bash
An 8-month-old infant presents with fever for 3 days. A rash appears after defervescence. The most likely diagnosis is:
A. Measles
B. Rubella
C. Roseola infantum (Exanthem subitum)
D. Scarlet fever
E. Varicella (Chickenpox)
```

Answer：
```bash
**Answer: C. Roseola infantum (Exanthem subitum)**

### Differential Diagnosis

| Disease | Fever-Rash Relationship | Rash Characteristics | Other Features |
|---------|------------------------|---------------------|----------------|
| A. Measles | Rash **during** fever | Dark red maculopapular, cephalocaudal spread | Koplik spots, coryza |
| B. Rubella | Rash **during** fever | Pink maculopapular, face → entire body | Post-auricular/occipital lymphadenopathy |
| **✅ C. Roseola** | Rash **after** defervescence | Rose-colored maculopapular, trunk → face → limbs, resolves in 1–2 days | High fever (39–40°C), otherwise well |
| D. Scarlet fever | Rash **during** fever | Pinpoint erythematous, Pastia lines | Strawberry tongue, pharyngitis |
| E. Varicella | Rash **during** fever | Centrifugal "four generations" lesions: macule → papule → vesicle → crust | Intense pruritus |

### Why C?

Key clues in the question:
- **8 months old** → most common age for roseola (6–18 months)
- **Fever 3 days, rash after defervescence** → **"Rash after fever resolves" is the classic feature of roseola**, distinct from other exanthematous diseases where rash appears during fever
- Rose-colored maculopapular rash, trunk first then spreading → matches roseola eruption pattern

### Management

Self-limiting; no specific antiviral therapy. Supportive care:
- Antipyretics for high fever (physical cooling, acetaminophen/ibuprofen)
- Ensure adequate fluid intake
- Monitor for febrile seizures

---

**Related skill:** [Pediatric Infectious Disease Diagnosis & Prevention](er-tong-chuan-ran-bing-zhen-duan-yu-fang-zhi/SKILL.md)
```

## About the Author

**Xiaolvlyu (https://xllgreen.github.io)** — Medical Student at Jiujiang University College of Clinical Medicine · Tech Enthusiast

## Technical Support
<br>
PDF2App Project: https://pdf2app.cn
<br>
Microsoft Visual Studio Code: https://code.visualstudio.com/
<br>
Claude Code for VS Code: https://claude.com/
© 2026 Anthropic PBC
<br>
<br>
<img src="https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_1920" width="130px">
<br>DeepSeek API: https://platform.deepseek.com/
© 2026 Hangzhou DeepSeek Artificial Intelligence Basic Technology Research Co., Ltd. All Rights Reserved
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## License

This project is based on "Pediatrics" (PMPH 10th Edition) and is provided for educational reference only.

## Star History

<a href="https://www.star-history.com/#">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=&type=date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=&type=date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=&type=date" />
 </picture>
</a>
