## Description:

Feishu App Bot (open.feishu.cn). Use this skill for ANY Feishu App Bot request — reading, creating, updating, and deleting data. Whenever a task involves Feishu App Bot, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other Feishu users use the skill to read and manage Feishu content and resources through natural language tasks. It guides the agent to inspect action requirements, then read, create, update, or delete items such as messages, documents, sheets, tasks, and calendar events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses downloads that were not verified, and the CLI may change other agents’ skills during its first invocation.

Mitigation: Review setup before installation, use a separately verified CLI release, and set OO_SKILLS_SYNC_DISABLED=1 before first invocation if you want to prevent skill synchronization.

Risk: Feishu permissions may expose or allow changes to more content than a task needs, and transferred content is handled by OOMOL.

Mitigation: Limit Feishu permissions to the task’s needs and consider OOMOL’s handling of transferred content.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Feishu Open Platform](https://open.feishu.cn)
- [Feishu message creation API](https://open.feishu.cn/document/server-docs/im-v1/message/create)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands; JSON API payloads and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions can run directly; actions that change or delete data require user confirmation.]

## Skill Version(s):

1.0.11 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
