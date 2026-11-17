## Description:

Guides agents through user-approved Lemlist campaign, lead, schedule, activity, and unsubscribe tasks using a Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations users can ask an agent to read Lemlist data and, with approval, manage campaigns, leads, schedules, and unsubscribes. User-approved hosted functions and triggers can automate selected tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writes or new connections can change outreach data or expand account access.

Mitigation: Start with read-only requests and confirm each write or new connection with the user; authorize only the needed scopes.

Risk: Hosted functions, triggers, and destinations can continue acting on business data after the immediate task.

Mitigation: Review and approve each automation and destination before enabling it, then remove unused functions and triggers.

Risk: Direct API calls with a long-lived key can expose credentials.

Mitigation: Prefer OAuth through the Maton CLI; if direct API access is necessary, keep the key out of logs, command lines, and committed files.

## Reference(s):

- [Lemlist API reference](https://developer.lemlist.com/api-reference)
- [Maton documentation](https://docs.maton.ai)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with inline shell and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Maton account and network access; actions depend on the user's authorized Lemlist connection.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence; artifact metadata lists 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
