## Description: <br>
Monitor NFT collection floor prices, compare collections, set target alerts, and optionally send Discord webhook notifications when floors cross thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check NFT collection floor prices, compare collections, and configure threshold alerts. It is suited for monitoring and reporting workflows, not as a substitute for independent trading or valuation review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenSea API keys and Discord webhook URLs can expose sensitive access if shared in prompts, command history, or logs. <br>
Mitigation: Use environment variables for secrets, avoid passing webhook URLs in shared commands, restrict secret access, and rotate exposed values. <br>
Risk: NFT floor price data depends on external APIs and may be unavailable, delayed, rate-limited, or unsuitable for trading decisions on its own. <br>
Mitigation: Confirm prices against trusted sources before acting, handle failed fetches, and respect API rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzzyb33s/nft-floor-price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text floor reports or JSON records; skill guidance uses Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call OpenSea, CoinGecko, and Discord webhook endpoints when invoked.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
