## Description:

Execute triangular arbitrage on Base network via KyberSwap for finding arbitrage opportunities, calculating optimal swap paths, executing multi-hop trades, and managing gas and slippage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to reason about KyberSwap triangular arbitrage on Base, including quote retrieval, path calculation, trade execution parameters, and risk checks for gas, slippage, price impact, and token contract behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide real on-chain cryptocurrency trades, which may be irreversible and may cause financial loss.

Mitigation: Use quote or simulation mode by default, require explicit approval for each transaction, and validate token addresses, recipient addresses, slippage, gas cost, and price impact before execution.

Risk: The security assessment flags missing clear consent, irreversibility, and loss-risk controls.

Mitigation: Add human confirmation gates and loss-limit checks before any swap execution guidance is followed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harleyscodes/skills/kyberswap-arbitrage)
- [Publisher profile](https://clawhub.ai/user/harleyscodes)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction-planning guidance and code snippets for quote, path, and swap logic.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
