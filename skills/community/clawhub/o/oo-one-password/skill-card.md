## Description:

Provides agent access to search and read 1Password vault, item, health, and activity data through OOMOL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users can use the agent to inspect connected 1Password vaults, items, health details, and activity records through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses an unpinned internet installer without a clear approval step.

Mitigation: Review the installer, use a reviewed fixed CLI release, and require approval for installation and skill changes.

Risk: Connected 1Password access is provided through OOMOL, and CLI synchronization settings may affect agent skills.

Mitigation: Limit the connected token to the vaults needed and review the CLI's automatic skill synchronization settings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-one-password)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [1Password](https://1password.com)
- [1Password Connect API reference](https://developer.1password.com/docs/connect/connect-api-reference/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured connector results with text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account data; available fields depend on the selected action and connected access token.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
