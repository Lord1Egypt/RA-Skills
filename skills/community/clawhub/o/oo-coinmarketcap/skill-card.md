## Description: <br>
CoinMarketCap lets an agent retrieve cryptocurrency market data, pricing, listings, global metrics, and API key usage information through an OOMOL-connected CoinMarketCap account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query CoinMarketCap data for cryptocurrency discovery, quotes, listings, price conversion, global market metrics, and API key plan usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security verdict is suspicious, with scanner guidance warning about workflows that may use more authority than a review task needs. <br>
Mitigation: Review the release before deployment, use least-privilege execution settings where available, and require explicit confirmation for moderation, publishing, or other high-impact actions. <br>
Risk: The skill requires a connected CoinMarketCap account and API key, so requests depend on sensitive credentials and account limits. <br>
Mitigation: Use OOMOL server-side credential handling, inspect the live connector schema before each action payload, and reconnect or recharge only when an authentication, scope, expiration, or billing error requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-coinmarketcap) <br>
- [CoinMarketCap homepage](https://coinmarketcap.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with oo CLI command examples and JSON payload instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Action responses are connector JSON with data and meta.executionId when commands are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
