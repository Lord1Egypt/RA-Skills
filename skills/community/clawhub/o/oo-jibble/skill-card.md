## Description:

Jibble (jibble.io). Use this skill for ANY Jibble request — reading, creating, updating, and deleting data. Whenever a task involves Jibble, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to read Jibble organizations, members, and work locations, or to create, update, archive, and delete work locations through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI installer code whose full local effects have not been verified.

Mitigation: Review setup before installation, independently verify the CLI, check its automatic skill-installation behavior, and limit changes to intended agents.

Risk: The OOMOL connection mediates access to the connected Jibble account, and write or destructive actions can change or remove account data.

Mitigation: Review the live action schema and exact payload, then obtain confirmation before running write or destructive actions.

## Reference(s):

- [Jibble](https://www.jibble.io)
- [Jibble API documentation](https://docs.api.jibble.io/)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that write or delete Jibble data are identified and require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
