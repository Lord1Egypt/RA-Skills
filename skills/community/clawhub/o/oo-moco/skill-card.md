## Description:

MOCO (mocoapp.com). Use this skill for ANY MOCO request — searching and reading data. Whenever a task involves MOCO, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users with a connected MOCO account use this skill to retrieve company, contact, and profile information through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute a remote installer without a clear approval step.

Mitigation: Review and install a fixed CLI release separately before enabling the skill, and require approval for installation or changes to other agent skills.

Risk: The connected OOMOL account mediates access to MOCO data.

Mitigation: Review the permissions granted to the MOCO connection before using the skill.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [MOCO homepage](https://www.mocoapp.com)
- [MOCO API documentation](https://everii-group.github.io/mocoapp-api-docs/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with shell command and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
