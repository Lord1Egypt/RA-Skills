## Description: <br>
Users describe a trading style in natural language, and the skill creates a crypto trading bot, runs local backtests, supports periodic reflection-driven evolution, and can optionally connect to an external platform for verification and simulated live trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fei-moss](https://clawhub.ai/user/fei-moss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language crypto trading ideas into local strategy parameters, backtests, and evolution plans. When explicitly enabled, it can package verification uploads or run simulated live-trading workflows against the configured Moss platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit trading-bot data to the configured platform. <br>
Mitigation: Review the platform URL before upload and require explicit user confirmation before any verification upload. <br>
Risk: The skill can store platform API credentials locally. <br>
Mitigation: Keep the credentials file private, use the configured credentials path intentionally, and never print API secrets in responses. <br>
Risk: The skill can run automated simulated-trading order loops. <br>
Mitigation: Require explicit confirmation before auto trading, prefer a finite max-cycles value for live runs, and surface trading errors to the user. <br>
Risk: The skill installs Python dependencies for local execution. <br>
Mitigation: Install only from the bundled requirements file into the local .venv after user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fei-moss/moss-trade-bot-factory-en) <br>
- [Moss Trader](https://moss.site/agent) <br>
- [Complete Parameter Reference](knowledge/params_reference.md) <br>
- [Complete Evolution Guide](knowledge/evolution_guide.md) <br>
- [Platform Operations Manual](knowledge/platform_ops.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON parameter files, and local backtest or upload artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local bot-parameter JSON, fingerprint JSON, backtest-result JSON, upload-package JSON, logs, and a local Python virtual environment when the user confirms setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
