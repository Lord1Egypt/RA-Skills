## Description:

Use ConfigCat through an OOMOL-connected account to find and read products, configurations, environments, feature flags, settings, and setting values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect ConfigCat products, configurations, environments, feature flags, settings, and setting values through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup includes installing the oo CLI through a remote installer; the scanner notes that downloaded code may execute without separate approval, though no malicious behavior was established.

Mitigation: Preinstall a vetted CLI version and require approval before downloaded code executes.

Risk: The CLI may automatically synchronize skills, and ConfigCat data passes through OOMOL as disclosed.

Mitigation: Check the CLI's automatic skill synchronization settings and connect ConfigCat with only the access needed.

## Reference(s):

- [ConfigCat](https://configcat.com/)
- [ConfigCat Public Management API documentation](https://configcat.com/docs/api/reference/configcat-public-management-api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ConfigCat ClawHub release](https://clawhub.ai/oomol/skills/oo-configcat)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Text responses and structured data returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only ConfigCat information; responses depend on the connected account's access.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
