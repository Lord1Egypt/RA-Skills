## Description:

Trade Polymarket strike/action markets using military aircraft ADS-B positioning via pref.trade. Fires when tracked mil aircraft cluster in a target region.

This skill is for research and development only.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor pref.trade military ADS-B clusters across configured regions, inspect Polymarket strike/action opportunities, and run dry-run, SIM, or explicit live trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is a disclosed trading automation tool, and server security evidence says some advertised financial safety controls are not reliably implemented.

Mitigation: Use dry-run or SIM mode first; for real funds, use a dedicated environment, narrowly scoped API keys, pinned dependencies, external account-level limits, and manual monitoring of open positions and P&L.

Risk: Military aircraft positioning is a heuristic signal and may not predict market outcomes.

Mitigation: Treat cluster signals as exploratory, validate behavior with paper trading, and review market context manually before enabling live execution.

Risk: Live mode can place real-money Polymarket trades when credentials and wallet linkage are present.

Mitigation: Keep the default dry-run posture unless a human deliberately enables live mode, confirms wallet setup, and monitors trade size, exposure, and daily activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-mil-aircraft-tracker)
- [Disclaimer](DISCLAIMER.md)
- [Configured regions](regions.yaml)
- [pref.trade MCP endpoint](https://pref.trade/mcp)
- [pref.trade agent registration API](https://pref.trade/v1/agents/register)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with optional JSON automaton summary and configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run is the default; live trading requires explicit opt-in and configured credentials.]

## Skill Version(s):

1.2.0 (source: server release evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
