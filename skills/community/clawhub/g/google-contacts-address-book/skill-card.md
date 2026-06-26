## Description: <br>
Google Contacts API integration with managed OAuth for searching, inspecting, creating, and updating contacts and contact groups stored in Google People. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an OpenClaw agent to Google Contacts through managed OAuth, then search, inspect, create, update, and organize contacts and contact groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth access to contacts and contact groups in the connected Google account. <br>
Mitigation: Review the Google OAuth consent screen before connecting and install only when ClawLink access to Google Contacts is intended. <br>
Risk: Create, update, and delete operations can change or remove contact and contact group data. <br>
Mitigation: Confirm the exact target resource and intended change before executing any write or delete operation. <br>
Risk: An active connection can continue to provide access after the immediate task is complete. <br>
Mitigation: Revoke the ClawLink or Google connection when ongoing access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Google Contacts Skill Page](https://clawhub.ai/hith3sh/google-contacts-address-book) <br>
- [Google People API Overview](https://developers.google.com/people/api/rest) <br>
- [Google Contacts API](https://developers.google.com/contacts/v3) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance includes OAuth connection checks, live tool discovery, and confirmation steps for write operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
