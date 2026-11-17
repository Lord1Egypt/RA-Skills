## Description:

Operate Ninox through an OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Ninox users use the skill to inspect and manage workspaces, databases, tables, and records through a connected account. Write and delete actions require user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unverified remote code and may make broader agent changes that are not disclosed.

Mitigation: Review setup before installation, use a pinned and verified CLI release, and decide whether to disable automatic startup synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Ninox access can modify or delete data through the connected account.

Mitigation: Connect an appropriately scoped account and retain the skill's explicit approval requirements for writes and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Ninox API documentation](https://forum.ninox.com/t/83yzlg7/introduction-to-ninox-api)
- [Ninox](https://ninox.com)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Text with shell commands and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live connector schema to shape payloads; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
