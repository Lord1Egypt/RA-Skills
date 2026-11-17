## Description:

Trade Polymarket using PMXT cross-exchange predictions and orderbook data for entry/exit signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senarokalie](https://clawhub.ai/user/senarokalie)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to identify Polymarket trading opportunities from PMXT cross-exchange market data and optionally execute dry-run or live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated live trading can use trading credentials and place real Polymarket orders.

Mitigation: Use dry-run mode unless live trading is intentional, restrict API keys to the minimum permissions possible, avoid exposing wallet keys, and keep conservative position and trade limits.

Risk: The documented live-trading safeguards may not match what the implementation enforces.

Mitigation: Review the implementation and test safeguards in dry-run or a limited environment before enabling live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/senarokalie/skills/polymarket-pmxt-trader)
- [Publisher profile](https://clawhub.ai/user/senarokalie)
- [PMXT](https://pmxt.dev)
- [PMXT API base](https://api.pmxt.dev/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with shell command examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run, live trading, positions-only, and smart-sizing modes depending on command flags and credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
