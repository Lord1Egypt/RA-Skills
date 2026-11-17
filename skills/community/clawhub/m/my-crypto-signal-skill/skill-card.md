## Description:

Provides crypto trading signals, price prediction, and market analysis for Binance pairs using market data, news, and macro-event triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k2-l](https://clawhub.ai/user/k2-l)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run a crypto signal pipeline for Binance symbols, combining technical indicators and news sentiment into BUY, SELL, or HOLD summaries. Outputs should be treated as informational analysis, not financial advice or automated trading authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts market and news APIs and may use a configured proxy with user-provided credentials.

Mitigation: Install only when those third-party service calls and credential requirements are acceptable; prefer environment variables or the chmod 600 credentials file described by the skill.

Risk: BUY, SELL, and HOLD outputs could be mistaken for automated trading authority or financial advice.

Mitigation: Use outputs as informational analysis only and require human review before making trading decisions.

Risk: Generated market data, signal records, and verification history are stored on disk.

Mitigation: Review local retention and sharing practices for the generated data, signals, and records directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k2-l/skills/my-crypto-signal-skill)
- [Binance API base endpoint](https://api.binance.com/api/v3)
- [CryptoPanic posts API endpoint](https://cryptopanic.com/api/v1/posts/)
- [NewsAPI everything endpoint](https://newsapi.org/v2/everything)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown summaries with shell commands and JSON-backed signal records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local data, signals, and records files; requires a NewsAPI key and may use optional CryptoPanic, Binance, and proxy credentials.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
