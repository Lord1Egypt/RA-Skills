## Description: <br>
Promote schedule details from Gmail into Google Calendar via Maton by reading Gmail messages, extracting structured or free-text event information, and creating Google Calendar events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orulink](https://clawhub.ai/user/orulink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn scheduling details in Gmail into Google Calendar events through Maton-backed Gmail and Calendar connections. It can also guide agents through Gmail message listing, reading, and related helper workflows before creating an event. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key grants access to Gmail content and Google Calendar writes through active OAuth connections. <br>
Mitigation: Store MATON_API_KEY only in the local .env file or environment, do not commit it, and install the skill only when that account access is intended. <br>
Risk: Free-text date and timezone parsing can create calendar events with incorrect timing. <br>
Mitigation: Run the helper with --dry-run first and verify the extracted event payload, especially dates, timezones, and default durations. <br>
Risk: The documentation includes broader Gmail send, label, trash, draft, and connection-management examples beyond the Gmail-to-Calendar workflow. <br>
Mitigation: Use those account-management actions only when explicitly needed and review each command before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orulink/gmail-to-calendar) <br>
- [Maton](https://maton.ai) <br>
- [Maton connection management](https://ctrl.maton.ai) <br>
- [Gmail API reference](https://developers.google.com/gmail/api/reference/rest) <br>
- [Gmail users.messages.list](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/list) <br>
- [Gmail users.messages.get](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/get) <br>
- [Gmail users.messages.send](https://developers.google.com/gmail/api/reference/rest/v1/users.messages/send) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python snippets, API endpoints, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Google Calendar event payloads or helper-script JSON output; requires MATON_API_KEY and active Maton Gmail and Google Calendar connections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
