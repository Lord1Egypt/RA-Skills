## Description: <br>
Currency exchange rates and conversion for current, historical, and supported currency pairs via the Frankfurter API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to get current and historical exchange rates, convert currency amounts, and list supported currencies for travel planning, analysis, and localized price display. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a remote MCP/API endpoint for exchange-rate data, so responses may be unavailable, delayed, or unsuitable as the sole source for financial commitments. <br>
Mitigation: Verify rates against an authoritative financial source before making payments, trades, accounting entries, or other commitments. <br>
Risk: Security guidance for this release advises review before use because installed tooling may operate with elevated agent permissions. <br>
Mitigation: Review the installed skill files before deployment and keep normal sandbox controls enabled unless broader access is explicitly required. <br>


## Reference(s): <br>
- [Pipeworx Exchange homepage](https://pipeworx.io/packs/exchange) <br>
- [Pipeworx Exchange MCP endpoint](https://gateway.pipeworx.io/exchange/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/b-gutman/pipeworx-exchange) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON responses and concise text summaries, with Markdown examples for curl and MCP client configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented manual request example; no API key requirement is declared in the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
