## Description:

Analyze the structure and content of PowerPoint (.pptx) presentations using MinerU, returning structured Markdown with slide content, headings, and layout preserved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content reviewers, presentation auditors, and automated quality checks use this skill to inspect PowerPoint decks, understand slide structure, and extract presentation content into Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing confidential slide decks or private URLs through third-party MinerU/OpenDataLab tooling may expose sensitive presentation content.

Mitigation: Confirm the service's data-handling terms before use and avoid confidential decks unless those terms meet the deployment requirements.

Risk: Installing the MinerU CLI with unpinned package commands can introduce unreviewed dependency changes.

Mitigation: Use a pinned, reviewed CLI version in an isolated environment and expose only the MINERU_TOKEN required by this tool.

## Reference(s):

- [PPTX Analysis on ClawHub](https://clawhub.ai/mzlzyca/skills/pptx-analysis)
- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU API Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write extracted Markdown to stdout or to an output directory when the MinerU CLI is invoked with -o.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
