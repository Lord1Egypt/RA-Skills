## Description:

Receive a prior session handoff and continue execution safely by validating repo state, resuming from next steps, and refreshing the handoff artifact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Handoff Receiver to take over an existing project handoff, validate repository state against the handoff, resume the recorded next steps, and refresh handoff metadata before yielding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may continue work from an unreviewed or stale handoff, causing the agent to follow outdated goals or next steps.

Mitigation: Review the active handoff contents and compare them with repository state before executing.

Risk: The skill may update handoff metadata or status files in the repository.

Mitigation: Confirm the active handoff path and keep changes limited to the selected handoff stream.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown status summaries with inline shell commands and repository update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to read and update project handoff files.]

## Skill Version(s):

1.3.2 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
