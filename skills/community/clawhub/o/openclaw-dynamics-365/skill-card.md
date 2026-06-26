## Description: <br>
Create and update CRM records in Microsoft Dynamics 365, including Opportunities, Leads, Contacts, Accounts, and Tasks, through the Dataverse Web API with Azure AD OAuth 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vieiradiego](https://clawhub.ai/user/vieiradiego) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external CRM users, and developers use this skill to create or update Dynamics 365 CRM records from agent-mediated instructions. It is suited for teams that need authenticated Dataverse operations for opportunities, leads, contacts, accounts, and tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update CRM records in the configured Dynamics 365 tenant. <br>
Mitigation: Install and run it only for users authorized to modify the target tenant, and test workflows with non-production CRM data before using real customer or deal records. <br>
Risk: OAuth client secrets, access tokens, and refresh tokens could expose CRM access if copied into prompts or logs. <br>
Mitigation: Store credentials in a secret manager, keep them out of prompts and logs, and rotate them according to the tenant's security policy. <br>
Risk: Over-broad Azure app permissions could allow more CRM access than the agent workflow needs. <br>
Mitigation: Use least-privilege delegated permissions and review admin consent before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vieiradiego/openclaw-dynamics-365) <br>
- [Microsoft Dataverse Web API overview](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview) <br>
- [Microsoft Dataverse OAuth documentation](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth) <br>
- [npm package](https://www.npmjs.com/package/openclaw-dynamics-365) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with TypeScript snippets, shell commands, configuration values, and Dynamics 365 record links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Azure AD OAuth credentials and a Dynamics 365 instance URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
