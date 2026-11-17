## Description:

Builder.io (builder.io). Use this skill for ANY Builder.io request — reading, creating, updating, and deleting data. Whenever a task involves Builder.io, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to read, create, update, and delete Builder.io content through their connected account. It guides the agent to check each action's input schema and to get confirmation before changes or deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions direct the agent to execute remote installer code without a separate approval step.

Mitigation: Review setup behavior first and use a separately approved, verified CLI installation; review or disable automatic agent-skill synchronization using the publisher's documented controls.

Risk: The connected Builder.io account may have broader access than the requested task needs.

Mitigation: Connect only the intended account and permissions, and keep user confirmation for content changes and deletion.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Builder.io Content API documentation](https://www.builder.io/c/docs/content-api)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Shell command instructions, JSON request payloads, and API response data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read content or propose content changes; write and delete actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
