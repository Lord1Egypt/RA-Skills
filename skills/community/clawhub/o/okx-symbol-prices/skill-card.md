## Description:

Fetch specified crypto spot prices from OKX and present them in USD display.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chgy123](https://clawhub.ai/user/chgy123)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to retrieve one-shot OKX spot prices for requested cryptocurrency symbols and display the results in USD terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live network requests to www.okx.com, so results depend on external service availability and current market data.

Mitigation: Use the timeout option, handle N/A or null results, and avoid treating returned prices as guaranteed execution quotes.

Risk: The requests dependency is specified with a lower bound rather than an exact pinned version.

Mitigation: Pin and review dependency versions before deployment in controlled environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chgy123/skills/okx-symbol-prices)
- [OKX API Base](https://www.okx.com)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Plain text price list or JSON array of symbol price objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves input symbol order; unavailable supported tickers are reported as N/A or null.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
