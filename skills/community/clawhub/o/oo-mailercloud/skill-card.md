## Description:

Use the oo CLI to create Mailercloud contacts and lists, and to list, create, update, or delete contact properties.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use the skill to manage Mailercloud contacts, recipient lists, and contact properties through an OOMOL-connected account. It supports these tasks with approval checks for changes and deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute remote installer code whose source and exact runtime release are unverified.

Mitigation: Review and approve a verified CLI installation before use; confirm the installer and runtime release before proceeding.

Risk: Automatic installation or synchronization may introduce undisclosed changes to other agent skills.

Mitigation: Review these changes and disable automatic skill installation or synchronization when they are not needed.

Risk: Connector actions can create, update, or delete Mailercloud data.

Mitigation: Keep account permissions limited and confirm the exact payload and effect before writes; explicitly approve the target before deletions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Mailercloud website](https://www.mailercloud.com/)
- [Mailercloud API documentation](https://apidoc.mailercloud.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [Mailercloud connector responses as JSON, with shell command instructions and task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector actions may read or change Mailercloud data; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
