## Description:

Karakeep (karakeep.app). Use this skill for ANY Karakeep request — reading, creating, updating, and deleting data. Whenever a task involves Karakeep, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Karakeep bookmarks, lists, tags, feeds, highlights, backups, and assets through their OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installer and connector code were not inspected, and setup can execute remote code or introduce broader agent changes.

Mitigation: Review the installer before setup; where appropriate, use a reviewed CLI version with OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: Administrative Karakeep actions can affect other users or instance-wide data.

Mitigation: Use a non-admin connection unless administration is needed, and follow the skill's confirmation requirements for write and destructive actions.

## Reference(s):

- [Karakeep](https://karakeep.app)
- [Karakeep API documentation](https://docs.karakeep.app/api/karakeep-api)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-karakeep)
- [CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and structured connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change Karakeep data; write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
