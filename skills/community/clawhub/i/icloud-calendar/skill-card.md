## Description:

Add events to iCloud Calendar via CalDAV. Syncs to iPhone automatically with alarm reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teenlucifer](https://clawhub.ai/user/teenlucifer)

### License/Terms of Use:

MIT License

## Use Case:

External users and developers use this skill to let an agent create iCloud Calendar events with reminders through the user's own Apple account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles iCloud credentials and can write events to a user's iCloud Calendar.

Mitigation: Use only an Apple app-specific password, keep credentials in local environment configuration, and review intended calendar writes before execution.

Risk: Help or invalid invocations may create calendar entries.

Mitigation: Avoid running the script without valid event arguments until that behavior is fixed.

Risk: User-provided calendar text may be written into iCalendar content without robust escaping.

Mitigation: Avoid untrusted event text or serialize event content with a proper iCalendar library before relying on the skill for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teenlucifer/skills/icloud-calendar)
- [Apple app-specific password setup](https://appleid.apple.com)
- [iCloud CalDAV endpoint](https://caldav.icloud.com)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ICLOUD_EMAIL and ICLOUD_PASSWORD for authenticated calendar writes.]

## Skill Version(s):

0.1.0 (source: _meta.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
