## Description:

Research prediction-market odds, order books, price history, and public market rules across Polymarket, Kalshi, Metaculus, and DraftKings Predictions, whose routes cover categories, availability, and rules rather than live quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to compare live and historical market odds, order-book data, community forecasts, and public settlement rules across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawlora receives research queries and the API key; the helper briefly stores the key in a private temporary file.

Mitigation: Avoid confidential query content, use only a Crawlora key, and keep it in CRAWLORA_API_KEY without hardcoding or committing it.

Risk: Successful requests consume Crawlora credits.

Mitigation: Check credit usage when making repeated or large batches of requests.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Normalized JSON market data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public information; DraftKings routes provide categories, availability, and rules rather than live quotes.]

## Skill Version(s):

1.0.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
