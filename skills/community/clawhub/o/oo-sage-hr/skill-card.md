## Description:

Sage HR (sage.com). Use this skill for ANY Sage HR request — searching and reading data. Whenever a task involves Sage HR, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and authorized employees use the skill to search and read workforce records in Sage HR, including employee, position, team, termination, and time-off information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup can run downloaded software without a separate approval step.

Mitigation: Install a verified CLI release yourself and require approval before the agent runs downloaded installers.

Risk: Use involves employee data handled through OOMOL, and the remote installers and connector implementation could not be verified.

Mitigation: Review the setup and whether your organization permits OOMOL to handle employee data before use.

## Reference(s):

- [Sage HR](https://www.sage.com/en-us/sage-business-cloud/people/)
- [Sage HR API documentation](https://developer.sage.com/hr/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON responses with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-oriented Sage HR data returned through the connected account.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
