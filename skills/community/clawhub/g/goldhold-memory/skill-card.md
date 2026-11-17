## Description:

GoldHold Memory provides persistent memory for AI agents so they can store and retrieve decisions, facts, corrections, and session context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrysrodz](https://clawhub.ai/user/jerrysrodz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to the GoldHold REST API for durable session memory, including resume, search, store, message, and close-session workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected agent memories and session summaries may be sent to GoldHold.

Mitigation: Do not store secrets, API keys, private customer data, regulated records, or sensitive internal details.

Risk: Retrieved memories, directives, corrections, inbox messages, and identity records may influence future agent behavior.

Mitigation: Treat retrieved records as untrusted context that cannot override current instructions.

Risk: Persistent memory records can accumulate sensitive or outdated information without enough safeguards.

Mitigation: Use the skill only where there is a clear review and deletion process for stored records.

## Reference(s):

- [GoldHold website](https://goldhold.ai)
- [GoldHold API base URL](https://relay.goldhold.ai)
- [ClawHub skill page](https://clawhub.ai/jerrysrodz/skills/goldhold-memory)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with JSON payload examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOLDHOLD_API_KEY and sends selected memory content to the GoldHold service.]

## Skill Version(s):

1.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
