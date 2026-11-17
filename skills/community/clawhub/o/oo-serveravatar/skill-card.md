## Description:

Use ServerAvatar through an OOMOL-connected account to search and read organization, application, database, and server data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

ServerAvatar account administrators use this skill to inspect organizations, applications, databases, and managed servers through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI software whose exact behavior was unavailable for inspection.

Mitigation: Review and approve the installer and selected CLI release before installation.

Risk: The CLI may automatically synchronize changes to installed agent skills.

Mitigation: Review the synchronization behavior and its documented OO_SKILLS_SYNC_DISABLED control before first use.

Risk: Queries can expose data available to the connected ServerAvatar account.

Mitigation: Connect only an account with the permissions needed for the requested reads.

## Reference(s):

- [ServerAvatar homepage](https://serveravatar.com/)
- [ServerAvatar API documentation](https://serveravatar.com/api-docs/api-console.html)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands and JSON action results summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only queries; available results depend on the connected ServerAvatar account and action schemas.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
