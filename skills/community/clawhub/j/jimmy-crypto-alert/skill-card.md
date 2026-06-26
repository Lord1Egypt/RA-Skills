## Description: <br>
Monitor cryptocurrency prices and send alerts when configured thresholds are crossed, using public market-price APIs without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to check supported cryptocurrency prices, configure local threshold alerts, and receive optional alert notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence flags this release as suspicious because the documentation is inconsistent and the alert-setting script can mishandle crafted input. <br>
Mitigation: Review or patch the scripts before use; accept only simple token names, numeric thresholds, and non-sensitive alert messages. <br>
Risk: Alert state is stored locally and optional notification setup may involve Telegram credentials. <br>
Mitigation: Do not add Telegram credentials to this package as shipped, and remove ~/.crypto-alert-state.json to clear saved alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimmyclanker/jimmy-crypto-alert) <br>
- [Binance public API](https://api.binance.com/api/v3) <br>
- [CoinGecko public API](https://api.coingecko.com/api/v3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Terminal text output and local JSON alert-state configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes alert state to ~/.crypto-alert-state.json when alerts are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
