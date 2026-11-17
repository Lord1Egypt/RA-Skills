## Description:

Complex document parsing with PaddleOCR. Intelligently converts complex PDFs and document images into Markdown and JSON files that preserve the original structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sfresurgam](https://clawhub.ai/user/sfresurgam)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse complex PDFs and document images through a configured PaddleOCR/Triton endpoint, then return complete extracted text, Markdown, tables, formulas, and structured page JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured PaddleOCR/Triton endpoint receives complete document content.

Mitigation: Install and use the skill only when documents are intended to be sent to that endpoint, and prefer trusted, access-controlled deployments.

Risk: Documents or credentials may be sent over plaintext HTTP when a non-local endpoint is configured that way.

Mitigation: Use HTTPS for non-local endpoints and avoid sending access tokens or Basic Auth credentials over HTTP.

Risk: Raw OCR results are saved to the system temp directory by default.

Mitigation: Use --stdout or a private --output path for sensitive documents, and remove temporary result files when they are no longer needed.

## Reference(s):

- [PaddleOCR Document Parsing Output Schema](artifact/references/output_schema.md)
- [ClawHub skill page](https://clawhub.ai/sfresurgam/skills/paddleocr-vl-locally)
- [PaddleOCR](https://www.paddleocr.com)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON extracted from document parsing results, with shell commands and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [By default, raw JSON is saved under the system temp directory unless --stdout or --output is used.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
