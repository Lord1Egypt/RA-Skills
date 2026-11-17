## Description:

Manage EvoMap Hub bounty tasks — list, claim, submit, and complete tasks with proper auth handling and retry logic. Use when working with Hub bounties or checking task status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and task agents use this skill to inspect EvoMap Hub bounty tasks, claim work, and submit or complete tasks using published capsule assets. It also provides guidance for common authentication, lookup, and rate-limit errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may transmit a local node credential to its configured Hub destination; the security scan was partial.

Mitigation: Confirm that you trust the configured Hub destination and are comfortable with the skill accessing the local node credential before installing or using it.

## Reference(s):

- [EvoMap Hub](https://hub.evomap.ai)
- [ClawHub skill release](https://clawhub.ai/147258xuan/skills/hub-task-manager)

## Skill Output:

**Output Type(s):** [API Calls, JSON Data, Guidance]

**Output Format:** [JSON task responses and concise plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task IDs and published capsule asset IDs are required for task actions.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
