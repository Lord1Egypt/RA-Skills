## Description: <br>
Manage crypto wallets and make x402 micropayments with USDC stablecoins on Polygon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AkshatGada](https://clawhub.ai/user/AkshatGada) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw users use this skill to let agents create or import wallets, check balances, set spending limits, register paid APIs, and make approved x402 USDC micropayments on Polygon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real-money payments when configured for Polygon mainnet. <br>
Mitigation: Start on Polygon Amoy testnet, keep per-transaction and daily limits low, and review the exact URL and amount before approving each payment. <br>
Risk: Wallet credentials or encryption keys could be exposed through chat, shell history, or committed files. <br>
Mitigation: Do not paste production private keys in chat or command history; store wallet encryption keys in environment variables or a secret manager. <br>
Risk: An agent could call a paid API endpoint that is unexpected or more expensive than intended. <br>
Mitigation: Use payment pre-checks, require explicit user approval for payments, and monitor transaction history and daily usage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AkshatGada/llm-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/AkshatGada) <br>
- [x402 protocol overview](references/x402-protocol.md) <br>
- [Wallet setup guide](references/wallet-setup.md) <br>
- [Usage examples](references/examples.md) <br>
- [x402 website](https://www.x402.org/) <br>
- [x402 documentation](https://docs.cdp.coinbase.com/x402/welcome) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet addresses, balances, payment status, transaction hashes, spending limits, and registered API names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
