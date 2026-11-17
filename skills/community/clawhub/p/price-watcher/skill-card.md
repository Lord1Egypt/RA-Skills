## Description:

Monitor product URLs to track and alert on significant price changes using a local watchlist without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Price Watcher to add product URLs to a local watchlist, check current prices, compare changes against a threshold, and produce Markdown alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently fetch any URL stored in the local watchlist.

Mitigation: Only add trusted public product pages; avoid internal, localhost, metadata-service, credential-bearing, or otherwise sensitive URLs.

Risk: Scheduled checks can repeatedly request retailer pages and may trigger rate limits, blocks, CAPTCHA pages, or inaccurate no-price results.

Mitigation: Use conservative schedules, review fetch_error and no_price results, and use manual price entry for heavily protected sites.

Risk: Optional webhook delivery can send product names, URLs, and price history-derived alerts outside the local environment.

Mitigation: Review alert content before enabling webhook delivery and restrict webhook destinations to trusted channels.

Risk: The local watchlist stores product URLs, last prices, timestamps, and price history.

Mitigation: Treat watchlist.json as local user data and avoid adding private or sensitive purchase-intent information.

## Reference(s):

- [Price Watcher Setup Guide](references/setup-guide.md)
- [ClawHub Price Watcher Listing](https://clawhub.ai/newageinvestments25-byte/skills/price-watcher)
- [Publisher Profile](https://clawhub.ai/user/newageinvestments25-byte)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [JSON price-check results, Markdown alert reports, and command/configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and updates a local watchlist.json file with product URLs, prices, timestamps, and capped price history.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
