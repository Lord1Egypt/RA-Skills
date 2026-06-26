## Description: <br>
Creates cryptocurrency trading bots from natural-language strategy descriptions, runs local backtests, supports iterative parameter evolution, and can optionally connect to an external platform for verification or simulated live trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fei-moss](https://clawhub.ai/user/fei-moss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn a trading style description into bot parameters, run local Binance USDT-M backtests, review evolved parameter schedules, and optionally submit results to a Moss trading platform workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store reusable platform credentials in a local agent_creds.json file. <br>
Mitigation: Use only the intended platform URL, restrict file access to the credential path, and rotate or delete the credentials when platform access is no longer needed. <br>
Risk: The skill can start unattended live trading after a broad approval. <br>
Mitigation: Enable automatic trading only after reviewing backtest results, set a max cycle count for live runs, and prefer manual mode when each order should receive explicit confirmation. <br>
Risk: Generated strategies may use leveraged cryptocurrency positions. <br>
Mitigation: Use low leverage, small position limits, and conservative risk-per-trade settings; review stop-loss and take-profit parameters before any live run. <br>
Risk: Platform-connected verification and trading workflows send data and signed requests to the configured platform. <br>
Mitigation: Confirm the platform origin before binding, uploading, or live trading, and avoid submitting credentials or strategy packages to unexpected hosts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fei-moss/moss-trade-bot-factory) <br>
- [Publisher Profile](https://clawhub.ai/user/fei-moss) <br>
- [Moss Trader Platform](https://moss.site/agent) <br>
- [Platform Operations Guide](artifact/knowledge/platform_ops.md) <br>
- [Parameter Reference](artifact/knowledge/params_reference.md) <br>
- [Evolution Guide](artifact/knowledge/evolution_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON parameter files and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local backtest, fingerprint, evolution, upload package, credential, and live trading log files when the user enables those workflows.] <br>

## Skill Version(s): <br>
1.0.21 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
