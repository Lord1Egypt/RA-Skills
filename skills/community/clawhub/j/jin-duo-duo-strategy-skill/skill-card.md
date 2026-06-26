## Description: <br>
A stock technical-analysis skill that calculates MA, MACD, and volume indicators, matches six trading strategies, and produces strategy recommendations with risk notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liupython520](https://clawhub.ai/user/liupython520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze historical stock OHLCV data, calculate technical indicators, match predefined trading-strategy patterns, and generate a report with signals, suggested posture, and risk reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat technical-analysis output as financial advice or an automated trading instruction. <br>
Mitigation: Present outputs as educational analysis only, require independent investment judgment, and avoid using the skill as an automated trading system. <br>
Risk: Unpinned pandas and numpy dependencies may change behavior across environments. <br>
Mitigation: Install dependencies from a trusted package index and pin reviewed package versions for reproducible deployments. <br>
Risk: Retaining stock-analysis history may expose user interests or trading research. <br>
Mitigation: Avoid enabling memory or persistent logging unless the user explicitly accepts retention of analysis history. <br>


## Reference(s): <br>
- [Strategy guide](references/strategy-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/liupython520/jin-duo-duo-strategy-skill) <br>
- [Publisher profile](https://clawhub.ai/user/liupython520) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis report with optional JSON indicator output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires historical stock data with date, open, high, low, close, and volume fields; at least 20 trading days are required and 60 are recommended.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
