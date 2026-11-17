## Description:

飞书审批 API：审批实例、审批任务管理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Feishu/Lark approval schemas and manage approval instances and tasks through lark-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change real Feishu/Lark approval workflows by approving, rejecting, canceling, transferring, adding signers, sending reminders, or rolling back approval tasks.

Mitigation: Require explicit user confirmation before any write action and inspect the relevant lark-cli schema before submitting parameters.

## Reference(s):

- [ClawHub skill page: lark-approval](https://clawhub.ai/gu2003li/skills/lark-approval)
- [ClawHub publisher profile: gu2003li](https://clawhub.ai/user/gu2003li)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API method guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires lark-cli; instructs agents to inspect schemas before calling approval APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
