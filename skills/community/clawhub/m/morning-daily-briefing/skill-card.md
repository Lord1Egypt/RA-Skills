## Description:

Creates a morning briefing with priorities, calendar, and key updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Employees and individual users use this skill to generate concise daily briefings that summarize schedule items, priorities, inbox highlights, follow-ups, relevant news, and optional evening recaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can gather sensitive calendar, email, CRM, task, and note details through broad triggers or optional automatic runs.

Mitigation: Use explicit source permissions, prefer a named daily briefing command, and keep any automated delivery to a private destination.

Risk: Briefings may expose inbox, follow-up, schedule, or note details if shared too broadly.

Mitigation: Limit outputs to the requesting user or a private workspace, and skip unavailable sources instead of fabricating missing information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/morning-daily-briefing)
- [Context packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown daily briefing or evening recap]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize calendar, email, CRM, task, note, news, and weather information when the agent has explicit access to those sources.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
