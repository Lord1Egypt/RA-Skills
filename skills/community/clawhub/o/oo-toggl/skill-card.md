## Description:

Toggl Track (toggl.com). Use this skill for ANY Toggl Track request — reading, creating, updating, and deleting data. Whenever a task involves Toggl Track, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users can read, create, update, and delete Toggl Track data through their connected OOMOL account, including time entries, projects, tasks, tags, and workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: If the oo CLI is missing, setup may use a remote installer whose contents have not been verified.

Mitigation: Review and approve the installer separately before installing; require confirmation before writes or deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Toggl Track](https://toggl.com/track/)
- [Toggl Track API authentication documentation](https://engineering.toggl.com/docs/track/api/authentication/)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Guidance]

**Output Format:** [Structured Toggl Track data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Toggl Track account and requested action.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
