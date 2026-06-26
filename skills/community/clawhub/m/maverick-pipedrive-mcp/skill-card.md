## Description: <br>
Search, read, and update Pipedrive deals, contacts, organizations, activities, pipelines, and sales workflows through a local MCP wrapper. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to inspect and manage Pipedrive CRM records from an agent workflow. It is intended for Pipedrive-related sales pipeline, contact, organization, activity, note, and deal work using the connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create records, update properties, change deal stages, mark activities done, create notes, and otherwise modify Pipedrive CRM state. <br>
Mitigation: Confirm clear user intent before write actions, search or read current records first, and review the proposed change before execution. <br>
Risk: The skill requires OAuth access tokens, refresh tokens, client IDs, client secrets, and API base configuration for the connected Pipedrive account. <br>
Mitigation: Use least-privilege OAuth scopes where possible, store credentials only through the configured local vault flow, and rotate the refresh token or client secret if exposed. <br>
Risk: The install metadata uses an unpinned mcporter package, which may be unsuitable for stricter supply-chain environments. <br>
Mitigation: Pin mcporter to an approved version in controlled deployments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick/maverick-pipedrive-mcp) <br>
- [Maverick Publisher Profile](https://clawhub.ai/user/maverick) <br>
- [mcporter](https://github.com/steipete/mcporter) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>
- [Pipedrive API Base](https://api.pipedrive.com/api) <br>
- [Pipedrive OAuth Token Endpoint](https://oauth.pipedrive.com/oauth/token) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Configuration] <br>
**Output Format:** [JSON responses from local MCP tools, with setup and invocation commands documented in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses OAuth credentials and a local stdio MCP server to access Pipedrive CRM data for the connected account.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
