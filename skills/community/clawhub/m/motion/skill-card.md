## Description:

Helps agents read and manage Motion tasks, projects, workspaces, and schedules through a user-authorized connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to ask an agent about scheduled work and, with explicit approval, create or update Motion tasks and projects. Optional automation can run an approved action on a schedule or supported external event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating or changing Motion data without the user's intent.

Mitigation: Default to reading data and obtain explicit approval for each write or delete and for new connections.

Risk: Hosted functions, triggers, and destinations can continue acting or forwarding data after setup.

Mitigation: Review their scope and destination with the user, obtain approval before creation or changes, and remove them when no longer needed.

Risk: Connected-account credentials can expose more data than a task requires.

Mitigation: Prefer OAuth over API keys and authorize only the scopes needed for the task.

## Reference(s):

- [Motion API documentation](https://docs.usemotion.com/)
- [Motion API reference](https://docs.usemotion.com/api-reference)
- [Maton](https://maton.ai)
- [Motion skill release](https://clawhub.ai/byungkyu/skills/motion)
- [Time trigger reference](artifact/references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown guidance with commands, code examples, and Motion task or schedule details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the permissions of the user's connected account.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
