## Description:

Family Account Book 家庭财务记账 records household income, expenses, transfers, balances, and monthly summaries in a local SQLite account book.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silent404](https://clawhub.ai/user/silent404)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to maintain household financial records, including adding income or expense entries, checking account balances, producing monthly summaries, and recording transfers between accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change local household finance records.

Mitigation: Require explicit user confirmation before add, transfer, initialization, or account-affecting actions.

Risk: Natural-language account selection and fuzzy matching can post entries to the wrong account.

Mitigation: Prefer account IDs over fuzzy account names before writing transactions.

Risk: Finance records may become inaccurate if data is lost or transfers are only partially recorded.

Mitigation: Keep database backups and review transfer entries before relying on reports.

Risk: The current implementation is not suitable as an authoritative financial ledger.

Mitigation: Use it for household tracking only until amount validation, ledger scoping, and atomic transfer handling are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/silent404/skills/keep-accounts)
- [家庭财务数据库参考文档](artifact/references/finance.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and local SQLite query or update output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persistently create or update a local household finance SQLite database when the agent executes the provided commands.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
