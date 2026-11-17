## Description:

MinerU Doc Parser helps agents choose and run the MinerU CLI to parse PDFs, scanned documents, images, Office files, and web pages into Markdown, HTML, LaTeX, DOCX, or JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mineru-extract](https://clawhub.ai/user/mineru-extract)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and data teams use this skill to extract structured content from documents and web pages with MinerU. It guides agents between quick tokenless parsing and authenticated extraction for tables, formulas, OCR, batch jobs, and multiple output formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected documents or URLs may be sent to MinerU/OpenDataLab for processing.

Mitigation: Use the skill only for documents approved for external processing, and avoid confidential or regulated content unless the user has explicit approval.

Risk: The skill installs a mutable global CLI package.

Mitigation: Prefer a pinned CLI version in an isolated environment and review package updates before use.

Risk: MinerU API tokens can be exposed through shared terminals, scripts, logs, or screenshots.

Mitigation: Treat tokens as secrets, configure them through approved secret handling, and avoid pasting them into shared or recorded contexts.

## Reference(s):

- [MinerU Homepage](https://mineru.net)
- [MinerU Source Metadata Link](https://github.com/MinerU-Extract/mineru-ai)
- [MinerU CLI Issue Reference](https://github.com/opendatalab/MinerU-Ecosystem/tree/main/cli)
- [MinerU Token Management](https://mineru.net/apiManage/token)
- [ClawHub Skill Page](https://clawhub.ai/mineru-extract/skills/mineru-ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Files]

**Output Format:** [Markdown guidance with inline shell commands and file output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct MinerU to produce Markdown, HTML, LaTeX, DOCX, JSON, or extracted image files depending on command flags.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
