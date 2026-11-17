## Description:

Search and read KickoffLabs campaign data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operators use this skill to inspect available campaigns, lead statistics, and configured scoring actions in a connected KickoffLabs account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded CLI code that has not been verified.

Mitigation: Review the CLI setup and provision a verified CLI release yourself before enabling the skill.

Risk: Startup synchronization can make broader changes to other agent skills without clear user approval.

Mitigation: Decide whether to allow skill synchronization; set OO_SKILLS_SYNC_DISABLED=1 to disable it.

Risk: Connecting KickoffLabs entrusts OOMOL with account access.

Mitigation: Review and approve the account connection before using the skill.

## Reference(s):

- [KickoffLabs API documentation](https://support.kickofflabs.com/developer/common-api-behavior/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [KickoffLabs](https://kickofflabs.com/)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Structured campaign data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only campaign lists, lead statistics, and scoring action definitions.]

## Skill Version(s):

1.0.2 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
