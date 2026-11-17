## Description:

Microsoft Clarity (clarity.microsoft.com). Use this skill for ANY Microsoft Clarity request — reading, creating, and updating data. Whenever a task involves Microsoft Clarity, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to export recent Microsoft Clarity live insights through an OOMOL-connected account, using the connector's action schema to shape requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup runs remote installer payloads that have not been verified and may affect other installed agent skills.

Mitigation: Review and approve CLI setup separately, use a verified fixed release, and disable unwanted skill synchronization with OO_SKILLS_SYNC_DISABLED.

## Reference(s):

- [Microsoft Clarity](https://clarity.microsoft.com)
- [Clarity Data Export API documentation](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-data-export-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector requests depend on the live action schema and the user's connected Microsoft Clarity account.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
