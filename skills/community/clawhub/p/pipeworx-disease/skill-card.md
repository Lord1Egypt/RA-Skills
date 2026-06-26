## Description: <br>
COVID-19 statistics - global totals, per-country breakdowns, historical trends, and vaccination data from disease.sh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query current and historical COVID-19 totals, country-level statistics, time-series trends, and vaccination data through the Pipeworx disease MCP service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: COVID-19 statistics queries are sent to gateway.pipeworx.io. <br>
Mitigation: Use the skill only when sending those queries to the named remote service is acceptable. <br>
Risk: The MCP configuration runs the third-party npm package mcp-remote@latest, which may change over time. <br>
Mitigation: Review the package before use and pin or otherwise control the package version in managed environments. <br>


## Reference(s): <br>
- [Pipeworx disease homepage](https://pipeworx.io/packs/disease) <br>
- [Pipeworx disease MCP endpoint](https://gateway.pipeworx.io/disease/mcp) <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-disease) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides an agent to call a remote MCP service and return COVID-19 statistics as text or structured tool results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
