## Description: <br>
Use KaspaCom LFG Launchpad through the KaspaCom DeFi MCP/CLI for launch discovery and launch-token trading on IGRA and Kasplex. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marciano147](https://clawhub.ai/user/marciano147) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to guide agents through KaspaCom LFG launch discovery, bonding-curve token access, and launch-token buy or sell flows through the KaspaCom DeFi MCP/CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward real on-chain launch-token buys and sells. <br>
Mitigation: Require manual confirmation before every launch or trade, use limited wallet balances, and review transaction parameters before execution. <br>
Risk: Trade examples may omit clear slippage safeguards and can expose users to unfavorable execution. <br>
Mitigation: Set explicit, reasonable slippage or minimum-output limits instead of accepting zero-minimum-output examples. <br>
Risk: Server-managed wallets may create custodial access to funds. <br>
Mitigation: Use limited API keys and wallet balances appropriate to the task and avoid placing unrelated funds in connected wallets. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/marciano147/kaspacom-lfg-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance can include command examples for read-only launchpad lookups and transaction flows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
