## Description: <br>
Direct iCloud Calendar integration via CalDAV protocol. Create, read, update, and delete calendar events without third-party services. Use when the user wants to manage their iCloud Calendar, check schedule, create events, or find free time. Requires Apple ID and app-specific password. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samuelhe52](https://clawhub.ai/user/samuelhe52) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to manage iCloud Calendar data directly from the local environment, including listing calendars and events, creating events, deleting events, and checking schedule availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete iCloud calendar events, and the security review notes under-scoped destructive authority. <br>
Mitigation: Install only if iCloud calendar access is acceptable; before deletion, list or preview the target event and verify the UID, filename, and calendar yourself. <br>
Risk: The skill requires Apple ID app-specific credentials for calendar access. <br>
Mitigation: Provide credentials only through environment variables, avoid exposing them in prompts or logs, and revoke the app-specific password at appleid.apple.com when access is no longer needed. <br>


## Reference(s): <br>
- [CalDAV Protocol Reference](references/caldav-protocol.md) <br>
- [RFC 4791: CalDAV](https://tools.ietf.org/html/rfc4791) <br>
- [RFC 5545: iCalendar](https://tools.ietf.org/html/rfc5545) <br>
- [Apple Support: App-Specific Passwords](https://support.apple.com/en-us/102654) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APPLE_ID and APPLE_APP_PASSWORD environment variables; commands may read, create, or delete calendar events through iCloud CalDAV.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
