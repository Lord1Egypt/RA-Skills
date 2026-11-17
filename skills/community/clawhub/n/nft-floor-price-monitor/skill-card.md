## Description:

Monitor NFT collection floor prices across platforms, set target alerts, compare multiple collections, track history, and receive Discord DM notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and NFT market participants use this skill to check collection floor prices, compare collections, configure threshold alerts, and optionally send Discord webhook notifications when a floor crosses a target.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discord webhook URLs and alert details can expose sensitive notification configuration or trading intent if placed in shared command logs or error output.

Mitigation: Prefer DISCORD_WEBHOOK_URL from an environment variable or secret manager, avoid passing webhook URLs in shared commands, and treat failed alert logs as sensitive.

Risk: Configured Discord alerts send collection names, thresholds, floor prices, and timestamps to the webhook destination.

Mitigation: Enable Discord delivery only for NFT collections and alert thresholds that are acceptable to share with the configured Discord endpoint.

Risk: Floor-price results depend on external API availability and may be missing, delayed, or inconsistent across sources.

Mitigation: Review the reported source and null or missing floor-price values before relying on alert results for financial decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fuzzyb33s/skills/nft-floor-price-monitor)
- [Publisher profile](https://clawhub.ai/user/fuzzyb33s)
- [OpenSea Collection API v2 endpoint](https://api.opensea.io/api/v2/collections/{slug})
- [OpenSea Collection API v1 endpoint](https://api.opensea.io/api/v1/collection/{slug})
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI examples; script output as plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch NFT and ETH pricing from external APIs and optionally post alert payloads to a user-configured Discord webhook.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact metadata lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
