## Description:

Analyze the structure and content of HTML documents using MinerU, returning structured Markdown with layout information, headings, and content hierarchy preserved.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SEO analysts, and content auditors use this skill to inspect local or remote HTML structure and extract a Markdown representation of headings, sections, tables, lists, and layout hierarchy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTML content may be processed by a third-party MinerU/OpenDataLab service or tooling.

Mitigation: Avoid submitting confidential local files, private URLs, or internal pages unless that provider is approved for the data.

Risk: The required MINERU_TOKEN can be exposed through repositories, logs, screenshots, or shared shell sessions.

Mitigation: Store the token outside source control and avoid printing or sharing authenticated shell output.

Risk: Global or latest CLI installation can make behavior harder to reproduce.

Mitigation: Pin the mineru-open-api version or install it in an isolated environment.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the mineru-open-api CLI and requires MINERU_TOKEN for HTML extraction.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
