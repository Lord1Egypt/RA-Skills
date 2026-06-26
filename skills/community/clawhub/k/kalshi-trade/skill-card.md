## Description: <br>
Read-only Kalshi OpenAPI scouting skill for market discovery, liquidity checks, and market validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRS999](https://clawhub.ai/user/BRS999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect Kalshi exchange status, markets, events, series, trades, and order books for scouting and validation before any separate execution workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setting KALSHI_BASE_URL can redirect read-only requests to a replacement API endpoint. <br>
Mitigation: Leave KALSHI_BASE_URL unset unless the replacement endpoint is intentionally trusted. <br>
Risk: Market scouting output could be mistaken for trading execution capability. <br>
Mitigation: Use a separate reviewed skill for order placement, amendment, cancellation, portfolio, or account actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BRS999/kalshi-trade) <br>
- [Kalshi Trade API v2 base URL](https://api.elections.kalshi.com/trade-api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with shell commands; command output is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js; KALSHI_BASE_URL is optional and defaults to the Kalshi production API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
