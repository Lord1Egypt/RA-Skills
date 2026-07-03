# Neurology — Neurology-PMPH-9edition
<div align="center">

> *「21st Century Medical Student Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical skills manual based on the 9th edition of "Neurology" (People's Medical Publishing House) — 66 core clinical skills in neurology and neurosurgery
<br>
<br>

**Other Languages:**

[简体中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Project Overview

This project systematically integrates core domains of neurology and neurosurgery, covering **66 key clinical skills** across 9 major categories. Content includes cerebrovascular diseases (ischemic/hemorrhagic stroke, interventional treatment), neurodegenerative and cognitive disorders, spinal cord and peripheral nerve pathologies, neurological emergencies and critical care, epilepsy and seizure disorders, neuromuscular diseases, and neuroimaging/electrophysiology interpretation.

**Target Audience**: Neurologists, neurosurgeons, medical students, emergency and critical care teams, interventional physicians

**Textbook Reference**: *Neurology*, 9th Edition, People's Medical Publishing House

**⚠️ Risk Notice ⚠️**: This skill covers neurological diagnosis, dosing, emergency treatment, and interventional procedure assessments, which may be misused as independent medical advice.

Mitigation: Use output only as educational reference or for clinician review. Verify recommendations against current official guidelines, local protocols, and qualified neurology specialists.

**⚠️ Risk ⚠️**: Source content does not strictly enforce clinician-only safety boundaries.

Mitigation: Deploy system-level medical safety policies requiring escalation to qualified clinicians for diagnosis, prescribing, dosing, emergency care, and self-treatment decisions.

## Project Structure

```
Neurology-PMPH-9edition/
├── SKILL.md                        # Core config — 66-skill registry
├── README.md                       # Project documentation (Chinese)
├── README_EN.md                    # Project documentation (English)
├── <skill-name>/                   # Individual skill definitions
│   └── SKILL.md                    #   Skill details (when to use, steps, references)
├── scripts/                        # Executable tool scripts
├── config/                         # Configuration files
└── tests/                          # Validation and tests
```

## Skills by Category

| Category | Count | Description |
|----------|-------|-------------|
| 🩸 Cerebrovascular & Intervention | 16 | Stroke, CAS, aneurysm, CVST, steal syndrome |
| 🚑 Emergency & Critical Care | 5 | Consciousness disorders, herniation, ICH, hyponatremia |
| 🧠 Neurodegenerative & Cognitive | 5 | VCI/DLB/bvFTD/CJD/PD non-motor symptoms |
| ⚡ Epilepsy & Seizure Disorders | 4 | Classification, ASMs, status epilepticus, DRE surgery |
| 💪 Spinal Cord, PNS & Neuromuscular | 11 | DMD/CMT/myotonia/peripheral neuropathy |
| 🛡️ Neuroimmune, Infection & Demyelinating | 6 | MS/NMOSD/ADEM/encephalitis/NPSLE |
| 🔬 Neurosurgery, Congenital & Craniocervical | 4 | Hydrocephalus, Chiari, basilar invagination |
| 👁️ Exam, Localization & Diagnostics | 10 | Localization, cranial nerves, EEG/imaging |
| 🩺 Systemic Neurological Complications | 5 | Thyroid/pregnancy/SLE/paraneoplastic/movement disorders |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install neurology-pmph-9edition
```

### Usage

Each skill contains four sections:
1. **When to Use** — Trigger conditions for the skill
2. **Procedure** — Standardized operating steps
3. **Caveats** — Contraindications and warnings
4. **References** — Detailed supplementary materials

### Query Examples

**Example 1 — Cerebrovascular Intervention:**
> Use the `acute-ischemic-stroke-endovascular-treatment` skill to evaluate endovascular treatment indications and workflow for an acute ischemic stroke patient with large vessel occlusion presenting 4 hours after onset.

**Example 2 — Neurological Localization:**
> Invoke the `neurological-localization-diagnosis` skill. A patient presents with right-sided central paralysis, right central facial/lingual palsy, and motor aphasia. Perform a detailed neuroanatomical localization diagnosis.

**Example 3 — Dementia Differentiation:**
> Use the `dlb-imaging-biomarker-differentiation` skill to analyze how imaging biomarkers (PET, MRI) can differentiate Dementia with Lewy Bodies (DLB) from Alzheimer's disease.

**Example 4 — Neurological Emergency:**
> Based on the `neurological-emergency-crisis-management` skill, provide the standard emergency crisis management protocol and first-/second-line medication guidelines for status epilepticus.

## Author

**xllgreen** — [GitHub](https://xllgreen.github.io) — Medical Student at Jiujiang University · Tech Enthusiast

## License

This project is based on the 9th edition of "Neurology" (People's Medical Publishing House) and is provided for educational reference only.
