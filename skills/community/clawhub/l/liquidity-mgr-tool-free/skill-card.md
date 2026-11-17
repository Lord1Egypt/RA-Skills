## Description:

面向个人用户的 Uniswap V2/V3/V4 流动性查询与基础管理工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Uniswap V2/V3/V4 pools and positions, estimate fees and impermanent loss, and prepare single-position liquidity actions with human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports suspicious activation scope and fund-moving liquidity actions without clear confirmation requirements.

Mitigation: Require explicit user approval before wallet, RPC, add-liquidity, remove-liquidity, modify, delete, save, export, or transaction-signing actions.

Risk: Liquidity actions can move assets or incur gas costs if pool, chain, token amounts, fee tier, range, or destination details are wrong.

Mitigation: Check the exact pool, chain, token amounts, fee tier, gas cost, and destination before executing or signing any transaction.

Risk: The artifact describes wallet and RPC configuration for DeFi workflows.

Mitigation: Keep private keys local, prefer environment variables or permission-restricted configuration, and do not disclose secrets to the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/liquidity-mgr-tool-free)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference wallet, RPC, pool, token, fee tier, range, amount, gas, and destination parameters for user-approved Uniswap liquidity workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
