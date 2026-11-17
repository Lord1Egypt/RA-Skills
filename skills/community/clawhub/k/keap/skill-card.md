## Description:

Guides agents in managing Keap CRM records, marketing campaigns, and email through a Maton-authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

CRM and marketing teams use this skill to look up and manage Keap contacts, orders, opportunities, campaigns, and email through their authorized connection. Automation requires separately approved hosted functions and triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad account access or writes to the wrong Keap connection.

Mitigation: Use OAuth with the narrowest available scopes, verify the account and connection, and confirm each write before execution.

Risk: Emails, campaign enrollments, and deletions may reach people or cause irreversible changes.

Mitigation: Review recipients, content, records, and intended effects with the user before approval.

Risk: Hosted functions and triggers can continue acting or forward event data after setup.

Mitigation: Require separate approval for the function, trigger, and destination; inspect their access and destination before enabling them.

## Reference(s):

- [Keap skill on ClawHub](https://clawhub.ai/byungkyu/skills/keap)
- [Maton homepage](https://maton.ai)
- [Keap REST API V2 documentation](https://developer.infusionsoft.com/docs/restv2/)
- [Keap OAuth authentication](https://developer.infusionsoft.com/authentication/)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with CLI, API, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May handle personal and commercial account data; return only details needed for the task.]

## Skill Version(s):

1.2.6 (source: ClawHub server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
