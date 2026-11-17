## Description:

Convert academic papers from arXiv HTML pages or local PDFs into structured Chinese reading reports with original figures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nuaalixu](https://clawhub.ai/user/nuaalixu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, students, and other paper readers use this skill to summarize, analyze, and create structured Chinese reading reports for academic papers. It supports HTML, Markdown, and Word outputs with selected original figures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads paper HTML, PDFs, and figure assets from the web, which can expose the workspace to untrusted content.

Mitigation: Run it in a constrained workspace, avoid untrusted paper HTML pages, and verify figure URLs before download.

Risk: Generated HTML reports may contain unsafe or poorly escaped content.

Mitigation: Treat generated HTML as untrusted until escaping and script controls are reviewed.

Risk: Dependency installation guidance is under-scoped and may use unpinned packages.

Mitigation: Prefer pinned local dependencies and review package installs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nuaalixu/skills/paper-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Chinese reading reports in HTML, Markdown, or DOCX, with extracted figure assets and supporting shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create workspace files such as downloaded paper inputs, extracted text, page images, figures, and final report files.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
