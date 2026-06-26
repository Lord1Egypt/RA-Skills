## Description: <br>
iHRFlow HR assistant for recruiting. Use when searching candidates, managing positions, scheduling interviews, advancing pipeline, or viewing recruitment stats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MikeLing](https://clawhub.ai/user/MikeLing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR employees and recruiting teams use this skill to search candidates, manage positions, schedule or reschedule interviews, move candidates through hiring stages, and summarize recruitment activity from iHRFlow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated tool calls can publish or close jobs, schedule or cancel interviews, submit feedback, add notes, recommend candidates, and change candidate status. <br>
Mitigation: Require explicit user confirmation before record-changing actions and run the skill with a least-privilege iHRFlow account. <br>
Risk: The skill depends on credentials, an optional API key, and a cached MCP session on the host. <br>
Mitigation: Protect environment variables, avoid shared hosts unless session caching is hardened, and rotate credentials when access changes. <br>
Risk: The integration trusts the configured iHRFlow MCP endpoint for HR data and actions. <br>
Mitigation: Install only when the configured MCP endpoint is trusted and verify IHRFLOW_MCP_URL before use. <br>


## Reference(s): <br>
- [iHRFlow MCP Tool & Resource Reference](artifact/references/api-reference.md) <br>
- [iHRFlow AI Recruiting Assistant User Manual](artifact/docs/用户手册.md) <br>
- [iHRFlow](https://ihrflow.com) <br>
- [ClawHub Release Page](https://clawhub.ai/MikeLing/ihrflow-hr) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown summaries with JSON MCP tool results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, IHRFLOW_MCP_URL, IHRFLOW_USERNAME, and IHRFLOW_PASSWORD; authenticated calls can change live HR records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, changelog, ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
