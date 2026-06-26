## Description: <br>
Provides national and local housing market analysis by combining data from FRED, BLS, ATTOM, and HUD APIs for property and market insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Housing analysts, real estate professionals, and agents use this skill to query national indicators, local property data, rental estimates, affordability metrics, and employment signals through a hosted Pipeworx MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Housing and property queries may be sent to Pipeworx and optionally saved by memory tools. <br>
Mitigation: Avoid submitting or saving sensitive addresses, ownership details, valuations, or investment notes unless remote handling and possible memory persistence are acceptable. <br>
Risk: Hosted connector results may combine third-party housing, labor, property, and rental data sources with different freshness and coverage. <br>
Mitigation: Review important market or investment conclusions against authoritative source data before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-housing-analyst) <br>
- [Pipeworx hosted MCP endpoint](https://gateway.pipeworx.io/mcp?task=housing%20analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with MCP server configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a hosted Pipeworx MCP server for housing, property, rental, affordability, and labor-market queries.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
