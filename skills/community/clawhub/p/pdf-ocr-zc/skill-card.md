## Description:

Batch OCR for scanned PDFs that creates searchable PDF outputs and can support downstream Markdown or plain-text extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclawzhangchong](https://clawhub.ai/user/openclawzhangchong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and agent builders use this skill to OCR scanned PDF collections before indexing, retrieval, or document-ingestion workflows. It supports single-file processing and recursive batch processing with a configurable OCR language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive batch processing can create many local *_ocr.pdf outputs and logs.

Mitigation: Test on a small folder first, verify generated outputs, and avoid unattended scheduled use until the workflow is reviewed.

Risk: The installation guidance depends on unpinned third-party OCR components.

Mitigation: Use a virtual environment and verify or pin dependency versions before production use.

Risk: Incorrect OCR language settings can reduce text quality for scanned documents.

Mitigation: Select the correct OCR language with --lang and validate sample results before bulk processing.

## Reference(s):

- [OCR Installation Guide](references/install_ocr.md)
- [OCR Parameters and Tips](references/ocr_tips.md)
- [UB Mannheim Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated local PDF or text artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local PDF paths supplied by the user and may create *_ocr.pdf files plus logs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
