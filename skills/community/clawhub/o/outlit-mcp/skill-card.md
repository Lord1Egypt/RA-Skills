## Description: <br>
Use when querying Outlit customer data via MCP tools for customer analytics, revenue metrics, activity timelines, cohort analysis, churn risk assessment, SQL queries, and other Outlit data exploration tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leo-paz](https://clawhub.ai/user/leo-paz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and operators use this skill to connect an agent to Outlit MCP tools, query customer intelligence data, and produce account health, revenue, churn risk, and activity analyses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent to customer, user, revenue, and activity data through Outlit MCP tools. <br>
Mitigation: Install only when this agent should access Outlit analytics, verify the API key in Outlit MCP Integration settings, and prefer least-privilege credentials where available. <br>
Risk: Broad queries can expose more customer, user, or revenue data than needed for the task. <br>
Mitigation: Ask for bounded analyses, use filters, time ranges, and limits, and request only the customer include sections needed for the answer. <br>
Risk: API keys added to MCP configuration can be copied into shared repositories or chat logs. <br>
Mitigation: Keep the key out of shared files and logs where possible, and review configuration changes before committing or sharing them. <br>


## Reference(s): <br>
- [Outlit Skill Page](https://clawhub.ai/leo-paz/outlit-mcp) <br>
- [Outlit App](https://app.outlit.ai) <br>
- [Outlit MCP Endpoint](https://mcp.outlit.ai/mcp) <br>
- [SQL Reference](references/sql-reference.md) <br>
- [Common Workflows](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL query guidance, MCP setup snippets, and summarized customer analytics results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
