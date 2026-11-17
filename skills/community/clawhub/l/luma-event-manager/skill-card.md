## Description:

Luma Event Manager for Clawdbot helps users discover Luma events by topic or location, view event details and guest lists, manage RSVPs, and sync events to Google Calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariovallereyes](https://clawhub.ai/user/mariovallereyes)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Luma event discovery, attendee workflows, host guest-list checks, RSVP updates, and optional Google Calendar sync from a Clawdbot interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses raw Luma session cookies and can access private event and guest-list data.

Mitigation: Install only when ongoing cookie access is acceptable, store cookies in a password manager, and rotate or remove the cookies when access is no longer needed.

Risk: RSVP and calendar tools can change external state.

Mitigation: Review the exact event slug, RSVP response, Google account, and calendar target before approving those actions.

Risk: Web scraping selectors and Luma endpoints may change.

Mitigation: Check returned event details before acting on them and update the skill when scraping or RSVP behavior degrades.

Risk: Dependencies may age after release.

Mitigation: Review and update dependencies before use in a sensitive environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mariovallereyes/skills/luma-event-manager)
- [Luma](https://lu.ma)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON-like tool results and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include event lists, event details, RSVP status, calendar sync status, setup instructions, and actionable error messages.]

## Skill Version(s):

2.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
