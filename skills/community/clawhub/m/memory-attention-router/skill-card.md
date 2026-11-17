## Description:

Deterministic long-term memory routing for OpenClaw that routes, writes, reflects on, and refreshes reusable memory for multi-step agent work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiqiangh](https://clawhub.ai/user/kaiqiangh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give OpenClaw agents compact, role-aware working-memory packets from durable preferences, procedures, summaries, reflections, and prior task evidence. It also supports adding, reflecting on, and refreshing stored memories when new outcomes or user preferences should affect future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and reuse long-term agent memory across future sessions without strong confirmation, isolation, or trust boundaries.

Mitigation: Use an isolated database per user or project, avoid global memories by default, and require explicit user approval before saving or replacing durable preferences.

Risk: Shell invocation that interpolates JSON input can expose command-injection risk when caller-controlled content is used.

Mitigation: Invoke the Python script with argument arrays or stdin-style input handling instead of constructing shell strings.

Risk: Stale or conflicting memories can affect future routing decisions if replacement behavior is not used.

Mitigation: Use the refresh and replacement flows to deactivate stale memories, link replacements, and record retirement reasons when newer evidence supersedes old guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiqiangh/skills/memory-attention-router)
- [Reference Guide](references/REFERENCE.md)
- [Memory Schema](references/MEMORY_SCHEMA.md)
- [Prompt Templates](references/PROMPTS.md)
- [Testing Guide](references/TESTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and compact memory packet structures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The routed packet is designed to cap selected memory IDs, hard constraints, relevant facts, procedures, pitfalls, and open questions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
