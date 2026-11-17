## Description:

Calculates the real-time Bitcoin Kimchi Premium by comparing Upbit KRW and Binance USD Bitcoin prices using live USD/KRW exchange rates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seungdols](https://clawhub.ai/user/seungdols)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to fetch public BTC market prices and USD/KRW rates, then calculate the current Kimchi Premium for comparison between South Korean and global Bitcoin markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to exchange-rate, Upbit, and Binance APIs whenever it runs.

Mitigation: Run it only in environments where public market API calls to open.er-api.com, api.upbit.com, and api.binance.com are allowed.

Risk: Live market data can be unavailable, delayed, or changed by the upstream APIs.

Mitigation: Treat the JSON output as a point-in-time market calculation and handle error JSON or missing data before using it in downstream decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seungdols/skills/kimp-price)
- [ClawHub publisher profile](https://clawhub.ai/user/seungdols)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Pretty-printed JSON emitted to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timestamp, USD/KRW rate, Upbit BTC price, Binance BTC price, Kimchi Premium percentage, and KRW price difference; errors are emitted as JSON.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
