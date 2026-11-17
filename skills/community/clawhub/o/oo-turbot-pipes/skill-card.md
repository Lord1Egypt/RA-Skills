## Description:

Use an OOMOL-connected Turbot Pipes account to run read-only SQL queries and retrieve rows with query metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query and read Turbot Pipes data through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute downloaded CLI code without a clear user checkpoint; the external installers and live connector were not verified.

Mitigation: Review and approve CLI installation separately, verify a specific release, and check whether automatic skill synchronization is acceptable.

## Reference(s):

- [Turbot Pipes API documentation](https://turbot.com/pipes/docs/reference/api)
- [Turbot Pipes](https://turbot.com/pipes)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON rows and query metadata, with any necessary text explanation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query inputs follow the live action schema; results include rows and query metadata.]

## Skill Version(s):

1.0.4 (source: artifact frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
