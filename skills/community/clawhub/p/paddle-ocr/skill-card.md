## Description:

PaddleOCR converts legal PDFs and scanned document images into Markdown with structured OCR outputs and a traceable local archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

Developers, legal operations teams, and agents use this skill to convert legal PDFs, case files, medical records, evidence scans, tables, formulas, and complex layouts into editable Markdown and archived JSON outputs for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive legal, medical, financial, or evidence files may be uploaded to the configured OCR service.

Mitigation: Use only a trusted PaddleOCR endpoint and prefer limited page ranges for sensitive documents.

Risk: The skill keeps local archives by default, which may retain sensitive source files, OCR text, JSON, and extracted images.

Mitigation: Use --no-archive when retention is not appropriate and review archive storage permissions before processing sensitive files.

Risk: Output image directories can be replaced during conversion.

Mitigation: Avoid choosing output paths where an existing *_images directory contains important files.

## Reference(s):

- [PaddleOCR official site](https://www.paddleocr.com)
- [Output schema](references/output_schema.md)
- [ClawHub skill page](https://clawhub.ai/cat-xierluo/skills/paddle-ocr)
- [Project homepage](https://github.com/cat-xierluo/legal-skills)

## Skill Output:

**Output Type(s):** [Markdown, Text, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown files, JSON archive files, local file paths, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local archive by default; optional page ranges and output paths can narrow processing.]

## Skill Version(s):

1.1.1 (source: frontmatter and changelog, released 2026-04-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
