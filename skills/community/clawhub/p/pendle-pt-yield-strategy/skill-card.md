## Description:

Pendle PT fixed-yield strategy for scanning and ranking markets, tracking positions, monitoring maturities, and preparing managed-wallet or manual execution plans with explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moshu](https://clawhub.ai/user/moshu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and DeFi analysts use this skill to research Pendle PT fixed-yield opportunities, rank stable-ish markets, monitor positions, and prepare deposit, redeem, withdraw, or rollover plans. It is oriented toward managed-wallet execution with manual user-executed fallback and explicit confirmation before any real onchain action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may call live third-party DeFi APIs and can expose wallet-linked quote intent when a real wallet address is used for previews.

Mitigation: Use throwaway or non-sensitive wallet addresses for quote research when possible, and provide a real wallet address only when the operator accepts the metadata exposure.

Risk: Market rankings, route labels, liquidity, borrow caps, and loop data may be incomplete or weakly verified.

Mitigation: Treat outputs as research leads and independently verify protocol support, liquidity, borrow caps, slippage, and URLs before execution.

Risk: Financial plans can lead to real onchain transactions if routed through a managed wallet or manually submitted by the user.

Mitigation: Require explicit confirmation after showing market, chain, amount estimates, slippage or price impact, maturity date, notable risks, and wallet path.

Risk: Local position data may become stale or diverge from actual onchain state.

Mitigation: Reconcile local position records against wallet and protocol state before relying on status, redemption, withdrawal, or rollover recommendations.

## Reference(s):

- [Eligible Underlyings for PT Yield Strategy](references/eligible-underlyings.md)
- [Chain Addresses](references/chain-addresses.md)
- [Pendle PT Ranking Framework](references/ranking-framework.md)
- [Manual Contango PT Comparison Framework](references/manual-contango-comparison.md)
- [Pendle API](https://api-v2.pendle.finance/core)
- [ClawHub Skill Page](https://clawhub.ai/moshu/skills/pendle-pt-yield-strategy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update local JSON position data; outputs should distinguish research, planning, and confirmed execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
