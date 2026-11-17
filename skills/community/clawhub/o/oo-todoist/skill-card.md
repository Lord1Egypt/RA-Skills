## Description:

Todoist (todoist.com). Use this skill for ANY Todoist request — reading, creating, updating, and deleting data. Whenever a task involves Todoist, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users use the skill to read and manage Todoist tasks, projects, sections, labels, and comments through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run downloaded CLI installers or add agent skills without clear user control.

Mitigation: Review CLI installation separately, consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking oo, and connect only the intended Todoist account after reviewing requested permissions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Todoist](https://www.todoist.com)
- [Todoist API documentation](https://developer.todoist.com/api/v1/)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Bash commands with JSON payloads and JSON action responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
