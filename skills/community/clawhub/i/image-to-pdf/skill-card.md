## Description:

Merge multiple images into a single PDF document, with guidance for Excel-based PDF renaming, scanned-PDF OCR, and optional Telegram delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo)

### License/Terms of Use:


## Use Case:

Developers and operations users can use this skill to guide image-to-PDF merging, voucher-style PDF naming from Excel indexes, and OCR extraction from scanned PDFs for accounting or document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive accounting documents may be sent through Telegram without a clear per-run confirmation step.

Mitigation: Require visible confirmation of the recipient, filenames, and message text before sending any generated PDF or summary.

Risk: Spreadsheet-derived filenames may contain unsafe or invalid characters.

Mitigation: Sanitize generated filenames and validate Excel index-to-row mappings before copying or renaming files.

Risk: Unpinned dependencies and local OCR tooling can behave differently across environments.

Mitigation: Pin Python and system dependencies and verify OCR/PDF behavior in a controlled workspace before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meowlegemy-sudo/skills/image-to-pdf)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dependency installation commands, file naming patterns, OCR extraction steps, and Telegram send guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
