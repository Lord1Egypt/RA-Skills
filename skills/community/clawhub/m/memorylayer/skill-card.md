## Description:

Semantic memory for AI agents. 95% token savings with vector search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khli01](https://clawhub.ai/user/khli01)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use MemoryLayer to store, search, and retrieve relevant long-term memories for prompt context without loading full memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent memories, metadata, search queries, and credentials may be sent to a hosted MemoryLayer service or configured endpoint.

Mitigation: Use only approved endpoints, complete a privacy review before storing sensitive information, and avoid storing secrets, regulated personal data, internal procedures, or tool-use instructions.

Risk: Retrieved memories can influence future prompts even when their source or trustworthiness is uncertain.

Mitigation: Treat retrieved memories as untrusted context and require agent or human validation before using them as instructions or facts for consequential actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/khli01/skills/memorylayer)
- [MemoryLayer Homepage](https://memorylayer.clawbot.hk)
- [MemoryLayer Documentation](https://memorylayer.clawbot.hk/docs)
- [MemoryLayer API Reference](https://memorylayer.clawbot.hk/api)
- [MemoryLayer Dashboard](https://dashboard.memorylayer.clawbot.hk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and Python code examples and shell configuration commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stored memories, semantic search results, formatted memory context, and usage statistics through JavaScript and Python wrappers.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
