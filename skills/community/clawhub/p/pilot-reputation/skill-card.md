## Description:

Advanced reputation analytics and trend visualization for Pilot Protocol agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to record Pilot Protocol peer reputation snapshots, query recent score history, and calculate trend changes for trust decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local snapshots may contain sensitive Pilot Protocol peer lists or reputation scores.

Mitigation: Restrict permissions on ~/.pilot/reputation and remove or rotate old snapshot files.

Risk: The example continuous collection loop can run indefinitely even though the skill is not intended for real-time monitoring.

Mitigation: Prefer manual or bounded snapshot collection and stop long-running collection when the analysis window is complete.

## Reference(s):

- [Pilot Protocol](https://pilotprotocol.network)
- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-reputation)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses pilotctl, jq, and bc; writes local reputation snapshot JSON under ~/.pilot/reputation/data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
