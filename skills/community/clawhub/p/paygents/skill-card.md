## Description:

Accept crypto payments in AI agent conversations. Generate MetaMask/Trust Wallet deeplinks, verify transactions on-chain, check balances, issue receipts. No custody, no backend, no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitaybohadana](https://clawhub.ai/user/amitaybohadana)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use PayGents to let an AI agent request EVM payments, generate wallet deeplinks for user approval, verify transactions on-chain, check balances, and produce receipts without taking custody of private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation flaws could allow crafted inputs to run code or produce unsafe payment confirmations.

Mitigation: Use the skill only as a manually supervised helper until fixed, and avoid passing untrusted chain IDs, merchant names, memos, or token symbols.

Risk: Payment verification could be misused as the sole basis for fulfilling orders or crediting accounts.

Mitigation: Require a specific transaction hash, track consumed transactions, wait for confirmations, and keep an independent fulfillment review step.

## Reference(s):

- [EVM Payment Deeplink Reference](references/evm-usdc-poc.md)
- [PayGents on ClawHub](https://clawhub.ai/amitaybohadana/skills/paygents)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples and JSON or Markdown command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can generate payment deeplink payloads, on-chain verification results, balance reports, and receipts.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
