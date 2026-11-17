## Description:

Memory system v4.13: Dual-layer structure (todos for execution + knowledge for strategy) with Dream/Refinement memory mechanisms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jujitao](https://clawhub.ai/user/jujitao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an OpenClaw agent durable, structured memory for user preferences, corrections, project decisions, references, and periodic memory review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Durable memory may retain personal preferences, role details, corrections, and project decisions more broadly than expected.

Mitigation: Review the memory files before and after installation, and keep separate controls for deletion, review, and disabling recall.

Risk: Stored context may be inappropriate for secrets, regulated data, confidential client material, or settings where cross-conversation recall is not acceptable.

Mitigation: Do not use the skill with sensitive or regulated content unless independent controls prevent storage and recall of that material.

Risk: Recalled memories can become stale and conflict with the current workspace or user intent.

Mitigation: Verify referenced files, facts, and dates against current evidence before acting on memory-derived guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jujitao/skills/memory-never-forget)
- [Memory System v2.0 - Detailed Design](artifact/references/memory-v2.md)
- [Memory Writing Templates v2.0](artifact/references/templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces durable memory entries and recall guidance; users should review stored memory content before relying on it across conversations.]

## Skill Version(s):

4.1.3 (source: server release evidence; artifact text references v4.13 and artifact _meta.json lists 4.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
