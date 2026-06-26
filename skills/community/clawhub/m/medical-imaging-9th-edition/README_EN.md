# Medical Imaging-9thEdition
<div align="center">

> *「21st Century Medical Imaging Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical skills handbook based on the 9th edition of "Medical Imaging" (People's Medical Publishing House) — 136 core skills in medical imaging diagnosis and interventional therapy
<br>
<br>

Why read a whole textbook?<br>
Just ask a question, and get solutions directly from the textbook

<br>

**Other Languages / 其他语言:**

[中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Introduction

This project systematically integrates core domains of medical imaging diagnosis, interventional radiology, AI-assisted analysis, and multimodal imaging technique selection, covering **136 key clinical skills** organized into 13 categories.

**Target Audience**: Radiologists, clinicians of all specialties, medical students, interventional radiology teams, medical educators

**Reference Textbook**: *Medical Imaging*, 9th Edition, People's Medical Publishing House (National Health Commission "14th Five-Year Plan" textbook)

**⚠️ Risk ⚠️**: This skill set covers imaging diagnosis, contrast agent use, interventional therapy indications, and report interpretation, which could be misused as independent diagnostic or treatment decisions.

Mitigation: Use outputs only as educational or clinician-reviewed reference material, and verify recommendations against current official guidelines, local protocols, and qualified radiology specialists.

**⚠️ Risk ⚠️**: Source content does not consistently enforce clinician-only safety boundaries.

Mitigation: Deploy system-level medical safety policies requiring escalation to qualified clinicians for diagnosis, treatment decisions, and interventional procedures.

## Project Structure

```
Medical-Imaging-9thEdition/
├── SKILL.md              # Core configuration — 136-skill registry
├── README.md             # This document — project description and usage guide
├── README_EN.md          # English documentation
├── <skill-name>/         # Detailed definitions for each skill
│   └── SKILL.md          #   Skill details (when to use, execution steps, notes)
├── scripts/              # Executable tool scripts
├── config/               # Configuration files
├── tests/                # Verification and testing
└── assets/               # Static resources (images, etc.)
```

## Skills Overview

| Category | Skills | Description |
|----------|--------|-------------|
| 🏗️ Imaging Fundamentals & Technology | 9 | X-ray, CT, MRI, ultrasound principles, post-processing, and safety |
| 🤖 AI & Digital Resources | 5 | AI-assisted analysis, smart workflows, digital textbook resources |
| 📚 Textbook & Curriculum | 3 | Textbook verification, revision principles, curriculum reform |
| 🧠 Central Nervous System | 7 | Head trauma CT/MRI, spinal cord MRI, demyelinating diseases |
| 👁️ Head & Neck | 4 | Orbital, parotid, and mandibular lesion diagnosis |
| 🫁 Chest & Cardiovascular | 18 | Lung, pleura, mediastinum, and cardiac imaging assessment |
| 🫄 Breast & Gynecology | 8 | Mammography, ovarian tumors, placenta previa, UAE |
| 🫃 Digestive System | 19 | GI tract, hepatobiliary-pancreatic multimodal imaging |
| 🫘 Urinary & Adrenal | 8 | Renal tumors, cystic lesion classification, urinary stones |
| 🦴 Musculoskeletal | 10 | Fracture classification, bone tumors, osteomyelitis, joint diseases |
| 👶 Pediatrics & Congenital | 4 | NRDS grading, DDH measurement, intussusception, rickets |
| 💉 Interventional Radiology | 19 | Vascular access, embolization, stents, ablation, TIPS |
| 📋 Comprehensive Diagnosis | 14 | Diagnostic reasoning, report interpretation, multimodal fusion |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install medical-imaging-9th-edition
```

Prompt:
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "medical-imaging-9th-edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Usage

Each skill contains four sections:
1. **When to Use** — Indications for triggering the skill
2. **Execution Steps** — Standardized operating procedures
3. **Cautions** — Contraindications and warnings
4. **References** — Detailed supplementary materials

### Query Strategies

#### 1. **Concept Query**

Question:
```bash
Bosniak renal cyst classification 2019 criteria
```

Answer:
```bash
## Bosniak Renal Cyst Classification (2019)

| Type | Imaging Features | Malignancy Risk | Management |
|------|-----------------|-----------------|------------|
| **I** | Simple cyst, hairline-thin wall, no septa/calcification/solid components | <1% | Benign, no follow-up |
| **II** | Few (≤3) thin (≤2mm) septa; fine calcification | <5% | Benign, no follow-up |
| **IIF** | Multiple (≥4) thin septa; minimally thickened wall/septa; no enhancing soft tissue | ~10% | Surveillance |
| **III** | One or more enhancing solid components; irregularly thickened (≥4mm) wall/septa | ~55% | Surgical resection |
| **IV** | Clearly enhancing soft tissue components (≥25% of lesion is solid) | >90% | Surgical resection |
```

#### 2. **Differential Diagnosis**

Question:
```bash
60-year-old male, long-term smoker, CT shows right upper lobe lobulated mass with spiculation and ipsilateral hilar lymphadenopathy
```

Answer:
```bash
## Case Analysis

Most Likely Diagnosis: **Peripheral Lung Cancer (squamous cell carcinoma or adenocarcinoma)**

Key Findings:
1. Age 60 + long-term smoking → high-risk profile
2. Lobulated shape + spiculation → malignant growth pattern
3. Ipsilateral hilar lymphadenopathy → regional lymph node involvement

Differential:
- Tuberculoma: satellite lesions, calcification, rim enhancement
- Inflammatory pseudotumor: smoother margins, history of infection
- Lung abscess: cavity with air-fluid level, acute onset

Suggested Next Steps:
1. Contrast-enhanced CT for vascular assessment and mediastinal evaluation
2. PET-CT for systemic staging
3. CT-guided percutaneous biopsy for pathological confirmation
```

#### 3. **Treatment Protocol**

Question:
```bash
Patient develops nausea, vomiting, right upper quadrant pain, and fever after TACE
```

Answer:
```bash
## Post-TACE Chemoembolization Syndrome Management

This is **Chemoembolization Syndrome (CES)** — typically self-limited (3-7 days):

| Symptom | Management | Note |
|---------|-----------|------|
| Fever | Antipyretics (acetaminophen/ibuprofen), cooling | >39°C persistent → rule out infection |
| Pain | WHO analgesic ladder | Avoid NSAIDs in liver patients |
| Nausea/Vomiting | 5-HT₃ antagonists (ondansetron) | Correct fluid/electrolyte balance |
| Hepatoprotection | Glycyrrhizin, glutathione | Monitor LFTs post-procedure |

**Red flags (urgent evaluation needed):**
- Severe progressive pain → hepatic abscess/cholecystitis/pancreatitis
- Fever >39°C with chills → infectious complications
- Increasing ascites, worsening jaundice → acute liver failure
```

## License

This project is based on the 9th edition of *Medical Imaging* (People's Medical Publishing House) and is provided for educational reference only.
