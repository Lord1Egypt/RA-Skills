## Description: <br>
Query crypto intelligence via Pond3r MCP for curated datasets, SQL queries, protocol metrics, yields, and market analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fabriziogianni7](https://clawhub.ai/user/fabriziogianni7) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to query Pond3r datasets for DeFi yields, protocol metrics, token opportunities, Polymarket activity, and cross-protocol blockchain analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create scheduled remote reports even though most of its workflow is framed as read-only analytics. <br>
Mitigation: Only create scheduled reports after an explicit user request, and confirm how to delete or disable any reports created in the Pond3r account. <br>
Risk: Pond3r API keys and user query contents may be exposed if copied into logs, chat, SQL, or report descriptions. <br>
Mitigation: Use a dedicated Pond3r API key, store it in environment variables, avoid secret values in prompts or queries, and rotate the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fabriziogianni7/pond3r-skill) <br>
- [Pond3r Reference](reference.md) <br>
- [Pond3r MCP endpoint](https://mcp.pond3r.xyz/mcp) <br>
- [Pond3r report API](https://api.pond3r.xyz/v1/api/reports) <br>
- [Pond3r web interface](https://makeit.pond3r.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON with shell commands, SQL snippets, configuration examples, and analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Pond3r query results are capped at 10,000 rows; SQL examples are intended to be read-only SELECT queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
