## Description:

Trades Polymarket BTC 5-minute and 15-minute fast markets using CEX price momentum signals via the Simmer API, with Binance BTC/USDT klines as the default signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnjerry8749](https://clawhub.ai/user/johnjerry8749)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure and run a dry-run-first trading loop for short-term crypto prediction markets on Polymarket. It can also execute live USDC trades through Simmer after the user reviews API access, sizing, scheduling, and loss risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real-money Polymarket trades when live mode is enabled.

Mitigation: Start in dry-run mode, review the trading logic and position size, and avoid putting --live in cron or heartbeat automation until the user accepts the loss risk.

Risk: An endpoint override can send SIMMER_API_KEY to an untrusted destination.

Mitigation: Use a scoped, revocable Simmer API key and keep SIMMER_API_BASE unset unless the destination is fully trusted and controlled.

Risk: Fast markets, fees, thin liquidity, and short time windows can reduce or eliminate expected edge.

Mitigation: Review fee impact, liquidity, max_position, smart sizing, and configured thresholds before live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnjerry8749/skills/polymarket-fast-loop-1-0-6)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and CLI output text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry run is the default; live mode can execute real Polymarket trades when --live is used.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
