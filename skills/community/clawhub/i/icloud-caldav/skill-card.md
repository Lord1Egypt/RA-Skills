## Description:

Direct iCloud Calendar integration via CalDAV protocol. Create, read, update, and delete calendar events without third-party services. Use when the user wants to manage their iCloud Calendar, check schedule, create events, or find free time. Requires Apple ID and app-specific password.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samuelhe52](https://clawhub.ai/user/samuelhe52)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage iCloud Calendar events directly from an agent session, including listing calendars, checking upcoming events, creating events, and deleting events. It is intended for iCloud calendars and requires an Apple ID with an app-specific password.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Apple account credentials through an app-specific password.

Mitigation: Use a revocable Apple app-specific password, keep credentials in environment variables, and revoke the password when access is no longer needed.

Risk: Calendar deletion actions are destructive and may remove the wrong event if the target is not verified.

Mitigation: List and confirm the exact calendar event before deletion, prefer UID-based targeting, and avoid delete operations unless the event target is clear.

Risk: The security review notes insufficient safeguards around Apple CalDAV host validation, deletion filenames, UID matching, and destructive-action confirmation.

Mitigation: Review the installed version before use and prefer a version that validates Apple CalDAV hostnames, restricts deletion filenames to safe .ics basenames, parses UID values exactly, and confirms destructive actions.

## Reference(s):

- [CalDAV Protocol Reference](references/caldav-protocol.md)
- [RFC 4791: CalDAV](https://tools.ietf.org/html/rfc4791)
- [RFC 5545: iCalendar](https://tools.ietf.org/html/rfc5545)
- [Apple Support: App-Specific Passwords](https://support.apple.com/en-us/102654)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APPLE_ID and APPLE_APP_PASSWORD environment variables; calendar changes are sent to Apple's CalDAV service over HTTPS.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
