## Description:

Reads Hyperliquid account positions, balances, orders, fills, funding, ledger, portfolio, fee, and rate-limit data through read-only API calls, with curl and Python examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Desk operators and developers use the skill to review account exposure, reconcile orders and fills, inspect funding and portfolio history, and prepare sizing or risk checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional role and approved-agent queries retrieve account authorization metadata in addition to financial data.

Mitigation: Use those queries only when the account review requires role or approved-agent details.

Risk: The security assessment has incomplete coverage because two local references could not be resolved.

Mitigation: Review the unresolved references and assess their behavior before relying on the scanner verdict.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/galleonlabs/skills/hypergrok-hyperliquid-account)
- [HyperGrok Trading Desk project attribution](https://github.com/galleonlabs/hypergrok-trading-desk)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Code]

**Output Format:** [Markdown with inline curl and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account data retrieval guidance.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
