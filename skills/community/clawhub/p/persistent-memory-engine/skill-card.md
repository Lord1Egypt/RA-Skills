## Description:

Provides an agent workflow for durable local memory under ~/memory, using structured Markdown entries, layered indexes, retrieval guidance, lifecycle maintenance, and conflict versioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve long-running project, people, decision, collection, and domain knowledge records across sessions in local Markdown files. It is intended for agent workflows that need searchable, durable context without modifying the agent's built-in memory file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store broad conversational and people-related information durably.

Mitigation: Require explicit approval for the exact content of each saved memory entry and periodically review, archive, or delete stored records.

Risk: Credentials, sensitive personal data, or third-party profiles could be written into persistent local memory.

Mitigation: Do not store API keys, passwords, secrets, sensitive personal data, or third-party profiles; use dedicated secret or records-management tools instead.

Risk: The artifact includes inconsistent API and network guidance for a primarily local-memory skill.

Mitigation: Keep the skill in local-only mode by default and disable or ignore optional API and network features unless intentionally configured.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/persistent-memory-engine)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent to create and update local Markdown memory files under ~/memory.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
