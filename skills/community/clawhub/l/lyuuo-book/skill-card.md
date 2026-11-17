## Description:

Helps agents manage personal bookkeeping by running local CLI commands to record income, expenses, transfers, budgets, accounts, imports, exports, and financial reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luo-jun-hub](https://clawhub.ai/user/luo-jun-hub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance agents use this skill to record personal income, expenses, transfers, budgets, and account balances in a local ledger, then summarize financial status and reports for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal financial records locally.

Mitigation: Use it only when the user is comfortable keeping this data on the local machine and understands where the ledger is stored.

Risk: The documented setup uses a global npm dependency install.

Mitigation: Prefer an isolated and pinned local dependency install before using the CLI.

Risk: Update, delete, import, and export commands can materially change or expose local financial data.

Mitigation: Confirm those actions with the user first and only import from or export to trusted local paths the user explicitly chooses.

## Reference(s):

- [Command Reference](references/commands.md)
- [ClawHub Skill Page](https://clawhub.ai/luo-jun-hub/skills/lyuuo-book)
- [Publisher Profile](https://clawhub.ai/user/luo-jun-hub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [JSON command results summarized as concise text or Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against SQLite; import and export commands may read from or write to user-selected local paths.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
