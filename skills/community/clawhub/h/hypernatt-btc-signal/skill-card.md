## Description: <br>
HyperNatt Terminal signal skill provides read-only live BTC/USDC Mimo vault cycle state via HTTP x402 and returns JSON status, track record, and disclaimer information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dialloube-research](https://clawhub.ai/user/dialloube-research) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve current read-only BTC/USDC Mimo vault cycle direction, leg context, and track record information from HyperNatt. It is not intended for trade execution, TP/SL advice, or direct financial recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote API responses and service claims may change outside the packaged skill. <br>
Mitigation: Install only when the publisher and hypernatt.com service are trusted, and independently verify important outputs before acting on them. <br>
Risk: The skill can require wallet-based x402 payment or an Agent Pass/free-tier decision controlled by the remote service. <br>
Mitigation: Confirm billing, free-tier, and payment terms outside the skill before use, and only provide an x402 payment payload for an explicit intended call. <br>
Risk: Crypto market output could be mistaken for financial advice. <br>
Mitigation: Use the JSON as read-only cycle-state information and do not rely on it for financial decisions without independent checks. <br>
Risk: Sensitive environment variables may be exposed if supplied unnecessarily. <br>
Mitigation: Provide only the required `X402_PAYMENT_B64` value for a planned request and avoid passing unrelated secrets into the skill environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dialloube-research/hypernatt-btc-signal) <br>
- [HyperNatt server card](https://hypernatt.com/.well-known/mcp/server-card.json) <br>
- [HyperNatt MCP protocol](https://hypernatt.com/mcp/protocol) <br>
- [HyperNatt stats](https://hypernatt.com/stats) <br>
- [HyperNatt terminal quickstart](https://github.com/DIALLOUBE-RESEARCH/hypernatt-terminal/blob/main/docs/quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance] <br>
**Output Format:** [JSON object printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only remote API summary; may return HTTP 402 payment instructions when x402 payment is required.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
