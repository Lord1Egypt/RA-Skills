## Description:

Hermes-style self-improvement and memory management for OpenClaw agents, including a learning loop, skill system, persistent memory, and overflow archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[protechsysipem-lang](https://clawhub.ai/user/protechsysipem-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add recurring session review, memory maintenance, and skill proposal workflows to OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring self-review jobs can read past sessions and retain profile or project details indefinitely.

Mitigation: Enable the skill only with explicit approval for memory changes and defined retention and deletion rules for USER.md, MEMORY.md, and overflow archives.

Risk: Automatic skill or memory updates can introduce unreviewed behavior into the agent workspace.

Mitigation: Require human approval for every skill and memory change, remove the 24-hour auto-apply path, and keep cron or heartbeat review disabled until controls are in place.

## Reference(s):

- [Aquila Hermes Features Reference](artifact/aquila-hermes-features.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with tool, schedule, and file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose recurring jobs, memory writes, and skill changes that require human review.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
