## Description:

Automates a configurable ETH 15-minute Polymarket mid-candle trading strategy that checks ETH momentum, BTC alignment, volume, entry price, and optional safeguards before paper or live trade execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to configure and run an automated ETH Up/Down Polymarket strategy in paper mode or live mode. It is intended for users who understand market, execution, and account-risk controls before enabling real-money trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has high-impact financial authority when live trading is enabled.

Mitigation: Use paper mode first, keep position sizes low, and avoid unattended cron or live mode until the strategy and account exposure are understood.

Risk: Security evidence reports weak live-mode controls and fail-open safeguards.

Mitigation: Do not use --no-safeguards for live trading; review safeguard behavior before deployment and monitor results closely.

Risk: The skill depends on SIMMER_API_KEY and can optionally use a Discord webhook URL.

Mitigation: Restrict the API key server-side where possible and avoid storing or printing webhook URLs in logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-eth-midcandle)
- [ClawHub publisher profile](https://clawhub.ai/user/djdyll)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, API calls]

**Output Format:** [CLI text output, configuration updates, JSON automaton status, and trade API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run in paper mode by default or live mode when configured; live mode may execute real-money Polymarket trades.]

## Skill Version(s):

1.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
