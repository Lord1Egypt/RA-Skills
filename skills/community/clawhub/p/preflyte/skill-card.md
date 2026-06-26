## Description: <br>
Preflyte provides evidence-based market data for AI agents deploying capital in DeFi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hayespeter](https://clawhub.ai/user/hayespeter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and DeFi agent operators use Preflyte to query pre-trade market intelligence, validate market assumptions, estimate gas and net position outcomes, and compare historical DeFi returns before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeFi strategy, position size, and risk-preference queries are sent to Preflyte. <br>
Mitigation: Use the skill only when that data sharing is acceptable, avoid unnecessary sensitive detail, and cross-check critical decisions with on-chain sources. <br>
Risk: Optional paid MPP endpoints can spend funds for requests. <br>
Mitigation: Require explicit approval, use a limited wallet or allowance, and set a fixed spending cap before enabling paid endpoints. <br>
Risk: The PREFLYTE_API_KEY is a sensitive credential. <br>
Mitigation: Store the key in the environment or a secrets manager, avoid logging it, and rotate it if exposed. <br>


## Reference(s): <br>
- [ClawHub Preflyte listing](https://clawhub.ai/hayespeter/preflyte) <br>
- [Preflyte homepage](https://preflyte.xyz) <br>
- [Preflyte REST API](https://api.preflyte.xyz) <br>
- [Preflyte MCP server](https://mcp.preflyte.xyz/mcp) <br>
- [Paid API discovery document](https://pay.preflyte.xyz/openapi.json) <br>
- [MPPScan](https://www.mppscan.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with endpoint references and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PREFLYTE_API_KEY for API-key mode; paid MPP endpoints require explicit payment handling.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
