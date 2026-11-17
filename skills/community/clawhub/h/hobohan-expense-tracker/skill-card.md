## Description:

Log daily expenses via check-in prompts; dedup, categorize, sync to local ledger and Google Sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hohobohan](https://clawhub.ai/user/hohobohan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal finance operators use this skill to capture daily spending through recurring check-ins, maintain local markdown ledger files, and sync expense rows to Google Sheets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring automation may continue collecting expense information after installation.

Mitigation: Confirm the cron jobs are desired before enabling the skill and document how to disable them.

Risk: Financial records are synced to a hardcoded Google Sheet using a local service-account credential.

Mitigation: Use the skill only with a Google Sheet and credential you control, and verify the destination before syncing any ledger data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hohobohan/skills/hobohan-expense-tracker)
- [Publisher Profile](https://clawhub.ai/user/hohobohan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown ledger entries, prompts, configuration guidance, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recurring check-in behavior and sync guidance for local ledger files and Google Sheets.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
