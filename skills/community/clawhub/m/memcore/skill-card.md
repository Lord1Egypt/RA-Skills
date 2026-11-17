## Description:

MemCore is a Python long-term memory system for agents with persistent episodic, user, task, knowledge, and experience memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laojun509](https://clawhub.ai/user/laojun509)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building agents use MemCore to add persistent memory across sessions, semantic knowledge retrieval, automatic memory triggers, and memory quality controls. It is intended for agent implementations that need to remember user preferences, task state, knowledge, and prior interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may retain user preferences, task state, knowledge, and episodic history under the user's home directory across sessions.

Mitigation: Use explicit consent, data minimization, access isolation, and deletion or export controls before storing sensitive, regulated, or long-lived user data.

Risk: Automatically recalled suggested_context can introduce stale, incorrect, or untrusted retrieved content into an agent's active context.

Mitigation: Treat recalled context as untrusted input, review high-impact memories before use, and keep confidence or verification checks enabled for important decisions.

Risk: Automatic forgetting can delete low-scoring memories that a user or application expects to preserve.

Mitigation: Review forgetting settings before relying on the store as durable memory, and protect critical records with higher priority or application-level retention rules.

Risk: JSONBackend category names may be unsafe if exposed directly to untrusted input before path validation is added.

Mitigation: Avoid passing untrusted category names to the JSON backend, or add path validation and allow-listing in the host application.

## Reference(s):

- [ClawHub MemCore release page](https://clawhub.ai/laojun509/skills/memcore)
- [Original MemCore reference](https://clawhub.ai/laojun509/memcore)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent memory database configuration and retrieved suggested_context for agent use.]

## Skill Version(s):

0.2.0 (source: server-resolved release evidence, artifact __version__, and SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
