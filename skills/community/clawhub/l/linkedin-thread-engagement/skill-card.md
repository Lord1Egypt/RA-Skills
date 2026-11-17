## Description:

Monitor LinkedIn threads where the user commented for author replies and inbound signals, flag high-value engagement windows, draft follow-up responses, and optionally route dormant but meaningful threads to DM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergebulaev](https://clawhub.ai/user/sergebulaev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to monitor LinkedIn comment threads where they have participated, identify author replies within the highest-value response windows, and draft timely public replies or DMs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reviewing LinkedIn comments and thread activity may expose personal or sensitive professional context.

Mitigation: Confirm the user is comfortable with the workflow reviewing LinkedIn comment and thread data before use.

Risk: Connected posting backends may draft only or may be capable of publishing public replies or DMs.

Mitigation: Verify the active backend behavior and require explicit human approval before public replies or DMs are sent.

Risk: Overusing follow-ups, reply chains, or coordinated engagement patterns can create spam-like behavior.

Mitigation: Follow the skill's timing limits, avoid three or more chained replies under one comment, and use substantive non-reciprocal engagement only.

## Reference(s):

- [Thread Timing Matrix](references/thread-timing.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown reports with suggested response drafts, stage classifications, priorities, and timing guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include daily thread reports, warm-thread previews, reaction targets, weekly roll-ups, and DM draft guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
