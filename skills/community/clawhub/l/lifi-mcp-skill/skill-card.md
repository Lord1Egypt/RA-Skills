## Description: <br>
Use the LI.FI MCP server through UXC for cross-chain route discovery, bridge/DEX availability checks, token and chain lookup, gas/balance/allowance checks, quote generation, and transfer status tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to plan and monitor cross-chain swaps and bridges through LI.FI MCP, including chain and token discovery, route availability, quote generation, wallet prechecks, and transfer status checks. It supports informational planning workflows and does not sign or broadcast transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, transaction hashes, route details, and token choices may be sent to LI.FI during MCP queries. <br>
Mitigation: Use the skill only with a trusted local UXC setup and only share wallet or transaction details appropriate for LI.FI queries. <br>
Risk: Quotes and transaction requests may be mistaken for completed trades or safe-to-sign instructions. <br>
Mitigation: Treat returned quotes and transaction requests as informational until chain, token, spender, recipient, amount, and fees are independently verified in an external wallet. <br>


## Reference(s): <br>
- [LI.FI MCP Usage Patterns](references/usage-patterns.md) <br>
- [LI.FI MCP endpoint](https://mcp.li.quest/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/lifi-mcp-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jolestar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only planning and monitoring guidance; LI.FI quote and transaction request data must be verified externally before signing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
