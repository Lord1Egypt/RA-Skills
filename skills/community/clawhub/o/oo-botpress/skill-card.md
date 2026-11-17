## Description:

Search and read Botpress bots and workspaces through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Botpress workspace operators use the skill to list accessible workspaces and bots or retrieve details for a specific bot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can run downloaded installers whose full effects were not inspected and may make broader changes to installed agent skills.

Mitigation: Review the setup, install a reviewed and verified oo CLI release separately, and use OO_SKILLS_SYNC_DISABLED to prevent automatic skill synchronization where supported.

Risk: Connecting Botpress gives OOMOL account access and involves handling requested data.

Mitigation: Review the account and data access granted when connecting Botpress, and use an account with access appropriate to the requested work.

## Reference(s):

- [Botpress documentation](https://botpress.com/docs/)
- [Botpress homepage](https://botpress.com)
- [oo CLI repository (tool reference)](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON data, Text summaries]

**Output Format:** [Structured Botpress bot or workspace data, with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected account's access and available Botpress data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
