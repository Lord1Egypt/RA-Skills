# Verified Humanizer

**Make AI text sound natural without turning privacy into collateral damage.**

Verified Humanizer rewrites stiff, generic, or overly polished AI text into writing that sounds more natural and human. It keeps rewriting local, measures the transformation with simple before/after metrics, and supports an optional verification step for the final evaluation summary.

## What it does

This skill helps agents:

- remove obvious AI-writing patterns
- improve rhythm, specificity, and tone
- measure the before/after transformation
- optionally attach a verification result for the evaluation summary

## Core model

Verified Humanizer separates three things:

1. **Transformation** — rewrite the text locally
2. **Evaluation** — measure the change using simple metrics
3. **Verification** — optionally verify the evaluation summary using structured data only

That separation matters. The skill does not treat external verification as the editor, and it does not expose raw user text by default.

## Why this exists

Most “humanizer” tools make big claims and hide the process. This skill takes a safer approach:

- rewriting stays local
- evaluation is visible
- verification is optional
- sensitive text stays out of verification flows

## What it is not

Verified Humanizer is **not**:

- proof of human authorship
- an AI detector
- a plagiarism bypass tool
- a claim that text is “undetectable”

It is a writing transformation and evaluation workflow.

## Package contents

This packaged release includes:

- `SKILL.md` — main operating guide
- `assets/` — templates for reports and rewrite review
- `hooks/` — OpenClaw bootstrap guidance
- `references/` — examples and integration notes
- `scripts/` — local helper scripts for scan-safe workflow support
- `.learnings/` — operational notes, errors, and improvement ideas

## Verification design

Verification is optional and should only use structured metrics such as counts, deltas, and simple boolean checks. Do **not** send the original or rewritten text to a verifier.

## Best use cases

- polishing AI-assisted drafts
- cleaning up repetitive or generic text
- making writing sound less formulaic
- adding an audit trail for style transformations in higher-trust workflows

## License

MIT-0
