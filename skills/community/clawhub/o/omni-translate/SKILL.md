---
name: omni-translate
description: Apply high-fidelity localization to structured artifacts such as web apps, docs, PDFs, slide decks, Office files, subtitles, code repositories, and game assets. Use when an agent needs to preserve structure, layout, placeholders, encoding, stable identifiers, and delivery safety instead of treating translation as plain text replacement.
---

# OmniTranslate

## Quick Start

1. Run `python scripts/probe_artifacts.py <path>` on the target file or folder.
2. Read [references/workflow.md](references/workflow.md).
3. Apply [references/decision-thresholds.md](references/decision-thresholds.md) before editing.
4. Use [references/artifact-pipelines.md](references/artifact-pipelines.md) to select the correct path.
5. Use [references/translation-boundaries.md](references/translation-boundaries.md) to protect non-translatable content.
6. Load [references/format-risk-checklists.md](references/format-risk-checklists.md) for the active format.
7. Use [references/locale-sensitive-typography.md](references/locale-sensitive-typography.md) for CJK, RTL, or mixed-script output.
8. Validate with [references/quality-gates.md](references/quality-gates.md) before handoff.

## Operating Rules

- Prefer editable sources over derived exports.
- Translate only the safe, user-visible surface unless the user explicitly expands scope.
- Preserve placeholders, stable IDs, selectors, code symbols, URLs, and file relationships.
- Fail closed when safe round-tripping is not possible.
- Report skipped content and residual risk explicitly.

## Deliverables

- the localized artifact or repository
- a concise note describing the selected pipeline
- a list of protected or skipped items
- a validation summary with any remaining fidelity risk
