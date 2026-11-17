## Description:

CLI tool to search, download, and parse academic papers from arXiv into AI-friendly Markdown using MinerU API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaihangyang](https://clawhub.ai/user/kaihangyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent operators use this skill to find arXiv papers, download paper assets, and convert PDFs into AI-friendly Markdown through the MinerU API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the external PyPI package executes third-party code on the user's system.

Mitigation: Install in a dedicated virtual environment or container and review the referenced source and exact package version before use.

Risk: The MinerU API token can authorize PDF parsing requests.

Mitigation: Use a dedicated, revocable token and keep it out of shared logs, repositories, and prompts.

Risk: PDFs and paper metadata are submitted to MinerU for processing.

Mitigation: Do not submit confidential, unpublished, or sensitive PDFs unless MinerU processing and data handling are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaihangyang/skills/paper-parser-skill)
- [PyPI package](https://pypi.org/project/paper-parser-skill/)
- [MinerU API service](https://mineru.net/)
- [Project homepage disclosed in artifact](https://github.com/KaiHangYang/paper-parser-skill)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and YAML configuration examples; parsed paper outputs are stored as local Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local config file at ~/.paper-parser/config.yaml and a MINERU_API_TOKEN for parsing.]

## Skill Version(s):

0.1.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
