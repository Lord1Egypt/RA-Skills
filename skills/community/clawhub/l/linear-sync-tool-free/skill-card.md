## Description:

管理Linear任务与项目的免费命令行工具，支持任务列表、查看与基础创建。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, individual contributors, and teams use this skill to query Linear issues, review team and project information, and create basic Linear issues from an agent-assisted command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill's permissions and activation scope are broader than expected for its stated purpose.

Mitigation: Review the skill before installation and invoke it only for explicit Linear CLI workflows.

Risk: Linear workspaces can contain sensitive team, project, and issue data.

Mitigation: Use least-privilege Linear API credentials, avoid hardcoding tokens, and review command output before sharing it.

Risk: Issue creation changes Linear workspace state.

Mitigation: Confirm create commands, target teams, and issue content before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/linear-sync-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Linear CLI command suggestions, query results, task creation steps, and error-handling guidance.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
