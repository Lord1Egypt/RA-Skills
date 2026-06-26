## Description: <br>
AI-powered stock multi-factor analysis for checking watchlists, viewing reports, triggering analyses, and checking quota across US stocks, cryptocurrency, and China A-shares. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmhu](https://clawhub.ai/user/xmhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage a MarketSensor watchlist, trigger or poll market analyses, retrieve Markdown or JSON reports, and check account quota with a user-provided API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market symbols, watchlist activity, generated report requests, and quota usage to MarketSensor. <br>
Mitigation: Install only if the user trusts MarketSensor with that information. <br>
Risk: The skill depends on MARKETSENSOR_API_KEY for authenticated API access. <br>
Mitigation: Keep the API key private and prefer a limited or revocable key when available. <br>
Risk: Watchlist changes and analysis triggers can modify account state or consume paid quota. <br>
Mitigation: Review requests before letting the agent add or remove watchlist items or trigger analyses. <br>


## Reference(s): <br>
- [MarketSensor skill page](https://clawhub.ai/xmhu/market-sensor) <br>
- [MarketSensor publisher profile](https://clawhub.ai/user/xmhu) <br>
- [MarketSensor website](https://www.marketsensor.ai) <br>
- [MarketSensor Open API Reference](references/api-reference.md) <br>
- [MarketSensor usage examples](references/examples.md) <br>
- [MarketSensor supported markets](references/supported-markets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON market reports, plain-text guidance, and curl-based shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger API calls that consume MarketSensor quota and may modify watchlist state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, _meta.json, and changelog released 2026-03-30) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
