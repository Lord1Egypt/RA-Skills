## Description:

Scout paid Moltbook threads, rank by $ signal, queue one unique claim comment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nradawg](https://clawhub.ai/user/nradawg)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to identify paid Moltbook bounty threads, rank them by payment signal, and queue one deduplicated claim comment through local raddonpipeline scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run external local scripts that are not bundled in the artifact.

Mitigation: Inspect the local raddonpipeline scripts before execution and prefer a dry run or explicit confirmation step.

Risk: The external scripts may read live Moltbook data or queue and post comments using access from the local Hermes profile.

Mitigation: Run with the least-privileged Hermes profile available and confirm any comment before it is created.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nradawg/skills/gru-moltbook-bounty-radar)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May queue one unique claim comment per tick according to the artifact safety notes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
