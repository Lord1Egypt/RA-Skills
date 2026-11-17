## Description:

Tracks cryptocurrency prices, helps set threshold or percentage-change alerts, and generates market reports for BTC, ETH, SOL, and meme coins without placing trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to check cryptocurrency market prices, configure local alert rules, and produce concise market summaries. It is for informational monitoring only, not trade execution, DeFi operations, wallet management, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market reports, risk notes, and operation-advice wording could be mistaken for financial advice.

Mitigation: Present outputs as informational only, avoid treating them as investment recommendations, and independently verify market decisions.

Risk: Configured alerts may not fire unless a monitoring process is actually running.

Mitigation: Confirm the alert monitor is active and test alert delivery before relying on it.

Risk: Public market APIs can fail, rate-limit, or return stale or inconsistent prices.

Mitigation: Cross-check important prices against multiple sources and handle API failures or delays explicitly.

## Reference(s):

- [Detailed crypto monitoring reference](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/mimo-crypto-monitor)
- [Binance ticker price API](https://api.binance.com/api/v3/ticker/price)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price)
- [CoinCap assets API](https://api.coincap.io/v2/assets)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with optional Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save alert configuration locally and may query public cryptocurrency market APIs.]

## Skill Version(s):

1.3.1 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
