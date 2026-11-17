## Description:

Converts scanned PDF books into OCR-derived, chapter-structured study notes with Markdown and HTML outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4zsz6jmmx6-source](https://clawhub.ai/user/4zsz6jmmx6-source)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn scanned PDF books into OCR text, chapter guides, study notes, extracted assets, and navigable HTML pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF page images are uploaded to an external GLM-OCR/ZhipuAI service.

Mitigation: Use the skill only with PDFs that are approved for transmission to that service, and review organizational data handling requirements before running OCR.

Risk: Generated HTML from untrusted PDFs may be unsafe to open because the renderer is under-scoped.

Mitigation: Open generated HTML only in an isolated environment unless the renderer is fixed to escape or sanitize content and disclose all remote resources.

Risk: Dependencies and runtime behavior require review before installation.

Mitigation: Pin or review Python dependencies and run the workflow in an isolated environment before using it with sensitive documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/4zsz6jmmx6-source/skills/pdf-learning-workflow)
- [ZhipuAI GLM-OCR Service](https://bigmodel.cn)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, HTML, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, local files, and command-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces page images, OCR chunks, merged notes, guide files, chapter files, cropped image assets, and an HTML index.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
