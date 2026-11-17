## Description:

Screen a watchlist of stock tickers for cash-secured put candidates suited to the options wheel strategy, using free Yahoo Finance data via yfinance with no API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to screen ticker watchlists for cash-secured put candidates, compare estimated wheel-strategy premium yields, and review basic liquidity signals before further trade analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Options data or yield estimates may be stale, incomplete, or unsuitable for making a trade decision.

Mitigation: Verify options quotes, liquidity, and strategy assumptions independently before making trades.

Risk: The yfinance dependency is not pinned, so future package versions could change behavior.

Mitigation: Install in a virtual environment and pin or review dependency versions before operational use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and tabular command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces screening estimates only; it does not place trades or connect to brokerage accounts.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
