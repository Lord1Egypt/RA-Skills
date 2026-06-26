## Description: <br>
Unified crosschain USDC balance via Circle Gateway and Circle Programmable Wallets: deposit USDC on supported testnet chains, check a unified balance, and mint USDC on a destination chain without raw private keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[botmechanic](https://clawhub.ai/user/botmechanic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to set up Circle Gateway testnet workflows for unified USDC balance checks, deposits, and cross-chain transfers through Circle Programmable Wallets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scripts can create wallets, sign typed data, and submit transactions using Circle credentials. <br>
Mitigation: Use testnet-only, least-privilege Circle credentials and inspect the fixed amounts, chains, and recipient before running deposit.js or transfer.js. <br>
Risk: Circle API keys and entity secrets can authorize sensitive wallet operations if exposed. <br>
Mitigation: Keep CIRCLE_API_KEY and CIRCLE_ENTITY_SECRET out of logs and source control, and rotate credentials if exposure is suspected. <br>
Risk: Production use would lack confirmation gates, transaction limits, and explicit wallet-creation controls. <br>
Mitigation: Do not connect production wallet sets or credentials until those controls are added. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/botmechanic/nexwave-gateway) <br>
- [Circle Gateway Documentation](https://developers.circle.com/gateway) <br>
- [Circle Programmable Wallets](https://developers.circle.com/wallets) <br>
- [Gateway Unified Balance EVM Quickstart](https://developers.circle.com/gateway/quickstarts/unified-balance-evm) <br>
- [Arc Testnet Documentation](https://docs.arc.network) <br>
- [Circle Wallet Skill](https://clawhub.ai/eltontay/circle-wallet) <br>
- [Circle Gateway API Reference](https://gateway-api-testnet.circle.com/v1/info) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and execution guidance for scripts that use Circle credentials, testnet chain settings, typed-data signing, and Gateway API calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
