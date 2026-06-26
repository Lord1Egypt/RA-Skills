## Description: <br>
Work with Jira issue tracking and project workflow state through Atlassian Rovo's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and project teams use this skill to inspect Jira work tracking state and, when explicitly authorized, perform workflow updates through Atlassian Rovo MCP using the connected user's Jira permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration stores Atlassian OAuth credentials locally and uses the connected user's Jira permissions. <br>
Mitigation: Use an Atlassian account with appropriate permissions, protect local credentials, and revoke the OAuth grant in Atlassian when access is no longer needed. <br>
Risk: Jira tools may create, edit, comment on, transition, or otherwise mutate work items. <br>
Mitigation: Review write actions before allowing them and require clear user intent before making Jira changes. <br>
Risk: Tool arguments and results transit Atlassian Rovo's hosted MCP service. <br>
Mitigation: Avoid sending unrelated sensitive content through Jira tool calls. <br>


## Reference(s): <br>
- [Atlassian Rovo MCP client setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-clients/) <br>
- [Atlassian Rovo MCP OAuth 2.1 setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/) <br>
- [Atlassian Rovo MCP supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/) <br>
- [mcporter config docs](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON tool output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live tool schemas and server instructions are discovered at runtime from Atlassian Rovo MCP.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
