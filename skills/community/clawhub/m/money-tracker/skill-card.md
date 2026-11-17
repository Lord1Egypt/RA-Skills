## Description:

Personal Money Tracker Pro helps an agent manage local SQLite bookkeeping from Chinese natural-language requests, including recording, querying, updating, deleting, categorizing, account balance checks, recurring transactions, and period reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanmwx](https://clawhub.ai/user/seanmwx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance agents use this skill to turn Chinese bookkeeping requests into local SQLite operations for transactions, categories, wallet accounts, balances, recurring schedules, and spending or income reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can permanently alter financial records through delete, delete-latest, update, and account-currency changes.

Mitigation: Ask the agent to preview and confirm destructive or rewriting actions before execution, and keep a backup of the SQLite database when records matter for audits or recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanmwx/skills/money-tracker)
- [Publisher profile](https://clawhub.ai/user/seanmwx)
- [commands.md](references/commands.md)
- [intent_mapping.md](references/intent_mapping.md)
- [chat_reference.md](references/chat_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands; the bundled script emits JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database; day, week, month, and year reports show raw stored amounts without FX conversion.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
