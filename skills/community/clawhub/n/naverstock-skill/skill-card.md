## Description:

Fetch text-based real-time stock prices for KRX and overseas markets using Naver Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seungdols](https://clawhub.ai/user/seungdols)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to look up current stock and exchange-rate data from Naver Finance by providing a ticker, stock name, or supported currency query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock names, tickers, and exchange-rate queries are sent to Naver Finance.

Mitigation: Do not enter confidential watchlists, private notes, proprietary identifiers, or other sensitive free-text queries.

Risk: Returned market data depends on live external Naver Finance responses and may differ from other sources or trading venues.

Mitigation: Verify prices and exchange rates with an authoritative market-data source before making financial or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seungdols/skills/naverstock-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON printed by a Node.js command-line script, with error responses also returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and network access to Naver Finance; supported operating systems are macOS, Linux, and Windows.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
