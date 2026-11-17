## Description:

Use this skill to read, create, and update Teamcamp data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using Teamcamp through OOMOL can retrieve project, task, user, and customer information, and post comments on tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup can execute downloaded software whose contents and full local effects were not verified.

Mitigation: Review the oo CLI separately and require approval before running its installer.

Risk: Task comments change Teamcamp data.

Mitigation: Confirm before posting a task comment.

## Reference(s):

- [Teamcamp](https://www.teamcamp.app)
- [Teamcamp API reference](https://api.teamcamp.app/api-reference/introduction)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses include Teamcamp action data and execution metadata.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
