## Description:

Generates a structured global market snapshot covering major stock indices and commodities using public finance sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiediking](https://clawhub.ai/user/jiediking)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to assemble a current market snapshot for major U.S., China, Japan, and India stock indices plus gold, silver, crude oil, and copper. It supports daily market summaries where the agent fetches raw public finance data, calculates changes, and presents a concise report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live public finance sources may fail, rate limit, or change response formats, which can lead to N/A values or incomplete snapshots.

Mitigation: Treat results as informational market data and verify market-sensitive decisions against authoritative financial sources.

Risk: Raw market payloads must be parsed and calculated by the agent, so parsing errors or incorrect close-price selection can misstate daily change.

Mitigation: Use the documented close-array method for Yahoo Finance, follow the stated fallback order, and preserve N/A handling when payloads are unavailable or unparsable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiediking/skills/market-global-snapshot)
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/{TICKER}?interval=1d&range=5d)
- [Trading Economics United States stock market](https://tradingeconomics.com/united-states/stock-market)
- [Trading Economics China stock market](https://tradingeconomics.com/china/stock-market)
- [Trading Economics Japan stock market](https://tradingeconomics.com/japan/stock-market)
- [Trading Economics India stock market](https://tradingeconomics.com/india/stock-market)
- [Sina Finance market quote endpoint](https://hq.sinajs.cn/list=sh000680)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown market report with timestamped index and commodity rows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes price, daily change, and percent change; unavailable items may be marked N/A when sources fail.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
