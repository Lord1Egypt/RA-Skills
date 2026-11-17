## Description:

Research and analyze tokens on supported blockchains, including token search, price and market data, security audit signals, liquidity pools, holders, traders, and K-line candlestick data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombmod](https://clawhub.ai/user/bombmod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to research specific tokens before making decisions, using public token data, security audit signals, holder distribution, liquidity, trader, and candlestick information. It is informational only and does not execute trades or broadcast transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill tells agents to silently install a global CLI package and misreport install failures.

Mitigation: Review before installing; ask for confirmation before installing the CLI, prefer a non-global or pinned installation when possible, verify the package source, and report installation errors accurately.

Risk: Token analysis and security audit results may be incomplete or misleading if treated as proof that a token is safe.

Mitigation: Present token security results as informational signals, clearly state raised flags and missing audit data, and recommend independent due diligence.

## Reference(s):

- [LiberFi homepage](https://liberfi.io)
- [Liberfi Token on ClawHub](https://clawhub.ai/bombmod/skills/liberfi-token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON-derived token data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public token data and no authentication; token security results are informational and should not be presented as a guarantee of safety.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
