## Description:

Image OCR helps agents extract text and structured content from photos, screenshots, scanned documents, and other image files using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other external users use this skill when an agent needs to read text from photographs, screenshots, scanned documents, receipts, whiteboards, signs, or other image files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and extracted text can contain sensitive or private information.

Mitigation: Use only approved inputs, avoid private documents unless authorized, and handle OCR output as potentially sensitive data.

Risk: The skill depends on the external mineru-open-api package and authentication for some extraction modes.

Mitigation: Prefer a pinned or isolated installation of mineru-open-api and manage MINERU_TOKEN as a secret.

## Reference(s):

- [ClawHub Image OCR Skill](https://clawhub.ai/mzlzyca/skills/photo-ocr)
- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML, LaTeX, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with bash commands; OCR results can be Markdown, HTML, JSON, LaTeX, or plain text depending on the selected MinerU command.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill documents quick OCR, token-based extraction, language hints, VLM mode, formula recognition, table recognition, and stdout or directory output.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
