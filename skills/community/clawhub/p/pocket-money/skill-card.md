## Description:

Give your AI agent crypto wallets on Base. Create purpose-specific wallets, ask your human to fund each one, check balances, and manage budgets. No accounts, no KYC - just wallet addresses and USDC on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[operator-auteng-ai](https://clawhub.ai/user/operator-auteng-ai)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to give an agent small, purpose-specific USDC wallets on Base, then request funding, check balances, and track budgets with human approval before spending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real USDC balances and stores wallet private keys locally.

Mitigation: Fund only small, purpose-specific amounts and keep `.auteng/wallets/` files out of source control and backups.

Risk: A leaked wallet file or compromised machine can expose funds held by that wallet.

Mitigation: Treat wallet files like passwords, use restricted local access, and rotate to new wallets if exposure is suspected.

Risk: Agent-initiated spending can create unintended costs.

Mitigation: Require explicit human approval before every spend and list estimated cost, wallet, and purpose before proceeding.

Risk: Installing or running the npm package introduces third-party package and network dependency risk.

Mitigation: Review or pin the npm package where possible and install only in environments where outbound Base RPC access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/operator-auteng-ai/skills/pocket-money)
- [Pocket Money homepage](https://github.com/operator-auteng-ai/pocket-money)
- [npm package @auteng/pocket-money](https://www.npmjs.com/package/@auteng/pocket-money)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance focuses on wallet creation, funding requests, balance checks, and approval prompts.]

## Skill Version(s):

2.0.0 (source: VERSION.txt and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
