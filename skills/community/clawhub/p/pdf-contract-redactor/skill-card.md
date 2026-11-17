## Description:

PDF Contract Redactor uses Alibaba Cloud OCR to identify field names and corresponding values in scanned contracts, then covers the values while keeping field names visible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chayjan](https://clawhub.ai/user/chayjan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to redact sensitive values from scanned PDF contracts while preserving surrounding field labels for review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The implementation may leave or recreate sensitive contract data even when the output appears redacted.

Mitigation: Review generated PDFs before sharing and prefer a version that uses secure PDF redaction or page rasterization.

Risk: Document pages are uploaded to Alibaba Cloud OCR during processing.

Mitigation: Use the skill only for contracts where third-party cloud OCR processing is approved.

Risk: Generated outputs, logs, or sidecar JSON files may expose values intended to be hidden.

Mitigation: Restrict access to output files, remove plaintext value export and stdout logging when handling sensitive contracts, and delete temporary artifacts after review.

Risk: OCR credentials are supplied at runtime and need safer handling.

Mitigation: Use approved secret storage or environment-based credential handling instead of exposing credentials in command history or process arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chayjan/skills/pdf-contract-redactor)
- [Alibaba Cloud OCR API endpoint](https://ocr.aliyuncs.com)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; runtime outputs are PDF and JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a redacted PDF and a sidecar JSON file listing matched field-value pairs when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
