## Description:

Converts screenshots into organized knowledge-base documents using OCR and optional AI categorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyiyong985](https://clawhub.ai/user/haoyiyong985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a local screenshot-processing workspace, extract text with Tencent Cloud OCR, Baidu Cloud OCR, or local Tesseract, and produce organized Markdown and Word knowledge-base documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshot content may be sent to configured cloud providers even when related config flags appear disabled.

Mitigation: Avoid sensitive screenshots unless cloud processing is acceptable, review configuration before use, and remove unused API keys instead of relying only on enabled:false.

Risk: The skill installs dependencies and runs local processing scripts.

Mitigation: Use a dedicated work folder and install dependencies in an isolated virtual environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haoyiyong985/skills/image-knowledge-converter)
- [Usage Guide](references/usage-guide.md)
- [Quick Start](docs/quick-start.md)
- [Installation](docs/installation.md)
- [Multi-Engine OCR](docs/multi-engine-ocr.md)
- [OCR Fallback](docs/ocr-fallback.md)
- [Tencent Cloud OCR](https://cloud.tencent.com/product/ocr)
- [Baidu OCR](https://ai.baidu.com/tech/ocr)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, YAML configuration, generated Markdown and Word documents, and JSON processing reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs under the selected work folder and may use configured OCR, LLM, or IMA services.]

## Skill Version(s):

1.2.8 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
