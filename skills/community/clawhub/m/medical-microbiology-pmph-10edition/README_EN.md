# Medical Microbiology Medical Microbiology-PMPH-10edition
<div align="center">

> *「21st Century Medical Student Guide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>
> A clinical microbiology skill set based on the 10th edition of "Medical Microbiology" (People's Medical Publishing House) — 153 core microbiology & infectious disease skills
<br>
<br>
<img src="/assets/Microbiology.svg" width="260px">
<br>

Why struggle through an entire textbook?<br>
Just ask a question, and get answers directly from the textbook.

<br>

**Other Languages:**

[中文](README.md) · [日本語](README_JP.md) · [Français](README_FR.md) · [Русский](README_RU.md)

</div>

---

## Project Overview

This project systematically integrates core domains of medical microbiology, including bacteriology, virology, mycology, immunology, disinfection & sterilization, microbiome science, and infection control, covering **153 key skills** across 9 major categories.

**Target Audience**: Medical students, clinicians, laboratory technologists, public health workers, infection control teams

**Reference Textbook**: People's Medical Publishing House *Medical Microbiology* 10th Edition (ISBN: 978-7-117-34552-3)

**⚠️Risk⚠️**: This skill set covers microbiological diagnostics, antimicrobial therapy, infection control, and laboratory procedures, which could be misused as independent medical advice.

Mitigation: Use output only as educational reference or for clinician review. Verify recommendations against current official guidelines, local protocols, and qualified specialists.

**⚠️Risk⚠️**: Source content does not consistently enforce clinician-only safety boundaries.

Mitigation: Deploy system-level medical safety policies requiring escalation to qualified clinicians for diagnosis, prescription, dosing, emergency care, and self-treatment decisions.


## Project Structure

```
MedicalMicrobiology-PMPH-10edition/
├── SKILL.md              # Core config — 153-skill registry
├── README.md             # This document — Chinese version
├── README_EN.md          # English version
├── README_JP.md          # Japanese version
├── README_FR.md          # French version
├── README_RU.md          # Russian version
├── <skill-name>/         # Skill definitions
│   └── SKILL.md          #   Skill details (when to use, steps, references)
├── index.md              # Full skill index with Chinese descriptions
├── assets/               # Static assets (icons, images)
└── scripts/              # Optional scripts
```

## Skill Categories

| Category | Skills | Description |
|----------|--------|-------------|
| 🦠 Bacteriology | 60 | Resistance, identification, pathogenesis, AST, culture |
| 🧬 Virology | 42 | Classification, replication, diagnostics, antivirals, vaccines |
| 🔬 Immunology & Serology | 26 | Immune mechanisms, serology, vaccines, inflammation |
| 🧹 Sterilization & Infection Control | 8 | Chemical disinfection, heat sterilization, biosafety |
| 🌿 Microbiome & FMT | 7 | Microbiota composition, FMT, probiotics, dysbiosis |
| 🧪 Special Pathogens | 2 | Prion classification & pathogenesis |
| 📚 Textbook & Resources | 4 | Textbook authority, revision principles, digital resources |
| 🔬 Clinical Microbiology Lab | 3 | Specimen collection, transport, QC |
| 🏥 Emerging Infectious Diseases | 3 | Anaplasmosis, HGA, etc. |

## Quick Start

### Installation

CLI:
```bash
openclaw skills install medical-microbiology-pmph-10edition
```

Prompt:
```bash
Before installing anything, inspect the ClawHub skill metadata and setup requirements.
Install the skill "MedicalMicrobiology-PMPH-10edition" from ClawHub only after those checks pass.
Keep the work scoped to this skill only.
```

### Usage

Each skill contains four parts:
1. **When to Use** — Triggers for invoking the skill
2. **Execution Steps** — Standardized workflow
3. **Cautions** — Contraindications & warnings
4. **References** — Supplementary materials

### Query Examples

- "How to differentiate Shigella from Salmonella?"
- "What control measures should be taken during a norovirus outbreak?"
- "What are the diagnostic methods for Helicobacter pylori?"
- "How to assess the risk of HCV chronic progression to HCC?"
- "What are the key points for assessing bacterial biofilm infections?"

## License

This project is based on the 10th edition of *Medical Microbiology* (People's Medical Publishing House) and is for educational reference only.

## Technical Support

PDF2App: https://pdf2app.cn

Microsoft Visual Studio Code: https://code.visualstudio.com/

Claude Code for VS Code: https://claude.com/
© 2026 Anthropic PBC

DeepSeek API: https://platform.deepseek.com/

Xiaomi Mimo API: https://platform.xiaomimimo.com/
