## Description:

iCloud Calendar, Reminders & Contacts via Pear. Manage events, reminders, contacts, daily briefings, and AI scheduling. 27 tools for Apple iCloud via CalDAV/CardDAV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashtonau](https://clawhub.ai/user/ashtonau)

### License/Terms of Use:


## Use Case:

External users use this skill to let an agent read and manage their iCloud calendars, reminders, contacts, daily briefings, and meeting scheduling through Pear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires ongoing access to sensitive iCloud calendar, reminder, and contact data.

Mitigation: Install only when this access is acceptable, protect PEAR_API_KEY, and use an Apple app-specific password.

Risk: Delete, bulk, and update actions can permanently remove or change personal information.

Mitigation: Confirm delete and bulk actions with item names, dates, and counts before execution, and summarize updates before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ashtonau/skills/pear-icloud)
- [Pear Homepage](https://pearmcp.com)
- [Pear Documentation](https://pearmcp.com/docs)
- [Apple App-Specific Passwords](https://support.apple.com/en-us/102654)
- [CalDAV Protocol (RFC 4791)](https://www.rfc-editor.org/rfc/rfc4791)
- [CardDAV Protocol (RFC 6352)](https://www.rfc-editor.org/rfc/rfc6352)
- [IANA Timezone Database](https://www.iana.org/time-zones)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance, Configuration instructions]

**Output Format:** [Markdown or plain text responses with Pear MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEAR_API_KEY and network access to pearmcp.com.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
