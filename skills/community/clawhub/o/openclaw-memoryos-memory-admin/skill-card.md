## Description:

Inspect, back up, search, export, and update OpenClaw long-term memory stored with MemoryOS for OpenClaw-style agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this skill to inspect, back up, search, export, and intentionally update MemoryOS long-term memory files used by OpenClaw-style agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can administer sensitive long-term MemoryOS files, including user profiles and durable user or assistant knowledge.

Mitigation: Install only when that administration is intended, use trusted data roots and identifiers, and treat generated exports as private data.

Risk: Mutating commands can append knowledge or replace a synthesized user profile.

Mitigation: Back up memory files before writes, search for existing related entries first, and require an explicit user request before mutation.

Risk: Under-scoped path and identifier handling can broaden access beyond the intended memory records.

Mitigation: Prefer a hardened version that confines paths, validates user_id and assistant_id values, and disables implicit invocation.

## Reference(s):

- [MemoryOS Long-Term Memory Layout](references/memoryos-layout.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON summaries and Markdown exports from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference private MemoryOS profile and knowledge data; exports should be handled as sensitive user data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
