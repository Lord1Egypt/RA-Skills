## Description:

HTML OCR helps agents extract text from image-embedded or scanned content in local HTML files using MinerU OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to OCR scanned or image-heavy HTML pages and convert embedded image text into searchable Markdown or text-oriented outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the third-party MinerU CLI and API for OCR processing.

Mitigation: Install MinerU only from the documented package or repository, pin or review the version, and run it in an isolated environment when possible.

Risk: MINERU_TOKEN is a credential required for OCR extraction.

Mitigation: Store the token in the environment or credential manager, avoid committing it, and rotate it if exposed.

Risk: HTML documents sent for OCR may contain confidential content.

Mitigation: Process sensitive documents only after confirming that MinerU API handling is acceptable for the data classification.

## Reference(s):

- [HTML OCR on ClawHub](https://clawhub.ai/mzlzyca/skills/html-ocr)
- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU API Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [OCR output is written to stdout by default or to a user-specified output directory when the MinerU CLI is invoked with -o.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
