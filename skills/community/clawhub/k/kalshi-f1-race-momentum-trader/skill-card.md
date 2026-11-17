## Description:

Trades F1 Drivers Championship markets on Kalshi using recent race results weighted by recency, with hot streaks boosting championship probability and cold streaks reducing it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading strategy developers use this skill to evaluate and optionally trade Kalshi F1 Drivers Championship markets with a configurable recent-race momentum model. It is intended for users who can manage trading credentials, market risk, and live-execution settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real-money trades through Kalshi via DFlow/Solana.

Mitigation: Keep the skill in dry-run until the static model inputs, market behavior, and execution settings have been reviewed; require explicit live-mode enablement.

Risk: Trading credentials and the Solana private key can expose funds if over-scoped or reused.

Mitigation: Use dedicated, low-balance trading credentials and avoid providing a broad wallet private key unless live execution has been reviewed.

Risk: The default model relies on static recent-race results and base probabilities.

Mitigation: Refresh and validate model inputs before live trading, especially after race weekends or market-moving events.

Risk: Dependency behavior can change if simmer-sdk is installed without a pinned version.

Mitigation: Prefer a pinned simmer-sdk version and review dependency updates before deploying live trading.

Risk: Live-trade safeguards may be insufficient for unattended approval.

Mitigation: Use conservative max-position, max-trades, slippage, and liquidity settings, and add stronger confirmation or fail-closed controls before automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-f1-race-momentum-trader)
- [Simmer skills homepage](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text with optional JSON automaton reports and Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform API calls and live trades only when explicitly run with the live flag and valid credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
