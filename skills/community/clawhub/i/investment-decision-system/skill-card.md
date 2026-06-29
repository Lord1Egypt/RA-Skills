## Description: <br>
Personal investment decision-support skill that structures portfolio records, INVEST six-factor scoring, position sizing, risk checks, and interactive HTML reports into a decision workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and individual investors use this skill to organize holdings, evaluate buy/sell/hold decisions with the INVEST framework, calculate position size, check risk discipline, and generate review reports. Its outputs are informational decision-support materials, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial scoring thresholds, buy/sell labels, stop-loss percentages, and position sizing may be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational decision support, verify market data, and seek qualified financial advice before acting. <br>
Risk: Portfolio, trade, and decision records are stored locally in the skill directory. <br>
Mitigation: Install and run only in a trusted local workspace, and avoid entering sensitive records on shared machines. <br>
Risk: Report fields render user-provided text into local HTML reports. <br>
Mitigation: Avoid pasting untrusted HTML-like content into notes, theses, or risk fields, and review generated reports before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/investment-decision-system) <br>
- [INVEST decision framework reference](references/framework.md) <br>
- [Investment indicators reference](references/indicators.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, text summaries, and local HTML reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local SQLite database under data/investment.db and HTML reports under outputs/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
