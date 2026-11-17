## Description:

Reconcile a Mercury missing-receipts CSV by searching connected Gmail accounts for original merchant receipt emails and forwarding valid matches to receipts@mercury.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srosro](https://clawhub.ai/user/srosro)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators who manage Mercury card-expense reconciliation use this skill to match missing-receipt transactions against connected Gmail accounts, forward valid original merchant receipts, and preserve a SQLite-backed audit trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches all connected Gmail accounts and forwards selected emails outside the inbox environment.

Mitigation: Confirm the intended Gmail account scope and verify that forwarded messages are original merchant receipts sent only to receipts@mercury.com.

Risk: The workflow stores financial transaction details, receipt candidates, search attempts, and forwarding records in /workspace/receipts.db and exported reports.

Mitigation: Treat the database and reports as sensitive financial records; restrict access and delete or protect them when no longer needed.

Risk: The skill is designed to run on a recurring schedule.

Mitigation: Review the OpenClaw cron cadence before enabling the skill and use the OpenClaw cron controls to pause, disable, or remove the job.

## Reference(s):

- [Receipt matcher workflow](references/workflow.md)
- [SQLite receipt reconciliation schema](references/schema.sql)
- [Plow private preview](https://plow.co/private-preview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown batch summaries, shell commands, SQLite state updates, and CSV status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May forward selected original merchant emails to receipts@mercury.com and write sensitive transaction, candidate, search, and forwarding records to /workspace/receipts.db.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
