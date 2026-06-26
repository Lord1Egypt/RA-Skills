## Description: <br>
Searches and retrieves public CDC datasets and records from data.cdc.gov through a hosted Pipeworx MCP endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to help users search CDC public health datasets by keyword and fetch rows from a specific Socrata dataset ID for public health research, reporting, or data exploration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and dataset requests are routed through a third-party hosted MCP gateway. <br>
Mitigation: Use the skill for public CDC dataset lookups and avoid entering private health details, credentials, or sensitive internal identifiers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-cdc) <br>
- [CDC Open Data](https://data.cdc.gov) <br>
- [Pipeworx CDC MCP endpoint](https://gateway.pipeworx.io/cdc/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [Markdown or plain text summaries of CDC dataset search results and retrieved records, plus MCP server configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns public dataset names, descriptions, IDs, update details, and rows for a supplied Socrata dataset ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
