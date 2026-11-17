## Description:

Image to Markdown extracts text from images such as screenshots, photos, and scanned pages into Markdown using OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to read text from screenshots, photos, scanned pages, and other image files and convert the OCR result into Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images are uploaded to MinerU's cloud service for OCR processing.

Mitigation: Avoid sending confidential images unless MinerU's privacy terms meet the user's needs.

Risk: The skill depends on installing and trusting the third-party MinerU CLI.

Mitigation: Install from trusted package sources and prefer a pinned or reviewed CLI version in sensitive environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/image-to-markdown)
- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single OCR extraction result; images are limited to 10MB by the documented CLI behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
