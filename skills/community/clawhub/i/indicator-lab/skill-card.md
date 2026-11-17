## Description:

Indicator Lab helps an agent backtest 13 technical indicators on SPY and QQQ using five years of daily data, including single, paired, and triple-indicator strategies ranked by return, Sharpe ratio, and max drawdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plato-1](https://clawhub.ai/user/plato-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, quant researchers, and trading analysts use this skill to have an agent backtest technical indicator strategies on SPY and QQQ, compare single and combined indicator signals, and summarize rankings against a buy-and-hold baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The referenced backtest script is missing from the submitted artifact, so the skill may not run as described.

Mitigation: Verify that scripts/indicator_backtest.py is supplied elsewhere before executing the skill or relying on generated commands.

Risk: Dependency installation is not pinned, which can lead to inconsistent behavior or unexpected package changes.

Mitigation: Install in a dedicated virtual environment and pin or review dependency versions before use.

Risk: The skill expects network and file-write access for market-data retrieval and local outputs.

Mitigation: Run with least-privilege permissions and avoid elevated privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plato-1/skills/indicator-lab)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and tabular performance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the referenced backtest script and Python dependencies to be available in the execution environment.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
