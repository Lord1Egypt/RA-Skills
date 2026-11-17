## Description:

Search and read Lucid SCIM user, group, and service-provider configuration data through the connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Lucid administrators and developers can use the skill to look up users, groups, and service-provider configuration in a connected Lucid SCIM account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can automatically run downloaded, unverified CLI installers.

Mitigation: Install and verify the oo CLI yourself, prevent automatic installer execution, and review its bundled-skill installation behavior and the Lucid account access it receives.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Lucid SCIM](https://lucid.co)
- [Lucid SCIM API documentation](https://developer.lucid.co/reference/overview-scim)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only user, group, and service-provider configuration data; available fields depend on each action's schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
