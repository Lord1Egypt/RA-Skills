## Description:

Pear Apple lets agents manage iCloud calendars, reminders, contacts, daily briefings, and AI scheduling through Pear's 27 CalDAV/CardDAV-backed Apple iCloud tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashtonau](https://clawhub.ai/user/ashtonau)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent manage iCloud calendars, reminders, contacts, daily briefings, and scheduling through Pear's CalDAV/CardDAV-backed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pear-mediated access can read and modify iCloud calendars, reminders, and contacts.

Mitigation: Install only if this access is acceptable, and confirm event updates, contact deletion, and other destructive or bulk actions before execution.

Risk: The PEAR_API_KEY authorizes access through Pear and could expose personal information if leaked.

Mitigation: Keep the API key secret, avoid exposing it in prompts or logs, and rotate it if it is disclosed.

Risk: Bulk event, reminder, or contact operations can affect many records at once.

Mitigation: Review counts and target records before running batch creates or deletes.

## Reference(s):

- [Pear Documentation](https://pearmcp.com/docs)
- [Pear](https://pearmcp.com)
- [Apple App-Specific Passwords](https://support.apple.com/en-us/102654)
- [CalDAV Protocol (RFC 4791)](https://www.rfc-editor.org/rfc/rfc4791)
- [CardDAV Protocol (RFC 6352)](https://www.rfc-editor.org/rfc/rfc6352)
- [IANA Time Zone Database](https://www.iana.org/time-zones)

## Skill Output:

**Output Type(s):** [text, guidance, API calls, configuration]

**Output Format:** [Markdown guidance with tool-call parameters and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PEAR_API_KEY and network access to pearmcp.com.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
