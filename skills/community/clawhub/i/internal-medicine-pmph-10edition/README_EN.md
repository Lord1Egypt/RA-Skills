# Internal Medicine — PMPH 10th Edition
<div align="center">

> *「21st Century Medical Student Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical skills handbook based on *Internal Medicine*, 10th Edition, People's Medical Publishing House — 423 core clinical skills in internal medicine
<br>
<br>
<img src="assets/Internal-Medicine.jpg" width="260px">
<br>

Why slog through an entire textbook?<br>
Just ask a question, and get the solution straight from the textbook.

<br>

**Other Languages:**

[简体中文](README.md) · [日本語](README_JA.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Project Overview

This project systematically integrates core knowledge in internal medicine, covering **15 major categories** — Cardiovascular Diseases, Respiratory Diseases, Digestive Diseases, Endocrine & Metabolic Diseases, Renal Diseases, Hematologic Diseases, Rheumatic & Immunologic Diseases, Infectious Diseases & Tuberculosis, Poisoning & Physical/Chemical Injuries, Oncology & Comprehensive Care, Chronic Disease Management & Tiered Healthcare, Clinical Skills & Procedures, Pharmacotherapy & Safety, Laboratory & Imaging Interpretation, and Educational Resources & Quality Control — totaling **423 key clinical skills**.

**Target Audience**: Internists, general practitioners, emergency physicians, medical students, residents in standardized training

**Reference Textbook**: *Internal Medicine*, 10th Edition, People's Medical Publishing House

**⚠️ Risk ⚠️**: High-risk clinical treatments, procedures, and dosage guidance may not be suitable for unsupervised general installation or use.

**Mitigation**: Intended for qualified clinicians, supervised medical education environments, and requires clinician review before acting on any output.

**⚠️ Risk ⚠️**: Guidance may conflict with current local guidelines, institutional protocols, or patient-specific contraindications.

**Mitigation**: Verify that plans, procedures, thresholds, and follow-up plans conform to the latest local standards and institutional policies before use.

**⚠️ Risk ⚠️**: Invasive procedures in emergencies, chemotherapy protocol adjustments, and sensitive end-of-life decisions could compromise patient safety or privacy if handled too casually.

**Mitigation**: Add explicit warnings for these scenarios, direct emergencies to acute care, and restrict access to users with appropriate clinical or supervised educational needs.

## Project Structure

```
Internal-Medicine-PMPH-10edition/
├── SKILL.md                  # Core configuration — 423-skill registry
├── README.md                 # This document — project description and usage guide
├── <skill-name>/             # Detailed definitions for each skill
│   └── SKILL.md              #   Skill details (indications, steps, references)
├── scripts/                  # Executable utility scripts
│   ├── list-skills.sh        #   Skill keyword search
│   └── build-index.py        #   Skill index generator
├── config/                   # Configuration files
│   └── skills-index.json     #   JSON index of all 423 skills
└── tests/                    # Validation and testing
```

## Skill Categories at a Glance

| Category | Skills | Description |
|----------|--------|-------------|
| ❤️ Cardiovascular Diseases | 56 | Coronary artery disease, heart failure, arrhythmias, cardiomyopathy, hypertension, valvular disease, etc. |
| 🫁 Respiratory Diseases | 45 | Pneumonia, COPD, asthma, pulmonary embolism, interstitial lung disease, pleural disease, etc. |
| 🫃 Digestive Diseases | 50 | Gastritis, peptic ulcers, inflammatory bowel disease, cirrhosis, pancreatitis, ascites, etc. |
| 🧬 Endocrine & Metabolic Diseases | 46 | Diabetes, thyroid disease, pituitary-adrenal disorders, gout, electrolyte disturbances, etc. |
| 🫘 Renal Diseases | 29 | Glomerulonephritis, renal failure, dialysis, proteinuria, AKI, etc. |
| 🩸 Hematologic Diseases | 37 | Leukemia, anemia, coagulation disorders, multiple myeloma, lymphoma, MDS, etc. |
| 🦿 Rheumatic & Immunologic Diseases | 12 | RA, SLE, Sjögren's syndrome, systemic sclerosis, vasculitis, etc. |
| 🦠 Infectious Diseases & Tuberculosis | 20 | Community-acquired infections, nosocomial infections, tuberculosis, fungal infections, viral hepatitis, etc. |
| 💊 Poisoning & Physical/Chemical Injuries | 15 | Drug poisoning, organic solvent poisoning, carbon monoxide poisoning, heatstroke, drowning, etc. |
| 🎗️ Oncology & Comprehensive Care | 18 | Lung cancer, gastric cancer, colorectal cancer, pancreatic cancer, tumor markers & targeted therapy, etc. |
| 📋 Chronic Disease Management & Tiered Healthcare | 20 | Hypertension tiered management, diabetes follow-up, long-term dyslipidemia management, etc. |
| 🔬 Clinical Skills & Procedures | 25 | Thoracentesis, abdominocentesis, bone marrow aspiration, CPR, defibrillation, etc. |
| 💉 Pharmacotherapy & Safety | 20 | Anticoagulant management, rational antibiotic use, standardized glucocorticoid use, etc. |
| 📡 Laboratory & Imaging Interpretation | 15 | ECG analysis, echocardiography interpretation, blood gas analysis, lab test interpretation, etc. |
| 📚 Educational Resources & Quality Control | 15 | Textbook structure, syllabus review, core exam points, clinical reasoning training, etc. |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install internal-medicine-pmph-10edition
```

Prompt:
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
If the skill asks you to install a third-party package or CLI, verify its source, maintainer, and package contents before running the install command.
Install the skill "Internal-Medicine-PMPH-10edition" (xllgreen/internal-medicine-pmph-10edition) from ClawHub only after those checks pass.
Skill page: https://clawhub.ai/xllgreen/internal-medicine-pmph-10edition
Keep the work scoped to this skill only.
After install, help me finish setup from verified skill metadata.
Use only the metadata you can verify from ClawHub; do not invent missing requirements.
Ask before making any broader environment changes.
```

### Usage After Installation
Instruct the agent as follows:
```bash
Before each response, please consult the relevant medical skill to verify the information.
```

### Searching Skills

```bash
# Search by keyword
bash scripts/list-skills.sh search heart failure

# List all skills
bash scripts/list-skills.sh list
```

### How to Use

Each skill consists of four parts:
1. **Indications** — When to trigger this skill
2. **Procedure** — Standardized operational steps
3. **Precautions** — Contraindications and warnings
4. **References** — Detailed supplementary materials

### Query Strategies

#### 1. **Concept Query**
Question:
```bash
What is the definition of infective endocarditis in internal medicine?
```
Answer:
```bash
Definition from Internal Medicine (10th Edition):
**Infective endocarditis (IE)** is a clinical syndrome characterized by the formation of **vegetations** on the endocardium, heart valves, or adjacent great artery intima, caused by direct hematogenous invasion by pathogenic microorganisms (bacteria, fungi, etc.). Vegetations are composed of platelets, fibrin, pathogenic microorganisms, and inflammatory cells.
Key points:
- **Core pathology**: Microorganisms attach to damaged valve or endocardial surfaces → vegetation formation
- **Predilection sites**: Mitral valve > Aortic valve (predominantly left-sided)
- **Clinical triad**: Fever + Heart murmur + Embolic/vascular phenomena
- **Classification**: Acute vs. subacute by course; native valve IE, prosthetic valve IE, and right-sided IE by valve type
```

#### 2. **Clinical Case Analysis**
Question:
```bash
A 60-year-old female presents with recurrent cough and sputum production for 25 years, palpitations, dyspnea, and intermittent lower extremity edema for 3 years, with recent exacerbation accompanied by chills and fever for 1 week. Examination: T 38°C, tachypnea, cyanosis of the lips, bilateral hyperresonance on chest percussion, moist rales in the middle and lower lung fields, HR 110 bpm, regular rhythm, no murmurs, severe bilateral lower extremity edema. What is the diagnosis?
```
Answer:
```bash
This represents a classic progression of **COPD → Chronic Cor Pulmonale → Right Heart Failure**.
**Complete Diagnosis:**
1. **Acute Exacerbation of Chronic Obstructive Pulmonary Disease (COPD)**
   - Evidence: 25-year history of chronic cough/sputum + emphysema signs (hyperresonance) + acute exacerbation with fever and tachypnea
2. **Chronic Cor Pulmonale (Decompensated)**
   - Evidence: COPD background + 3-year history of palpitations, dyspnea, and leg edema (suggesting prolonged right ventricular overload) + current severe bilateral leg edema and cyanosis
**Pathophysiological Chain:**
COPD → Hypoxic pulmonary vasoconstriction + reduced pulmonary capillary bed → Pulmonary hypertension → Increased right ventricular afterload → RV hypertrophy/dilation → Right heart failure → Systemic congestion (leg edema, cyanosis)
**Differential Exclusion:**
- Regular rhythm, no murmurs → Rules out rheumatic valvular disease and atrial fibrillation as causes of heart failure
- Symmetric edema → Rules out renal origin (latter typically presents with periorbital/facial edema)
```
#### 3. **Exam Questions**
Question:
```bash
The most common site of intestinal tuberculosis is:
A. Duodenum
B. Jejunum
C. Ileocecal region
D. Transverse colon
E. Sigmoid colon
```
Answer:
```bash
**C. Ileocecal region**
This is the most characteristic predilection site for intestinal tuberculosis. Reasons:
- The ileocecal region has the richest lymphoid tissue (Peyer's patches), making it prone to Mycobacterium tuberculosis colonization
- Slower peristalsis and longer retention time of contents facilitate bacterial invasion
Therefore, the differential diagnosis between intestinal tuberculosis and Crohn's disease also centers on this region — when the ileocecal area shows circumferential/irregular ulcers, localized distribution, and positive acid-fast staining, it favors intestinal tuberculosis; longitudinal ulcers, segmental distribution, and fistulas favor Crohn's disease.
```

## About the Author

**xllgreen (https://xllgreen.github.io)** — Medical student at Jiujiang University Clinical Medical College · Tech enthusiast

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
© 2026 Hangzhou DeepSeek Artificial Intelligence Fundamental Technology Research Co., Ltd. All Rights Reserved
<br>
<br>
<img src="https://cdn.cnbj1.fds.api.mi-img.com/aife/mimo-blog-fe/doc_build/static/image/logo.99baaffe.png" width="130px">
<br>Xiaomi Mimo API: https://platform.xiaomimimo.com/
Copyright © 2010 - 2026 Xiaomi. All Rights Reserved
<br>

## License

This project is compiled based on *Internal Medicine*, 10th Edition (PMPH) and is intended for learning and reference purposes only.

## Star History

<a href="https://www.star-history.com/?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=Internal-Medicine-PMPH-10edition&type=date&legend=top-left" />
 </picture>
</a>
