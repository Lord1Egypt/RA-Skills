## Description: <br>
Automated trader for Polymarket weather highest temperature markets. Uses Simmer SDK's importable endpoint for market discovery and trades only during local 9-10 AM window when YES price exceeds threshold. Supports Telegram notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stefantaylor5](https://clawhub.ai/user/stefantaylor5) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and traders use this skill to automate discovery, monitoring, and optional live execution for Polymarket highest-temperature weather markets through the Simmer SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated live execution can trade or redeem real funds. <br>
Mitigation: Review the live execution path, run dry-run mode first, and use a dedicated low-balance wallet or managed account before enabling live trading. <br>
Risk: Credential-bearing environment variables and Telegram tokens can be exposed through examples, local files, or browser URLs. <br>
Mitigation: Keep secrets out of shared files, replace any example tokens, and rotate credentials that may have been exposed. <br>
Risk: Dependency ranges are not pinned for real-money automation. <br>
Mitigation: Pin or lock dependencies before relying on the skill for live trading. <br>
Risk: Automatic redemption may move funds in ways the operator did not intend. <br>
Mitigation: Disable automatic redemption unless the operator explicitly wants that behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stefantaylor5/polymarket-weather-high-temp-sniper) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [Simmer agent registration](https://simmer.markets/agents/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, notifications] <br>
**Output Format:** [Console text, JSON runtime state, Telegram notifications, and Markdown documentation with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run mode is the default; live trading is enabled only when the script is run with --live.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
