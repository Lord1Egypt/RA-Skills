## Description:

Quote and prepare cross-chain token swaps via LayerHop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[layerhop](https://clawhub.ai/user/layerhop)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers can compare cross-chain swap routes, review fees and expected amounts, and prepare a swap link or unsigned transaction for their own wallet to review and sign.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quote requests send wallet addresses and proposed swap details to LayerHop, and the scan advises that this data flow be disclosed before requesting a quote.

Mitigation: Before sending a quote request, explain that the source and destination details, amount, and wallet addresses will be sent to LayerHop, then get the user's consent.

## Reference(s):

- [LayerHop AI agent guide](https://docs.layerhop.com/guides/ai-agents)
- [LayerHop API reference](https://docs.layerhop.com/api-reference)
- [LayerHop MCP endpoint](https://mcp.layerhop.com/mcp)
- [LayerHop ClawHub release](https://clawhub.ai/layerhop/skills/layerhop)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Swap quote summaries, Swap links, Unsigned transaction data]

**Output Format:** [Markdown summaries, URLs, and JSON transaction data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quote amounts are estimates and may change; the user's wallet reviews and signs any swap.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
