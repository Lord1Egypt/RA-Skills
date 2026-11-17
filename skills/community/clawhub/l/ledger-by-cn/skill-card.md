## Description:

A Chinese-localized personal ledger and account management skill for recording transactions, managing multiple ledgers, summarizing balances, generating charts, and producing Markdown-friendly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[victor233k](https://clawhub.ai/user/victor233k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create local SQLite-backed personal ledgers, add income and expense transactions, inspect monthly summaries and trends, and produce command-line or Markdown reports for Chinese-language bookkeeping workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe ledger-name path handling that could expose or modify financial data unexpectedly.

Mitigation: Use trusted ledger names, avoid path-like ledger names, and prefer a release that validates ledger paths before writing files.

Risk: The security review notes broad triggers and overstated export or sync claims.

Mitigation: Review requested ledger actions before execution and do not rely on Feishu or CSV sync behavior unless the implementation and consent controls are confirmed.

Risk: The skill stores financial records on local disk.

Mitigation: Install only where local storage of personal financial data is acceptable and restrict access to the ledger data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/victor233k/skills/ledger-by-cn)
- [SQLite ledger architecture outline](src/OUTLINE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown and command-line text with SQLite-backed file outputs such as charts or ledger databases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local ledger data under ~/.openclaw/skills_data/ledger/ and chart files when requested.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
