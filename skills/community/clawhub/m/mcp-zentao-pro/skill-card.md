## Description:

禅道(ZenTao) MCP大模型能力扩展包。提供跨项目的数据聚合视图、一句话生成任务、无缝报工(Log Effort)、自动状态流转等四组原生能力。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenish](https://clawhub.ai/user/chenish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and AI agents use this skill to inspect ZenTao tasks, bugs, stories, team workload, standup risks, and weekly delivery summaries. With user authorization, it can also create tasks, log effort, and update task, story, or bug status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live ZenTao project records, including creating tasks, logging effort, reassigning work, updating statuses, and creating iterations.

Mitigation: Require explicit user confirmation before any create, update, reassignment, effort logging, or automatic iteration creation.

Risk: Installation and credential handling patterns may expose users to unreviewed package versions or command-line password leakage.

Mitigation: Review and pin the npm package source/version, use a least-privileged ZenTao account, and avoid putting passwords on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenish/skills/mcp-zentao-pro)
- [Publisher profile](https://clawhub.ai/user/chenish)
- [npm package @chenish/zentao-mcp-agent](https://www.npmjs.com/package/@chenish/zentao-mcp-agent)
- [GitHub issues](https://github.com/chenish/mcp-zentao-pro/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or structured text with inline command examples and ZenTao task, bug, story, workload, standup, or weekly summary data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute ZenTao CLI/tool actions after user authorization; mutating actions should require explicit confirmation.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
