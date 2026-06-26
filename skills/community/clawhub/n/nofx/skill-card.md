## Description: <br>
NOFX AI Trading OS integration for crypto market data, AI trading signals, strategy management, trader control, and automated reporting on the NOFX platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinkle-community](https://clawhub.ai/user/tinkle-community) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to work with the NOFX crypto-trading platform: reviewing market signals, querying NOFX APIs, managing strategies and traders, running backtests, configuring alerts, and generating market reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with live crypto trading workflows, including strategy activation, trader control, and exchange-connected account activity. <br>
Mitigation: Use paper trading or isolated sub-accounts first, require explicit confirmation before activating strategies or starting traders, and keep withdrawals disabled. <br>
Risk: The skill handles API credentials and exchange access that could affect financial accounts. <br>
Mitigation: Use least-privilege, IP-restricted API keys, store credentials outside shared transcripts, and rotate keys if exposed. <br>
Risk: Deployment instructions include remote installation commands and service exposure patterns. <br>
Mitigation: Review scripts before running them, avoid unreviewed curl-to-bash installs, and do not expose the service over plain HTTP. <br>


## Reference(s): <br>
- [NOFX ClawHub listing](https://clawhub.ai/tinkle-community/nofx) <br>
- [NOFX web dashboard](https://nofxai.com) <br>
- [NOFX data API](https://nofxos.ai) <br>
- [NOFX API docs](https://nofxos.ai/api-docs) <br>
- [NOFX GitHub repository](https://github.com/NoFxAiOS/nofx) <br>
- [API examples](references/api-examples.md) <br>
- [Browser automation guide](references/browser-automation.md) <br>
- [Deployment guide](references/deployment.md) <br>
- [Supported exchanges](references/exchanges.md) <br>
- [Grid trading guide](references/grid-trading.md) <br>
- [Market charts guide](references/market-charts.md) <br>
- [Multi-account guide](references/multi-account.md) <br>
- [Strategy schema](references/strategy-schema.md) <br>
- [Webhooks guide](references/webhooks.md) <br>
- [FAQ](references/faq.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, bash commands, API call examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce market reports and trading workflow guidance; API and browser actions require user-provided NOFX credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
