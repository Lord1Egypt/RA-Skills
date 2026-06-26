# Workflow

This document describes the repository's platform-neutral workflow for high-fidelity localization of structured artifacts.

## 1. Inventory the artifact

- Identify whether the input is a code repository, web app, document container, PDF, subtitle package, or mixed folder.
- Prefer editable sources over derived outputs. If both `pptx` and exported `pdf` exist, localize the `pptx`.
- Run `python scripts/probe_artifacts.py <path>` when the file makeup is unclear or when a folder contains multiple artifact types.

## 2. Apply decision thresholds

- Treat [decision-thresholds.md](decision-thresholds.md) as release gates.
- Decide whether the artifact is safely round-trippable before editing.
- If a hard-stop condition is triggered, narrow scope, switch pipelines, or stop and report the limitation.

## 3. Define the translation boundary

- Determine exactly which text is translatable.
- Protect placeholders, stable identifiers, selectors, URLs, paths, schema keys, code symbols, and signatures.
- Decide whether metadata, comments, notes, captions, or hidden content are in scope.

## 4. Choose the pipeline

- Use [artifact-pipelines.md](artifact-pipelines.md) to select the correct workflow.
- Use [format-risk-checklists.md](format-risk-checklists.md) before editing the chosen format.
- Use [locale-sensitive-typography.md](locale-sensitive-typography.md) for Chinese, Japanese, Korean, RTL, or mixed-script output.

## 5. Extract with structure intact

- Use the highest-fidelity editable representation available.
- Preserve segment IDs or stable mapping keys wherever possible.
- Keep enough context for terminology and tone without flattening the artifact into unstructured text.

## 6. Translate conservatively

- Apply terminology and brand locks before translation.
- Preserve formatting anchors, placeholders, inline markup, and structural boundaries.
- Preflight narrow containers such as buttons, table cells, labels, and slide titles.

## 7. Reinsert and rebuild

- Reinsert translations into the original structure whenever possible.
- Preserve ordering, relationships, metadata, notes, and text runs if the format supports them.
- Rebuild with the native toolchain when that is the most reliable path.

## 8. Validate and report

- Run [quality-gates.md](quality-gates.md) before handoff.
- Record what was translated, what was protected, what was skipped, and which thresholds determined scope.
- If any approximation was required, document exactly where and why.

## Expected outputs

- the localized artifact or repository
- a concise note describing the selected pipeline
- a list of protected or skipped items
- a validation summary with remaining fidelity risk, if any
