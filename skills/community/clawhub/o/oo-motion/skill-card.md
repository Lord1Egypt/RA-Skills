## Description:

Use Motion to read, create, update, and delete data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Motion account can ask an agent to read and manage Motion tasks and projects, including creating, updating, and deleting tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code, and installer contents were not verified.

Mitigation: Install a verified CLI release yourself and approve its lasting changes.

Risk: Automatic agent-skill synchronization can introduce broader changes without clear user control.

Mitigation: Disable automatic agent-skill synchronization unless intended.

Risk: OOMOL mediates Motion access, and remote connector behavior was not verified.

Mitigation: Connect only the Motion account you intend to use.

## Reference(s):

- [Motion API documentation](https://docs.usemotion.com/)
- [Motion homepage](https://www.usemotion.com/)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Structured Motion connector requests and JSON responses, with setup guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Motion data; deleting a task is destructive.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
