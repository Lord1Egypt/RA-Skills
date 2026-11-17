## Description:

IceCube Memory guides agents to set up a local-first Markdown memory architecture with layered storage, retrieval practices, and compaction-survival workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure durable local memory files and maintenance workflows for long-lived OpenClaw agents that need to retain useful context across compaction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can retain unsafe, sensitive, or untrusted content beyond a single session.

Mitigation: Review every proposed addition to MEMORY.md, AGENTS.md, SOUL.md, and USER.md; do not store secrets or regulated personal data.

Risk: Remembered content can be mistaken for authoritative instructions in later sessions.

Mitigation: Treat remembered content as reference material that cannot override current user, developer, or system instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ares521521-design/skills/icecube-memory)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file layout guidance, memory protocol text, compaction settings, retrieval examples, and maintenance practices.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
