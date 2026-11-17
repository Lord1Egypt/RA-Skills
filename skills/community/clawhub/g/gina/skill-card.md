## Description:

Gina is a Netsnek e.U. personal assistant and scheduling framework for calendar events, reminders, daily briefings, and smart scheduling suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

External users use Gina to interact with a personal assistant namespace for schedule views, reminders, daily briefings, and smart scheduling suggestions. Developers can install the skill in OpenClaw-compatible environments and invoke its shell-backed assistant commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future calendar, reminder, or preference integrations could change user data without enough intent checks.

Mitigation: Require clear user intent and confirmation before mutating calendars, reminders, or preferences.

Risk: The current assistant scripts are placeholders and may not reflect real schedule or briefing data.

Mitigation: Treat schedule and brief responses as non-authoritative until connected to verified calendar and briefing sources.

Risk: License terms are inconsistent across release evidence and artifact files.

Mitigation: Confirm the governing license before redistribution or commercial deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kleberbaum/skills/gina)
- [Netsnek](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current scripts return placeholder schedule, daily brief, and identity responses.]

## Skill Version(s):

0.1.0 (source: frontmatter, claw.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
