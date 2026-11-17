## Description:

Manage Plane.so projects and work items using a zero-dependency Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiseduardoaugusto](https://clawhub.ai/user/luiseduardoaugusto)

### License/Terms of Use:

MIT

## Use Case:

Developers and project teams use this skill to inspect Plane.so workspace data and propose or run CLI commands for listing projects, creating and updating issues, assigning work, adding comments, and searching work items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change or delete Plane.so project data.

Mitigation: Use a scoped Plane.so API token where possible and confirm project, issue, update, and delete targets before executing commands.

Risk: The inspected package did not contain the bundled CLI executable/source it claims to provide.

Mitigation: Verify the installed package includes the intended plane-so-cli executable/source before relying on the skill.

## Reference(s):

- [Plane.so CLI homepage](https://github.com/luiseduardoaugusto/plane-so-cli)
- [Plane.so](https://plane.so)
- [ClawHub skill page](https://clawhub.ai/luiseduardoaugusto/skills/plane-so-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require PLANE_API_KEY, PLANE_WORKSPACE, python3, and internet access to the Plane.so API.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
