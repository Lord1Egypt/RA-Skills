## Description:

Integrates and tracks multi-platform passive income with categorization, trend analysis, AI forecasting, tax reports, and financial goal monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and developers with passive income streams use this skill to consolidate platform revenue, analyze trends, forecast future income, prepare tax reports, and track financial goals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live financial API keys could be exposed if pasted into Markdown configuration files that agents or source-control tools can read.

Mitigation: Use read-only, least-privilege credentials through a secrets manager or local environment variables, and do not commit or share credential-bearing Markdown.

Risk: Connected financial accounts may grant broader access than the income-tracking workflow requires.

Mitigation: Verify account scopes before syncing, prefer read-only access, and document revocation steps for every connected platform.

Risk: Local storage and backups may retain sensitive income and account data longer than intended.

Mitigation: Confirm encryption, backup, deletion, and recovery behavior before using real accounts or importing production financial records.

Risk: Forecasts, tax estimates, and generated reports may be incomplete or inaccurate.

Mitigation: Reconcile generated reports against source platform records and review tax outputs with qualified financial or tax guidance before filing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text reports with inline shell commands and optional CSV or PDF exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financial summaries, trend analysis, forecasts, tax-report preparation output, and goal-tracking status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
