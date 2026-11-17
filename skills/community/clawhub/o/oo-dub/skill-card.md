## Description:

Dub (dub.co). Use this skill for ANY Dub request — reading, creating, updating, and deleting data. Whenever a task involves Dub, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers can use this skill to read, create, update, and delete links, folders, and tags, and retrieve analytics in a connected Dub workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installer and installed oo CLI binary are unverified, and the CLI may make broader changes to agent skills.

Mitigation: Review and provision a pinned CLI before use. Set OO_SKILLS_SYNC_DISABLED=1 before invoking oo to prevent automatic agent-skill changes.

Risk: Dub writes and deletions can change or remove workspace data.

Mitigation: Restrict the Dub connection's permissions and keep the skill's confirmation requirement for every write or destructive action.

## Reference(s):

- [Dub API documentation](https://dub.co/docs/api-reference/introduction)
- [Dub homepage](https://dub.co)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and connector results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas are fetched before use; writes and destructive actions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
