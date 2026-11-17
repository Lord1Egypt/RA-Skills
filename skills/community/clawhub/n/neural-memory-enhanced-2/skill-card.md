## Description:

Neural Memory Enhanc helps agents use a local associative memory workflow with spreading activation, typed memory relationships, recall, context retrieval, and memory management commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure and operate NeuralMemory for persistent local recall of decisions, facts, preferences, tasks, errors, and related context across work sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can cause an agent to keep durable local memories from conversations without explicit consent or sensitivity limits.

Mitigation: Use it only after confirming what information may be stored, where the local database lives, and how memories can be deleted or isolated.

Risk: Secrets, credentials, regulated personal data, or confidential project details could be retained in memory.

Mitigation: Avoid using the skill with sensitive data unless retention policy, database access, and deletion controls have been reviewed.

Risk: Optional package, embedding, or LLM configuration could change where data is processed.

Mitigation: Verify the neural-memory package source and any optional embedding or LLM settings before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/neural-memory-enhanced-2)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown instructions with command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent to store, recall, summarize, and manage durable local conversation memories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
