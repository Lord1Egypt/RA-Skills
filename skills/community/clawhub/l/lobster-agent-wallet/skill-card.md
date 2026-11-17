## Description:

Manage a USDC wallet for AI agents on Base, supporting balance checks and x402 payments with configurable network and key settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengtang05-hash](https://clawhub.ai/user/chengtang05-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to inspect Base USDC and ETH balances and prepare x402 payments for paid resources from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment signing can authorize real USDC transfers without sufficiently constrained or disclosed transaction terms.

Mitigation: Review the payment terms before use, prefer testnet first, use a dedicated low-balance wallet, and validate the network, USDC contract, recipient, amount, and expiration before signing.

Risk: Arbitrary payment URLs can present payment requirements that are not appropriate for the wallet holder.

Mitigation: Avoid arbitrary payment URLs and only use endpoints whose operator, price, token contract, recipient, and timeout are independently trusted.

## Reference(s):

- [Agent Wallet (Lobster) ClawHub listing](https://clawhub.ai/chengtang05-hash/skills/lobster-agent-wallet)
- [Publisher profile](https://clawhub.ai/user/chengtang05-hash)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JavaScript snippets; CLI commands return plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate network RPC calls and x402 payment requests when run with wallet environment variables.]

## Skill Version(s):

0.1.0 (source: evidence release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
