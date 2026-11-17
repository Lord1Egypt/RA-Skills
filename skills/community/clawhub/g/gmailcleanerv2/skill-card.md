## Description:

Gmail email-management automation pack for reading and searching mail, organizing labels and messages, analyzing phishing, prompts, and tasks, drafting or sending replies, scheduling workflows, and reporting activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coorops25](https://clawhub.ai/user/coorops25)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect Gmail mailboxes, summarize and prioritize messages, manage labels and mailbox state, draft or send replies, schedule recurring checks, and produce reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is presented as an email reader but also includes mailbox-changing, sending, scheduling, and external AI-analysis behavior.

Mitigation: Review requested actions before execution, prefer read-only OAuth credentials for reader and reporting use, and use separate accounts or tokens before enabling organizer, responder, or scheduler workflows.

Risk: Gmail modify and compose scopes can alter mailbox state or send messages.

Mitigation: Avoid permanent delete and auto modes unless backups exist and the exact query, message IDs, and intended action have been reviewed.

Risk: Analyzer, responder, and summarizer behavior can send email content to Anthropic for analysis or drafting.

Mitigation: Confirm that email content is appropriate for external AI processing and redact sensitive content when possible before using AI-backed analysis or drafting.

Risk: Automated scheduler workflows can run recurring mailbox operations with reduced user review.

Mitigation: Run scheduled workflows in confirmation mode first, keep conservative query limits, and enable automatic cleanup only after reviewing the affected mailbox scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coorops25/skills/gmailcleanerv2)
- [ClawHub publisher profile](https://clawhub.ai/user/coorops25)
- [Gmail read-only OAuth scope](https://www.googleapis.com/auth/gmail.readonly)
- [Gmail modify OAuth scope](https://www.googleapis.com/auth/gmail.modify)
- [Gmail compose OAuth scope](https://www.googleapis.com/auth/gmail.compose)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Gmail message summaries, analysis JSON, draft text, audit logs, reports, and mailbox action commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
