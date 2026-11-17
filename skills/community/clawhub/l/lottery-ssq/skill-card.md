## Description:

双色球选号系统 v2 helps an agent update Chinese Double Color Ball draw history, generate two main and three backup number selections, and optionally run backtests using configurable statistical filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasplycc](https://clawhub.ai/user/nasplycc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use this skill to maintain local SSQ draw history, generate disciplined lottery number selections, and review backtest summaries. It is an analysis and entertainment aid, not a prediction tool or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install metadata can automatically install unpinned Python packages.

Mitigation: Install in an isolated environment and pin or review requests and beautifulsoup4 before deployment.

Risk: The history update script contacts a public lottery-data website.

Mitigation: Run the update step only where outbound access to the listed 500.com data source is approved.

Risk: Generated lottery numbers may be mistaken for winning predictions or financial advice.

Mitigation: Present outputs as entertainment or statistical analysis only, matching the artifact disclaimer that winnings are not guaranteed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nasplycc/skills/lottery-ssq)
- [Strategy documentation](artifact/docs/strategy.md)
- [500.com SSQ history data source](https://datachart.500.com/ssq/history/newinc/history.php?start=03001&end=99999)
- [500.com SSQ history page](https://datachart.500.com/ssq/history/history.shtml)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Console text and JSON files containing generated picks, scores, selection attributes, and backtest summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated selections under outputs/ and backtest results under backtests/.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact README and SKILL.md describe v2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
