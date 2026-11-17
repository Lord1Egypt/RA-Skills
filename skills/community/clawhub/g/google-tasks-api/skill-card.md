## Description:

Helps agents read and manage Google Tasks lists and tasks through a connected Maton account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to list, create, update, move, and delete Google Tasks and task lists in an authorized account. Optional hosted functions and triggers can automate actions with separate user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Writes or new connections could affect the wrong Google account or tasks.

Mitigation: Confirm the target account and connection, resource, payload, and intended effect before any connection or write.

Risk: Hosted functions or trigger destinations can act or forward data continuously.

Mitigation: Obtain separate approval for persistent automation, verify destinations and data scope, and remove automations when no longer needed.

Risk: API-key authentication can expose a long-lived credential.

Mitigation: Prefer the Maton OAuth login flow and use API-key mode only when necessary.

## Reference(s):

- [Google Tasks API overview](https://developers.google.com/workspace/tasks)
- [Google Tasks tasks reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasks)
- [Google Tasks task lists reference](https://developers.google.com/workspace/tasks/reference/rest/v1/tasklists)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton homepage](https://maton.ai)
- [Time trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown with command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include task data from the connected account; automations may continue until disabled.]

## Skill Version(s):

1.2.5 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
