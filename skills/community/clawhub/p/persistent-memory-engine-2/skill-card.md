## Description:

持久记忆引擎 guides agents in creating and maintaining a local ~/memory/ hierarchy for long-term project, people, decision, and knowledge memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill to initialize, write, retrieve, and maintain structured local memory for long-running projects, relationship notes, decision records, domain knowledge, and collections. It is intended for agent workflows that need persistent local context across sessions while avoiding built-in memory mutation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to create, update, archive, or delete long-term local memory files over time.

Mitigation: Require user confirmation for memory category setup, built-in memory sync, archival, deletion, and any operation that changes existing records.

Risk: Long-term memory may accidentally capture secrets, credentials, or sensitive personal data.

Mitigation: Define allowed memory categories before use and instruct the agent to exclude API keys, passwords, credentials, and sensitive personal data from ~/memory/.

Risk: The artifact contains inconsistent guidance about API keys, callback URLs, network checks, and optional external services.

Mitigation: Use the core local-memory workflow by default and ignore external-service guidance unless a user deliberately configures an optional vector or sync service.

Risk: Automatic retention and conflict-handling rules can preserve stale or conflicting information.

Mitigation: Schedule human review for weekly index maintenance, monthly archive decisions, and conflict merges before treating stored memory as current.

## Reference(s):

- [Artifact SKILL.md](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/persistent-memory-engine-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands, file paths, and agent-facing status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform local filesystem changes under ~/memory/ when the hosting agent has write access.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
