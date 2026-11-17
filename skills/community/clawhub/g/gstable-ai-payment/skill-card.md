## Description:

GStable AI Payment Protocol - enables AI Agents to discover, negotiate, and execute cryptocurrency payments on behalf of users

This skill is ready for commercial/non-commercial use.

## Publisher:

[d5c5ceb0](https://clawhub.ai/user/d5c5ceb0)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect GStable payment links, create signed payment sessions, prepare payment calldata, check balances and allowances, and submit stablecoin payments across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a wallet private key to sign and submit live on-chain transactions.

Mitigation: Use a dedicated low-balance wallet and verify the chain, token, recipient, spender, amount, and calldata before approval or execution.

Risk: The one-command payment path can automatically approve tokens and the approval command defaults to a maximum token allowance when no amount is supplied.

Mitigation: Prefer the step-by-step flow for review, supply explicit approval amounts where possible, and revoke unneeded allowances after payment.

Risk: Custom API or RPC endpoints can affect returned payment details, calldata, balances, gas estimates, and submitted transactions.

Mitigation: Use only GStable API and RPC endpoints that the operator fully trusts.

## Reference(s):

- [GStable AI Payment Protocol Documentation](https://docs.gstable.io/zh-Hans/docs/category/ai-payment-protocol)
- [GStable AI Agent Integration Documentation](https://docs.gstable.io/zh-Hans/docs/category/ai-agent-integration)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WALLET_PRIVATE_KEY; outputs can include wallet addresses, payment session identifiers, transaction calldata, balances, allowances, and transaction hashes.]

## Skill Version(s):

1.0.0 (source: pyproject.toml and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
