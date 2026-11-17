## Description:

Record corrections with evidence, verify the fix and retrieve relevant lessons before another task. Use for Agent Lessons Journal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers use this skill to record corrections they explicitly want retained, verify fixes, and retrieve relevant lessons before another task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Journal entries and exported reports are stored locally without application-level encryption and may contain sensitive information.

Mitigation: Save only corrections intended for retention, omit passwords and other secrets, and keep the host sandbox enabled.

## Reference(s):

- [Agent Lessons Journal on ClawHub](https://clawhub.ai/hznetnewpower/skills/mochi-agent-lessons)
- [MochiLab](https://mochilab.bz)
- [Action contract](references/input.md)

## Skill Output:

**Output Type(s):** [Files, JSON, HTML, Guidance]

**Output Format:** [Structured lesson records and JSON or HTML review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review reports are saved under exports/ in the current agent workspace; lesson records remain in local state.]

## Skill Version(s):

1.0.1 (source: SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
