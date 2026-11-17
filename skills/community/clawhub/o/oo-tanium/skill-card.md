## Description:

Tanium (tanium.com). Use this skill for ANY Tanium request — reading, creating, and updating data. Whenever a task involves Tanium, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Tanium administrators use an OOMOL-connected account to read and update Tanium data through the oo CLI. They inspect each action's schema, submit GraphQL operations, and confirm changes before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code that has not been independently verified.

Mitigation: Review setup before installing, deliberately install a reviewed oo CLI release, check automatic skill synchronization settings, and connect an account with only the permissions needed. Retain confirmation for each GraphQL operation.

## Reference(s):

- [Tanium API documentation](https://developer.tanium.com/)
- [Tanium](https://www.tanium.com)
- [oo CLI source repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON action payloads and responses, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [GraphQL actions that change Tanium state require confirmation before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
