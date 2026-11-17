## Description:

GitLab (gitlab.com). Use this skill for ANY GitLab request — reading, creating, updating, and deleting data. Whenever a task involves GitLab, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to read and manage GitLab projects, issues, merge requests, and comments through their connected GitLab account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute unverified downloads and change other agents’ installed skills without disclosure.

Mitigation: Install a verified CLI yourself, review its automatic skill synchronization, use narrowly scoped GitLab permissions, and require approval for writes and deletions.

## Reference(s):

- [oo CLI project (linked from the skill)](https://github.com/oomol-lab/oo-cli)
- [GitLab](https://gitlab.com)
- [GitLab REST API authentication documentation](https://docs.gitlab.com/api/rest/authentication/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action results and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and deletion actions require user confirmation.]

## Skill Version(s):

1.0.8 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
