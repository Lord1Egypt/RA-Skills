## Description: <br>
PayQL helps agents discover live The Graph subgraphs, quote an x402 USDC price, and run paid GraphQL reads from a dedicated Base wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulieb14](https://clawhub.ai/user/paulieb14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use PayQL to retrieve live on-chain DeFi, DEX, NFT, ENS, token, and governance data without API keys while paying per query in USDC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spend real USDC from a user-provided Base wallet for paid queries. <br>
Mitigation: Install it only with a dedicated low-balance wallet funded with the USDC intended for queries; avoid primary or reused private keys. <br>
Risk: Wallet private keys in agent harness configuration may be logged, synced, screenshotted, or accidentally committed. <br>
Mitigation: Keep private keys out of shared chats and repositories, and prefer managed wallet controls, spend caps, or allowlists when agents may run many queries. <br>


## Reference(s): <br>
- [PayQL ClawHub skill page](https://clawhub.ai/paulieb14/skills/payqlskill) <br>
- [The Graph x402 gateway recipe](references/gateway.md) <br>
- [x402 protocol](https://x402.org) <br>
- [Ampersend managed wallets](https://ampersend.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Shell commands, JSON, Text] <br>
**Output Format:** [Markdown guidance with JSON, GraphQL, and shell/configuration snippets; tool responses may include JSON data and payment receipts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid queries can spend real USDC from the configured wallet.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
