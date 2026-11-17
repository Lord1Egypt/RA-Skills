## Description:

Guides agents interacting with Kimi Group Chat or Sessions through required context reads, member awareness, message replies, file handling, and workspace-scoped group memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yurken](https://clawhub.ai/user/yurken)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when participating in Kimi group chats or sessions that require reading group rules, recent messages, and member context before responding. It helps keep replies, file transfers, and workspace-scoped memory updates aligned with the active group or thread.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read Kimi group context, members, recent messages, shared files, and workspace-scoped memory.

Mitigation: Review group rules and limit use to chats where the agent is authorized to access that context.

Risk: Downloaded shared files and stored group memory may contain untrusted content.

Mitigation: Treat downloaded files and memory entries as untrusted until verified, and scan or inspect them before acting on their contents.

Risk: The skill can send replies or files through kimiim-cli.

Mitigation: Follow the mandated context-read workflow and send only concise, task-relevant messages or files to the active group or thread.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yurken/skills/kimiim)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Plain text or Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kimi IM CLI commands, concise chat replies, downloaded files, attached files, and workspace memory notes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
