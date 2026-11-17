## Description:

Mem0 Memory provides a local semantic memory layer for storing, retrieving, updating, and reusing user, session, and agent memories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chircken891](https://clawhub.ai/user/chircken891)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent semantic memory workflows to an agent, including memory extraction, search, updates, history, batch deletion, and memory-augmented chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain conversation-derived facts and task state across sessions.

Mitigation: Install only where persistent memory is acceptable and users understand that remembered facts may be reused later.

Risk: Sensitive content could be stored or reused without enough user control or safety boundaries.

Mitigation: Avoid secrets, private URLs, credentials, sensitive business data, and prompt-like instructions unless consent, redaction, review/delete controls, and clear handling for MiniMax requests are added.

## Reference(s):

- [ClawHub Mem0 Memory release](https://clawhub.ai/chircken891/skills/mem0-memory)
- [ZejunCao/bilibili_code Mem0 framework reference](https://github.com/ZejunCao/bilibili_code)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce memory-management commands and guidance for add, search, update, delete, reset, and chat workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
