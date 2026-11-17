## Description:

Memory-to-Wisdom Engine for AI agents. Use this skill to give yourself long-term memory, extract user preferences/facts from conversations, and track wisdom evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengyi-thinking](https://clawhub.ai/user/zengyi-thinking)

### License/Terms of Use:


## Use Case:

Developers and agent operators use M2Wise to add long-term memory to agents, retrieve user-specific context before responding, and consolidate conversation-derived memories into reusable guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages automatic long-term storage and reuse of conversation-derived facts, preferences, and inferred guidance.

Mitigation: Require explicit opt-in, block secrets and sensitive categories from storage, and provide clear review, export, and deletion controls.

Risk: Stored memories or generated wisdom can preserve outdated, inaccurate, or overbroad assumptions about a user.

Mitigation: Review retrieved context before using it, scope memories by user and purpose, and allow users to correct or remove stored items.

Risk: API keys, dependencies, and API or MCP exposure can increase operational risk when the skill is connected to real users.

Mitigation: Protect API keys, pin dependency versions, and require authentication around API or MCP endpoints before deployment.

## Reference(s):

- [M2Wise Reference](artifact/REFERENCE.md)
- [M2Wise API Reference](artifact/references/api.md)
- [Memory Subsystem](artifact/references/memory.md)
- [Wisdom Subsystem](artifact/references/wisdom.md)
- [M2Wise Examples](artifact/EXAMPLES.md)
- [M2Wise on ClawHub](https://clawhub.ai/zengyi-thinking/skills/m2wise)
- [M2Wise on PyPI](https://pypi.org/project/m2wise/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce persisted memory records, retrieved context bundles, and wisdom summaries through SDK or MCP calls.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
