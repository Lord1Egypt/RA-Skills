## Description:

Converts local HTML files or web page URLs into clean Markdown using MinerU.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzlzyca](https://clawhub.ai/user/mzlzyca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to convert HTML pages or local HTML files into Markdown for documentation, migration, publishing, and archiving workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses MinerU's third-party CLI.

Mitigation: Use a pinned or isolated install when possible and avoid running the CLI with elevated privileges.

Risk: Conversion requires a MinerU token and processes the files or URLs supplied to the workflow.

Mitigation: Treat MINERU_TOKEN as a secret and only pass files or URLs intended for conversion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mzlzyca/skills/html2markdown)
- [MinerU](https://mineru.net)
- [OpenDataLab MinerU GitHub Repository](https://github.com/opendatalab/MinerU)
- [MinerU Token Management](https://mineru.net/apiManage/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; converted content is Markdown text or files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mineru-open-api CLI and a MINERU_TOKEN.]

## Skill Version(s):

0.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
