## Description: <br>
Integrates Microsoft Outlook email so an agent can read, search, send, reply to, and manage folders through MorphixAI access to Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to let an agent operate a linked Outlook mailbox for message lookup, folder browsing, email sending, and replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and send real email through a linked mailbox without documented confirmation or draft safeguards. <br>
Mitigation: Use only with a mailbox suitable for MorphixAI linking, verify the external plugin source, and require manual review of account, recipients, subject, and full message body before send or reply actions. <br>


## Reference(s): <br>
- [Outlook Email on ClawHub](https://clawhub.ai/paul-leo/outlook-email-2) <br>
- [MorphixAI API Keys](https://morphix.app/api-keys) <br>
- [MorphixAI Connections](https://morphix.app/connections) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and YAML-like tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MORPHIXAI_API_KEY and a linked Outlook account through MorphixAI.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
