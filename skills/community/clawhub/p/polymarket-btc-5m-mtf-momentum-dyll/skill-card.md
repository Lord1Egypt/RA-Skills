## Description:

Runs a configurable BTC 5-minute momentum trading bot that compares 1m, 3m, and 5m Binance BTC/USDT returns and can place simulated or live Simmer/Polymarket fast-market trades when confidence thresholds are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to run or adapt a momentum-based bot for BTC 5-minute prediction markets, with tunable confidence, timing, and trade-size settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Simmer API key can be sent to an environment-controlled API endpoint.

Mitigation: Use a least-privileged Simmer API key and leave SIMMER_API_URL set to the official HTTPS endpoint unless the endpoint has been reviewed.

Risk: The simmer-sdk dependency is unpinned.

Mitigation: Pin or review simmer-sdk before installation and deployment.

Risk: Live mode can place real trades.

Mitigation: Start in paper mode, enable --live only after review, and keep explicit trade limits and monitoring in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-btc-5m-mtf-momentum-dyll)
- [Simmer API endpoint](https://api.simmer.markets)
- [Binance Klines API endpoint](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, JSON, configuration]

**Output Format:** [CLI text output with optional JSON automaton reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update local tunables and report positions, trade attempts, executed trades, skip reasons, and execution errors.]

## Skill Version(s):

1.1.0 (source: server evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
