## Description:

Compile LaTeX documents to PDF using pdflatex, xelatex, or lualatex with template support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willamhou](https://clawhub.ai/user/willamhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and technical writers use this skill to compile LaTeX source into PDFs, preview generated PDFs, and retrieve starter templates through a local Prismer LaTeX container.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LaTeX source is active input processed by a separate local compilation container.

Mitigation: Review and trust the Prismer LaTeX container before use, and treat submitted LaTeX content as potentially active input.

Risk: Compilation requires a local server at localhost:8080; calls fail when the service is unavailable.

Mitigation: Start and verify the expected Prismer LaTeX compilation server before invoking compile or preview tools.

Risk: Generated PDF paths are container-internal and are not host-mounted.

Mitigation: Use the preview path that returns base64 output when an agent needs to inspect or display the PDF without relying on host filesystem access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/willamhou/skills/latex-compiler)
- [Prismer Project](https://github.com/Prismer-AI/Prismer)
- [Prismer LaTeX Container Source](https://github.com/Prismer-AI/Prismer/tree/main/docker/base)
- [Prismer Dockerfile](https://github.com/Prismer-AI/Prismer/blob/main/docker/base/Dockerfile)
- [Prismer Docker Compose](https://github.com/Prismer-AI/Prismer/blob/main/docker/docker-compose.dev.yml)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [JSON tool results containing compilation status, PDF paths, logs, warnings, errors, templates, or base64-encoded PDF output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [LaTeX compilation depends on a local server at localhost:8080; generated PDF paths are container-internal unless returned as base64 preview output.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
