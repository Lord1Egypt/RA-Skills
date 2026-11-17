## Description:

Kelly Formula Crypto calculates crypto position sizes with Kelly Criterion, fractional Kelly suggestions, multi-strategy allocation, leverage safety checks, and disclosed x402 payment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to estimate crypto trading position sizes, compare full, half, and quarter Kelly allocations, and check leverage safety for a trading thesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 requests can transfer 0.01 USDC through the disclosed payment flow.

Mitigation: Confirm the payment amount, destination wallet, chain, and API endpoint before invoking the skill.

Risk: Position recommendations can be misleading when win probability, payoff, loss, or leverage inputs are inaccurate or unbounded.

Mitigation: Validate finite inputs, review assumptions, apply strict position caps, and keep a human review step before trading.

Risk: Leverage can cause liquidation even when a Kelly estimate appears favorable.

Mitigation: Use conservative fractional Kelly settings, require leverage safety checks, and review stop-loss distance before using any result.

## Reference(s):

- [Kelly Formula Crypto ClawHub page](https://clawhub.ai/jinboh68-prog/skills/kelly-formula-crypto)
- [Skill API endpoint](https://kelly-formula-crypto.vercel.app/api/calculate)
- [Original article referenced by the skill](https://x.com/KKaWSB/status/1968453490084299020)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, JSON, guidance]

**Output Format:** [Plain text or JSON calculation results, with Markdown guidance and inline command examples in documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes position-size percentages, fractional Kelly recommendations, net-edge values, and optional leverage safety results.]

## Skill Version(s):

1.0.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
