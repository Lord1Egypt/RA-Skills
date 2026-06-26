## Description: <br>
Find available meeting times, free/busy slots, and employee calendar availability using Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ARTISONG](https://clawhub.ai/user/ARTISONG) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and workplace assistants use this skill to resolve company attendees, check Microsoft Graph calendar availability, and suggest meeting times from free/busy data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read employee calendar and directory records through Microsoft Graph application permissions. <br>
Mitigation: Install only after administrator review, grant the smallest mailbox scope possible, and use Exchange application access policies where appropriate. <br>
Risk: Azure client secrets and temporary access tokens are sensitive and may expose calendar access if logged or retained improperly. <br>
Mitigation: Store credentials with restricted file permissions, avoid logging token command output, and rotate or delete credentials when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ARTISONG/ms-graph-calendar) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ARTISONG) <br>
- [Microsoft Graph API](https://graph.microsoft.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with shell commands and JSON or text output from Microsoft Graph helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, Azure tenant credentials, and Microsoft Graph application permissions for Calendars.Read and User.Read.All.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
