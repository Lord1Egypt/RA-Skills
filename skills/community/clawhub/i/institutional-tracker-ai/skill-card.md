## Description: <br>
Institutional Tracker Ai analyzes A-share AI-chain stocks with Tushare market data, multi-factor scoring, market-regime checks, sentiment signals, and backtesting to identify possible institutional accumulation buy signals. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[casparzhong-cloud](https://clawhub.ai/user/casparzhong-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial-market researchers use this skill to run local scans and backtests for A-share AI-chain equities, generate HTML reports, and review possible accumulation signals. Its outputs should be treated as research signals, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a Tushare or proxy token in a local Python config file. <br>
Mitigation: Keep config.py out of version control, restrict file permissions, and avoid sharing generated reports or logs that may expose credentials. <br>
Risk: The skill calls third-party market and news data sources while generating signals. <br>
Mitigation: Review configured endpoints before running and use network controls appropriate for the environment. <br>
Risk: The skill may execute another local Xiaohongshu search script if that path exists. <br>
Mitigation: Review or disable external-script paths before installation, especially in shared or production workspaces. <br>
Risk: The generated stock signals can be misleading if treated as financial advice. <br>
Mitigation: Use outputs only for research review and require human financial judgment before any trading decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/casparzhong-cloud/institutional-tracker-ai) <br>
- [Project Homepage](https://github.com/casparzhong-cloud/institutional-tracker-ai) <br>
- [Algorithm Methodology](references/algorithm_methodology.md) <br>
- [Backtest Framework](references/backtest_framework.md) <br>
- [Install Guide](references/install_guide.md) <br>
- [Paper Citations](references/paper_citations.md) <br>
- [Technical Indicator Library](https://github.com/build-web/ta) <br>
- [Chip Distribution Reference](https://github.com/liumenglife/ChipDistribution) <br>
- [Smart Money Concepts Reference](https://github.com/Siva7891/smart-money-concepts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python configuration edits, JSON score data, and generated HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and a user-supplied Tushare proxy token; runs locally on macOS or Linux.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
