## Description:

Provides ICP filing guidance for China websites, including filing workflows, document checklists, timelines, filing status query guidance, provincial ICP prefixes, and footer code snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and teams preparing China-hosted websites can use this skill to get concise ICP filing process guidance, document checklists, timeline expectations, and shell command outputs for related lookup and footer tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because it mixes an ICP filing guide with an unrelated persistent local utility that logs command inputs and has a misleading remove command.

Mitigation: Review the skill before installation, avoid passing secrets or sensitive business details as command arguments, and set ICP_FILING_DIR to an isolated directory if running the utility script.

Risk: The ICP helper provides local guidance and generated snippets that may become outdated or incomplete for a specific province, provider, or filing scenario.

Mitigation: Verify filing requirements and generated footer or query guidance against the relevant filing provider and official MIIT resources before publication or operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/icp-filing)
- [MIIT ICP filing portal](https://beian.miit.gov.cn/)
- [ChinaZ ICP lookup](https://icp.chinaz.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and stdout text with inline shell commands and optional HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local history and data files under ICP_FILING_DIR or ~/.local/share/icp-filing when the included utility script is used.]

## Skill Version(s):

2.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
