## Description:

Provides machine-learning-assisted Double Color Ball lottery recommendations and backtesting using Random Forest, Gradient Boosting, feature engineering, and rule-based scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mumuli2021](https://clawhub.ai/user/mumuli2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate lottery number recommendations from a local OpenClaw SQLite lottery database and to run historical backtests. Outputs should be treated as entertainment-oriented analysis rather than reliable financial guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lottery recommendations can be mistaken for reliable financial guidance.

Mitigation: Present predictions as entertainment only and avoid using them as the basis for financial decisions.

Risk: The skill reads a local OpenClaw lottery SQLite database and backtests may write reports in the OpenClaw workspace.

Mitigation: Run in a controlled workspace with the intended database path and review generated reports before sharing them.

Risk: Python dependency hygiene issues may affect reproducibility or local environment safety.

Mitigation: Use a virtual environment and pinned versions for scikit-learn, numpy, and pandas.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mumuli2021/skills/lottery-predictor-v3-8)
- [Publisher profile](https://clawhub.ai/user/mumuli2021)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text with lottery recommendations and optional Markdown backtest reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local lottery history from SQLite and may write Markdown backtest reports in the OpenClaw workspace.]

## Skill Version(s):

3.8.0 (source: evidence.release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
