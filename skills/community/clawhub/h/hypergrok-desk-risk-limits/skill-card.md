## Description:

How the Risk Manager writes the desk's risk limits with the user, sizes every proposed trade from live account state and Hyperliquid's real constraints, checks the book, and issues a PASS or REJECT with exact ticket fields. Use for setting up or changing limits, sizing any trade, and answering "how's the book".

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Risk managers and trading desk operators use this skill to set and enforce user-defined limits, size proposed perpetual trades from current account and market data, and review open exposure. It returns a PASS or REJECT with calculations and ticket fields, or identifies missing inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is suspicious because referenced paths were unavailable, leaving coverage incomplete.

Mitigation: Review the unavailable materials and the skill instructions before installing or relying on it, and consider the Review verdict.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Configuration]

**Output Format:** [Markdown risk assessments, sizing calculations, and ticket fields; optionally a risk-limits.md file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fresh live account, market, and order data; rejects when required inputs are missing or stale.]

## Skill Version(s):

1.9.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
