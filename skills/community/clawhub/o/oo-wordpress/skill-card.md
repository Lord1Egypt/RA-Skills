## Description:

Manage WordPress content through a connected OOMOL account, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to inspect and manage WordPress posts, pages, media, users, comments, categories, and tags through a connected WordPress account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may automatically run an unchecked remote installer when the oo CLI is missing.

Mitigation: Review and approve CLI installation separately, using a verified release where available.

Risk: WordPress changes are performed through the connected account and OOMOL service.

Mitigation: Connect a minimally privileged WordPress account, retain confirmation for changes, and consider disabling automatic skill synchronization with the documented OO_SKILLS_SYNC_DISABLED setting.

## Reference(s):

- [OO CLI project](https://github.com/oomol-lab/oo-cli)
- [OO CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [WordPress REST API documentation](https://developer.wordpress.org/rest-api/)
- [WordPress](https://wordpress.org)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON connector results with explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions may read or change WordPress data; write and destructive actions require confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
