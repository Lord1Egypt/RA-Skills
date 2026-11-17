## Description:

A structured decision framework for embodied navigation using Goal Tree, Current State Tree, and Future Tree analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the0xka1](https://clawhub.ai/user/the0xka1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and embodied-agent operators use this skill to guide Habitat-GS navigation decisions by structuring goals, current observations, and candidate actions before selecting the next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to write long-term episode notes or change skill files without clear approval.

Mitigation: Require explicit user approval before memory writes, skill-file updates, or new-skill creation.

Risk: Stored episode lessons may become untrusted instructions in later sessions.

Mitigation: Treat saved lessons as evidence only, review them before reuse, and do not let them override higher-priority instructions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/the0xka1/skills/philosophical-three-questions)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown decision notes with a selected navigation action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include episode summaries and lessons for memory when explicitly approved.]

## Skill Version(s):

0.1.0 (source: SKILL.md metadata.version and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
