## Description:

Use at the end of any session that discovered durable knowledge (architecture decisions, root causes, setup gotchas, workflow changes, security findings, reusable patterns), or when the user says "hand off", "write a handoff", or "save this for the memory system".

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture durable session knowledge in a structured Markdown handoff for a memory owner to review and route. It applies when a session produces reusable findings or the user explicitly requests a handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Handoff notes may contain secrets or sensitive project details, or preserve inaccurate information.

Mitigation: Review each note for accuracy and sensitive content; redact it before sharing or promoting it into long-term memory.

## Reference(s):

- [ClawHub memory-handoff release](https://clawhub.ai/solomonneas/skills/memory-handoff)
- [Brigade project](https://github.com/escoffier-labs/brigade)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Files]

**Output Format:** [Structured Markdown handoff note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes durable facts, evidence, and memory-routing sections.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
