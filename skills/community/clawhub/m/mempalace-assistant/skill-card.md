## Description:

MemPalace记忆系统助手 - 基于老四的AI记忆系统。提供结构化记忆存储、快速检索、记忆组织等功能。适用于需要持久化知识、跨会话记忆、语义搜索等场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to help an AI agent store, retrieve, list, and export structured memories across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may expose secrets, credentials, or sensitive personal data if users store them.

Mitigation: Avoid storing sensitive data unless the storage location and later list/export access are understood.

Risk: Retrieved memories may be outdated, irrelevant, or unintended for the current task.

Mitigation: Review search, list, and export results before relying on them in an agent workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/mempalace-assistant)
- [Publisher profile](https://clawhub.ai/user/534422530)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May interact with local persistent memory storage through explicit mempalace commands.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
