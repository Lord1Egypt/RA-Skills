## Description: <br>
Your agent needs money. MoonPay is the crypto onramp for AI agents - wallets, swaps, bridges, transfers, DCA, limit orders, deposits, market data, and fiat on/off ramps via CLI or MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevarifin14](https://clawhub.ai/user/kevarifin14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let agents work with MoonPay CLI, local MCP, and REST surfaces for wallet management, token swaps, bridges, transfers, deposits, market data, fiat on/off-ramp flows, and related crypto operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad access to wallets, signing, fund movement, fiat flows, persistent accounts, and automated trading setup. <br>
Mitigation: Install only if the publisher and @moonpay/cli package are trusted; use a dedicated low-balance wallet and require explicit human approval before transfers, swaps, bridges, buys, transaction signing, wallet export, wallet deletion, x402 payments, or automated trading setup. <br>
Risk: Crypto operations can be irreversible or materially affected by recipient address, chain, token contract, amount, fee, and slippage mistakes. <br>
Mitigation: Verify recipient addresses, chains, token contracts, amounts, fees, and slippage before execution, and prefer simulate-then-execute flows where available. <br>


## Reference(s): <br>
- [MoonPay Agents Homepage](https://agents.moonpay.com) <br>
- [ClawHub MoonPay Skill Page](https://clawhub.ai/kevarifin14/moonpay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the MoonPay CLI binary `mp`; some flows require login, KYC, explicit confirmation, and local wallet access.] <br>

## Skill Version(s): <br>
0.6.24 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
