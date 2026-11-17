## Description:

商机跟进官 is a sales pipeline operating skill that reviews CRM exports, spreadsheets, follow-up queues, and deal notes to identify stale opportunities, overdue next steps, stage bottlenecks, close-risk accounts, and practical outreach to send next.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operators, founders, account executives, and revenue teams use this skill to turn CRM-like records, spreadsheets, inbox notes, or deal history into a prioritized follow-up plan. It highlights which opportunities to push today, which deals are going cold, where stages are bottlenecked, and what message or action should happen next.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive CRM, spreadsheet, inbox-note, or deal-history data.

Mitigation: Confirm the intended data sources before use and provide only the sales records needed for the review.

Risk: Drafted outreach could be inaccurate, off-tone, or not ready to send without human judgment.

Mitigation: Review and edit all generated follow-up messages before sending them to customers.

Risk: CRM updates, emails, messages, or reminders could affect live sales records or customer communications if connected tools are granted write access.

Mitigation: Do not grant CRM write or messaging permissions unless each action is explicit and user-confirmed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/harrylabsj/skills/pipeline-keeper)
- [Pipeline Signals](references/pipeline-signals.md)
- [Follow-Up Playbook](references/follow-up-playbook.md)
- [Output Modes](references/output-modes.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, text]

**Output Format:** [Markdown or plain text with prioritized lists, risk summaries, recommended actions, and drafted follow-up messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence labels when source quality is partial; drafted outreach should be reviewed before sending.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
