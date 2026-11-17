## Description:

Search and read JumpCloud data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

IT administrators can list JumpCloud systems and system users or retrieve individual records by ID through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can run unverified remote code and make broader agent changes without clear user control.

Mitigation: Review setup first, install a verified oo CLI release manually, require approval before installing software, and consider disabling automatic skill synchronization.

Risk: A connected JumpCloud account's credentials and data are handled by OOMOL.

Mitigation: Connect a minimally privileged JumpCloud account only if you accept OOMOL handling its credentials and data.

## Reference(s):

- [JumpCloud API documentation](https://docs.jumpcloud.com/api/1.0/index.html)
- [JumpCloud](https://jumpcloud.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [JumpCloud connection setup](https://console.oomol.com/connections/jumpcloud)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-jumpcloud)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data with Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only system and system-user lookups; available data depends on the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
