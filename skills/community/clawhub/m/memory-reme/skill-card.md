## Description:

Memory-reme provides persistent cross-session memory, automatic user preference application, and intelligent context compression for OpenClaw using ReMe.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minybear](https://clawhub.ai/user/minybear)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to retrieve and apply persistent user preferences, record corrections, and preserve continuity during long or repeated sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived memories can persist sensitive data or stale behavioral rules across sessions.

Mitigation: Avoid storing secrets or sensitive client data, and periodically inspect and delete stored memories.

Risk: Automatic preference application can change future agent behavior without enough user control.

Mitigation: Require explicit approval before saving or applying behavioral rules, and review remembered preferences before use.

Risk: The skill depends on the third-party reme-ai package and ReMe API processing conversation content.

Mitigation: Pin and review reme-ai before deployment, and install only where ReMe API processing is acceptable.

## Reference(s):

- [Memory Structure Guide](references/memory-structure.md)
- [Best Practices for Memory Management](references/best-practices.md)
- [Common User Preferences Reference](references/common-prefs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local memory files and the third-party reme-ai package.]

## Skill Version(s):

1.0.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
