## Description: <br>
Queries a user's Keep App exercise records, body measurements, health metrics, daily statistics, recent values, and historical trends through Keep's MCP service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuchuanhao1](https://clawhub.ai/user/liuchuanhao1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Keep users use this skill in OpenClaw or Hermes agents to authenticate with Keep, query their own exercise and health data, and view returned records or statistics. The skill is for data retrieval and presentation, not independent health analysis or advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive Keep health-account data through Keep's MCP service. <br>
Mitigation: Install only when the user is comfortable granting this access, and present upstream results without unsupported health analysis or advice. <br>
Risk: Authentication stores a Keep token under ~/.keepai/.env. <br>
Mitigation: Use the documented logout or clear-credentials flow to remove local credentials when the integration is no longer needed. <br>
Risk: Global installation can send install metadata and copy the skill into local OpenClaw or Hermes skill directories. <br>
Mitigation: Review the install behavior before global installation and use the documented unlink or manual removal steps to clear runner copies. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/liuchuanhao1/keep-query) <br>
- [Keep MCP gateway](https://mcp.gotokeep.com/skills-mcp-gateway-page/v1) <br>
- [Keep 扫码登录鉴权](references/auth.md) <br>
- [Keep 查询工具](references/query.md) <br>
- [Keep 退出登录](references/revoke-auth.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Presents upstream Keep query results and login or logout guidance; should not add unsupported analysis, health advice, or derived statistics.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata, artifact metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
