## Description:

激活并加载用户提供的 Markdown 记忆资料，使代理能够在对话中沿用用户的身份信息、知识和方法论。

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, developers, and knowledge workers use this skill to point an agent at a curated folder of personal Markdown notes so it can load identity, style, decisions, insights, and reusable methods during conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to read and persist personal Markdown memory files, which may expose sensitive notes if the memory folder is too broad.

Mitigation: Keep the configured memory folder limited to files intentionally shared with the agent, and exclude secrets, credentials, regulated data, and unrelated personal records.

Risk: .memory-path can point outside the workspace and expand what the agent can inspect.

Mitigation: Review .memory-path before use and prefer a dedicated, minimal memory directory with only approved Markdown files.

Risk: Saved conversation notes may preserve inaccurate or sensitive information for later reuse.

Mitigation: Review and edit memory updates before relying on them in future conversations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/markma84/skills/memory-palace-yu)
- [Core concept memory template](artifact/examples/memory/00-概念模板.md)
- [Daily memory template](artifact/examples/memory/日记录模板.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and memory file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for reading and updating user-managed Markdown memory files; no executable code is bundled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
