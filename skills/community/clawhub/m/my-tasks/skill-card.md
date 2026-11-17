## Description:

View a user's authenticated OpenAnt task history and status, including created, assigned, submitted, active, and completed tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

OpenAnt users use this skill to query their own task involvement, including work they completed, current assignments, submissions awaiting review, and tasks they created.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose personal OpenAnt task metadata in agent responses.

Mitigation: Install only when the user wants authenticated task-history queries, and verify authentication before running task commands.

Risk: Unauthenticated sessions return errors instead of task data.

Mitigation: Run openant status --json first and direct the user to authenticate before any --mine query if authentication is missing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses based on structured JSON returned by read-only OpenAnt CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an authenticated OpenAnt session and appends --json to task-query commands.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
