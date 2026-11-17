## Description:

Use this skill for Plane requests to read, create, update, or delete data through the Plane connector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing work in Plane use this skill to retrieve projects and work items and to create, update, or delete work items through their connected Plane account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses downloaded installers that have not been verified, and the CLI may synchronize skill content beyond this integration.

Mitigation: Verify and install a trusted CLI release yourself, and consider setting OO_SKILLS_SYNC_DISABLED before invoking it.

Risk: Actions use the connected Plane account and can change work items.

Mitigation: Review the account permissions and confirm each requested change before running it.

## Reference(s):

- [Plane API documentation](https://developers.plane.so/api-reference/introduction)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Shell commands with JSON inputs and structured JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected Plane account; actions cover reading and managing Plane data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
