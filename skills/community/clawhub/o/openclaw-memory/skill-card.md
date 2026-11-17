## Description:

Persistent, locally stored semantic memory for agents with automatic learning, searchable facts, and optional paid unlimited retention across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atlaspa](https://clawhub.ai/user/atlaspa)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give OpenClaw agents persistent memory across sessions, semantic retrieval of stored facts and preferences, local memory management, and optional paid unlimited retention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically stores conversation-derived memories, which may include sensitive user, project, or regulated data.

Mitigation: Review before installing, configure retention deliberately, and avoid storing secrets or regulated data in agent conversations handled by this skill.

Risk: The default embedding provider can send memory text and search queries to OpenAI, which conflicts with broad local-only privacy expectations.

Mitigation: Use the local embedding provider unless the operator explicitly accepts remote embedding API processing for memory content and queries.

Risk: The dashboard and REST APIs expose memory and payment operations with weak scoping around wallet identifiers.

Mitigation: Keep the dashboard local or place it behind authentication, and do not expose the API on an untrusted network.

Risk: Agent-controlled x402 payment flows can involve funded wallets and irreversible transactions.

Mitigation: Require explicit spending caps and human approval for funded wallets, and verify payment behavior before enabling Pro-tier automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atlaspa/skills/openclaw-memory)
- [README](artifact/README.md)
- [Agent payments guide](artifact/AGENT-PAYMENTS.md)
- [Implementation summary](artifact/IMPLEMENTATION-SUMMARY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with CLI commands, REST API examples, local configuration guidance, and generated memory context for agent requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store and retrieve local SQLite memories, inject retrieved memories into agent request context, and expose CLI and dashboard/API workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
