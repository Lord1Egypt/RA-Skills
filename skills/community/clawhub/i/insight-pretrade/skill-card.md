## Description:

Insight Pre-Trade gives onchain agents a signed, re-verifiable assessment of price trustworthiness before signing a trade for $0.02 USDC per successful x402 check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imokokok](https://clawhub.ai/user/imokokok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and onchain trading agents use this skill to assess oracle price trustworthiness before signing swaps, loans, repayments, or liquidations. The verdict informs the agent's trading policy rather than authorizing a trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A paid check calls an external service and may spend USDC from an agentic wallet.

Mitigation: Approve the disclosed x402 fee and wallet access before enabling calls; budget for charged BLOCK checks.

Risk: A PASS verdict may be mistaken for proof of price correctness or trade approval.

Mitigation: Use the verdict as advisory input under the agent's own trading policy, not as automatic authorization.

Risk: A verdict may be stale by the time the agent trades.

Mitigation: Check each assessment's freshness and validity window before acting.

## Reference(s):

- [Insight homepage](https://www.oracleinsight.xyz)
- [Insight receipt verification](https://www.oracleinsight.xyz/verify)
- [Insight Pre-Trade on ClawHub](https://clawhub.ai/imokokok/skills/insight-pretrade)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text or Markdown summarizing a signed pre-trade verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PASS, WARN, or BLOCK with supporting price and risk metrics; receipt signature can be checked separately.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
