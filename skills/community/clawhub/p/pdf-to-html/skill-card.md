## Description:

Convert PDF documents to HTML using MinerU while preserving document structure and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, web publishers, and content teams use this skill to convert local or URL-hosted PDF documents into HTML for web display, CMS integration, or online archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF contents may be sent to the external MinerU/OpenDataLab service during conversion.

Mitigation: Use only PDFs the user is allowed to process through that service, and review provider privacy, retention, and compliance terms before handling sensitive documents.

Risk: The documented installer uses an unpinned mineru-open-api command-line tool.

Mitigation: Prefer a pinned, project-local or isolated installation and avoid installing or running the tool with elevated privileges.

## Reference(s):

- [PDF to HTML ClawHub Skill](https://clawhub.ai/mzlzyca/skills/pdf-to-html)
- [MinerU Homepage](https://mineru.net)
- [MinerU Token Management](https://mineru.net/apiManage/token)
- [MinerU Repository](https://github.com/opendatalab/MinerU)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML-file output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mineru-open-api and a MINERU_TOKEN for HTML extraction.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
