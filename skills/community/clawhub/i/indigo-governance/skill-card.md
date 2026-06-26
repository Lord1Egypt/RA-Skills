## Description: <br>
Query Indigo Protocol governance data including protocol parameters, temperature checks, and polls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to look up Indigo Protocol governance state, including current protocol parameters, active temperature checks, and formal poll results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Governance and protocol data may be incomplete, stale, or misleading if the configured MCP server is not trusted or current. <br>
Mitigation: Use a trusted Indigo MCP server and verify important financial or governance decisions against authoritative protocol sources before acting. <br>


## Reference(s): <br>
- [Governance MCP Tools Reference](references/mcp-tools.md) <br>
- [Governance Concepts](references/concepts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries of Indigo governance data returned by read-only MCP tool calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No file output or protocol mutations are described; results depend on the configured Indigo MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
