## Description: <br>
Access US Census international trade data for imports, exports, trade balances, and monthly trends by commodity and country. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to look up US Census international trade information, including import and export values, trade balances with a country, and month-by-month trade trends for a commodity or country. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trade lookup queries are sent to an external Pipeworx-hosted MCP service. <br>
Mitigation: Do not include confidential business plans, customer data, or sensitive internal context in trade queries unless the Pipeworx provider is trusted for that use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown text with JSON MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns read-only trade lookup results from the configured Census Trade MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
