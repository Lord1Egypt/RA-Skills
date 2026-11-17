## Description:

约面招聘协调虾 helps agents coordinate interview scheduling from candidate spreadsheets or natural-language requests by checking Feishu calendar availability, preparing confirmed meeting events, and drafting or sending interview emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and HR coordinators use this skill to process candidate interview batches, identify interviewer availability, confirm proposed slots, create Feishu video meeting events, and prepare candidate email invitations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback Feishu script handles powerful calendar credentials and stores a tenant token in a temporary cache.

Mitigation: Prefer the openclaw-lark OAuth plugin path, grant Feishu and SMTP permissions narrowly, and use the fallback script in shared environments only after moving the token cache to a private protected location or disabling it.

Risk: The skill can mutate real calendars and send interview communications to candidates.

Mitigation: Require explicit user confirmation before creating calendar events, adding attendees, or sending email invitations.

## Reference(s):

- [Feishu calendar API reference](references/feishu-calendar-api.md)
- [Interview invitation email templates](references/email-templates.md)
- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/interview-scheduler-claw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with optional bash commands, tool-call parameters, and email draft text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before calendar creation or email sending.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
