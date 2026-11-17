## Description:

HeartFlow is a cognitive engine for AI agents that provides self-reflection, dream-based experience synthesis, emergent personality, memory, reasoning, and self-healing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local cognitive-engine capabilities to AI agents, including reflection, memory retrieval, dream-style synthesis, reasoning checks, CLI commands, and MCP-accessible tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local cognitive and memory features can store conversation traces.

Mitigation: Install only when persistent memory is intended, review stored memories regularly, and delete records that should not persist.

Risk: Code-execution dispatch routes can expand the impact of untrusted prompts or inputs.

Mitigation: Keep code-execution routes disabled or isolated unless explicitly needed, and review requested actions before running them.

Risk: The memory-to-system-prompt plugin can inject stored content into future agent context.

Mitigation: Treat memory injection as high-risk, enable it only for trusted workflows, and audit stored content before use.

Risk: The HTTP MCP server exposes a persistent local service.

Mitigation: Bind the MCP server to localhost and avoid exposing it beyond the local machine.

## Reference(s):

- [HeartFlow README](README.md)
- [Agent Integration Guide](AGENTS.md)
- [Skill Definition](SKILL.md)
- [Changelog](CHANGELOG.md)
- [Audit Zombie Reference Script](references/audit-zombie.js)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, plain text, JSON tool responses, and shell commands depending on the interface used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent-facing output; some interfaces can read or write local memory state when enabled.]

## Skill Version(s):

2.10.1 (source: SKILL.md frontmatter, package.json, CHANGELOG, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
