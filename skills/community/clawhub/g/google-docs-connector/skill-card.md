## Description: <br>
Google Docs Connector helps agents create, edit, format, export, search, and share Google Docs through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to automate Google Docs workflows such as report generation, template creation, collaborative editing, batch document updates, exports, and permission management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector can export document content, including potentially sensitive Google Docs data. <br>
Mitigation: Confirm the exact document and export format before exporting, keep inputs scoped to the task, and avoid placing secrets or sensitive account details in prompts or logs. <br>
Risk: The connector can change sharing permissions, including domain-wide or public access. <br>
Mitigation: Use get_permissions before changing access, verify recipients, roles, domains, and public-access intent, and prefer the least permissive sharing role that satisfies the task. <br>


## Reference(s): <br>
- [ClawHub Google Docs Connector listing](https://clawhub.ai/agentpmt/skills/google-docs-connector) <br>
- [AgentPMT Google Docs Connector marketplace page](https://www.agentpmt.com/marketplace/google-docs-connector) <br>
- [Google Docs Connector generated schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, text, markdown] <br>
**Output Format:** [Markdown instructions with JSON request examples and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote tool calls may return Google Docs content, exported document data, permission details, warnings, or validation results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
