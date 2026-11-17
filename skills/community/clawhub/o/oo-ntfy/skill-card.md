## Description:

Operate ntfy through an OOMOL-connected account to retrieve account details or publish notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using ntfy through an OOMOL-connected account can retrieve account profile, limits, and usage, or publish a notification to a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI setup may run downloaded installers and synchronize changes across agents' skills.

Mitigation: Review the installation steps first; use OO_SKILLS_SYNC_DISABLED to disable startup skill synchronization when appropriate.

Risk: Publishing sends a notification to the selected ntfy topic.

Mitigation: Confirm the destination and message before publishing.

## Reference(s):

- [ntfy](https://ntfy.sh)
- [ntfy publishing documentation](https://docs.ntfy.sh/publish/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and shell commands, with connector responses in JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
