## Description:

Expense Tracker lets an agent log, categorize, query, and report personal expenses locally from natural-language spending statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicholasrae](https://clawhub.ai/user/nicholasrae)

### License/Terms of Use:

MIT

## Use Case:

External users use this skill to maintain a local personal expense ledger, check spending against editable monthly budgets, and generate weekly or monthly spending reports through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, edit, and delete entries in its local expense ledger.

Mitigation: Keep backups of expenses/ledger.json and confirm delete or correction requests before allowing the agent to update the ledger.

Risk: The local ledger may contain sensitive personal financial details.

Mitigation: Store the skill and its expenses/ledger.json file only in locations appropriate for personal financial data.

## Reference(s):

- [Expense Tracker ClawHub listing](https://clawhub.ai/nicholasrae/skills/nicholasrae-expense-tracker)
- [Category definitions](references/categories.json)
- [Budget defaults](references/budgets.json)
- [Weekly report template](templates/weekly-report.md)
- [Monthly report template](templates/monthly-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON, configuration, guidance]

**Output Format:** [Conversational text, Markdown reports, shell command invocations, and JSON ledger updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and edits expense data in a local expenses/ledger.json file; requires bash, jq, and bc.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
