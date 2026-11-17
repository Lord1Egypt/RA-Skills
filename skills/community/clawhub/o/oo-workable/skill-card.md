## Description:

Workable (workable.com). Use this skill for ANY Workable request — searching and reading data. Whenever a task involves Workable, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and recruiting teams can use this skill to search and read candidate and job information from a connected Workable account. It provides read-only access to candidate and job details and lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded installer code whose full effects have not been verified.

Mitigation: Review and version-pin the oo CLI, and require approval before running any downloaded installer.

Risk: Using the connected account involves OOMOL handling Workable credentials and candidate data.

Mitigation: Confirm that OOMOL is permitted to handle this account's credentials and candidate data before use.

Risk: The CLI may synchronize skills at startup.

Mitigation: If that behavior is unwanted, disable it with OO_SKILLS_SYNC_DISABLED=1.

## Reference(s):

- [Workable](https://www.workable.com/)
- [Workable API documentation](https://workable.readme.io/reference/generate-an-access-token)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Workable candidate and job records returned as JSON and presented as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only candidate and job data; fields depend on the selected Workable action.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
