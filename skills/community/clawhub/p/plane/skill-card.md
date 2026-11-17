## Description:

Manage Plane.so projects and work items using the plane CLI, including projects, issues, cycles, modules, comments, and member assignment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaguilera-jinko](https://clawhub.ai/user/vaguilera-jinko)

### License/Terms of Use:


## Use Case:

Developers, operators, and project teams use this skill to manage Plane.so workspace projects and work items from an agent-assisted CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads a remote executable without evidence of pinning or checksum verification.

Mitigation: Review the installer before use, prefer a pinned reviewed release, and verify a checksum or signature when available.

Risk: A Plane API token can change or delete workspace data through the CLI.

Mitigation: Use a least-privilege Plane token and avoid deletion or admin-scoped tokens unless the workflow requires them.

Risk: Issue deletion may be difficult or impossible to reverse.

Mitigation: Review destructive commands before execution and treat delete operations as final.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vaguilera-jinko/skills/plane)
- [Plane.so](https://plane.so)
- [Plane skill repository](https://github.com/JinkoLLC/plane-skill)
- [Plane CLI installer script](https://raw.githubusercontent.com/JinkoLLC/plane-skill/main/scripts/plane)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional Plane CLI table or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a plane executable plus PLANE_API_KEY and PLANE_WORKSPACE environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
