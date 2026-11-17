## Description:

Use this skill when the user wants to discover the best USDC vaults with LI.FI Earn, ask an agent to choose a safe vault on Base/Arbitrum/Ethereum, prepare a Composer-compatible deposit, execute the deposit with an Agentic Wallet, and explain which receipt token was received after deposit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask an agent to discover USDC yield vaults, recommend a suitable vault, prepare a LI.FI Composer deposit, and explain the resulting receipt token. It is intended for wallet-connected yield workflows on Base, Arbitrum, and Ethereum.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet approval and deposit steps could move user funds without enough explicit confirmation or transaction validation.

Mitigation: Require explicit user confirmation before each approval and deposit, show decoded transaction details, verify contract addresses, limit approvals, and simulate transactions before signing.

Risk: A wrong vault, chain, amount, or insufficient gas balance could produce financial loss or failed execution.

Mitigation: Use small amounts and a wallet prepared for risk, confirm the selected vault and chain with the user, and verify native gas availability before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/miraix-lifi-earn-agent)
- [Miraix Earn discovery API](https://app.miraix.fun/api/earn/chat)
- [Miraix Composer quote API](https://app.miraix.fun/api/earn/quote)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with plain-language recommendations and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include vault name, chain, protocol, APY, rationale, deposit status, gas guidance, and receipt token explanation.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
