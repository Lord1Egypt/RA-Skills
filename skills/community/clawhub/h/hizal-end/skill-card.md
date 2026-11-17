## Description:

Close the agent's context session and consolidate what was learned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parkerscobey](https://clawhub.ai/user/parkerscobey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to end a work session, review surfaced memory chunks, and decide whether each should remain personal memory, be promoted to project memory, or be discarded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write promoted chunks into persistent project memory.

Mitigation: Review each promoted chunk carefully and require explicit approval before project memory writes.

Risk: The skill can delete source context after promotion.

Mitigation: Require explicit approval before source-context deletion and keep original agent memory when promotion is uncertain.

Risk: Untrusted files or conversations may produce memory chunks that should not become project knowledge.

Mitigation: Avoid promoting content from untrusted sources and discard chunks that are noisy, one-off, or not suitable for shared memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parkerscobey/skills/hizal-end)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces end-of-session memory review guidance and command examples for keep, promote, and discard decisions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
