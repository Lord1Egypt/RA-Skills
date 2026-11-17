## Description:

Plutus Pro analyzes bank or app CSV exports and raw expense text to categorize spending, compare budgets, flag tax categories, forecast spending, calculate savings rate, and export local reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway)

### License/Terms of Use:

MIT-0

## Use Case:

People managing personal or small-business finances use this skill to turn transaction exports or pasted expense lines into categorized spend summaries, budget comparisons, forecasts, tax-deductible flags, and savings-rate/P&L reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes detailed financial reports into the current working directory.

Mitigation: Run it only in a private folder and review generated Markdown, CSV, and JSON files before sharing, syncing, or committing them.

Risk: The documented setup uses a system pip install command with --break-system-packages.

Mitigation: Use an isolated Python virtual environment for dependencies when possible.

Risk: The skill processes personal financial transaction data.

Mitigation: Use local files carefully, avoid shared directories, and remove sensitive report outputs when they are no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/occupythemilkyway/skills/plutus-pro)
- [Publisher Profile](https://clawhub.ai/user/occupythemilkyway)
- [Skill Homepage](https://clawhub.ai/occupythemilkyway/plutus-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, JSON, Code, Shell commands, Configuration]

**Output Format:** [Console text plus Markdown, CSV, and JSON report files; setup guidance includes shell and Python code blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes plutus_pro_report_<period>.md, plutus_pro_summary_<period>.csv, and plutus_pro_data_<period>.json into the working directory.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
