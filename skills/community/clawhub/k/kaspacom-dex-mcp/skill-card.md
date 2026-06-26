## Description: <br>
Use KaspaCom DEX through the KaspaCom DeFi MCP/CLI for pair discovery, token pricing, swaps, and liquidity management on IGRA and Kasplex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marciano147](https://clawhub.ai/user/marciano147) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover KaspaCom DEX pairs, check token prices, and prepare swap or liquidity-management commands for IGRA and Kasplex. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction commands can move crypto funds if swaps or liquidity changes are run without sufficient review. <br>
Mitigation: Require the exact token pair, amount, network, wallet, quote, fees, slippage, and expected transaction effect to be shown and explicitly confirmed before any transaction command runs. <br>
Risk: DEX helper output may be legitimate but still operationally risky when used unattended. <br>
Mitigation: Use read-only pair and price commands freely, and keep swaps or liquidity changes under direct human approval. <br>


## Reference(s): <br>
- [KaspaCom DEX MCP on ClawHub](https://clawhub.ai/marciano147/kaspacom-dex-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only DEX queries and transaction command proposals that require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
