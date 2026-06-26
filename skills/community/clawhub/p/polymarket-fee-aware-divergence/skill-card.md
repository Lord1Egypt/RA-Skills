## Description: <br>
Trades AI-vs-market divergence on Polymarket only when the gap clears fees, spread, and a configurable safety margin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chasewebb](https://clawhub.ai/user/chasewebb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-agent operators use this skill to run a fee-aware prediction-market divergence strategy that only trades when estimated edge exceeds fees, spread, slippage, and a safety margin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run automatically every 30 minutes and place recurring prediction-market trades using sensitive trading credentials. <br>
Mitigation: Keep TRADING_VENUE=sim until tested, use a dedicated low-balance account or scoped API key, and disable the cron or add hard exposure and loss limits before using a live venue. <br>
Risk: Providing wallet private keys can increase custody and credential exposure risk. <br>
Mitigation: Avoid providing a wallet private key unless external-wallet self-custody trading is necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chasewebb/polymarket-fee-aware-divergence) <br>
- [Simmer Markets](https://simmer.markets) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Console logs and trade reasoning strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place recurring prediction-market trades through Simmer SDK when credentials and a trading venue are configured.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
