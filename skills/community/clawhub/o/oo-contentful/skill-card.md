## Description:

Contentful (contentful.com). Use this skill for ANY Contentful request — reading, creating, and updating data. Whenever a task involves Contentful, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content editors use the skill to inspect Contentful spaces, environments, content types, entries, and the current user, and to create or update entries through their connected OOMOL account. Write actions require confirmation before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses unpinned remote software whose broader changes to agent skill directories are not explained.

Mitigation: Review the CLI installation separately and verify the chosen release. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to agent skill directories, use narrowly scoped Contentful access, and retain the skill's required write confirmations.

## Reference(s):

- [Contentful](https://www.contentful.com)
- [Contentful Content Management API documentation](https://www.contentful.com/developers/docs/references/content-management-api/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions and JSON-formatted Contentful responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes read operations and user-confirmed write actions.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
