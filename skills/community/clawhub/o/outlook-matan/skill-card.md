## Description: <br>
Access Microsoft Outlook through Maton Gateway to read, send, and manage emails, folders, calendar events, and contacts with OAuth authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[otman-ai](https://clawhub.ai/user/otman-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to call Microsoft Outlook through Maton Gateway for mailbox, calendar, folder, and contact workflows. It is suited for generating authenticated curl commands, connection setup guidance, and safe operational checklists around Outlook data changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Maton API key can grant access to sensitive Outlook mailbox, calendar, and contact data. <br>
Mitigation: Store MATON_API_KEY as a secret, avoid logging or committing it, and rotate it if exposure is suspected. <br>
Risk: The documented commands can send email or delete, move, and create Outlook resources. <br>
Mitigation: Require explicit user confirmation before running send, delete, move, create, or update operations. <br>
Risk: Stale or unexpected Maton Outlook connections may continue to provide access. <br>
Mitigation: Review active Maton connections and remove connections that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Outlook release page](https://clawhub.ai/otman-ai/outlook-matan) <br>
- [Maton sign-in](https://maton.ai) <br>
- [Maton connection management](https://ctrl.maton.ai) <br>
- [Maton Outlook gateway example](https://gateway.maton.ai/outlook/v1.0/me) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MATON_API_KEY secret and an active Outlook connection through Maton Gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
