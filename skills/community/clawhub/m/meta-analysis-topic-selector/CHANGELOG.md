# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.0.1] - 2026-06-22

### Changed

- **Full English translation** of all skill files for global researchers:
  - SKILL.md (main entry, workflow, decision gates, cross-check rules R1–R6)
  - 5 reference documents (topic-selection-framework, pico-decomposition-guide, novelty-assessment-guide, prisma-2020-checklist, amstar-2-checklist)
  - 2 asset documents (topic_report_template, prospero-registration-mapping)
  - Report generator script (dimension names, score labels, cross-check messages, example input, all output strings)
  - Example JSON input
- Bumped version 1.0.0 → 1.0.1
- Regenerated example reports (Markdown + HTML) from the English script

### Removed

- Previous Chinese-only example reports

## [1.0.0] - 2026-06-22

### Added

- **Three-path entry**: rapid assessment (≤30 min) / full assessment (5 stages) / dedup re-audit
- **Four-dimension topic assessment model**: clinical value / methodological feasibility / data availability / novelty, 0–20 quantified
- **6 cross-check rules R1–R6**: conservative style; triggering forces re-review
- **PICO/PECO operational decomposition spec**: includes complex interventions (combination / titration / sequential / planned switch)
- **Three-layer dedup search flow**: PROSPERO + Cochrane + PubMed + non-English DB extension
- **Near-duplicate judgment matrix**: 7 near-duplicate types
- **PRISMA 2020 + AMSTAR-2 pre-check**: 11 key items + 7 critical-weakness avoidance checklist
- **Meta-analysis type decision tree**: 8 meta types
- **Standardized topic-report generation**: 11-section Markdown / HTML output
- **PROSPERO 22-field mapping table**
- **JSON schema validation** (warn mode) + missing-field warnings
- **5 methodological reference documents**

### Documentation

- Full SKILL.md main entry
- 5 references/ docs
- 1 PROSPERO field-mapping asset
- 1 Mustache template
- Markdown + HTML example reports
