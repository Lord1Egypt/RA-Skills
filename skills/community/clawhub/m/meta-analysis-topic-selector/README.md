# meta-analysis-topic-selector

> Topic-selection assessment and topic-report generation Skill for meta-analyses (systematic reviews) — turns "intuition-driven topic judgment" into an auditable, standardized workflow.

![version](https://img.shields.io/badge/version-1.0.1-blue)
![license](https://img.shields.io/badge/license-MIT--0-green)
![platform](https://img.shields.io/badge/platform-OpenClaw%20%7C%20WorkBuddy-orange)

## ✨ What it does

This Skill formalizes the "meta-analysis topic selection" process into an auditable, output-driven standardized workflow — from a vague research interest to a PROSPERO-ready topic report.

## 🎯 Core capabilities

| Module | Description |
|---|---|
| **Three-path entry** | Rapid assessment (≤30 min verdict card) / Full assessment (5 stages) / Dedup re-audit (post-rejection) |
| **Four-dimension topic assessment** | Clinical value / Methodological feasibility / Data availability / Novelty, 0–20 quantified |
| **6 cross-check rules R1–R6** | Conservative style; triggering forces re-review and auto-downgrades the recommendation to "hold" |
| **PICO/PECO operational decomposition** | Every qualifier must be expressible in a search string; includes complex-intervention specs (combination / titration / sequential / planned switch) |
| **Three-layer deduplication search** | PROSPERO + Cochrane + PubMed + non-English DB extension (CNKI / Wanfang / SinoMed) |
| **Near-duplicate judgment matrix** | Distinguishes 7 near-duplicate types (switch within-class intervention / dose / outcome / subgroup, etc.) |
| **PRISMA 2020 + AMSTAR-2 pre-check** | 11 key items compliance preview + 7 critical-weakness avoidance checklist |
| **Meta-type decision tree** | pairwise / NMA / IPD / dose-response / DTA / proportion / genetic association / multivariate |
| **Standardized report generation** | 11-section Markdown / HTML output with JSON schema validation |
| **PROSPERO field mapping** | 22 form fields map directly to avoid omissions |

## 📦 Directory structure

```
meta-analysis-topic-selector/
├── SKILL.md                          # Main entry: 5-stage workflow + cross-check rules
├── references/                       # 5 methodological reference docs
│   ├── topic-selection-framework.md       # Four-dim assessment + meta-type decision tree
│   ├── pico-decomposition-guide.md        # PICO decomposition + complex-intervention spec
│   ├── novelty-assessment-guide.md        # Dedup search + near-duplicate judgment
│   ├── prisma-2020-checklist.md           # PRISMA pre-check + field examples
│   └── amstar-2-checklist.md              # AMSTAR-2 + critical-weakness avoidance checklist
├── scripts/
│   ├── generate_topic_report.py           # Report generator (MD/HTML)
│   └── generate_topic_report.example.json # Input JSON schema doc
├── assets/
│   ├── topic_report_template.md           # Manual-fill template
│   └── prospero-registration-mapping.md   # PROSPERO 22-field mapping
├── topic-report-example.md                # Script-generated example report
└── topic-report-example.html
```

## 🚀 Install

### OpenClaw / WorkBuddy

```bash
# Install via ClawHub
clawhub install wenhan9739/meta-analysis-topic-selector

# Or use OpenClaw
openclaw skills install wenhan9739/meta-analysis-topic-selector
```

### Manual install

```bash
git clone https://github.com/wenhan9739/meta-analysis-topic-selector.git
# Copy into the skills directory
cp -r meta-analysis-topic-selector ~/.workbuddy/skills/
```

## 📖 Usage examples

### Trigger phrases

- "I want to do a meta-analysis on hepatocellular carcinoma immunotherapy but don't know what topic"
- "Can PD-1 + lenvatinib be done as a meta?"
- "Tell me in 5 min whether this can be a meta" (→ rapid assessment path)
- "Generate a meta-analysis topic report"
- "Is this topic duplicated with an existing meta?"
- "Does switching to PD-L1 count as a duplicate?" (→ near-duplicate judgment)
- "Should I choose NMA or traditional pairwise meta?"
- "Can my topic comply with PRISMA 2020?"
- "What do I need to prepare before PROSPERO registration?"

### Generate a topic report

```bash
# Markdown output
python scripts/generate_topic_report.py input.json output.md

# HTML output (auto-detected by extension, or explicit --format)
python scripts/generate_topic_report.py input.json output.html
```

See `scripts/generate_topic_report.example.json` for the input JSON schema.

## 🏥 Applicable fields

Intervention / exposure / diagnostic / prognostic meta-analysis topic selection in medicine, epidemiology, pharmacy, nursing, public health, psychology, education, and related fields.

## 📚 Reference standards

- PRISMA 2020 — Page MJ et al., BMJ 2021;372:n71
- AMSTAR-2 — Shea BJ et al., BMJ 2017;358:j4008
- Cochrane Handbook for Systematic Reviews of Interventions (Version 6.x)
- GRADE Working Group guidance
- PROGRESS-Plus framework
- Cochrane RoB 2 / ROBINS-I / QUADAS-2 / ROBINS-E

## 📄 License

MIT-0 — anyone may freely use, modify, and redistribute (including commercially), no attribution required.

## 👤 Author

**wenhan9739** — [GitHub](https://github.com/wenhan9739)
