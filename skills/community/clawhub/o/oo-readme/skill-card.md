## Description:

ReadMe (readme.com). Use this skill for ANY ReadMe request — reading, creating, updating, and deleting data. Whenever a task involves ReadMe, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation teams can use this skill to search and manage ReadMe project content, including docs, categories, changelogs, custom pages, API specifications, and versions. It directs the agent to inspect each action's schema and to seek confirmation before writes or destructive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can install and update other agent skills without this skill explaining that behavior.

Mitigation: Review the CLI's broader installation effects and disable unwanted startup skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

Risk: The remote installers and deployed connector service remain unverified.

Mitigation: Use a reviewed installation, connect only the intended ReadMe account, and approve exact edits or deletions.

## Reference(s):

- [ReadMe API authentication documentation](https://docs.readme.com/main/reference/authentication)
- [oo CLI repository and documentation](https://github.com/oomol-lab/oo-cli)
- [oo CLI environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions and payload fields depend on the selected ReadMe operation; inspect its schema before building a payload.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
