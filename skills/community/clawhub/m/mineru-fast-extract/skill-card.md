## Description:

MinerU Fast Extract helps agents run mineru-open-api to convert PDFs, images, DOCX, PPTX, and document URLs into Markdown with OCR, table extraction, and formula extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mineru-extract](https://clawhub.ai/user/mineru-extract)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, students, and agent users use this skill to extract text, tables, formulas, and images from local or remote documents into Markdown without setting up API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted documents, remote URLs, and extracted outputs may contain sensitive information.

Mitigation: Use the skill only when comfortable with the MinerU/OpenDataLab CLI handling the file, and specify an explicit output directory for sensitive documents.

Risk: The skill installs and runs an unpinned third-party CLI.

Mitigation: Prefer a pinned or sandboxed installation and review the CLI before using it in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mineru-extract/skills/mineru-fast-extract)
- [MinerU homepage](https://mineru.net)
- [OpenClaw source metadata](https://github.com/MinerU-Extract/mineru-fast-extract)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and shell command guidance; extraction results may be written to stdout or Markdown files with extracted images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can target local files or document URLs, with optional output directory, language, page range, and timeout settings.]

## Skill Version(s):

0.2.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
