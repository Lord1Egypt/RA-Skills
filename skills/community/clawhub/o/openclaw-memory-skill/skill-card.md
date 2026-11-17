## Description:

MongoDB-backed long-term semantic memory for recalling, storing, searching, and managing facts, decisions, and user preferences across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrlynn](https://clawhub.ai/user/mrlynn)

### License/Terms of Use:

MIT

## Use Case:

Agents and developers use this skill to give OpenClaw agents persistent, searchable memory across sessions, including prior decisions, user preferences, project facts, and session summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory capture can persist preferences, decisions, and session summaries, including content users may not intend to retain.

Mitigation: Review or disable automatic hooks when conversations may include secrets, regulated data, or untrusted content.

Risk: Persistent memory and local daemon behavior can retain searchable information across sessions.

Mitigation: Install only when long-term memory is desired, prefer pinned and reviewed plugin versions, and run the daemon in a constrained local or containerized environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrlynn/skills/openclaw-memory-skill)
- [Publisher profile](https://clawhub.ai/user/mrlynn)
- [Repository listed in skill documentation](https://github.com/mrlynn/openclaw-mongodb-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation with JSON, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers memory search, storage, deletion, listing, health checks, automatic hooks, daemon setup, and configuration.]

## Skill Version(s):

0.2.1 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
