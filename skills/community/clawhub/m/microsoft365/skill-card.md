## Description: <br>
Microsoft 365 integration for Outlook, Calendar, Contacts, and OneDrive via Microsoft Graph API that supports reading and sending emails, managing calendar events, and accessing files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Robert-Janssen](https://clawhub.ai/user/Robert-Janssen) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and end users use this skill to connect a local agent workflow to Microsoft 365 through Microsoft Graph for email, calendar, contacts, and OneDrive tasks after Microsoft device-code consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access and change mail, calendar, contacts, and OneDrive after Microsoft consent. <br>
Mitigation: Use your own Azure app registration, review the Microsoft consent prompt, and install only for accounts where this access is acceptable. <br>
Risk: Local credential files can expose Microsoft account access if they are synced, shared, or committed. <br>
Mitigation: Protect ~/.openclaw/credentials, do not sync or commit token files, and revoke the app in Microsoft account settings when you stop using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Robert-Janssen/microsoft365) <br>
- [Azure Portal app registrations](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/RegisteredApps) <br>
- [Microsoft device login](https://microsoft.com/devicelogin) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls] <br>
**Output Format:** [Terminal text from a Node.js CLI with Microsoft Graph side effects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive prompts can send email, create calendar events, create contacts, upload files, and store local Microsoft tokens.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
