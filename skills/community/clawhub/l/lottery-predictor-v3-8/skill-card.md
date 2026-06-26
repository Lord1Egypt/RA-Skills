## Description: <br>
Lottery Predictor V3 8 generates entertainment-only Double Color Ball lottery recommendations and backtest summaries using local historical draw data, machine-learning models, and rule-based scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumuli2021](https://clawhub.ai/user/mumuli2021) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run local lottery analysis, generate entertainment-only number recommendations, and produce backtest summaries from a local SQLite history database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lottery prediction output and advertised accuracy can be mistaken for gambling or financial advice. <br>
Mitigation: Treat predictions and backtests as entertainment-only analysis and do not rely on them for purchasing or financial decisions. <br>
Risk: Backtest runs can create or overwrite local Markdown report files. <br>
Mitigation: Verify the intended report location before running backtests and preserve any reports that should not be replaced. <br>
Risk: The model depends on the selected local SQLite lottery database. <br>
Mitigation: Confirm the database path and data source before running predictions or evaluating claimed accuracy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mumuli2021/lottery-predictor-v3-8) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text with optional Markdown backtest report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Python, SQLite, and lottery history data; backtests may write a local Markdown report.] <br>

## Skill Version(s): <br>
3.8.0 (source: package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
