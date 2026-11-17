## Description:

Tracks commitments made on sales calls, closes them only when activity evidence confirms completion, and flags due or overdue commitments in Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales representatives and sales leaders use the agent to track dated promises from call logs, verify completion from activity records, and receive due or overdue follow-ups in Slack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Call-derived details, including customer promises, may be visible to people who should not see them if posted to an inappropriate Slack channel.

Mitigation: Use a designated internal channel whose membership is appropriate for the call details, and keep the post destination locked.

## Reference(s):

- [Next-step tracker source](https://github.com/getcargohq/gtm-skills/tree/main/next-step-tracker)
- [Nudge message format](references/nudge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Structured records]

**Output Format:** [Markdown Slack reminders with quoted commitments, due dates, owners, and source paths; commitment ledger records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most one Slack post per day, grouped by owner and limited to open commitments due today or earlier.]

## Skill Version(s):

0.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
