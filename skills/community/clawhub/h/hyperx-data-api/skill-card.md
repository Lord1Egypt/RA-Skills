## Description: <br>
HyperX Data API provides reference guidance for building applications with Hyperliquid wallet analytics, market data, crypto Twitter, and news feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyperxtrade](https://clawhub.ai/user/hyperxtrade) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to construct HyperX Data API requests for Hyperliquid wallet analytics, market positions, trading fills, Twitter feeds, news feeds, and BTC mining data while accounting for authentication and rate limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens or session cookies can expose authenticated HyperX access if pasted into chat, logs, or shared code. <br>
Mitigation: Use API tokens instead of session cookies where possible, store credentials in environment variables or a secret manager, and redact secrets from examples and logs. <br>
Risk: Wallet addresses and authenticated requests may be sent to HyperX when using wallet analytics or fills endpoints. <br>
Mitigation: Query only wallet addresses the user intends to analyze and avoid sending sensitive account context beyond what the API request requires. <br>
Risk: Rate limits and endpoint weights can cause failed requests or unexpected quota use. <br>
Mitigation: Check the documented tier budget and endpoint weight before batching requests, and throttle or paginate calls when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hyperxtrade/hyperx-data-api) <br>
- [Publisher profile](https://clawhub.ai/user/hyperxtrade) <br>
- [HyperX Data API base URL](https://data-api.hyperx.trade) <br>
- [HyperX API token settings](https://hyperx.trade/hyperliquid/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with endpoint tables, authentication guidance, and Python and WebSocket examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides API usage against HyperX endpoints; authenticated wallet analysis may require an API token or session cookie.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
