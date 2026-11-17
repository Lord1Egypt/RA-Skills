## Description:

Manage the full meeting lifecycle by scheduling through Google Calendar, suggesting time slots, preparing briefs, generating agendas, and creating follow-up tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT-0

## Use Case:

Professionals and teams use this agent to schedule meetings, prepare meeting briefs and agendas, capture follow-ups, and review calendar health using Google Calendar plus optional Gmail, web, and local meeting-history context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad calendar, Gmail, web, and local meeting-history processing can expose sensitive attendee names, event details, email snippets, and meeting notes.

Mitigation: Install only when that access is acceptable, disable auto_prep, include_email_context, and include_web_search until needed, and review stored meeting notes regularly.

Risk: Calendar updates, task sync, and follow-up emails can affect real recipients and schedules.

Mitigation: Confirm exact recipients, event IDs, dates, message bodies, and task details before approving creates, updates, sends, or syncs.

Risk: The workflow depends on the gog CLI for Google Calendar and Gmail access.

Mitigation: Verify the gog CLI source and requested OAuth scopes before installing or authenticating it globally.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nollio/skills/meeting-scheduler-pro)
- [Publisher profile](https://clawhub.ai/user/nollio)
- [README](artifact/README.md)
- [Security considerations](artifact/SECURITY.md)
- [Setup prompt](artifact/SETUP-PROMPT.md)
- [Dashboard specification](artifact/dashboard-kit/DASHBOARD-SPEC.md)
- [OpenClaw](https://openclaw.com)
- [NormieClaw](https://normieclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, calendar actions, configuration updates, meeting notes, agenda drafts, and follow-up email/task drafts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write Google Calendar through gog, optionally query Gmail and web context, and persist meeting notes as local markdown files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and dashboard manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
