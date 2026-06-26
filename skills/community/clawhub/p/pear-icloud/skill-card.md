## Description: <br>
iCloud Calendar, Reminders & Contacts via Pear. Manage events, reminders, contacts, daily briefings, and AI scheduling. 27 tools for Apple iCloud via CalDAV/CardDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AshtonAU](https://clawhub.ai/user/AshtonAU) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to read and manage iCloud calendar events, reminders, contacts, daily briefings, and meeting-time suggestions through Pear. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pear receives sensitive iCloud calendar, reminder, contact, attendee, phone, email, address, and birthday data. <br>
Mitigation: Install only when Pear is trusted for that data, and revoke the Pear API key or iCloud app-specific password when the integration is no longer needed. <br>
Risk: Delete, update, and batch actions can change or remove iCloud events, reminders, or contacts. <br>
Mitigation: Review affected items, dates, and counts before approving destructive, update, or batch operations. <br>
Risk: A custom PEAR_MCP_URL endpoint could route iCloud data and actions through an untrusted service. <br>
Mitigation: Use custom endpoints only when the endpoint operator is trusted. <br>
Risk: The PEAR_API_KEY grants access to the Pear integration. <br>
Mitigation: Treat the key as a secret and avoid exposing it in prompts, logs, or shared output. <br>


## Reference(s): <br>
- [Pear Homepage](https://pearmcp.com) <br>
- [Pear Documentation](https://pearmcp.com/docs) <br>
- [Apple App-Specific Passwords](https://support.apple.com/en-us/102654) <br>
- [CalDAV Protocol (RFC 4791)](https://www.rfc-editor.org/rfc/rfc4791) <br>
- [CardDAV Protocol (RFC 6352)](https://www.rfc-editor.org/rfc/rfc6352) <br>
- [IANA Time Zone Database](https://www.iana.org/time-zones) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Text or Markdown summaries with structured MCP tool calls and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PEAR_API_KEY and network access to pearmcp.com.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
