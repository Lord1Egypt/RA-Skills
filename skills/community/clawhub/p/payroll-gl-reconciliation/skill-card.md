## Description:

Reconcile payroll processor exports from Gusto, ADP, Paychex, and Rippling to general ledger journal entries, detect variances, and produce audit-ready reconciliation workpapers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill during monthly payroll close to map payroll processor exports to the chart of accounts, build draft payroll journal entries, compare expected entries to GL activity, and document variances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles highly sensitive payroll data.

Mitigation: Use it only in an approved secure workspace and avoid placing raw employee payroll data in logs or unnecessary prompts.

Risk: Generated workpapers may include a default preparer name.

Mitigation: Remove or replace the preparer name before sharing or filing client workpapers.

Risk: Generated journal entries may be incomplete or incorrect for the client's books.

Mitigation: Treat all journal entries as drafts and review account mapping, balances, and variances before posting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/payroll-gl-reconciliation)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, account mapping tables, reconciliation checks, and workpaper templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces draft journal entries, variance summaries, and audit workpapers that require human review before posting.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
