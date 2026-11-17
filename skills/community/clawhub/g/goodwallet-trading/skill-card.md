## Description:

GoodWallet Trading extends GoodWallet MPC agentic wallets with ERC20 transfers, token approvals, Uniswap V2 swaps, arbitrary contract calls, balance checks, and token information queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoniassia](https://clawhub.ai/user/yoniassia)

### License/Terms of Use:

MIT-0

## Use Case:

External GoodWallet users and agents use this skill to inspect Hoodi testnet balances and run MPC-signed ERC20 transfers, approvals, swaps, and contract calls after GoodWallet authorization and pairing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign broad on-chain actions, including arbitrary contract calls and token approvals.

Mitigation: Use only testnet funds unless independently audited, decode calldata before contract-call, verify recipient, spender, router, token, and amount values, and specify exact approval amounts.

Risk: The documented slippage option should not be relied on as price protection.

Mitigation: Avoid swaps unless the expected output and route are independently checked, and treat every submitted swap as potentially irreversible.

Risk: Untrusted SIGN_URL or RPC_URL environment values can redirect signing or chain access.

Mitigation: Set SIGN_URL and RPC_URL only from trusted shells, wrappers, or CI environments and review them before executing trading commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoniassia/skills/goodwallet-trading)
- [Hoodi Explorer](https://hoodi.etherscan.io/)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-language command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce transaction hashes, explorer links, balances, token metadata, and approval or allowance status.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
