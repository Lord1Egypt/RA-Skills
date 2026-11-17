## Description:

Build a concise "what needs action now" daily brief by aggregating reminders from multiple channels, including email, calendar, SMS/iMessage, weather, and task notes, and prioritizing them into Must-do, Should-do, and Nice-to-have actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yikailucas](https://clawhub.ai/user/yikailucas)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and individual contributors use this skill to turn connected calendar, message, billing, weather, and task-note signals into a concise daily action brief. It helps prioritize urgent commitments, near-term follow-ups, and lower-priority reminders while marking uncertainty when source details are missing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The daily brief can consolidate sensitive calendar, message, billing, weather, and notes context into one summary.

Mitigation: Use only where those sources are intentionally connected, and ask the agent to exclude any source that should not be summarized.

Risk: Connected sources may omit dates, amounts, or account details needed for confident prioritization.

Mitigation: Mark missing details as unknown, downgrade uncertain items, and redact secrets, tokens, and full account numbers.

## Reference(s):

- [Life Radar Modes](references/modes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with prioritized action lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sections are limited to Must-do, Should-do, Nice-to-have, and suggested next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
