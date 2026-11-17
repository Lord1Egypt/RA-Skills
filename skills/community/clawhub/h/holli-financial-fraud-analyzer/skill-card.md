## Description:

Financial Fraud Analyzer Lite helps agents screen financial statements for earnings manipulation and accounting fraud risk using Beneish M-Score, Dechow F-Score, cash-flow checks, and structured evidence summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollis9087](https://clawhub.ai/user/hollis9087)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to screen company financial statements for manipulation risk and generate cautious low, medium, or high risk findings with supporting tables and follow-up checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users could treat a model score or risk label as proof of financial fraud.

Mitigation: Frame every result as risk screening, include data limitations, and require corroborating disclosure, audit, governance, and cash-flow evidence before action.

Risk: Formula, threshold, or input-data mismatches could produce misleading company risk rankings.

Mitigation: Verify formulas, thresholds, financial-statement mappings, and local data paths before relying on outputs.

Risk: The workflow is Chinese-first and includes sample China equities data, which may not match all users' reporting regimes or terminology.

Mitigation: Confirm accounting standards, period alignment, translations, and jurisdiction-specific reporting conventions before comparing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hollis9087/skills/holli-financial-fraud-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown analysis with tables, risk labels, limitations, and optional JSON calculation output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are screening signals, not determinations of fraud.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
