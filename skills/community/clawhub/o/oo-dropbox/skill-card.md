## Description:

Dropbox (dropbox.com). Use this skill for ANY Dropbox request — reading, creating, updating, and deleting data. Whenever a task involves Dropbox, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Dropbox account can use the skill to find and manage files, folders, shared links, members, and revisions through Dropbox actions. It also supports uploading, downloading, restoring, and other documented account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup directs the agent to execute remote installation code that the security evidence marks as unverified and lacking separate approval. Connecting Dropbox grants OOMOL account access, and downloads pass through transit storage with unspecified retention.

Mitigation: Review and approve CLI installation separately using a fixed, verified release, and check its skill-installation behavior before first use. Keep the documented approvals for writes and deletions; account for OOMOL access and unspecified transit-storage retention when connecting Dropbox.

## Reference(s):

- [Dropbox API documentation](https://www.dropbox.com/developers/documentation/http/documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files]

**Output Format:** [JSON action results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [File downloads may be returned through transit storage.]

## Skill Version(s):

1.0.8 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
