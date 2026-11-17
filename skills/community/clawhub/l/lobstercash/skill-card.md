## Description:

Lobster Cash gives agents a CLI-guided payment workflow for online purchases, virtual cards, wallet setup, USDC transfers, x402 API payments, balance checks, and on-chain transaction signing with human approval controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manu-xmint](https://clawhub.ai/user/manu-xmint)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to delegate payment-related tasks to an agent, including shopping checkout, virtual card handling, crypto funding, x402 API payments, wallet status checks, and transaction signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through spending, virtual card use, API payments, crypto transfers, and blockchain transaction signing.

Mitigation: Require explicit user confirmation before every spend, card creation, funding request, checkout action, token transfer, or transaction signature.

Risk: Secrets or bearer tokens may be exposed if passed through command arguments or debug output.

Mitigation: Avoid command-line bearer tokens where possible and only use debug output when necessary, with secret redaction before sharing logs.

Risk: Trust depends on the external Lobster Cash CLI and payment service publisher.

Mitigation: Install only from trusted sources, pin and review the CLI version where possible, and revoke wallet or card access when finished.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manu-xmint/skills/lobstercash)
- [Lobster Cash Install](https://www.lobster.cash/install)
- [Agents Reference](references/agents.md)
- [Setup Reference](references/setup.md)
- [Status Reference](references/status.md)
- [Balance Reference](references/balance.md)
- [Virtual Cards Reference](references/cards.md)
- [Card Request Reference](references/cards-request.md)
- [Purchase Flow Reference](references/purchase-flow.md)
- [Bring-Your-Own Browser Purchase Flow](references/purchase-flow-byo.md)
- [Purchase Command Reference](references/purchase.md)
- [Crypto Request Reference](references/crypto-request.md)
- [Send Tokens Reference](references/send.md)
- [Transaction Reference](references/tx.md)
- [x402 API Payments Reference](references/x402.md)
- [Examples Reference](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and summarized CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires human approval before card creation, funding requests, checkout actions, crypto transfers, or transaction signing.]

## Skill Version(s):

0.0.16 (source: skill frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
