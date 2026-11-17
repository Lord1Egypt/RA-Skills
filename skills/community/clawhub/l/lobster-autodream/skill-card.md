## Description:

AI memory consolidation system that automatically organizes conversation history, extracts important information, and updates long-term memory during heartbeat checks or session compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to consolidate conversation history into concise long-term memory entries while applying time, content-volume, and quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically persist selected conversation details into long-term memory.

Mitigation: Install only when memory consolidation is desired, review or disable HEARTBEAT.md integration for automatic updates, and periodically inspect MEMORY.md for sensitive or stale entries.

## Reference(s):


## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with configuration snippets and memory-writing procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update MEMORY.md and daily memory notes when configured with heartbeat or session-compression triggers.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
