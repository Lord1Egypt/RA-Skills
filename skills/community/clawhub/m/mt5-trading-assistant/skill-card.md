## Description: <br>
Automates MetaTrader 5 account monitoring, market data retrieval, and buy, sell, and position-closing workflows through Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[canvascn00-crypto](https://clawhub.ai/user/canvascn00-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent workflow to MetaTrader 5 for account checks, market snapshots, scripted trade execution, and position management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports embedded brokerage credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed credentials, and load secrets from a secure runtime source before installation or use. <br>
Risk: The security evidence reports scripts that can immediately place or close trades without strong safeguards. <br>
Mitigation: Do not use the skill with a funded or live account until every trade and close-position action has an explicit preview and confirmation step. <br>
Risk: The security guidance calls for output minimization or redaction. <br>
Mitigation: Minimize or redact account, position, and financial output before sharing logs or agent transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/canvascn00-crypto/mt5-trading-assistant) <br>
- [Setup guide](references/setup_guide.md) <br>
- [Configuration template](references/config_template.py) <br>
- [MetaTrader5 Python Documentation](https://www.mql5.com/en/docs/integration/python_metatrader5) <br>
- [MT5 API Reference](https://www.mql5.com/en/docs/constants/structures) <br>
- [Exness API Guide](https://exness.com/developers/) <br>
- [IC Markets API](https://www.icmarkets.com/development-api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include account-monitoring summaries, market-data summaries, and MT5 script invocation commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
