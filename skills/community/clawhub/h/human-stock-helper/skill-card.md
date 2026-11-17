## Description:

Human Stock Helper supports stock traders with rational analysis, technical calculations, and strategy execution reminders using AKShare, yfinance, pandas, and pandas-ta.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxhou-infinity](https://clawhub.ai/user/maxhou-infinity)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to analyze A-share, Hong Kong, and U.S. stock positions, calculate take-profit and stop-loss levels, manage position records, and review whether executed trades matched a planned strategy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Portfolio and trade history can be stored in plaintext in a hard-coded local path.

Mitigation: Review the storage behavior before installing, change the path to a private application directory, and avoid recording real positions until local storage is configured appropriately.

Risk: Holdings, account-like details, or trading plans may be sent to third-party search or research tools if those workflows are used.

Mitigation: Do not submit sensitive portfolio details to third-party tools unless the user consents to that processing.

Risk: Buy, sell, take-profit, and stop-loss outputs may be mistaken for professional financial advice.

Mitigation: Treat outputs as non-professional analysis and require human review before making trading decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maxhou-infinity/skills/human-stock-helper)
- [Example A-share case study](examples/case-study-600089.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, command-line guidance, and JSON analysis records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local JSON files for portfolio, trade, strategy, and execution records when the helper scripts are used.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
