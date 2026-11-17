## Description:

Microsoft Outlook calendar integration for managing calendars and events, including creating, updating, deleting, and listing events by date range through a MorphixAI proxy to Microsoft Graph API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paul-leo](https://clawhub.ai/user/paul-leo)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers can use this skill to let an agent inspect Outlook calendars, review schedules, and create, update, or delete calendar events after the required MorphixAI and Microsoft account setup is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an unpinned third-party plugin that receives MorphixAI API-key authority and connected Outlook calendar permissions.

Mitigation: Review the openclaw-morphixai plugin source, publisher, and version before installing, and prefer a pinned or verified release.

Risk: The connected integration can read calendar details and create, update, delete, or invite attendees to events.

Mitigation: Use a narrowly scoped, revocable MorphixAI API key and confirm the Microsoft account permissions before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paul-leo/skills/outlook-calendar-2)
- [MorphixAI API keys](https://morphix.app/api-keys)
- [MorphixAI connections](https://morphix.app/connections)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown with inline tool-call examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Outlook Calendar account.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
