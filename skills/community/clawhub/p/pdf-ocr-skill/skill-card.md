## Description:

pdf-ocr extracts text from scanned PDF and image files using local RapidOCR or SiliconFlow cloud OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yejinlei](https://clawhub.ai/user/yejinlei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to extract Chinese and English text from scanned PDFs, screenshots, and image files. It supports local OCR for offline-style workflows and SiliconFlow cloud OCR when configured for higher-accuracy processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document contents can be sent to SiliconFlow cloud OCR after RapidOCR initialization fails or when cloud OCR is selected.

Mitigation: Use the skill only with documents approved for cloud processing, avoid configuring a SiliconFlow API key unless cloud OCR is intended, and monitor the selected OCR engine before processing sensitive files.

Risk: The skill can install Python packages at runtime when dependencies are missing.

Mitigation: Install and review dependencies in an isolated environment before enabling the skill, and restrict network access during execution when runtime installation is not acceptable.

Risk: OCR may produce incomplete or inaccurate text for low-quality scans, complex layouts, or handwriting.

Mitigation: Review extracted text against the source document before using it for contracts, IDs, financial records, medical records, or other high-impact workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yejinlei/skills/pdf-ocr-skill)
- [SiliconFlow chat completions endpoint](https://api.siliconflow.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text OCR results, Markdown usage guidance, Python code examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR result objects include extracted text, page count, selected engine, and optionally a saved image directory.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
