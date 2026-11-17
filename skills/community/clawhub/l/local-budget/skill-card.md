## Description:

Local Budget analyzes exported bank and credit card CSV files locally, categorizes transactions, compares spending against user-defined budgets, and generates Markdown spending reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals, financial reviewers, and agents assisting them use this skill to process local bank exports, review transaction categories, and create budget-versus-actual reports without sending data to third-party APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive financial data may be stored in generated JSON and Markdown outputs.

Mitigation: Process only bank exports intended for local use and keep generated files in a private folder.

Risk: Untrusted transaction text can be written into generated Markdown reports.

Mitigation: Review CSV and JSON inputs before rendering reports, and keep remote content loading disabled in Markdown viewers such as Obsidian.

Risk: Suggested transaction categories may be incorrect.

Mitigation: Review low- and medium-confidence category assignments before relying on budget reports.

## Reference(s):

- [CSV Format Reference](artifact/references/csv-formats.md)
- [Spending Categories Reference](artifact/references/categories.md)
- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/local-budget)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON transaction files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local CSV inputs and optional budget JSON; generated reports may contain sensitive financial data.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
