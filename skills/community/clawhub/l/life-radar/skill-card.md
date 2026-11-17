## Description:

Build a concise "what needs action now" daily brief by aggregating reminders from multiple channels (email, calendar, SMS/iMessage, weather, and task notes) and prioritizing them into Must-do / Should-do / Nice-to-have.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:


## Use Case:

Employees and individual users use this skill to turn calendar events, urgent messages, billing notices, weather impacts, and task notes into a concise prioritized daily action brief. It can adapt prioritization for CEO, department lead, or individual contributor perspectives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The brief may aggregate sensitive messages, calendar items, billing notices, weather context, and notes into one visible summary.

Mitigation: Review results in private contexts and limit connected sources when financial, message, or personal content should not be included.

Risk: Unavailable or incomplete source data may produce uncertain priorities, deadlines, or amounts.

Mitigation: Skip unavailable sources, mark missing dates or amounts as unknown, downgrade uncertain items, and verify critical actions before acting.

## Reference(s):

- [Life Radar Modes](artifact/references/modes.md)
- [Life Radar on ClawHub](https://clawhub.ai/yikailucas/skills/life-radar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown action brief with prioritized sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits output to concise Must-do, Should-do, Nice-to-have, and suggested next action sections.]

## Skill Version(s):

0.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
