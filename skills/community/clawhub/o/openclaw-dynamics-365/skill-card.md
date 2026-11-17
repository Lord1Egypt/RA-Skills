## Description:

Create and update CRM records in Microsoft Dynamics 365, including Opportunities, Leads, Contacts, Accounts, and Tasks, via the Dataverse Web API with Azure AD OAuth 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vieiradiego](https://clawhub.ai/user/vieiradiego)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business users use this skill to create or update Microsoft Dynamics 365 CRM opportunities, leads, contacts, accounts, and tasks from agent-guided workflows using Dataverse and Azure AD OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update live Dynamics 365 CRM records.

Mitigation: Install only in a controlled tenant with least-privilege Dataverse permissions and require users to confirm the exact CRM record and fields before create or update actions.

Risk: The configured Dynamics 365 instance URL controls the API destination that receives bearer-token requests.

Mitigation: Validate and lock DYNAMICS365_INSTANCE_URL to the exact expected HTTPS Dynamics 365 origin before token-backed API calls.

Risk: OAuth client secrets and refresh tokens are sensitive credentials.

Mitigation: Store secrets and refresh tokens in managed secret storage, limit access, and rotate or re-authorize if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vieiradiego/skills/openclaw-dynamics-365)
- [npm package](https://www.npmjs.com/package/openclaw-dynamics-365)
- [Microsoft Dataverse Web API](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview)
- [Microsoft Dataverse OAuth authentication](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with TypeScript examples, shell commands, and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success or error feedback and record links when CRM operations complete.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
