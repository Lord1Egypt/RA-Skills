## Description:

Sets up an autonomous MoltMarkets prediction-market trading system with trader, market creator, resolution crons, Kelly-style bet sizing, and learning-loop memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shirtlessfounder](https://clawhub.ai/user/shirtlessfounder)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to configure recurring MoltMarkets trading, market creation, and resolution workflows with memory files for tracking decisions and performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring agents can spend funds, create markets, post public comments, and resolve markets.

Mitigation: Use a dedicated low-balance account, set spend and rate limits, keep notifications visible, and require manual approval for market creation and resolution before real funds are used.

Risk: Credentials are read from a local MoltMarkets credentials file.

Mitigation: Use narrowly scoped API keys if available and protect the credentials file with restrictive permissions or a real secret store.

Risk: Market titles and comments may be untrusted inputs for recurring agent workflows.

Mitigation: Isolate market titles and comments from agent instructions before allowing automated trading, commenting, or resolution.

Risk: Historical-price oracle logic may affect market resolution accuracy.

Mitigation: Review and fix the historical-price oracle logic, including fallback behavior, before enabling automated resolution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shirtlessfounder/skills/moltmarkets-trading)
- [MoltMarkets API Reference](references/api-reference.md)
- [Cron Job Definitions](references/cron-definitions.md)
- [Kelly Criterion Guide](references/kelly-formula.md)
- [Memory File Templates](references/memory-templates.md)
- [MoltMarkets API](https://api.zcombinator.io/molt)
- [CoinGecko Price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd)
- [Binance Klines API](https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&startTime={ms}&limit=1)
- [HN Algolia API](https://hn.algolia.com/api/v1/items/{storyId})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript cron definitions, JSON configuration examples, and setup instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The setup script creates local memory JSON and Markdown files after validating MoltMarkets credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
