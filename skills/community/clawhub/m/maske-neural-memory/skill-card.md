## Description:

An associative memory skill that helps an agent store, recall, and connect persistent conversation memories across sessions using spreading activation, causal links, contradiction checks, and recency-aware context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillforge-jojo](https://clawhub.ai/user/skillforge-jojo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users can use this skill when an agent should preserve decisions, facts, preferences, errors, todos, and prior context across conversations and retrieve related memories for future tasks or causal questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory may capture secrets, regulated data, customer information, or private project details.

Mitigation: Use the skill only where persistent memory is intended, avoid storing sensitive data, and require explicit confirmation before saving memories.

Risk: Memories may be reused across sessions or transferred across projects without sufficient user control.

Mitigation: Confirm with the user before recalling or transferring memories across project boundaries, and review stored context before using it in a new task.

Risk: Automatically captured memories may become stale, incomplete, or contradictory.

Mitigation: Prefer explicit user confirmation for important memories and review recalled context before relying on it for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillforge-jojo/skills/maske-neural-memory)
- [Publisher profile](https://clawhub.ai/user/skillforge-jojo)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown and structured tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memory recall depth ranges from 0 to 3; examples include priority and token-limit parameters.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
