## Description:

Keeper SCIM (keepersecurity.com). Use this skill for ANY Keeper SCIM request — searching and reading data. Whenever a task involves Keeper SCIM, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Administrators and support teams use this skill to retrieve Keeper SCIM user, group, and service-provider configuration data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup can execute remote code, and the CLI can modify installed agent skills without separate approval.

Mitigation: Review and approve installation separately using a verified release; set OO_SKILLS_SYNC_DISABLED=1 to prevent automatic skill synchronization.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Keeper Security](https://www.keepersecurity.com/)
- [Keeper SCIM API documentation](https://docs.keeper.io/enterprise-guide/user-and-team-provisioning/automated-provisioning-with-scim/using-scim-api-provisioning)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Structured Keeper SCIM records returned as JSON, with textual summaries when presented by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only user, group, and service-provider configuration lookups]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
