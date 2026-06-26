## Description: <br>
Search, read, and update HubSpot CRM contacts, companies, deals, tickets, associations, owners, and pipelines via HubSpot's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external operators, developers, and agents use this skill to inspect HubSpot CRM records, understand pipeline state, and make confirmed updates through HubSpot's hosted MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act as the connected HubSpot account and read or update CRM data within that account's OAuth grant. <br>
Mitigation: Review the HubSpot OAuth grant before use, confirm user intent before write actions, and revoke the integration in HubSpot when it is no longer needed. <br>
Risk: OAuth credentials are stored locally for use by mcporter. <br>
Mitigation: Protect the local environment where the skill is installed and rotate or revoke HubSpot credentials if that environment is no longer trusted. <br>
Risk: Tool arguments and results transit HubSpot's hosted MCP server. <br>
Mitigation: Send only HubSpot-relevant data through tool arguments and avoid including unrelated sensitive information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/maverick/maverick-hubspot-mcp) <br>
- [Maverick Publisher Profile](https://clawhub.ai/user/maverick) <br>
- [HubSpot MCP Server Documentation](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server) <br>
- [HubSpot MCP Auth App Documentation](https://developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server#create-an-mcp-auth-app) <br>
- [mcporter Config Reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and MCP tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on HubSpot's live MCP tool catalog and the connected account's OAuth grant.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
