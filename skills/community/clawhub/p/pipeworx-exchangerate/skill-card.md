## Description: <br>
Simple currency exchange rates - all rates for a base currency or a direct pair lookup via open.er-api.com. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch current currency exchange rates, either as a full table for one base currency or as a direct pair rate lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns current exchange-rate data from an external service, which may be delayed, unavailable, or unsuitable as the sole source for financial decisions. <br>
Mitigation: Confirm rates against an authoritative financial source before using them for transactions, accounting, compliance, or other high-impact decisions. <br>
Risk: The provided examples and MCP configuration invoke external Pipeworx endpoints. <br>
Mitigation: Review the endpoint and command configuration before installation, and run it only in environments where outbound access to that service is approved. <br>


## Reference(s): <br>
- [Pipeworx ExchangeRate Pack](https://pipeworx.io/packs/exchangerate) <br>
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/pipeworx-exchangerate) <br>
- [Pipeworx ExchangeRate MCP Endpoint](https://gateway.pipeworx.io/exchangerate/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct examples and can be configured through an MCP server entry.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
