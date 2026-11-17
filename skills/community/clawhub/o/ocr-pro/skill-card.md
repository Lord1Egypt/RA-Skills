## Description:

Ocr Pro guides agents through using MinerU's mineru-open-api CLI to extract text and structured content from PDFs and images, including complex layouts with OCR and VLM modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and run MinerU OCR for PDFs, scanned documents, screenshots, photos, and images that need accurate text extraction or layout-aware processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on MinerU/OpenDataLab and the mineru-open-api package.

Mitigation: Install only when that dependency chain is trusted, and prefer pinned versions or an isolated environment.

Risk: OCR processing may send documents to a third-party service.

Mitigation: Do not process confidential documents unless third-party OCR processing has been approved.

Risk: The skill requires a MinerU token for extraction.

Mitigation: Store MINERU_TOKEN using the agent environment's secret-handling mechanism and avoid exposing it in logs or shared command history.

## Reference(s):

- [Ocr Pro on ClawHub](https://clawhub.ai/mzlzyca/skills/ocr-pro)
- [MinerU Homepage](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on the mineru-open-api CLI, requires MINERU_TOKEN for extraction, and may direct output to stdout or files.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
