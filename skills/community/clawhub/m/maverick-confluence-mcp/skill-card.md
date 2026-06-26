## Description: <br>
Work with Confluence workspace content through Atlassian Rovo's hosted MCP server, using the live server catalog for pages, spaces, docs, comments, and knowledge-base updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents with authorized Confluence access use this skill to search, read, and, with explicit user intent, modify Confluence pages, spaces, docs, comments, and knowledge-base content through Atlassian Rovo MCP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Atlassian OAuth values locally and uses them to access Confluence with the connected user's permissions. <br>
Mitigation: Keep OAuth values private, install only when Confluence access is intended, and revoke the Atlassian OAuth grant when the skill is no longer needed. <br>
Risk: Confluence tools may create, update, publish, comment on, or otherwise change workspace content. <br>
Mitigation: Review any mutating action before it runs and require clear user intent for the specific content being changed. <br>
Risk: Tool arguments and results transit Atlassian Rovo's hosted MCP service. <br>
Mitigation: Avoid sending unrelated sensitive content through tool arguments or prompts. <br>
Risk: Rerunning setup with stale OAuth values can overwrite a newer refresh token in the local vault. <br>
Mitigation: Run setup again only with freshly issued OAuth credentials or re-authorize the integration if credentials become invalid. <br>


## Reference(s): <br>
- [Atlassian Rovo MCP client setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/setting-up-clients/) <br>
- [Atlassian Rovo MCP OAuth 2.1 setup](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/configuring-oauth-2-1/) <br>
- [Atlassian Rovo MCP supported tools](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/) <br>
- [mcporter config docs](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON tool output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool availability and results are determined by Atlassian Rovo MCP and the connected user's Confluence permissions.] <br>

## Skill Version(s): <br>
1.0.5 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
