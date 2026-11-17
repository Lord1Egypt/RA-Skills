## Description:

组织知识审计、分类体系设计与文档模板管理，将隐性经验转化为可检索的组织智能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

个人用户和团队使用此技能审计知识库、设计分类体系、生成文档模板，并规划关键知识提取工作。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags broad command execution and automation/API/file behavior for a loosely defined knowledge-management task.

Mitigation: Use the skill in a constrained workspace and require confirmation before shell commands, package installs, external API calls, or file writes.

Risk: Knowledge-management outputs may contain incorrect audit findings, templates, or knowledge-retention recommendations.

Mitigation: Have a responsible team member review generated guidance before adding it to an organizational knowledge base or workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/knowledge-mgmt-tool-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured examples, inline code, and shell/Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file reads or writes, package installs, external API calls, and command execution; confirm privileged actions before running.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
