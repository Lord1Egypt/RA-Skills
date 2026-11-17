## Description:

NARRA is a 5-file memory system that gives agents identity continuity through curated narrative instead of fragmented database lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install a narrative memory architecture for agents that need a stable identity, concise operational memory, and periodic consolidation of logs into curated first-person history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent identity and behavior files can steer future agent behavior beyond a single session.

Mitigation: Review all proposed changes to AGENTS.md, HEARTBEAT.md, IDENTITY.md, ORIGIN.md, NARRATIVE.md, MEMORY.md, and generated memory files before accepting them, and keep generated memory lower priority than system, developer, and user instructions.

Risk: Log, transcript, and memory review may expose secrets or confidential content during consolidation.

Mitigation: Limit which logs and transcripts may be read, redact sensitive content before consolidation, and treat generated memory as reference data rather than authoritative instruction.

## Reference(s):

- [IDENTITY.md Template](references/IDENTITY-template.md)
- [NARRATIVE.md Template](references/NARRATIVE-template.md)
- [ORIGIN.md Template](references/ORIGIN-template.md)
- [ClawHub Skill Page](https://clawhub.ai/di5cip1e/skills/narra-memory-system)
- [ClawHub Publisher Profile](https://clawhub.ai/user/di5cip1e)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and ordered setup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and revises persistent memory files such as IDENTITY.md, ORIGIN.md, NARRATIVE.md, MEMORY.md, memory/events/, AGENTS.md, and HEARTBEAT.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
