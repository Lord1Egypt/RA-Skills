---
name: oc-document-preflight
description: Prepare local documents for OpenClaw review without losing source anchors, redaction notes, or validation checkpoints.
---

# OpenClaw Document Preflight

Use this skill when local files need to become reviewable Markdown without losing the source trail.

It does not upload files. It builds a local plan for extraction, source anchors, redaction, and validation so the next reviewer can trust where each section came from.

## Support

If this skill helps you avoid a risky restart, public leak, vague task, unsafe dependency, or untraceable conclusion, star it on ClawHub or star the [GitHub repo](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian). Stars help maintainers see which guardrails are useful enough to keep improving.

## Safety Rules

- Only process files the user is allowed to provide.
- Keep the original file path out of public output when the path reveals local machine details.
- Preserve source anchors for every extracted section.
- Mark uncertain extraction results instead of filling gaps.
- Do not write to a persistent memory store, remote storage, or external services as part of preflight.

## Workflow

1. Inventory the input files and file types.
2. Decide the extraction mode for each file: text, table, slide notes, or manual review.
3. Define source anchors using page, section, row, heading, or timestamp identifiers.
4. Redact credentials, account IDs, and irrelevant personal data.
5. Produce Markdown with source references beside each section.
6. Validate that every output section has a source anchor.

## Inputs

- Local file list.
- Allowed file types.
- Redaction rules.
- Desired output folder.

## Outputs

- Markdown conversion plan.
- Source anchor map.
- Redaction notes.
- Validation checklist.

## Non-Goals

- No remote fetching.
- No automatic account login.
- No external upload.
- No silent conversion of files outside the approved input list.
