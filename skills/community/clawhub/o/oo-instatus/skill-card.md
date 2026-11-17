## Description:

Use the connected Instatus account to read, create, update, or delete status pages, components, incidents, and incident updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and status page operators use the connected Instatus account to inspect status pages and manage components, incidents, and incident updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes remote installers whose contents and exact release behavior are unverified.

Mitigation: Review and approve CLI installation separately, and use a verified, fixed release.

Risk: Broader agent-skill changes from startup synchronization are not disclosed in the artifact.

Mitigation: Review the synchronization behavior; set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Create and update actions change Instatus data, and delete actions remove data.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for destructive actions.

## Reference(s):

- [Instatus API documentation](https://instatus.com/help/api)
- [Instatus homepage](https://instatus.com)
- [oo CLI command reference: environment variables](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub Instatus release](https://clawhub.ai/oomol/skills/oo-instatus)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Shell commands]

**Output Format:** [JSON connector responses with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the connected Instatus account and the selected action.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
