## Description:

Operate Google Calendar to read, create, update, or delete calendar data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to find calendar information and manage events, calendars, attendees, or access rules through their connected Google Calendar account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may introduce persistent agent skills beyond Google Calendar.

Mitigation: Review the setup first, prefer a verified user-managed CLI, and decide whether startup skill synchronization should be disabled with OO_SKILLS_SYNC_DISABLED=1.

Risk: The remote installer and connector implementation were not verified, and the connected account may grant access to sensitive calendar data.

Mitigation: Review the Google Calendar permissions granted through OOMOL and confirm each calendar change before execution; require explicit approval for destructive actions.

## Reference(s):

- [Google Calendar API guide](https://developers.google.com/workspace/calendar/api/guides/overview)
- [Google Calendar](https://workspace.google.com/products/calendar/)
- [oo CLI commands and synchronization controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with JSON payloads and oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calendar changes require user confirmation; destructive actions require explicit approval.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
