## Description:

Evidence-based market data for AI agents deploying capital in DeFi. Empirical, not advertised.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hayespeter](https://clawhub.ai/user/hayespeter)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Preflyte to query read-only DeFi market intelligence before deploying capital, including opportunity assessment, claim verification, gas timing, position estimates, pool viability, returns, and rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may send sensitive DeFi query details, including assets, chains, position sizes, strategies, and API keys, to PreFlyte services.

Mitigation: Install only when this data sharing is acceptable, keep the PREFLYTE_API_KEY in environment-managed secrets, and avoid sending unnecessary portfolio context.

Risk: Market intelligence, projected returns, gas estimates, and rankings can be wrong, stale, or unsuitable for a specific trade.

Mitigation: Treat responses as decision support, cross-check critical decisions with on-chain data, and do not treat projected returns as guarantees.

Risk: MPP paid endpoints can spend funds per request.

Mitigation: Use explicit spending controls, approval gates, and request limits before enabling pay-per-request access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hayespeter/skills/preflyte)
- [PreFlyte homepage](https://preflyte.xyz)
- [PreFlyte MCP endpoint](https://mcp.preflyte.xyz/mcp)
- [PreFlyte paid OpenAPI discovery document](https://pay.preflyte.xyz/openapi.json)
- [MPPScan listing](https://www.mppscan.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PREFLYTE_API_KEY for free beta API calls, or MPP payment credentials for paid endpoints.]

## Skill Version(s):

1.2.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
