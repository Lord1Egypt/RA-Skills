# Changelog

All notable changes to `knowledge-health-checker` are documented here.

## [1.1.0] - 2026-04-25

### Added

- Added ClawHub-ready metadata and public-facing positioning.
- Added a safer default workflow:
  - confirm scope
  - build file/heading index
  - detect hollow notes
  - detect broken links
  - analyze density and structure
  - analyze graph health
  - score health
  - generate report and safe fix plan
- Added a 0-100 health scoring model with labels:
  - Excellent
  - Healthy
  - Needs maintenance
  - Fragile
  - Critical
- Added a standard output format for findings, risks, fixes, and artifacts.
- Added a safe fix policy with low/medium/high-risk actions.
- Added anti-patterns and quality bar for knowledge-base audits.

### Improved

- Refocused the skill for broad Markdown knowledge-base use across Obsidian, Logseq, Notion exports, docs folders, and wiki repositories.
- Improved safety guidance: report and propose by default; never delete, rename, or rewrite without explicit confirmation.
- Improved scoring clarity by separating hollow notes, broken links, density, and network connectivity.
- Improved scalability guidance for large knowledge bases.
- Improved portability for non-English filenames and mixed Markdown conventions.

### Changed

- Reorganized the original long workflow into a clearer ClawHub-friendly structure.
- Reframed “automatic repair” as a reviewed fix plan rather than default mutation.

### Verified

- Ran the bundled scanner smoke test:

```bash
python3 scripts/health_check.py /tmp/knowledge-health-sample
```

Expected behavior: scan Markdown files, report hollow notes / broken links / graph stats, and complete without crashing.
