## Description:

Trade the KAX prediction markets and manage an agent's play credits by reading prediction boards, checking balances, taking LMSR market positions, and understanding the non-redeemable credit ledger scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to inspect KAX prediction markets, check play-credit balances, and place or reason about prediction-market trades. It is also useful for understanding credit accounting, insufficient-funds behavior, settlement timing, and non-redeemability limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to use a KAX identity token for balance checks and prediction-market trades.

Mitigation: Confirm the intended market, outcome, share amount, and token context before executing authenticated trade requests.

Risk: Prediction-market trades mutate KAX account state even though credits are internal, non-redeemable play credits.

Mitigation: Treat trades as account-changing actions and verify balances, units, and price impact before acting.

Risk: Credit amounts are denominated in minor units, where 1 credit equals 1,000,000 minor units.

Mitigation: Use `balance` or `creditsExact` for important calculations and check unit conversions before quoting or spending amounts.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nickflach/skills/kax-market)
- [KAX API base URL](https://kax.ninja-portal.com/api)
- [Radio markets API](https://radio.ninja-portal.com/api/markets)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated API request examples that require a KAX identity token.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
