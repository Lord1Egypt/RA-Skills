## Description:

Intelligent PDF and image to Markdown converter using Ollama GLM-OCR with smart content detection for text, tables, and figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsukisama9292](https://clawhub.ai/user/tsukisama9292)

### License/Terms of Use:

MIT

## Use Case:

Developers and document-processing teams use this skill to convert PDFs and images into structured Markdown while preserving text, table, and figure content where the OCR model can identify it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install paths include shell commands and installer guidance that should be reviewed before execution.

Mitigation: Use trusted package-manager or verified installer paths, review hook scripts before running them, and avoid running setup as root unless required.

Risk: OCR processing sends document page images to the configured Ollama service.

Mitigation: Process sensitive documents only against a trusted local Ollama service or another endpoint approved for the data being handled.

Risk: PDF conversion writes generated PNG page images near the source PDF and removes matching generated files after processing.

Mitigation: Run conversion in a working directory that does not contain important PNG files whose names match the PDF page prefix.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tsukisama9292/skills/pdf-ocr-tool)
- [Publisher profile](https://clawhub.ai/user/tsukisama9292)
- [Ollama API documentation](https://docs.ollama.com/api/generate)
- [GLM-OCR model page](https://ollama.com/library/glm-ocr)
- [poppler-utils](https://poppler.freedesktop.org/)
- [uv package manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files generated from OCR results, with command-line usage and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process PDFs page by page or images directly; supports text, table, figure, mixed, and auto modes.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
