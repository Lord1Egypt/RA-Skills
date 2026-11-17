## Description:

Use CodeRabbit through an OOMOL-connected account to retrieve review metrics, users, roles, and audit logs, and to manage roles and seats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CodeRabbit organization administrators use this skill to retrieve review metrics, users, roles, and audit logs, and to manage roles and seats through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs the agent to run a remote installer without a separate approval check.

Mitigation: Install a reviewed oo CLI version yourself and require approval before any downloaded installer runs.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [CodeRabbit](https://www.coderabbit.ai)
- [CodeRabbit API documentation](https://docs.coderabbit.ai/api-reference)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON inputs and JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action results depend on the selected CodeRabbit connector action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
