## Description:

Family household coordinator: calendar, briefings, kids' meals, school email, groceries, health log, receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hchawla](https://clawhub.ai/user/hchawla)

### License/Terms of Use:

MIT-0

## Use Case:

Families and their agents use this skill to coordinate household logistics through local tools for calendars, school email queues, meal planning, groceries, health logs, receipts, weather, and trip preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queued school email-derived events can be written to Google Calendar without a technical approval gate.

Mitigation: Call confirm_pending_school_events only after explicit family approval for the exact pending events, and keep automated runners from invoking it without that check.

Risk: The skill stores family PII locally in configuration and household state files.

Mitigation: Keep config.json private, use restrictive file permissions, and review local state files before sharing or publishing an installation.

Risk: Gmail and Google Calendar access depends on the external gog integration.

Mitigation: Install only when the operator is comfortable granting gog those permissions, and verify gog authentication status during setup and maintenance.

## Reference(s):

- [Homebase skill page](https://clawhub.ai/hchawla/skills/homebase)
- [Agent tool reference](references/agent.md)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI tool responses as JSON or concise text; documentation as Markdown with shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON state and depends on Python 3.12+ plus the external gog CLI for Gmail and Google Calendar access.]

## Skill Version(s):

0.6.1 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
