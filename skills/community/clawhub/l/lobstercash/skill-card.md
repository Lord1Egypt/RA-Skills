## Description: <br>
lobstercash helps agents make online purchases, manage virtual cards and payment wallets, send crypto, pay x402 API endpoints, and sign blockchain transactions through the Lobster Cash CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manu-xmint](https://clawhub.ai/user/manu-xmint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent perform controlled payment tasks: shopping with virtual cards, funding or checking wallets, sending tokens, paying x402 APIs, and managing transaction approval flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent spending authority through virtual cards, wallet funding, crypto transfers, x402 API payments, and transaction signing. <br>
Mitigation: Install only when controlled payment authority is intended; use low wallet and card limits and require explicit human approval before creating cards, funding wallets, submitting orders, or approving transactions. <br>
Risk: Several flows can submit orders or on-chain transactions after CLI steps, making insufficient final review a financial risk. <br>
Mitigation: Require a final human review of merchant, amount, recipient, network, and transaction details before running order submission, send, x402, or transaction approval commands. <br>
Risk: Card details, bearer tokens, and signed payment payloads can be exposed through untrusted browser automation, logs, or unknown domains. <br>
Mitigation: Avoid revealing card details or tokens to untrusted tools or sites, do not echo sensitive values back to the user or logs, and restrict checkout automation to domains the user authorized. <br>
Risk: Raw or externally supplied blockchain transactions may be difficult for users to inspect and can transfer assets or grant permissions. <br>
Mitigation: Avoid raw transaction signing from untrusted tools; prefer higher-level commands when possible and review transaction source, target chain, recipient, and expected effect before approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/manu-xmint/lobstercash) <br>
- [Publisher profile](https://clawhub.ai/user/manu-xmint) <br>
- [Skill definition](SKILL.md) <br>
- [Buy something online: browser-automated flow](references/purchase-flow.md) <br>
- [Buy something online: agent-driven browser flow](references/purchase-flow-byo.md) <br>
- [Virtual card reference](references/cards.md) <br>
- [Crypto funding reference](references/crypto-request.md) <br>
- [x402 API payments reference](references/x402.md) <br>
- [Transactions reference](references/tx.md) <br>
- [Lobster Cash install](https://www.lobster.cash/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment approval URLs, merchant checkout instructions, wallet status summaries, and transaction explorer links.] <br>

## Skill Version(s): <br>
0.0.16 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
